"""Robust grouped Gemini TTS → per-beat clips.

1. Synthesize a group of beats in one request (quota friendly).
2. Group QA: transcribe the group and compare with the script (catches repeated / skipped paragraphs).
   Retry up to 2×; if still bad, fall back to one request per beat.
3. Boundaries: ask Gemini for paragraph start times, snap each to the nearest pause.
4. Beat QA: first/last words of every beat must match the script.
Manifest format is identical to tools/tts.py.
"""
import difflib, hashlib, json, re, subprocess, sys, wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tts import synth
from lexicon import speak
from qa_tts import transcribe as _transcribe
from align import para_starts
import functools, os

QA = os.environ.get("TTS_QA", "1") != "0"  # TTS_QA=0: no Gemini transcription (e.g. no GEMINI_API_KEY on the GPU machine)


@functools.lru_cache(maxsize=None)
def transcribe(path):  # each clip is transcribed once (synth QA and boundary QA share it)
    return _transcribe(path)

SR = 24000
NUM = set("bir iki üç dört beş altı yedi sekiz dokuz on yirmi otuz kırk elli altmış yetmiş seksen doksan yüz bin milyon virgül nokta eksi artı".split())


def words(s):
    s = s.lower().replace("'", " ").replace("’", " ")
    return [w for w in re.findall(r"[a-zçğıöşüâî]+", s) if len(w) >= 3 and w not in NUM]


def similar(expected, got):
    e, g = words(expected), words(got)
    if not e or not g:
        return 0.0, 0.0
    return difflib.SequenceMatcher(None, e, g).ratio(), len(g) / len(e)


def silences(path, db=-38, d=0.2):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return list(zip(st, en))


def write_wav(fn, pcm):
    with wave.open(str(fn), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)


def read_wav(fn):
    with wave.open(str(fn)) as w:
        return w.readframes(w.getnframes())


def groups_of(beats, max_chars):
    g, n = [], 0
    for b in beats:
        if g and n + len(b["text"]) > max_chars:
            yield g; g, n = [], 0
        g.append(b); n += len(b["text"])
    if g:
        yield g


def run(script_path, out_dir, max_chars=700, workers=2, log=print):
    s = json.loads(Path(script_path).read_text())
    model, voice, style = s["model"], s["voice"], s.get("style", "")
    from tts import BACKEND
    if BACKEND == "xtts":  # one beat per request (no group cutting), one GPU model, no style prompt
        import os
        # speaker: env override > script's "xtts_speaker" (season 2 sets a female voice) > Damien Black (season 1)
        model, voice, style = "xtts-v2", os.environ.get("XTTS_SPEAKER") or s.get("xtts_speaker") or "Damien Black", ""
        max_chars, workers = 1, 1
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    groups = list(groups_of(s["beats"], max_chars))

    def synth_ok(key, text_spoken, text_display, tries=3):
        """Synthesize with QA; returns (path, pcm) or (None, None)."""
        for k in range(tries):
            fn = out / f"{key}_{k}.wav"
            if not fn.exists():
                write_wav(fn, synth(model, voice, style, text_spoken, seed=1234 + 101 * k))
            if not QA:
                return fn, read_wav(fn)
            tx = transcribe(str(fn))
            sim, ratio = similar(text_display, tx)
            if sim >= 0.8 and 0.85 <= ratio <= 1.15:
                return fn, read_wav(fn)
            log(f"   {key} try{k}: sim={sim:.2f} len={ratio:.2f} → retry")
        return None, None

    def job(gi_g):
        gi, g = gi_g
        spoken = [speak(b["text"]) for b in g]
        key = "g" + hashlib.sha1(f"{model}|{voice}|{style}|{'¶'.join(spoken)}".encode()).hexdigest()[:10]
        fn, pcm = synth_ok(key, "\n\n".join(spoken), " ".join(b["text"] for b in g)) if len(g) > 1 else (None, None)
        res = []
        if fn is not None:
            dur = len(pcm) / 2 / SR
            starts = para_starts(str(fn), spoken) or []
            sil = [((a + e) / 2, e - a) for a, e in silences(str(fn)) if 0.3 < a and e < dur - 0.2]
            cuts = []
            for i in range(1, len(g)):
                t = starts[i] if len(starts) == len(g) else dur * sum(map(len, spoken[:i])) / sum(map(len, spoken))
                near = [(abs(m - (t - 0.1)) - 0.8 * d, m) for m, d in sil if abs(m - t) < 1.6 and (not cuts or m > cuts[-1] + 1.0)]
                cuts.append(min(near)[1] if near else t - 0.12)
            edges = [0.0] + cuts + [dur]
            for b, a, e in zip(g, edges[:-1], edges[1:]):
                bf = out / f"{b['id']}_{key}.wav"
                write_wav(bf, pcm[int(a * SR) * 2:int(e * SR) * 2])
                res.append({"id": b["id"], "file": str(bf.resolve()), "duration": round(e - a, 3), "text": b["text"]})
            log(f"group {gi:02d}: {len(g)} beats in 1 request, {dur:.1f}s, cuts " + " ".join(f"{c:.1f}" for c in cuts))
        else:
            if len(g) > 1:
                log(f"group {gi:02d}: falling back to per-beat requests")
            for b, sp in zip(g, spoken):
                k1 = "b" + hashlib.sha1(f"{model}|{voice}|{style}|{sp}".encode()).hexdigest()[:10]
                bf, bp = synth_ok(k1, sp, b["text"])
                if bf is None:  # accept the last attempt but flag it
                    bf = out / f"{k1}_2.wav"; bp = read_wav(bf); log(f"   !! {b['id']} accepted with QA warning")
                res.append({"id": b["id"], "file": str(Path(bf).resolve()), "duration": round(len(bp) / 2 / SR, 3), "text": b["text"]})
        # beat-level QA on boundaries
        for r in res:
            if not QA:
                r["qa"] = "skipped"; continue
            tx = transcribe(r["file"])
            ew, tw = words(r["text"]), words(tx)
            head = sum(w in tw[:12] for w in ew[:3]) >= 2 if len(ew) >= 3 else True
            tail = sum(w in tw[-12:] for w in ew[-3:]) >= 2 if len(ew) >= 3 else True
            r["qa"] = "ok" if head and tail else f"head={int(head)} tail={int(tail)}"
            if r["qa"] != "ok":
                log(f"   BEAT {r['id']}: {r['qa']} → {tx[:140]}")
        return res

    with ThreadPoolExecutor(workers) as ex:
        beats = [b for r in ex.map(job, enumerate(groups)) for b in r]
    man = {"voice": voice, "model": model, "beats": beats, "total": round(sum(b["duration"] for b in beats), 2)}
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    bad = [b["id"] for b in beats if b.get("qa") not in ("ok", "skipped")]
    log(f"{script_path}: {len(beats)} beats, {man['total']:.1f}s, QA issues: {bad or 'none'}")
    return bad


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
