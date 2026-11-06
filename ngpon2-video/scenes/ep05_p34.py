"""B05 · Perde 3 (zaman ve ayar) and Perde 4 (senkron, FEC ve ilk adımlar)."""
from ep05_common import *


def square(x0, x1, y, h, n, color, sw=2.5):
    tb = (x1 - x0) / (2 * n)
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(nrz([1, 0] * n, x0, tb, y - h / 2, y + h / 2, rise=0.02))


def wave(bits, x0, x1, y, h, color, sw=2.5):
    tb = (x1 - x0) / len(bits)
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(nrz(bits, x0, tb, y - h / 2, y + h / 2, rise=min(0.04, tb * 0.3)))


class E5P3A(Act5):
    HDR, MANIFEST, FIRST = H5[3], M5("p3"), True

    def construct(self):
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Zaman ve ayar")
        self.at(self.cue("Aşağı yön sürekli", 1))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Saat çıkarımı — §9.3.6.5")
        y1, y2 = 1.15, -1.25
        l1 = T("↓ sürekli sinyal", 20, TW_DS, BOLD).move_to([-5.6, y1 + 0.6, 0])
        bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
        w1 = wave(bits, -6.6, -1.6, y1, 0.6, TW_DS)
        cdr = sbox("CDR", "saat çıkarıcı", ACC, 1.6, 0.9, 20, 15).move_to([-0.4, y1, 0])
        a1 = arrow([-1.55, y1, 0], cdr.get_left(), MUTED)
        clk = square(1.6, 6.4, y1, 0.5, 12, GOLD)
        a2 = arrow(cdr.get_right(), [1.5, y1, 0], MUTED)
        clt = T("saat", 18, GOLD, BOLD).next_to(clk, UP, buff=0.12)
        conv = T("geleneksel saat çıkarımı", 18, ACC, BOLD).next_to(cdr, DOWN, buff=0.15)
        l2 = T("↑ burst (OLT alıcısı)", 20, TW_US, BOLD).move_to([-5.3, y2 + 0.65, 0])
        idle = Line([-6.6, y2 - 0.3, 0], [-5.4, y2 - 0.3, 0], color=TW_US, stroke_width=2.5)
        pre = wave([1, 0] * 8, -5.4, -3.0, y2, 0.6, GOLD)
        dat = wave([1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1], -3.0, -0.6, y2, 0.6, TW_US)
        idle2 = Line([-0.6, y2 - 0.3, 0], [0.2, y2 - 0.3, 0], color=TW_US, stroke_width=2.5)
        prl = T("önsöz: değişen bitler", 16, GOLD, BOLD).next_to(pre, DOWN, buff=0.15)
        bt = VGroup(T("önsözden hızlı saat çıkarımı", 19, TXT, BOLD), pill("→ Bölüm 8", ACC, 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, y2, 0])
        self.at(self.cue("ve ONU saatini", 3.4))
        self.play(FadeIn(l1), Create(w1), run_time=0.8)
        self.play(GrowArrow(a1), FadeIn(cdr), GrowArrow(a2), Create(clk), FadeIn(clt), run_time=0.9)
        self.at(self.cue("standart bunu geleneksel", 6.1))
        self.play(FadeIn(conv, shift=UP * 0.1), self.set_src("G.989.2 §9.3.6.5"), run_time=0.5)
        self.at(self.cue("Yukarı yöndeki burst", 10.3))
        self.play(FadeIn(l2), Create(idle), Create(pre), Create(dat), Create(idle2), run_time=1.0)
        self.play(FadeIn(prl), FadeIn(bt[0]), run_time=0.5)
        self.at(self.cue("onu sekizinci", 18.9))
        self.play(FadeIn(bt[1], shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        self.beat("d1a")
        self.clear(h)
        h = self.show_heading("Alıcının saati = vericinin saati", h)
        olt = sbox("OLT", "PON'un saati", "#94A3B8", 1.6, 1.0, 20, 15).move_to([-5.6, 0.6, 0])
        onu = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=6.4, height=2.6, color=SIG, stroke_width=2), num_dashes=60).move_to([1.6, 0.6, 0])
        onut = T("ONU", 20, SIG, BOLD).next_to(onu, UP, buff=0.08).align_to(onu, LEFT).shift(RIGHT * 0.2)
        rx = sbox("alıcı · CDR", None, ACC, 2.0, 0.75, 18).move_to([-0.2, 1.25, 0])
        tx = sbox("verici", None, TW_US, 2.0, 0.75, 18).move_to([3.4, -0.05, 0])
        dn = arrow([-4.75, 1.25, 0], rx.get_left(), TW_DS, 3)
        up = arrow(tx.get_left() + LEFT * 0.0, [-4.75, -0.05, 0], TW_US, 3)
        dnl = T("↓", 22, TW_DS, BOLD).next_to(dn, UP, buff=0.05)
        upl = T("↑", 22, TW_US, BOLD).next_to(up, DOWN, buff=0.05)
        ck = CurvedArrow(rx.get_right() + DOWN * 0.1, tx.get_top(), angle=-1.0, color=GOLD, stroke_width=3, tip_length=0.15)
        ckt = T("saat", 18, GOLD, BOLD).move_to([3.3, 1.2, 0])
        rule = T("↑ frekans doğruluğu = alınan ↓ sinyalinki (§11.1.1.2)", 20, TXT, BOLD).move_to(DOWN * 1.35)
        p1 = pill("normal çalışma: Stratum-1'e izlenebilir", GOOD, 18)
        p2 = pill("serbest çalışma: ≥ Stratum-4 · 32 ppm", GOLD, 18)
        ps = VGroup(p1, p2).arrange(RIGHT, buff=0.4).move_to(DOWN * 2.35)
        self.play(FadeIn(olt), Create(onu), FadeIn(onut), FadeIn(rx), FadeIn(tx), run_time=0.8)
        self.at(self.cue("ONU'nun yukarı", 4.7))
        self.play(GrowArrow(dn), FadeIn(dnl), GrowArrow(up), FadeIn(upl), run_time=0.7)
        self.at(self.cue("alınan aşağı yön", 6.3))
        self.play(FadeIn(rule, shift=UP * 0.1), self.set_src("G.989.2 §11.1.1"), run_time=0.5)
        self.at(self.cue("Yani alıcının", 11.9))
        self.play(Create(ck), FadeIn(ckt), run_time=0.7)
        self.at(self.cue("Aşağı yön saati", 16.7))
        self.play(FadeIn(p1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("serbest çalışmada", 21))
        self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d2")
        self.clear(h)
        h = self.show_heading("Ardışık özdeş rakam (CID) bağışıklığı", h)
        bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1] + [0] * 22 + [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
        x0, x1, yw = -6.3, 6.3, 1.0
        w = wave(bits, x0, x1, yw, 0.7, TW_DS)
        tb = (x1 - x0) / len(bits)
        trans = VGroup(*[Dot([x0 + i * tb, yw - 0.6, 0], radius=0.045, color=ACC) for i in range(1, len(bits)) if bits[i] != bits[i - 1]])
        trl = T("geçişler → saat çıkarıcı kilitli", 17, ACC, BOLD).move_to([x0 + 6 * tb, yw - 0.95, 0])
        run = Rectangle(width=22 * tb, height=1.05, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.1).move_to([x0 + 23 * tb, yw, 0])
        rl = T("geçişsiz bitler", 18, GOLD, BOLD).next_to(run, UP, buff=0.1)
        big = VGroup(T("CID bağışıklığı", 24, TXT, BOLD), T("72 bit", 40, GOLD, BOLD), T("2,5G ve 10G", 20, MUTED)).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.75)
        scr = VGroup(sbox("karıştırıcı", None, TW_DS, 2.0, 0.65, 18), T("uzun 0 / 1 dizilerini olasılıksal olarak kırar", 19, TXT)).arrange(RIGHT, buff=0.35)
        rest = VGroup(sbox("72 bit", None, GOLD, 2.0, 0.65, 18), T("kalan riski karşılar", 19, TXT)).arrange(RIGHT, buff=0.35)
        VGroup(scr, rest).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 2.3)
        self.play(Create(w), run_time=1.2)
        self.at(self.cue("sinyalde geçiş", 0.9))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in trans], lag_ratio=0.05), FadeIn(trl), run_time=0.8)
        self.at(self.cue("Ardışık özdeş", 4.2))
        self.play(Create(run), FadeIn(rl), run_time=0.6)
        self.at(self.cue("her iki hızda", 11))
        self.play(FadeIn(big, shift=UP * 0.1), self.set_src("G.989.2 Tablo 11-4, 11-5"), run_time=0.6)
        self.at(self.cue("Karıştırıcı uzun", 13.5))
        self.play(FadeIn(scr, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yetmiş iki bitlik bağışıklık", 18.7))
        self.play(FadeIn(rest, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d2a")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("72 bit kaç nanosaniye?", h)
        k = 0.19
        r1 = VGroup(T("10G", 22, GOOD, BOLD), Rectangle(width=7.2 * k, height=0.55, stroke_width=0, fill_color=GOOD, fill_opacity=0.8), T("≈ 7 ns", 26, GOOD, BOLD)).arrange(RIGHT, buff=0.3)
        r2 = VGroup(T("2,5G", 22, TW_DS, BOLD), Rectangle(width=28.9 * k, height=0.55, stroke_width=0, fill_color=TW_DS, fill_opacity=0.8), T("≈ 29 ns  (4 kat)", 26, TW_DS, BOLD)).arrange(RIGHT, buff=0.3)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-0.8, 1.05, 0])
        r1[1].align_to(r2[1], LEFT)
        r1[2].next_to(r1[1], RIGHT, buff=0.3)
        o = np.array([-6.1, -2.95, 0])
        pax = VGroup(Line(o, o + [5.6, 0, 0], color=MUTED, stroke_width=2), Line(o + [0, -0.05, 0], o + [0, 1.75, 0], color=MUTED, stroke_width=2),
                     T("zaman", 14, MUTED).next_to(o + [5.6, 0, 0], DOWN, buff=0.08), T("faz hatası", 14, MUTED).next_to(o + [0, 1.75, 0], RIGHT, buff=0.1))
        lim = DashedLine(o + [0, 1.35, 0], o + [5.5, 1.35, 0], color=WARN, stroke_width=2)
        rng = np.random.default_rng(5)
        pts = [o + [x, 0.25 + 0.06 * rng.standard_normal(), 0] for x in np.linspace(0.1, 1.9, 12)]
        pts += [o + [x, 0.25 + 0.42 * (x - 1.9), 0] for x in np.linspace(2.0, 3.9, 8)]
        pts += [o + [x, 0.25 + 0.06 * rng.standard_normal() + 0.8 * np.exp(-(x - 3.9) * 4), 0] for x in np.linspace(4.0, 5.5, 10)]
        ph = VMobject(stroke_color=GOLD, stroke_width=2.5).set_points_smoothly(pts)
        runb = Rectangle(width=2.0, height=1.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.1).move_to(o + [2.9, 0.85, 0])
        rbl = T("geçiş yok", 14, GOLD, BOLD).move_to(o + [2.9, 1.6, 0])
        card_ = card("Döngü bant genişliği", "hızla orantılı:\n2,5G'de daha yavaş döngü →\nfaz daha uzun süre korunur", None, ACC, w=5.6, h=1.9, tsize=22, bsize=18).move_to([3.7, -2.0, 0])
        self.at(self.cue("on gigabitte yaklaşık", 0.9))
        self.play(FadeIn(r1[0]), GrowFromEdge(r1[1], LEFT), FadeIn(r1[2]), run_time=0.7)
        self.at(self.cue("Saat çıkarıcı bu süre", 4.2))
        self.play(Create(pax), Create(lim), FadeIn(runb), FadeIn(rbl), run_time=0.6)
        self.play(Create(ph), run_time=1.6)
        self.at(self.cue("İki buçuk gigabitte", 9.6))
        self.play(FadeIn(r2[0]), GrowFromEdge(r2[1], LEFT), run_time=0.7)
        self.at(self.cue("yaklaşık yirmi dokuz", 14.1))
        self.play(FadeIn(r2[2]), run_time=0.5)
        self.at(self.cue("ama döngü bant", 16.7))
        self.play(FadeIn(card_, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep05_p3A")


class E5P3B(Act5):
    HDR, MANIFEST, PREV_BADGE = H5[3], M5("p3"), "fiz"

    def construct(self):
        self.beat("d3")
        self.set_badge("std")
        h = self.show_heading("Titreşim toleransı — tanım (§11.1.5.4.2)")
        qt = self.quote("G.989.2 §11.1.5.4.2",
                        "“…the peak-to-peak amplitude of sinusoidal jitter applied on the input TWDM PON signal\nthat causes a 1-dB optical power penalty at the optical receiver.”",
                        "girişe uygulanan sinüzoidal titreşimin tepeden tepeye genliği → alıcıda 1 dB güç cezası", width=12.4).move_to(UP * 1.4)
        o = np.array([-5.8, -3.0, 0])
        ax = VGroup(Line(o, o + [6.0, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 2.5, 0], color=MUTED, stroke_width=2),
                    T("alınan güç (dBm)", 14, MUTED).next_to(o + [3.0, 0, 0], DOWN, buff=0.08), T("−log BER", 14, MUTED).next_to(o + [0, 2.5, 0], RIGHT, buff=0.1))
        yr = o[1] + 1.2
        ref = DashedLine(o + [0, 1.2, 0], o + [6.0, 1.2, 0], color=ACC, stroke_width=2)
        reft = T("BER ref", 14, ACC, BOLD).next_to(ref, RIGHT, buff=0.08)
        c1 = Line(o + [0.6, 0.2, 0], o + [3.6, 2.4, 0], color=GOOD, stroke_width=3.5)
        c2 = Line(o + [1.6, 0.2, 0], o + [4.6, 2.4, 0], color=GOLD, stroke_width=3.5)
        x1 = o[0] + 0.6 + (1.2 - 0.2) / 2.2 * 3.0
        da = DoubleArrow([x1, yr - 0.35, 0], [x1 + 1.0, yr - 0.35, 0], buff=0, color=WARN, stroke_width=2.5, tip_length=0.1)
        dat = T("1 dB", 17, WARN, BOLD).next_to(da, DOWN, buff=0.06)
        lg = VGroup(T("titreşimsiz", 15, GOOD, BOLD), T("+ sinüzoidal titreşim", 15, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(o + [1.5, 2.25, 0])
        cd = card("Ölçüt: 1 dB güç cezası", "BER'de bir çöküş değil\nstres testi → çalışmada ek ceza olmasın", None, WARN, w=5.8, h=1.8, tsize=23, bsize=19).move_to([3.6, -1.85, 0])
        self.play(FadeIn(qt[0]), FadeIn(qt[1]), self.set_src("G.989.2 §11.1.5.4"), run_time=0.7)
        self.at(self.cue("giriş sinyaline", 1.4))
        self.play(FadeIn(qt[2], shift=UP * 0.1), run_time=0.5)
        self.play(Create(ax), Create(ref), FadeIn(reft), Create(c1), FadeIn(lg[0]), run_time=0.9)
        self.at(self.cue("Dikkat edin", 12.1))
        self.play(Create(c2), FadeIn(lg[1]), run_time=0.7)
        self.at(self.cue("bir desibellik güç", 15.8))
        self.play(GrowFromCenter(da), FadeIn(dat), run_time=0.5)
        self.at(self.cue("Standart bunu bir stres", 17.8))
        self.play(FadeIn(cd, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d3a")
        self.clear(h)
        h = self.show_heading("Titreşim toleransı maskesi — Şekil 11-9", h)
        xa0, xa1, ya = -5.9, 1.3, -2.3
        lax, LX = log_axis(1e4, 1e8, xa0, xa1, ya, [(1e4, "10 kHz"), (1e5, "100 kHz"), (1e6, "1 MHz"), (1e7, "10 MHz"), (1e8, "100 MHz")], size=14)
        UY = lambda u: ya + (math.log10(u) + 1.45) * 1.75
        yax = Line([xa0, ya, 0], [xa0, UY(2.0), 0], color=MUTED, stroke_width=2)
        yl = T("UIpp (log)", 14, MUTED).next_to(yax, UP, buff=0.08)
        fl = T("sinüzoidal titreşim frekansı", 14, MUTED).next_to(lax, DOWN, buff=0.1).set_x((xa0 + xa1) / 2)
        hi = DashedLine([xa0, UY(0.75), 0], [xa1, UY(0.75), 0], color=MUTED, stroke_width=1.5)
        lo = DashedLine([xa0, UY(0.075), 0], [xa1, UY(0.075), 0], color=MUTED, stroke_width=1.5)
        hil = T("0,75", 16, TXT, BOLD).next_to([xa0, UY(0.75), 0], LEFT, buff=0.1)
        lol = T("0,075", 16, TXT, BOLD).next_to([xa0, UY(0.075), 0], LEFT, buff=0.1)

        def mask(f0, color):
            return VMobject(stroke_color=color, stroke_width=4).set_points_as_corners([[LX(1e4), UY(0.75), 0], [LX(f0), UY(0.75), 0], [LX(f0 * 10), UY(0.075), 0], [LX(1e8), UY(0.075), 0]])
        m25, m10 = mask(1e5, TW_DS), mask(4e5, GOOD)
        tb = table(["hız", "f0", "ft"], [["2,5G", "100 kHz", "1 MHz"], ["10G", "400 kHz", "4 MHz"]], [1.4, 1.7, 1.6], size=21, hsize=17, row_h=0.55).move_to([4.4, 1.3, 0])
        tb[1][1].set_color(TW_DS)
        tb[2][1].set_color(GOOD)
        lvl = VGroup(T("f < f0:  0,75 UIpp", 19, TXT, BOLD), T("f > ft:  0,075 UIpp", 19, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.4, -0.35, 0])
        sc = T("G.984.2'den 10G'ye ölçeklendi", 18, GOLD, BOLD).move_to([4.4, -1.5, 0])
        shp = T("ara eğim: temsili", 14, MUTED).move_to([4.4, -2.05, 0])
        self.play(Create(lax[0]), FadeIn(lax[1:]), Create(yax), FadeIn(yl), FadeIn(fl), self.set_src("G.989.2 Şekil 11-9"), run_time=0.7)
        self.at(self.cue("Düşük frekanslarda", 1.5))
        self.play(Create(hi), FadeIn(hil), FadeIn(lvl[0]), run_time=0.5)
        self.at(self.cue("yüksek frekanslarda", 4.7))
        self.play(Create(lo), FadeIn(lol), FadeIn(lvl[1]), run_time=0.5)
        self.at(self.cue("Köşe frekansları", 9.5))
        self.play(FadeIn(tb[0]), FadeIn(tb[1]), Create(m25), run_time=0.9)
        self.at(self.cue("on gigabitte dört", 14.7))
        self.play(FadeIn(tb[2]), Create(m10), run_time=0.9)
        self.at(self.cue("Değerler G.984.2", 18.5))
        self.play(FadeIn(sc), FadeIn(shp), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d4")
        self.clear(h)
        h = self.show_heading("Titreşim üretimi — Tablo 11-10 (G.783)", h)
        rows = [["10G", "20 kHz – 80 MHz", "0,3"], ["10G", "4 MHz – 80 MHz", "0,1"], ["2,5G", "5 kHz – 20 MHz", "0,3"], ["2,5G", "1 MHz – 20 MHz", "0,1"]]
        tb = table(["hız", "ölçüm bandı", "en çok (UIpp)"], rows, [1.6, 4.0, 2.6], size=22, hsize=17, row_h=0.52).move_to([0, 1.05, 0])
        lax, LX = log_axis(1e3, 1e8, -5.4, 5.4, -2.75, [(1e3, "1 kHz"), (1e4, "10 kHz"), (1e5, "100 kHz"), (1e6, "1 MHz"), (1e7, "10 MHz"), (1e8, "100 MHz")], size=14)
        specs = [(2e4, 8e7, GOOD, "0,3"), (4e6, 8e7, GOOD, "0,1"), (5e3, 2e7, TW_DS, "0,3"), (1e6, 2e7, TW_DS, "0,1")]
        bars = VGroup()
        for i, (a, b, c, v) in enumerate(specs):
            r = Rectangle(width=LX(b) - LX(a), height=0.28, stroke_width=0, fill_color=c, fill_opacity=0.75 if v == "0,3" else 0.45).move_to([(LX(a) + LX(b)) / 2, -0.85 - i * 0.42, 0])
            bars.add(VGroup(r, T(v + " UIpp", 14, BG, BOLD).move_to(r)))
        self.play(FadeIn(tb[0]), Create(lax[0]), FadeIn(lax[1:]), self.set_src("G.989.2 Tablo 11-10 · G.783"), run_time=0.6)
        for i, (key, d) in enumerate((("On gigabitte yirmi", 3), ("dört megahertz ile", 9.2), ("beş kilohertz", 17.4), ("ve bir megahertz", 20))):
            self.at(self.cue(key, d))
            self.play(FadeIn(tb[i + 1], shift=UP * 0.05), GrowFromEdge(bars[i][0], LEFT), FadeIn(bars[i][1]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d4a")
        self.clear(h)
        h = self.show_heading("Titreşim aktarımı — yalnız ONU", h)
        y = 1.35
        jin = VMobject(stroke_color=TW_DS, stroke_width=2.5).set_points_smoothly([[x, y + 0.25 * np.sin(6 * x), 0] for x in np.linspace(-6.4, -4.2, 30)])
        jl = T("↓ titreşim", 17, TW_DS, BOLD).next_to(jin, DOWN, buff=0.12)
        box_ = sbox("ONU", "CDR → verici", SIG, 2.6, 1.0, 20, 15).move_to([-2.3, y, 0])
        jout = VMobject(stroke_color=TW_US, stroke_width=2.5).set_points_smoothly([[x, y + 0.25 * np.sin(6 * x), 0] for x in np.linspace(-0.4, 1.8, 30)])
        jo = T("↑ titreşim", 17, TW_US, BOLD).next_to(jout, DOWN, buff=0.12)
        a1, a2 = arrow([-4.1, y, 0], box_.get_left(), MUTED), arrow(box_.get_right(), [-0.5, y, 0], MUTED)
        gk = T("tepe kazancı ≤ 0,1 dB", 24, WARN, BOLD).move_to([4.4, y, 0])
        o = np.array([-5.8, -3.0, 0])
        ax = VGroup(Line(o, o + [7.0, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 2.6, 0], color=MUTED, stroke_width=2),
                    T("frekans (log)", 14, MUTED).next_to(o + [3.5, 0, 0], DOWN, buff=0.08), T("kazanç (dB)", 14, MUTED).next_to(o + [0, 2.6, 0], RIGHT, buff=0.1))
        y0 = o[1] + 2.0
        pts = []
        for x in np.linspace(0.1, 6.9, 70):
            g = 0.18 * np.exp(-((x - 3.0) / 0.6) ** 2) - (0 if x < 3.2 else 0.55 * (x - 3.2) ** 1.3)
            pts.append(o + [x, 2.0 + g, 0])
        tf = VMobject(stroke_color=ACC, stroke_width=3).set_points_smoothly(pts)
        zero = DashedLine(o + [0, 2.0, 0], o + [7.0, 2.0, 0], color=MUTED, stroke_width=1.5)
        msk = DashedLine(o + [0, 2.25, 0], o + [7.0, 2.25, 0], color=WARN, stroke_width=2.5)
        mskt = T("+0,1 dB", 15, WARN, BOLD).next_to(msk, RIGHT, buff=0.08)
        zt = T("0 dB", 14, MUTED).next_to(zero, LEFT, buff=0.08)
        ex = T("(ölçek abartılı)", 13, MUTED).move_to(o + [5.8, 2.6, 0])
        why = card("Neden?", "ONU ↑ yönde, ↓ sinyalden\nçıkardığı saati kullanır →\nbu saat titreşimi büyütmemeli", None, GOLD, w=4.8, h=2.0, tsize=22, bsize=18).move_to([4.6, -1.75, 0])
        self.play(Create(jin), FadeIn(jl), GrowArrow(a1), FadeIn(box_), run_time=0.8)
        self.at(self.cue("Aşağı yöndeki titreşimin", 3.8))
        self.play(GrowArrow(a2), Create(jout), FadeIn(jo), run_time=0.7)
        self.at(self.cue("tepe kazancı", 8.9))
        self.play(FadeIn(gk), Create(ax), Create(zero), FadeIn(zt), run_time=0.6)
        self.play(Create(tf), Create(msk), FadeIn(mskt), FadeIn(ex), self.set_src("G.989.2 §11.1.5.4.1 · G.783"), run_time=1.0)
        self.at(self.cue("Çünkü ONU", 13))
        self.play(FadeIn(why, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep05_p3B")


class E5P3C(Act5):
    HDR, MANIFEST, PREV_BADGE = H5[3], M5("p3"), "std"

    def construct(self):
        self.beat("d5")
        h = self.show_heading("Alıcının ayarı — adım ve süre")
        st = VGroup()
        for i in range(6):
            st.add(Line([-6.2 + i * 0.42, 0.95 + i * 0.18, 0], [-5.78 + i * 0.42, 0.95 + i * 0.18, 0], color=PINK, stroke_width=4))
            if i:
                st.add(Line([-6.2 + i * 0.42, 0.95 + (i - 1) * 0.18, 0], [-6.2 + i * 0.42, 0.95 + i * 0.18, 0], color=PINK, stroke_width=4))
        stt = VGroup(T("en büyük ayar adımı", 20, MUTED), T("≤ 5 GHz", 36, PINK, BOLD)).arrange(RIGHT, buff=0.3).next_to(st, RIGHT, buff=0.4)
        tax, TX = log_axis(1e-6, 10, -5.6, 5.6, -2.4, [(1e-6, "1 µs"), (1e-5, "10 µs"), (1e-4, "100 µs"), (1e-3, "1 ms"), (1e-2, "10 ms"), (1e-1, "100 ms"), (1, "1 s"), (10, "10 s")], size=14)
        tl = T("Tablo 9-2 — ayar süresi sınıfları", 19, TXT, BOLD).move_to([-2.5, 0.0, 0])
        cls = [(1e-6, 1e-5, "Sınıf 1:  < 10 µs", CH[1]), (1e-5, 25e-3, "Sınıf 2:  10 µs – 25 ms", CH[2]), (25e-3, 1, "Sınıf 3:  25 ms – 1 s", CH[3])]
        bars = VGroup()
        for i, (a, b, s, c) in enumerate(cls):
            r = Rectangle(width=TX(b) - TX(a), height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([(TX(a) + TX(b)) / 2, -0.6 - i * 0.55, 0])
            bars.add(VGroup(r, T(s, 17, c, BOLD).next_to(r, RIGHT, buff=0.15)))
        bars[0][0].set_fill(opacity=0.0).set_stroke(CH[1], 2)
        bars[0].add(Rectangle(width=TX(1e-5) - TX(1e-6), height=0.38, stroke_width=0, fill_color=CH[1], fill_opacity=0.8).move_to(bars[0][0]))
        nm = pill("alıcı için sınıf zorunlu değil (Tablo 11-4 / 11-5)", GOLD, 18).move_to([2.6, 0.0, 0])
        self.at(self.cue("alıcı en çok", 2.4))
        self.play(Create(st), FadeIn(stt), self.set_src("G.989.2 Tablo 11-4, 11-5 · Tablo 9-2"), run_time=0.8)
        self.at(self.cue("Ayar süresi sınıfları", 6.9))
        self.play(Create(tax[0]), FadeIn(tax[1:]), FadeIn(tl), run_time=0.6)
        for i, (key, d) in enumerate((("birinci sınıf", 10.2), ("ikinci sınıf", 13.2), ("üçüncü sınıf", 17.7))):
            self.at(self.cue(key, d))
            self.play(GrowFromEdge(bars[i][0], LEFT), FadeIn(bars[i][1:]), run_time=0.6)
        self.at(self.cue("Tablolar alıcı", 21.9))
        self.play(FadeOut(tl), FadeIn(nm, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d5a")
        self.clear(h)
        self.set_badge("tc")
        h = self.show_heading("Otonom alıcı kalibrasyonu — G.989.3 §17.2", h)
        steps = [("1  tara", "alıcı ayar aralığı"), ("2  senkron ol", "sinyal bulunca"), ("3  oku", "Channel_Profile"), ("4  kaydet", "iç ayar ↔ kanal")]
        bx = VGroup(*[sbox(a, b, c, 2.85, 1.05, 21, 16) for (a, b), c in zip(steps, (PINK, STATE, PROF_C, GOOD))]).arrange(RIGHT, buff=0.42).move_to(UP * 1.2)
        ars = VGroup(*[arrow(bx[i].get_right(), bx[i + 1].get_left(), MUTED, 2.5, 0.12) for i in range(3)])
        o = np.array([-6.0, -3.0, 0])
        ax = VGroup(Line(o, o + [5.6, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 2.2, 0], color=MUTED, stroke_width=2),
                    T("ayar parametresi", 14, MUTED).next_to(o + [2.8, 0, 0], DOWN, buff=0.08), T("sinyal kalitesi", 14, MUTED).next_to(o + [0, 2.2, 0], RIGHT, buff=0.1))
        qf = lambda x: 1.9 * np.exp(-((x - 2.9) / 1.2) ** 2) + 0.1
        cv = VMobject(stroke_color=ACC, stroke_width=3).set_points_smoothly([o + [x, qf(x), 0] for x in np.linspace(0.2, 5.4, 50)])
        dot = Dot(o + [2.3, qf(2.3), 0], radius=0.1, color=GOLD)
        dl = T("küçük titreşim (dither)", 15, GOLD, BOLD).move_to(o + [2.9, 2.35, 0])
        cd = card("Çalışma sırasında ince ayar", "ayar parametresine küçük bir titreşim ekle\n→ sinyal kalitesini en iyi yapan noktayı izle", "öneri — G.989.3 §17.2.1", GOLD, w=6.6, h=1.9, tsize=22, bsize=18).move_to([3.1, -1.95, 0])
        self.play(self.set_src("G.989.3 §17.2"), run_time=0.3)
        for i, (key, d) in enumerate((("alıcı ayar aralığını", 5.3), ("sinyal bulduğu", 7.3), ("kanal profilinden", 10.1), ("ve bunları kendi", 13.6))):
            self.at(self.cue(key, d))
            anims = [FadeIn(bx[i], shift=RIGHT * 0.1)]
            if i:
                anims.append(GrowArrow(ars[i - 1]))
            self.play(*anims, run_time=0.5)
        self.at(self.cue("Çalışma sırasında", 18))
        self.play(Create(ax), Create(cv), FadeIn(cd, shift=UP * 0.1), run_time=0.9)
        self.at(self.cue("ayar parametresine", 20.5))
        self.play(FadeIn(dot), FadeIn(dl), run_time=0.4)
        for x in (3.3, 2.5, 3.1, 2.75, 3.0, 2.85, 2.95):
            self.play(dot.animate.move_to(o + [x, qf(x), 0]), run_time=0.45)
        self.end(pad=0.05)

        self.beat("d5c")
        self.clear(h)
        h = self.show_heading("TC katmanı ayar süresi — G.989.3 Ek F.2", h)
        y = 0.45
        segs = [("hazırlık", 2.4, MUTED), ("PMD ayar süresi", 4.2, PINK), ("yeniden senkron", 3.4, ACC)]
        sg = VGroup()
        for name, w, c in segs:
            r = Rectangle(width=w, height=0.75, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.35)
            sg.add(VGroup(r, T(name, 19, TXT, BOLD).move_to(r)))
        sg.arrange(RIGHT, buff=0).move_to([0, y, 0])
        pm = T("G.989.2 §9.3.7 · Tablo 9-2", 15, PINK).next_to(sg[1], UP, buff=0.12)
        st0 = VGroup(arrow([sg.get_left()[0], y + 1.35, 0], [sg.get_left()[0], y + 0.45, 0], GOLD, 2.5, 0.12), T("Scheduled SFC", 16, GOLD, BOLD).move_to([sg.get_left()[0], y + 1.6, 0]))
        st1 = VGroup(arrow([sg.get_right()[0], y + 1.35, 0], [sg.get_right()[0], y + 0.45, 0], GOOD, 2.5, 0.12), T("↓ çerçeve senkronu yeniden kuruldu", 16, GOOD, BOLD).move_to([sg.get_right()[0] - 1.5, y + 1.6, 0]))
        br = Brace(sg, DOWN, color=GOLD)
        brt = T("TC katmanı ayar süresi", 22, GOLD, BOLD).next_to(br, DOWN, buff=0.1)
        msg = pill("lazer / filtre ne kadar hızlı olursa olsun: bitiş = yeni kanalda senkron", GOOD, 19).move_to(DOWN * 2.35)
        self.at(self.cue("G.989.3'ün F eki", 4))
        self.play(self.set_src("G.989.3 Ek F.2"), run_time=0.3)
        for i, (key, d) in enumerate((("hazırlık süresi", 9.7), ("fiziksel katmandaki", 10.9), ("ve yeniden senkron", 13.3))):
            self.at(self.cue(key, d))
            anims = [GrowFromEdge(sg[i], LEFT)]
            if i == 1:
                anims.append(FadeIn(pm))
            self.play(*anims, run_time=0.5)
        self.play(FadeIn(br), FadeIn(brt), run_time=0.5)
        self.at(self.cue("Yani alıcının", 15.3))
        self.play(GrowArrow(st0[0]), FadeIn(st0[1]), run_time=0.5)
        self.at(self.cue("ONU ancak", 20.2))
        self.play(GrowArrow(st1[0]), FadeIn(st1[1]), FadeIn(msg, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d5b")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Geçirme, ret ve ayar adımı birlikte", h)
        ya = -2.0
        axg, X = lin_axis(-130, 130, -5.8, 5.8, ya, list(range(-120, 121, 20)), labels=[-100, -80, -20, 0, 20, 80, 100], size=14, fmt=gh5, unit="frekans farkı (GHz)")

        def H(f, sh=0.0):
            a = abs(f - sh)
            if a <= 22:
                return 1.0
            if a >= 78:
                return 0.02
            return 0.02 + 0.98 * np.cos((a - 22) / 56 * np.pi / 2) ** 2
        fs = np.linspace(-130, 130, 140)
        flt = VMobject(stroke_color=ACC, stroke_width=3.5).set_points_smoothly([[X(f), ya + 2.7 * H(f), 0] for f in fs])
        fsh = DashedVMobject(VMobject(stroke_color=GOLD, stroke_width=3).set_points_smoothly([[X(f), ya + 2.7 * H(f, 5), 0] for f in fs]), num_dashes=70)
        pb = Rectangle(width=X(20) - X(-20), height=2.7, stroke_width=0, fill_color=SIG, fill_opacity=0.18).move_to([X(0), ya + 1.35, 0])
        pbt = T("düz geçir: ± 20 GHz", 18, SIG, BOLD).move_to([X(0), ya + 3.0, 0])
        rj = VGroup(*[Line([X(s * 80), ya, 0], [X(s * 80), ya + 1.2, 0], color=WARN, stroke_width=3) for s in (-1, 1)])
        rjt = VGroup(*[T("ret", 17, WARN, BOLD).next_to(r, UP, buff=0.08) for r in rj])
        tz = VGroup(*[Rectangle(width=X(78) - X(22), height=2.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.08).move_to([X(s * 50), ya + 1.35, 0]) for s in (-1, 1)])
        tzt = T("geçiş bölgesi", 16, GOLD, BOLD).move_to([X(-50), ya + 3.0, 0])
        sh = VGroup(arrow([X(0), ya + 3.45, 0], [X(5) + 0.15, ya + 3.45, 0], GOLD, 2.5, 0.1))
        sht = T("5 GHz adım → konumlama hatası", 18, GOLD, BOLD).move_to([X(70), ya + 3.45, 0])
        msg = pill("kenar ne kadar dikse, aynı küçük hata o kadar pahalı", WARN, 19).move_to([X(0) + 2.4, ya + 1.35, 0])
        self.play(Create(axg[0]), FadeIn(axg[1:]), run_time=0.5)
        self.at(self.cue("Alıcı filtresi", 2.2))
        self.play(Create(flt), FadeIn(pb), FadeIn(pbt), run_time=1.0)
        self.at(self.cue("seksen gigahertzde", 7.9))
        self.play(Create(rj), FadeIn(rjt), run_time=0.5)
        self.at(self.cue("Beş gigahertzlik", 10.7))
        self.play(Create(fsh), GrowArrow(sh[0]), FadeIn(sht), run_time=0.9)
        self.at(self.cue("bu geçiş bandının", 12.8))
        self.play(FadeIn(tz), FadeIn(tzt), run_time=0.5)
        self.at(self.cue("filtre kenarı", 17.5))
        self.play(FadeIn(msg, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.note5("d6", [("1", "Titreşimde ölçütü karıştırmayın", "1 dB güç cezası — hata oranı eşiği değil.", "Bir:"),
                          ("2", "Vericinin saati alıcıdan gelir", "Alıcıdaki bir saat sorunu yukarı yönde de iz bırakır.", "İki:")])
        self.bridge_beat("d7", "Alıcı bit akışını yakaladı.\nŞimdi çerçeveyi bulması gerekiyor.")
        self.save_timeline("ep05_p3C")


PROF_C = "#A78BFA"


def gh5(v):
    return "C" if v == 0 else ("+" if v > 0 else "−") + str(abs(int(v)))


# ================================ PERDE 4 ======================================
class SyncMachine:
    """Reference DS sync state machine (G.989.3 Fig. 10-4) laid out on one row."""

    def __init__(self, y=0.75):
        names = [("Av", "Hunt"), ("Ön senkron", "Pre-Sync"), ("Senkron", "Sync"), ("Yeniden senkron", "Re-Sync")]
        xs = [-5.05, -1.7, 1.65, 5.0]
        self.y = y
        self.b = [sbox(a, b, STATE, 2.5, 0.85, 19, 14).move_to([x, y, 0]) for (a, b), x in zip(names, xs)]
        H, P, S, R = self.b
        u, d = UP * 0.17, DOWN * 0.17
        lab = lambda s, c, p: T(s, 15, c, BOLD).move_to(p)
        self.hp = VGroup(arrow(H.get_right() + u, P.get_left() + u, GOOD, 2.5, 0.12), lab("PSync 64/64 + SFC ✓", GOOD, [-3.38, y + 0.72, 0]))
        self.ph = VGroup(arrow(P.get_left() + d, H.get_right() + d, WARN, 2.5, 0.12), lab("biri ✗", WARN, [-3.38, y - 0.62, 0]))
        self.ps = VGroup(arrow(P.get_right() + u, S.get_left() + u, GOOD, 2.5, 0.12), lab("ikisi ✓", GOOD, [-0.03, y + 0.72, 0]))
        loop = CurvedArrow(S.get_top() + LEFT * 0.5, S.get_top() + RIGHT * 0.5, angle=-PI * 1.1, color=GOOD, stroke_width=2.5, tip_length=0.12)
        self.ss = VGroup(loop, lab("ikisi ✓", GOOD, [S.get_x(), y + 1.3, 0]))
        self.sr = VGroup(arrow(S.get_right() + u, R.get_left() + u, WARN, 2.5, 0.12), lab("biri ✗", WARN, [3.33, y + 0.72, 0]))
        self.rs = VGroup(arrow(R.get_left() + d, S.get_right() + d, GOOD, 2.5, 0.12), lab("ikisi ✓", GOOD, [3.33, y - 0.62, 0]))
        arc = CurvedArrow(R.get_bottom() + LEFT * 0.3, H.get_bottom() + RIGHT * 0.3, angle=-0.42, color=WARN, stroke_width=3, tip_length=0.15)
        self.rh = VGroup(arc, lab("M − 1 ardışık ✗  →  LODS", WARN, [0, y - 1.25, 0]))


class E5P4A(Act5):
    HDR, MANIFEST, FIRST = H5[4], M5("p4"), True

    def construct(self):
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Senkron, FEC ve ilk adımlar")
        self.at(self.cue("Her yüz yirmi beş", 1.3))
        self.to_header(tc)
        self.set_badge("tc")
        h = self.show_heading("PSBd — fiziksel senkron bloğu")
        fy = 1.35
        psb = Rectangle(width=0.55, height=0.6, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([-5.725, fy, 0])
        pay = Rectangle(width=11.45, height=0.6, stroke_color=TW_DS, stroke_width=1.5, fill_color=TW_DS, fill_opacity=0.18).next_to(psb, RIGHT, buff=0)
        payt = T("yük: FEC kod sözcükleri", 18, TW_DS).move_to(pay)
        ft = T("125 µs aşağı yön çerçevesi", 18, MUTED, BOLD).next_to(VGroup(psb, pay), UP, buff=0.12)
        blocks = [("PSync", "8 B", STATE), ("SFC yapısı", "8 B · sayaç + HEC", ACC), ("OC yapısı", "8 B · işletim kontrol", GOLD)]
        bg = VGroup()
        for n, s, c in blocks:
            r = Rectangle(width=3.7, height=0.85, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.22)
            bg.add(VGroup(r, VGroup(T(n, 21, TXT, BOLD), T(s, 15, c, BOLD)).arrange(DOWN, buff=0.05).move_to(r)))
        bg.arrange(RIGHT, buff=0).move_to([0, -0.5, 0])
        zl = VGroup(DashedLine(psb.get_corner(DL), bg.get_corner(UL), color=GOLD, stroke_width=1.5), DashedLine(psb.get_corner(DR), bg.get_corner(UR), color=GOLD, stroke_width=1.5))
        br = Brace(bg, DOWN, color=GOLD)
        brt = T("PSBd = 24 bayt", 19, GOLD, BOLD).next_to(br, DOWN, buff=0.08)
        pv = T("PSync = 0xC5E51840 FD59BB49 · sabit 64 bit", 21, STATE, BOLD).move_to(DOWN * 2.55)
        self.play(FadeIn(psb), FadeIn(pay), FadeIn(payt), FadeIn(ft), self.set_src("G.989.3 §10.1.1"), run_time=0.7)
        self.at(self.cue("yirmi dört baytlık", 5.3))
        self.play(Indicate(psb, color=GOLD, scale_factor=1.3), Create(zl), run_time=0.8)
        for i, (key, d) in enumerate((("sekiz baytlık PSync", 9.3), ("sekiz baytlık süper", 10.9), ("ve sekiz baytlık işletim", 13.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(bg[i], shift=UP * 0.1), *([FadeIn(br), FadeIn(brt)] if i == 2 else []), run_time=0.5)
        self.at(self.cue("PSync sabit", 16.6))
        self.play(FadeIn(pv, shift=UP * 0.1), Indicate(bg[0], color=STATE, scale_factor=1.03), run_time=0.7)
        self.end(pad=0.05)

        self.beat("e2")
        self.clear(h)
        h = self.show_heading("Referans senkron durum makinesi — Şekil 10-4", h)
        sm = SyncMachine()
        self.sm = sm
        for i, (key, d) in enumerate((("av,", 4.1), ("ön senkron", 4.3), ("senkron ve yeniden", 5.2))):
            self.at(self.cue(key, d))
            if i < 2:
                self.play(FadeIn(sm.b[i], scale=0.9), run_time=0.35)
            else:
                self.play(FadeIn(sm.b[2], scale=0.9), FadeIn(sm.b[3], scale=0.9), run_time=0.4)
        t1 = VGroup(T("Av:", 21, STATE, BOLD), T("bütün bit ve bayt hizalamalarında PSync — hatasız eşleşme (64 / 64)", 20, TXT)).arrange(RIGHT, buff=0.2)
        t2 = VGroup(T("sonra:", 21, STATE, BOLD), T("sonraki 64 bit geçerli, HEC korumalı bir SFC mi?", 20, TXT)).arrange(RIGHT, buff=0.2)
        low = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.9, 0])
        self.at(self.cue("Av durumunda", 7.2))
        self.play(Indicate(sm.b[0], color=STATE), FadeIn(t1, shift=UP * 0.1), self.set_src("G.989.3 §10.1.1.3"), run_time=0.7)
        self.at(self.cue("Bulduğunda", 14))
        self.play(GrowArrow(sm.hp[0]), FadeIn(sm.hp[1]), FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e2a")
        self.play(FadeOut(low), run_time=0.4)
        self.play(GrowArrow(sm.ps[0]), FadeIn(sm.ps[1]), GrowArrow(sm.ph[0]), FadeIn(sm.ph[1]), run_time=0.6)
        hd = T("kilitlendikten sonra: her çerçevede iki doğrulama", 21, ACC, BOLD)
        v1 = VGroup(T("PSync:", 20, STATE, BOLD), T("64 bitten ≥ 62 eşleşme → 2 bit hata tolere edilir", 20, TXT)).arrange(RIGHT, buff=0.2)
        v2 = VGroup(T("SFC:", 20, ACC, BOLD), T("geçerli HEC  +  yerel kopya + 1'e eşit", 20, TXT)).arrange(RIGHT, buff=0.2)
        low = VGroup(hd, v1, v2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-0.6, -1.65, 0])
        pa = pill("av: 64 / 64 → yanlış kilitlenmeye karşı sıkı", WARN, 17)
        pb = pill("kilitli: 62 / 64 → yanlış kayba karşı gevşek", GOOD, 17)
        pp = VGroup(pa, pb).arrange(RIGHT, buff=0.3).move_to(DOWN * 2.95)
        self.play(FadeIn(hd), run_time=0.4)
        self.at(self.cue("PSync için", 4.1))
        self.play(FadeIn(v1, shift=UP * 0.1), Create(sm.ss[0]), FadeIn(sm.ss[1]), run_time=0.6)
        self.at(self.cue("yani iki bit", 9.7))
        self.play(GrowArrow(sm.sr[0]), FadeIn(sm.sr[1]), GrowArrow(sm.rs[0]), FadeIn(sm.rs[1]), run_time=0.6)
        self.at(self.cue("Süper çerçeve sayacı", 12.2))
        self.play(FadeIn(v2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Avda tam", 20.7))
        self.play(FadeIn(pa, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yanlış kayba", 26.5))
        self.play(FadeIn(pb, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e2b")
        self.set_badge("fiz")
        self.play(FadeOut(low), FadeOut(pp), run_time=0.4)
        l1 = T("rastgele bit akışında, her konumda:  P(64 bit tam eşleşme) = 2⁻⁶⁴", 21, TXT)
        l2 = T("10G: saniyede ≈ 10¹⁰ konum denenir", 21, TXT)
        l3 = T("→ rastgele eşleşme: ortalama ≈ 59 yılda bir", 26, GOLD, BOLD)
        lines = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-0.3, -1.6, 0])
        p4 = pill("+ geçerli HEC + sonraki çerçevede yeniden doğrulama", GOOD, 18).move_to(DOWN * 3.0)
        self.play(Indicate(sm.b[0], color=GOLD), run_time=0.7)
        self.at(self.cue("her konumda", 10.8))
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("On gigabitte saniyede", 14))
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yani rastgele", 18.2))
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Üstelik", 22.8))
        self.play(FadeIn(p4, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e3")
        self.set_badge("tc")
        self.play(FadeOut(lines), FadeOut(p4), run_time=0.4)
        fx = [-5.4, -3.6, -1.8, 0.0]
        marks = [("✓", GOOD, "Senkron"), ("✗", WARN, "→ Yeniden senkron"), ("✗", WARN, "Yeniden senkron"), ("✗", WARN, "→ Av · LODS")]
        fr = VGroup()
        for x, (m, c, s) in zip(fx, marks):
            r = Rectangle(width=1.65, height=0.55, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([x, -1.55, 0])
            fr.add(VGroup(r, T(m, 24, c, BOLD).move_to(r), T(s, 14, c, BOLD).next_to(r, DOWN, buff=0.1)))
        ftl = T("125 µs çerçeveler", 15, MUTED).next_to(fr, UP, buff=0.12).align_to(fr, LEFT)
        bb = BraceBetweenPoints([fx[2] - 0.8, -2.25, 0], [fx[3] + 0.8, -2.25, 0], DOWN, color=WARN)
        bbt = T("M − 1 ardışık ✗", 16, WARN, BOLD).next_to(bb, DOWN, buff=0.06)
        m3 = T("M = 3 (önerilen)", 28, GOLD, BOLD).move_to([4.3, -1.3, 0])
        ber = VGroup(T("yanlış senkron kaybı yok:", 18, TXT), T("BER ≤ 10⁻³'e kadar", 22, GOOD, BOLD), T("= 10G referans BER rejimi", 18, MUTED)).arrange(DOWN, buff=0.08).move_to([4.3, -2.45, 0])
        self.play(Indicate(sm.sr[0], color=WARN), FadeIn(ftl), FadeIn(fr[0]), run_time=0.6)
        self.play(FadeIn(fr[1], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("Orada M eksi bir", 6.4))
        self.play(FadeIn(fr[2], shift=RIGHT * 0.1), run_time=0.4)
        self.play(FadeIn(fr[3], shift=RIGHT * 0.1), FadeIn(bb), FadeIn(bbt), run_time=0.5)
        self.at(self.cue("yani LODS", 12.8))
        self.play(Create(sm.rh[0]), FadeIn(sm.rh[1]), run_time=0.8)
        self.at(self.cue("Önerilen M", 15.5))
        self.play(FadeIn(m3, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("on üzeri eksi üçe", 19))
        self.play(FadeIn(ber, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep05_p4A")


class E5P4B(Act5):
    HDR, MANIFEST, PREV_BADGE = H5[4], M5("p4"), "tc"

    def construct(self):
        self.beat("e3a")
        h = self.show_heading("LODS — ONU'nun algıladığı tek kusur")
        top = pill("G.989.3 Tablo 14-3: ONU'da algılanan tek kusur", WARN, 19).move_to(UP * 1.95)
        o5 = sbox("O5", "çalışma", GOOD, 2.6, 0.95, 21, 16).move_to([-4.9, 0.2, 0])
        o6 = sbox("O6", "aralıklı LODS", WARN, 2.8, 0.95, 21, 16).move_to([-0.7, 0.2, 0])
        o1 = sbox("O1", "baştan aktivasyon", STATE, 2.8, 0.95, 21, 16).move_to([4.6, 1.0, 0])
        o8 = sbox("O8", "↓ kanal ayarı", PINK, 2.8, 0.95, 21, 16).move_to([4.6, -1.3, 0])
        a56 = VGroup(arrow(o5.get_right() + UP * 0.15, o6.get_left() + UP * 0.15, WARN, 3), T("LODS", 17, WARN, BOLD).move_to([-2.8, 0.65, 0]))
        tm = VGroup(T("zamanlayıcı:", 17, MUTED), T("koruma (WLCP) varsa TO3", 17, PINK, BOLD), T("yoksa TO2", 17, STATE, BOLD)).arrange(DOWN, buff=0.06).next_to(o6, DOWN, buff=0.2)
        a65 = VGroup(CurvedArrow(o6.get_left() + DOWN * 0.3, o5.get_right() + DOWN * 0.3, angle=-0.9, color=GOOD, stroke_width=2.5, tip_length=0.13),
                     T("senkron zamanında geri ✓", 16, GOOD, BOLD).move_to([-2.85, -0.8, 0]))
        a61 = VGroup(arrow(o6.get_right() + UP * 0.2, o1.get_left(), STATE, 2.5, 0.13), T("TO2 doldu", 16, STATE, BOLD).move_to([1.85, 1.0, 0]))
        a68 = VGroup(arrow(o6.get_right() + DOWN * 0.2, o8.get_left(), PINK, 2.5, 0.13), T("TO3 doldu", 16, PINK, BOLD).move_to([1.85, -1.05, 0]))
        a65[1].shift(DOWN * 0.45)
        self.at(self.cue("ONU'nun kendisinin", 0.2))
        self.play(FadeIn(top, shift=DOWN * 0.1), self.set_src("G.989.3 Tablo 14-3, Tablo 12-1 / 12-4"), run_time=0.5)
        self.at(self.cue("Çalışma durumunda", 3.5))
        self.play(FadeIn(o5), run_time=0.4)
        self.play(GrowArrow(a56[0]), FadeIn(a56[1]), FadeIn(o6), run_time=0.6)
        self.at(self.cue("dalga boyu kanalı", 10.4))
        self.play(FadeIn(tm[0]), FadeIn(tm[1]), run_time=0.5)
        self.at(self.cue("yoksa TO2", 13.2))
        self.play(FadeIn(tm[2]), run_time=0.3)
        self.at(self.cue("Senkron zamanında", 14))
        self.play(Create(a65[0]), FadeIn(a65[1]), run_time=0.6)
        self.at(self.cue("Gelmezse ya baştan", 17.6))
        self.play(GrowArrow(a61[0]), FadeIn(a61[1]), FadeIn(o1), run_time=0.6)
        self.at(self.cue("ya da korumalı", 19.9))
        self.play(GrowArrow(a68[0]), FadeIn(a68[1]), FadeIn(o8), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e3b")
        self.clear(h)
        h = self.show_heading("Diğer durumlarda LODS", h)
        tb = table(["durum", "LODS olursa"], [["O2-3 · seri numarası", "zamanlayıcı (TOZ) durur → O1 başlangıç"], ["O4 · ranging", "zamanlayıcı durur → O1 başlangıç"],
                                              ["O7 · acil durdurma", "senkron makinesi çalışır → başka bir ↓ kanal ara"]], [4.0, 7.8], size=21, hsize=17, row_h=0.62).move_to(UP * 0.9)
        nt = T("arama: varsa önceden yapılandırılmış koruma kanalından başlar", 20, PINK, BOLD).move_to(DOWN * 1.05)
        pe = pill("O7 yeniden başlatma ve güç kesintisinden sonra da sürer", WARN, 20).move_to(DOWN * 2.1)
        self.play(FadeIn(tb[0]), run_time=0.4)
        self.at(self.cue("Seri numarası ya da", 2.5))
        self.play(FadeIn(tb[1], shift=UP * 0.05), FadeIn(tb[2], shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("Acil durdurma durumunda", 10.7))
        self.play(FadeIn(tb[3], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("varsa önceden", 16.9))
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Acil durdurma,", 23.8))
        self.play(FadeIn(pe, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e4")
        self.clear(h)
        h = self.show_heading("Çerçeve alıcı tarafında", h)

        def frame(y, label, c):
            p = Rectangle(width=0.8, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([-5.8, y, 0])
            r = Rectangle(width=11.6, height=0.5, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.25).next_to(p, RIGHT, buff=0)
            return VGroup(p, r, T("PSBd", 13, BG, BOLD).move_to(p), T(label, 18, TXT, BOLD).move_to(r))
        f10 = frame(1.65, "10G: 627 × 248 B kod sözcüğü", GOOD)
        f25 = frame(0.95, "2,5G: 157 kod sözcüğü (sonuncusu kısa)", TW_DS)
        y = -0.65
        tx = VGroup(sbox("FEC kodla", None, MUTED, 1.9, 0.65, 17), sbox("karıştır", None, MUTED, 1.7, 0.65, 17)).arrange(RIGHT, buff=0.35).move_to([-4.5, y, 0])
        rx = VGroup(sbox("karıştırmayı çöz", None, ACC, 2.6, 0.75, 19), sbox("FEC çöz", None, GOOD, 1.9, 0.75, 19)).arrange(RIGHT, buff=0.4).move_to([3.2, y, 0])
        txl = T("verici (Bölüm 4)", 15, MUTED).next_to(tx, UP, buff=0.1)
        rxl = T("alıcı", 17, ACC, BOLD).next_to(rx, UP, buff=0.1)
        fib = arrow(tx.get_right() + RIGHT * 0.1, rx.get_left() + LEFT * 0.1, FEED, 3)
        ta = arrow(tx[0].get_right(), tx[1].get_left(), MUTED, 2, 0.1)
        ra = arrow(rx[0].get_right(), rx[1].get_left(), GOOD, 2.5, 0.12)
        ps = pill("PSBd: FEC ile korunmaz — kendi HEC'i korur", GOLD, 20).move_to(DOWN * 2.15)
        self.at(self.cue("on gigabitte altı", 3.8))
        self.play(FadeIn(f10, shift=UP * 0.1), self.set_src("G.989.3 §10.1.3"), run_time=0.6)
        self.at(self.cue("iki buçuk gigabitte", 6.3))
        self.play(FadeIn(f25, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Alıcı tarafında sıra", 9.8))
        self.play(FadeIn(tx), FadeIn(txl), GrowArrow(ta), GrowArrow(fib), run_time=0.7)
        self.at(self.cue("önce karıştırma", 12.5))
        self.play(FadeIn(rx[0], shift=RIGHT * 0.1), FadeIn(rxl), run_time=0.5)
        self.at(self.cue("sonra FEC", 14.4))
        self.play(GrowArrow(ra), FadeIn(rx[1], shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("PSBd ise", 15.8))
        self.play(FadeIn(ps, shift=UP * 0.1), Indicate(VGroup(f10[0], f25[0]), color=GOLD), run_time=0.7)
        self.end(pad=0.05)

        self.beat("e4a")
        self.clear(h)
        h = self.show_heading("Aşağı yön FEC: açık mı, kapalı mı?", h)
        top = pill("statik: kanaldaki bütün ONU'lar için açık ya da kapalı", GOLD, 19).move_to(UP * 1.95)
        frs = VGroup(*[VGroup(Rectangle(width=0.95, height=0.5, stroke_color=TW_DS, stroke_width=1.5, fill_color=TW_DS, fill_opacity=0.15),
                              T("1", 18, GOLD, BOLD)) for _ in range(5)]).arrange(RIGHT, buff=0.08).move_to([-3.6, 0.65, 0])
        for f in frs:
            f[1].move_to(f[0])
        frl = T("PSBd · OC · DS FEC bayrağı", 17, TW_DS, BOLD).next_to(frs, UP, buff=0.1)
        cp = sbox("Channel_Profile", "oktet 12 · E biti", PROF_C, 3.4, 0.95, 19, 16).move_to([-3.6, -0.85, 0])
        dec = sbox("karşılaştır", "yeterli sayıda özdeş bayrak", ACC, 3.3, 0.95, 19, 15).move_to([1.4, -0.1, 0])
        res = VGroup(T("FEC durumu", 18, MUTED), T("kanalda kaldıkça korunur", 20, GOOD, BOLD)).arrange(DOWN, buff=0.06).move_to([5.0, -0.1, 0])
        a1 = arrow(frs.get_right() + RIGHT * 0.1, dec.get_left() + UP * 0.2, MUTED, 2.5, 0.13)
        a2 = arrow(cp.get_right() + RIGHT * 0.1, dec.get_left() + DOWN * 0.2, MUTED, 2.5, 0.13)
        a3 = arrow(dec.get_right(), res.get_left() + LEFT * 0.1, GOOD, 2.5, 0.13)
        ho = pill("başka FEC durumlu kanala geçiş: senkronun kurulduğu andan itibaren doğru FEC", PINK, 18).move_to(DOWN * 2.3)
        self.play(FadeIn(top, shift=DOWN * 0.1), self.set_src("G.989.3 §10.1.3.1.2"), run_time=0.5)
        self.at(self.cue("PSBd'deki FEC", 7.1))
        self.play(LaggedStart(*[FadeIn(f) for f in frs], lag_ratio=0.15), FadeIn(frl), run_time=0.8)
        self.at(self.cue("kanal profilindeki", 9.5))
        self.play(FadeIn(cp, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Yeterli sayıda", 11.6))
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(dec), run_time=0.7)
        self.at(self.cue("ve kanalda kaldığı", 16.6))
        self.play(GrowArrow(a3), FadeIn(res), run_time=0.6)
        self.at(self.cue("Farklı FEC durumlu", 19.8))
        self.play(FadeIn(ho, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e4b")
        self.clear(h)
        h = self.show_heading("Alıcının yan görevi: hata oranını izlemek", h)

        def row(y, tag, c, body):
            p = pill(tag, c, 19).move_to([-5.3, y, 0])
            b = sbox(body, None, c, 5.6, 0.85, 18).move_to([-0.2, y, 0])
            a = arrow(p.get_right(), b.get_left(), MUTED, 2.5, 0.12)
            e = T("↓ BER tahmini", 20, TXT, BOLD).move_to([4.6, y, 0])
            a2 = arrow(b.get_right(), e.get_left() + LEFT * 0.1, MUTED, 2.5, 0.12)
            return VGroup(p, a, b, a2, e)
        r1 = row(1.1, "FEC açık", GOOD, "düzeltilen bayt · kod sözcüğü sayaçları")
        r2 = row(-0.4, "FEC kapalı", WARN, "çerçeve sonundaki BIP-32 hata sayısı")
        om = pill("sayaçlar → OMCI → OLT", ACC, 20).move_to([4.6, -2.0, 0])
        oa = VGroup(arrow(r1[4].get_bottom() + DOWN * 0.05, r2[4].get_top() + UP * 0.05, MUTED, 2, 0.1), arrow(r2[4].get_bottom() + DOWN * 0.05, om.get_top(), ACC, 2.5, 0.12))
        self.at(self.cue("FEC açıkken", 3.9))
        self.play(FadeIn(r1, shift=RIGHT * 0.1), self.set_src("G.989.3 §10.1.3.1.2 · Tablo 14-1"), run_time=0.7)
        self.at(self.cue("FEC kapalıyken", 11.7))
        self.play(FadeIn(r2, shift=RIGHT * 0.1), run_time=0.7)
        self.at(self.cue("Bu sayaçlar", 16.4))
        self.play(GrowArrow(oa[1]), FadeIn(om, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e4c")
        self.clear(h)
        h = self.show_heading("LODS sayaçları — Tablo 14-1", h)
        names = ["toplam LODS olayı", "çalışma kanalında geri gelen", "önceden yapılandırılmış koruma kanalında geri gelen",
                 "keyfi bir kanalda geri gelen", "senkron gelmeden yeniden aktivasyon"]
        rows = VGroup()
        for i, n in enumerate(names):
            ctr = VGroup(RoundedRectangle(corner_radius=0.08, width=0.8, height=0.42, stroke_color=WARN if i in (0, 4) else ACC, stroke_width=2, fill_color="#050810", fill_opacity=1),
                         T("#", 16, WARN if i in (0, 4) else ACC, BOLD))
            ctr[1].move_to(ctr[0])
            rows.add(VGroup(ctr, T(n, 21, TXT)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-2.4, -0.3, 0])
        qs = VGroup(pill("fiber?", FEED, 22), pill("OLT kanalı?", TW_DS, 22), pill("ONU?", SIG, 22)).arrange(DOWN, buff=0.35).move_to([4.8, -0.3, 0])
        keys = [("toplam LODS", 1.9), ("çalışma kanalında", 3.55), ("önceden yapılandırılmış", 6.0), ("keyfi bir kanalda", 10.2), ("ve senkron geri", 12.7)]
        self.play(self.set_src("G.989.3 Tablo 14-1"), run_time=0.3)
        for r, (key, d) in zip(rows, keys):
            self.at(self.cue(key, d))
            self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.45)
        for p, (key, d) in zip(qs, (("fiberde mi", 17.7), ("OLT kanalında", 20.0), ("yoksa ONU'nun", 21.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(p, shift=LEFT * 0.1), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep05_p4B")


class E5P4C(Act5):
    HDR, MANIFEST, PREV_BADGE = H5[4], M5("p4"), "tc"

    def construct(self):
        self.beat("e5")
        h = self.show_heading("Bir ONU'nun ilk adımları — G.989.3 §12.1")
        y = 0.75
        o11 = sbox("O1.1", "senkron dışı", STATE, 2.6, 1.0, 22, 16).move_to([-4.5, y, 0])
        o12 = sbox("O1.2", "profil öğrenme", STATE, 2.6, 1.0, 22, 16).move_to([-0.5, y, 0])
        o23 = sbox("O2-3", "seri numarası", GOOD, 2.6, 1.0, 22, 16).move_to([4.6, y, 0])
        grp = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=7.2, height=1.6, color=MUTED, stroke_width=2), num_dashes=60).move_to([-2.5, y, 0])
        grpt = T("O1 · başlangıç", 17, MUTED, BOLD).next_to(grp, UP, buff=0.08).align_to(grp, RIGHT).shift(LEFT * 0.2)
        pw = pill("güç açılır", MUTED, 17).next_to(grp, UP, buff=0.08).align_to(grp, LEFT).shift(RIGHT * 0.2)
        txo = pill("verici: KAPALI", WARN, 17).move_to([-4.5, -0.55, 0])
        a1 = VGroup(arrow(o11.get_right(), o12.get_left(), STATE, 2.5, 0.12), T("DSYNC", 15, STATE, BOLD).move_to([-2.5, y + 0.3, 0]))
        tpd = pill("TProfileDwell ≥ 10 s", GOLD, 17).move_to([1.0, -0.55, 0])
        self.at(self.cue("Açılışta verici", 1.9))
        self.play(FadeIn(pw), FadeIn(txo, shift=UP * 0.1), self.set_src("G.989.3 §12.1, Tablo 12-1"), run_time=0.5)
        self.at(self.cue("ONU başlangıç", 3.9))
        self.play(Create(grp), FadeIn(grpt), run_time=0.6)
        self.at(self.cue("senkron dışı", 5.7))
        self.play(FadeIn(o11, scale=0.9), run_time=0.5)
        self.at(self.cue("Senkron olunca", 9.8))
        self.play(GrowArrow(a1[0]), FadeIn(a1[1]), FadeIn(o12, scale=0.9), run_time=0.6)
        self.at(self.cue("ve en az on", 13.6))
        self.play(FadeIn(tpd, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e5a")
        prof = VGroup(pill("System_Profile", GOLD, 17), pill("Channel_Profile", PROF_C, 17), pill("Burst_Profile", TW_DS, 17)).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.55)
        prl = T("toplanır:", 17, MUTED).next_to(prof, LEFT, buff=0.2)
        ok = VGroup(arrow(o12.get_right(), o23.get_left(), GOOD, 3), T("OK to activate", 17, GOOD, BOLD).move_to([2.05, y + 0.32, 0]))
        cond = card("OK to activate — hepsi uyuyorsa", "kanal bölümü · ↑ bağlantı tipi · ↑ hız  +  uygun tipte SN grantı", None, GOOD, w=10.6, h=1.05, tsize=19, bsize=18).move_to(DOWN * 2.65)
        blk = VGroup(CurvedArrow(o12.get_bottom() + LEFT * 0.6, o11.get_bottom() + RIGHT * 0.6, angle=-0.9, color=WARN, stroke_width=2.5, tip_length=0.13),
                     T("Activation blocked: burst profillerini at → başka ↓ kanal", 15, WARN, BOLD).move_to([-2.0, -0.62, 0]))
        amd = pill("Amd.2 (2025) ile netleşti", ACC, 16).move_to([4.6, 1.95, 0])
        self.play(FadeIn(prl), LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in prof], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("kanal bölümü", 5.2))
        self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("aktivasyona devam", 13.1))
        self.play(GrowArrow(ok[0]), FadeIn(ok[1]), FadeIn(o23, scale=0.9), run_time=0.6)
        self.at(self.cue("Uymuyorsa", 14.8))
        self.play(FadeOut(txo), FadeOut(tpd), run_time=0.3)
        self.play(Create(blk[0]), FadeIn(blk[1]), run_time=0.7)
        self.at(self.cue("Bu ayrım", 20.8))
        self.play(FadeIn(amd, shift=DOWN * 0.1), self.set_src("G.989.3 Tablo 12-1 (Amd.2)"), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e5b")
        self.play(FadeOut(prof), FadeOut(prl), FadeOut(cond), run_time=0.4)
        pt = T("profiller 1–5 s'de bir tekrarlanır (T_minProfile)", 19, PROF_C, BOLD).move_to([0, -1.3, 0])
        segs = VGroup()
        x = -5.6
        for i in range(4):
            t = Rectangle(width=0.4, height=0.5, stroke_width=0, fill_color=PINK, fill_opacity=0.85).move_to([x + 0.2, -1.95, 0])
            p = Rectangle(width=1.85, height=0.5, stroke_color=PROF_C, stroke_width=1.5, fill_color=PROF_C, fill_opacity=0.3).next_to(t, RIGHT, buff=0)
            segs.add(VGroup(t, p, T(f"kanal {i + 1}", 14, TXT, BOLD).move_to(p)))
            x += 2.25
        fst = VGroup(Line([x + 0.15, -2.3, 0], [x + 0.15, -1.6, 0], color=GOOD, stroke_width=4), T("ilk SN yanıtı", 16, GOOD, BOLD).move_to([x + 1.2, -1.95, 0]))
        tl = T("ayar: alıcı sınıfına bağlı", 14, PINK, BOLD).next_to(segs[0][0], UP, buff=0.08).align_to(segs[0][0], LEFT)
        br = BraceBetweenPoints([-5.6, -2.3, 0], [x, -2.3, 0], DOWN, color=GOLD)
        brt = T("sessiz süre: saniyeler … onlarca saniye", 18, GOLD, BOLD).next_to(br, DOWN, buff=0.06)
        self.play(FadeIn(pt), run_time=0.4)
        self.at(self.cue("Hiçbir şey bilmeyen", 3.4))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in segs], lag_ratio=0.25), run_time=1.4)
        self.at(self.cue("alıcı ayar sınıfına", 7.9))
        self.play(FadeIn(tl), *[Indicate(s[0], color=PINK) for s in segs], run_time=0.7)
        self.at(self.cue("hatta onlarca", 11.2))
        self.play(FadeIn(br), FadeIn(brt), run_time=0.5)
        self.at(self.cue("İlk yanıttan", 13.8))
        self.play(FadeIn(fst), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e5d")
        self.play(*[FadeOut(m) for m in (pt, segs, fst, tl, br, brt)], run_time=0.4)
        txn = pill("verici: AÇIK", GOOD, 17).move_to([4.6, -0.55, 0])
        sn = VGroup(T("Serial_Number_ONU — ilk yanıt", 20, GOOD, BOLD),
                    *[T("• " + s, 18, TXT) for s in ("seçilen ↓ ve ↑ PON-ID", "kalibrasyon kaydı durumu", "ayar adımı · tek adımlık ayar süresi", "rastgele gecikme")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.4, -2.05, 0])
        g1 = pill("kalibre → bant içi SN grantı", GOOD, 17)
        g2 = pill("yeterince kalibre değil → AMCC SN grantı", GOLD, 17)
        gs = VGroup(g1, g2).arrange(DOWN, buff=0.15).move_to([3.6, -1.75, 0])
        b67 = T("ayrıntı: Bölüm 6 ve 7", 17, ACC, BOLD).next_to(gs, DOWN, buff=0.2)
        self.at(self.cue("seri numarası durumunda", 1.1))
        self.play(FadeIn(txn, shift=UP * 0.1), Indicate(o23, color=GOOD, scale_factor=1.05), run_time=0.7)
        self.at(self.cue("seçtiği aşağı", 6.7))
        self.play(FadeIn(sn[0]), FadeIn(sn[1], shift=RIGHT * 0.1), run_time=0.5)
        for k, (key, d) in enumerate((("kalibrasyon kaydının", 10), ("ayar adımı", 12.2), ("rastgele gecikmesi", 15.1))):
            self.at(self.cue(key, d))
            self.play(FadeIn(sn[k + 2], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("Yeterince kalibre", 16.5))
        self.play(FadeIn(g1, shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("AMCC seri", 19.6))
        self.play(FadeIn(g2, shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("Bunların ayrıntısı", 22.9))
        self.play(FadeIn(b67), run_time=0.4)
        self.end(pad=0.05)

        self.beat("e5c")
        self.clear(h)
        h = self.show_heading("TOL ile kaba yol kaybı tahmini", h)
        y = 0.9
        tol = sbox("TOL (PSBd · OC)", "OLT başlatma gücü", GOLD, 3.6, 1.15, 20, 16).move_to([-4.55, y, 0])
        rxp = sbox("ONU'nun ölçtüğü", "alınan güç (± 3 dB, Ek II)", ACC, 3.6, 1.15, 20, 16).move_to([0, y, 0])
        opl = sbox("≈ yol kaybı", "kaba tahmin", GOOD, 3.0, 1.15, 22, 16).move_to([4.6, y, 0])
        ops = VGroup(T("−", 36, TXT, BOLD).move_to([-2.27, y, 0]), T("=", 36, TXT, BOLD).move_to([2.48, y, 0]))
        td = T("TOL: −30 dBm'den 0,1 dB adımlarla — her çerçevede (Bölüm 4)", 19, GOLD).move_to(DOWN * 0.55)
        nd = pill("standart bu kullanımı açıkça tanımlamaz — ama bilgi orada", MUTED, 19).move_to(DOWN * 1.5)
        oc = T("aynı yapıda ODN sınıf kodu:  N1 000 · N2 001 · E1 011 · E2 100", 19, TXT, BOLD).move_to(DOWN * 2.45)
        self.play(FadeIn(tol, shift=UP * 0.1), self.set_src("G.989.3 §10.1.1.1.3"), run_time=0.6)
        self.at(self.cue("kendi ölçtüğü", 4.75))
        self.play(FadeIn(ops[0]), FadeIn(rxp, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("OLT'nin her çerçevede", 6.7))
        self.play(FadeIn(td), run_time=0.5)
        self.at(self.cue("yol kaybını kabaca", 11.5))
        self.play(FadeIn(ops[1]), FadeIn(opl, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Standart bu kullanımı", 14.3))
        self.play(FadeIn(nd, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ODN sınıf kodu", 18.8))
        self.play(FadeIn(oc, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.note5("e6", [("1", "Görünmeyen ONU → önce LODS sayaçları", "LODS olayları sayılır; senkronun hangi kanalda geri geldiği kaydedilir.", "Bir:"),
                          ("2", "Aktivasyon hata ayıklama alanı", "Seri numarası mesajı: ONU neden yeniden başlangıca döndü?", "İki:")])
        self.bridge_beat("e7", "Şimdi bunları laboratuvarda ölçelim.", label="Sıradaki: Laboratuvar", pad=0.3)
        self.save_timeline("ep05_p4C")
