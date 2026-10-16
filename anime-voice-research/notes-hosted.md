# Hosted APIs + contenders (verified fetches, 2026-10-14)

## SiliconFlow (siliconflow.cn) — VERIFIED https://docs.siliconflow.cn/docs/userguide/capabilities/text-to-speech
- OpenAI-compatible: endpoint `/audio/speech` on base `https://api.siliconflow.cn/v1`; usable via `openai` python SDK `client.audio.speech.with_streaming_response.create(...)` with `base_url="https://api.siliconflow.cn/v1"`
- Params: model, input, voice, speed (float, default 1.0, range [0.25,4.0]), gain (dB, default 0.0, [-10,10]), response_format (mp3, opus, wav, pcm), sample_rate
  - opus only 48000; wav/pcm support (8000,16000,24000,32000,44100) default 44100; mp3 (32000,44100) default 44100
- ADVICE from docs: "输入内容不要加空格，参考音频要小于30s" (don't put spaces in input; reference audio must be <30s)
- Voice types: (1) system preset, (2) user preset (用户预置音色), (3) user dynamic (用户动态音色)
- 8 system preset voices (Fish Audio-derived naming): alex, benjamin, charles, david (male); anna, bella, claire, diana (female)
  - Naming: `FunAudioLLM/CosyVoice2-0.5B:alex` = model + ":" + voice
- **CUSTOM VOICE CLONE**: `POST https://api.siliconflow.cn/v1/uploads/audio/voice` with model + customName + audio (base64 data URI) or file upload + text (transcript of ref audio). Returns `uri` like `speech:your-voice-name:cm04pf7az00061413w7kz5qxs:mjtkgbyuunvtybnsvbxd` → use as `voice` param.
  - **REQUIRES 实名认证 (real-name verification)** for user-preset voices
- List: `GET /v1/audio/voice/list`; Delete: `POST /v1/audio/voice/deletions` with uri
- Models: **FunAudioLLM/CosyVoice2-0.5B** (cross-lingual zh/en/ja/ko + Chinese dialects 粤语/四川话/上海话/郑州话/长沙话/天津话; emotion control; fine-grained control via rich text or natural language); **fnlp/MOSS-TTSD-v0.5** (two-person voice clone, zero-shot, auto speaker switching, zh+en, long-form)
  - Also: "支持 fishaudio / GPT-SoVITS / CosyVoice2-0.5B 系列模型" (comment in example code)
- Billing: by UTF-8 BYTE COUNT of input text ("按照输入文本长度对应的 UTF-8 字节数进行计费")
- Ref audio best practices: single speaker only; clear articulation, stable volume/pitch/emotion; short pauses (~0.5s); ideally no background noise / professional recording / no room echo; **recommended 8–10s**; formats mp3/wav/pcm/opus; >192kbps mp3 recommended
- Emotion syntax: `input="你能用高兴的情感说吗？<|endofprompt|>今天真是太开心了..."` — `<|endofprompt|>` separator
- Model list page: https://cloud.siliconflow.cn/models?types=speech

## Azure Custom Neural Voice — VERIFIED https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice
- "Custom voice access is limited based on eligibility and usage criteria. Request access on the intake form https://aka.ms/customneural"
- Process: set up professional voice project → set up voice talent → **submit a recording of the voice talent's consent statement** → prepare fine-tuning data → train → deploy to custom endpoint
- Limited Access page (https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access):
  - "custom neural voice is a Limited Access feature available by registration only, and only for certain use cases"
  - "**Only customers managed by Microsoft, meaning those who are working directly with Microsoft account teams, are eligible for access.**"
  - Customers must warrant they have **explicit written permission from voice talent** prior to creating a voice model, and share the Disclosure for voice and avatar talent
  - Microsoft uses **speaker recognition biometric identification** on the recorded acknowledgement statement and verifies against training audio
  - Must disclose synthetic nature when deploying; must support feedback channel
  - "Personal voice, including the try-with-your-own-data demo experience in Speech Studio, is a Limited Access feature and requires registration and approval."
  - Custom neural voice **lite** (public preview): record 20-50 voice samples in Speech Studio, lightweight model for demo/eval only, Microsoft pre-defines recording & testing scripts
- Last updated 2026-09-23 (custom voice), 2026-08-26 (limited access)
- => NOT viable for a hobbyist anime-character voice. Effectively enterprise-only.

## ElevenLabs — VERIFIED
- Docs structure: /docs/eleven-creative/voices/voice-cloning (Voice Cloning overview; Instant Voice Cloning + Professional Voice Cloning)
- Instant Voice Cloning page: best practices include "Record at least 1 minute of audio", keep audio consistent, replicate performance, find good balance for volume
- Prohibited Use Policy: https://elevenlabs.io/use-policy — Last Updated 09 October 2026 (need detail on voice cloning consent; truncated)
- API pricing page: https://elevenlabs.io/pricing/api
- (Could not fetch elevenlabs.io/docs/overview/capabilities/voice-cloning — 404. Correct path is /docs/eleven-creative/voices/voice-cloning)

## edge-tts (rany2/edge-tts) — VERIFIED https://ghproxy.net/.../rany2/edge-tts/master/README.md
- Python module using Microsoft Edge's online TTS service. `pip install edge-tts` or `pipx install edge-tts`
- CLI: `edge-tts --text "Hello" --write-media hello.mp3 --write-subtitles hello.srt`; `edge-playback` (needs mpv except on Windows)
- `--list-voices`, `--voice`, `--rate`, `--volume`, `--pitch`
- **Custom SSML removed** — "Microsoft prevents the use of any SSML that could not be generated by Microsoft Edge itself... the service only permits a single `<voice>` tag with a single `<prosody>` tag inside it."
- Voice names like `af-ZA-AdriNeural`, `ar-EG-SalmaNeural`, `zh-CN-XiaoxiaoNeural`, `ja-JP-NanamiNeural` — Neural voices, many languages
- NO cloning. Free, no API key. Stars 12,276, actively pushed 2026-10-14.
- Caveat: unofficial client for an Edge-internal service; ToS grey area.

## Chatterbox (resemble-ai/chatterbox) — VERIFIED https://ghproxy.net/.../chatterbox/master/README.md
- Stars 26,941, pushed 2026-07-21. `pip install chatterbox-tts`
- Model zoo:
  - **Chatterbox-Turbo** 350M, English, paralinguistic tags `[laugh]` `[cough]` `[chuckle]`, lower compute/VRAM. Space: https://huggingface.co/spaces/ResembleAI/chatterbox-turbo-demo
  - **Chatterbox-Nano** 110M, English, same arch as Turbo, **runs on CPU: 3x faster than realtime on 8 CPU cores**. Model: https://huggingface.co/ResembleAI/chatterbox-nano
  - **Chatterbox-Multilingual V3** 500M, 23+ languages, improved speaker similarity, reduced hallucinations, cross-language voice cloning. Demo: https://huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS
  - Single Language Pack: 6 dedicated finetunes incl. Chinese https://huggingface.co/ResembleAI/Chatterbox-Multilingual-zh-cmn
  - Original Chatterbox 500M English, CFG & exaggeration tuning
- **Supported languages (Multilingual):** ar, da, de, el, en, es, fi, fr, he, hi, it, **ja (Japanese)**, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, **zh (Chinese)** — 23 languages
- Voice cloning: zero-shot via `audio_prompt_path="your_10s_ref_clip.wav"` (a 10s ref clip in the example). Generate: `model.generate(text, language_id="zh", audio_prompt_path=...)`
- Tips: default exaggeration=0.5, cfg_weight=0.5; for expressive/dramatic speech lower cfg_weight ~0.3 and raise exaggeration ~0.7+. If ref clip language ≠ language tag, set cfg_weight=0 to avoid accent transfer.
- **Built-in PerTh watermarking** on every generated file (imperceptible neural watermark surviving MP3 compression). Extraction: https://github.com/resemble-ai/perth
- Developed/tested Python 3.11 on Debian 11 (Linux-first). device="cuda"/"cpu"/"mps"
- "Disclaimer: Don't use this model to do bad things. Prompts are sourced from freely available data on the internet."
- Space demo: https://huggingface.co/spaces/ResembleAI/Chatterbox

## CosyVoice (FunAudioLLM → QwenAudio/CosyVoice) — VERIFIED via hf-mirror model card
- CosyVoice2-0.5B: license **apache-2.0**, 9 languages, ONNX + Safetensors, likes 95
  - ModelScope https://www.modelscope.cn/models/iic/CosyVoice2-0.5B ; HF https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B
- CosyVoice 1.0 300M: https://www.modelscope.cn/models/iic/CosyVoice-300M
- **Fun-CosyVoice 3.0**: demos https://funaudiollm.github.io/cosyvoice3/ ; paper https://arxiv.org/abs/2505.17589 ; ModelScope https://www.modelscope.cn/models/FunAudioLLM/Fun-CosyVoice3-0.5B-2512 ; HF https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512 ; CV3-Eval https://github.com/FunAudioLLM/CV3-Eval
- CosyVoice 2 paper https://arxiv.org/abs/2412.10117 ; v1 paper https://arxiv.org/abs/2407.05407
- Repo stars 23,958, pushed 2026-05-25

## F5-TTS — VERIFIED
- Repo SWivid/F5-TTS stars 15,403, pushed 2026-10-11
- **HF model license: cc-by-nc-4.0** (NON-COMMERCIAL) — https://huggingface.co/SWivid/F5-TTS
- Downloads last month 819,538 (very popular). Model tree: 152 finetunes, 7 quantizations
- Paper arXiv 2410.06885 (F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching)
- Checkpoints: F5TTS_v1_Base, F5TTS_Base, E2TTS_Base

## Kokoro — VERIFIED
- 82M params, **Apache-licensed weights**, https://huggingface.co/hexgrad/Kokoro-82M
- 24kHz output. NO cloning (fixed voice list, e.g. af_heart)
- Languages: a=American English, b=British English, e=Spanish, f=French, h=Hindi, i=Italian, **j=Japanese (pip install misaki[ja])**, p=Brazilian Portuguese, **z=Mandarin Chinese (pip install misaki[zh])**
- Windows: install espeak-ng MSI from https://github.com/espeak-ng/espeak-ng/releases
- G2P: misaki https://github.com/hexgrad/misaki
- Repo stars 9,303, last pushed 2025-08-06 (slower maintenance)
- Samples: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/SAMPLES.md ; Discord referenced

## IndexTTS — VERIFIED (see notes-raw)
## Fish Speech — VERIFIED (see notes-raw): Fish Audio Community License; Drama 3 35B-A3B, S2-Pro 4B; 10-30s cloning; RTF 0.195 H200
## Style-Bert-VITS2 — VERIFIED (see notes-raw)

## Japanese copyright context — PARTIAL
- Cultural Affairs Agency (文化庁) AI and copyright page: https://www.bunka.go.jp/seisaku/chosakuken/aiandcopyright.html (linked from https://www.bunka.go.jp/seisaku/chosakuken/index.html as "AIと著作権について") — NOT yet fetched
- 2026 (令和8) copyright amendment: "レコード演奏・伝達権" (record performance/transmission right) for musicians/performers on commercial records played publicly; passed 2026-06-17, promulgated 2026-06-24 as 令和8年法律第48号; effective within 3 years by cabinet order. Source: https://www.bunka.go.jp/seisaku/chosakuken/index.html
- Copyright infringement consultation desk for individual creators: https://www.bunka.go.jp/seisaku/chosakuken/kaizoku/contact.html
