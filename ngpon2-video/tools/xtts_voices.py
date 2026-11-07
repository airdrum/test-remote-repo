"""Render the same Turkish technical paragraph with several XTTS-v2 built-in speakers so a voice can be chosen by ear.
usage (GPU machine, from ngpon2-video/):  .venv-xtts/Scripts/python.exe tools/xtts_voices.py ["Name 1" "Name 2" ...]
Without arguments it renders the female candidates below that exist in speakers_xtts.pth → build/voices/<name>.wav,
and prints every speaker name the model contains."""
import os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("XTTS_REQUIRE_GPU", "1")
import numpy as np, soundfile as sf
import xtts_backend as x
from lexicon import speak

FEMALE = ["Ana Florence", "Claribel Dervla", "Daisy Studious", "Gracie Wise", "Tammie Ema", "Alison Dietlinde",
          "Annmarie Nele", "Asya Anara", "Sofia Hellen", "Gitta Nikolina", "Henriette Usha", "Tanja Adelina",
          "Brenda Stern", "Tammy Grit", "Nova Hogarth"]
TEXT = ("Bölüm bir: Çerçevenin içinde. Aşağı yönde her yüz yirmi beş mikrosaniyede bir çerçeve gelir; "
        "ONU önce senkron desenini bulur, sonra PLOAM mesajlarını ve XGEM çerçevelerini çözer. "
        "OLT, yukarı yön için her ONU'ya bir zaman dilimi ayırır; on gigabitte ek yük iki bin kırk sekiz bittir, "
        "ve alıcı hassasiyeti eksi yirmi sekiz dBm'dir.")

if __name__ == "__main__":
    m = x.get_model()
    names = sorted(m.speaker_manager.speakers)
    print(f"{len(names)} speakers in the model:\n  " + "\n  ".join(names))
    want = [n for n in (sys.argv[1:] or FEMALE) if n in m.speaker_manager.speakers]
    out = Path("build/voices"); out.mkdir(parents=True, exist_ok=True)
    for n in want:
        t0 = time.time()
        pcm = x.synthesize_pcm16(speak(TEXT), seed=1234, speaker=n)
        wav = np.frombuffer(pcm, dtype="<i2")
        fn = out / (n.replace(" ", "_") + ".wav")
        sf.write(fn, wav, x.SAMPLE_RATE, subtype="PCM_16")
        print(f"{n:20s} {len(wav) / x.SAMPLE_RATE:5.1f} s  ({time.time() - t0:.1f} s)  -> {fn}")
