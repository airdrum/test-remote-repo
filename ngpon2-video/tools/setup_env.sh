#!/usr/bin/env bash
# Rebuild the render toolchain in a fresh container: Manim CE 0.22.1 (Cairo/Pango, no LaTeX), Inter font, ffmpeg (rubberband).
# srt's wheel build fails under build isolation, hence the separate install.
set -e
apt-get update -q
apt-get install -y -q libpango1.0-dev pkg-config ffmpeg fonts-inter
pip install --no-build-isolation srt
pip install manim==0.22.1
