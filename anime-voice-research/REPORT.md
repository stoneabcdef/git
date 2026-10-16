# Custom Anime Character Voices for a Text-to-Speech HTTP API
### A research report for wiring an anime-character voice into a coding-agent plugin (Windows)
**Research date: 2026-10-14** · Research only — nothing was installed and no models were downloaded.

---

## 0. How to read this report (and a note on method)

**Verified** = I fetched the primary source myself and quote it. Every such claim carries the URL I actually fetched.
**Community/hearsay** = blog posts, tutorials, forum claims, aggregator sites. Treated as unverified.
**Unverified** = I could not confirm it and I say so explicitly rather than guessing.

**Network caveat (affects reproducibility):** From this environment, `github.com`, `raw.githubusercontent.com`, and `huggingface.co` were **DNS-blocked** ("resolves to a non-public IP address"). I reached primary sources through these working routes, and URLs in this report are given in their canonical form:

| Blocked | Working mirror/route I used |
|---|---|
| `github.com/<o>/<r>` (HTML) | `https://api.github.com/repos/<o>/<r>`, `https://ungh.cc/repos/<o>/<r>` |
| `raw.githubusercontent.com/...` | `https://ghproxy.net/https://raw.githubusercontent.com/<o>/<r>/<branch>/<path>` |
| `huggingface.co/...` | `https://hf-mirror.com/...` (mirror; includes `/api/models?search=` JSON API) |
| — | `https://www.modelscope.cn/...` (reachable directly) |

`web_search` was available but hit repeated HTTP 429 (concurrency) and then HTTP 402 (insufficient balance) on the search backend. I therefore relied on **direct primary-source fetches**, which is stronger evidence anyway. Bing's RSS endpoint (`cn.bing.com/search?q=...&format=rss`) worked but returned poor results for niche Japanese/Chinese queries — I flag the two topics where that limited me.

---

## 1. Executive summary

**The single most important technical finding:** **no mainstream open-source character-TTS engine ships an OpenAI-compatible `/v1/audio/speech` endpoint natively.** I read GPT-SoVITS's `api_v2.py` in full: it exposes `GET/POST /tts`, `/control`, `/set_gpt_weights`, `/set_sovits_weights`, `/set_refer_audio` — and nothing else. Style-Bert-VITS2 ships `server_fastapi.py` (OpenAPI docs at `/docs`). CosyVoice ships a FastAPI/gRPC server. Fish Speech ships `tools/api_server.py` with `/v1/tts` (msgpack body — *not* OpenAI-shaped). AivisSpeech Engine speaks the **VOICEVOX** API on port 10101.

So for a DSH voice plugin that POSTs to an OpenAI-compatible `/audio/speech`, you have exactly two clean options:

- **(A) Put a small adapter in front of a local engine**, or
- **(B) Use a hosted provider that is already OpenAI-compatible.**

Everything else in this report is about picking which engine sits behind that adapter.

### Recommendation

**🥇 Top recommendation — GPT-SoVITS locally on Windows, behind a ~50-line OpenAI-compatible adapter.**
It is the only option that combines all four of: permissive **MIT** license, an **official maintained one-click Windows package**, **5-second zero-shot** cloning *and* 1-minute fine-tuning, and a genuinely deep **community library of anime/game character models** (I verified concrete repos on HuggingFace). It covers Chinese + Japanese + English + Korean + Cantonese, and runs acceptably on **CPU** with a GPU optional. The cost is that you must write/run a tiny translation layer.

**🥈 Runner-up — SiliconFlow (硅基流动) hosted CosyVoice2-0.5B / IndexTTS-2.**
Natively OpenAI-compatible (the docs literally show `openai` SDK usage against `https://api.siliconflow.cn/v1`), supports **uploading your own reference audio to create a custom voice ID**, bills per UTF-8 byte, is fast, needs zero installation, and is **China-accessible**. Downside: custom voices require **实名认证** (real-name verification), and zero-shot fidelity on a specific anime character is below a purpose-fine-tuned local model.

**🥉 Strong dark horse for Japanese-only anime voices — AivisSpeech Engine + AivisHub.**
LGPL-3.0, free, **CPU-only friendly**, built explicitly for emotive Japanese character voices, and AivisHub is a curated model-sharing hub with a dedicated **"キャラクター（既存）"** (existing character) category on a proper license (**ACML**). It speaks the VOICEVOX API, not OpenAI's — so it also needs the adapter. **Japanese only** (verified).

**⚠️ Key correction to a common assumption:** people assume "GPT-SoVITS `api_v2.py` is basically OpenAI-compatible." It is not. Do not plan around that.

---

## 2. Feature-level comparison — open-source engines

| Engine | License (verified) | Cloning | zh | ja | VRAM / hardware | Windows | Ships an HTTP API? | OpenAI `/audio/speech`? |
|---|---|---|---|---|---|---|---|---|
| **GPT-SoVITS** | **MIT** ✅ | 5 s zero-shot; 1 min finetune | ✅ | ✅ | CPU works; RTF 0.028 @4060Ti | ✅ **official 1-click pkg** | ✅ `api_v2.py` | ❌ `/tts` only |
| **Style-Bert-VITS2** | AGPL-3.0 ✅ | **Training required** (2–14 s clips ×N) | ✅ | ✅ (best-in-class ja) | CPU inference OK; GPU needed to train | ✅ `sbv2.zip` 1-click | ✅ `server_fastapi.py` | ❌ |
| **IndexTTS-2.5** | **bilibili custom** ✅ | 1 reference clip, zero-shot | ✅ | ✅ | RTF 0.2065 @4090 (bf16) | ⚠️ needs `uv`; DeepSpeed hard | ⚠️ WebUI + vLLM recipe | ❌ |
| **CosyVoice 2 / 3** | **Apache-2.0** ✅ | zero-shot | ✅ | ✅ | 0.5B class | ⚠️ conda/uv scripts | ✅ FastAPI/gRPC | ❌ |
| **Fish Speech (S2-Pro/Drama 3)** | **Fish Audio Community License** ✅ (non-commercial ≤$500k) | 10–30 s | ✅ | ✅ | **24 GB** (S2-Pro) / **48 GB** (Drama 3) | ❌ **Linux/WSL only** | ✅ `/v1/tts` (msgpack) | ❌ |
| **F5-TTS** | **CC-BY-NC-4.0** weights ✅ | zero-shot | ✅ | ❌ native | ~0.3B | ⚠️ Python | Community Gradio | ❌ |
| **Chatterbox** | MIT (repo) ✅ | zero-shot, 10 s ref | ✅ | ✅ (23 langs) | Nano 110M **runs on CPU 3× realtime** | ⚠️ tested on Debian 11 | ❌ library only | ❌ |
| **XTTS-v2** | code MPL-2.0 ✅ / **weights CPML (non-commercial)** | 6 s | ✅ | ✅ | ~4 GB VRAM | ⚠️ | via `openedai-speech` | ✅ **yes, via wrapper** |
| **MegaTTS3** | unverified (README 500) | zero-shot | ✅ | ❌ | unverified | unverified | unverified | ❌ |
| **Kokoro-82M** | **Apache-2.0** ✅ | ❌ **none** | ✅ | ✅ | 82M, trivial | ✅ | via `Kokoro-FastAPI` | ✅ **yes** |
| **edge-tts** | GPL-3.0 wrapper ✅ | ❌ **none** | ✅ | ✅ | none (cloud) | ✅ | via `openai-edge-tts` | ✅ **yes** |

---

## 3. GPT-SoVITS (the deep dive)

**Repo:** https://github.com/RVC-Boss/GPT-SoVITS
Verified via `https://api.github.com/repos/RVC-Boss/GPT-SoVITS` (fetched 2026-10-14):
**License MIT** · **62,801 stars** · 6,704 forks · created 2024-01-14 · last push 2026-10-08 · 896 open issues.

### 3.1 How few-shot cloning works
From the README (fetched via the GitHub API readme endpoint):

> **"Zero-shot TTS:** Input a **5-second** vocal sample and experience instant text-to-speech conversion."
> **"Few-shot TTS:** Fine-tune the model with just **1 minute** of training data for improved voice similarity and realism."

