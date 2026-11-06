#!/usr/bin/env bash
# Voice all parts of an episode, falling back across TTS models per part; waits for the daily reset if all are spent.
# usage: tts_episode.sh 04 "open recap p1 p2 p3 p4 p5 lab end"
cd "$(dirname "$0")/.."
EP=$1; PARTS=$2
MODELS=${TTS_MODELS:-"gemini-2.5-flash-preview-tts gemini-3.1-flash-tts-preview gemini-3.8-flash-lite-tts gemini-3.8-flash-tts gemini-2.5-pro-preview-tts"}
ST=build/ep${EP}_tts.status; : > $ST
for p in $PARTS; do
  until [ -f build/ep$EP/$p/audio/manifest.json ]; do
    python3 -u tools/tts_part.py script/ep${EP}_$p.json build/ep$EP/$p/audio $MODELS >> build/ep${EP}_tts_$p.log 2>&1
    rc=$?
    if [ $rc -eq 3 ]; then echo "$p WAITING_FOR_QUOTA $(date -u +%H:%M)" >> $ST; sleep 1800; elif [ $rc -ne 0 ]; then echo "$p ERROR rc=$rc" >> $ST; sleep 120; fi
  done
  echo "$p exit=0 $(grep -h MODEL_USED build/ep${EP}_tts_$p.log | tail -1)" >> $ST
done
echo ALL_DONE >> $ST
