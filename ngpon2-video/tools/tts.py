"""Gemini TTS: narration JSON -> per-beat WAV (24 kHz mono) + manifest with durations. Cached by content hash."""
import base64, hashlib, json, sys, time, urllib.request, wave, io
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"

def synth(model, voice, style, text, retries=4):
    prompt = f"{style}\n\n{text}" if style else text
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for i in range(retries):
        try:
            req = urllib.request.Request(API.format(model), data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
            r = json.load(urllib.request.urlopen(req, timeout=300))
            d = r["candidates"][0]["content"]["parts"][0]["inlineData"]
            raw = base64.b64decode(d["data"])
            if raw[:4] == b"RIFF":  # some models return a full WAV container
                with wave.open(io.BytesIO(raw)) as w:
                    assert w.getframerate() == 24000 and w.getnchannels() == 1
                    raw = w.readframes(w.getnframes())
            return raw
        except Exception as e:
            print(f"  retry {i+1}: {e}", file=sys.stderr); time.sleep(2 ** (i + 1))
    raise RuntimeError("TTS failed")

def run(script_path, out_dir, voice=None, model=None):
    s = json.loads(Path(script_path).read_text())
    voice, model = voice or s["voice"], model or s["model"]
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    def job(b):
        key = hashlib.sha1(f"{model}|{voice}|{s['style']}|{b['text']}".encode()).hexdigest()[:10]
        fn = out / f"{b['id']}_{key}.wav"
        if not fn.exists():
            pcm = synth(model, voice, s["style"], b["text"])
            with wave.open(str(fn), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
        with wave.open(str(fn)) as w: dur = w.getnframes() / w.getframerate()
        print(f"{b['id']:10s} {dur:6.2f}s  {fn.name}")
        return {"id": b["id"], "file": str(fn.resolve()), "duration": dur, "text": b["text"]}
    with ThreadPoolExecutor(6) as ex: beats = list(ex.map(job, s["beats"]))
    man = {"voice": voice, "model": model, "beats": beats, "total": sum(b["duration"] for b in beats)}
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(f"total narration: {man['total']:.1f}s")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(sys.argv[3:5]))
