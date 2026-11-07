# LAMBDA — NG-PON2'nin Dili
### Sezon 2 · ITU-T G.989.3 (+ G.989.2 köprüleri) · 10 bölüm × 40–45 dk

**Üretim ilkesi:** Senaryo, animasyon, diyagram, grafik ve ekrandaki tüm yazılar Claude tarafından
kodla (Manim) üretilir. Anlatım yerel XTTS-v2 ile, **kadın sesiyle — "Ana Florence"** üretilir.
Intro müziği Sezon 1 ile aynıdır.

**Kaynaklar (yürürlükteki tam metinler):**
- G.989.3 (05/2021) + Amd.1 (06/2023) + Amd.2 (05/2025) — TC katmanı, 282 sayfa — **ana kaynak**
- G.989.2 (02/2019) + Cor.1 (08/2019) + Amd.1 (10/2020) — PMD katmanı — köprüler için
- G.988 (OMCI) yalnızca G.989.3'ün atıf yaptığı yerde, adıyla anılır; içeriği bu sezonun kapsamı dışındadır.

Her alan, mesaj ve zamanlayıcı ekranda madde, tablo ve şekil numarasıyla gösterilir (ör. "G.989.3 §11.3.3.2,
Tablo 11-5"). Amd.1 ve Amd.2'nin değiştirdiği yerler ayrıca işaretlenir. "Laboratuvarda" bölümleri, standardın
bir yöntem verdiği yerlerde (ör. Ek IV altın vektörler, Ek F ayar süresi) o yöntemi izler; vermediği yerlerde
mühendislik pratiği olarak etiketlenir.

---

## Seviye ve Sezon 1 ile ilişki

**Hedef: ileri seviye mühendis.** Sezon 1'i izlemiş ya da PMD katmanını bilen izleyici. Sezon 1 bir
"fizik" sezonuydu; Sezon 2 bir "dil" sezonudur: ışığın üstünde hangi bitlerin, hangi sırayla, neden taşındığı.

| Sezon 1'den varsayılan (1 cümleyle, bölüm numarasıyla hatırlatılır) | Sezon 2'de sıfırdan kurulur |
|---|---|
| ODN sınıfları, mesafe, EqD fikri (S1·B2) | TC alt katmanları ve kimlikler (PON-ID, ONU-ID, Alloc-ID, XGEM Port-ID) |
| Dalga boyu planı, kanal çiftleri (S1·B3) | Çerçeveleme: BWmap, PLOAM bölmesi, FS yükü, burst başlığı ve kuyruğu |
| PSBd, FEC, karıştırıcı (S1·B4–B5) | XGEM kapsülleme, parçalama, servis eşleme |
| Burst modu, önsöz, sınırlayıcı (S1·B6, B8) | DBA, durum raporlama, düşük gecikme |
| Ayarlanabilirlik, ayar sınıfları (S1·B7) | PLOAM mesaj kataloğu, OMCC |
| Güç dengeleme, burst alıcısı (S1·B8) | Aktivasyon durum makinesi, ranging, günün saati |
| PtP WDM, AMCC (S1·B9) | Kanal yönetimi, devir, kilitleme, bağlama |
| İzleme, koruma (PMD görünümü), ONU'nun hayatı (S1·B10) | Güvenlik, güç yönetimi, kusurlar, koruma ve başıboş ONU |

**Anlatım dili:** Bit alanları ölçekli kutularla (bit genişlikleri birebir), durum makineleri zamanlayıcılarıyla,
mesaj akışları ok diyagramlarıyla. Her PMD bağlantısı **"PMD Köprüsü"** rozetiyle ve ilgili Sezon 1 bölümüne
atıfla verilir (ör. "PMD Köprüsü · S1·B6: önsöz ve sınırlayıcı").

**Sezon sonu hedefi:** İzleyici bir NG-PON2 aşağı yön çerçevesini ve yukarı yön burst'ünü bit bit çözebilir,
bir ONU'nun aktivasyonunu ve kanal devrini mesaj mesaj izleyebilir, bir protokol analizöründe gördüğü her alanı
G.989.3'teki yerine bağlayabilir, ve TC kararlarının PMD üzerindeki etkisini (ve tersini) açıklayabilir.

---

## Bölüm formatı (40–45 dk) — Sezon 1 ile aynı

| Segment | Süre | İçerik |
|---|---|---|
| **Bölüm özeti** | 60–90 sn | "Bu bölümde…" |
| **Intro** | 10 sn | Seri müziği + LAMBDA jeneriği + "Sezon 2 · Bölüm N · Ad" kartı |
| **Önceki bölümde** | 1–2 dk | Önceki bölümün 3 sorusunun cevapları (S2·B1'de: Sezon 1 finalinin soruları) |
| **Konu anlatımı** | 34–38 dk | 4 perde. Her perde: **Standart ne diyor** → **Neden böyle** → **Mühendis notu**; G.989.2 bağlantıları **"PMD Köprüsü"** rozetiyle |
| **Laboratuvarda** | 5–6 dk | Protokol analizörü / OLT–ONU emülatörü / trafik üreteci düzenekleri |
| **Kapanış** | 1,5–2 dk | 5 maddelik özet, 3 soru (cevaplar sonraki bölümün başında), sonraki bölüm |

---

## Bölümler ve kaynak eşlemesi

| # | Başlık | G.989.3 | PMD Köprüsü (G.989.2 · Sezon 1) | Laboratuvarda |
|---|---|---|---|---|
| 1 | **Işığın Dili** — TC katmanına giriş | §6.1 (TC alt katmanları, hat hızı kombinasyonları Tablo 6-1/6-2, yönetim kanalları PLOAM/OMCC/ICTP §6.1.4, kimlik alanları), §6.2 (PtP WDM AMCC TC özeti), Ek VIII (PON-ID ve NG2SYS ID örnekleri) | §6 mimari, kanal grubu/kanal çifti, 125 µs (S1·B1); PSBd (S1·B4); AMCC (S1·B9) | Test tezgâhı 2.0: protokol analizörü, OLT/ONU emülatörü; PON-ID ve sistem kimliğini çözmek |
| 2 | **Çerçeve** — bitten çerçeveye | §10.1 PHY uyarlama (PSBd: PSync, SFC, PON-ID yapısı; FEC Ek B RS(248,216)/(248,232); karıştırıcı ve HEC Ek A; PSBu önsöz/sınırlayıcı; Ek III burst profilleri), §8.1 çerçeveleme (DS FS çerçevesi: HLend, BWmap, PLOAM bölmesi, FS yükü; US FS burst: başlık, tahsisler, kuyruk), §8.2 ve §10.2 (PtP yönetim çerçevesi), Ek IV altın vektörler | PSBd ve FEC (S1·B4), senkron ve LODS (S1·B5), önsöz/sınırlayıcı ve ek yük Tablo 11-11 (S1·B6), burst edinimi (S1·B8) | Ek IV altın vektörlerle çerçeve çözücü doğrulaması; FEC açık/kapalı hata sayaçları |
| 3 | **XGEM** — yükü taşımak | §9 (XGEM başlığı ve alanları, çerçeve sınırlama, SDU parçalama, servislerin XGEM'e eşlenmesi), Ek I (aşağı yön hat verisi desen koşullandırma) | Ardışık özdeş rakam bağışıklığı 72 bit ve karıştırıcı (S1·B5); Ek I ↔ CID | Trafik üreteciyle parçalama ve boşta XGEM; desen koşullandırma testi |
| 4 | **Paylaşım** — kaynak tahsisi ve DBA | §7 (Alloc-ID'ler, BWmap tahsis yapıları, DBRu durum raporu, trafik izleme, DBA referans modeli §7.3, başarım gereksinimleri §7.4), Ek IX (düşük gecikmeli servisler için iş birlikli DBA), Ek J/K (çekişmeli işletim, çarpışma çözümü) | Burst ek yükü ve koruma süresi (S1·B6, Ek III), OLT burst alıcısı (S1·B8) | DBA gecikme ve verim ölçümü; atanmış/garantili bant genişliği testleri |
| 5 | **Yönetim Kanalları** — PLOAM ve OMCC | §11 (PLOAM formatı, 48 bayt, MIC, sıra numaraları; mesaj kataloğu: profil, ONU-ID, ranging, devre dışı bırakma, anahtar, uyku, kalibrasyon, ayar, koruma, güç seviyesi, hız), §6.1.4.3 OMCC (G.988'e atıf) | Kanal profili alanları (S1·B3, B7), burst profili (S1·B6), güç seviyesi değişimi (S1·B8), TOL (S1·B10) | PLOAM yakalama ve çözme; MIC doğrulaması |
| 6 | **Uyanış** — aktivasyon, ranging, günün saati | §12.1 (O1–O9 durumları, zamanlayıcılar, seri numarası edinimi, ranging, ONU-ID ataması, aktivasyon hata ayıklama), §12.2 (PtP aktivasyonu), §13.1 (iletim zamanlaması, EqD, yanıt süresi, sessiz pencere, kayma), §13.2 + Ek II (günün saati ve hata analizi), Ek VII (kanallar arası EqD) | Mesafe sınıfları (S1·B2), burst ve Tx açma (S1·B6), güç dengeleme (S1·B8), "bir ONU'nun hayatı" (S1·B10) | Aktivasyon süresi, ranging doğruluğu, günün saati hata bütçesi |
| 7 | **Renk Değiştirmek** — kanal yönetimi | §17 (profil duyurusu, kalibrasyon, 11 adımlı devir ve hata kodları, kilitleme), Ek F (ayar dizileri, TC ayar süresi), Ek H (kanal bağlama), Ek X (farklı OPL sınıflı CT'ler) | Ayar sınıfları Tablo 9-2, Ek VIII (S1·B7), dalga boyu planı (S1·B3) | Devir süresi ölçümü (hazırlık + PMD ayarı + yeniden senkron); kilitleme kararlılığı |
| 8 | **Güven** — güvenlik | §15 (tehdit modeli, kayıt tabanlı kimlik doğrulama, OMCI ile karşılıklı kimlik doğrulama Ek C, IEEE 802.1X Ek D, anahtar türetme, XGEM yük şifreleme, anahtar değişimi, PLOAM/OMCI bütünlüğü, azaltılmış şifreleme gücü) | Aşağı yönün yayın doğası (S1·B1), başıboş vericiler (S1·B10) | Anahtar değişimi ve etkinleştirme zamanlaması; MIC hatası enjeksiyonu |
| 9 | **Enerji ve Sağlık** — güç yönetimi, sayaçlar, kusurlar | §16 (TWDM güç yönetimi durumları ve parametreleri, kanal seçimiyle güç tasarrufu; PtP hız uyarlama), §14 (başarım sayaçları, OLT ve ONU kusurları, acil durum anlık görüntüsü) | Verici açma/kapama ve karanlık güç (S1·B6), izleme ölçümleri Ek II (S1·B10) | Durumlara göre güç tüketimi; kusur enjeksiyonu ve sayaç doğrulaması |
| 10 | **Ayakta Kalmak** — koruma, başıboş ONU, sezon finali | §18 (B tipi koruma, durum makinesi, zamanlayıcılar), Ek VI (ICTP), §19 (başıboş ONU modelleri, G.984/G.987 ile birlikte yaşama, yabancı ONU'lar, boş pencere), Ek XI (acil durdurma); final: "bir paketin hayatı" — bir Ethernet çerçevesinin XGEM'den ışığa ve geri yolculuğu | Koruma ve izlemenin PMD görünümü (S1·B10), dalga boyu alanında başıboşluk (S1·B7) | Koruma anahtarlama ölçümü; başıboş ONU senaryoları; acil durdurma |

---

## Üretim akışı (bölüm başına)
1. **Bilgi dosyası:** G.989.3 maddelerinden kaynaklı bilgi derlemesi (Amd.1/Amd.2 farkları dahil)
2. **Senaryo:** ~25.000 karakter Türkçe, beat'lere bölünmüş; senaryo JSON'unda `"xtts_speaker": "Ana Florence"`
3. **Ses:** Kullanıcının GPU'sunda yerel XTTS-v2 (`tools/tts_episode.sh`), bulutta transkripsiyon QA
4. **Animasyon:** Manim sahneleri, yer tutucu sürelerle düzen kontrolü, sese senkron
5. **Render + miks:** 1080p30, −16 LUFS
