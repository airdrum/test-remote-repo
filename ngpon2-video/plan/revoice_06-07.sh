#!/usr/bin/env bash
# B6/B7: beats whose TEXT was corrected (no Annex D relaxation during tuning; G.989.2 §9.3.7).
# Removes their old clips in build/ and audio_cache/ so local_all re-voices them (instead of unpacking the old audio).
# Run on the GPU PC after `git pull`, then: bash tools/local_all.sh 06 07
cd "$(dirname "$0")/.."
PY=${PY:-python3}
$PY tools/revoice.py 06 end:h3
$PY tools/revoice.py 07 open:o3 recap:a1 p1:b3b p2:c3,c3a,c4,c5a,c6,c7 lab:g4 end:h1
echo "şimdi: bash tools/local_all.sh 06 07"
