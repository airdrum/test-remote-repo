#!/usr/bin/env bash
# Episode 14 beats voiced before the splitter fix with likely stray XTTS syllables (cloud QA).
# Run on the GPU PC after `git pull`, then: bash tools/local_all.sh 14
cd "$(dirname "$0")/.."
PY=${PY:-python3}
$PY tools/revoice.py 14 p1:b6,b7,b13 p3:d14 p4:e11
echo "şimdi: bash tools/local_all.sh 14"
