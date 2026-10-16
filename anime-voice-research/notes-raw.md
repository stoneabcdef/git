# Raw research notes (verified fetches)

Network notes: api.github.com was reachable early then DNS-blocked. Working paths:
- `https://ghproxy.net/https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` (works)
- `https://ungh.cc/repos/<owner>/<repo>` (metadata, works)
- `https://hf-mirror.com/<...>` (HuggingFace mirror, works)
- `https://www.modelscope.cn/...` (works)
- github.com, raw.githubusercontent.com, huggingface.co direct: BLOCKED (non-public IP / ENOENT)

## GPT-SoVITS (RVC-Boss/GPT-SoVITS)
- Fetched: https://api.github.com/repos/RVC-Boss/GPT-SoVITS  (2026-10-14)
- License: MIT. Stars 62,801. Forks 6,704. created 2024-01-14, pushed 2026-10-08, updated 2026-10-14. open issues 896. lang Python.
- README (fetched via api readme, base64) facts:
  - "Zero-shot TTS: Input a 5-second vocal sample and experience instant text-to-speech conversion."
  - "Few-shot TTS: Fine-tune the model with just 1 minute of training data for improved voice similarity and realism."
  - Cross-lingual: English, Japanese, Korean, Cantonese, Chinese.
  - WebUI tools: voice accompaniment separation, auto training-set segmentation, Chinese ASR, text labeling.
  - RTF of GPT-SoVITS v2 ProPlus: 0.028 on 4060Ti, 0.014 on 4090 (1400 words≈4min, inference 3.36s), 0.526 on M4 CPU.
  - Windows: "download the integrated package" https://huggingface.co/lj1995/GPT-SoVITS-windows-package/resolve/main/GPT-SoVITS-v3lora-20250228.7z?download=true → double-click go-webui.bat
  - China download: yuyue.com link.
  - install.ps1: `pwsh -F install.ps1 --Device <CU126|CU128|CPU> --Source <HF|HF-Mirror|ModelScope> [--DownloadUVR5]`
  - Tested: Python 3.10/3.11/3.12, PyTorch 2.5.1/2.7.0/2.7.1/2.8.0dev, CUDA 11.8/12.4/12.8, Apple silicon, CPU (py3.9/py2.2.2)
  - Release notes: V2 (Korean+Cantonese, 5k hours pretrain), V3 (higher timbre similarity, better emotion), V4 (fixes metallic artifacts, native 48k output; V4 is a direct replacement for V3), V2Pro (slightly higher VRAM than v2, surpasses v4 perf with v2's hardware cost), V5 (improved similarity without SoVITS finetuning; new vocoder reduces spectral mirroring; supports cuda_graph + flash_attention)
  - v1/v2/v2Pro share characteristics; v3/v4 similar. "For training sets with average audio quality, v1/v2/v2Pro can deliver decent results, but v3/v4 cannot." v3/v4 tone leans toward reference audio rather than whole training set.
  - Dataset format: `vocal_path|speaker_name|language|text`, language codes zh/ja/en/ko/yue
  - Files present: api.py (47003 bytes), api_v2.py (22631 bytes), install.ps1, go-webui.bat, go-webui.ps1, docker-compose.yaml, Docker/ , webui.py (82922)
  - Repo also has `requirements-py312-win-flash_attention` dir.
  - HF pretrained: https://huggingface.co/lj1995/GPT-SoVITS ; gsv-v2final-pretrained, gsv-v4-pretrained, gsv-v5-pretrained
  - G2PW model: HF XXXRT/GPT-SoVITS-Pretrained, ModelScope XXXRT/GPT-SoVITS-Pretrained
  - UVR5 weights: https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/uvr5_weights
  - Chinese ASR: ModelScope damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch, damo/speech_fsmn_vad, damo/punc_ct-transformer
  - EN/JA ASR: Systran/faster-whisper-large-v3
  - HF space demo: https://lj1995-gpt-sovits-proplus.hf.space/
  - Docker: hub.docker.com/r/xxxxrt666/gpt-sovits

## jianchang512/gptsovits-api (wrapper of api.py)
- Fetched: https://api.github.com/repos/jianchang512/gptsovits-api/readme (base64)
- Wraps GPT-SoVITS api.py (renamed api2.py); default port 9880, default host 127.0.0.1
- Startup: `.\runtime\python api2.py -dr "123.wav" -dt "一二三四五六七八九十。" -dl "zh"`
- `-a <ip>` `-p <port>`; `-s SoVITS_weights/<name>` `-g GPT_weights/<name>`; `-d cpu|cuda|mps`
- API: GET `http://127.0.0.1:9880?text=...&text_language=zh`
- POST JSON: {"refer_wav_path","prompt_text","prompt_language","text","text_language"} → returns wav stream (200) or JSON error 400 {"code":400,"message":"未指定参考音频且接口无预设"}
- Only supports zh/ja/en via -dl
- KEY LIMITATION stated by author: api2.py and official api.py do NOT support dynamic model switching. Solution = one model per api service instance, bind different ports. Example: default model on 9880; custom model on 9881 with `-p 9881 -s "SoVITS_weights/mymode-e200.pth" -g "GPT_weights/mymode-e200.ckpt" -dr "wavs/10.wav" -dt "..." -dl zh`

## Style-Bert-VITS2 (litagin02)
- Fetched: https://api.github.com/repos/litagin02/Style-Bert-VITS2 → fork of fishaudio/Bert-VITS2
- License AGPL-3.0. Stars 1,384. forks 219. created 2023-12-01. pushed 2025-12-07. updated 2026-10-14. open issues 84.
- README (via ghproxy raw, master):
  - Ver 2.7.0 2025-08-24: ONNX conversion GUI added, and `litagin/anime-whisper` added as ASR model (for Aivis Project interop)
  - Ver 2.6.0 2024-06-16: model diff merge / weighted merge / null model merge
  - Ver 2.5.0 2024-06-02: added TERMS_OF_USE (利用規約), 小春音アミ・あみたろ models added
  - "音声合成のみに使う場合は、グラボがなくてもCPUで動作します。" (CPU synthesis works without GPU)
  - `pip install style-bert-vits2` (inference only)
  - API server bundled: `python server_fastapi.py`; API spec at `/docs` after start. Input limit default 100 chars via config.yml server.limit. CORS default allow-all, should restrict server.origins.
  - Windows "GitやPythonに馴染みが無い方": download https://github.com/litagin02/Style-Bert-VITS2/releases/latest/download/sbv2.zip → Install-Style-Bert-VITS2.bat (GPU) or Install-Style-Bert-VITS2-CPU.bat (CPU; no training). Update-Style-Bert-VITS2.bat
  - Training: "学習には2-14秒程度の音声ファイルが複数と、それらの書き起こしデータが必要です。" (multiple 2-14s audio files + transcripts)
  - Model structure: model_assets/<model>/{config.json, *.safetensors, style_vectors.npy} — share these 3
  - style_vectors.npy controls style; default average style "Neutral" generated at training. Style creation tab (StyleVectors.bat)
  - 動作環境: Windows cmd, WSL2, Linux(Ubuntu Desktop) confirmed. No NVidia GPU → no training, but synthesis and merge OK.
  - Merge tab: merge 2 models on 4 axes (声質/声の高さ/感情表現/テンポ)
  - ONNX conversion for Aivis Project (https://aivis-project.com/), AIVM Generator
  - SpeechMOS script for naturalness eval
  - Base pretrained: https://huggingface.co/litagin/Style-Bert-VITS2-1.0-base ; JP-Extra: https://huggingface.co/litagin/Style-Bert-VITS2-2.0-base-JP-Extra
  - HF space demo: https://huggingface.co/spaces/litagin/Style-Bert-VITS2-Editor-Demo
  - text/user_dict/ module = LGPL v3 (from VOICEVOX engine)
  - Editor UI in separate repo: litagin02/Style-Bert-VITS2-Editor
  - Colab: colab.ipynb

## Style-Bert-VITS2 JVNV model (HF)
- Fetched: https://hf-mirror.com/litagin/style_bert_vits2_jvnv
- License cc-by-sa-4.0 (inherited from JVNV corpus). Languages ja/zh/en. Styles: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral (7). JP-Extra version (jvnv-*-jp) plus older versions. Online demo space litagin/Style-Bert-VITS2-JVNV. 100 Spaces use it.

## IndexTTS (bilibili / index-tts)
- Fetched: https://api.github.com/repos/index-tts/index-tts → license "Other"/NOASSERTION. Stars 24,481. forks 2903. created 2025-02-06, pushed 2026-09-29.
- LICENSE fetched via ghproxy: "bilibili Model Use License Agreement" for model "bilibili indextts2"
  - Grant: worldwide, non-exclusive, non-transferable, royalty-free limited license
  - 2.2: if you/affiliates had >100M MAU previous month OR annual revenue > RMB 1 billion → must request separate license
  - 3.4(c): may not use indextts2 or Derivative Works to improve any AI model except indextts2 itself/derivatives/non-commercial AI models
  - Governed by PRC law; Shanghai Arbitration Commission
- README (via ghproxy):
  - Latest = IndexTTS-2.5 released 2026/08/10; supports Chinese, English, Japanese, Spanish, Arabic
  - 0.8B params (IndexTTS2.5). Emotion control (emo_audio_prompt, emo_alpha, emo_vector 8-dim [happy,angry,sad,afraid,disgusted,melancholic,surprised,calm]), speaking speed via duration_factor (0.5–2.0)
  - Pronunciation control: Pinyin / CMU phonemes / Japanese Kana
  - Model zoo: IndexTTS-2.5, IndexTTS-2, IndexTTS-1.5, IndexTTS
    - ModelScope: https://modelscope.cn/models/IndexTeam/IndexTTS-2.5 ; HF https://huggingface.co/IndexTeam/IndexTTS-2.5
  - Install: uv; `uv sync --all-extras`; Windows: DeepSpeed may be difficult → skip --all-extras; CUDA toolkit 12.8+ if CUDA error
  - WebUI: `uv run webui.py` → http://127.0.0.1:7860
  - BF16 (2.5) / FP16 (2) inference for lower VRAM; DeepSpeed optional
  - vLLM production recipe: https://recipes.vllm.ai/IndexTeam/IndexTTS-2.5
  - Python API: `tts.infer(spk_audio_prompt='examples/voice_01.wav', text=..., lang="EN", output_path="gen.wav")`
  - RTF on RTX 4090, kv_cache=True: IndexTTS2.0 fp16 overall 0.3257; 2.5 bf16 0.2065; 2.5 fp32 0.2060
  - Zero-shot from a single reference audio clip
  - HF_ENDPOINT=https://hf-mirror.com supported
  - Commercial contact: indexspeech@bilibili.com
  - Only official channel = github.com/index-tts/index-tts

## Fish Speech / OpenAudio (fishaudio/fish-speech)
- Fetched: https://api.github.com/repos/fishaudio/fish-speech → license Other/NOASSERTION. Stars 33,103. forks 2875. pushed 2026-10-14.
- README (via ghproxy):
  - License notice: "This codebase and its associated model weights are released under FISH AUDIO COMMUNITY LICENSE. The S2-Pro weights remain under the Fish Audio Research License."
  - Models: Drama 3 = 35B-A3B (3B active per token) → https://huggingface.co/fishaudio/drama-3 ; S2-Pro = 4B params → https://huggingface.co/fishaudio/s2-pro
  - Drama 3 features: multi-turn director revision, infilling/precise editing, scene-style multi-character production, long dialogues, stronger expressiveness (laughter/crying/whispers/dramatic emotion), multilingual voice cloning, inline tags [whisper] [angry] [laughing]
  - S2-Pro: inline tags [pause] [excited] [whisper]; native multi-speaker via speaker IDs; "Rapid voice cloning: 10–30 seconds of reference audio is enough"; single pass long audio streaming; "RTF 0.195 on a single H200, about 100 ms to first audio"
  - S2-Pro benchmarks: Seed-TTS Eval WER Chinese 0.54%, English 0.99% (best overall); Audio Turing Test 0.515; EmergentTTS-Eval win rate 81.88%
  - Install docs: https://speech.fish.audio/install/ ; inference: https://speech.fish.audio/inference/
  - Recommends SGLang-Omni for efficiency; vLLM-Omni recipe
  - Docker: hub.docker.com/r/fishaudio/fish-speech
  - Blog: https://fish.audio/blog/fish-audio-open-sources-s2/ ; papers arXiv 2610.18010 (Drama 3), 2603.08823 (S2), 2411.01156 (v1.4)
  - Website: https://fish.audio/

## Kokoro (hexgrad/kokoro)
- Fetched: https://api.github.com/repos/hexgrad/kokoro → stars 9,303, pushed 2025-08-06
- README: "open-weight TTS model with 82 million parameters ... With Apache-licensed weights". `pip install kokoro`
- NO voice cloning (fixed voice list, e.g. voice='af_heart')
- Languages via misaki packages: a=American English, b=British English, e=Spanish, f=French, h=Hindi, i=Italian, j=Japanese (pip install misaki[ja]), p=Brazilian Portuguese, z=Mandarin Chinese (pip install misaki[zh])
- 24kHz sample rate. Windows needs espeak-ng MSI install.
- Model: https://huggingface.co/hexgrad/Kokoro-82M
- G2P: https://github.com/hexgrad/misaki

## CosyVoice (FunAudioLLM/CosyVoice → now QwenAudio/CosyVoice)
- ungh.cc says repo is "QwenAudio/CosyVoice" now. Stars 23,958. pushed 2026-05-25.
- HF CosyVoice2-0.5B: https://hf-mirror.com/FunAudioLLM/CosyVoice2-0.5B → License apache-2.0, 9 languages, ONNX + Safetensors
  - CosyVoice 2.0 ModelScope https://www.modelscope.cn/models/iic/CosyVoice2-0.5B ; HF https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B
  - CosyVoice 1.0 (300M): ModelScope iic/CosyVoice-300M
  - **Fun-CosyVoice 3.0**: demos https://funaudiollm.github.io/cosyvoice3/ ; paper arXiv 2505.17589 ; ModelScope https://www.modelscope.cn/models/FunAudioLLM/Fun-CosyVoice3-0.5B-2512 ; HF https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512 ; CV3-Eval https://github.com/FunAudioLLM/CV3-Eval
  - Papers: 2505.17589 (v3), 2412.10117 (v2), 2407.05407 (v1)

## Other repo metadata (ungh.cc)
- F5-TTS (SWivid/F5-TTS): stars 15,403, pushed 2026-10-11. HF model license: **cc-by-nc-4.0** (non-commercial!). HF: https://hf-mirror.com/SWivid/F5-TTS
- Chatterbox (resemble-ai/chatterbox): stars 26,941, pushed 2026-07-21
- edge-tts (rany2/edge-tts): stars 12,276, pushed 2026-10-14
- IndexTTS repo (index-tts/index-tts): see above
