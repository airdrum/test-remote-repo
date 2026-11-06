# LAMBDA — NG-PON2'nin Fizik Katmanı
### Sezon 1 · ITU-T G.989.2 (+ G.989.3 köprüleri) · 10 bölüm × 40–45 dk

**Üretim ilkesi:** Senaryo, animasyon, diyagram, grafik ve ekrandaki tüm yazılar Claude tarafından
kodla (Manim) üretilir. Gemini yalnızca sesi üretir: anlatım (TTS, ses: **Sadaltager**), intro müziği (Lyria)
ve ses kalite kontrolü (transkripsiyon).

**Kaynaklar (yürürlükteki tam metinler, itu.int'ten indirildi):**
- G.989.2 (02/2019) + Cor.1 (08/2019) + Amd.1 (10/2020) — PMD katmanı, 122 sayfa
- G.989.3 (05/2021) + Amd.1 (06/2023) + Amd.2 (05/2025) — TC katmanı, 282 sayfa

Her limit ekranda madde ve tablo numarasıyla gösterilir (ör. "G.989.2 §6.2, Tablo 6-1").
"Laboratuvarda" bölümleri, standardın bir ölçüm yöntemi tanımladığı yerlerde (ör. G.989.2 Ek V)
o yöntemi izler. Tanımlamadığı yerlerde mühendislik pratiği olarak etiketlenir.

---

## Seviye

**Hedef: ileri seviye mühendis.** RF/optik/haberleşme altyapısı olan, PON'a özgü kavramları ve G.989
dokümanlarını derinlemesine öğrenmek isteyen izleyici.

| Varsayılan (tekrar anlatılmaz, 1 cümleyle hatırlatılır) | Sıfırdan kurulur |
|---|---|
| dB/dBm, BER ve Q faktörü, göz diyagramı, NRZ | ODN, OPL sınıfları, diferansiyel kayıp ve mesafe |
| Lazer (DFB/DBR), PIN/APD, sönüm oranı | Burst modu, ranging, eşitleme gecikmesi (EqD) |
| Kromatik dispersiyon, yansıma, ORL | TWDM, kanal çifti, kanal yönetimi, ayar sınıfları |
| FEC kavramı (RS kodları), temel ölçüm cihazları | X/S toleransı, OOC/OOB PSD maskeleri, güç dengeleme |
| | G.989.3 ile PMD arasındaki tüm temas noktaları |

**Anlatım dili:** Formüller ekranda (güç bütçesi, Q↔BER, dispersiyon cezası tahmini), 1–2 satırlık
türetme. Gerçek birimler ve eksen ölçekleri, tablo değerleri birebir. Karikatür yok, mühendislik çizimi var.

**Sezon sonu hedefi:** İzleyici G.989.2'nin her PMD tablosunu satır satır açıklayabilir, bir NG-PON2
OLT/ONU için test planı çıkarabilir, PMD'yi ilgilendiren G.989.3 akışlarını (aktivasyon, kanal ayarı,
güç dengeleme, koruma) takip edebilir.

---

## Bölüm formatı (40–45 dk)

| Segment | Süre | İçerik |
|---|---|---|
| **Bölüm özeti** | 60–90 sn | "Bu bölümde…": bölümün soruları ve göreceğimiz şeyler, kısa görsel önizlemelerle |
| **Intro** | 10 sn | Seri müziği + LAMBDA jeneriği + "Bölüm N · Ad" kartı (her bölümde aynı) |
| **Konu anlatımı** | 36–40 dk | 4–6 perde. Her perde: **Standart ne diyor** (madde + tablo) → **Fizik** (neden bu limit) → **Laboratuvarda** (düzenek ve adımlar) → **Mühendis notu**. G.989.3 bağlantıları **"TC Köprüsü"** rozetiyle ayrı alt bölümler |
| **Kapanış** | 1,5–2 dk | 5 maddelik özet, 3 soru (cevaplar sonraki bölümün başında), sonraki bölümün sorusu |

Anlatım sırasında arka plan müziği yok; müzik yalnızca intro'da.

---

## Bölümler ve kaynak eşlemesi

