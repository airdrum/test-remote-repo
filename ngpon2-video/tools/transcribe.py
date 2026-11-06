import base64, json, sys, urllib.request
f = sys.argv[1]; model = sys.argv[2] if len(sys.argv) > 2 else "gemini-3.5-transcribe"
body = {"contents": [{"parts": [
  {"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(f, "rb").read()).decode()}},
  {"text": "Transcribe this Turkish audio verbatim."}]}]}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
  data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
try:
  r = json.load(urllib.request.urlopen(req, timeout=180))
  print(f, "->", "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"]).strip())
except urllib.error.HTTPError as e:
  print("HTTP", e.code, e.read()[:400].decode())
