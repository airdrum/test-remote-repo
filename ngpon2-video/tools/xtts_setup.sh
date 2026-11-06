#!/usr/bin/env bash
# One-time XTTS-v2 setup on the GPU machine (steps from the tested guide). Stops — never falls back to CPU — if there is no NVIDIA GPU.
# usage (from ngpon2-video/): bash tools/xtts_setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."
VENV=${XTTS_VENV:-.venv-xtts}
MODEL_DIR=${XTTS_MODEL_DIR:-$HOME/.cache/xtts_v2}

echo "== 1) GPU"
if ! command -v nvidia-smi >/dev/null || ! nvidia-smi; then
  echo "DUR: NVIDIA GPU / sürücü bulunamadı. XTTS CPU'ya düşürülmeyecek." >&2; exit 2
fi

echo "== 2) venv + coqui-tts"
if [ ! -x "$VENV/bin/python" ]; then
  if command -v uv >/dev/null; then uv venv "$VENV" --python 3.12; else python3.12 -m venv "$VENV"; fi
fi
PIP=(uv pip install --python "$VENV/bin/python"); command -v uv >/dev/null || PIP=("$VENV/bin/python" -m pip install)
"${PIP[@]}" "coqui-tts[cuda,codec]==0.28.0" six soundfile   # six is missing from coqui-tts 0.28.0's deps
if [ "$("$VENV/bin/python" -c 'import torch; print(torch.cuda.is_available())')" != "True" ]; then
  echo "torch CUDA görmüyor (PyPI torch'un CUDA sürümü sürücüden yeni olabilir) → cu128 index'inden yeniden kuruluyor"
  "${PIP[@]}" --reinstall torch torchaudio --index-url https://download.pytorch.org/whl/cu128
fi
"$VENV/bin/python" -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"
[ "$("$VENV/bin/python" -c 'import torch; print(torch.cuda.is_available())')" = "True" ] || { echo "DUR: torch.cuda.is_available() hâlâ False" >&2; exit 3; }

echo "== 3) model (~1.87 GB) → $MODEL_DIR"
mkdir -p "$MODEL_DIR"
for f in model.pth speakers_xtts.pth config.json vocab.json; do
  [ -s "$MODEL_DIR/$f" ] || curl -sSL --retry 4 -o "$MODEL_DIR/$f" "https://huggingface.co/coqui/XTTS-v2/resolve/main/$f"
done
check() { [ "$(sha256sum "$MODEL_DIR/$1" | cut -d' ' -f1)" = "$2" ] || { echo "DUR: $1 SHA256 uyuşmuyor" >&2; exit 4; }; echo "$1 SHA256 ok"; }
check model.pth c7ea20001c6a0a841c77e252d8409f6a74fb423e79b3206a0771ba5989776187
check speakers_xtts.pth f0f6137c19a4eab0cbbe4c99b5babacf68b1746e50da90807708c10e645b943b

echo "== 4) test (Damien Black, tr, CUDA zorunlu)"
mkdir -p build
XTTS_REQUIRE_GPU=1 XTTS_MODEL_DIR="$MODEL_DIR" "$VENV/bin/python" - <<'PY'
import sys, time; sys.path.insert(0, "tools")
import xtts_backend as x
from tr_text import normalize_tr
from lexicon import speak
t0 = time.time(); m = x.get_model(); load = time.time() - t0
text = normalize_tr(speak("NG-PON2'de her TWDM kanalı 10 Gbit/s taşır; 4 kanalla toplam kapasite 40 Gbit/s olur. "
                    "Alıcı hassasiyeti eksi 28 dBm civarındadır ve kanal aralığı 100 GHz'dir."))
t0 = time.time(); w = x.synthesize(text, "build/xtts_test.wav"); gen = time.time() - t0
dur = len(w) / x.SAMPLE_RATE
print(f"cihaz={next(m.parameters()).device}  yükleme={load:.1f}s  ses={dur:.1f}s  üretim={gen:.1f}s  RTF={gen/dur:.2f}  -> build/xtts_test.wav")
PY