So there are two distinct modes, and this matters for your architecture:
- **Zero-shot** — point at a ~5 s reference WAV + its transcript; *no training at all*. This is what makes "one reference clip per character → a voice" practical.
- **Few-shot fine-tune** — 1 minute of audio, yields noticeably higher similarity. Needs a GPU and ~an hour-ish of pipeline work (the repo's own tooling does slicing, denoising, ASR, and labelling).

**Cross-lingual** support is explicitly **English, Japanese, Korean, Cantonese, Chinese**.

### 3.2 Quality and latency
RTF ("real-time factor"; lower is faster) published in the README for **v2 ProPlus**:

> "0.028 tested in 4060Ti, 0.014 tested in 4090 (1400 words ≈ 4 min, inference time is 3.36s), **0.526 in M4 CPU**."

That RTF 0.526 on a Mac CPU is the concrete evidence that **CPU-only operation is genuinely viable** for synthesis (slow, but usable for short agent replies). Training, however, wants a GPU.

### 3.3 Hardware
**Verified:** the README's "Tested Environments" table covers Python 3.10–3.12, PyTorch 2.5.1–2.8.0dev, CUDA 11.8/12.4/12.8, **Apple silicon**, and **CPU** (Python 3.9 / PyTorch 2.2.2). `install.ps1` takes `--Device <CU126|CU128|CPU>`.
**Unverified:** the README does **not** publish a VRAM figure. Community reports cluster around "runs in ~4–6 GB VRAM, and on CPU" — treat the specific number as **hearsay**. The RTF numbers and the CPU row in the tested-environment table are the real, citable signals.

### 3.4 Maintained one-click Windows package — **YES**
This is a genuine differentiator. The README (Windows section) says:

> "If you are a Windows user (tested with win>=10), you can **download the integrated package** and double-click on `go-webui.bat` to start GPT-SoVITS-WebUI."

The integrated package lives at
**https://huggingface.co/lj1995/GPT-SoVITS-windows-package** (verified via `https://hf-mirror.com/api/models?search=GPT-SoVITS` → `lj1995/GPT-SoVITS-windows-package`, license MIT, 112 likes; and `lj1995/GPT-SoVITS`, the official pretrained repo, MIT, 427 likes).
Windows setup also needs `ffmpeg.exe` / `ffprobe.exe` placed in the repo root (or the packaged build handles it). Docker path: `hub.docker.com/r/xxxxrt666/gpt-sovits`, with `GPT-SoVITS-CU126`, `-CU128`, and `-Lite` variants.

### 3.5 The API server — **this is the critical part**
I read `api_v2.py` in full (via `https://ghproxy.net/https://raw.githubusercontent.com/RVC-Boss/GPT-SoVITS/main/api_v2.py`). Launch:

```
python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
```

**Endpoints (complete list):**
- `GET|POST /tts` → returns a WAV audio stream (HTTP 200) or JSON error (HTTP 400)
- `GET /control?command=restart|exit`
- `GET /set_gpt_weights?weights_path=...`
- `GET /set_sovits_weights?weights_path=...`
- `GET /set_refer_audio?refer_audio_path=...`

**`POST /tts` body fields** (from the source's own docstring and Pydantic model):
`text`(req), `text_lang`(req), `ref_audio_path`(req), `aux_ref_audio_paths`(opt — **multi-speaker tone fusion**), `prompt_text`(opt), `prompt_lang`(req), `top_k`=15, `top_p`=1, `temperature`=1, `text_split_method`=`cut5`, `batch_size`=1, `batch_threshold`=0.75, `split_bucket`=True, `speed_factor`=1.0, `fragment_interval`=0.3, `seed`=-1, `media_type`=`wav|raw|ogg|aac`, `streaming_mode` (0/1/2/3: 1=best quality slowest, 2=medium, 3=lower quality faster), `parallel_infer`=True, `use_cuda_graph`=True, `repetition_penalty`=1.35, `sample_steps`, `cfg_rate`, `super_sampling`, `overlap_length`=2, `min_chunk_length`=16.

**Three things worth flagging:**
1. **There is no `/v1/audio/speech`.** The endpoint is `/tts`, and the response is raw audio bytes, not base64 JSON.
2. **`ref_audio_path` is a path on the *server's* filesystem**, not an upload. (A POST file-upload variant exists in the source but is **commented out**.) So a per-character voice mapping is a **path → voice** mapping, not a blob upload.
3. **Runtime model switching IS supported** via `GET /set_gpt_weights` + `GET /set_sovits_weights`. This is a meaningful capability: one server process can host multiple fine-tuned character models and switch between them. Note this contradicts an older widely-cited wrapper's claim — see §3.7.

**Version history** (from README release notes): v2 added Korean + Cantonese and 5k-hour pretraining; v3 improved timbre similarity and emotion; v4 fixed metallic artifacts from non-integer upsampling and outputs native 48 kHz (author calls v4 a direct replacement for v3); **v2Pro** has slightly higher VRAM than v2 but surpasses v4's performance at v2's hardware cost; **v5** improves similarity *without* SoVITS fine-tuning, adds a new vocoder reducing high-frequency spectral mirroring, and supports `cuda_graph` + `flash_attention`.

⚠️ Important caveat straight from the README: *"For training sets with average audio quality, v1/v2/v2Pro can deliver decent results, but v3/v4 cannot."* And v3/v4's timbre leans toward the reference audio rather than the whole training set. **For messy anime-rip reference audio, prefer v2Pro or v5 over v3/v4.**

### 3.6 Community OpenAI-compatible wrappers
**Verified to exist** (metadata via `ungh.cc`):
- **`X-T-E-R/GPT-SoVITS-Inference` ("GSVI")** — https://github.com/X-T-E-R/GPT-SoVITS-Inference — 513 stars. Inference-specialised fork whose *whole point* is convenient character handling. I fetched its `api_doc.md`:
  - `GET /character_list` → JSON of characters and their emotions, e.g. `{"Hanabi": ["default","Normal","Yandere"], "Hutao": ["default"]}`
  - `GET|POST /tts?character=<name>&text=<text>` with optional `character`, `emotion`, `text_language`(auto|zh|en|ja), `batch_size`, `speed`, `top_k`, `top_p`, `temperature`, `stream`, `format`(WAV/MP3/OGG), `save_temp`
  - **Model folder convention — this is the key ergonomic win:** put `.ckpt` + `.pth` + a `.wav` whose *filename is the prompt text* into `trained/<CharacterName>/`, e.g. `trained/hutao/hutao-e75.ckpt`, `trained/hutao/hutao_e60_s3360.pth`, `trained/hutao/hutao said something.wav`. Then `character=hutao` just works.
  - Ships a **pre-packaged Windows distribution** (`XTer123/GSVI_prezip` on HF) and a model-management WebUI.
  - Still **not** OpenAI-shaped — it's `/tts?character=...`. But the character abstraction is exactly what a DSH plugin wants.
- **`jianchang512/gptsovits-api`** — https://github.com/jianchang512/gptsovits-api — 352 stars. I fetched its README. It wraps the *older* `api.py` (renamed `api2.py`), default port 9880, supports `-dr`(ref audio) `-dt`(ref transcript) `-dl`(zh|ja|en) `-s`(SoVITS) `-g`(GPT) `-d cpu|cuda|mps`, plus GET `?text=...&text_language=zh` and POST JSON with `refer_wav_path`/`prompt_text`/`prompt_language`/`text`/`text_language`. Only zh/ja/en.
  - ⚠️ **Its README states it does NOT support dynamic model switching and recommends one process per model on different ports.** That was true of the old `api.py`; the current upstream `api_v2.py` **does** expose `/set_gpt_weights` and `/set_sovits_weights`. **Verify against your installed version before architecting around multi-model switching.**
  - Last push 2024-03-07 — effectively unmaintained.

### 3.7 Where to get anime character voice models
I queried the HuggingFace API (`https://hf-mirror.com/api/models?search=GPT-SoVITS&limit=30`). **Verified to exist** — real repos, real license tags:

| Model | Character | License tag |
|---|---|---|
| `MomoyamaSawa/GPT-SoVITS_KusanagiNene` | 草薙寧々 (Project Sekai) — tags `pjsk`,`プロセカ`, zh/ja/en | gpl-3.0 |
| `Killuazyt/kurisu-gpt-sovits-v5turbo-20261012` | Kurisu (Steins;Gate), v5turbo + LoRA, created 2026-10-12 | (none) |
| `2DIPW/ATRI_GPT-SoVITS` | ATRI | cc-by-nc-sa-4.0 |
| `MondMeer/GPT-SoVITS-HiiragiHakua` | 柊白亜 | gpl-3.0 |
| `baicai1145/GPT-SoVITS-STAR` | (character set) | mit |
| `modelloosrvcc/Kotoko_Utsugi_GPT-SOVITS`, `modelloosrvcc/Nagisa_Shingetsu_GPT-SoVITS` | visual-novel characters | — |
| `shibing624/parrots-gpt-sovits-speaker-maimai` | まいまい | **cc-by-nc-4.0** |

Non-zero-shot-model sources: **ModelScope** (`https://www.modelscope.cn/models`, reachable) hosts the Chinese ecosystem's model zoo; the GPT-SoVITS README itself directs Chinese users to a Yuque-hosted mirror of all models (`yuyue.com/b...`) and to `XXXRT/GPT-SoVITS-Pretrained` on both HF and ModelScope.

**⚠️ Ethical/legal flag:** these are third-party finetunes of copyrighted characters made from copyrighted voice-actor performances. The license tag on the repo (e.g. `mit`) covers *the uploader's contribution* and does **not** clear the underlying character or performance rights. See §6.

---

## 4. Style-Bert-VITS2

**Repo:** https://github.com/litagin02/Style-Bert-VITS2
Verified via `https://api.github.com/repos/litagin02/Style-Bert-VITS2`: **AGPL-3.0** · 1,384 stars · 219 forks · created 2023-12-01 · last push 2025-12-07 · 84 open issues. It is a fork of `fishaudio/Bert-VITS2` (AGPL-3.0).

**Why it's interesting for anime specifically:** it is *the* Japanese-anime-style engine. Its README (fetched via `ghproxy.net`) describes it as built on Bert-VITS2 v2.1 + Japanese-Extra specifically to make **emotion and speaking style freely controllable with intensity**. And notably — v2.7.0 (2025-08-24) added **`litagin/anime-whisper`** as an ASR model, i.e. the project explicitly ships an anime-tuned recogniser for building datasets.

**Styles:** the README explains `style_vectors.npy` drives style. A default average style **"Neutral"** is generated during training; if you organise training audio into subfolders, one style per folder is generated automatically. Additional styles can be created any time from the "スタイル作成" tab (`StyleVectors.bat`) with an audio file — independently of training, and re-doable repeatedly.

**Adding a custom character model** requires **training**, not zero-shot:
> "学習には **2-14秒程度の音声ファイルが複数** と、それらの書き起こしデータが必要です。" — multiple 2–14-second audio files plus transcripts.
The workflow is: dataset creation tab (slice + auto-transcribe) → training tab. The README explicitly says **CPU can do inference without a GPU, but training needs an NVIDIA GPU**.

FAQ answer on dataset size (`docs/FAQ.md`, fetched): *"どのくらいの音声データが必要なの？ 分かりません。試行錯誤してください"* ("How much data? Unknown. Trial and error.") with a note that "a few minutes can work" and the RVC rule-of-thumb of **45 minutes being plenty**. On steps: timbre starts resembling around 2k–3k steps, and 5k–10k–15k feels good including emotion.

**Disk/VRAM:** the README requires **1.5 GB+ free RAM** for the engine (that figure is stated by the Aivis Project docs for the derived engine, and the SBV2 model structure is `config.json` + `*.safetensors` + `style_vectors.npy`). **I did not find a published VRAM number in the SBV2 README — unverified.**

**API server — verified:** `python server_fastapi.py`, with the OpenAPI spec at **`/docs`** after start. Default input cap is **100 characters**, changeable via `config.yml` → `server.limit` (`-1` = unlimited). CORS defaults to allow-all and the README explicitly asks you to restrict `server.origins`.

**Windows — verified and good:** download `sbv2.zip` from the releases page, then:
- `Install-Style-Bert-VITS2.bat` (GPU), or
- `Install-Style-Bert-VITS2-CPU.bat` (**CPU: inference + merge only, no training**), or
- `Update-Style-Bert-VITS2.bat`

Also `pip install style-bert-vits2` for inference-only library use. Verified environments: Windows cmd, WSL2, Linux (Ubuntu Desktop).

**Ready-made anime models on HuggingFace — verified** (`hf-mirror.com/api/models?search=style-bert-vits2`):

| Model | Notes | License |
|---|---|---|
| `litagin/style_bert_vits2_jvnv` | **Official.** 7 styles: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral | cc-by-sa-4.0 |
| `litagin/Style-Bert-VITS2-2.0-base-JP-Extra` | JP-Extra pretrained base | agpl-3.0 |
| `RikkaBotan/style_bert_vits2_jp_extra_sweet_original` | cute/childish ja voice, 129 dl | cc-by-sa-4.0 |
| `RikkaBotan/style_bert_vits2_jp_extra_cool_original` | 132 dl | cc-by-sa-4.0 |
| `RikkaBotan/style_bert_vits2_jp_extra_asmr_original` | 112 dl | cc-by-sa-4.0 |
| `RikkaBotan/style_bert_vits2_chinese_original` | 162 dl | cc-by-sa-4.0 |
| `ayousanz/tsukuyomi-chan-style-bert-vits2-model` | つくよみちゃん, **246 downloads** | other |
| `Mofa-Xingche/girl-style-bert-vits2-JPExtra-models` | mit | mit |
| `zgock/style-bert-vits2-zonoko-cc0` | **public domain** | **cc0-1.0** |
| `RinneAi/Rinne_Style-Bert-VITS2`, `Lycoris53/style-bert-vits2-sakura-miko`, `kaunista/style-bert-vits2-Anneli` | — | mixed |

**Its own terms-of-use is a model of good practice** — `docs/TERMS_OF_USE.md` (fetched) is careful and honest. It states the "お願い" (requests) section has **no binding force** and does not conflict with the repo license; the binding part is AGPL-3.0. It asks users not to use it for illegal, political, harm-to-others, or **impersonation/deepfake** purposes, and to check each model's own license. It then documents the bundled models' licenses in detail — e.g. for the あみたろ-derived voices it requires a **specific credit string** (`あみたろの声素材工房 (https://amitaro.net/)`), forbids treating output as that person's real voice or anyone else's, and sets a **model-merge rule**: merging is only allowed if the rights-holders of *all* voices involved consented, and if ≥25% of あみたろ's voice characteristics remain, the merged model inherits those terms.

---

## 5. Other strong contenders

### 5.1 IndexTTS / IndexTTS-2 / IndexTTS-2.5 (bilibili)
**Repo:** https://github.com/index-tts/index-tts — 24,481 stars, 2,903 forks, last push 2026-09-29.

**License — read carefully.** GitHub reports `NOASSERTION`. The actual `LICENSE` file (fetched via ghproxy) is the **"bilibili Model Use License Agreement"**, governed by **PRC law** with disputes at the **Shanghai Arbitration Commission**. Key terms:
- Grants a worldwide, non-exclusive, non-transferable, **royalty-free** limited license.
- **§2.2:** if you or your affiliates had **>100M MAU** in the prior month **or >RMB 1 billion** annual revenue, you must obtain a separate license.
- **§3.4(c):** you may **not** use indextts2 or derivatives **to improve any AI model** (except itself/derivatives/non-commercial AI models).
- **For a hobbyist agent plugin this license is fine.** For a commercial product above those thresholds it is not.
- The repo also ships a `DISCLAIMER` (fetched, dated 2025-03-17, by "Bilibili Index Team") that explicitly forbids synthesising **政治人物、公众人物 (politicians, public figures) or any unauthorised person's voice**, deception, impersonation, defamation, and commercial use of synthetic voices without authorisation.

**Capability (`README` fetched):** latest is **IndexTTS-2.5** (released 2026/08/10), **0.8B params**, supporting **Chinese, English, Japanese, Spanish, Arabic** — with fine-grained emotion control, speaking-speed control, pronunciation control (Pinyin / CMU phonemes / **Japanese Kana**), and faster inference than IndexTTS-2.

The emotion API is unusually rich and worth noting for *character acting*:
- `emo_audio_prompt` + `emo_alpha` (0.0–1.0) — a **separate emotional reference clip**, with intensity
- `emo_vector` — an 8-float vector in order `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]`
- `use_emo_text=True` (+ `emo_text`) — derive emotion from the text itself
- `duration_factor` (0.5–2.0) for speed

The `README` notes *"Enabling random sampling reduces the voice cloning fidelity"* and, for 2.5, `use_emo_text=True` requires constructing with `use_qwen_emo=True`.

**Zero-shot from a single reference clip** — `tts.infer(spk_audio_prompt='examples/voice_01.wav', text=..., lang="EN", output_path="gen.wav")`.

**Latency — published RTF on RTX 4090, `kv_cache=True`:** overall **0.3257** for 2.0 fp16, **0.2065** for 2.5 bf16, **0.2060** for 2.5 fp32.

**Windows:** `uv sync --all-extras`, then `uv run webui.py` → `http://127.0.0.1:7860`. The README warns explicitly: *"**Windows:** DeepSpeed may be difficult to install. You can skip it by removing the `--all-extras` flag"*, and CUDA Toolkit **12.8+** is needed if you hit CUDA errors. BF16 (2.5) / FP16 (2.0) inference reduces VRAM. **A published VRAM figure is not in the README — unverified.** Production path is a vLLM recipe (https://recipes.vllm.ai/IndexTeam/IndexTTS-2.5). Commercial contact: `indexspeech@bilibili.com`.

Models: ModelScope `https://modelscope.cn/models/IndexTeam/IndexTTS-2.5` · HF `https://huggingface.co/IndexTeam/IndexTTS-2.5` (and `IndexTTS-2`). Demo space: `https://huggingface.co/spaces/IndexTeam/IndexTTS-2.5-Demo`.

### 5.2 CosyVoice 2 / CosyVoice 3 (Alibaba FunAudioLLM)
**Repo:** https://github.com/FunAudioLLM/CosyVoice (note: `ungh.cc` now reports the canonical path as **`QwenAudio/CosyVoice`**) — 23,958 stars, last push 2026-05-25.
**License: `apache-2.0`** — verified on the HF model card `https://hf-mirror.com/FunAudioLLM/CosyVoice2-0.5B` (also: 9 languages, ONNX + Safetensors, 95 likes). **This is the most permissive license among the strong zero-shot cloners.**

**CosyVoice 3.0 key features (README fetched via ghproxy):**
- **9 languages:** Chinese, English, Japanese, Korean, German, Spanish, French, Italian, Russian — plus **18+ Chinese dialects/accents** (Guangdong, Minnan, Sichuan, Dongbei, Shanghai, Tianjin, Shandong, …)
- Both **multi-lingual and cross-lingual zero-shot voice cloning**
- Pronunciation inpainting for Chinese Pinyin / English CMU phonemes
- Text normalization without a traditional frontend
- **Bi-streaming with latency as low as 150 ms**
- Instruct support (languages, dialects, emotions, speed, volume)

**Benchmarks (from README):** Fun-CosyVoice3-0.5B-2512 scores test-zh CER **1.21** / SS **78.0**, test-en WER **2.24** / SS **71.8**, test-hard CER **6.71** / SS **75.8**. The `_RL` variant scores 0.81 / 1.68 / 5.44. CosyVoice2-0.5B (the version SiliconFlow hosts) scores 1.45 / 2.57 / 6.83.

**Serving:** official `runtime/python/fastapi/server.py` and a gRPC server, both in a Docker image; modes are `sft|zero_shot|cross_lingual|instruct`. **vLLM 0.11.x+ / 0.9.0 supported.** TensorRT-LLM path gives ~4× LLM acceleration. Also Docker: `cosyvoice:v1.0`.

**Windows:** conda env, `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`. Not as turnkey as GPT-SoVITS/SBV2, but workable. **VRAM unverified.**

### 5.3 Fish Speech / OpenAudio S1 (Fish Audio)
**Repo:** https://github.com/fishaudio/fish-speech — 33,103 stars, last push 2026-10-14 (very active).

**⚠️ License changed — this is the headline.** I read the full `LICENSE` (fetched via ghproxy), **"FISH AUDIO COMMUNITY LICENSE AGREEMENT, Version 1.0, Last Updated: October 13, 2026."** It is **not** an OSI open-source license:
- **Research & Non-Commercial:** free, including personal/hobbyist use.
- **§III(a) Community Commercial:** free **only while Annual Revenue < USD 500,000**. At/above that you must notify `business@fish.audio` within 30 days, get a 90-day transition, then need a separate written license.
- **§III(c) Hosted Services:** *"regardless of Your purpose or Annual Revenue, **no license is granted** … to offer a Hosted Service"* — i.e. offering third parties self-serve TTS/voice-cloning via API requires a separate license. **Relevant to you:** running it locally so *your own agent* speaks is explicitly carved out (generating speech for content you control, "an assistant's spoken replies") — that is **not** a Hosted Service.
- **§IV(b):** must not generate speech imitating an identifiable natural person's voice **without prior consent**; must not remove/disable watermarks or provenance signals; must not use it to train/improve another foundational speech model.
- **§IV(c)(iii):** you own the outputs.
- Governed by **California / US** law.

**Models:** **Drama 3** — 35B-A3B (3B active) at `https://huggingface.co/fishaudio/drama-3`; **S2-Pro** — 4B at `https://huggingface.co/fishaudio/s2-pro` (the README says S2-Pro weights remain under a separate **Fish Audio Research License**).

**Cloning:** *"Rapid voice cloning: **10–30 seconds** of reference audio is enough to reproduce a timbre."* Multilingual, ~100 languages, inline tags like `[whisper]`, `[angry]`, `[laughing]`, `[pause]`, `[excited]`.

**Latency:** *"RTF 0.195 on a single H200, about 100 ms to first audio"* (S2-Pro).

**Hardware — the deal-breaker** (from `docs/en/inference.md`, fetched):
| Model | GPU memory | GPU |
|---|---|---|
| Drama 3 | **at least 48 GB (FP8)** | **NVIDIA only; no CPU, no Apple MPS, no AMD ROCm** |
| S2-Pro | **at least 24 GB** | NVIDIA GPU or CPU |

And: **"System: Linux, WSL"** — with an explicit note that `--compile` is unsupported on Windows and macOS. **For a Windows desktop user this is impractical.** (S2-Pro CPU is theoretically possible, but the stated system requirements are Linux/WSL.)

**API — verified, and it is *not* OpenAI-shaped:** `python tools/api_server.py --listen 0.0.0.0:8080 --llama-checkpoint-path ...`. Endpoints: `POST /v1/tts` (**request body is msgpack**), `GET /v1/tts/defaults`, `GET /v1/health`, `POST /v1/vqgan/encode`, `POST /v1/vqgan/decode`, `POST /v1/references/add` (fields `id`, `audio`, `text`), `GET /v1/references/list`, `POST /v1/references/update`, `DELETE /v1/references/delete`, `GET /ui`.
**The `/v1/references/*` family is exactly the right primitive for a per-character voice table** — save a reference once under an `id`, then pass `--reference_id`.

### 5.4 F5-TTS
**Repo:** https://github.com/SWivid/F5-TTS — 15,403 stars, last push 2026-10-11. Paper: arXiv 2410.06885.
**License — important:** I verified via the HF model card (`https://hf-mirror.com/SWivid/F5-TTS`) that the weights are **`cc-by-nc-4.0` — NON-COMMERCIAL**. (Note: the *repo* license is often described as MIT; the *model weights* are the restrictive part. I verified the model card, which is what governs the weights.) 819,538 downloads last month, 152 finetunes — very popular.
**Language:** Chinese + English primarily. **Japanese is not natively supported** (no `ja` in the model card's language set) — a real limitation for your use case.
Zero-shot cloning from reference audio; ~0.3B params; fast.

### 5.5 Chatterbox (Resemble AI)
**Repo:** https://github.com/resemble-ai/chatterbox — 26,941 stars, last push 2026-07-21. `pip install chatterbox-tts`.
README fetched. Model zoo:

| Model | Size | Languages | Notes |
|---|---|---|---|
| **Chatterbox-Nano** | **110M** | English | **Runs on CPU — 3× realtime on 8 cores** |
| Chatterbox-Turbo | 350M | English | `[laugh]`, `[cough]`, `[chuckle]` tags; single-step decoder |
| **Chatterbox-Multilingual V3** | 500M | **23+** | improved speaker similarity, reduced hallucination |
| Single Language Pack | 500M ea | 6 finetunes | incl. **Chinese** (`ResembleAI/Chatterbox-Multilingual-zh-cmn`) |

**Languages verified:** ar, da, de, el, en, es, fi, fr, he, hi, it, **ja**, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, **zh** — **both Japanese and Chinese are supported.**

**Cloning:** zero-shot via `model.generate(text, language_id="zh", audio_prompt_path="your_10s_ref_clip.wav")` — a ~10 s reference in the example.
**Tuning knobs:** default `exaggeration=0.5`, `cfg_weight=0.5`; for *expressive/dramatic* speech lower `cfg_weight` to ~0.3 and raise `exaggeration` to ~0.7+. If the reference clip's language differs from the language tag, set `cfg_weight=0` to avoid accent transfer. **These two knobs are genuinely useful for anime-style delivery.**
**Responsible-AI:** every generated file carries Resemble's **PerTh perceptual watermark** (survives MP3 compression; ~100% detection). `https://github.com/resemble-ai/perth`.
**Caveat:** developed and tested on **Python 3.11 / Debian 11** (Linux-first). Runs with `device="cuda"/"cpu"/"mps"`. **VRAM not published in the README — unverified.** Disclaimer: *"Don't use this model to do bad things."*
**No official OpenAI-compatible server** — it's a Python library, so you'd wrap it.

### 5.6 XTTS-v2 (Coqui) — and why it's now a legacy choice
**Repo:** https://github.com/coqui-ai/TTS — 46,115 stars · **but last push 2024-08-16**. The company shut down; the repo is effectively frozen.
**License — nuanced, and I verified both halves:**
- **Code:** I fetched `LICENSE.txt` from the `dev` branch → **Mozilla Public License 2.0 (MPL-2.0)**.
- **Weights:** XTTS-v2 model weights are under the **Coqui Public Model License (CPML)**, which restricts to non-commercial use. *(I verified the code license directly; the CPML text itself I did not fetch — the CPML characterization is well-established, but treat the exact terms as unverified here.)*
**Maintained fork:** `idiap/coqui-ai-TTS` (https://github.com/idiap/coqui-ai-TTS) — 2,336 stars, last push **2026-10-02**. This is the live one.
**Cloning:** XTTS-v2 works with **as little as ~6 seconds** of clean audio. Coqui's own guidance (reproduced in the `openedai-speech` README): mono, **22050 Hz WAV**, **6–30 s**, low noise, no partial words/breathing/music, even pace; **audio over 30 s is silently truncated**.
**Languages:** 17 including **Chinese (`zh-cn`) and Japanese (`ja`)**.
**Conclusion: XTTS-v2 is the historical default, but in 2026 it is outclassed and legally encumbered (CPML). Prefer CosyVoice2 (Apache-2.0) or GPT-SoVITS (MIT).**

### 5.7 MegaTTS3 (ByteDance)
**Repo:** https://github.com/bytedance/MegaTTS3 — 6,097 stars, last push 2026-06-15.
⚠️ **I could not verify this one.** `https://ghproxy.net/.../MegaTTS3/main/README.md` returned HTTP 500 three times, and `api.github.com` was DNS-blocked at that point. **License, VRAM, Windows support, and whether weights are gated are all UNVERIFIED.** Widely described as Chinese+English with zero-shot cloning and a large VRAM requirement, but **I am not asserting that as fact.** If MegaTTS3 matters to you, verify directly.

### 5.8 Kokoro-82M — no cloning, but excellent, and OpenAI-compatible *today*
**Repo:** https://github.com/hexgrad/kokoro — 9,303 stars, last push 2025-08-06. Docs: `https://huggingface.co/hexgrad/Kokoro-82M`.
README verified: **"open-weight TTS model with 82 million parameters"** with **Apache-licensed weights**.
**⚠️ No voice cloning.** Voices are a fixed list (`voice='af_heart'`). Language pipelines via `misaki`: `a`=US English, `b`=UK English, `e`=Spanish, `f`=French, `h`=Hindi, `i`=Italian, **`j`=Japanese** (`pip install misaki[ja]`), `p`=Brazilian Portuguese, **`z`=Mandarin Chinese** (`pip install misaki[zh]`). 24 kHz output. On Windows you must install `espeak-ng` (MSI from the espeak-ng releases page).
**Why it still matters to you:** the **Kokoro-FastAPI** wrapper gives you a true OpenAI-compatible endpoint *today*.

**Kokoro-FastAPI** — https://github.com/remsky/Kokoro-FastAPI — **5,548 stars, pushed 2026-10-14** (actively maintained). I fetched its README:
```
docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest   # CPU
docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest
```
- **`POST /v1/audio/speech`** with `model`, `input`, `voice`, `response_format` (mp3/wav/opus/flac/aac/pcm), `speed` — verified to work with the official `openai` Python SDK against `base_url="http://localhost:8880/v1"`.
- Also `GET /v1/audio/voices`, `/v1/models`, `/docs`, web UI at `/web`.
- **Voice combination/mixing:** `voice="af_bella(2)+af_sky(1)"` weighted blends; **aliases** (`{"narrator": "af_bella(2)+af_sky"}`) and inline `[voice:...]` tags for multi-speaker.
- Inline control tokens: `[pause:1.5s]`, `[rate:1.5]`, IPA `[Worcester](/wˈʊstər/)`, SSML subset.
- **`POST /dev/tune`** — takes a 3–30 s clip and tunes a voice toward it via `inno-kokoro`. **Read the wording carefully: the README calls it *"A tuner, not a cloner: expect the same neighbourhood, not a match"*** and says *"Only tune voices you have permission to use."* **So Kokoro-FastAPI is NOT a character-cloning solution** — do not plan around it as one.
- Performance: first-token latency **~300 ms (GPU)** / ~3500 ms (CPU, older i7) / **<1 s (CPU, M3 Pro)**. Model unload for VRAM reclaim via `POST /dev/unload`.
- License: **Apache-2.0** (wrapper), Kokoro weights **Apache-2.0**, StyleTTS2-derived inference code MIT.

### 5.9 edge-tts — free, no cloning, surprisingly useful as a baseline
**Repo:** https://github.com/rany2/edge-tts — 12,276 stars, **pushed 2026-10-14** (very active). `pip install edge-tts`.
README verified: uses **Microsoft Edge's online TTS service**, so it is **completely free** with **no API key**. CLI: `edge-tts --text "..." --write-media hello.mp3 --write-subtitles hello.srt`. `--list-voices`, `--voice`, `--rate`, `--volume`, `--pitch`.
**⚠️ Custom SSML was removed:** *"Microsoft prevents the use of any SSML that could not be generated by Microsoft Edge itself … the service only permits a single `<voice>` tag with a single `<prosody>` tag inside it."*
**⚠️ No cloning.** Voices are Microsoft Neural voices — huge list including Chinese (`zh-CN-XiaoxiaoNeural`, etc.) and Japanese (`ja-JP-NanamiNeural`) — **but these are not anime characters.**
**Wrapper that makes it OpenAI-compatible:** **`travisvn/openai-edge-tts`** (https://github.com/travisvn/openai-edge-tts, 2,126 stars) — README fetched. Emulates `POST /v1/audio/speech` with `input`(≤4096 chars), `model`(`tts-1`/`tts-1-hd`), `voice` (OpenAI names **or any edge-tts voice**, e.g. `ja-JP-KeitaNeural`), `response_format` (mp3/opus/aac/flac/wav/pcm), `speed` (0.25–4.0), `stream_format` (`audio` or `sse`). Also `GET/POST /v1/models`, `/v1/voices`, `/v1/voices/all`. Port 5050. Docker one-liner: `docker run -d -p 5050:5050 travisvn/openai-edge-tts:latest`. **License GPL-3.0, "acceptable use-case is intended to be personal use."**
**Caveat (community):** it is an unofficial client for a service Microsoft runs for the Edge browser; using it programmatically is a terms-of-service grey area, and it requires network access.

---

## 6. Hosted / API options

### 6.1 SiliconFlow (硅基流动) — **the best hosted fit for this specific plugin**
**Docs (fetched):** https://docs.siliconflow.cn/docs/userguide/capabilities/text-to-speech
**Natively OpenAI-compatible.** The docs' own example is the OpenAI SDK:
```python
client = OpenAI(api_key="...", base_url="https://api.siliconflow.cn/v1")
client.audio.speech.with_streaming_response.create(
    model="FunAudioLLM/CosyVoice2-0.5B",
    voice="FunAudioLLM/CosyVoice2-0.5B:alex",
    input="...", response_format="mp3")
```
- **Endpoint:** `/audio/speech`. Params: `model`, `input`, `voice`, `speed` (0.25–4.0, default 1.0), `gain` (dB, −10…10), `response_format` (**mp3, opus, wav, pcm**), `sample_rate` (opus→only 48000; wav/pcm→8000/16000/24000/32000/44100 default 44100; mp3→32000/44100).
- **8 system preset voices:** alex, benjamin, charles, david (male); anna, bella, claire, diana (female) — Fish-Audio-derived.
- **✅ CUSTOM VOICE CLONING:** `POST https://api.siliconflow.cn/v1/uploads/audio/voice` with `model`, `customName`, reference audio (base64 data URI **or** file upload), and `text` (transcript). Returns a `uri` like `speech:your-voice-name:cm04pf7az00061413w7kz5qxs:mjtkgbyuunvtybnsvbxd` → **pass that `uri` as `voice`**. Also `GET /v1/audio/voice/list`, `POST /v1/audio/voice/deletions`.
  - **⚠️ Requires 实名认证 (real-name identity verification)** to use user-preset voices. This is a hard gate for non-Chinese-resident users — *I did not verify whether foreign IDs are accepted; treat as a risk.*
- **Models:** `FunAudioLLM/CosyVoice2-0.5B` (cross-lingual zh/en/**ja**/ko + 6 Chinese dialects; emotion control; fine-grained control; supports `<|endofprompt|>` emotion prompts like `你能用高兴的情感说吗？<|endofprompt|>今天真是太开心了`), `fnlp/MOSS-TTSD-v0.5` (two-person clone, zero-shot, auto speaker switching, zh+en, long-form). The example code comments also list **fishaudio / GPT-SoVITS / CosyVoice2-0.5B** series.
- **Billing:** by **UTF-8 byte count of the input text** (*"按照输入文本长度对应的 UTF-8 字节数进行计费"*). **I did not verify the exact per-byte price.**
- **Ref-audio guidance from the docs:** single speaker; clear articulation, stable volume/pitch/emotion; short pauses (~0.5 s); no background noise/echo; **recommended 8–10 s**; mp3/wav/pcm/opus, >192 kbps; **reference audio must be <30 s**; *"输入内容不要加空格"* (don't put spaces in the input).
- Model list: https://cloud.siliconflow.cn/models?types=speech

### 6.2 MiniMax (海螺)
**Docs (fetched):** https://platform.minimax.io/docs/guides/speech-voice-clone (EN) / `https://platform.minimax.cn/docs/...` (CN).
**TTS endpoint:** `POST https://api.minimax.cn/v1/t2a_v2` with `model` (e.g. `speech-2.8-hd`), `text`, `stream`, `voice_setting{voice_id, speed, vol, pitch, emotion}`, `pronunciation_dict{tone:[...]}`. **This is MiniMax's own schema — NOT OpenAI `/audio/speech`.** (MiniMax does offer OpenAI-compatible *text* endpoints, and a separate OpenAI-compatible section, but the speech endpoint is `t2a_v2`.)
**✅ Voice cloning ("音色快速复刻" / Voice Clone), verified workflow:**
1. Upload source audio via the File Upload API → get a `file_id`. **Formats mp3/m4a/wav; duration min 10 s, max 5 minutes; ≤20 MB.**
2. *(Optional)* Upload an example audio (<8 s) and pass it as `clone_prompt.prompt_audio` to improve quality.
3. Call the Voice Clone API with the `file_id` and your custom `voice_id`.
4. Use the resulting `voice_id` with the T2A API.
**Pricing:** I fetched `https://platform.minimax.io/docs/pricing/overview` — the LLM tables rendered, but the **Audio section did not render in my fetch**. **MiniMax speech pricing and whether cloning requires manual review are UNVERIFIED.** There is an "Audio Subscription" package tier. Community sources (e.g. `aireiter.com/zh/blog/minimax-voice-clone-api-guide`, `apizero.cn/ai/models/hailuo-speech-28`) discuss pricing/speech-2.8 but I did **not** verify them — treat as **hearsay**.
**Free tier:** the MiniMax CN docs mention a free trial. Unverified in detail.

### 6.3 Fish Audio (hosted)
**Website:** https://fish.audio/ · Blog: https://fish.audio/blog/fish-audio-open-sources-s2/
Hosts the S2 / Drama models as a service with a live playground and (per the open-source README) a **model marketplace** concept. The open-source **license forbids offering a Hosted Service** yourself (§III(c)), but Fish Audio's *own* hosted service is exactly that — so the API path is legitimate.
**⚠️ I could not fetch `https://docs.fish.audio/` or the pricing page** (repeated `fetch failed`). **Fish Audio API endpoint paths, pricing, and cloning-approval policy are UNVERIFIED.** What *is* verified: the open-source server exposes `/v1/references/add` (id + audio + text) and `/v1/tts` (msgpack), which tells you the *shape* of per-voice management.

### 6.4 Azure Custom Neural Voice — **effectively unavailable to individuals**
Verified from two Microsoft Learn pages:
- https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice (updated 2026-09-23)
- https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access (updated 2026-08-26)

**This is a hard blocker:**
> *"custom neural voice is a Limited Access feature available by registration only, and only for certain use cases."*
> *"**Only customers managed by Microsoft, meaning those who are working directly with Microsoft account teams, are eligible for access.**"*

Additional verified requirements: you must warrant **explicit written permission from the voice talent** before creating a model and share Microsoft's disclosure document with them; Microsoft runs **speaker-recognition biometric verification** comparing a recorded consent statement against the training audio; you must **disclose the synthetic nature** of the voice and provide a user feedback channel; Microsoft **retains** both the consent recording and the custom voice model. There is a **Custom neural voice "lite"** in public preview — 20–50 voice samples recorded in Speech Studio with **Microsoft-defined scripts**, for **demonstration and evaluation only** unless you obtain full access.
**⇒ Not viable for a hobbyist anime-character voice. Do not plan around it.**

### 6.5 ElevenLabs
**Docs (verified paths):** https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning (overview), `/instant-voice-cloning`, `/professional-voice-cloning`.
**Instant Voice Cloning (IVC)** best practices per the docs include **"Record at least 1 minute of audio"**, keep audio consistent, replicate the performance, and balance volume. **Professional Voice Cloning (PVC)** is the higher-fidelity tier requiring much more, studio-quality audio.
**Prohibited Use Policy:** https://elevenlabs.io/use-policy — **Last Updated: 09 October 2026**. I fetched it but the body was truncated before the voice-cloning clauses; the policy clearly covers Input/Output including voice samples and states categories are non-exhaustive. **The precise IVC consent requirements and the exact plan gating for IVC are UNVERIFIED from my fetch.** The pricing page (`https://elevenlabs.io/pricing/api`) rendered only its header — **tier prices UNVERIFIED**.
**Model:** Eleven v4 is current per the site banner.
**Shape:** ElevenLabs uses its own `POST /v1/text-to-speech/{voice_id}` API — **not** OpenAI-compatible.
**Known-good general position (community):** IVC requires a paid plan; cloning other people without consent is prohibited. **Treat specifics as hearsay.**

---

## 7. Where the *anime character models* actually come from

Three distinct routes, in order of legal cleanliness:

**(1) Build your own reference clip (cleanest, fully legal for private use).**
The standard community workflow with GPT-SoVITS's own tooling: extract a few seconds of a character's clean dialogue from an episode, run **UVR5** vocal/accompaniment separation (weights: https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/uvr5_weights), slice, and use it as the 5-second zero-shot reference. For fine-tuning, repeat across many lines. You are still using the voice actor's performance — see §8 — but you are not *distributing* a clone.

**(2) Download community finetunes from HuggingFace / ModelScope.**
Verified to exist (§3.7 and §4). Licenses range from permissive (`mit`, `cc0-1.0`) to restrictive (`cc-by-nc-4.0`, `cc-by-nc-sa-4.0`) to copyleft (`gpl-3.0`, `agpl-3.0`). **The license tag covers only the uploader's contribution.**

**(3) AivisHub — the only *curated, license-aware* character-model hub I found.**
**Verified:** https://hub.aivis-project.com/search — 76 models, filterable by category and license. **The category taxonomy is the key finding:** キャラクター（オリジナル）· **キャラクター（既存）** · 実在人物（存命）· 実在人物（故人）· 架空人物 · その他 — i.e. "original character", **"existing character"**, "real living person", "real deceased person", "fictional character", "other". Licenses: **ACML 1.0**, **ACML-NC 1.0**, **Public Domain (CC0)**, or custom. 76 models listed.
Top models by download: まお (59,944 dl, 6 styles), コハク (47,754 dl, 4 styles), 阿井田 茂 (21,620 dl, 7 styles), にせ (20,247 dl), まい (16,627 dl), fumifumi (15,077 dl).
**ACML 1.0** (fetched: https://github.com/Aivis-Project/ACML) is a genuinely thoughtful model license: it **permits free personal, corporate, non-profit and commercial use** and makes credit **optional**; it prohibits impersonation/deepfake confusion (requiring "※非公式です"-style disclaimers), uses that harm the speaker's dignity, harassment/defamation, deceptive misinformation, predatory marketing, political/religious advocacy, and criminal use. It explicitly extends the harm prohibition to **the work the character appears in**. It also has a pragmatic clause: for apps exposing synthesis to arbitrary users/LLMs, the developer complying "to a realistic extent" suffices. **Note ACML is a *model* license, and its §2 language about the "話者" (speaker) suggests it is designed for voices whose rights are genuinely cleared — which is why AivisHub's model-makers are vetted by category.**

**AivisHub also operates a rights-holder takedown mechanism.** Verified on the site footer: a dedicated **削除申請 (deletion request)** page at `https://hub.aivis-project.com/takedown-request/`, alongside terms of service and a 特定商取引法 notice. Operator: **Walkers Inc.** (© 2024–2026), contact `x.com/aivis_project` / `github.com/Aivis-Project`. **This is the only character-voice hub I found that publishes a formal removal route for rights-holders** — a meaningful good-faith signal, and the practical remedy if a model infringes your rights or someone else's.

**⚠️ Aggregator sites (a strong caution).** My web-search tooling could not reliably reach the Chinese/Japanese community model-sharing sites for verification (Bing RSS returned unrelated results for those queries). I therefore **cannot confirm specific domain names** for GPT-SoVITS/Bert-VITS2 community model dumps. What I *can* say with confidence: the HuggingFace and ModelScope ecosystems verified in §3.7/§4 contain exactly such third-party character models, and they are distributed **without permission from the character owners or voice actors**. Any site of that kind carries the same problem. **Do not treat "it's on HuggingFace" or "it has an MIT tag" as legal clearance.**

---

## 8. Legal and ethical position

This is the part most likely to matter to you later, so I'll separate what I verified from what I could not.

### 8.1 What I verified

**Japan's copyright authority's position — I fetched the actual source.**
The Agency for Cultural Affairs (文化庁) "AIと著作権について" page: **https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html**
Verified contents:
- In **March 2024 (令和6年3月)**, the Copyright Subcommittee's Legislative System Subcommittee compiled **「AIと著作権に関する考え方について」** ("General Understanding on AI and Copyright"). Primary document: `https://www.bunka.go.jp/seisaku/bunkashingikai/chosakuken/pdf/94037901_01.pdf`, English overview: `https://www.bunka.go.jp/english/policy/copyright/pdf/94055801_01.pdf`
- The underlying framework is **Article 30-4** and the 2018 (平成30年) "flexible rights limitation" provisions, described in `https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/h30_hokaisei/pdf/r1406693_17.pdf`
- A practical **「AIと著作権に関するチェックリスト＆ガイダンス」** (checklist & guidance for stakeholders, 令和6年7月31日): `https://www.bunka.go.jp/seisaku/chosakuken/pdf/94097701_01.pdf`
- Cultural Affairs also runs an **"AIと著作権に関する関係者ネットワーク"** (stakeholder dialogue platform) — a direct response to creator/voice-actor concerns.
⚠️ **I was unable to read the PDFs** (the fetch tool rejects `application/pdf`). So I have verified that the guidance **exists, is official, and is dated**, but **I have not verified its specific conclusions about voice cloning or performers' rights.** I am deliberately not paraphrasing it.

**Recent amendment (verified):** from `https://www.bunka.go.jp/seisaku/chosakuken/index.html` — a copyright amendment (令和8年法律第48号) passed the 221st special Diet session on **2026-06-17** and was promulgated **2026-06-24**, creating a **「レコード演奏・伝達権」** (record performance/transmission right) so that performers and record producers receive secondary-use remuneration when commercial records are played publicly. Effective within 3 years by cabinet order. This is about music remuneration, not AI voice cloning, but it shows the direction of travel: **performers' economic rights are being strengthened.**

**Platform policies (verified):**
- **Azure CNV** is the strictest — registration-only, Microsoft-managed customers only, **explicit written voice-talent consent**, biometric verification of the consent recording, mandatory synthetic-voice disclosure (§6.4).
- **Fish Audio Community License §IV(b)** (verified, October 13 2026): *"You will not use the Fish Audio Materials … to generate speech that imitates the voice of an identifiable natural person without that person's prior consent (or, for a minor, the consent of a parent or legal guardian, and for a deceased person, the consent of the holder of the relevant rights)."* Also prohibits watermarks removal and training competing foundational speech models.
- **IndexTTS DISCLAIMER** (verified, 2025-03-17, Bilibili Index Team): forbids synthesising 政治人物、公众人物 (politicians/public figures), any **unauthorised person's voice**, defamation, fraud, identity theft, and unauthorised commercial use.
- **Style-Bert-VITS2 TERMS_OF_USE** (verified): asks users not to use it for **impersonation/deepfake** creation, and documents, model-by-model, the exact credit and non-disparagement obligations for its bundled voices (including the ≥25%-merge rule).
- **AivisHub / ACML** (verified): the only ecosystem I found that **categorises models by whether the speaker is an original character, an existing character, a living real person, or a deceased person** — a genuine rights-hygiene signal.

**Concrete evidence that this is a live problem, not a theoretical one:** my HuggingFace search for `style-bert-vits2` returned openly-published models of **real Japanese politicians** — `AbeShinzo0708/AbeShinzo_Style_Bert_VITS2`, `AbeShinzo0708/KishidaFumio_Style_Bert_VITS2`, `AbeShinzo0708/SugaYoshihide_Style_Bert_VITS2`, `AbeShinzo0708/NikaiToshihiro_Style_Bert_VITS2` (all tagged `apache-2.0`). This is exactly the "public figure cloned without consent" case every policy above prohibits, and it sits on a major model host with a permissive license label. **It demonstrates that a license tag is not a rights clearance.**

### 8.2 What I could NOT verify (stated plainly)
I could **not** verify the **"NOMORE 無断生成AI"** movement, its participating voice actors, the **VOICE-69** effort, or the **2024 "AI voice cloning of anime voice actors" controversy**, because my search backend degraded (429 → 402) and Bing's RSS returned unrelated Chinese results for those Japanese-language queries. **These may well exist and be important — but I will not describe events I did not read.** Likewise I did not verify any JVA (日本映像ソフト協会) or CODA statement. If these matter, they need a separate targeted research pass.

### 8.3 The practical bottom line for a hobbyist
The legal picture has three tiers, and they are **not** the same risk:

| Tier | Example | Risk |
|---|---|---|
| **1. Your own voice** | Clone yourself | None |
| **2. Loan/licensed voice** | AivisHub **CC0 / ACML** original-character model | Low — rights are represented as cleared |
| **3. Real voice actor's performance** | Any anime character model off HuggingFace, or a self-made clip from an episode | **Highest — the VA's performance rights and the studio/publisher's character rights are both implicated** |

Two things are true simultaneously and it's worth being honest about both:
- **For purely private, non-distributed, personal use** — your agent speaking to you in your own room — the realistic enforcement risk is very low, and this is what the overwhelming majority of the community does. The *practical* exposure is a takedown of a distributed model, not a suit over your local playback.
- **The moment you distribute it** — publish the model, put the voice in a public app, post the audio, or use it commercially — you are in genuinely contested territory affecting real working people whose livelihoods depend on their voices. Japanese voice actors have been notably vocal on this, and the Cultural Affairs Agency has built a formal stakeholder dialogue process around it.

**Recommended posture for your project:** pick an **original character** voice from AivisHub (CC0/ACML), or **train on your own voice / a consenting friend's**, or use a **Style-Bert-VITS2 model with a clear license** like `litong/zgock/style-bert-vits2-zonoko-cc0` (**CC0**). If you do clone a specific anime character for personal use, **keep it local and never redistribute the model or the audio.** And do not build anything commercial on a community character finetune.

---

## 9. Recommended architecture for a Windows user

### 9.1 Decision

```
                     ┌──────────────────────────────────────┐
DSH voice plugin ──▶ │  OpenAI-compatible /v1/audio/speech  │
(POST text,          └───────────────┬──────────────────────┘
 play returned                   │
 audio file)          ┌──────────┴───────────┐
                      │                      │
             PATH A (local)          PATH B (hosted)
             GPT-SoVITS +            SiliconFlow
             adapter shim            (no adapter needed)
```

**Choose PATH A if** you want the best character fidelity, want it free after setup, have the disk/GPU, and are willing to run a small local server.
**Choose PATH B if** you want it working in five minutes, don't want to install anything, and accept real-name verification.

### 9.2 PATH A — GPT-SoVITS locally + a thin adapter (recommended)

**Step 1 — Install GPT-SoVITS.**
Download the official integrated Windows package from
**https://huggingface.co/lj1995/GPT-SoVITS-windows-package**
(China mirror: the Yuque link in the project README). Extract to a path **without spaces or Japanese/Chinese characters** — this matters, it breaks the toolchain. Run `go-webui.bat` / `go-webui.ps1`, or `go-webui-v2.bat` for the v2 inference WebUI. Manual route: `conda create -n GPTSoVits python=3.10`, then `pwsh -F install.ps1 --Device <CU126|CU128|CPU> --Source <HF|HF-Mirror|ModelScope> [--DownloadUVR5]`.

**Step 2 — Start the API server on 9880.**
```
.\runtime\python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
```
Health check: `GET http://127.0.0.1:9880/tts?...` should return audio or a 400 JSON error (a 400 with `ref_audio_path is required` proves the server is alive).

**Step 3 — Prepare one reference clip per character.**
For zero-shot you need a ~5 s clean clip **plus its exact transcript**. Create a folder per character:
```
voices/
  kurisu/
    ref.wav          # 5-10 s, clean, single speaker, no BGM
    ref.txt          # exact transcript of ref.wav
```
Clean the audio first (UVR5 for BGM/vocals separation, then trim to 5–10 s). **The transcript must match the audio exactly** — GPT-SoVITS uses it as the prompt.

**Step 4 — Write the adapter (this is the glue that doesn't exist off the shelf).**
A single-file FastAPI app that exposes `POST /v1/audio/speech` and translates to `/tts`:

```python
# sovits_openai_adapter.py   — run:  uvicorn sovits_openai_adapter:app --port 8000
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx, pathlib

SOVITS = "http://127.0.0.1:9880"

# ---- per-character config: OpenAI `voice` name -> reference clip ----
VOICES = {
    "kurisu": {"ref": "voices/kurisu/ref.wav", "text": "…exact transcript…", "lang": "ja"},
    "nene":   {"ref": "voices/nene/ref.wav",   "text": "…exact transcript…", "lang": "ja"},
}

class SpeechRequest(BaseModel):
    model: str = "gpt-sovits"
    input: str
    voice: str = "kurisu"
    response_format: str = "wav"
    speed: float = 1.0

app = FastAPI()

@app.get("/v1/models")
def models():
    return {"object": "list",
            "data": [{"id": "gpt-sovits", "object": "model"}]}

@app.post("/v1/audio/speech")
async def speech(req: SpeechRequest):
    v = VOICES.get(req.voice)
    if v is None:
        return JSONResponse(status_code=400,
                            content={"error": {"message": f"unknown voice {req.voice!r}"}})
    payload = {
        "text": req.input,
        "text_lang": v["lang"],
        "ref_audio_path": v["ref"],          # path on the GPT-SoVITS host
        "prompt_text": v["text"],
        "prompt_lang": v["lang"],
        "text_split_method": "cut5",
        "media_type": "wav",
        "streaming_mode": 0,
        "speed_factor": req.speed,
        "seed": -1,
    }
    async with httpx.AsyncClient(timeout=180) as c:
        r = await c.post(f"{SOVITS}/tts", json=payload)
    if r.status_code != 200:
        return JSONResponse(status_code=r.status_code, content={"error": {"message": r.text}})
    return Response(content=r.content, media_type="audio/wav")
```

Point your DSH plugin at **`http://127.0.0.1:8000/v1`**. Adding a character = adding a `VOICES` entry plus a folder. That is your **"reference audio per character → voice id"** mapping.

**Performance note:** if the agent's replies run long, set `"streaming_mode": 2` (or 3 for lowest latency) in the payload and return `StreamingResponse` — `api_v2.py` supports chunked audio, which will substantially improve perceived responsiveness. Mode 1 = best quality/slowest, 2 = medium, 3 = lower quality/faster.

**Optional upgrade — skip the adapter for multi-character fidelity:** install **GSVI** (https://github.com/X-T-E-R/GPT-SoVITS-Inference, Windows prezip at `https://huggingface.co/XTer123/GSVI_prezip`), which already gives you `GET /character_list` and `POST /tts?character=hutao&emotion=Yandere`, with the elegant `trained/<Character>/` folder convention. Your adapter then becomes a 10-line proxy to `:5000/tts`.

**If you fine-tune (better similarity, needs a GPU):** the WebUI's dataset tab handles slicing → denoise → ASR → labelling; ~1 minute of audio is the documented minimum, and the FAQ's practical guidance is that **45 minutes is the community's "plenty"**. Then register the resulting `SoVITS_weights/*.pth` + `GPT_weights/*.ckpt` — either as the server's startup model, or switch at runtime via `GET /set_gpt_weights` + `GET /set_sovits_weights`.

### 9.3 PATH B — SiliconFlow (zero install, OpenAI-compatible today)

**Step 1.** Get an API key: https://cloud.siliconflow.cn/account/ak
**Step 2.** *(For a custom character voice)* complete **实名认证**, then upload a reference clip (8–10 s recommended, <30 s, single speaker, clean):
```bash
curl -X POST https://api.siliconflow.cn/v1/uploads/audio/voice \
  -H "Authorization: Bearer $SF_KEY" \
  -F model="FunAudioLLM/CosyVoice2-0.5B" \
  -F customName="kurisu" \
  -F file=@kurisu_ref.wav \
  -F text="…exact transcript of the reference audio…"
# -> {"uri": "speech:kurisu:cm04...:mjt..."}
```
**Step 3.** Point the plugin at `https://api.siliconflow.cn/v1` with the returned `uri` as the `voice` value. **No adapter needed.**

### 9.4 Per-character config shape (either path)
```yaml
# The plugin only ever needs:  base_url + voice-id
characters:
  kurisu:
    voice_id: "speech:kurisu:cm04pf7az00061413w7kz5qxs:mjtkgbyuunvtybnsvbxd"   # SiliconFlow uri
    # --- or, for PATH A ---
    ref_audio: "voices/kurisu/ref.wav"
    ref_text:  "…exact transcript…"
    lang: ja
    notes: "tsundere delivery; speed_factor 1.05 sounds more in-character"
```
**Keep the reference clip, its transcript, and the voice id together as one unit.** If you swap the clip you must re-upload (SiliconFlow) or update the config (PATH A) — the id does not follow the audio.

### 9.5 Windows gotchas (all verified from primary sources)
1. **Path with no spaces / no CJK characters** — Style-Bert-VITS2's FAQ explicitly documents that renaming the install folder breaks it (`ModuleNotFoundError: No module named '_socket'`).
2. **ffmpeg** — GPT-SoVITS needs `ffmpeg.exe` + `ffprobe.exe` in the repo root; Kokoro/edge-tts need it for non-MP3 formats.
3. **`espeak-ng`** — required by Kokoro on Windows (MSI installer).
4. **DeepSpeed on Windows** — IndexTTS's README says outright to drop `--all-extras` and add extras manually.
5. **CUDA Toolkit 12.8+** — needed by IndexTTS if you hit CUDA errors.
6. **Fish Speech is Linux/WSL-only** — `--compile` is unsupported on Windows. Rule it out.
7. **PowerShell execution policy** — the `.ps1` installers may need `-ExecutionPolicy Bypass`.
8. **Port collisions** — GPT-SoVITS 9880, SVB2 (per its config), AivisSpeech 10101, Kokoro-FastAPI 8880, openai-edge-tts 5050, CosyVoice 50000, Fish Speech 8080. Pick deliberately.

### 9.6 Migration path if you later want a different engine
Because the adapter is the seam, swapping engines is a one-file change as long as the new engine's API is stable:
- **CosyVoice2 local** (Apache-2.0, if license purity matters): change the adapter to call `runtime/python/fastapi/server.py` with `mode=zero_shot` and pass the reference wav path; provisioned voices work the same way.
- **AivisSpeech (Japanese-only, CPU, free, CC0/ACML models):** point the adapter at `POST http://127.0.0.1:10101/audio_query?speaker=<style_id>` then `POST /synthesis?speaker=<style_id>`; get `style_id` from `GET /speakers`. This is a two-call dance, so the adapter is ~15 lines instead of 10.
- **Actually-OpenAI-compatible fallbacks, if you want to drop the adapter entirely:** Kokoro-FastAPI (`:8880`, Apache-2.0, **but no cloning**) and openai-edge-tts (`:5050`, GPL-3.0, **free, no cloning**, huge Chinese/Japanese Microsoft voice list). Useful as a *baseline* to prove your plugin works end-to-end before wiring the cloner.

---

## 10. Source index

**Engines**
- GPT-SoVITS — https://github.com/RVC-Boss/GPT-SoVITS · API source: `api_v2.py` · Windows package: https://huggingface.co/lj1995/GPT-SoVITS-windows-package · pretrained: https://huggingface.co/lj1995/GPT-SoVITS · UVR5 weights: https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/uvr5_weights · demo: https://lj1995-gpt-sovits-proplus.hf.space/ · Docker: https://hub.docker.com/r/xxxxrt666/gpt-sovits
- GSVI — https://github.com/X-T-E-R/GPT-SoVITS-Inference · prezip: https://huggingface.co/XTer123/GSVI_prezip
- gptsovits-api (legacy) — https://github.com/jianchang512/gptsovits-api
- Style-Bert-VITS2 — https://github.com/litagin02/Style-Bert-VITS2 · terms: `/docs/TERMS_OF_USE.md` · FAQ: `/docs/FAQ.md` · base: https://huggingface.co/litagin/Style-Bert-VITS2-1.0-base · JP-Extra: https://huggingface.co/litagin/Style-Bert-VITS2-2.0-base-JP-Extra · JVNV: https://huggingface.co/litagin/style_bert_vits2_jvnv · editor: https://github.com/litagin02/Style-Bert-VITS2-Editor
- IndexTTS — https://github.com/index-tts/index-tts · LICENSE (bilibili) + DISCLAIMER in-repo · models: https://modelscope.cn/models/IndexTeam/IndexTTS-2.5 · https://huggingface.co/IndexTeam/IndexTTS-2.5 · demo: https://huggingface.co/spaces/IndexTeam/IndexTTS-2.5-Demo · vLLM: https://recipes.vllm.ai/IndexTeam/IndexTTS-2.5
- CosyVoice — https://github.com/FunAudioLLM/CosyVoice · https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B · https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512 · https://www.modelscope.cn/models/iic/CosyVoice2-0.5B · demos: https://funaudiollm.github.io/cosyvoice3/
- Fish Speech — https://github.com/fishaudio/fish-speech · docs: https://speech.fish.audio/install/ , https://speech.fish.audio/inference/ · models: https://huggingface.co/fishaudio/drama-3 , https://huggingface.co/fishaudio/s2-pro · site: https://fish.audio/
- F5-TTS — https://github.com/SWivid/F5-TTS · weights: https://huggingface.co/SWivid/F5-TTS (cc-by-nc-4.0) · paper: https://arxiv.org/abs/2410.06885
- Chatterbox — https://github.com/resemble-ai/chatterbox · nano: https://huggingface.co/ResembleAI/chatterbox-nano · zh: https://huggingface.co/ResembleAI/Chatterbox-Multilingual-zh-cmn · watermark: https://github.com/resemble-ai/perth
- XTTS / Coqui — https://github.com/coqui-ai/TTS (frozen 2024-08) · maintained fork: https://github.com/idiap/coqui-ai-TTS
- MegaTTS3 — https://github.com/bytedance/MegaTTS3 ⚠️ **unverified**
- Kokoro — https://github.com/hexgrad/kokoro · https://huggingface.co/hexgrad/Kokoro-82M · G2P: https://github.com/hexgrad/misaki
- Kokoro-FastAPI — https://github.com/remsky/Kokoro-FastAPI
- edge-tts — https://github.com/rany2/edge-tts · OpenAI wrapper: https://github.com/travisvn/openai-edge-tts · voice samples: https://tts.travisvn.com/
- openedai-speech (obsolete, but documents XTTS practice) — https://github.com/matatonic/openedai-speech
- AivisSpeech — https://github.com/Aivis-Project/AivisSpeech-Engine · site: https://aivis-project.com/ · hub: https://hub.aivis-project.com/search · ACML: https://github.com/Aivis-Project/ACML · ONNX converter: https://aivm-generator.aivis-project.com/ · Cloud API: https://api.aivis-project.com/v1/docs

**Hosted**
- SiliconFlow — https://docs.siliconflow.cn/docs/userguide/capabilities/text-to-speech · https://cloud.siliconflow.cn/models?types=speech
- MiniMax — https://platform.minimax.io/docs/guides/speech-voice-clone · https://platform.minimax.cn/docs/api-reference/speech-t2a-http · https://platform.minimax.io/docs/pricing/overview
- Azure CNV — https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice · https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access
- ElevenLabs — https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning · https://elevenlabs.io/use-policy · https://elevenlabs.io/pricing/api

**Legal**
- Cultural Affairs Agency, AI & copyright — https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html · guidance PDF: https://www.bunka.go.jp/seisaku/bunkashingikai/chosakuken/pdf/94037901_01.pdf · English overview: https://www.bunka.go.jp/english/policy/copyright/pdf/94055801_01.pdf · checklist: https://www.bunka.go.jp/seisaku/chosakuken/pdf/94097701_01.pdf
- Art. 30-4 guidance — https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/h30_hokaisei/pdf/r1406693_17.pdf
- Copyright policy hub (2026 amendment) — https://www.bunka.go.jp/seisaku/chosakuken/index.html

---

## 11. Known gaps in this report

Stated so you don't over-trust it:
1. **MegaTTS3** — completely unverified (README fetch failed 3×).
2. **VRAM figures** for GPT-SoVITS, Style-Bert-VITS2, IndexTTS, CosyVoice2, and Chatterbox are **not published in their READMEs**. Any GPU-memory number you see elsewhere for these is community hearsay.
3. **Pricing** for MiniMax speech, Fish Audio, and ElevenLabs did **not render** in my fetches. SiliconFlow's *metering basis* (UTF-8 bytes) is verified; the **per-byte rate is not**.
4. **Japanese anti-AI-voice-cloning movement** (NOMORE 無断生成AI, VOICE-69, the 2024 VA controversy) — **could not verify**; search tooling failed. I did not guess.
5. **Cultural Affairs PDF contents** — the official documents are verified to exist and be dated, but the fetch tool rejects PDFs, so I did not read their conclusions.
6. **Whether SiliconFlow accepts non-Chinese real-name verification** — unverified, and it gates the custom-voice feature.
7. **Community model-aggregator domain names** — not verified; search returned unrelated results.
8. **XTTS-v2 CPML terms** — the *code* license (MPL-2.0) is verified; the CPML text is not.
9. **Style-Bert-VITS2's default API port** — the README documents `python server_fastapi.py` and that the spec is at `/docs`, but I could not fetch `config.yml` (404 at that path) to confirm the default port and full config keys. Read `/docs` on your running instance.
10. **AivisHub category-filter URLs** — the documented filter labels (キャラクター（既存）, etc.) are verified from the search page's own UI, but my attempt to deep-link a filtered query returned HTTP 500 (`Unexpected Server Error`). Use the on-page filters rather than a constructed URL.
11. **ElevenLabs plan gating and IVC consent specifics** — the FAQ sub-page 404s and the pricing page rendered only its header.
