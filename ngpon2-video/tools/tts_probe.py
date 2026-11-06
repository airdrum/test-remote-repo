import base64, json, sys, time, urllib.request, wave
model, voice, text, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
body = {
  "contents": [{"parts": [{"text": text}]}],
  "generationConfig": {"responseModalities": ["AUDIO"],
    "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
}
req = urllib.request.Request(
  f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
  data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
t=time.time()
try:
  r = json.load(urllib.request.urlopen(req, timeout=180))
except urllib.error.HTTPError as e:
  print("HTTP", e.code, e.read()[:500].decode()); sys.exit(1)
part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
pcm = base64.b64decode(part["data"])
with wave.open(out, "wb") as w:
  w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
print(model, voice, part["mimeType"], f"{len(pcm)/48000:.2f}s audio", f"{time.time()-t:.1f}s latency")
