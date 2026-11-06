#!/usr/bin/env bash
# Back up finished TTS parts of an episode to audio_cache/epNN (beat clips only, FLAC). usage: cache_ep.sh NN
cd "$(dirname "$0")/.."
EP=$1
for d in build/ep$EP/*/audio; do
  p=$(basename "$(dirname "$d")")
  [ -f "$d/manifest.json" ] || continue
  [ -f audio_cache/ep$EP/$p/manifest.json ] && cmp -s <(python3 -c "import json;print(sorted(b['file'].split('/')[-1] for b in json.load(open('$d/manifest.json'))['beats']))") <(python3 -c "import json;print(sorted(b['file'] for b in json.load(open('audio_cache/ep$EP/$p/manifest.json'))['beats']))") && continue
  ${PY:-python3} tools/audio_cache.py pack "$d" audio_cache/ep$EP/$p
  python3 - "$EP" "$p" <<'PY'
import json, sys
from pathlib import Path
d = Path(f"audio_cache/ep{sys.argv[1]}/{sys.argv[2]}"); keep = {Path(b["file"]).stem for b in json.loads((d / "manifest.json").read_text())["beats"]}
[f.unlink() for f in d.glob("*.flac") if f.stem not in keep]
PY
  echo "cached $p"
done
