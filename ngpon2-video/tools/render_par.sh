#!/usr/bin/env bash
# usage: render_par.sh <scene_file.py> <quality: l|h> <Class...>   (each class gets its own media dir → no text-cache races)
f=$1; q=$2; shift 2
cd "$(dirname "$0")/../scenes"
for c in "$@"; do
  ( if [ "$q" = h ]; then a="-qh --resolution 1920,1080 --frame_rate 30"; else a="-ql"; fi
    manim $a --media_dir ../build/media_$c --disable_caching "$f" "$c" > ../build/render_$c.log 2>&1
    echo "$c exit=$?" ) &
done
wait
