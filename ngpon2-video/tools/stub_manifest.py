"""Silent stand-in manifest (estimated durations) so scenes can be laid out before TTS exists.
usage: stub_manifest.py NN part [cps=13.4] → build/epNN/part/audio_proc/manifest.json (only if no real one exists, unless --force)"""
import json, re, sys, wave
from pathlib import Path
ep, part = sys.argv[1], sys.argv[2]
cps = float(next((a for a in sys.argv[3:] if not a.startswith("--")), 13.4))
root = Path(__file__).resolve().parent.parent
out = root / f"build/ep{ep}/{part}/audio_proc/manifest.json"
if out.exists() and not json.loads(out.read_text()).get("stub") and "--force" not in sys.argv:
    sys.exit(0)
sil = root / "build/silence1s.wav"
if not sil.exists():
    with wave.open(str(sil), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b"\0\0" * 48000)
beats = []
for b in json.loads((root / f"script/ep{ep}_{part}.json").read_text())["beats"]:
    dur = len(b["text"]) / cps
    ph = [x.strip() for x in re.split(r"(?<=[.,:;])\s+", b["text"]) if x.strip()]
    tot, acc, cues = sum(map(len, ph)), 0, []
    for x in ph:
        cues.append({"text": x, "t": round(dur * acc / tot, 2)}); acc += len(x)
    beats.append({"id": b["id"], "file": str(sil), "duration": round(dur, 2), "text": b["text"], "cues": cues})
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"beats": beats, "total": sum(b["duration"] for b in beats), "stub": True}, ensure_ascii=False, indent=1))
