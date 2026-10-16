# DSH Voice / Speech Plugin Catalog — ranked, evidence-based

**Research date:** 2026-10-14 (Asia/Shanghai) · **Method:** pure web research (web_search + web_fetch). Nothing was installed.
**Scope:** third-party voice/STT/TTS plugins installable into DeepSeek Harness (DSH) via `dsh plugin add` / `dsh plugin --profile web add`, with emphasis on **custom / user-chosen voice timbres**.

> **Read this first — three corrections to the brief's premises**
> 1. **`github:zhuiyueya/dsh-voice` does NOT exist.** `GET https://api.github.com/repos/zhuiyueya/dsh-voice` → **HTTP 404**. The author `zhuiyueya` has 25 public repos, none named `dsh-voice`. dshbase still serves a cached page + README for it (marked "Verified") — **a stale catalog entry**. Do not install it from GitHub.
> 2. **The npm name `dsh-voice` is a _different_ project.** `registry.npmjs.org/dsh-voice` → `dsh-voice@0.3.6`, repo `STARDUSTLC666/dsh-voice`. So "dsh-voice" is an **ambiguous identifier** — the name in the brief and the dshbase README refer to a repo that no longer resolves, while the npm name resolves to unrelated code.
> 3. **`dsh-voice-mic` is not an npm package** (404) but **does exist on GitHub**: [`Zachary7456/dsh-voice-mic`](https://github.com/Zachary7456/dsh-voice-mic) — confirmed, with a sherpa-onnx local backend exactly as the local file suggested.

---

## 1. Executive summary — the ranking

Ranking is by **custom-voice capability first**, then robustness/maintenance, then feature breadth.

| # | Plugin | Custom timbre? | Verdict |
|---|---|---|---|
| **1** | **`@memef1f1y/dsh-plugin-tts`** (repo `1624318455/dsh-plugin-tts`) | ✅✅✅ **RVC cloning + IndexTTS2 reference-audio + CosyVoice zero-shot + Edge + Google Cloud** | **Best-in-class.** The only plugin that natively covers four custom-voice families plus free Edge default. 25★, actively maintained, dshbase-verified. |
| **2** | **`github:91koukou/dsh-gpt-sovits`** | ✅✅✅ **GPT-SoVITS voice presets** (name + reference audio + reference text + language) | Purpose-built for custom anime-character voices via your own local GPT-SoVITS. Fully offline. 3★, MIT, maintained to 2026-10-09. |
| **3** | **`github:abbccdd/dsh-localtts`** | ✅✅✅ **IndexTTS 2.5 + GPT-SoVITS + RVC** local engines | A richer fork/companion of #1's stack, built on the same upstream commit. 5★, dshbase **Unverified**. |
| **4** | **`dsh-live2d-voice`** | ✅✅✅ **Fish Audio voice library — full-catalog search + preview + per-character & per-workspace voice IDs** | The strongest *character-role-switching* story: Live2D avatar, per-workspace voice override, dual-character stage, video-call mode. |
| **5** | **`dsh-voice-chat`** | ✅✅ **Custom OpenAI-compatible TTS endpoint** (per-engine isolated config) | Best "just works" voice-chat loop with a pluggable TTS backend. |
| **6** | **`dsh-voice-mode`** | ✅ **local VITS / Kokoro** (103 Kokoro + 322 Edge voices) | Most feature-complete full-duplex; heavy, complex, and **npm-deprecated on old versions**. |
| **7** | **`dsh-voice-studio`** | ✅✅ **XTTS v2 voice cloning from any sample** + ElevenLabs | Cloning-first and agent-tool-driven (`dsh_voice`). Low maturity. |
| **8** | **`dsh-ears`** | ❌ STT only (multi-ASR + LLM polish) | Best pure **voice input** plugin. 23★, verified. |
| **9** | **`dsh-voice-kit`** | ⚠️ **SiLU/SiliconFlow CosyVoice2 via OpenAI-compatible `/audio/speech`** | Three read-aloud engines incl. a China-direct cloud neural voice. |
| **10** | **`dsh-voice-alert`** | ⚠️ **Volcano/ByteDance voice-cloning console integration** | Turn-end/failure/approval announcements; not a conversational TTS front-end. |
| **11** | **`dsh-localtts` / `dsh-talk` / `dsh-voice-call` / `@fslong/dsh-voice` / `dsh-speech-plugin`** | mixed | See detailed entries below. |

**Bottom line for custom anime-character voices:** the winning stack is **`@memef1f1y/dsh-plugin-tts` for RVC / IndexTTS2 / CosyVoice** or **`dsh-gpt-sovits` for GPT-SoVITS**, optionally combined with **`dsh-live2d-voice`** for per-character role switching and the avatar.

---

## 2. Comparison table

Legend: ✅ yes · ❌ no · ⚠️ partial/conditional · ? unverified · **CU** = custom timbre support (the key criterion)

| Plugin | Install identifier | Profile | STT | TTS | **CU** | Custom-backend mechanism | Per-character presets / cloning | ★ | Last push | dshbase status |
|---|---|---|---|---|---|---|---|---|---|---|
| **dsh-plugin-tts** | `dsh plugin --profile web add "@memef1f1y/dsh-plugin-tts"` (npm) or `github:1624318455/dsh-plugin-tts#main` | web | ❌ | ✅ | **✅✅✅** | RVC local service (`.pth`+`.index`), IndexTTS2 HTTP (port 7880), CosyVoice HTTP (port 7890), Edge TTS, Google Cloud TTS | Voice presets; voice-pack registry; per-message read; approval alerts | 25 | 2026-10-13 | ✅ **Verified** (L1+L2+L3 on 0.1.0-rc.6) |
| **dsh-gpt-sovits** | `dsh plugin --profile desktop add github:91koukou/dsh-gpt-sovits` (also `web`) | web+desktop | ❌ | ✅ | **✅✅✅** | Your own local GPT-SoVITS `api_v2.py` on `http://127.0.0.1:9880` | **Named voice presets**: name + reference audio path + reference text + reference language; default preset | 3 | 2026-10-09 | ❌ not listed (repo exists, MIT) |
| **dsh-localtts** | `dsh plugin --profile web add github:abbccdd/dsh-localtts` | web | ❌ | ✅ | **✅✅✅** | IndexTTS 2.5 + GPT-SoVITS + RVC + Edge, via JSONL stdio worker to your local Python install | Reference audio + reference transcript + output language + speed | 5 | 2026-10-05 | ⏳ **Unverified** (`pending`) |
| **dsh-live2d-voice** | `dsh plugin --profile web add dsh-live2d-voice` (npm) or `github:john-walks-slow/dsh-live2d-voice` | web | ✅ (Volcano ASR) | ✅ | **✅✅✅** | **Fish Audio** TTS (`voiceId` = any 32-hex id), full public voice-library search/preview | `voiceId`, `playerVoiceId`, `modelSelection`, `workspaces{}` per-workspace overrides, `emotionMap` | 1 | 2026-10-13 | ❌ not listed |
| **dsh-voice-chat** | `dsh plugin --profile web add dsh-voice-chat` | web | ✅ | ✅ | **✅✅** | TTS engine `custom` = **any OpenAI-compatible** base URL/model/key/voice; also Edge + Xiaomi MiMo | Per-engine isolated config slots (`tts.mimo`, `tts.custom`); one `voice` per engine | 3 | 2026-10-11 | not checked |
| **dsh-voice-mode** | `dsh plugin --profile web add dsh-voice-mode` | web | ✅ local | ✅ | **✅** | Edge (322 voices) **or local VITS / Kokoro (103 voices)**; `modelHost` for CN mirrors | Voice/engine choice + wake word; **not** per-character | 16 | 2026-10-10 | ⏳ **Unverified** (`pending`) |
| **dsh-voice-studio** | `dsh plugin --profile web add dsh-voice-studio` | web | ❌ | ✅ | **✅✅** | **XTTS v2 cloning from an arbitrary sample**, Piper, or ElevenLabs API | `samplePath` default sample; `dsh_voice action=clone text=… sample=…` | 0 | 2026-08-31 | not listed |
| **dsh-ears** | `dsh plugin --profile web add dsh-ears` | web (+ desktop UI) | ✅ | ❌ | n/a | 9 ASR backends incl. local whisper.cpp GGML + custom OpenAI-compatible | ASR only; **no TTS at all** | 23 | 2026-10-09 | ✅ **Verified** |
| **dsh-voice-kit** | `dsh plugin --profile web add dsh-voice-kit` | web (desktop verified) | ✅ | ✅ | ⚠️ | Edge neural **or cloud neural via OpenAI-compatible `/audio/speech`** (SiliconFlow CosyVoice2 preset) or system speech | Engine + voice + rate + pitch; **no cloning** | 1 | 2026-08-26 | ✅ **Verified** (`已验证`) |
| **dsh-voice-alert** | `dsh plugin --profile web add dsh-voice-alert` | web | ❌ | ✅ | ⚠️ | Volcano Engine cloned-voice console (external); 20 built-in SFX | Voice library w/ clone + preset routes; **alerts only** | 0 | 2026-10-14 | not listed |
| **dsh-talk** | `dsh plugin --profile web add dsh-talk` | web | ✅ | ✅ | ? | Web Speech, FunASR, whisper.cpp (STT); browser, edge-tts, piper (TTS) | `speak` agent tool; per-session voices unclear | 15 | 2026-10-12 | not checked |
| **dsh-speech-plugin** | `dsh plugin --profile web add dsh-speech-plugin` | web | ✅ | ✅ | ? | Cloud TTS/ASR (DashScope, Volcengine) + Web Speech fallback | Per-message speak button, auto-announce toggle | 1 | 2026-08-16 | not checked |
| **@fslong/dsh-voice** | `dsh plugin --profile web add @fslong/dsh-voice` | web | ✅ | ❌ | n/a | Web Speech API **or local faster-whisper**; F2 hotkey | ASR only | — | 2026-08-19 (npm) | not checked |
| **dsh-voice-input-plugin** | `dsh plugin --profile web add @zhangbo-cn/dsh-client-ui-voice-input` (or `github:Zhangbo-cn/dsh-voice-input-plugin`) | web | ✅ | ✅ | ❌ | Browser Web Speech; host Edge TTS `/api/tts` or `speechSynthesis` fallback | None | 6 | 2026-08-25 | ✅ **Verified** |
| **dsh-voice-mic** | `dsh plugin --profile web add github:Zachary7456/dsh-voice-mic` | web | ✅ | ❌ | n/a | Web Speech, local SenseVoice/Paraformer, or custom OpenAI-compatible transcription | ASR only | 2 | 2026-08-15 | ❌ not listed |
| **dsh-voice** (npm) | `dsh plugin --profile web add dsh-voice` | web | ✅ | ✅ | ? | OpenAI-compatible TTS + STT | Text→speech / audio→text tools | 5 | 2026-10-08 | not checked |
| **dshbase-catalog** | `dsh plugin add dshbase-catalog` | any | n/a | n/a | n/a | **Directory** — lets the agent discover/install any listed plugin | n/a | 1 (repo) | 2026-10-14 | ✅ verified |
| **dsh-market** | `dsh plugin --profile web add dshmarket` | web | n/a | n/a | n/a | **Marketplace** — browse/search/one-click install; depends on awesome-dsh-plugin registry | n/a | 6495 | 2026-10-13 | ✅ **Verified** ⚠️ **Medium risk static scan** |

---

## 3. Detailed entries

### 3.1 `@memef1f1y/dsh-plugin-tts` — repo [`1624318455/dsh-plugin-tts`](https://github.com/1624318455/dsh-plugin-tts) — **RANK 1**

**Install.** Four equivalent forms (all register the same loader entry id `tts` — **you must uninstall one before installing another**, the installer rolls back rather than overwrite):
```sh
dsh plugin --profile web add "@memef1f1y/dsh-plugin-tts"          # npm
dsh plugin --profile web add "github:1624318455/dsh-plugin-tts#main"
dsh plugin --profile web add "file:/path/to/dsh-plugin-tts/plugin"
# or via dsh-market UI
```
Profile: **web** (requires `dsh web`; Node ≥ 22 for the native `WebSocket`).

**What it does.** Read-aloud button on every finalized assistant message; auto-read toggle in the composer; voice settings panel at 设置 → 插件 → 语音; preview; download audio; read-selected-text chip; streaming gapless chunked playback; mini player; **approval voice alerts** (`approval/asked` / `approval/decided`). Content plugin, not a conversational STT loop — **no microphone input.**

**Custom timbres — this is the headline.** Five selectable providers, four of them custom:
1. **Edge TTS** — free, no API key, 22 live-verified voices (default `zh-CN-XiaoxuanNeural`).
2. **Custom RVC voice** — your own trained `.pth` (+ optional `.index`), via a local `rvc-server.py`; one-click **portable RVC runtime** (no RVC WebUI install); voice-pack registry (`https://raw.githubusercontent.com/1624318455/rvc-for-tts/main`).
3. **Index-TTS2** — local reference-audio voices; service URL default port **7880**; reference-voice picker/upload, clean-text toggle, emotion control, sampling params.
4. **CosyVoice** — local zero-shot prompt cloning (CosyVoice-2.0-0.5B); service URL default port **7890**; prompt-audio picker + **prompt transcript (required)** + speed 0.5–2.0 + seed.
5. **Google Cloud TTS** — paid, API key (write-only, Host-file-only).

**Config keys.** Service-class config lives in a host file `~/.dsh/tts-rvc/settings.json` (`{ version: 1, rvc: …, index: …, cosy: …, cloud: … }`), UI prefs in `localStorage` key `dsh-tts-settings`, i18n in `dsh-tts-lang`. Routes: `/dsh-tts-api/speak`, `/dsh-tts-audio/<id>`, `/dsh-tts-api/rvc-next`, `/dsh-tts-api/rvc-files`, `/rvc-compact-index`, `/rvc-packs*`, `/dsh-tts-api/index-*`, `/dsh-tts-api/cosy-*`, `/dsh-tts-api/cloud-*`, `/dsh-tts-api/notify`, `/dsh-tts-api/diagnose`, plus `GET/POST /dsh-tts-api/rvc-config[-save]`.

**Maintenance.** 25★, 6 forks, 1 open issue, last push **2026-10-13**, MIT, 2 contributors. dshbase: **Verified**, "L1 install + L2 load + L3 runtime from GitHub source on dsh 0.1.0-rc.6", "Actively maintained". **Security: not yet scanned.**

**Caveats.** Edge path depends on Microsoft's undocumented `Sec-MS-GEC` protocol — a `403` means the endpoint changed and you must update `CHROMIUM_FULL_VERSION`/`TRUSTED_CLIENT_TOKEN` in `lib/index.mjs`. `1007 Unsupported voice` = the voice was retired. Local providers need a separate runtime (RVC portable is ~1.3 GB macOS / ~2–3 GB Windows CPU / ~7 GB Windows CUDA). RVC auto-fallback to Edge **sends your text to Microsoft** (off by default, opt-in). Synthesized audio goes to the OS temp dir. On Windows a `file:` install is a **copy**, not a symlink.

---

### 3.2 `github:91koukou/dsh-gpt-sovits` — **RANK 2 (best pure GPT-SoVITS)**

**Install.**
```sh
dsh plugin --profile desktop add github:91koukou/dsh-gpt-sovits
dsh plugin --profile desktop add github:91koukou/dsh-gpt-sovits#v0.3.0   # pin
```
README shows `--profile desktop`; the plugin is a Web-GUI plugin so `--profile web` is the equivalent on CLI installs. **Refresh the page after install** (the client half is composed in the boot graph).

**Prereqs (you supply everything).** A working GPT-SoVITS with `api_v2.py`, at least one GPT (`.ckpt`) + SoVITS (`.pth`) pair, and a reference audio clip. Start it yourself:
```sh
cd <your GPT-SoVITS dir>
runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
```
First model load takes ~12–30 s. Health probe hits `GET /control`, which **deliberately returns HTTP 400 without arguments** — the plugin treats 400 as "alive" and only treats unreachable as "not connected".

**Custom timbres — the core feature.** Voice presets = `名称 (name)` + `参考音频路径 (reference audio path)` + `参考音频文本 (reference text)` + `参考语言 (reference language)`; add/delete/multiple, one settable as default. Switching is skipped when the weight pair is unchanged, to avoid reloading the model on every read. Reference audio guidance: 3–10 s, clean single speaker, no BGM; **the path must be readable by the engine's machine**. **Filling in the reference text is strongly recommended** — leaving it blank makes the engine run ASR on the reference audio, taking first synthesis from ~1.5 s to ~40 s.

**Config keys** (settings panel 设置 → 语音朗读（GPT-SoVITS）; persisted at `$DSH_HOME/gpt-sovits/`):
| Key | Default | Notes |
|---|---|---|
| 引擎地址 / engine address | `http://127.0.0.1:9880` | `api_v2.py` listen address |
| 音色预设 / voice presets | empty | name + ref audio + ref text + ref lang |
| 朗读文本语言 | `zh` | `zh/en/ja/ko/yue/auto` |
| 语速 | `1.0` | engine `speed_factor`, 0.5–2.0 |
| 采样步数 | `32` | **lower to 16 for the biggest speedup** |
| 音量 / 播放倍速 | 90% / 1× | browser-side only |

**Features beyond plain TTS.** Per-reply 🔊 button with single-channel preemption; queued auto-read that reads only *newly completed sentences* and **never cuts off the sentence being spoken**; new turn cancels the previous turn; conversation switch stops playback; startup greeting that doubles as engine warm-up; streaming steps use `cut0` (one request per sentence, earliest start) while settled summaries use `cut5` (batched, ~2× fewer requests); text normalization (`cmd.exe`→「cmd点exe」, `120km/h`→「120千米每小时」, `3/4`→「4分之3」); punctuation-driven pauses (period 340 ms, comma 150 ms, ellipsis 460 ms, paragraph 520 ms); per-sentence speed + `temperature`/`top_k`/`top_p`; Markdown/code-block stripping.

**Maintenance.** 3★, 0 forks, 0 open issues, MIT, created 2026-10-02, last push **2026-10-09**, version v0.3.2, Windows + DSH desktop. **Self-declared AI-written** ("代码是 AI 写的" — by `deepseek-flash` inside a DSH session). Ships **no model weights, reference audio, or audio samples**.

**Caveats.** Loopback-only routes + same-origin checks on writes. The repo explicitly warns: use only voices you have rights to; synthesized audio may be mistaken for a real person; **your models/reference audio are not covered by the MIT license**. npm package `dsh-gpt-sovits` is **404** — GitHub-source install only. It does not start the engine for you.

---

### 3.3 `github:abbccdd/dsh-localtts` — **RANK 3 (IndexTTS 2.5 + GPT-SoVITS + RVC)**

**Install.** `dsh plugin --profile web add github:abbccdd/dsh-localtts` (also `file:` for local dev). Restart `dsh web` and refresh. Based on `1624318455/dsh-plugin-tts` at commit `ec0cf87ef52ab81ae91681a966aa3096365e631` — i.e. **the same upstream as RANK 1**, but adding a **local process launcher over a JSONL stdio worker protocol**.

**What it does.** Reads assistant replies with **IndexTTS 2.5** or **GPT-SoVITS**, started by the plugin as a thin JSONL worker; one natural sentence per request. Also offers inherited Edge TTS and RVC. Message buttons, Auto Read toggle, pause/stop, settings panel and Harness API integration are reused from upstream.

**Custom timbres.** Three-field standard setup: **Engine** (IndexTTS 2.5 / GPT-SoVITS) → **Project folder** (absolute path to your existing install; blank auto-discovers, "Find files automatically" rescans) → **Reference audio** (one candidate auto-filled; multiple require a choice; an external path can be typed manually). Advanced (collapsed) holds Python/Conda env, custom model paths, and **GPT-SoVITS reference transcripts + languages** ("some model versions require matching text, which cannot reliably be inferred from a filename; arbitrary checkpoint files are never guessed"). IndexTTS uses its official `duration_factor` (0.50 faster → 2.00 slower); GPT-SoVITS uses the WebUI `speed`/`speed_factor` range (0.60–1.65). Main panel also exposes output language and the model's own speed control.

**Coexistence.** Detects the original plugin and switches to **"Local companion mode"** — offering only the local process providers and leaving Edge/RVC, selection reading, generic shortcuts and approval alerts to the original. Turn **off the original Auto Read before enabling Local Auto Read**. Its settings tab is 本地语音 / **Local voice**, its button is marked **Local**, its toggle is **Local Auto Read**.

**Maintenance.** 5★, MIT, last push **2026-10-05**, v0.1.11 release candidate, 0.1.8 is incompatible with Harness 0.2. **dshbase: ⏳ Unverified (`pending`)** — "not yet install-tested". No npm package.

**Security posture (notably good, and notable caveats).** Loopback `127.0.0.1`/`localhost` allowed by default, localhost DNS pinned to IPv4 loopback; **LAN consent required** for a private RFC1918 IPv4 with an explicit warning that text leaves the machine; public addresses/hostnames always blocked. No automatic cloud fallback; this fork **disables** inherited cloud approval announcements in Local Runtime mode. Legacy HTTP config retained internally but "not the normal setup flow". Plain logs exclude complete reply text; **Debug** explicitly enables sentence-text logging. Local queues are in-memory, bounded, released on playback ack/cancel/expiry. `~/.dsh/voice-studio-venv`-style side effects: the IndexTTS worker uses a temp WAV and deletes it after return, though abnormal termination may leave one behind. Docs are extensive: `docs/VALIDATION.md`, `docs/PROCESS-WORKER-PROTOCOL.md`, `docs/ENGINE-DISCOVERY.md`, `docs/COEXISTENCE.md`, `docs/LOCAL-RUNTIME-PROTOCOL.md`.

---

### 3.4 `dsh-live2d-voice` — [`john-walks-slow/dsh-live2d-voice`](https://github.com/john-walks-slow/dsh-live2d-voice) — **RANK 4 (best per-character role switching)**

**Install.** npm `dsh-live2d-voice` (v1.6.1) or `github:john-walks-slow/dsh-live2d-voice`. README documents a manual profile install:
```bash
cd ~/.dsh/profiles/web && pnpm add dsh-live2d-voice
# append "dsh-live2d-voice" to package.json → dsh.profile.bundles
pnpm install && sv restart dsh
```
Requires DSH ≥ the 0.1.5-rc.3 host package series; browser needs WebGL.

**What it does.** Adds a **Live2D tab** to the session view: a Cubism 4 model (pixi.js v7) whose `ParamMouthOpenY` is driven by audio RMS, with per-sentence emotion tags switching expressions and bilingual subtitles. Continuous voice input (browser-local VAD → **Volcano Engine ASR**, bidirectional streaming `bigmodel_async` + `enable_nonstream` second pass, ≈0.6 s finalization) auto-submits; barge-in and speaker-echo rejection. Extras: fullscreen + Wake Lock, MediaPipe eye tracking, gyroscope parallax, `look_at_user` camera tool, standalone entry `/live2d-voice/app?session=<id>`, session picker `/live2d-voice`, **third-person dual-character stage** (`liveMode: "third"`), **video-call mode** (`liveMode: "call"`).

**Custom timbres — the strongest role-switching model.** TTS is **Fish Audio**, streaming 44.1 kHz PCM over SSE. `voiceId` is any 32-hex Fish Audio reference-voice id. The ⚙ panel and system settings open a **voice library** connected to Fish Audio's public catalog: keyword full-library search, filter by language (Chinese/Japanese/English/Korean) and tag (anime/character/female/male/narration/storytelling), per-row preview (author pre-rendered samples preferred, zero TTS quota), selection writes back to `voiceId`. Built-in presets include Rem (温柔女仆) `0c7771ca5910484e8a4933068017fcee`, 芙莉莲 `c174516c799a42e7be88b96c86cfbd3e`, 芙宁娜 `3fd70bbcdb6342df8c0c4143b958944b`.

**Config** at `<DSH_HOME>/live2d-voice.json` (`~/.dsh/live2d-voice.json`): `modelPath`, `voiceId`, `ttsModel` (default `s2.1-pro-free`), `apiKeys[]` (multiple keys auto-rotate on 401/402/429), `asrApiKey`/`asrAppId`/`asrAccessToken`, `sttLanguage`, `asrMode` (`stream`|`nostream`), `speechLanguage` (default `ja`!), `subtitleLanguage` (default `zh`), `sentenceSubtitles`, `eyeTracking`, `gyroParallax`, `emotionMap`, `speechPrompt`, `liveMode`, `playerModelSelection`, `playerVoiceId`, `playerPolish`, `playerSpeechLanguage`, `playerPrompt`, `playerEmotionMap`, and **`workspaces`** — per-workspace absolute path overrides of `voiceId`/`modelPath`/`modelSelection`/`speechLanguage`/`sttLanguage`/`subtitleLanguage`/`speechPrompt`/`emotionMap` (credentials global only).

**Maintenance.** 1★, 0 forks, 0 open issues, MIT, created 2026-09-27, last push **2026-10-13** (very active — v1.6.1). No npm-version caveats found. Prompt injection is session-scoped (only while the Live2D view is open) and delivered as a **user-message injection** via `agent/pre-step` with `source: {kind:"plugin", plugin:"dsh-live2d-voice"}` so it survives `complete: true` presets.

**Caveats.** ASR requires Volcano Engine credentials; **streaming mode does not support Japanese/Korean input** (use `asrMode: nostream`, 25 languages incl. ja-JP, ~1.3 s). TTS requires Fish Audio API keys (free tier model `s2.1-pro-free`). Browser needs HTTPS or localhost for `getUserMedia`. The voice library depends on host-side Fish connectivity.

---

### 3.5 `dsh-voice-chat` — [`maoyuching/dsh-voice-chat`](https://github.com/maoyuching/dsh-voice-chat) — **RANK 5 (cleanest pluggable-backend voice chat)**

**Install.** `dsh plugin --profile web add dsh-voice-chat` (npm, v0.4.1, Node ≥ 22, Chrome/Edge). Restart `dsh web`. Description: 「豆包式语音对话客户端插件」.

**What it does.** 🎤 click-to-talk (ding on start, 2.5 s silence auto-end, dong on stop) → transcribe → auto-send; TTS reads replies at +10%. Optional **转述朗读 (paraphrase-and-read)** — long replies are first condensed by an LLM "in the assistant's own voice" (≤ original length, no code/tables) before speaking; the model follows the session's current LLM. Single-channel playback with preemption; per-session replay de-duplication; mute toggle; `Ctrl+Shift+Space` hotkey (fallbacks `Ctrl+M` / `Ctrl+Shift+M`); settings live in the DSH settings modal under 「voice chat」 (gear icon, bottom-left) and **apply without restart**.

**Custom timbres.** **TTS engines: Edge TTS (free) / Xiaomi MiMo TTS (chat/completions protocol, several built-in Chinese voices) / custom TTS (OpenAI-compatible).** Each engine **stores its own Base URL / model / API key / voice**, so switching never overwrites another engine's config. ASR similarly: SiliconFlow (SenseVoice, free in CN) / Groq (Whisper) / Xiaomi MiMo / custom OpenAI-compatible.

**Config keys** — `~/.dsh/profiles/web/cordis.patch.yml`:
```yaml
- id: dsh-voice-chat
  name: 'dsh-voice-chat'
  config:
    asrEngine: siliconflow        # siliconflow | groq | mimo | custom
    asrApiKey: sk-xxxx            # or DSH_VOICE_ASR_KEY
    asrBaseUrl: https://api.siliconflow.cn/v1
    asrModel: FunAudioLLM/SenseVoiceSmall
    asr:
      custom: { baseUrl: http://127.0.0.1:8000/v1, model: whisper-v3, apiKey: sk-xxxx }
    llmModel: deepseek-v4-flash   # paraphrasing model (fallback)
    silenceMs: 2500
    rewrite: false                # paraphrase-and-read (default off)
    ttsEngine: edge               # edge | mimo | custom
    voice: zh-CN-XiaoxiaoNeural
    ttsBaseUrl: https://api.openai.com/v1
    ttsModel: tts-1
    ttsApiKey: sk-xxxx
    tts:
      mimo:   { baseUrl: https://api.xiaomimimo.com/v1, model: mimo-v2.5-tts, apiKey: sk-xxxx, voice: 冰糖 }
      custom: { baseUrl: https://api.openai.com/v1, model: tts-1, apiKey: sk-xxxx, voice: alloy }
    rate: '+10%'
    shortTextChars: 50
```
Precedence: settings panel > `cordis.patch.yml` (per-engine > legacy flat keys) > env vars > defaults.

**Maintenance.** 3★, MIT, published 2026-08-23, last modified **2026-10-11** (v0.4.1). Runtime dep `ws`. Has tests: `test/settings.test.mjs`, `test/client-settings.test.mjs`, `test/host-smoke.mjs`, plus `test/diagnose-tts.mjs` (per-engine real synthesis diagnostics).

**Caveats.** **ASR requires an API key** (SiliconFlow free tier / MiMo paid) — no keyless STT. Browser must be Chrome/Edge (`MediaRecorder`). README says the npm package is the recommended route. Not clearly dshbase-verified.

---

### 3.6 `dsh-voice-mode` — [`qishuilalala/dsh-voice-mode`](https://github.com/qishuilalala/dsh-voice-mode) — **RANK 6 (most complete full-duplex)**

**Install.** `dsh plugin --profile web add dsh-voice-mode`, then restart. npm v0.7.23. `Ctrl+Shift+V` enters voice mode.

**What it does.** Full duplex: streaming ASR (**local zipformer2 + SenseVoice final pass**, host-side, **zero API key**, with ITN), text streams into the draft while you speak, ~1500 ms silence auto-sends, replies are read sentence-by-sentence with live captions, and **true barge-in** (speak while it reads → reading stops). Wake-word standby with a prefix-filler whitelist; backchannel yield (`backchannelYield`: saying 「嗯/对」 yields 1.5 s instead of hard-interrupting); 3-level interrupt sensitivity; caption a11y (4 font sizes, 3 widths, theme following); 433 tests across 33 suites.

**Custom timbres.** Three engines: **Edge cloud (322 voices, default)** or **local VITS (pure Chinese)** or **local Kokoro (103 voices, CN/EN mixed)** — local engines keep reply text on-machine. Inline voice preview. **Not** per-character; a single global engine/voice choice. `modelHost` can be set to `https://hf-mirror.com` for CN networks.

**Config keys.** Settings → 语音模式 (Voice Mode). On dsh ≤0.1.5 settings live in the official store; on 0.1.7+ the plugin card writes its **own overlay file `~/.dsh/voice-mode.settings.json`** which overrides same-named profile keys (reset by setting the file to `{}` — **do not delete it**, deletion re-triggers migration). Notable keys: `senseITN` (true), `captionFontSize` (0=12px/1=14/2=18/3=24), `captionMaxWidth` (0=50vw/1=70/2=90), `backchannelYield` (true), `silenceMs` (1500), `rate` (1.1), `idleTimeoutMinutes` (5), `interruptLevel`, `echoGateDb`. 19 settings total.

**Maintenance.** 16★, MIT, last push 2026-10-10. Compatible with dsh 0.1.1-rc.2 through 0.2.1-alpha.2 incl. the Electron desktop host. **dshbase status: ⏳ Unverified (`pending`)** — "Not yet L3-verified".

**Caveats — important.** The npm registry lists **older versions as `deprecated`**: *"Known install/load defect: fresh install fails with pnpm 11 / npm (msedge-tts preinstall), and on dsh >=0.1.7 the installed plugin fails to import. Please upgrade to >=0.7.18."* Also, `optionalDependencies` include native `sherpa-onnx-node` and `sherpa-onnx`, so `pnpm use:platform`-style native trees matter; model download is large (use `npm run prefetch` / `modelHost` mirror in CN). Troubleshooting note: do **not** tune `echoGateDb` — with native AEC active it is never executed (ADR-0006).

---

### 3.7 `dsh-voice-studio` — [`meliodascz89/dsh-voice-studio`](https://github.com/meliodascz89/dsh-voice-studio) — **RANK 7 (cloning-first, tool-driven)**

**Install.** `dsh plugin --profile web add dsh-voice-studio` (npm v0.2.0), then add `dsh-voice-studio` to `dsh.profile.bundles` **and** `dependencies` in `~/.dsh/profiles/web/package.json`, then `dsh plugin --profile web install`. (The README's extra two steps suggest the bundle registration is not fully automatic — worth verifying.)

**What it does.** Local TTS + **voice cloning** + best-effort dubbing, exposed as an **agent tool** rather than a chat read-aloud button:
- `dsh_voice action=tts text="Ahoj světe"`
- `dsh_voice action=clone text="Hello" sample=/abs/voice.wav`
- `dsh_voice action=dub media=/abs/video.mp4`

**Custom timbres.** **XTTS v2** (quality + cloning) or **Piper** (fast) locally, or the **ElevenLabs** API. Requires `python3` on PATH (auto-creates `~/.dsh/voice-studio-venv`), `ffmpeg` for dubbing, a Piper voice model in `~/.local/share/piper/`. Outputs to `~/.dsh/voice-studio-outputs/`. Host spawns `worker/voice_worker.py` (stdlib HTTP server on `127.0.0.1:7862`) with `/tts`, `/clone`, `/dub` endpoints.

**Config:** `backend` (`local`|`api`), `ttsEngine` (`xtts`|`piper`), `language` (`cs`|`en` — **only Czech and English**), `apiKey`, `voiceId` (ElevenLabs), `samplePath`.

**Maintenance.** 0★, MIT, last push **2026-08-31**. **Low maturity**; no dshbase listing found; language limited to `cs`/`en`.

---

### 3.8 `dsh-ears` — [`WizisCool/dsh-ears`](https://github.com/WizisCool/dsh-ears) — **RANK 8 (best STT)**

**Install.** `dsh plugin --profile web add dsh-ears` (npm v0.4.1). Requires dsh `>=0.2.0-rc.1`, Node `^22.19.0 || >=24.0.0`. For dsh 0.1.x pin older versions (`dsh-ears@<0.4.0` for 0.1.2–0.1.6, `<0.4.1` for 0.1.7, `<0.3.0` for 0.1.1) — DSH refuses to install on an older host. Desktop has its own `desktop` profile that `dsh` does not manage.

**What it does.** Mic icon in the composer, `Ctrl+Shift+Space` (configurable). **Transcription always goes into an editable draft and never auto-sends.** Optional **LLM polish** (default on) removes filler words, fixes ASR typos, handles self-corrections; provider/model blank = the session's default agent model; credentials reuse existing DSH config; supports reasoning effort; custom prompt up to 4000 chars; raw transcript preserved on failure.

**ASR backends (9):** Web Speech (default), **local Whisper** (`@fugood/whisper.node` — no Python/FFmpeg/external deps, GGML models `tiny`→`turbo` downloadable in settings, `default`/`vulkan`/`cuda` acceleration), Groq Whisper, Deepgram (`nova-3`), Alibaba Cloud Bailian/DashScope, Tencent Cloud, Xiaomi MiMo (`mimo-v2.5-asr`), **SiliconFlow CN** (`FunAudioLLM/SenseVoiceSmall`), Volcano Engine, and **custom OpenAI-compatible `/audio/transcriptions`**.

**Maintenance.** 23★, 3 forks, 10 open issues, MIT, last push **2026-10-09**, TypeScript, builds on **15 official DSH packages**. dshbase: **✅ Verified**. Has CHANGELOG, CONTRIBUTING, SECURITY files.

**Caveats.** **No TTS whatsoever.** Web Speech may send audio to the browser vendor's servers (not fully local/offline). Bailian single recording ≤300 s. Deepgram Flux models need Listen V2 — unsupported. Local Whisper audio limit 24 MB, 120 s timeout. Acceleration mode locks after first native load; switching needs a `dsh web` restart. Front-end edits need only a refresh; server/settings/Remote/schema edits need a restart + refresh.

---

### 3.9 `dsh-voice-kit` — [`aaaadrop/dsh-voice-kit`](https://github.com/aaaadrop/dsh-voice-kit) — **RANK 9**

**Install.** `dsh plugin add dsh-voice-kit` (npm v0.4.0) or `dsh plugin --profile web add github:aaaadrop/dsh-voice-kit`. Node `^22.19.0 || >=24.0.0`. Restart + refresh. Verified in a real DSH **Desktop** profile.

**What it does.** 🎤 mic button left of the composer; recording is transcribed **host-side** and **appended** to the draft (never overwrites). Backends: browser Web Speech (Chrome/Edge) or **host-side OpenAI-compatible transcription** (e.g. SiliconFlow SenseVoice). `Esc` cancels.

**Custom timbres — three read-aloud engines.** (a) **Microsoft neural voices** (free; 晓晓/云希/云健/云扬…) synthesized host-side via `msedge-tts`, cached, with automatic system-proxy tunnelling for blocked networks; (b) **cloud neural voices** via an **OpenAI-compatible `/audio/speech`** endpoint with a one-click **SiliconFlow CosyVoice2** preset — China-direct, no proxy needed, **reuses the same API key as speech input**; (c) **system speech** — fully offline fallback, always available. Markdown/emoji stripped; long replies streamed in sentence chunks (first chunk audible in ~1 s); one message at a time; click again to stop.

**Settings:** first-level settings page with engine choice, one-click cloud presets, voice, rate, pitch, recognition language, engine reachability probe (Edge reachable ✅/❌), and key status (shows only 已保存/未设置, **never echoes the value**).

**Maintenance.** 1★, MIT, published 2026-08-19, last push **2026-08-26**, v0.4.0, 239 unit tests passing, `pnpm typecheck` clean. dshbase: **✅ Verified** (`已验证`), "已在 dsh 上安装测试".

**Caveats.** README's own FAQ: Microsoft voices need a proxy (`科学上网`) if Edge is unreachable; cloud neural voices need a key; system speech is always available but low quality. No voice cloning. **Repo shows 1★** despite the polished README. dshbase's cached page had no README text (repo metadata only).

---

### 3.10 `dsh-voice-alert` — [`loyalchiiina/dsh-voice-alert`](https://github.com/loyalchiiina/dsh-voice-alert) — **RANK 10 (alerts, not conversation)**

**Install.** `dsh plugin --profile web add dsh-voice-alert` (npm v0.4.12). Requires `engines.dsh >= 0.1.7-rc.1`, Node `^22.19.0 || >=24.0.0`.

**What it does.** Deterministically plays a fixed voice alert when a conversation turn ends and a different one when something failed (`agent/error` or tool `isError`) — plus approval events. Per-turn dedup, error-first (never stacks "done"), 5 s error throttle, 3 s done-suppression after a fail, user aborts silent by default, subagent sessions skipped. Three alert modes: 🗣 voice / 🎵 SFX (**20 built-in sounds**, 10 alerts + 10 nature, **zero config, no API key**) / 🔕 off. **Never touches system volume or mute state.**

**Custom timbres.** ⚠️ **Volcano Engine (ByteDance) voice cloning** via their console, with dual routing (cloned voice / preset voice), batch import, and trial-synthesis validation. Voice library defaults to **empty** — the plugin ships no specific voice. v0.3.4 notes "本插件不内置任何具体音色". Interface labels are deliberately generic (「🎙 我的音色」, no real names) so it can be redistributed.

**Notable engineering detail (and a caveat).** Long release notes document a real Bluetooth problem: MCI/`mpegvideo` goes through DirectShow and can tear down/renegotiate the audio endpoint, killing music playing on BT headphones. v0.4.0 makes **waveOut/WAV the default** (`playerEngine: "wav"`, auto ffmpeg mp3→WAV conversion + cache) and sets `prewarmMs: 0` by default because the 350 ms silent prewarm was **interrupting BT music**. Measured: ~610 ms player-start→sound, ~0.8–1.0 s turn-end→audible audio.

**Maintenance.** 0★, MIT, last push **2026-10-14** (the most recently pushed of all candidates), self-test "312 项全过". Not found in dshbase.

**Caveats.** Windows-centric playback (MCI/waveOut, `winsound`, PowerShell/Python). Cloned voice requires Volcano Engine account + billing. 2.4 MB unpacked (bundles sounds).

---

### 3.11 Supporting plugins (summary)

**`dsh-talk`** ([PerryLink/dsh-talk](https://github.com/PerryLink/dsh-talk), npm v0.3.20, 15★, Apache-2.0, last push 2026-10-12). Most heavily engineered: **npm provenance attestation (SLSA v1)**, published via GitHub Actions OIDC trusted publisher, TypeScript, `zod` dep, oxlint, vitest, extensive scripts (`verify:self-contained`, `verify:artifacts`, `check-lockfile-drift`). Described as: composer mic with browser/**local** STT (Web Speech, FunASR, whisper.cpp), a **`speak` tool** for TTS replies (browser, edge-tts, piper), event announcements with mute. **Two `dsh-talk` npm entries showed a ⚠️ flag in search results** (unverified marker). Declares `permissions: ["network:outbound","subprocess:spawn"]` and an `engines.dsh` range covering 0.1.2-rc.1 through 0.2.1-alpha.1. Custom-timbre support is **not documented in the registry metadata — unverified**.

**`dsh-speech-plugin`** ([huangdejie/dsh-speech-plugin](https://github.com/huangdejie/dsh-speech-plugin), npm v0.1.1, 1★, MIT, last push 2026-08-16). "Per-message speak button, composer voice input, and auto-announce toggle, over **cloud TTS/ASR** with **Web Speech API fallback**." Keywords name **DashScope** and **Volcengine**. Deps: `ws`, `@deepseek-ai/schemastery`. Single release, thin — treat as low-maturity.

**`@fslong/dsh-voice`** (npm v0.1.1, MIT, published 2026-08-18). 「参考 vokie」: 🎤 or **F2** hotkey → ASR → spoken-language polish → text streams live into the chat box → confirm to send. **Dual engine: browser Web Speech API (default) / local faster-whisper** (offline, switchable from the status bar). Ships `whisper:install` and `whisper:model` helper scripts, with `HF_ENDPOINT=https://hf-mirror.com` for CN. **STT only — no TTS, no custom voices.** Deps: esbuild, React peer.

**`@zhangbo-cn/dsh-client-ui-voice-input`** / repo `Zhangbo-cn/dsh-voice-input-plugin` (npm v0.1.0, 6★, MIT, last push 2026-08-25, TypeScript, builds on 6 official packages). dshbase **✅ Verified**. Tap-to-monitor live transcription + hold-to-talk; **reply reading streams while the model generates** (sentence-chunked queue), echo-pause during reading, tap-to-stop. Config: `language: 'zh-CN'`, `interimResults: true` under the `ui-voice-input` id. Reply audio prefers **host Edge TTS `/api/tts` (plugin `@deepseek-ai/dsh-tts-edge`)** with `speechSynthesis` fallback. **Firefox mic unsupported (browser limitation — Mozilla never shipped `SpeechRecognition`).** 26 vitest tests. **⚠️ 0.1.1+ required** — `0.1.0` registered the browser bundle under the wrong ModuleLoader id and Harness failed with `loaded without registering`. **No custom timbres.**

**`github:Zachary7456/dsh-voice-mic`** (2★, MIT, last push **2026-08-15**, JavaScript, **not on npm**). The plugin the "local file" referenced. Mic button + `Alt+V`; recognition results stream into the draft live (tail-replacement, never overwrites manual typing, rolls back on error); **never auto-sends**. Three engines: browser Web Speech (default, auto-restarts recognizers across browser disconnects), **local offline backend** (one-click deploy: detect Python → pip install → download model with resume → start `asr_server.py` → poll ready) using **sherpa-onnx** with **SenseVoiceSmall int8 (~158 MB)** or **Paraformer (~223 MB)**, served on `127.0.0.1:7860`; or **cloud OpenAI-compatible `/v1/audio/transcriptions`** with OpenAI/Groq/SiliconFlow presets (**key stored in browser localStorage, browser talks directly to the provider, never through dsh**). Models at `~/.dsh/voice/models/<model>`; env vars `DSH_VOICE_MIC_HOTKEY`, `_LANG`, `_BACKEND`, `_PORT`, `_MODEL_TYPE`, `_MODEL_DIR`, `_AUTOSTART`, `_API_BASE/_MODEL/_KEY`; server config via `cordis.patch.yml` (`hotkey`, `port`, `autoStart`). Precedence: settings page > env > cordis > defaults. Test scripts: `smoke.mjs`, `verify-install.mjs`, `deploy-test.mjs`, `e2e-backend.mjs`, `e2e-api.mjs` (+ `server/mock_api.py`). **STT only — no TTS, no custom voices.** Backend process is host-managed: after a dsh restart you must redeploy unless `autoStart: true`.

---

## 4. Custom-voice capability matrix (the key criterion)

| Voice family | Plugin that supports it | Mechanism |
|---|---|---|
| **GPT-SoVITS** | `dsh-gpt-sovits` (native, first-class) · `dsh-localtts` · `@memef1f1y/dsh-plugin-tts` (indirectly, via RVC base + local runtimes) | local `api_v2.py` on :9880 / JSONL stdio worker |
| **IndexTTS / IndexTTS 2.5** | `@memef1f1y/dsh-plugin-tts` (port 7880) · `dsh-localtts` (native engine) | local HTTP service, reference-audio picker |
| **CosyVoice** | `@memef1f1y/dsh-plugin-tts` (CosyVoice-2.0-0.5B, port 7890) · `dsh-voice-kit` (SiliconFlow CosyVoice2 via `/audio/speech`) | local zero-shot prompt clone / cloud OpenAI-compatible |
| **RVC (voice conversion)** | `@memef1f1y/dsh-plugin-tts` (portable runtime, `.pth`+`.index`) · `dsh-localtts` | local `rvc-server.py` |
| **BERT-VITS2 / Style-Bert-VITS2** | ❌ **NONE FOUND** in any plugin | — |
| **XTTS v2 cloning** | `dsh-voice-studio` | local worker on :7862, `sample=` arbitrary WAV |
| **Kokoro** | `dsh-voice-mode` (local, 103 voices) · README of the (dead) `zhuiyueya/dsh-voice` mentions "point at local Kokoro" | local native addon |
| **VITS** | `dsh-voice-mode` (local, pure Chinese) | local WASM |
| **edge-tts** | `@memef1f1y/dsh-plugin-tts` · `dsh-voice-chat` · `dsh-voice-kit` · `dsh-voice-mode` · `dsh-voice-input-plugin` · `dsh-voice-alert` (SFX/voice) | inline `msedge-tts` / `node-edge-tts` protocol |
| **OpenAI-compatible `/audio/speech`** | `dsh-voice-chat` (`tts.custom`) · `dsh-voice-kit` (cloud neural) · `@memef1f1y/dsh-plugin-tts` (via providers) | configurable base URL + model + voice |
| **Fish Speech / Fish Audio** | `dsh-live2d-voice` (Fish Audio TTS, full voice-library search) | `voiceId` 32-hex + `apiKeys[]` |
| **Azure / Microsoft Custom Neural Voice** | ⚠️ **NOT directly supported.** `@memef1f1y/dsh-plugin-tts` and `dsh-localtts` both document that Azure Custom Neural Voice and Personal Voice are **separate Azure Speech features requiring Limited Access registration**, explicit written permission, and recorded talent consent. `dsh-localtts` states plainly: **"Edge TTS cannot train a personal voice."** | — |
| **ElevenLabs** | `dsh-voice-studio` (`backend: api`) | `apiKey` + `voiceId` |
| **Volcano Engine cloning** | `dsh-voice-alert` | external console, voice-library routes |
| **Piper** | `dsh-voice-studio` · `dsh-talk` (claimed) | local model in `~/.local/share/piper/` |
| **Per-character role switching** | `dsh-live2d-voice` (**best**: `voiceId` + `playerVoiceId` + `workspaces{}` per-workspace overrides + multi-model catalog) · `dsh-gpt-sovits` (named presets, default preset) · `@memef1f1y/dsh-plugin-tts` (voice packs) | — |
| **Reference-audio cloning** | `dsh-voice-studio` (XTTS) · `@memef1f1y/dsh-plugin-tts` (IndexTTS2/CosyVoice) · `dsh-localtts` · `dsh-gpt-sovits` | — |

---

## 5. Documented DSH plugin installation workflow

### 5.1 Core command

```sh
dsh plugin --profile web add <package>      # npm name, github:owner/repo, or file:/abs/path
dsh plugin --profile web list               # confirm what's installed
dsh plugin --profile web remove <package>   # uninstall
dsh plugin --profile web install            # re-resolve after hand-editing package.json
```

Per [dshbase's plugin guide](https://dshbase.com/plugins/) and [tutorial](https://dshbase.com/tutorial/):
> "Plugins are npm packages. Add one to a profile with the `dsh plugin` command — **the arguments are forwarded to `pnpm`** (install it with `npm install -g pnpm` first)."
> "The `--profile` flag is required and names the profile to modify (default profile: `web`). DSH records the plugin in the profile's `package.json` — **both as a dependency and in `dsh.profile.bundles`** — and loads it on the next launch."

Notes:
- **`pnpm` is a hard prerequisite.** Missing pnpm → `'pnpm' is not recognized`.
- **The `file:` form on Windows is a COPY, not a symlink** — after editing `lib/` you must re-copy or reinstall for the running `dsh web` to see changes (documented in `dsh-plugin-tts`'s dev notes).
- **DSH's boot is all-or-nothing**: one plugin that fails to load stops the whole process. `dsh-market` ships a recovery prompt ("Adjust plugins") served by a detached restart helper for exactly this.
- **`engines.dsh` / `peerDependencies` are load gates, not warnings** on dsh ≥ 0.2.0-rc.1: if the running version is out of range, the host **silently skips the plugin** with only a `skipping profile bundle "…" is incompatible with dsh <version>` log line. `dsh-voice-call` learned this the hard way (its 0.3.7 vanished with 284 tests green because no test read the manifest).

### 5.2 Bundle registration / activation

Each plugin declares its activation layer in `package.json`:

```json
"dsh": {
  "bundle": { "patch": "./cordis.patch.yml" },
  "client": { "inject": ["@deepseek-ai/dsh-client-runtime", "..."], "platform": "web" }
}
```

- **`dsh.bundle.patch` / `dsh.bundle`** — the bundle-manifest field. `dsh plugin add` reads it and registers the package into **`dsh.profile.bundles`** in `~/.dsh/profiles/<profile>/package.json`.
- **`cordis.patch.yml`** — the bundle activation layer shipped *inside the package*. From `dsh-voice`'s README: *"Activation is automatic: the package ships a bundle patch (`cordis.patch.yml`) and declares `dsh.bundle.patch`, so `dsh plugin add` registers it into the profile's bundles for you."*
- **`dsh.bundle.patch`** — dshbase's submission requirements list the accepted manifest filenames: **`cordis.patch.yml` / `cordis.yml` / `dsh.bundle.patch`** (plus a `dsh-plugin` GitHub topic and a LICENSE).
- **Profile-level patch layer** — `~/.dsh/profiles/<profile>/cordis.patch.yml` is where per-plugin `config:` overrides go, addressed **by `id`**:
  ```yaml
  - id: dsh-voice-chat
    name: 'dsh-voice-chat'
    config: { ... }
  ```
  **Never insert the same id twice** — `dsh-voice-call` documents that a duplicate `insert` of the same id crashes startup. Also, the loader passes **only the `config:` sub-object** to a plugin, so top-level keys beside `name:` are silently ignored (this bit `dsh-market`'s `allowRestart`, issue #227).
- **Hot disable/enable** — `dsh-market` writes `- id: …` + `disabled: true|false` into the profile's `cordis.patch.yml`; DSH's HMR re-composes within ~1 s with no restart.
- **`--patch` for development** — `pnpm dsh web --patch ./scratch-plugin/cordis.yml` with an `- insert:` list pointing at an absolute path. Note the limitation documented by `dsh-plugin-voice-input`: **the browser half requires the name to be a resolvable package name** (client-modules reads `<name>/package.json`), so a `--patch` file path only loads the host half.

### 5.3 Restart / HMR rules (as documented by plugin authors)

| Change | Action |
|---|---|
| Client (browser) half — `lib/client.js` | **Refresh the page.** Bundles are re-read from disk per request. |
| Host (server) half — `lib/index.js` | **Restart `dsh web`.** |
| Settings registration, Remote, schema | Restart `dsh web`, then refresh (dsh-ears) |
| New plugin install | Restart `dsh web` **and** refresh; some plugins additionally need one page load because the client half is composed at boot (`dsh-gpt-sovits`: 「装完刷新页面」; `dsh-live2d-voice`: 「保存后刷新页面即生效」) |
| Hot-reload-capable changes | `dsh-market`'s HMR re-composes in ~1 s for `disabled:` toggles |
| Never | `pnpm install --force` (explicitly warned against by `dsh-plugin-tts`) |

The DSH Web GUI note in this environment matches: client-plugin HMR only auto-reloads while `pnpm run dev:web` is running from the same checkout; everything else needs a rebuild + page refresh.

### 5.4 Profiles

- **`web`** — the default; the browser GUI. Most voice plugins target this.
- **`headless`** — CLI single-task mode (`dsh --profile headless "…"`).
- **`desktop`** — the DSH Desktop (Electron) app uses its own `desktop` profile, which **the `dsh` CLI does not manage** (dsh-ears documents this explicitly). Desktop plugins are installed through the desktop plugin-management UI.
- A plugin may support **both** web and headless (`dsh-voice`'s README shows both `--profile web add` and `--profile headless add`), but voice plugins are inherently web/GUI.

### 5.5 Agent-driven installation (dshbase-catalog / dsh-market)

```sh
dsh plugin add dshbase-catalog      # install once
```
Then: *"install dsh-voice for me"* — the agent finds it in the directory and installs it. Per [dshbase-catalog docs](https://github.com/ylwl1997/dshbase/blob/main/docs/dshbase-catalog.md), it is *"the official lightweight market entry … not a full Hub clone"*, with source of truth `ylwl1997/dshbase → src/data/plugins.json` and generator `scripts/gen-catalog.py`.

Alternatively **`dshmarket`** (repo `dsh-market/dsh-market`, npm v1.66.21) gives a full in-GUI market at **Settings → Plugin Market**. Important: *"This repo is the market app, not the catalog. The plugin list comes from the curated [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) registry."* It requires `dsh web 0.1.0-rc.6+`, **restricts installs to sources listed in that registry**, keeps build scripts blocked by default (pnpm ≥10), flags terminal/CLI-surface plugins, accepts same-origin POST only, and does not phone home. dshbase's static scan tags dsh-market **⚠️ Medium risk — suspicious permission (medium), 23 files, 2026-10-13**.

**How dshbase verification is defined** ([audit methodology](https://dshbase.com/audit/)) — quoted precisely because it is narrower than "works":
> L1 · Install — installed into a clean profile alongside a pinned DSH runtime. L2 · Load — profile boots and dumps its configuration. L3 · Headless — a headless question is answered with the plugin loaded. **If the plugin is GUI-only, L3 returns `web-only` — that is not a pass.** L4 · Web CDP — required when L3 is web-only: boot a web profile and run browser CDP Q&A. Only L4 `ok` upgrades to verified.

dshbase itself states: *"'Verified' means our automated CI actually ran `dsh plugin add` in a clean profile and it booted — **nothing more**. … This is **not a security audit** and not an endorsement of third-party code."* Current corpus stats: **18,502 plugins, 7,831 verified (7,093 L3 + 738 Web L4), 10,671 pending, 1,436 MIT-licensed.**

---

## 6. Cross-cutting caveats

1. **Chrome/Safari `SpeechRecognition` uploads audio to Google** and is **unreachable in mainland China** (symptom: `识别出错：network`). Multiple plugins work around it by recording with `MediaRecorder` and transcribing through a self-hosted Whisper-compatible backend — `dsh-voice` documents this, `dsh-voice-mic`, `dsh-ears`, `dsh-voice-local`, `dsh-voice-input-plugin` (Sherpa/SenseVoice), `@fslong/dsh-voice` (faster-whisper) implement it. `dsh-voice-input-cn`'s npm description states bluntly: 「国内必须使用 Edge 浏览器（Chrome 语音识别走谷歌服务器不可达）」.
2. **Firefox has no `SpeechRecognition` at all.** `dsh-voice-input-plugin` feature-detects and disables the mic with a "not supported in this browser" hint — a genuine browser limitation, not a plugin bug. A cross-browser fallback requires `MediaRecorder` + an external transcription service.
3. **Edge TTS is an undocumented Microsoft consumer protocol, not an API.** `dsh-plugin-tts` reverses `Sec-MS-GEC` tick params and pins `Sec-MS-GEC-Version=1-143.0.3650.75`; a protocol change surfaces as **HTTP 403**. `dsh-localtts`'s README adds the licensing caveat: Microsoft describes Read Aloud as an Edge browser feature; **availability does not grant commercial rights**; heavy/commercial use should move to Azure Speech or a local Runtime.
4. **Azure Custom Neural Voice / Personal Voice require Limited Access registration** — explicit written permission plus recorded talent consent. **No DSH plugin can bypass this**, and none claim to.
5. **API keys**: SiliconFlow/miniMax/MiMo/Groq/Deepgram/DashScope/Tencent/Volcano/Fish Audio/ElevenLabs/Google Cloud all require keys and billing. Fully keyless setups are Edge TTS (network-dependent), local whisper.cpp/SenseVoice, and local GPT-SoVITS/IndexTTS2/CosyVoice/RVC (all needing substantial local installs).
6. **Runtime weight**: local TTS stacks are not small. RVC portable ≈1.3 GB (macOS arm64) / 2–3 GB (Windows CPU) / ~7 GB (Windows CUDA); the full RVC WebUI is 7.8 GB. GPT-SoVITS first load 12–30 s. SenseVoice int8 ≈158 MB; Paraformer ≈223 MB. `dsh-voice-mode` downloads zipformer2 + SenseVoice models.
7. **Windows `file:` installs are copies, not symlinks** — a live `dsh web` reads the profile copy; you must re-copy after editing.
8. **A single plugin failing to load stops the entire DSH boot.** Install risky plugins one at a time.
9. **`dsh-market` writes to `cordis.patch.yml`, not source** — and its static scan carries a medium-risk flag.
10. **Some results are unverified community claims.** Everything in this report is sourced from the plugin's own README, npm registry metadata, the GitHub REST API, or dshbase. **No plugin was installed or executed by this research.** Feature descriptions, star counts, and "verified" badges are reproduced as claims, not as independently reproduced test results.

---

## 7. Items I could NOT verify — flagged explicitly

| Item | Status |
|---|---|
| **`github:zhuiyueya/dsh-voice`** | **HTTP 404 — does not exist.** dshbase's cached page + README are stale. The 6 official `@deepseek-ai/*` packages it claims to build on and its `voice_transcribe`/`voice_speak` tool signatures are described **only** in that cached README. |
| **`dsh-voice` npm vs. `zhuiyueya/dsh-voice`** | **Different projects.** npm `dsh-voice@0.3.6` = `STARDUSTLC666/dsh-voice` ("把文字生成语音，或通过兼容接口把音频转为文字", keywords tts/stt/whisper). Its custom-timbre support is **unverified** — I did not fetch its README. |
| **`dsh-voice-mic` on npm** | **404 — not published.** GitHub-only. The brief's "referenced by a local file" matches [`Zachary7456/dsh-voice-mic`](https://github.com/Zachary7456/dsh-voice-mic) exactly (sherpa-onnx ASR backend, `topics: [sherpa-onnx, funasr]`). |
| **`dsh-ears`, `dsh-voice-kit`, `dsh-plugin-tts`, `dsh-voice-input-plugin`** | dshbase-marked Verified, but dshbase's own disclaimer says that means only "install + boot in CI". **Not security audits.** All four show **"Security: not yet scanned."** |
| **`dsh-plugin-tts` RVC / Index-TTS2 / CosyVoice guides** | Referenced (`docs/RVC-GUIDE.md`, `docs/INDEX-TTS2-GUIDE.md`, `docs/COSYVOICE-GUIDE.md`, `docs/CLOUD-GUIDE.md`, `docs/USER-GUIDE.md`) but **not individually fetched** — capability claims come from the main README only. |
| **`dsh-talk` custom timbres** | **Unknown.** Registry metadata names edge-tts/piper/browser for TTS but gives no voice-config keys. `raw.githubusercontent.com` and `cdn.jsdelivr.net` were both unreachable from this environment for that repo. |
| **`dsh-speech-plugin` custom timbres** | **Unknown.** Registry description says "cloud TTS/ASR" and keywords name DashScope/Volcengine; no config schema in metadata. |
| **`@fslong/dsh-voice`, `dsh-voice`, `dsh-voice-local`, `dsh-voice-scribe`, `dsh-voice-control`, `dsh-voice-mini`, `dsh-voice-assistant`, `dsh-voice-call`, `@biliye/dsh-voice-call`, `@goodandready/dsh-voice`, `@achasoft/dsh-voice`, `@motong/dsh-voice`, `@hiye/dsh-voice`, `@haoku123/dsh-voice`, `@muxiva/dsh-voice`, `@nn12138/dsh-voice`, `@wayneyu430227/dsh-voice-*`, `@meomeo-dev/dsh-voice[-tts]`, `dsh-live-voice`, `dsh-voice-gateway`, `dsh-voice-input-qwen-asr`, `dsh-voice-plugin`, `dsh-voice-webspeech`, `dsh-voice-input-web`, `dsh-voice-input-en`, `dsh-voice-input-cn`, `@opensquad/dsh-voice-input`, `@lmber/dsh-voice-input`, `@difimim/dsh-voice-input`, `@sakka6868/dsh-voice-input`, `dsh-voice-announcer`, `dsh-voice-talk`, `@wayneyu430227/dsh-voice-duplex`, `@nutshelllee/dsh-voice-mode-desktop`, `dsh-plugin-voice-input`, `dsh-voice-interaction`, `dsh-web-voice-input`, `dsh-stt-input`, `dsh-voice-input-local`, `TTSTT`, `dsh-plugin-voiceloop` etc. | **Identified via npm search (32,094 total hits for "dsh voice") but deliberately NOT individually vetted.** There is a very large long tail. Several carry ⚠️ markers in npm search results. `dsh-voice-alert` claims **voice cloning**, `dsh-voice-studio` claims **XTTS cloning**, `@biliye/dsh-voice-call` claims **MiniMax / MiMo-V2.5-TTS with director mode**. |
| **`dsh-market`'s 6,397★ vs GitHub's 6,495★** | Discrepancy between dshbase's cached page and the live GitHub API. Live value is authoritative. |
| **`dshbase.com`'s "dsh 0.1.0-rc.8" audit baseline vs. its per-plugin pages saying "0.1.0-rc.6"** | Inconsistent across pages. |
| **`dshbase`'s "1,700+ plugins" (README) vs "18,502 plugins" (site)** | Inconsistent. The site figure is current; the README is stale. |
| **`dshbase` sync provenance** | Primary source is `dsh.so`'s `search-index.json`; **dshbase says it trusts the upstream feed with no separate screening pass.** Its own README admits: *"the topic still contains tag-squatting repos."* This is consistent with a ghost entry like `zhuiyueya/dsh-voice` surviving as "Verified". |
| **`dsh.deepseek404.com` listing for `zhuiyueya/dsh-voice`** | Returned **404** when fetched directly, despite appearing in search results. |
| **Star counts in the brief's candidate list** | Briefly checkable only via the GitHub API. Notable: `dsh-plugin-tts` **25★**, `dsh-ears` **23★**, `dsh-voice-mode` **16★**, `dsh-talk` **15★**, `dsh-voice` (STARDUSTLC666) **5★**, `dsh-localtts` **5★**, `dsh-gpt-sovits` **3★**. |
| **`raw.githubusercontent.com`, `cdn.jsdelivr.net`, `cdn.statically.io`, `www.npmjs.com`** | Blocked/unreachable from this environment (`getaddrinfo ENOENT` / HTTP 403 Cloudflare). Worked around via `api.github.com`, `registry.npmjs.org`, and PowerShell `Invoke-WebRequest`. **`registry.npmjs.org/<pkg>` (full doc)** sometimes returned 406; `/latest` worked. |

---

## 8. Sources

**Documentation / methodology**
- https://dshbase.com/tutorial/ — plugin install workflow, profiles, common errors
- https://dshbase.com/install/ — DSH download/install channels, Node requirement
- https://dshbase.com/plugins/ — what a plugin is, `apply`/`ctx`, `defineTool`, manifest requirements
- https://dshbase.com/audit/ — L1–L4 verification methodology
- https://github.com/ylwl1997/dshbase/blob/main/docs/dshbase-catalog.md — in-DSH catalog plugin
- https://github.com/dsh-market/dsh-market — marketplace README (via https://dshbase.com/plugins/dsh-market/)

**Primary plugins**
- https://dshbase.com/plugins/dsh-plugin-tts/ · https://github.com/1624318455/dsh-plugin-tts · https://registry.npmjs.org/@memef1f1y%2Fdsh-plugin-tts/latest
- https://github.com/91koukou/dsh-gpt-sovits · https://api.github.com/repos/91koukou/dsh-gpt-sovits/readme
- https://github.com/abbccdd/dsh-localtts · https://api.github.com/repos/abbccdd/dsh-localtts/readme · https://dshbase.com/plugins/dsh-localtts/ · https://blog.yeyupiaoling.cn/article/1790737876423
- https://github.com/john-walks-slow/dsh-live2d-voice · https://registry.npmjs.org/dsh-live2d-voice/latest
- https://github.com/maoyuching/dsh-voice-chat · https://registry.npmjs.org/dsh-voice-chat
- https://github.com/qishuilalala/dsh-voice-mode · https://dshbase.com/plugins/dsh-voice-mode/ · https://registry.npmjs.org/dsh-voice-mode
- https://github.com/meliodascz89/dsh-voice-studio · https://registry.npmjs.org/dsh-voice-studio/latest
- https://dshbase.com/plugins/dsh-ears/ · https://registry.npmjs.org/dsh-ears/latest
- https://dshbase.com/zh/plugins/dsh-voice-kit/ · https://registry.npmjs.org/dsh-voice-kit
- https://github.com/loyalchiiina/dsh-voice-alert · https://registry.npmjs.org/dsh-voice-alert/latest
- https://github.com/PerryLink/dsh-talk · https://registry.npmjs.org/dsh-talk/latest
- https://github.com/huangdejie/dsh-speech-plugin · https://registry.npmjs.org/dsh-speech-plugin/latest
- https://registry.npmjs.org/@fslong%2Fdsh-voice/latest
- https://dshbase.com/plugins/dsh-voice-input-plugin/ · https://registry.npmjs.org/@zhangbo-cn%2Fdsh-client-ui-voice-input/latest
- https://github.com/Zachary7456/dsh-voice-mic · https://api.github.com/repos/Zachary7456/dsh-voice-mic/readme
- https://dshbase.com/plugins/dsh-voice/ (stale — repo 404s) · https://api.github.com/repos/zhuiyueya/dsh-voice (404)
- https://registry.npmjs.org/dsh-voice/latest (= STARDUSTLC666/dsh-voice)
- https://github.com/PandaPolo/dsh-voice-call · https://registry.npmjs.org/dsh-voice-call/latest
- https://registry.npmjs.org/-/v1/search?text=dsh%20voice&size=50 (long-tail discovery)
- https://github.com/Zachary7456/dsh-voice-mic · https://github.com/woodess/dsh-voice-input · https://github.com/baisama-cloud/dsh-stt-input · https://github.com/hjcnx/dsh-web-voice-input · https://github.com/zq0951/dsh-voice-gateway · https://github.com/apetersson/dsh-voice-input-local
