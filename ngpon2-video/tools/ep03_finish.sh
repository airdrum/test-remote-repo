#!/usr/bin/env bash
# Finish B03 after the TTS quota resets. Stages: restore | tts | prep | render | assemble
cd "$(dirname "$0")/.."
P="open recap p1 p2 p3 p4 p5 lab end"
case "$1" in
restore)  # build/ is not in git: bring the cached FLAC clips back
  for p in $P; do [ -d audio_cache/ep03/$p ] && [ ! -f build/ep03/$p/audio/manifest.json -o "$p" = p5 ] && python3 tools/audio_cache.py unpack audio_cache/ep03/$p build/ep03/$p/audio; done ;;
tts)      # p1 only re-synthesises the edited b2b group; finished groups are cached as g*.wav
  for p in p1 p5 lab end; do python3 -u tools/tts_robust.py script/ep03_$p.json build/ep03/$p/audio > build/ep03_tts_$p.log 2>&1; echo "$p exit=$?"; done ;;
prep)
  for p in $P; do python3 tools/prep_audio.py build/ep03/$p/audio/manifest.json build/ep03/$p/audio_proc 0.87 > build/ep03_prep_$p.log 2>&1 & done; wait
  python3 -c "import json;print('speech min',sum(json.load(open(f'build/ep03/{p}/audio_proc/manifest.json'))['total'] for p in '$P'.split())/60)" ;;
render)
  (cd scenes && EP=3 manim -qh --resolution 1920,1080 --frame_rate 30 --media_dir ../build/media_Intro3 --disable_caching intro.py Intro > ../build/render_Intro3.log 2>&1)
  EXTRA_PAD=0.85 tools/render_many.sh h $(cat build/ep03_scenes.txt 2>/dev/null || echo "ep03_open.py:Ep03Open ep03_open.py:Ep03Recap ep03_p12.py:E3P1A ep03_p12.py:E3P1B ep03_p12.py:E3P1C ep03_p12.py:E3P2A ep03_p12.py:E3P2B ep03_p34.py:E3P3A ep03_p34.py:E3P3B ep03_p34.py:E3P3C ep03_p34.py:E3P4A ep03_p34.py:E3P4B ep03_p34.py:E3P4C ep03_p5le.py:E3P5A ep03_p5le.py:E3P5B ep03_p5le.py:E3LabA ep03_p5le.py:E3LabB ep03_p5le.py:E3End") ;;
assemble)
  python3 - <<'PY'
import json
order=[("Ep03Open","ep03_open","ep03_open","open"),("Intro3",None,None,None),("Ep03Recap","ep03_open","ep03_recap","recap"),
("E3P1A","ep03_p12","ep03_p1A","p1"),("E3P1B","ep03_p12","ep03_p1B","p1"),("E3P1C","ep03_p12","ep03_p1C","p1"),("E3P2A","ep03_p12","ep03_p2A","p2"),("E3P2B","ep03_p12","ep03_p2B","p2"),
("E3P3A","ep03_p34","ep03_p3A","p3"),("E3P3B","ep03_p34","ep03_p3B","p3"),("E3P3C","ep03_p34","ep03_p3C","p3"),("E3P4A","ep03_p34","ep03_p4A","p4"),("E3P4B","ep03_p34","ep03_p4B","p4"),("E3P4C","ep03_p34","ep03_p4C","p4"),
("E3P5A","ep03_p5le","ep03_p5A","p5"),("E3P5B","ep03_p5le","ep03_p5B","p5"),("E3LabA","ep03_p5le","ep03_labA","lab"),("E3LabB","ep03_p5le","ep03_labB","lab"),("E3End","ep03_p5le","ep03_end","end")]
spec=[{"video":"build/media_Intro3/videos/intro/1080p30/Intro.mp4","norm":False} if c=="Intro3" else
      {"video":f"build/media_{c}/videos/{f}/1080p30/{c}.mp4","norm":True,"timeline":f"build/{tl}_timeline.json","manifest":f"build/ep03/{p}/audio_proc/manifest.json"} for c,f,tl,p in order]
json.dump(spec,open("build/ep03_full_spec.json","w"),indent=1)
PY
  mkdir -p deliverables/B03
  NO_SUBS=1 CRF=20 python3 tools/assemble.py build/ep03_full_spec.json deliverables/B03/LAMBDA_B03_Renk_Haritasi.mp4 ;;
esac
