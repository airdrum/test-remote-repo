"""Quota-friendly Gemini TTS: synthesize several beats per request, then split the audio back into beats at the
pauses nearest to the expected (character-proportional) boundaries. Same manifest format as tools/tts.py."""
import hashlib, json, os, re, subprocess, sys, wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tts import synth
from lexicon import speak

SR = 24000

def silences(path, db=-38, d=0.22):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return list(zip(st, en))

def groups_of(beats, max_chars):
    g, n = [], 0
    for b in beats:
        if g and n + len(b["text"]) > max_chars:
            yield g; g, n = [], 0
        g.append(b); n += len(b["text"])
    if g: yield g

def run(script_path, out_dir, model=None, voice=None, max_chars=820, workers=2):
    s = json.loads(Path(script_path).read_text())
    model, voice = model or s["model"], voice or s["voice"]
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    groups = list(groups_of(s["beats"], max_chars))

    def job(gi_g):
        gi, g = gi_g
        text = "\n\n".join(speak(b["text"]) for b in g)
        key = hashlib.sha1(f"{model}|{voice}|{s['style']}|{text}".encode()).hexdigest()[:10]
        gf = out / f"grp{gi:02d}_{key}.wav"
        if not gf.exists():
            pcm = synth(model, voice, s["style"], text)
            with wave.open(str(gf), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)
        with wave.open(str(gf)) as w:
            pcm = w.readframes(w.getnframes()); dur = w.getnframes() / SR
        # boundaries
        sil = [(a, e) for a, e in silences(str(gf)) if a > 0.3 and e < dur - 0.3 and e - a >= 0.25]
        lens = [len(speak(b["text"])) for b in g]; tot = sum(lens); cuts, acc, prev = [], 0, 0.0
        for L in lens[:-1]:
            acc += L; exp = dur * acc / tot
            cand = [(abs((a + e) / 2 - exp) - 3.0 * (e - a), (a + e) / 2) for a, e in sil if (a + e) / 2 > prev + 1.0]
            c = min(cand)[1] if cand else exp
            cuts.append(c); prev = c
        edges = [0.0] + cuts + [dur]
        res = []
        for b, a, e in zip(g, edges[:-1], edges[1:]):
            fn = out / f"{b['id']}_{key}.wav"
            seg = pcm[int(a * SR) * 2:int(e * SR) * 2]
            with wave.open(str(fn), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(seg)
            res.append({"id": b["id"], "file": str(fn.resolve()), "duration": round(e - a, 3), "text": b["text"]})
        print(f"group {gi:02d}: {len(g)} beats, {dur:5.1f}s, cuts " + " ".join(f"{c:.1f}" for c in cuts), flush=True)
        return res

    with ThreadPoolExecutor(workers) as ex:
        beats = [b for r in ex.map(job, enumerate(groups)) for b in r]
    man = {"voice": voice, "model": model, "beats": beats, "total": sum(b["duration"] for b in beats)}
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(f"{script_path}: {len(groups)} requests, {len(beats)} beats, {man['total']:.1f}s")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(sys.argv[3:4] or [None]))
