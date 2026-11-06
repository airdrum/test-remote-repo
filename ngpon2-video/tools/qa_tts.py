"""Transcribe each beat with Gemini and compare to the script (word-level similarity)."""
import base64, difflib, json, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

def transcribe(path, model="gemini-3.5-flash"):
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(path, "rb").read()).decode()}},
                                    {"text": "Transcribe this Turkish audio verbatim. Write numbers as words."}]}]}
    for i in range(6):
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
            r = json.load(urllib.request.urlopen(req, timeout=180))
            return "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"]).strip()
        except Exception as e:
            time.sleep(5 * (i + 1))
    return ""

norm = lambda s: re.sub(r"[^\wçğıöşü ]", " ", s.lower().replace("'", "")).split()

def run(manifest):
    m = json.load(open(manifest))
    def job(b):
        tx = transcribe(b["file"])
        r = difflib.SequenceMatcher(None, norm(b["text"]), norm(tx)).ratio()
        return b["id"], r, tx
    with ThreadPoolExecutor(2) as ex:
        for bid, r, tx in ex.map(job, m["beats"]):
            flag = "OK " if r >= 0.85 else "CHK"
            print(f"{flag} {bid:5s} {r:.2f}" + ("" if r >= 0.85 else f"  -> {tx}"))

if __name__ == "__main__":
    run(sys.argv[1])
