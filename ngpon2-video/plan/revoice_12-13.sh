#!/usr/bin/env bash
# Beats from episodes 12–13 voiced before the splitter fix: short sentences where XTTS likely added a stray syllable (cloud QA).
# Run on the GPU PC after `git pull`, then: bash tools/local_all.sh 12 13  (only the affected parts are redone).
cd "$(dirname "$0")/.."
PY=${PY:-python3}
$PY tools/revoice.py 12 p1:b1a p2:c7,c10,c11 p3:d11 p4:e12,e13 lab:g11
$PY tools/revoice.py 13 p4:e6,e15 lab:g2
echo "şimdi: bash tools/local_all.sh 12 13"
