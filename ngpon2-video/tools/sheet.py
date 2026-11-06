"""Contact sheet: one frame near the end of every beat (+ optional mid frame) → tiled PNG(s) for layout review.
usage: sheet.py video.mp4 timeline.json out_prefix [cols]"""
import json, subprocess, sys, tempfile
from pathlib import Path

def run(video, timeline, out, cols=4):
    tl = json.loads(Path(timeline).read_text())
    tmp = Path(tempfile.mkdtemp())
    frames = []
    for i, b in enumerate(tl):
        for tag, t in (("m", b["start"] + b["dur"] * 0.5), ("e", b["start"] + b["dur"] + 0.2)):
            fn = tmp / f"{i:03d}{tag}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                            "-vf", f"scale=480:-1,drawtext=text='{b['id']} {tag}':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6",
                            str(fn)], check=True)
            if fn.exists():
                frames.append(fn)
    per = cols * 6
    for k in range(0, len(frames), per):
        chunk = frames[k:k + per]
        rows = (len(chunk) + cols - 1) // cols
        lst = tmp / f"l{k}.txt"
        args = []
        for f in chunk: args += ["-i", str(f)]
        layout = "|".join(f"{(j % cols) * 480}_{(j // cols) * 270}" for j in range(len(chunk)))
        o = f"{out}_{k // per}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex",
                        f"xstack=inputs={len(chunk)}:layout={layout}:fill=black" if len(chunk) > 1 else "null", o], check=True)
        print(o)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3], *(int(x) for x in sys.argv[4:5]))
