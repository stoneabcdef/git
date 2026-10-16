# HF model search results (verified via https://hf-mirror.com/api/models?search=...)

## search=GPT-SoVITS (fetched 2026-10-14)
Anime/game character + other community finetunes:
- `MomoyamaSawa/GPT-SoVITS_KusanagiNene` — 草薙寧々 (Project Sekai), tags pjsk/プロセカ, lang zh/ja/en, license gpl-3.0, likes 43, created 2024-01-29
- `2DIPW/ATRI_GPT-SoVITS` — ATRI, license cc-by-nc-sa-4.0, likes 14
- `Killuazyt/kurisu-gpt-sovits-v5turbo-20261012` — kurisu (Steins;Gate), v5turbo, lora, ja/zh, created 2026-10-12, base lj1995/GPT-SoVITS
- `MondMeer/GPT-SoVITS-HiiragiHakua` — 柊白亜/Hakua, zh, license gpl-3.0
- `baicai1145/GPT-SoVITS-STAR` — license mit, likes 62
- `modelloosrvcc/Kotoko_Utsugi_GPT-SOVITS`, `modelloosrvcc/Nagisa_Shingetsu_GPT-SoVITS`
- `shibing624/parrots-gpt-sovits-speaker` — zh/ja/en, license **cc-by-nc-4.0** (non-commercial), endpoints_compatible
- `shibing624/parrots-gpt-sovits-speaker-maimai` — zh, cc-by-nc-4.0, endpoints_compatible
- `AkitoP/GPT-SoVITS-JA-ProsodyControl_model` — apache-2.0 (Japanese prosody control)
- `fuckSelf/GPT-SoVITS-Russian` — mit
- `lj1995/GPT-SoVITS` — official pretrained, license mit, likes 427 (downloads field 0 = not tracked)
- `lj1995/GPT-SoVITS-windows-package` — likes 112, license mit  (<< the one-click Windows package repo)
- Also non-anime: RoversX/GPT_SOVITS_LeiJun_V1, RoversX/gpt-sovits-Arthur-Morgan-V1, Coolwowsocoolwow/Spongebob-GPT-SoVITS, Sprt98/GPT-SoVITS_Yasuo

## search=style-bert-vits2 (fetched 2026-10-14)
- `litagin/style_bert_vits2_jvnv` — official JVNV, cc-by-sa-4.0, ja/zh/en, likes 11
- `litagin/Style-Bert-VITS2-1.0-base` — base pretrained, ja/zh/en
- `litagin/Style-Bert-VITS2-2.0-base-JP-Extra` — license agpl-3.0, likes 20
- `RikkaBotan/style_bert_vits2_jp_extra_sweet_original` — cc-by-sa-4.0, ja, downloads 129  (childish/cute voice)
- `RikkaBotan/style_bert_vits2_jp_extra_cool_original` — cc-by-sa-4.0, ja, downloads 132
- `RikkaBotan/style_bert_vits2_jp_extra_asmr_original` — cc-by-sa-4.0, downloads 112
- `RikkaBotan/style_bert_vits2_english_original` — cc-by-sa-4.0, en, 57
- `RikkaBotan/style_bert_vits2_chinese_original` — cc-by-sa-4.0, zh, 162
- `ayousanz/tsukuyomi-chan-style-bert-vits2-model` — つくよみちゃん, downloads 246, license other, finetune of 2.0-base-JP-Extra
- `RinneAi/Rinne_Style-Bert-VITS2` — cc-by-sa-4.0, ja, likes 11
- `Mofa-Xingche/girl-style-bert-vits2-JPExtra-models` — license mit, downloads 101, tags japanese/female/bertvits2
- `Lycoris53/style-bert-vits2-sakura-miko` — ja, likes 2, license other
- `zgock/style-bert-vits2-zonoko-cc0` — **cc0-1.0** (public domain!), ja
- `kaunista/style-bert-vits2-Anneli` — creativeml-openrail-m, likes 34
- `SOashi/Style_Bert_VITS2_JP_taro` — mit
- NOTE: also many models of REAL politicians (AbeShinzo0708/AbeShinzo_Style_Bert_VITS2, KishidaFumio, SugaYoshihide, NikaiToshihiro, license apache-2.0 label) — a good concrete example of the ethics problem: real-person political clones distributed openly on HF.
- `AbeShinzo0708/AbeShinzo_Style_Bert_VITS2` etc. — real-person clones

KEY INSIGHT: both ecosystems have openly distributed anime-character finetunes on HuggingFace, with varying licenses (gpl-3.0, cc-by-nc-sa-4.0, mit, cc-by-sa-4.0, cc0). Many are third-party and the character/VA rights are NOT cleared.

## GPT-SoVITS api_v2.py full source (fetched via ghproxy, main branch 2026-10)
- Launch: `python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml`
- Endpoints: 
  - `GET/POST /tts` — returns wav audio stream (HTTP 200) or JSON error (400)
  - `GET /control?command=restart|exit`
  - `GET /set_gpt_weights?weights_path=...`
  - `GET /set_sovits_weights?weights_path=...`
  - `GET /set_refer_audio?refer_audio_path=...`
- POST /tts body fields: text(req), text_lang(req), ref_audio_path(req), aux_ref_audio_paths(opt, multi-speaker tone fusion), prompt_text, prompt_lang(req), top_k=15, top_p=1, temperature=1, text_split_method="cut5", batch_size=1, batch_threshold=0.75, split_bucket=True, speed_factor=1.0, fragment_interval=0.3, seed=-1, media_type=wav|raw|ogg|aac, streaming_mode (0/1/2/3 or bool: 1=best quality slowest, 2=medium, 3=lower quality faster), parallel_infer=True, use_cuda_graph=True, repetition_penalty=1.35, sample_steps, cfg_rate, super_sampling, overlap_length=2, min_chunk_length=16
- **NO OpenAI-compatible `/v1/audio/speech` endpoint.** Not in api_v2.py. Model switching IS supported at runtime via /set_gpt_weights + /set_sovits_weights (contradicts the older jianchang512 claim — this is the newer upstream api_v2.py).
- Media types supported: wav, raw, ogg, aac
- Ref audio is a PATH on the server, not an upload (POST upload is commented out).
