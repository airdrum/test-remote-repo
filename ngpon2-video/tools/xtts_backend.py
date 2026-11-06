"""XTTS-v2 Türkçe TTS backend (Damien Black). GPU varsa CUDA, yoksa CPU."""
import os
import threading

os.environ.setdefault("COQUI_TOS_AGREED", "1")  # CPML: ticari olmayan kullanım

import numpy as np
import soundfile as sf
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

MODEL_DIR = os.environ.get("XTTS_MODEL_DIR", os.path.expanduser("~/.cache/xtts_v2"))
SPEAKER = os.environ.get("XTTS_SPEAKER", "Damien Black")
LANGUAGE = "tr"
SAMPLE_RATE = 24000

_model = None
_lock = threading.Lock()


def _device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if os.environ.get("XTTS_REQUIRE_GPU") == "1":
        raise RuntimeError("XTTS_REQUIRE_GPU=1 ama CUDA bulunamadı")
    print("[xtts] UYARI: CUDA yok, CPU kullanılıyor (yaklaşık 1.4x gerçek zaman)")
    return "cpu"


def get_model() -> Xtts:
    global _model
    with _lock:
        if _model is None:
            cfg = XttsConfig()
            cfg.load_json(os.path.join(MODEL_DIR, "config.json"))
            m = Xtts.init_from_config(cfg)
            m.load_checkpoint(cfg, checkpoint_dir=MODEL_DIR, use_deepspeed=False)
            m.to(_device())
            m.eval()
            _model = m
            print(f"[xtts] model yüklendi, cihaz: {next(_model.parameters()).device}")
        return _model


def synthesize(text: str, out_path: str | None = None, temperature: float = 0.65,
               seed: int | None = 1234) -> np.ndarray:
    """Türkçe metni Damien Black sesiyle okur. 24 kHz mono float32 döner; out_path verilirse WAV yazar."""
    m = get_model()
    spk = m.speaker_manager.speakers[SPEAKER]
    if seed is not None:
        torch.manual_seed(seed)
    with torch.inference_mode():
        out = m.inference(
            text, LANGUAGE, spk["gpt_cond_latent"], spk["speaker_embedding"],
            temperature=temperature, repetition_penalty=10.0, top_k=50, top_p=0.85,
            enable_text_splitting=True,
        )
    wav = np.asarray(out["wav"], dtype=np.float32)
    if out_path:
        sf.write(out_path, wav, SAMPLE_RATE, subtype="PCM_16")
    return wav


def synthesize_pcm16(text: str, seed: int | None = 1234, gap_s: float = 0.22) -> bytes:
    """Project adapter: normalise, split into ≤200-char chunks, synthesise each, join with short pauses.
    Returns 24 kHz mono 16-bit PCM bytes — the same format the Gemini path returns."""
    from tr_text import normalize_tr, split_tr
    parts, gap = [], np.zeros(int(gap_s * SAMPLE_RATE), dtype=np.float32)
    for i, chunk in enumerate(split_tr(normalize_tr(text))):
        with _infer_lock:
            parts += [synthesize(chunk, seed=None if seed is None else seed + i), gap]
    wav = np.concatenate(parts[:-1]) if parts else np.zeros(1, dtype=np.float32)
    return (np.clip(wav, -1, 1) * 32767).astype("<i2").tobytes()


_infer_lock = threading.Lock()


if __name__ == "__main__":
    import sys
    import time
    text = sys.argv[1] if len(sys.argv) > 1 else "Merhaba, bu kayıt Damien Black sesiyle üretildi."
    out = sys.argv[2] if len(sys.argv) > 2 else "test_damien.wav"
    t0 = time.time()
    w = synthesize(text, out)
    print(f"{len(w) / SAMPLE_RATE:.1f} s ses, {time.time() - t0:.1f} s (model yükleme dahil) -> {out}")
