"""List 'file.py:Class' for scenes of episode NN whose 1080p render is missing or older than their scene file
or their part's processed audio. usage: stale_scenes.py NN [force=0|1]"""
import json, os, sys

ep = sys.argv[1]
force = len(sys.argv) > 2 and sys.argv[2] == "1"
t = lambda f: os.path.getmtime(f) if os.path.exists(f) else 0
out = []
for c, f, tl, p in json.load(open(f"plan/ep{ep}_order.json")):
    if not f:
        continue
    mp4 = f"build/media_{c}/videos/{f}/1080p30/{c}.mp4"
    newest_input = max(t(f"scenes/{f}.py"), t(f"build/ep{ep}/{p}/audio_proc/manifest.json"))
    if force or t(mp4) == 0 or t(mp4) < newest_input:
        out.append(f"{f}.py:{c}")
print(" ".join(out))