| # | Başlık | G.989.2 | G.989.3 köprüsü | Laboratuvarda |
|---|---|---|---|---|
| 1 | **Işığa Dönüş** — Neden NG-PON2, aile, mimari | §1, §6 (Şekil 6-1, S/R-CG, S/R-CP), §9.1 | §6.1: hat hızı kombinasyonları (Tablo 6-1/6-2), TC alt katmanları, PMD–TC arayüzü (125 µs çerçeve / burst) | Test tezgâhı turu |
| 2 | **Işığın Yolu** — ODN, kayıp ve mesafe | §6.2 (N1/N2/E1/E2), §6.3 (DD20/DD40), §9.3.5 (ORL, yansıma, dispersiyon), Ek XI | §13.1 EqD ve ranging; Ek VII (kanallar arası EqD); Ek X (farklı OPL sınıflı CT'ler) | Ekleme kaybı, ORL, OTDR, referans test ODN'i |
| 3 | **Renk Haritası** — Dalga boyu planı ve birlikte çalışma | §9.2 (Tablo 9-1), §11.1.3, Ek I, Ek VI (Raman), Ek VII (döngüsel AWG), Ek IX | §17.1 profil duyurusu (kanal profilleri) | OSA kanal haritası, CE/WM izolasyonu |
| 4 | **Kaynak** — OLT vericisi ve aşağı yön sinyali | §9.3.2–9.3.4, §11.1.1–11.1.2, §11.1.4.2, §11.1.5 | §8.1 ve §10.1: 125 µs PHY çerçevesi, PSBd, RS(248,216) FEC, karıştırıcı; Ek I (veri deseni koşullandırma) | DCA göz maskesi ve ER, OSA (SMSR, spektral sapma) |
| 5 | **Ayarlanabilir Kulak** — ONU alıcısı ve X/S toleransı | §9.3.6 (hassasiyet, aşırı yük, yol cezası, CID), §10 (X/S maskeleri, Cor.1 Tablo 10-1) | Ek B FEC; §14 başarım izleme ve kusurlar (LODS); §12.1 aktivasyonun ilk adımı | BER–Pin eğrisi, yol cezası, X/S tolerans testi |
| 6 | **Patlama** — ONU vericisi I: burst modu | §11.1.4.3, §11.1.5.2.8–9 (WNE-PSD), §11.1.5.3 göz maskesi, §11.2, Ek III, Ek IV (jitter) | §10.1 yukarı yön burst (PSBu, preamble, delimiter), Ek III burst profilleri, §7 DBA/BWmap zamanlaması | Kapılı DCA, açılma/kapanma zamanlaması, karanlık PSD |
| 7 | **Renk Değiştiren Lazer** — ayarlanabilirlik ve kanal yönetimi | §9.3.7 (Tablo 9-2, Class 1/2/2R1/2R2/3), §9.3.9 OOC maskesi, §11.1.5.2.4–7, Ek VIII | §17.2 kalibrasyon, §17.3 kanal devri, §17.4 kilitleme, Ek F ayar dizileri ve TC ayar süresi, O8/O9 durumları | Ayar süresi, burst içi dalga boyu kayması, OOC gücü |
| 8 | **Kalabalığı Dinlemek** — OLT burst alıcısı, aktivasyon, güç dengeleme | §11.1.4.3 OLT Rx, Ek V (burst edinim süresi ve göz açıklığı ölçümü), Ek D (güç dengeleme) | §12.1 ONU aktivasyonu (seri no., ranging), §19 rogue ONU, §16 güç yönetimi | Ek V ölçümü, burst-mode BER, iki ONU emülatörüyle dinamik aralık |
| 9 | **Özel Hat** — PtP WDM ve AMCC | Ek A (ayarlanabilir PtP WDM), Ek B (şeffaf AMCC), Ek C (düşük kayıplı PtP WDM) | §6.2, §8.2, §10.2, §12.2, §13.3, Ek E (AMCC), Ek G | AMCC modülasyon derinliği ve cezası |
| 10 | **Sahaya İniş** — koruma, izleme, uyumluluk (sezon finali) | Ek II (optik katman izleme ölçümleri), tüm tabloların test matrisi | §18 koruma (Tip B), Ek V–VI (ICTP), §14, Ek H (kanal birleştirme), §15 güvenlik ve diğer PMD dışı başlıklar (kısa harita) | Test planı matrisi, saha ölçümleri, arıza vakaları; final: "bir ONU'nun hayatı" baştan sona |

---

## Üretim akışı (bölüm başına)
1. **Bölüm planı:** dakika dakika akış + madde/tablo eşlemesi
2. **Senaryo:** ~5.500 kelime Türkçe, beat'lere bölünmüş
3. **Ses:** Gemini TTS (Sadaltager) + otomatik transkripsiyon kontrolü
4. **Animasyon:** Manim sahneleri, sese senkron; ortak bileşen kütüphanesi
5. **Render + miks:** 1080p30, −16 LUFS, Türkçe altyazı
