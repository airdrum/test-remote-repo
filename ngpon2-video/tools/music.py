"""Lyria background bed."""
import base64, json, sys, urllib.request
prompt, out = sys.argv[1], sys.argv[2]
req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/lyria-3.5:generateContent",
    data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
r = json.load(urllib.request.urlopen(req, timeout=400))
for p in r["candidates"][0]["content"]["parts"]:
    if "inlineData" in p:
        open(out, "wb").write(base64.b64decode(p["inlineData"]["data"])); print("saved", out, p["inlineData"]["mimeType"])
