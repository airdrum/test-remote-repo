"""Ask Gemini (audio understanding) for paragraph start times in a grouped TTS clip."""
import base64, json, os, re, sys, time, urllib.request

def para_starts(wav_path, paragraphs, model="gemini-3.5-flash"):
    listing = "\n".join(f"{i + 1}. {p}" for i, p in enumerate(paragraphs))
    prompt = ("The audio is a Turkish narration of the following paragraphs, read in order:\n" + listing +
              "\n\nFor each paragraph, give the time in seconds (two decimals) at which its FIRST word starts in the audio. "
              "Answer only with a JSON array of numbers, one per paragraph.")
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(wav_path, "rb").read()).decode()}},
                                    {"text": prompt}]}], "generationConfig": {"temperature": 0}}
    for i in range(5):
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "dummy")})
            r = json.load(urllib.request.urlopen(req, timeout=300))
            txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"])
            arr = json.loads(re.search(r"\[[^\]]*\]", txt).group(0))
            if len(arr) == len(paragraphs):
                return [float(x) for x in arr]
        except Exception as e:
            time.sleep(4 * (i + 1))
    return None

if __name__ == "__main__":
    import glob
    sys.path.insert(0, "tools")
    from lexicon import speak
    s = json.load(open(sys.argv[1])); ids = sys.argv[3].split(",")
    bm = {b["id"]: b for b in s["beats"]}
    print(para_starts(sys.argv[2], [speak(bm[i]["text"]) for i in ids]))
