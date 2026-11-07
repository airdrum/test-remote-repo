#!/usr/bin/env bash
# Beats from episodes 09–11 where XTTS added a stray syllable after a very short sentence (cloud QA, blind transcription).
# Run on the GPU PC after `git pull`, then re-run local_all for these episodes: only the affected parts are re-voiced,
# re-prepped and re-rendered (new seed, and the splitter now packs short sentences together).
cd "$(dirname "$0")/.."
PY=${PY:-python3}
$PY tools/revoice.py 09 p3:d9,d10 p4:e3,e5,e15 end:h1,h4
$PY tools/revoice.py 10 p2:c1 p4:e18 lab:g4
$PY tools/revoice.py 11 p1:b4 p2:c5
echo "şimdi: bash tools/local_all.sh 09 10 11"
