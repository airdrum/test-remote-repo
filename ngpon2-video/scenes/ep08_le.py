"""B08 · Laboratuvarda (kalabalığı ölçmek) ve Kapanış — serinin son bölümü."""
from ep08_common import *


class E8LabA(Act8):
    HDR, MANIFEST, FIRST = H8["L"], M8("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Kalabalığı ölçmek")
        self.at(self.q("daha zordur", 5))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("OLT alıcısını ölçmek: bir kalabalık üret")
        hint = T("tek bir sinyal değil → bir kalabalık üretmeliyiz", 20, GOLD, BOLD).move_to([0, 2.2, 0])
        em1 = sbox("ONU öyk. #1", "aşırı yük · yakın", NEAR, 3.0, 0.95, 20, 14).move_to([-4.3, 1.1, 0])
        em2 = sbox("ONU öyk. #2", "hassasiyet · uzak", FAR, 3.0, 0.95, 20, 14).move_to([-4.3, -0.3, 0])
        comb = sbox("birleştirici", None, MUTED, 1.9, 0.9, 18).move_to([-0.3, 0.4, 0])
        olt = sbox("OLT alıcısı", None, RX, 2.0, 0.95, 20).move_to([3.2, 0.4, 0])
        la = VGroup(arrow(em1.get_right(), comb.get_corner(UL) + DOWN * 0.2, FEED, 2.5),
                    arrow(em2.get_right(), comb.get_corner(DL) + UP * 0.2, FEED, 2.5),
                    arrow(comb.get_right(), olt.get_left(), FEED, 2.5))
        train, edges, xe = burst_train(-4.6, -2.3, [0.9, 0.35, 0.85, 0.4], BURST, bw=0.7, gap=0.4)
        trl = T("farklı güç · farklı gecikme · sırayla", 16, BURST, BOLD).next_to(train, DOWN, buff=0.18).set_x(-1.6)
        self.at(self.q("bir kalabalık üretmemiz", 12))
        self.play(FadeIn(hint, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.q("iki ONU öykünücüsü,", 18))
        self.play(FadeIn(em1, shift=RIGHT * 0.1), FadeIn(em2, shift=RIGHT * 0.1), run_time=0.7)
        self.at(self.q("sırayla burst gönderir;", 24.6))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in train], lag_ratio=0.15), FadeIn(trl), run_time=0.8)
        self.at(self.q("çıkışları birleştirilip", 26.3))
        self.play(FadeIn(comb), GrowArrow(la[0]), GrowArrow(la[1]), FadeIn(olt), GrowArrow(la[2]), run_time=0.8)
        self.end(pad=0.05)

        self.beat("g1a")
        self.clear(h)
        h = self.show_heading("İki öykünücü neden şart?", h)
        tst = T("asıl sınav: art arda gelen iki farklı güç", 21, GOLD, BOLD).move_to([0, 2.1, 0])
        b1 = Rectangle(width=2.4, height=1.7, stroke_color=NEAR, stroke_width=2.5, fill_color=NEAR, fill_opacity=0.4).move_to([-2.6, 0.2, 0])
        b2 = Rectangle(width=2.4, height=0.5, stroke_color=FAR, stroke_width=2.5, fill_color=FAR, fill_opacity=0.4).move_to([0.8, -0.4, 0])
        b1l = VGroup(T("#1 aşırı yük", 17, NEAR, BOLD), T("en yakın ONU", 14, MUTED)).arrange(DOWN, buff=0.05).next_to(b1, UP, buff=0.12)
        b2l = VGroup(T("#2 hassasiyet", 17, FAR, BOLD), T("en uzak ONU", 14, MUTED)).arrange(DOWN, buff=0.05).next_to(b2, UP, buff=0.12)
        seq = arrow(b1.get_right(), b2.get_left(), MUTED, 3)
        hard = card("en zorlu an", "gürültülü burst'ün hemen ardından\ngelen sessiz burst → kazanç denetimi", None, WARN, w=6.6, h=1.6, tsize=23, bsize=19).move_to([1.4, -2.3, 0])
        self.at(self.q("art arda gelen iki farklı güçtür.", 4.75))
        self.play(FadeIn(tst, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.q("Birinci öykünücüyü aşırı yük düzeyinde,", 7.19))
        self.play(GrowFromEdge(b1, DOWN), FadeIn(b1l), run_time=0.5)
        self.at(self.q("ikincisini hassasiyet düzeyinde,", 14.22))
        self.play(GrowFromEdge(b2, DOWN), FadeIn(b2l), GrowArrow(seq), run_time=0.5)
        self.at(self.q("Gürültülü bir burst'ün hemen ardından", 19.98))
        self.play(FadeIn(hard, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g2")
        self.clear(h)
        self.set_badge("lab")
        h = self.show_heading("Ölçüm 1: burst edinim süresi", h)
        env, edges, xe = burst_env(-4.8, -1.0, 1.3, BURST, widths={"g0": 0.6, "on": 0.6, "pre": 2.0, "dlm": 0.6, "pay": 3.2, "off": 0.6, "g1": 0.6})
        axl = Line([-4.8, -1.0, 0], [xe + 0.1, -1.0, 0], color=MUTED, stroke_width=2)
        t0 = DashedLine([edges["on"][0], -1.0, 0], [edges["on"][0], 1.8, 0], color=GOOD, stroke_width=2)
        t1 = DashedLine([edges["dlm"][1], -1.0, 0], [edges["dlm"][1], 1.8, 0], color=ACC, stroke_width=2)
        t0l = T("burst başı", 14, GOOD, BOLD).next_to(t0, UP, buff=0.05)
        t1l = T("veri güvenilir", 14, ACC, BOLD).next_to(t1, UP, buff=0.05)
        da = DoubleArrow([edges["on"][0], 1.5, 0], [edges["dlm"][1], 1.5, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12)
        dat = T("edinim süresi", 16, GOLD, BOLD).next_to(da, UP, buff=0.04)
        method = T("yöntem: Ek V (G.987.2'ye atıfla)", 18, MUTED, BOLD).move_to([0, -1.9, 0])
        tie = T("= 2. perdedeki önsöz bütçesinin gerçekte kullanılan payı", 19, BURST, BOLD).move_to([0, -2.6, 0])
        self.play(Create(axl), FadeIn(env, shift=UP * 0.1), run_time=0.8)
        self.at(self.q("alıcının veriyi güvenilir okumaya", 2.74))
        self.play(Create(t0), FadeIn(t0l), Create(t1), FadeIn(t1l), GrowFromCenter(da), FadeIn(dat), run_time=0.8)
        self.at(self.q("standardın beşinci ekinde,", 12.89))
        self.play(FadeIn(method, shift=UP * 0.1), self.set_src("G.989.2 Ek V (G.987.2)"), run_time=0.5)
        self.at(self.q("önsöz bütçesinin gerçekte ne kadarının", 18))
        self.play(FadeIn(tie, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g2a")
        self.clear(h)
        h = self.show_heading("Ölçüm 2: göz açıklığı", h)
        note = VGroup(T("göz ancak kilit sonrası, gövdede anlamlı", 20, ACC, BOLD),
                      T("→ ölçümü gövdeye kapıla, önsöze değil", 20, GOOD, BOLD)).arrange(DOWN, buff=0.12).move_to([0, 1.85, 0])
        e = eye(-2.5, -0.2, 3.8, 2.2, GOOD, 0.1)
        em = eye_mask(-2.5, -0.2, 3.8, 2.2, GOLD)
        bad = eye(2.6, -0.2, 3.8, 2.2, WARN, 0.55)
        el = T("iyi kilit → açık göz", 17, GOOD, BOLD).next_to(e, DOWN, buff=0.25)
        bl = T("kötü kilit → temiz sinyalde bile kapalı", 17, WARN, BOLD).next_to(bad, DOWN, buff=0.25)
        self.at(self.q("önsözden sonraki gövdede anlamlıdır.", 6.36))
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
        self.at(self.q("göz ölçümünü burst'ün gövdesine kapılarız,", 8.8))
        self.play(LaggedStart(*[Create(c) for c in e], lag_ratio=0.04), FadeIn(em), FadeIn(el), run_time=0.9)
        self.at(self.q("kötü kilitlenen bir alıcı,", 18.65))
        self.play(LaggedStart(*[Create(c) for c in bad], lag_ratio=0.04), FadeIn(bl), run_time=0.9)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep08_labA")


class E8LabB(Act8):
    HDR, MANIFEST, PREV_BADGE = H8["L"], M8("lab"), "lab"

    def construct(self):
        self.beat("g3")
        self.set_badge("lab")
        h = self.show_heading("Ölçüm 3: dinamik aralık")
        train, edges, xe = burst_train(-4.6, -1.2, [0.95, 0.32], NEAR, bw=1.7, gap=1.0)
        train[1].set_fill(FAR, 0.4).set_stroke(FAR)
        axl = Line([-4.6, -1.2, 0], [xe + 0.2, -1.2, 0], color=MUTED, stroke_width=2)
        l1 = T("aşırı yük", 16, NEAR, BOLD).next_to(train[0], UP, buff=0.12)
        l2 = T("hassasiyet", 16, FAR, BOLD).next_to(train[1], UP, buff=0.12)
        dr = DoubleArrow([xe + 0.8, -1.2, 0], [xe + 0.8, -1.2 + 0.95, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12)
        drt = VGroup(T("≈ 21 dB", 18, GOLD, BOLD), T("tablo penceresi", 13, GOLD)).arrange(DOWN, buff=0.05).next_to(dr, RIGHT, buff=0.12)
        ber = pill("ikisi de aynı alıcıyla · BER referansında çözülmeli", GOOD, 19).move_to([0, 1.9, 0])
        edge = T("güçleri birkaç dB oynatıp sınırları ara", 19, TXT, BOLD).move_to([0, -2.7, 0])
        self.play(Create(axl), FadeIn(train[0], shift=UP * 0.1), FadeIn(l1), run_time=0.6)
        self.at(self.q("biri aşırı yükte biri hassasiyette,", 4.67))
        self.play(FadeIn(train[1], shift=UP * 0.1), FadeIn(l2), run_time=0.5)
        self.at(self.q("aynı alıcıyla hata oranı referansında", 14.67))
        self.play(FadeIn(ber, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.q("Sonra güçleri birkaç desibel", 21.53))
        self.play(FadeIn(edge, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("tablodaki yirmi bir desibeli", 28.19))
        self.play(GrowFromCenter(dr), FadeIn(drt), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g3a")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Ölçüm 4: burst modu hata oranı", h)
        env, edges, xe = burst_env(-4.8, -1.4, 0.4, BURST, widths={"g0": 0.5, "on": 0.5, "pre": 1.6, "dlm": 0.5, "pay": 3.4, "off": 0.5, "g1": 0.5})
        axl = Line([-4.8, -1.4, 0], [xe + 0.1, -1.4, 0], color=MUTED, stroke_width=2)
        x0, x1 = edges["pre"][0], edges["g1"][0]
        xs = np.linspace(x0, x1, 40)
        berpts = [[x, 1.9 - 2.4 * np.exp(-3.2 * (x - x0) / (x1 - x0)), 0] for x in xs]
        bercv = VMobject(stroke_color=WARN, stroke_width=3).set_points_smoothly(berpts)
        berl = T("hata oranı", 15, WARN, BOLD).next_to(bercv, UP, buff=0.05).set_x(x0 + 0.6)
        hot = SurroundingRectangle(Line([edges["pre"][0], -1.3, 0], [edges["dlm"][1], 0.4, 0]), color=WARN, buff=0.03, stroke_width=2.5)
        hotl = T("ilk bitler riskli: edinim oturmadan", 16, WARN, BOLD).move_to([0.5, 1.5, 0])
        cont = T("sürekli modda BER kararlı; burstta konuma bağlı", 18, TXT, BOLD).move_to([0, -2.1, 0])
        ref = VGroup(T("referans:", 20, MUTED, BOLD), T("FEC öncesi " + sup(-3), 24, GOOD, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -2.75, 0])
        self.play(Create(axl), FadeIn(env, shift=UP * 0.1), run_time=0.7)
        self.at(self.q("her burst'ün ilk bitleri,", 7.07))
        self.play(Create(hot), FadeIn(hotl), run_time=0.5)
        self.at(self.q("hata oranını burst boyunca konuma göre", 13.3))
        self.play(Create(bercv), FadeIn(berl), FadeIn(cont), run_time=0.8)
        self.at(self.q("FEC öncesi on üzeri eksi üçtür.", 21.92))
        self.play(FadeIn(ref, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g4")
        self.clear(h)
        self.set_badge("lab")
        h = self.show_heading("Bir ölçüm daha: güç dengelemenin etkisi", h)
        axg, X = lin_axis(-28, -2, -5.6, 5.2, -0.4, [-26, -16, -7], size=14, fmt=lambda v: tr(v), unit="OLT'de alınan güç (dBm)")
        wide = DoubleArrow([X(-26), 1.4, 0], [X(-7), 1.4, 0], buff=0, color=WARN, stroke_width=3, tip_length=0.14)
        widet = T("dengeleme yok: geniş aralık", 18, WARN, BOLD).next_to(wide, UP, buff=0.1)
        narrow = DoubleArrow([X(-26), 0.7, 0], [X(-15), 0.7, 0], buff=0, color=GOOD, stroke_width=3, tip_length=0.14)
        narrowt = T("Perde 3 kuralı → aralık daraldı", 18, GOOD, BOLD).next_to(narrow, DOWN, buff=0.1).align_to(narrow, LEFT)
        red = VGroup(arrow([X(-7), 1.1, 0], [X(-15), 1.1, 0], GOOD, 3), T("−12 dB", 16, GOOD, BOLD).move_to([X(-11), 1.05, 0]))
        tail = T("teorideki 12 dB → tezgahta ölçülen rahatlama", 19, BURST, BOLD).move_to([0, -2.4, 0])
        self.play(Create(axg[0]), FadeIn(axg[1:]), GrowFromCenter(wide), FadeIn(widet), run_time=0.7)
        self.at(self.q("üçüncü perdedeki kurala göre kısıp,", 5.6))
        self.play(GrowArrow(red[0]), FadeIn(red[1]), run_time=0.5)
        self.at(self.q("dinamik aralığın gerçekten daraldığını", 8.57))
        self.play(GrowFromCenter(narrow), FadeIn(narrowt), run_time=0.6)
        self.at(self.q("tezgahta ölçülen bir rahatlamaya", 21.32))
        self.play(FadeIn(tail, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep08_labB")


class E8LabC(Act8):
    HDR, MANIFEST, PREV_BADGE = H8["L"], M8("lab"), "lab"

    def construct(self):
        self.beat("g5")
        self.set_badge("lab")
        h = self.show_heading("Hepsi birlikte: OLT alıcısının karakteri")
        tiles = VGroup(
            card("Hız", "ne kadar hızlı\nkilitleniyor", None, GOOD, w=3.9, h=1.7, tsize=24, bsize=18),
            card("Aralık", "ne kadar geniş\naralığı kaldırıyor", None, BURST, w=3.9, h=1.7, tsize=24, bsize=18),
            card("Toparlanma", "gürültülü → sessiz\nne kadar çabuk", None, GOLD, w=3.9, h=1.7, tsize=24, bsize=18)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.8)
        concl = T("Kalabalığı dinlemenin sınavı budur", 22, GOLD, BOLD).move_to([0, -1.6, 0])
        self.at(self.q("ne kadar hızlı kilitleniyor,", 6.4))
        self.play(FadeIn(tiles[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ne kadar geniş bir aralığı kaldırıyor,", 8.66))
        self.play(FadeIn(tiles[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ne kadar çabuk toparlanıyor.", 11.98))
        self.play(FadeIn(tiles[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("Kalabalığı dinlemenin sınavı budur.", 18.74))
        self.play(FadeIn(concl, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        self.note5("g6", [("1", "Dinamik aralığı art arda geçişle sınayın", "Gürültülüden sessize; iki burst'ü ayrı ölçmek kazanç denetiminin gerçek sınavını atlar.", "Bir:"),
                          ("2", "Göz ve BER'i burst içi konuma göre inceleyin", "Zayıflık neredeyse her zaman önsözün hemen ardında, gövdenin ilk bitlerinde saklıdır.", "İki:")])

        self.beat("g7")
        self.clear()
        self.drop_badge()
        fwd = VGroup(T("TWDM PON'un kalbini tamamladık", 32, ACC, BOLD),
                     T("aşağı yön · yukarı yön · verici · alıcı · ayar · etkinleştirme", 22, TXT, BOLD),
                     T("Bölüm 9: ağacın başka bir dalı", 26, BURST, BOLD),
                     T("noktadan noktaya WDM + yardımcı yönetim kanalı (AMCC)", 21, MUTED, BOLD)).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(fwd[0], shift=UP * 0.1), run_time=0.6)
        self.at(self.q("aşağı yön,", 4.47))
        self.play(FadeIn(fwd[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("Dokuzuncu bölümde ağacın bir başka dalına,", 10.54))
        self.play(FadeIn(fwd[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("noktadan noktaya WDM'e ve yardımcı yönetim", 13.67))
        self.play(FadeIn(fwd[3], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.3)
        self.play(FadeOut(fwd), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep08_labC")


class E8End(Act8):
    HDR, MANIFEST, FIRST = H8["E"], M8("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 8'in özeti")
        self.at(1.6)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["OLT burst alıcısı: ≈ 21 dB dinamik aralık + her burst sıfırdan güç/faz edinimi; referans BER 10⁻³ (FEC öncesi)",
               "PHY ek yük zamanı gard / önsöz / sınırlayıcı; 10G hedef toplam 2048 bit, sınırlayıcı ≥ 16 bit",
               "Güç dengeleme: yakın ONU'yu RSSI'ye göre ≤ 12 dB kısar → dinamik aralık daralır, kanal dışı maske gevşer",
               "Yeni ONU: sessiz pencere + seri numarası + mesafe ölçümü; eşitleme gecikmesi ortak zaman ekseni",
               "Kekeme ONU'lar boş pencere yöntemiyle saptanır ve susturularak yalıtılır"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 19, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        for it in items:
            fit(it, 13.3)
        self.at(self.cue("Bir:", 2.1))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 18.6))
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
            ("Noktadan noktaya WDM\nkanalları neden TWDM'den\nfarklı bir banda ve\nmimariye yerleştirilir?", CH[0]),
            ("Yardımcı yönetim ve\ndenetim kanalı (AMCC)\nnedir ve neden\ngereklidir?", CH[1]),
            ("Düşük kayıplı noktadan\nnoktaya WDM neden ayrı\nbir ek olarak\ntanımlanır?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 9'un başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        self.at(self.cue("noktadan noktaya WDM kanalları,", 3.09))
        self.play(FadeIn(qs[0], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("yardımcı yönetim ve denetim kanalı,", 12.6))
        self.play(FadeIn(qs[1], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("düşük kayıplı noktadan noktaya WDM,", 20.58))
        self.play(FadeIn(qs[2], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında.", 27.6))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        e9 = SERIES["episodes"][8]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Bölüm {e9['n']} · {e9['title']}", 50, TXT, BOLD), T(e9["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.4)
        self.at(self.q("Özel Hat.", 1.4))
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.1)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        topics = VGroup(*[pill(s, c, 18) for s, c in [("noktadan noktaya WDM", ACC), ("AMCC", GOLD), ("özel hatlar", BURST), ("her aboneye kendi rengi", GOOD)]]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.4)
        fit(topics, 13.0)
        self.at(self.q("Noktadan noktaya WDM ve yardımcı", 3.45))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in topics], lag_ratio=0.15), run_time=0.9)
        self.at(self.q("Görüşmek üzere.", 15))
        bye = T("Görüşmek üzere.", 26, TXT, BOLD).move_to(DOWN * 1.7)
        self.play(FadeIn(bye), run_time=0.5)
        self.end(pad=0.5)
        self.play(FadeOut(nxt), FadeOut(topics), FadeOut(bye), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 8 · Kalabalığı Dinlemek", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: XTTS-v2 · Damien Black", 22, ACC, BOLD),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep08_end")
