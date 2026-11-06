"""Grid of end-of-beat frames for chosen beats: pick.py out.png Class:timeline:beat[,beat] ..."""
import json, subprocess, sys, glob, tempfile
from pathlib import Path
out, specs = sys.argv[1], sys.argv[2:]
tmp = Path(tempfile.mkdtemp()); fr = []
for sp in specs:
    c, tl, beats = sp.split(":")
    v = sorted(glob.glob(f"build/media_{c}/videos/*/*/{c}.mp4"), key=lambda p: Path(p).stat().st_mtime)[-1]
    t = {b["id"]: b for b in json.load(open(f"build/{tl}_timeline.json"))}
    for bid in beats.split(","):
        b = t[bid]; fn = tmp / f"{len(fr):03d}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{b['start'] + b['dur'] + 0.2:.2f}", "-i", v, "-frames:v", "1",
                        "-vf", f"scale=640:360,drawtext=text='{c} {bid}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6", str(fn)], check=True)
        fr.append(fn)
cols = 3; args = []
for f in fr: args += ["-i", str(f)]
lay = "|".join(f"{(j % cols) * 640}_{(j // cols) * 360}" for j in range(len(fr)))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", f"xstack=inputs={len(fr)}:layout={lay}:fill=black", out], check=True)
print(out)
