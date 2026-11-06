# Proje notları

Ana proje: `ngpon2-video/` — "LAMBDA — NG-PON2'nin Fizik Katmanı" Türkçe ders videoları (Manim + TTS anlatım).

## Ses üretimi — VARSAYILAN: yerel XTTS-v2 (kullanıcı aksini söyleyene kadar)

Kullanıcı "ses üretelim" dediğinde **her zaman** yerel XTTS-v2 kullanılır; Gemini TTS **yalnızca kullanıcı açıkça isterse**.

- Model: Coqui XTTS-v2, hazır konuşmacı **"Damien Black"**, `language="tr"`, **GPU (CUDA)**.
- Kod yolu: `TTS_BACKEND=xtts` (varsayılan, `tools/tts.py`) → `tools/xtts_backend.py` (model süreç başına bir kez yüklenir).
  Gemini kodu silinmedi; yalnızca `TTS_BACKEND=gemini` ile çalışır.
- GPU yoksa **DUR ve kullanıcıya söyle**; CPU'ya sessizce düşme (`XTTS_REQUIRE_GPU=1`).
  Bulut konteynerinde GPU yok: XTTS, kullanıcının Remote Control ile paylaştığı NVIDIA GPU'lu bilgisayarında çalışır.
- Kurulum (GPU makinesinde, bir kez): `cd ngpon2-video && bash tools/xtts_setup.sh`
  — nvidia-smi kontrolü, `.venv-xtts` (Python 3.12, `coqui-tts[cuda,codec]==0.28.0 six soundfile`), CUDA doğrulama
  (gerekirse torch'u cu128 index'inden yeniden kurar), modeli `~/.cache/xtts_v2`'ye curl ile indirir, SHA256 kontrolü, test + RTF.
- Bölüm seslendirme: `bash tools/tts_episode.sh 05 "p4 lab end"` → `build/epNN/<part>/audio/manifest.json`
  (24 kHz mono 16-bit WAV, Gemini çıktısıyla aynı format; `prep_audio.py` / `assemble.py` değişmeden çalışır).
  Sonra `PY=.venv-xtts/bin/python bash tools/cache_ep.sh 05` ile `audio_cache/` (FLAC) altına alıp commit/push et.
- XTTS'e **stil talimatı gönderilmez** (prompt anlamaz, sesli okur); yalnızca okunacak düz metin.
- Metin hazırlama: `lexicon.speak()` (kısaltmalar) → `tr_text.normalize_tr()` (sayı/birim/yüzde → Türkçe yazı)
  → `split_tr()` (~200 karakter altı parçalar).
- Kalite: `temperature=0.65`, sabit seed (1234; QA tekrarlarında seed değişir). QA: Gemini (gemini-3.5-flash) transkripsiyonu
  `GEMINI_API_KEY` ile; anahtar yoksa `TTS_QA=0` (QA kapalı) — o durumda sesleri bulutta `tools/qa_tts.py` ile kontrol et.
  Kısaltma takası riski için `tools/acro_check.py`.
- Lisans: Coqui Public Model License — **ticari kullanım yok**. Jeneriklerde seslendirme "XTTS-v2 · Damien Black" olarak yazılır.

## Diğer kurallar

- Commit'lerde model adı yazma. 100 MB üstü MP4'ler git'e girmez (kullanıcıya dosya olarak gönderilir).
- `build/` git dışında; konteyner yeniden başlarsa sesler `audio_cache/` → `tools/audio_cache.py unpack` ile geri gelir.
