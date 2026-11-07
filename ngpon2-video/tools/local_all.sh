#!/usr/bin/env bash
# Everything after the scene code, on the GPU PC (Git Bash on Windows works):
#   XTTS voice → audio_cache (+ git push) → audio prep → 1080p30 render → assembled MP4 in deliverables/
# usage: bash tools/local_all.sh 09 10 11 12 13 14 15 16 17 18 19 20
#   Episodes run in the given order; each one is finished before the next starts.
# env: PY   = python that has manim (default python3; on Windows e.g. PY=/c/Python310/python.exe)
#      VPY  = XTTS venv python (auto: .venv-xtts/Scripts/python.exe or .venv-xtts/bin/python)
#      PUSH = 0 to skip committing/pushing audio_cache
#      GEMINI_API_KEY set → transcription QA runs during voicing; unset → QA is skipped (TTS_QA=0)
set -u
cd "$(dirname "$0")/.."
export PYTHONUTF8=1
PY=${PY:-python3}
if [ -z "${VPY:-}" ]; then
  [ -x .venv-xtts/Scripts/python.exe ] && VPY=.venv-xtts/Scripts/python.exe || VPY=.venv-xtts/bin/python
fi
PARTS="open recap p1 p2 p3 p4 lab end"
mkdir -p build
for EP in "$@"; do
  echo "=== ep$EP · 1/5 ses (XTTS)"
  for p in $PARTS; do   # audio already in git but not in build/ → unpack instead of re-voicing
    [ -f build/ep$EP/$p/audio/manifest.json ] || [ ! -f audio_cache/ep$EP/$p/manifest.json ] || $PY tools/audio_cache.py unpack audio_cache/ep$EP/$p build/ep$EP/$p/audio
  done
  bash tools/tts_episode.sh $EP "$PARTS" || { echo "ep$EP: seslendirme hatası — dur"; exit 1; }
  PY=$VPY bash tools/cache_ep.sh $EP
  if [ "${PUSH:-1}" = 1 ] && [ -n "$(git status --porcelain audio_cache/ep$EP)" ]; then
    git add audio_cache/ep$EP && git commit -q -m "ep$EP: XTTS seslendirme (audio_cache)" && git pull -q --rebase && git push -q \
      || echo "ep$EP: push başarısız (devam ediliyor)"
  fi
  echo "=== ep$EP · 2/5 ses hazırlama (tempo 0.93)"
  PY=$PY bash tools/ep_finish.sh $EP prep 0.93
  echo "=== ep$EP · 3/5 render (1080p30, birkaç saat sürebilir)"
  EXTRA_PAD=0.85 PY=$PY bash tools/ep_finish.sh $EP render | tee build/ep${EP}_render_all.log
  if grep -q "exit=[1-9]" build/ep${EP}_render_all.log; then
    echo "ep$EP: render hatası — build/render_<Sahne>.log dosyalarına bak"; exit 1
  fi
  echo "=== ep$EP · 4/5 birleştirme"
  PY=$PY bash tools/ep_finish.sh $EP assemble || { echo "ep$EP: birleştirme hatası — dur"; exit 1; }
  echo "=== ep$EP · 5/5 hazır: $(ls deliverables/B$EP/*.mp4 2>/dev/null | tail -1)"
done
