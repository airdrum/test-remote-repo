"""Boundary QA for split beats: transcribe each beat and check that its first/last words match the script."""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "tools")
from qa_tts import transcribe

def words(s):
    s = s.lower().replace("'", " ").replace("’", " ")
    return [w for w in re.findall(r"[a-zçğıöşüâî]+", s) if len(w) >= 3]

def check(b):
    tx = transcribe(b["file"])
    ew, tw = words(b["text"]), words(tx)
    head = sum(w in tw[:8] for w in ew[:3]) >= 2
    tail = sum(w in tw[-8:] for w in ew[-3:]) >= 2
    return b["id"], head, tail, tx

def run(manifest):
    m = json.load(open(manifest))
    bad = []
    with ThreadPoolExecutor(3) as ex:
        for bid, h, t, tx in ex.map(check, m["beats"]):
            ok = h and t
            print(f"{'OK ' if ok else 'BAD'} {bid:5s} head={int(h)} tail={int(t)}" + ("" if ok else f"  -> {tx[:160]}"), flush=True)
            if not ok: bad.append(bid)
    return bad

if __name__ == "__main__":
    for f in sys.argv[1:]:
        print("==", f); run(f)
