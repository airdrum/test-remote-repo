"""Voice one script part with the first TTS model that still has daily quota.
The whole part is voiced by a single model (no mid-part voice change): if a model runs out of quota half-way,
the part is redone with the next model. Exit 3 = every model is out of quota.
usage: tts_part.py script.json out_dir model1 [model2 ...]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tts import DailyQuota
import tts_robust

def main(script, out, models):
    from tts import BACKEND
    if BACKEND == "xtts":
        models = ["xtts-v2"]
    s = json.loads(Path(script).read_text())
    for m in models:
        s["model"] = m
        tmp = Path(out).parent / f"_script_{Path(script).stem}_{m}.json"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(s, ensure_ascii=False, indent=1))
        try:
            tts_robust.run(str(tmp), out)
            print(f"MODEL_USED {m}")
            return 0
        except DailyQuota:
            print(f"QUOTA {m} → next model", flush=True)
        except RuntimeError as e:
            print(f"FAIL {m}: {e}", flush=True)
    return 3

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
