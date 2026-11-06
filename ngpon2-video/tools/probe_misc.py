import base64, json, sys, urllib.request
def call(model, body, timeout=300):
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
    try: return json.load(urllib.request.urlopen(req, timeout=timeout))
    except urllib.error.HTTPError as e: print(model, "HTTP", e.code, e.read()[:600].decode()); return None
what = sys.argv[1]
if what == "music":
    for model in ["lyria-3.5", "lyria-3-clip-preview"]:
        r = call(model, {"contents": [{"parts": [{"text": "Calm, minimal ambient electronic background music for a technical engineering tutorial video. Soft synth pads, slow pulsing arpeggio, no drums, no vocals, unobtrusive, steady, 70 seconds."}]}]})
        if not r: continue
        for i, p in enumerate(r["candidates"][0]["content"]["parts"]):
            if "inlineData" in p:
                ext = p["inlineData"]["mimeType"].split("/")[-1].split(";")[0]
                fn = f"build/music_probe_{model}.{ext}"; open(fn, "wb").write(base64.b64decode(p["inlineData"]["data"]))
                print(model, p["inlineData"]["mimeType"], fn)
            else: print(model, "text:", p.get("text", "")[:200])
        break
else:
    r = call("gemini-3-pro-image", {"contents": [{"parts": [{"text": "Cinematic wide 16:9 dark navy background image: bundles of single-mode optical fibers glowing with several distinct laser wavelengths (violet, cyan, green, amber, red) converging into one fiber, subtle bokeh, high-tech optical lab atmosphere, lots of empty dark negative space on the left third for title text. Absolutely no text, no letters, no logos."}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"}}})
    if r:
        for p in r["candidates"][0]["content"]["parts"]:
            if "inlineData" in p:
                open("build/title_bg.png", "wb").write(base64.b64decode(p["inlineData"]["data"])); print("image", p["inlineData"]["mimeType"])
            else: print("text:", p.get("text", "")[:200])
