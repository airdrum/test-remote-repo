"""Mark single beats for re-voicing: deletes their clips (build/ and audio_cache/) and the part manifests,
so the next `bash tools/local_all.sh NN` voices only those beats and re-preps/re-renders only the affected parts.
usage: python tools/revoice.py 09 p4:e3,e5 lab:g2 end:h1"""
import json, sys
from pathlib import Path

ep = sys.argv[1]
for spec in sys.argv[2:]:
    part, ids = spec.split(":")
    ids = set(ids.split(","))
    b_dir, c_dir = Path(f"build/ep{ep}/{part}/audio"), Path(f"audio_cache/ep{ep}/{part}")
    man = b_dir / "manifest.json" if (b_dir / "manifest.json").exists() else c_dir / "manifest.json"
    beats = json.loads(man.read_text(encoding="utf-8"))["beats"]
    for b in beats:
        if b["id"] in ids:
            stem = Path(b["file"]).stem.rsplit("_", 1)[0]  # b<hash>; removes every try variant _0/_1/_2
            for f in list(b_dir.glob(stem + "_*.wav")) + list(c_dir.glob(stem + "_*.flac")):
                f.unlink()
                print("removed", f)
            b_dir.mkdir(parents=True, exist_ok=True)
            (b_dir / f"{stem}.bump").write_text("new seed on next voicing\n")
            ids.discard(b["id"])
    for m in (b_dir / "manifest.json", c_dir / "manifest.json"):
        if m.exists():
            m.unlink()
    if ids:
        print("not found:", part, sorted(ids))
print("now run: bash tools/local_all.sh", ep)
