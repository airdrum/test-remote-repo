"""Post-process TTS beats: trim edge silence, gentle tempo-up, 48 kHz; derive phrase cue times (for animation sync)."""
import json, re, subprocess, sys, wave
from pathlib import Path

def silences(path, db=-42, d=0.18):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", f"silencedetect=n={db}dB:d={d}",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return list(zip(st, en))

def run(manifest_in, out_dir, tempo=1.08):
    m = json.loads(Path(manifest_in).read_text()); out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    trim = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05"
    stretch = f"rubberband=tempo={tempo}:transients=mixed:formant=preserved:pitchq=quality" if abs(tempo - 1) > 1e-3 else "anull"
    af = f"{trim},areverse,{trim},areverse,{stretch},aresample=48000"
    for b in m["beats"]:
        fn = out / Path(b["file"]).name
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", b["file"], "-af", af, "-ac", "1", str(fn)], check=True)
        with wave.open(str(fn)) as w: dur = w.getnframes() / w.getframerate()
        # phrase cues: split on punctuation, estimate by char share, snap to nearest detected pause end
        phrases = [p.strip() for p in re.split(r"(?<=[.,:;])\s+", b["text"]) if p.strip()]
        total = sum(len(p) for p in phrases); acc = 0; ends = [e for s, e in silences(str(fn))]
        cues = []
        for p in phrases:
            est = dur * acc / total
            near = min(ends, key=lambda e: abs(e - est)) if ends and acc else None
            t = near if (near is not None and abs(near - est) < 0.9) else est
            cues.append({"text": p, "t": round(t, 2)}); acc += len(p)
        b.update(file=str(fn.resolve()), duration=round(dur, 3), cues=cues)
        print(f"{b['id']:10s} {dur:5.2f}s  " + " | ".join(f"{c['t']:.1f}" for c in cues))
    m["total"] = round(sum(b["duration"] for b in m["beats"]), 2); m["tempo"] = tempo
    (out / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=1)); print("total", m["total"])

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(float(x) for x in sys.argv[3:4]))
