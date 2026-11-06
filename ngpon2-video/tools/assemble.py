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
        if seg.get("norm"):  # two-pass style: measure integrated loudness, apply a fixed gain (no pumping)
            err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", seg["video"], "-map", "0:a", "-af", "ebur128",
                                  "-f", "null", "-"], capture_output=True, text=True).stderr
            I = float(err.split("Summary:")[1].split("I:")[1].split("LUFS")[0])
            a += f",volume={-16 - I:.2f}dB,alimiter=limit=0.84:level=false"
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
    import os
    subs = os.environ.get("NO_SUBS") != "1"
    cmd = ["ffmpeg", "-y", "-v", "error", *ins] + (["-i", str(srt)] if subs else []) + ["-filter_complex", ";".join(fc),
           "-map", "[v]", "-map", "[a]"] + (["-map", f"{n}:s", "-c:s", "mov_text", "-metadata:s:s:0", "language=tur"] if subs else []) + \
          ["-c:v", "libx264", "-crf", os.environ.get("CRF", "18"), "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("wrote", out, f"{dur(out):.1f}s")

if __name__ == "__main__":
    run(*sys.argv[1:3])
