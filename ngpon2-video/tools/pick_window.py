"""Find the best 10 s intro window in a music file: quiet-ish start, rising energy, strong onset ~6 s, sustained after."""
import subprocess, sys, numpy as np
f, L, hit = sys.argv[1], 10.0, 6.0
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                                   capture_output=True).stdout, np.int16).astype(np.float32) / 32768
hop = 400  # 50 ms
env = np.sqrt(np.convolve(pcm ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
db = 20 * np.log10(env)
onset = np.maximum(np.diff(db, prepend=db[0]), 0)  # positive energy jumps
fps = 8000 / hop; best = []
for s in np.arange(0, len(db) / fps - L, 0.25):
    i0, ih, i1 = int(s * fps), int((s + hit) * fps), int((s + L) * fps)
    pre, post = db[i0:ih - 4].mean(), db[ih:ih + int(2 * fps)].mean()
    jump = onset[ih - 3:ih + 4].max()
    score = jump + 0.6 * (post - pre) - 0.3 * abs(db[i0:i0 + 10].mean() - pre)
    best.append((score, s, jump, post - pre))
best.sort(reverse=True)
print(f"{f}: dur {len(db)/fps:.1f}s, overall {db.mean():.1f} dBFS")
for sc, s, j, r in best[:4]: print(f"  start {s:6.2f}s  score {sc:5.1f}  onset {j:4.1f} dB  rise {r:4.1f} dB")
