"""Mix narration (from Manim render) with a ducked music bed, loudness-normalise, attach Turkish soft subtitles."""
import json, subprocess, sys
from pathlib import Path

def srt_time(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"

def make_srt(timeline, manifest, out, max_chars=84):
    cues = {b["id"]: b["cues"] for b in manifest["beats"]}
    rows = []
    for b in timeline:
        ph = cues[b["id"]]; chunk, t_start = [], None
        for i, c in enumerate(ph):
            if t_start is None: t_start = c["t"]
            chunk.append(c["text"])
            nxt = ph[i + 1]["t"] if i + 1 < len(ph) else b["dur"]
            if i + 1 == len(ph) or len(" ".join(chunk + [ph[i + 1]["text"]])) > max_chars or chunk[-1].endswith("."):
                rows.append((b["start"] + t_start, b["start"] + nxt - 0.05, " ".join(chunk))); chunk, t_start = [], None
    Path(out).write_text("".join(f"{i}\n{srt_time(a)} --> {srt_time(z)}\n{t}\n\n" for i, (a, z, t) in enumerate(rows, 1)),
                         encoding="utf-8")

def run(video, music, timeline, manifest, out, music_db=-27):
    tl = json.loads(Path(timeline).read_text()); man = json.loads(Path(manifest).read_text())
    srt = Path(out).with_suffix(".tr.srt"); make_srt(tl, man, srt)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]))
    fc = (f"[1:a]aresample=48000,volume={music_db}dB,afade=t=in:d=2,afade=t=out:st={dur - 3.5:.2f}:d=3.5,apad,"
          f"atrim=0:{dur:.3f}[m];"
          "[0:a]aresample=48000,asplit=2[v1][v2];"
          "[m][v2]sidechaincompress=threshold=0.02:ratio=4:attack=20:release=600:makeup=1[md];"
          "[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-16:LRA=11:TP=-1.5,aresample=48000[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", music, "-i", str(srt), "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-map", "2:s", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-c:s", "mov_text", "-metadata:s:s:0", "language=tur", "-movflags", "+faststart", out], check=True)
    print("wrote", out, "and", srt)

if __name__ == "__main__":
    run(*sys.argv[1:6])
