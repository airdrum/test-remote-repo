#!/usr/bin/env bash
# usage: render_many.sh <l|h> file:Class [file:Class ...]   — runs up to 4 renders in parallel, isolated media dirs
q=$1; shift
cd "$(dirname "$0")/../scenes"
printf "%s\n" "$@" | xargs -P 4 -I{} bash -c '
  f=${1%%:*}; c=${1##*:}
  if [ "'$q'" = h ]; then a="-qh --resolution 1920,1080 --frame_rate 30"; else a="-ql"; fi
  manim $a --media_dir ../build/media_$c --disable_caching "$f" "$c" > ../build/render_$c.log 2>&1
  echo "$c exit=$?"' _ {}
