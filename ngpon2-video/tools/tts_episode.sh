#!/usr/bin/env bash
# Voice all parts of an episode. usage: tts_episode.sh 05 "p4 lab end"
# Default backend = local XTTS-v2 (Damien Black, tr, CUDA) — see ../CLAUDE.md. Gemini only with TTS_BACKEND=gemini:
# then each part falls back across TTS models and waits for the daily reset if all are spent.
cd "$(dirname "$0")/.."
export PYTHONUTF8=1   # Windows (Git Bash): Turkish text/JSON as UTF-8
EP=$1; PARTS=$2
export TTS_BACKEND=${TTS_BACKEND:-xtts}
if [ "$TTS_BACKEND" = xtts ]; then
  export XTTS_REQUIRE_GPU=${XTTS_REQUIRE_GPU:-1} XTTS_SPEAKER=${XTTS_SPEAKER:-Damien Black} XTTS_MODEL_DIR=${XTTS_MODEL_DIR:-$(command -v cygpath >/dev/null && cygpath -w "$HOME/.cache/xtts_v2" || echo "$HOME/.cache/xtts_v2")}
  [ -x .venv-xtts/Scripts/python.exe ] && DEF=.venv-xtts/Scripts/python.exe || DEF=.venv-xtts/bin/python
  PY=${PY:-$DEF}; [ -x "$PY" ] || { echo "XTTS venv yok: önce bash tools/xtts_setup.sh" >&2; exit 2; }
  [ -n "${GEMINI_API_KEY:-}" ] || [ -n "${HTTPS_PROXY:-}" ] || { export TTS_QA=${TTS_QA:-0}; echo "GEMINI_API_KEY yok → transkripsiyon QA kapalı (TTS_QA=0)"; }
else
  PY=${PY:-python3}
fi
export PY
MODELS=${TTS_MODELS:-"gemini-2.5-flash-preview-tts gemini-3.1-flash-tts-preview gemini-3.8-flash-lite-tts gemini-3.8-flash-tts gemini-2.5-pro-preview-tts"}
mkdir -p build; ST=build/ep${EP}_tts.status; : > $ST
for p in $PARTS; do
  until [ -f build/ep$EP/$p/audio/manifest.json ]; do
    "$PY" -u tools/tts_part.py script/ep${EP}_$p.json build/ep$EP/$p/audio $MODELS 2>&1 | tee -a build/ep${EP}_tts_$p.log
    rc=${PIPESTATUS[0]}
    if [ "$TTS_BACKEND" = xtts ] && [ $rc -ne 0 ]; then echo "$p ERROR rc=$rc (xtts)" >> $ST; exit $rc; fi
    if [ $rc -eq 3 ]; then echo "$p WAITING_FOR_QUOTA $(date -u +%H:%M)" >> $ST; sleep 1800; elif [ $rc -ne 0 ]; then echo "$p ERROR rc=$rc" >> $ST; sleep 120; fi
  done
  echo "$p exit=0 $(grep -h MODEL_USED build/ep${EP}_tts_$p.log | tail -1)" >> $ST
done
echo ALL_DONE >> $ST
