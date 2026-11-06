# LAMBDA — NG-PON2'nin Fizik Katmanı
### Sezon 1: ITU-T G.989.2 · 10 bölüm × ~40 dk

**Üretim ilkesi:** Senaryo, animasyon, diyagram, grafik ve ekrandaki tüm yazılar Claude tarafından üretilir
(Manim ile, kod olarak). Gemini yalnızca ses için kullanılır: Türkçe anlatım (TTS) ve ses kalite kontrolü.

**Kaynak ilkesi:** Tüm limitler ve tablo değerleri G.989.2 PDF'inden (2019 birleşik sürüm ve ekleri) alınır,
ekranda madde/tablo referansıyla gösterilir. "Laboratuvarda" bölümleri standardın normatif prosedürü değildir;
G.989.2 parametre ve limit tanımlar, ölçüm yöntemi tanımlamaz. Bu kısımlar mühendislik pratiğidir ve öyle etiketlenir.

---

## Bölüm formatı (~40 dk)

| Segment | Süre | İçerik |
|---|---|---|
| Soğuk açılış | 1–2 dk | Sahadan ya da laboratuvardan gerçek bir problem; bölümün sorusu |
| Jenerik | 20 sn | Seri kimliği, bölüm numarası ve adı |
| Önceki bölümlerde | ≤1 dk | B2'den itibaren, bu bölüme bağlanan 3 kavram |
| Perde 1…4/5 | 6–9 dk her biri | Her perde dört adımda: **Standart ne diyor** (parametre + limit tablosu) → **Fizik** (limit neden bu) → **Laboratuvarda** (düzenek, adımlar, hata kaynakları) → **Mühendis notu** (tuzaklar) |
| Özet + mini sınav | 2–3 dk | 5 madde özet, 3 soru (cevaplar bir sonraki bölümün başında) |
| Fragman | 30 sn | Sonraki bölümün sorusu |

Görsel dil: koyu tema, kanal renkleri (λ1–λ4 mor/camgöbeği/yeşil/amber) sezon boyunca sabit. Tekrar kullanılan
bileşenler: spektrum/OSA ekranı, blok diyagram, osiloskop, DCA göz diyagramı, BER–Pin eğrisi, burst zamanlama
diyagramı, limit tablosu kartı, test düzeneği şablonu.

---

## Bölümler

### B1 · "Işığa Dönüş" — Neden NG-PON2 ve G.989.2 haritası
*Soğuk açılış:* 2015, operatör ikilemi: tek dalga boyunda 40G mi, dört dalga boyunda 4×10G mi?
1. PON'un özü: noktadan çok noktaya, TDM/TDMA, burst, ranging
2. Nesiller: GPON → XG-PON → XGS-PON → NG-PON2; neden dalga boyu boyutu eklendi; TWDM ve PtP WDM
3. G.989 ailesi: G.989 / .1 / .2 / .3 — PMD nerede biter, TC nerede başlar
4. Sistem referans modeli: OLT CT'leri, WM, CE, ODN, ONU; referans noktaları
5. Hat hızı kombinasyonları; G.989.2'yi okuma kılavuzu (tablolar, notlar, opsiyonel/zorunlu)

