#!/usr/bin/env python3
"""
为一/多个动漫角色在硅基流动创建自定义音色（云端克隆）。

用法：
    set SF_KEY=sk-xxxx
    python setup-voices.py

或直接：
    python setup-voices.py sk-xxxx

它会：
  1. 上传每个角色的参考音频到 /v1/uploads/audio/voice
  2. 打印返回的 voice uri（形如 speech:kurisu:xxxx:yyyy）
  3. 把 uri 写进 voices.json，并生成可直接粘贴的 cordis.patch.yml 片段
"""
import base64
import json
import os
import sys
from pathlib import Path

import urllib.request
import urllib.error

BASE = "https://api.siliconflow.cn/v1"
MODEL = "FunAudioLLM/CosyVoice2-0.5B"
HERE = Path(__file__).resolve().parent

# 角色表：显示名 -> (参考音频文件, 参考音频逐字稿, 语言)
VOICES = {
    "kurisu": {
        "file": "kurisu.ja.wav",
        "text": "2週間だけ、菖蒲院に逆留学みたいなことしてたんだけど、そこの制服を改造して着てるの",
        "note": "牧濑红莉栖 (Steins;Gate) / 今井麻美 / 6.53s",
    },
    "nanami": {
        "file": "nanami.ja.wav",
        "text": "違うね、小前田くん もしかしてまだ何か隠してるんじゃないの あの停電の時。",
        "note": "七海千秋 (弹丸论破2) / 花泽香菜 / 8.70s",
    },
}


def post_json(url, payload, key, timeout=90):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        raise SystemExit(f"HTTP {e.code}: {body}")


def get_json(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        raise SystemExit(f"HTTP {e.code}: {body}")


def mime_for(p: Path) -> str:
    return {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".pcm": "audio/pcm",
        ".opus": "audio/opus",
    }.get(p.suffix.lower(), "audio/wav")


def main():
    key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SF_KEY", "")
    if not key:
        raise SystemExit("需要 API key：python setup-voices.py sk-xxxx   （或设 SF_KEY）")

    print("检查 key ...")
    try:
        lst = get_json(f"{BASE}/audio/voice/list", key)
        print("  已授权，现有自定义音色：", len(lst.get("data", lst) if isinstance(lst, dict) else lst))
    except SystemExit as e:
        raise SystemExit(f"key 校验失败 -> {e}")

    out = {}
    for name, spec in VOICES.items():
        p = HERE / spec["file"]
        if not p.exists():
            print(f"[跳过] {name}: 缺文件 {p}")
            continue
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        print(f"上传 {name} ({spec['note']}) ...")
        res = post_json(
            f"{BASE}/uploads/audio/voice",
            {
                "model": MODEL,
                "customName": name,
                "audio": f"data:{mime_for(p)};base64,{b64}",
                "text": spec["text"],
            },
            key,
        )
        uri = res.get("uri") or res.get("data", {}).get("uri")
        print(f"  -> {uri}")
        out[name] = {"uri": uri, "note": spec["note"], "text": spec["text"]}

    (HERE / "voices.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n=== 音色 ID ===")
    for k, v in out.items():
        print(f"{k}: {v['uri']}")

    default = next(iter(out.values()))["uri"] if out else ""
    print("\n=== 可粘贴到 cordis.patch.yml 的片段 ===")
    print(
        f"""- id: dsh-voice-chat
  name: 'dsh-voice-chat'
  config:
    ttsEngine: custom
    tts:
      custom:
        baseUrl: https://api.siliconflow.cn/v1
        model: {MODEL}
        voice: "{default}"
"""
    )
    print("换角色只需改 voice 那一行。")


if __name__ == "__main__":
    main()
