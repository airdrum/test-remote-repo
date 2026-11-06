"""Move the boundary between two consecutive beats (same group) to an earlier pause until the second beat's head matches."""
import json, sys, wave, re, subprocess
sys.path.insert(0, "tools")
from tts_robust import words, silences, read_wav, write_wav, SR
from qa_tts import transcribe

def fix(manifest, prev_id, cur_id, direction="earlier"):
    m = json.load(open(manifest)); bm = {b["id"]: b for b in m["beats"]}
    P, C = bm[prev_id], bm[cur_id]
    pp, cp = read_wav(P["file"]), read_wav(C["file"])
    joint = pp + cp; cut0 = len(pp) / 2 / SR
    tmp = "/tmp/claude_joint.wav"; write_wav(tmp, joint)
    sil = sorted(((a + e) / 2 for a, e in silences(tmp) if e - a >= 0.2), key=lambda m_: abs(m_ - cut0))
    cands = [s for s in sil if (s < cut0 - 0.3 if direction == "earlier" else s > cut0 + 0.3) and abs(s - cut0) < 6]
    ew = words(C["text"])
    for c in cands:
        seg = joint[int(c * SR) * 2:]
        write_wav(C["file"], seg)
        tx = transcribe(C["file"]); tw = words(tx)
        if sum(w in tw[:12] for w in ew[:3]) >= 2:
            write_wav(P["file"], joint[:int(c * SR) * 2])
            P["duration"] = round(c, 3); C["duration"] = round(len(seg) / 2 / SR, 3); C["qa"] = "ok(fixed)"
            json.dump(m, open(manifest, "w"), ensure_ascii=False, indent=1)
            print(f"{cur_id}: cut moved {cut0:.2f} → {c:.2f}  | {tx[:90]}")
            return True
    write_wav(C["file"], cp); print(f"{cur_id}: no better cut found"); return False

if __name__ == "__main__":
    fix(sys.argv[1], sys.argv[2], sys.argv[3], *(sys.argv[4:5]))