*Laboratuvarda:* Test tezgâhı turu (OSA, DCA, BERT, dalga boyu ölçer, VOA, burst'ü algılayan güç ölçer), sezon boyunca kullanılacak araçlar.
*Fragman:* "Işık 40 km yol alacak; ne kadarını kaybedebilir?"

### B2 · "Işığın Yolu" — ODN, mesafe ve kayıp bütçesi
1. ODN tipleri: güç ayırıcılı, dalga boyu yönlendirmeli, hibrit
2. Optik yol kaybı sınıfları (N1/N2/E1/E2) ve diferansiyel mesafe
3. Fiber etkileri: zayıflama, L-bantta kromatik dispersiyon, yansıma/ORL
4. Güç bütçesi: Tx min − yol kaybı − yol cezası ≥ Rx hassasiyeti (adım adım örnek)

*Laboratuvarda:* Ekleme kaybı (LS+PM), OTDR, ORL; referans test ODN'i kurma (VOA + fiber makarası).

### B3 · "Renk Haritası" — Dalga boyu planı ve birlikte çalışma
1. TWDM bantları (geniş/azaltılmış/dar), PtP WDM spektrumları
2. Kanal ızgaraları (50/100/200 GHz) ve kanal numaralandırma
3. Birlikte çalışma: GPON, XG(S)-PON, RF video, izleme bandı; CE ve izolasyon
4. Çok kanallı sistemde Raman ve nonlineer etkiler

*Laboratuvarda:* OSA ile kanal haritası doğrulama; CE/WM izolasyon ve ekleme kaybı ölçümü.

### B4 · "Kaynak" — OLT vericisi (aşağı yön)
1. Ortalama başlatma gücü, sönüm oranı, göz maskesi
2. Spektral sapma, SMSR, spektral genişlik
3. Kanallar arası güç farkı, yansıma toleransı, jitter

*Laboratuvarda:* DCA ile göz maskesi ve ER (referans alıcı, kalibrasyon tuzakları); OSA ve dalga boyu ölçer; sıcaklık taraması.

### B5 · "Ayarlanabilir Kulak" — ONU alıcısı
1. Hassasiyet, aşırı yük, BER referans seviyesi ve FEC
2. Ayarlanabilir alıcı filtresi ve kanal seçimi
3. Crosstalk: kanallar arası ve kanal dışı; tolerans gereksinimleri
4. CID bağışıklığı, jitter toleransı

*Laboratuvarda:* BER–Pin eğrisi, yol cezası ölçümü, girişimci kanallarla crosstalk tolerans testi.

### B6 · "Patlama" — ONU vericisi I: burst modu
1. Burst anatomisi: açılma/kapanma zamanları, preamble (TC katmanına köprü)
2. Burst modda güç, ER ve göz maskesi
3. Kapalıyken verici gücü: TWDM'de komşu kanala sızma neden kritik

*Laboratuvarda:* Kapılı DCA ölçümü, açılma/kapanma zamanlaması, karanlık güç ölçümü.

### B7 · "Renk Değiştiren Lazer" — ONU vericisi II: ayarlanabilirlik
1. Ayarlanabilir lazer teknolojileri (termal DFB, DBR, …)
2. Kalibrasyon ve ilk kanal edinimi (G.989.3 köprüsü)
3. Ayar süresi sınıfları
4. Burst içi dalga boyu kayması, spektral sapma, kanal dışı emisyon; rogue ONU

*Laboratuvarda:* Ayar süresi ölçümü, burst içi dalga boyu kayması ölçümü, kanal dışı güç ölçümü.

### B8 · "Kalabalığı Dinlemek" — OLT burst alıcısı ve yukarı yön sistemi
1. Burst alıcı hassasiyeti ve dinamik aralık
2. Burst'ten burst'e güç farkı (yakın–uzak), oturma süresi
3. Yukarı yön kanal izolasyonu, WM, crosstalk

*Laboratuvarda:* Burst-mode BER, iki ONU emülatörüyle dinamik aralık testi, oturma süresi ölçümü.

### B9 · "Özel Hat" — PtP WDM ve AMCC
1. PtP WDM'nin rolü (kurumsal, mobil fronthaul)
2. Hız sınıfları ve spektrum kullanımı
3. AMCC: yöntemler, modülasyon derinliği, getirdiği ceza

*Laboratuvarda:* AMCC modülasyon derinliği ve ceza ölçümü.

### B10 · "Sahaya İniş" — Uyumluluk, birlikte çalışabilirlik, saha (sezon finali)
1. G.989.2'den test planına: parametre → test case matrisi
2. Çevresel koşullar: sıcaklık, yaşlanma, marj yönetimi
3. Birlikte çalışabilirlik ve sertifikasyon yaklaşımı
4. Saha: kanal ayırt eden burst-aware güç ölçer, OTDR izleme, arıza vakaları

*Final:* Sezonun tüm parametre haritası tek ekranda.

---

## Üretim akışı (bölüm başına)
1. **Bölüm planı:** dakika dakika akış + G.989.2 madde/tablo eşlemesi → onay
2. **Senaryo:** ~5.000 kelime Türkçe, beat'lere bölünmüş → onay
3. **Ses:** Gemini TTS + otomatik transkripsiyon kontrolü
4. **Animasyon:** Manim sahneleri, sese senkron
5. **Render + miks:** 1080p30, −16 LUFS, Türkçe altyazı → teslim

İlk bölüm, ortak bileşen kütüphanesi ve jenerik de kurulacağı için en uzun süreni olacak.
