"""Catch TTS acronym swaps (e.g. ONU spoken as OLT): ask an audio model which acronyms are spoken, in order, per beat.
usage: acro_check.py manifest.json [ACR1 ACR2 ...]   (default ONU OLT)  → prints MISMATCH lines"""
import base64, json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

def ask(path, script, acrs):
    q = (f"This Turkish narration may contain the acronyms {', '.join(acrs)} (spelled out letter by letter). Script: «{script}». "
         "List, in order, every occurrence of these acronyms as actually SPOKEN in the audio. "
         "Ignore any omitted or reworded non-acronym words. Final line must be exactly ACRONYMS_MATCH or ACRONYMS_MISMATCH.")
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(path, "rb").read()).decode()}}, {"text": q}]}]}
    for _ in range(4):
        try:
            req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
                                         data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
            r = json.load(urllib.request.urlopen(req, timeout=180))
            return "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"])
        except Exception:
            pass
    return "ERROR"

if __name__ == "__main__":
    man = json.load(open(sys.argv[1])); acrs = sys.argv[2:] or ["ONU", "OLT"]
    beats = [b for b in man["beats"] if any(a in b["text"] for a in acrs)]
    def job(b):
        a = ask(b["file"], b["text"], acrs)
        return b["id"], ("MISMATCH" if "ACRONYMS_MISMATCH" in a else "ok" if "ACRONYMS_MATCH" in a else "?"), a.replace("\n", " ")[-220:]
    with ThreadPoolExecutor(4) as ex:
        for bid, v, a in ex.map(job, beats):
            if v != "ok":
                print(v, bid, "|", a)
    print("checked", len(beats))
