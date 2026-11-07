#!/usr/bin/env bash
# Generic episode pipeline after scripts + scenes exist. Order/spec comes from plan/epNN_order.json:
#   [["SceneClass", "scene_file_stem", "timeline_name", "part"], ..., ["Intro", null, null, null], ...]
# usage: ep_finish.sh NN prep|render|assemble [tempo]
cd "$(dirname "$0")/.."
EP=$1; STAGE=$2; TEMPO=${3:-0.87}
PY=${PY:-python3}   # Windows: $PY may be a broken stub; pass PY=/c/Python310/python.exe (has manim+stdlib)
ORDER=plan/ep${EP}_order.json
PARTS=$($PY -c "import json;print(' '.join(dict.fromkeys(p for c,f,t,p in json.load(open('$ORDER')) if p)))")
case "$STAGE" in
prep)
  for p in $PARTS; do $PY tools/prep_audio.py build/ep$EP/$p/audio/manifest.json build/ep$EP/$p/audio_proc $TEMPO > build/ep${EP}_prep_$p.log 2>&1 & done; wait
  $PY -c "import json;print('speech min',round(sum(json.load(open(f'build/ep$EP/{p}/audio_proc/manifest.json'))['total'] for p in '$PARTS'.split())/60,2))" ;;
render)
  N=$((10#$EP))
  [ -f build/media_Intro$N/videos/intro/1080p30/Intro.mp4 ] || (cd scenes && EP=$N manim -qh --resolution 1920,1080 --frame_rate 30 --media_dir ../build/media_Intro$N --disable_caching intro.py Intro > ../build/render_Intro$N.log 2>&1)
  S=$($PY -c "import json;print(' '.join(f'{f}.py:{c}' for c,f,t,p in json.load(open('$ORDER')) if f))")
  EXTRA_PAD=${EXTRA_PAD:-0.85} tools/render_many.sh h $S ;;
assemble)
  $PY - "$EP" <<'PY'
import json, sys
ep = sys.argv[1]; n = int(ep)
spec = []
for c, f, t, p in json.load(open(f"plan/ep{ep}_order.json")):
    if not f:
        spec.append({"video": f"build/media_Intro{n}/videos/intro/1080p30/Intro.mp4", "norm": False})
    else:
        spec.append({"video": f"build/media_{c}/videos/{f}/1080p30/{c}.mp4", "norm": True, "timeline": f"build/{t}_timeline.json", "manifest": f"build/ep{ep}/{p}/audio_proc/manifest.json"})
json.dump(spec, open(f"build/ep{ep}_full_spec.json", "w"), indent=1)
PY
  NAME=$($PY -c "import json,unicodedata;e=json.load(open('plan/episodes.json'))['episodes'][$((10#$EP))-1];t=unicodedata.normalize('NFKD',e['title'].replace('ı','i')).encode('ascii','ignore').decode().replace(' ','_');print(f'LAMBDA_B$EP'+'_'+t)")
  mkdir -p deliverables/B$EP
  NO_SUBS=1 CRF=20 $PY tools/assemble.py build/ep${EP}_full_spec.json deliverables/B$EP/$NAME.mp4 ;;
esac
