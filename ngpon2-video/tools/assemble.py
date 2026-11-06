"""Concatenate rendered segments (each with its own audio) into one episode file; narration segments are
loudness-normalised to -16 LUFS, music segments are taken as-is. Writes Turkish soft subtitles from timelines."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from finalize import make_srt, srt_time

def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

def run(spec_path, out):
    spec = json.loads(Path(spec_path).read_text())  # [{"video":..., "norm":bool, "timeline":..., "manifest":...}]
    ins, fc, rows, offset = [], [], [], 0.0
    for i, seg in enumerate(spec):
        ins += ["-i", seg["video"]]
        a = f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo"
        a += ",loudnorm=I=-16:LRA=11:TP=-1.5,aresample=48000" if seg.get("norm") else ""
        fc.append(f"{a}[a{i}];[{i}:v]fps=30,format=yuv420p[v{i}]")
        if seg.get("timeline"):
            tmp = Path(out).with_suffix(f".seg{i}.srt")
            make_srt(json.loads(Path(seg["timeline"]).read_text()), json.loads(Path(seg["manifest"]).read_text()), tmp)
            for block in tmp.read_text(encoding="utf-8").strip().split("\n\n"):
                _, tc, text = block.split("\n", 2)
                a0, a1 = [sum(float(x) * m for x, m in zip(t.replace(",", ".").split(":"), (3600, 60, 1))) for t in tc.split(" --> ")]
                rows.append((a0 + offset, a1 + offset, text))
            tmp.unlink()
        offset += dur(seg["video"])
    n = len(spec)
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    srt = Path(out).with_suffix(".tr.srt")
    srt.write_text("".join(f"{k}\n{srt_time(a)} --> {srt_time(z)}\n{t}\n\n" for k, (a, z, t) in enumerate(rows, 1)), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-i", str(srt), "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", "-map", f"{n}:s", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-metadata:s:s:0", "language=tur",
                    "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"{dur(out):.1f}s")

if __name__ == "__main__":
    run(*sys.argv[1:3])
