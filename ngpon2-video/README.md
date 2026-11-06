# NG-PON2 / ITU-T G.989.2 eğitim videoları — üretim hattı

Türkçe anlatımlı, animasyonlu teknik eğitim serisi (hedef: 4 × ~60 dk). Bu klasör şu an 1 dakikalık konsept örneğini içerir.

## Hat

| Adım | Araç | Komut |
|---|---|---|
| Senaryo (beat'lere bölünmüş) | `script/*.json` | elle / LLM taslak + insan doğrulama |
| Seslendirme | Gemini TTS (`gemini-2.5-pro-preview-tts`, ses `Charon`) | `python3 tools/tts.py script/sample_tr.json build/audio` |
| Ses QA | Gemini (`gemini-3.5-flash`) transkripsiyon, metinle karşılaştırma | `python3 tools/transcribe.py <wav> gemini-3.5-flash` |
| Ses işleme + senkron işaretleri | ffmpeg (kenar sessizlik kırpma, 1.08× tempo, 48 kHz), duraklama tabanlı öbek zamanları | `python3 tools/prep_audio.py build/audio/manifest.json build/audio_proc 1.08` |
| Animasyon | Manim CE 0.22 (Cairo), 1920×1080 @30 | `manim -qh --resolution 1920,1080 --frame_rate 30 --media_dir build/media --disable_caching scenes/sample.py Sample` |
| Görsel | Gemini `gemini-3-pro-image` (başlık arka planı, metinsiz) | `assets/title_bg.jpg` |
| Müzik | Gemini `lyria-3.5` (enstrümantal ambient yatak) | `python3 tools/music.py "<prompt>" assets/music_bed_v2.mp3` |
| Miks + altyazı | ffmpeg: sidechain ducking, loudnorm −16 LUFS, TR soft altyazı (mov_text) | `python3 tools/finalize.py <video> <müzik> build/timeline.json build/audio_proc/manifest.json <çıktı.mp4>` |

Senkron modeli: her beat ayrı bir TTS klibi; sahne kodu `beat(i)` ile klibi zaman çizelgesine koyar,
`at(t)` ile beat içindeki öbek zamanına (`cues`) kadar bekler, `end()` klip bitimine hizalar. Ses yeniden
üretilse bile animasyonlar kendini yeni sürelere göre ayarlar.

## Kurulum notları (bu konteyner)
- `apt-get install libpango1.0-dev pkg-config`, ardından `pip install manim`. `srt` paketi bu Python'da wheel
  derlemiyor; tek dosyalık modül elle site-packages'a kopyalandı.
- LaTeX yok → `MathTex` yerine `Text` (Inter font) kullanılıyor.
- Gemini API anahtarı ortam proxy'si tarafından enjekte ediliyor (`x-goog-api-key: dummy`).

## Bilinen kısıtlar
- `gemini-3.8-flash-tts` stil talimatını metinle birlikte sesli okuyor; talimatlı kullanım için 2.5-pro TTS seçildi.
- `www.itu.int` bu ortamdan erişilemiyor; G.989.2 PDF'i Drive veya repo üzerinden sağlanmalı.

## Seri: LAMBDA (10 × 40–45 dk)
Plan: `plan/sezon_plani.md`, bölüm planları `plan/B01_plan.md` …, bölüm meta verisi `plan/episodes.json`.
Ses: Gemini TTS, ses **Sadaltager**; intro müziği Lyria (`assets/intro_theme_a.mp3` içinden `tools/pick_window.py`
ile seçilen 10 sn, vuruş 5,88 sn → `assets/intro_theme_10s.wav`). Görsellerin tamamı Manim koduyla üretilir.

| Parça | Dosya | Komut |
|---|---|---|
| Ortak stil, senkron, cihaz kartları | `scenes/lib.py` | — |
| Seri intro'su (10 sn, müziğe kilitli) | `scenes/intro.py` | `cd scenes && EP=1 manim -qh --resolution 1920,1080 --frame_rate 30 --media_dir ../build/media --disable_caching intro.py Intro` |
| B01 açılış özeti | `scenes/ep01_open.py`, `script/ep01_open.json` | `python3 tools/tts.py script/ep01_open.json build/ep01_open/audio && python3 tools/prep_audio.py build/ep01_open/audio/manifest.json build/ep01_open/audio_proc 1.06` sonra manim |
| Birleştirme + altyazı | `tools/assemble.py` | `python3 tools/assemble.py <spec.json> <çıktı.mp4>` |
