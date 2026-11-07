"""B06 · Laboratuvarda (burst'ü ölçmek) ve Kapanış."""
from ep06_common import *


class E6LabA(Act6):
    HDR, MANIFEST, FIRST = H6["L"], M6("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Burst'ü ölçmek")
        self.at(self.q("ölçeceğiz:", 3))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Üç ölçüm · ortak zorluk: tetikleme")
        tiles = VGroup(
            card("Kapılı göz", "burst temiz\nbaşlıyor mu", None, GOOD, w=3.9, h=1.6, tsize=24, bsize=18),
            card("Açılma / kapanma", "ne kadar\nhızlı", None, BURST, w=3.9, h=1.6, tsize=24, bsize=18),
            card("Karanlık güç", "kapalıyken\nsessiz mi", None, LEAK, w=3.9, h=1.6, tsize=24, bsize=18)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.35)
        y = -1.4
        tl = Line([-5.4, y, 0], [5.4, y, 0], color=MUTED, stroke_width=2)
        bl = VGroup(*[Rectangle(width=1.1, height=0.55, stroke_color=BURST, stroke_width=2, fill_color=BURST, fill_opacity=0.5).move_to([x, y + 0.3, 0]) for x in (-3.3, 0.0, 3.3)])
        trig = VGroup(Line([0.0 - 0.55, y - 0.55, 0], [0.0 - 0.55, y + 0.85, 0], color=GOLD, stroke_width=3),
                      T("tetik", 15, GOLD, BOLD).move_to([0.0 - 0.55, y - 0.8, 0]))
        cap = T("sinyal yanıp sönüyor → her alet doğru ana tetiklenmeli", 19, GOOD, BOLD).move_to([0, -2.8, 0])
        self.at(self.q("kapılı göz,", 5.5))
        self.play(FadeIn(tiles[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("açılma ve kapanma zamanlaması,", 6.4))
        self.play(FadeIn(tiles[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ve karanlıktaki güç.", 9))
        self.play(FadeIn(tiles[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("yanıp sönüyor;", 13))
        self.play(Create(tl), LaggedStart(*[FadeIn(b, scale=0.8) for b in bl], lag_ratio=0.2), run_time=0.7)
        self.at(self.q("doğru ana tetiklenmelidir.", 16.5))
        self.play(Create(trig), FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g1a")
        self.clear(h)
        h = self.show_heading("Düzenek: DCA + filtre + Thomson", h)
        yb = 0.95
        onu = sbox("ONU", "sürekli burst", BURST, 1.9, 1.0, 19, 14).move_to([-5.1, yb, 0])
        filt = sbox("ısıl ayarlı\nfiltre", "↑ kanalı", PINK, 2.2, 1.0, 17, 13).move_to([-2.3, yb, 0])
        oe = sbox("O-E", None, GOLD, 1.3, 1.0, 18).move_to([0.2, yb, 0])
        thom = sbox("Thomson 4.d.", "f₃dB=0,75×R", ACC, 2.5, 1.0, 17, 13).move_to([2.9, yb, 0])
        dca = instrument("DCA", 2.3, 1.6).move_to([2.9, -1.6, 0])
        links = VGroup(Line(onu.get_right(), filt.get_left(), color=FEED, stroke_width=2.5),
                       Line(filt.get_right(), oe.get_left(), color=FEED, stroke_width=2.5),
                       Line(oe.get_right(), thom.get_left(), color=FEED, stroke_width=2.5),
                       arrow(thom.get_bottom(), dca.get_top() + UP * 0.1, FEED, 2.5))
        src = T("gerçek OLT ya da burst üreteci ile sürekli burst", 17, MUTED, BOLD).next_to(onu, DOWN, buff=0.3).set_x(-2.0)
        cut = T("kesim frekansı = bit hızının 0,75 katı", 18, ACC, BOLD).move_to([-2.4, -1.9, 0])
        self.play(FadeIn(onu), FadeIn(src), run_time=0.5)
        self.at(self.q("ısıl ayarlı bir filtre,", 7))
        self.play(FadeIn(filt), Create(links[0]), FadeIn(oe), Create(links[1]), run_time=0.7)
        self.at(self.q("dördüncü dereceden Thomson filtresi", 14))
        self.play(FadeIn(thom), Create(links[2]), FadeIn(dca), GrowArrow(links[3]), run_time=0.8)
        self.at(self.q("sıfır virgül yetmiş beş katı.", 20.6))
        self.play(FadeIn(cut, shift=UP * 0.1), self.set_src("G.989.2 §11.1.4.3 · Thomson 4. derece"), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Ölçüm 1: kapılı göz", h)
        bad = eye(-3.4, 0.6, 3.0, 1.5, MUTED, 0.0)
        pull = VGroup(*[Line([-3.4 - 1.3 + i * 0.5, -0.5, 0], [-3.4 - 1.3 + i * 0.5, -0.9, 0], color=WARN, stroke_width=3) for i in range(6)])
        badt = VGroup(T("serbest çalıştır:", 18, WARN, BOLD), T("karanlık anlar gözü\naşağı çeker → maske\nanlamsız", 16, TXT, line_spacing=0.9)).arrange(DOWN, buff=0.1).next_to(bad, DOWN, buff=0.35)
        good = eye(3.4, 0.6, 3.0, 1.5, GOOD, 0.1)
        gmask = eye_mask(3.4, 0.6, 3.0, 1.5, GOLD)
        goodt = VGroup(T("burst başına kapıla:", 18, GOOD, BOLD), T("sadece açıkken · önsözün\nilk bitlerinde örnek al", 16, TXT, line_spacing=0.9)).arrange(DOWN, buff=0.1).next_to(good, DOWN, buff=0.35)
        arr = arrow([-1.3, 0.6, 0], [1.3, 0.6, 0], ACC, 3)
        self.play(LaggedStart(*[Create(c) for c in bad], lag_ratio=0.04), run_time=0.8)
        self.at(self.q("gözü aşağı çeker ve maskeyi anlamsız", 5.2))
        self.play(Create(pull), FadeIn(badt), run_time=0.6)
        self.at(self.q("burst'ün başlangıcına kapılamaktır:", 12.66))
        self.play(GrowArrow(arr), LaggedStart(*[Create(c) for c in good], lag_ratio=0.04), run_time=0.9)
        self.at(self.q("önsözün ilk bitlerinde örnek alır.", 18.58))
        self.play(FadeIn(gmask), FadeIn(goodt), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g2a")
        self.clear(h)
        h = self.show_heading("Göz maskesini ilk bitlerde uygula", h)
        e = eye(-1.6, 0.4, 4.2, 2.6, BURST, 0.13)
        mask = eye_mask(-1.6, 0.4, 4.2, 2.6, GOLD)
        specs = VGroup(T("dikdörtgen genişliği", 19, TXT, BOLD), T("x₃ − x₂ = 0,2 UI", 24, GOLD, BOLD),
                       T("dikey kenarlar", 19, TXT, BOLD), T("y₁, y₂ = 0,25 · 0,75", 24, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, 0.9, 0])
        honest = VGroup(T("ihlaller: önsözün başında, lazer oturmadan", 18, WARN, BOLD),
                        T("dürüst ölçüm ilk bitleri sınar — kapıyı ortaya kaydırma", 18, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, -2.6, 0])
        self.play(LaggedStart(*[Create(c) for c in e], lag_ratio=0.04), run_time=0.9)
        self.at(self.q("burst'ün ilk bitlerinde uygularız:", 2))
        self.play(FadeIn(mask), run_time=0.5)
        self.at(self.q("dikdörtgen genişliği sıfır virgül iki", 4.48))
        self.play(FadeIn(specs[0]), FadeIn(specs[1]), run_time=0.5)
        self.play(FadeIn(specs[2]), FadeIn(specs[3]), run_time=0.5)
        self.at(self.q("lazer henüz oturmadan görülür.", 15.24))
        self.play(FadeIn(honest[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("dürüst ölçüm,", 22.36))
        self.play(FadeIn(honest[1], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep06_labA")


class E6LabB(Act6):
    HDR, MANIFEST, PREV_BADGE = H6["L"], M6("lab"), "lab"

    def construct(self):
        self.beat("g3")
        self.set_badge("lab")
        h = self.show_heading("Ölçüm 2: açılma / kapanma zamanlaması")
        env, edges, xe = burst_env(-4.8, -1.2, 1.2, BURST, widths={"g0": 0.8, "on": 0.9, "pre": 1.5, "dlm": 0.5, "pay": 3.0, "off": 0.9, "g1": 0.8})
        axl = Line([-4.8, -1.2, 0], [xe + 0.1, -1.2, 0], color=MUTED, stroke_width=2)
        dark = DashedLine([-4.8, -1.2, 0], [xe, -1.2, 0], color=DARK, stroke_width=1.5)
        full = DashedLine([-4.8, 1.2, 0], [xe, 1.2, 0], color=MUTED, stroke_width=1.5)
        dl = T("karanlık düzey", 13, DARK, BOLD).next_to(dark, LEFT, buff=0.05).set_y(-1.2)
        fl = T("tam güç", 13, MUTED, BOLD).next_to(full, LEFT, buff=0.05).set_y(1.2)
        onr = SurroundingRectangle(Line([edges["on"][0], -1.2, 0], [edges["on"][1], 1.2, 0]), color=GOOD, buff=0.03, stroke_width=2.5)
        ofr = SurroundingRectangle(Line([edges["off"][0], -1.2, 0], [edges["off"][1], 1.2, 0]), color=WARN, buff=0.03, stroke_width=2.5)
        onl = T("açılma", 16, GOOD, BOLD).next_to(onr, UP, buff=0.12)
        ofl = T("kapanma", 16, WARN, BOLD).next_to(ofr, UP, buff=0.12)
        val = VGroup(T("her ikisi ≤ 1280 bit", 26, TXT, BOLD), T("= 128,6 ns  (10G)", 24, BURST, BOLD)).arrange(DOWN, buff=0.12).move_to([0, -2.6, 0])
        self.play(Create(axl), FadeIn(env, shift=UP * 0.1), Create(dark), Create(full), FadeIn(dl), FadeIn(fl), run_time=0.9)
        self.at(self.q("gücün karanlık düzeyden tam güce", 11.17))
        self.play(Create(onr), FadeIn(onl), Create(ofr), FadeIn(ofl), run_time=0.7)
        self.at(self.q("bin iki yüz seksen bit,", 18.77))
        self.play(FadeIn(val[0], shift=UP * 0.1), self.set_src("G.989.2 §11.1.4.3, Tablo 11-9"), run_time=0.5)
        self.at(self.q("yüz yirmi sekiz virgül altı nanosaniye", 23.05))
        self.play(FadeIn(val[1], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g3a")
        self.clear(h)
        h = self.show_heading("İki eşiği karıştırma", h)
        defn = VGroup(T("geçiş süresi:", 20, TXT, BOLD), T("karanlık düzey ↔ çalışma düzeyi arasında tanımlı", 20, ACC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, 1.9, 0])
        levels = VGroup(T("referans düzeyler:  '1' · '0' · karanlık", 20, GOLD, BOLD)).move_to([0, 0.9, 0])
        bud = card("bu süre → koruma bütçesi", "4 ONU'nun geçişleri çakışırsa\nkaybedilen zaman katlanır", None, WARN, w=8.2, h=1.7, tsize=23, bsize=20).move_to([0, -1.1, 0])
        self.play(FadeIn(defn, shift=UP * 0.1), run_time=0.6)
        self.at(self.q("karanlık düzey ile çalışma düzeyi", 4.61))
        self.play(FadeIn(levels, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("doğrudan koruma süresi bütçenize girer;", 16.75))
        self.play(FadeIn(bud, shift=UP * 0.1), run_time=0.6)
        self.at(self.q("kaybedilen zaman katlanır.", 23))
        self.play(Indicate(bud, color=WARN, scale_factor=1.03), run_time=0.7)
        self.end(pad=0.05)

        self.beat("g4")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Ölçüm 3: karanlıktaki güç", h)
        step = VGroup(T("vericiyi kapat: başkasının burst'ünü taklit et", 20, TXT, BOLD)).move_to([0, 1.9, 0])
        crit = VGroup(T("KRİTİK:", 24, WARN, BOLD), T("lazeri gerçek çalışma ön gerilimiyle kapat", 22, GOLD, BOLD)).arrange(RIGHT, buff=0.3).move_to([0, 0.9, 0])
        bias = Arrow([-5.0, -2.2, 0], [-5.0, 0.2, 0], buff=0, color=MUTED, stroke_width=3, tip_length=0.18)
        biasl = T("optik güç", 14, MUTED).next_to(bias, UP, buff=0.05)
        real = VGroup(Dot([-3.6, -1.55, 0], radius=0.1, color=GOLD), T("sahada: eşiğe yakın ön gerilim\n→ gerçek karanlık", 16, GOLD, BOLD, line_spacing=0.9).next_to([-3.6, -1.55, 0], RIGHT, buff=0.3))
        full = VGroup(Dot([-3.6, -2.15, 0], radius=0.1, color=WARN), T("tamamen söndür → iyimser / yanlış", 16, WARN, BOLD).next_to([-3.6, -2.15, 0], RIGHT, buff=0.3))
        self.play(FadeIn(step, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("gerçek çalışma ön gerilimiyle kapatın.", 14.68))
        self.play(FadeIn(crit, shift=UP * 0.1), GrowArrow(bias), FadeIn(biasl), run_time=0.6)
        self.at(self.q("eşiğe yakın tutulur;", 18.07))
        self.play(FadeIn(real[0], scale=0.5), FadeIn(real[1]), run_time=0.6)
        self.at(self.q("iyimser bir sonuca götürür", 26.41))
        self.play(FadeIn(full[0], scale=0.5), FadeIn(full[1]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g4a")
        self.clear(h)
        self.set_badge("lab")
        h = self.show_heading("Karanlık güç + maskeler", h)
        osa = instrument("OSA", 2.6, 1.9).move_to([-4.0, 0.3, 0])
        pm = instr("PM", 2.4, 1.7, "−62,6 dBm", "karanlık · 15 GHz", LEAK).move_to([-0.9, 0.3, 0])
        rbw = T("15 GHz çözünürlük bandı", 16, MUTED, BOLD).next_to(VGroup(osa, pm), DOWN, buff=0.25)
        tb = table(["sınır (10G ↑)", "dBm / 15 GHz"],
                   [["WNE-PSD", "−62,6"], ["bant dışı (tüm dışı)", "−57,4"], ["kanal dışı (50 GHz)", "−36,7"]],
                   [3.6, 2.8], size=20, hsize=16, row_h=0.56).move_to([3.4, 0.5, 0])
        self.play(FadeIn(osa, shift=UP * 0.1), FadeIn(pm, shift=UP * 0.1), run_time=0.7)
        self.at(self.q("on beş gigahertzlik bir çözünürlük", 1.08))
        self.play(FadeIn(rbw), run_time=0.4)
        self.at(self.q("eksi altmış iki virgül altı dBm.", 8.85))
        self.play(FadeIn(tb[0]), FadeIn(tb[1], shift=UP * 0.05), self.set_src("G.989.2 §11.1.5.2.8–9"), run_time=0.6)
        self.at(self.q("elli gigahertzde eksi otuz altı virgül yedi", 21.04))
        self.play(FadeIn(tb[2], shift=UP * 0.05), FadeIn(tb[3], shift=UP * 0.05), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep06_labB")


class E6LabC(Act6):
    HDR, MANIFEST, PREV_BADGE = H6["L"], M6("lab"), "lab"

    def construct(self):
        self.beat("g5")
        self.set_badge("lab")
        h = self.show_heading("Üç ölçüm, bir hikaye")
        tiles = VGroup(
            card("Kapılı göz", "burst temiz\nbaşladı mı", None, GOOD, w=3.9, h=1.7, tsize=23, bsize=18),
            card("Zamanlama", "ne kadar\nhızlı", None, BURST, w=3.9, h=1.7, tsize=23, bsize=18),
            card("Karanlık güç", "kapalıyken\nne kadar sessiz", None, LEAK, w=3.9, h=1.7, tsize=23, bsize=18)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.8)
        concl = T("üçünü birden geçmeden kalabalık yukarı yöne güvenle katılamaz", 20, GOLD, BOLD).move_to([0, -1.6, 0])
        self.at(self.q("burst'ün temiz başlayıp", 3.6))
        self.play(FadeIn(tiles[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ne kadar hızlı açılıp kapandığını;", 7.77))
        self.play(FadeIn(tiles[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("kapalıyken ne kadar sessiz", 11.55))
        self.play(FadeIn(tiles[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("güvenle katılamaz.", 18.1))
        self.play(FadeIn(concl, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        self.note5("g6", [("1", "Her ölçümü tetiklenmiş yapın", "Tetiği burst'ün başına koyun; serbest çalışan hiçbir alet patlamalı sinyal hakkında dürüst değildir.", "Bir:"),
                          ("2", "Karanlığı gerçek ön gerilimle ölçün", "Bir değil çok sayıda ardışık sessiz pencerede tekrarlayın; sahada sizi 63 komşunun toplamı bulur.", "İki:")])

        self.beat("g7")
        self.clear()
        self.drop_badge()
        fwd = VGroup(T("Bölüm 8'in zemini", 30, ACC, BOLD),
                     T("Bugün: burst'ü GÖNDEREN taraf (ONU vericisi)", 24, TXT, BOLD),
                     T("Bölüm 8: burst'ü ALAN taraf — OLT burst alıcısı", 24, BURST, BOLD),
                     T("Önsözü ne kadar hızlı çözdüğü, bugün ölçtüğümüz\naçılma ve karanlık değerlerine bağlı", 21, MUTED, BOLD, line_spacing=0.9)).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeIn(fwd[0], shift=UP * 0.1), run_time=0.6)
        self.at(self.q("sekizinci bölümün zeminini kurar:", 1.98))
        self.play(FadeIn(fwd[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("OLT burst alıcısı olacak.", 8.04))
        self.play(FadeIn(fwd[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("açılma ve karanlık değerlerine bağlıdır", 13.19))
        self.play(FadeIn(fwd[3], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.3)
        self.play(FadeOut(fwd), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep06_labC")


class E6End(Act6):
    HDR, MANIFEST, FIRST = H6["E"], M6("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 6'nın özeti")
        self.at(1.4)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["Yukarı yön paylaşımlı → ONU burst modu; açılma/kapanma geçişi 1280 bit = 128,6 ns (10G)",
               "Kapalı verici karanlık değil: WNE-PSD −62,6 dBm/15 GHz + bant dışı / kanal dışı maskeler",
               "Burst ilk bitinden temiz: göz maskesi · titreşim · SMSR ≥ 30 dB",
               "TC: önsöz + sınırlayıcı = burst profili (OLT PLOAM ile duyurur, haritayla burst başına seçer); yük RS FEC",
               "Yukarı yönün tamamı merkezden, bant genişliği haritasıyla zamanlanır"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 20, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        for it in items:
            fit(it, 13.2)
        self.at(self.cue("Bir:", 1.8))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 19.4))
        self.play(FadeIn(items[1], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.05)

        self.beat("h2")
        for k, key in zip([2, 3, 4], ["Üç:", "Dört:", "Beş:"]):
            self.at(self.cue(key, 0.3))
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.7, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Ayar sırasında kanal dışı\ngüç maskesi gevşetilir mi?\nStandart bu anı\nnasıl ele alır?", CH[0]),
            ("Ayarlanabilir ONU vericisinin\nayar süresi sınıfları, Tablo 9-2'de\nneden tek değer değil,\nbir aralıkla tanımlanır?", CH[1]),
            ("Bir ONU bir kanaldan diğerine\ngeçerken, geçişin fiziksel\nkatman süresi ile TC katmanı\nsüresi neden farklıdır?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 7'nin başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        self.at(self.cue("Birinci soru:", 1.7))
        self.play(FadeIn(qs[0], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("ayar süresi sınıfları,", 9.5))
        self.play(FadeIn(qs[1], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("fiziksel katman süresiyle TC katmanı süresi", 26.6))
        self.play(FadeIn(qs[2], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında.", 33.3))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        e7 = SERIES["episodes"][6]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Bölüm {e7['n']} · {e7['title']}", 50, TXT, BOLD), T(e7["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.4)
        self.at(self.q("Renk Değiştiren Lazer.", 1.4))
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.1)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        topics = VGroup(*[pill(s, c, 18) for s, c in [("ayar sınıfları", ACC), ("kanal dışı maske", LEAK), ("kalibrasyon", GOLD), ("kanal devri · kilitleme", BURST)]]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.4)
        fit(topics, 13.0)
        self.at(self.q("ayar sınıfları,", 8.5))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in topics], lag_ratio=0.15), run_time=0.9)
        self.at(self.q("Görüşmek üzere.", 15))
        bye = T("Görüşmek üzere.", 26, TXT, BOLD).move_to(DOWN * 1.7)
        self.play(FadeIn(bye), run_time=0.5)
        self.end(pad=0.5)
        self.play(FadeOut(nxt), FadeOut(topics), FadeOut(bye), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 6 · Patlama", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: XTTS-v2 · Damien Black", 22, ACC, BOLD),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep06_end")
