"""Persist TTS output across container restarts (build/ is not in git).
pack:   audio_cache.py pack build/ep03/p1/audio audio_cache/ep03/p1   → FLAC of every wav + manifest with relative names
unpack: audio_cache.py unpack audio_cache/ep03/p1 build/ep03/p1/audio → wavs back + manifest with absolute paths
Group wavs (g*_k.wav) are kept too: tts_robust treats them as a cache, so finished groups are never re-synthesised."""
import json, shutil, subprocess, sys
from pathlib import Path


def _flac(w, f):
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-c:a", "flac", "-compression_level", "8", str(f)], check=True)
    else:  # GPU machine without ffmpeg: soundfile (installed in .venv-xtts) writes the same lossless FLAC
        import soundfile as sf
        data, sr = sf.read(str(w), dtype="int16")
        sf.write(str(f), data, sr, format="FLAC", subtype="PCM_16")


def pack(src, dst):
    src, dst = Path(src), Path(dst); dst.mkdir(parents=True, exist_ok=True)
    for w in sorted(src.glob("*.wav")):
        _flac(w, dst / (w.stem + ".flac"))
    m = src / "manifest.json"
    if m.exists():
        man = json.loads(m.read_text())
        for b in man["beats"]:
            b["file"] = Path(b["file"]).name
        (dst / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))


def unpack(src, dst):
    src, dst = Path(src), Path(dst); dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("*.flac")):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(f), "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(dst / (f.stem + ".wav"))], check=True)
    m = src / "manifest.json"
    if m.exists():
        man = json.loads(m.read_text())
        for b in man["beats"]:
            b["file"] = str((dst / b["file"]).resolve())
        (dst / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"pack": pack, "unpack": unpack}[sys.argv[1]](sys.argv[2], sys.argv[3])
