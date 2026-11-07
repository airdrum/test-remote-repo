"""B09 · Laboratuvarda (PtP WDM ve AMCC ölçümleri) and Kapanış."""
from ep09_common import *


def coil(center, r=0.36, color=FEED):
    return VGroup(*[Circle(radius=r - 0.07 * k, color=color, stroke_width=2) for k in range(3)]).move_to(center)


def burst_row(x0, x1, y, color, n=5, h=0.4):
    w = (x1 - x0) / (n * 1.6)
    return VGroup(*[Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.8).move_to([x0 + w / 2 + k * w * 1.6, y, 0]) for k in range(n)])


class E9LabA(Act9):
    HDR, MANIFEST, FIRST = H9["L"], M9("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "PtP WDM ve AMCC ölçümleri")
        self.at(self.cue("Üç düzenek", 1.0))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Üç düzenek")
        cs = VGroup(card("1 · Verici", "güç · ER · SMSR · PSD · λ", None, GOOD, w=4.0, h=1.2, tsize=23, bsize=17),
                    card("2 · Alıcı bütçesi", "hassasiyet · OPP · titreşim", None, ACC, w=4.0, h=1.2, tsize=23, bsize=17),
                    card("3 · AMCC", "indeks · AMCC cezası", None, AMC, w=4.0, h=1.2, tsize=23, bsize=17)).arrange(RIGHT, buff=0.3).move_to([0, 1.65, 0])
        y1, y2 = -0.05, -2.05
        olt = sbox("OLT CT", None, OLTC, 1.4, 0.6, 16).move_to([-5.7, y1, 0])
        wm = sbox("WM", None, PTP, 0.8, 0.9, 16).move_to([-4.05, y1, 0])
        pm1 = instr("PM", 2.15, 1.4, "+3,0 dBm").move_to([-0.85, y1 + 0.1, 0])
        l1 = VGroup(Line(olt.get_right(), wm.get_left(), color=PTP, stroke_width=3), Line(wm.get_right(), [pm1[0].get_left()[0], y1, 0], color=PTP, stroke_width=3))
        cg = VGroup(DashedLine([-2.8, y1 - 0.45, 0], [-2.8, y1 + 0.45, 0], color=GOLD, stroke_width=2), T("S/R-CG", 14, GOLD, BOLD).move_to([-2.8, y1 + 0.62, 0]))
        onu = sbox("ONU", None, PTP, 1.4, 0.6, 16).move_to([-5.7, y2, 0])
        pm2 = instr("PM", 2.15, 1.4, "+3,0 dBm").move_to([-0.85, y2 + 0.1, 0])
        l2 = Line(onu.get_right(), [pm2[0].get_left()[0], y2, 0], color=PTP, stroke_width=3)
        rs = VGroup(DashedLine([-3.6, y2 - 0.45, 0], [-3.6, y2 + 0.45, 0], color=GOLD, stroke_width=2), T("R/S", 14, GOLD, BOLD).move_to([-3.6, y2 + 0.62, 0]))
        wmn = T("çoğullayıcıdan sonra", 14, MUTED).next_to(wm, DOWN, buff=0.1).shift(RIGHT * 0.5)
        tt = T("TWDM ↑: burst → ölçümde düzeltme", 17, TW_US, BOLD).move_to([4.1, 0.55, 0])
        tb = burst_row(2.0, 6.2, -0.05, TW_US, 5)
        pt = T("PtP: sürekli → düzeltme yok", 17, PTP, BOLD).move_to([4.1, -1.25, 0])
        rng = np.random.default_rng(21)
        pw = VMobject(stroke_color=PTP, stroke_width=2.2).set_points_as_corners(nrz(list(rng.integers(0, 2, 26)), 2.0, 4.2 / 26, -2.1, -1.7, 0.03))
        ok = T("✓", 26, GOOD, BOLD).next_to(pt, RIGHT, buff=0.15)
        self.at(self.cue("PtP WDM verici", 2.8))
        self.play(FadeIn(cs[0], shift=UP * 0.15), run_time=0.5)
        self.at(self.cue("alıcı bütçesi ve AMCC", 5.1))
        self.play(LaggedStart(FadeIn(cs[1], shift=UP * 0.15), FadeIn(cs[2], shift=UP * 0.15), lag_ratio=0.4), run_time=0.8)
        self.at(self.cue("Önce verici", 7.0))
        self.play(cs[1:].animate.set_opacity(0.3), Indicate(cs[0], color=GOOD, scale_factor=1.04), run_time=0.6)
        self.at(self.cue("Ortalama başlatma", 8.0))
        self.play(FadeIn(olt), FadeIn(wm), Create(l1), run_time=0.6)
        self.at(self.cue("OLT için S/R-CG", 10.0))
        self.play(FadeIn(cg), FadeIn(pm1, shift=LEFT * 0.1), self.set_src("G.989.2 Tablo A.2–A.7 · §11.1.5.2.8 · §9.3.6.5"), run_time=0.6)
        self.at(self.cue("yani çoğullayıcıdan sonra", 12.3))
        self.play(FadeIn(wmn), Indicate(wm, color=GOLD), run_time=0.6)
        self.at(self.cue("ONU için R/S", 14.5))
        self.play(FadeIn(onu), Create(l2), FadeIn(rs), FadeIn(pm2, shift=LEFT * 0.1), run_time=0.7)
        self.at(self.cue("TWDM'den farklı", 17.2))
        self.play(FadeIn(tt), LaggedStart(*[GrowFromEdge(b, DOWN) for b in tb], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("PtP sinyali süreklidir", 21.4))
        self.play(FadeIn(pt), Create(pw), FadeIn(ok), run_time=0.8)
        self.end(pad=0.05)

        # g2 — extinction ratio
        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Sönüm oranı — §9.3.2", h)
        boxes, arrs = chain([("S/R-CG", "kanal çıkışı", PTP), ("referans BPF", "G.959.1 Ek B", GOLD), ("G.957 Şekil B.1", "ölçüm düzeneği", ACC)], 1.35, -6.3, 2.9, h=0.85, size=17, ssize=14)
        dca = instrument("DCA", 1.8, 1.25).move_to([4.85, 1.45, 0])
        a3 = arrow(boxes[2].get_right(), [dca[0].get_left()[0], 1.35, 0], MUTED, 2.5, 0.13)
        v1 = VGroup(T("ER ≥ 8,2 dB", 34, GOOD, BOLD), T("Tablo A.2–A.7 · C.3–C.6", 15, MUTED)).arrange(DOWN, buff=0.08).move_to([-3.2, -0.3, 0])
        v2 = VGroup(T("Ek C sınıf 3: ER ≥ 6 dB", 26, GOLD, BOLD), T("Tablo C.7 / C.8", 15, MUTED)).arrange(DOWN, buff=0.08).move_to([2.7, -0.3, 0])
        q = card_lines("AMCC açık mı, kapalı mı?", [("standartta yazılmamış", WARN), ("öneri (yorum): AMCC açıkken ölç — en kötü durum", GOOD)], WARN, 7.6, 1.5, 21, 18).move_to([-2.45, -2.25, 0])
        e1 = eye(4.3, -2.2, 2.3, 1.15, GOOD, 0.0, sw=2.0, op=0.6)
        e2 = eye(4.3, -2.2, 2.3, 1.15 * 0.88, AMC, 0.0, sw=2.0, op=0.8)
        el = T("AMCC açık: zarf gözü daraltır", 14, AMC, BOLD).next_to(e1, UP, buff=0.1)
        self.at(self.cue("G.959.1", 1.4))
        self.play(FadeIn(boxes[0]), GrowArrow(arrs[0]), FadeIn(boxes[1]), self.set_src("G.989.2 §9.3.2 · Tablo A.2–A.7, C.3–C.8"), run_time=0.7)
        self.at(self.cue("sonra G.957", 6.0))
        self.play(GrowArrow(arrs[1]), FadeIn(boxes[2]), GrowArrow(a3), FadeIn(dca), run_time=0.7)
        self.at(self.cue("En az sekiz virgül iki", 9.0))
        self.play(FadeIn(v1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("C ekinin üçüncü", 11.7))
        self.play(FadeIn(v2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("AMCC açıkken mi", 14.3))
        self.play(FadeIn(q[0]), FadeIn(q[1][0]), FadeIn(q[1][1]), run_time=0.6)
        self.at(self.cue("biz en kötü durumu", 18.9))
        self.play(FadeIn(q[1][2], shift=UP * 0.05), LaggedStart(*[Create(c) for c in e1], lag_ratio=0.05), run_time=0.7)
        self.play(LaggedStart(*[Create(c) for c in e2], lag_ratio=0.05), FadeIn(el), run_time=0.7)
        self.end(pad=0.05)

        # g3 — SMSR and PSD
        self.beat("g3")
        self.clear(h)
        h = self.show_heading("SMSR ve PSD sınırları", h)
        ox, oy = -6.2, -1.5
        lax = VGroup(Line([ox, oy, 0], [-0.8, oy, 0], color=MUTED, stroke_width=2), Line([ox, oy, 0], [ox, 1.75, 0], color=MUTED, stroke_width=2),
                     T("dB", 14, MUTED).next_to([ox, 1.75, 0], RIGHT, buff=0.1), T("OSA", 16, MUTED, BOLD).move_to([-1.3, 1.6, 0]))
        X = lambda v: v
        main = lobe(X, -3.5, oy, 2.9, 0.09, PTP, op=0.35)
        sides = VGroup(lobe(X, -4.35, oy, 0.55, 0.09, PTP, op=0.35), lobe(X, -2.65, oy, 0.55, 0.09, PTP, op=0.35))
        sb = BraceBetweenPoints([-2.25, oy + 0.55, 0], [-2.25, oy + 2.9, 0], RIGHT, color=GOLD)
        sbt = T("SMSR ≥ 30 dB", 18, GOLD, BOLD).next_to(sb, RIGHT, buff=0.08)
        st = T("ONU: lazer çıkışında, filtrelemeden önce", 17, PTP, BOLD).move_to([-3.5, -2.05, 0])
        rx0, rx1, ry = 0.5, 6.4, -1.5
        rax = Line([rx0, ry, 0], [rx1, ry, 0], color=MUTED, stroke_width=2)
        c = 3.45
        tgt = lobe(X, c, ry, 2.6, 0.13, GOOD, op=0.3)
        nb = [c - 1.15, c + 1.15, c + 2.3, c - 2.3]
        mse = 0.3
        lo, hi = ry + 0.3, ry + 0.85
        segs = []
        for sgn_ in (-1, 1):
            pts = []
            xs_ = sorted([n for n in nb if (n - c) * sgn_ > 0], key=lambda v: abs(v - c))
            x = c + sgn_ * 0.55
            for n in xs_:
                a, b = n - sgn_ * mse, n + sgn_ * mse
                pts += [[x, hi, 0], [a, hi, 0], [a, lo, 0], [b, lo, 0], [b, hi, 0]]
                x = b
            pts.append([rx1 if sgn_ > 0 else rx0, hi, 0])
            segs.append(VMobject(stroke_color=GOLD, stroke_width=3).set_points_as_corners(pts))
        mask = VGroup(*segs)
        ml = VGroup(T("OOC2: ±MSE içinde", 15, GOLD, BOLD).move_to([c + 1.15, ry - 0.3, 0]), T("OOC1: aralarda", 15, GOLD, BOLD).move_to([c - 1.75, hi + 0.25, 0]))
        nbm = VGroup(*[DashedLine([n, ry, 0], [n, ry + 1.3, 0], color=MUTED, stroke_width=1.5) for n in nb])
        bin_ = Rectangle(width=0.14, height=0.9, stroke_color=ACC, stroke_width=2, fill_color=ACC, fill_opacity=0.3).move_to([c + 0.85, ry + 0.45, 0])
        bt = T("15 GHz ≈ 0,13 nm @1610 nm", 16, ACC, BOLD).move_to([c + 1.55, 1.7, 0])
        bl = Line(bt.get_bottom(), bin_.get_top(), color=ACC, stroke_width=1.5)
        mt = T("maske: verici MSE aralığının her yerinde (§9.3.9)", 16, GOOD, BOLD).move_to([3.45, -2.4, 0])
        self.play(Create(lax[:2]), FadeIn(lax[2:]), FadeIn(main), FadeIn(sides), self.set_src("G.989.2 §9.3.8 · §9.3.9 · Tablo A.2–A.7"), run_time=0.7)
        self.at(self.cue("ONU'da lazer", 2.0))
        self.play(FadeIn(st), run_time=0.4)
        self.at(self.cue("en az otuz", 6.2))
        self.play(FadeIn(sb), FadeIn(sbt), run_time=0.5)
        self.at(self.cue("Bant dışı ve kanal dışı", 7.8))
        self.play(Create(rax), FadeIn(tgt), FadeIn(nbm), run_time=0.6)
        self.at(self.cue("bin altı yüz on", 14.6))
        self.play(FadeIn(bin_), Create(bl), FadeIn(bt), run_time=0.6)
        self.at(self.cue("Kanal dışı maske", 20.6))
        self.play(Create(mask), FadeIn(ml), run_time=0.8)
        self.at(self.cue("verici spektral sapma", 22.0))
        self.play(tgt.animate.shift(RIGHT * mse), FadeIn(mt), run_time=0.8)
        self.play(tgt.animate.shift(LEFT * 2 * mse), run_time=0.8)
        self.end(pad=0.05)

        # g4 — wavelength
        self.beat("g4")
        self.clear(h)
        h = self.show_heading("Dalga boyu: sapma, adım, ayar", h)
        osa = instrument("OSA", 2.1, 1.5).move_to([-5.0, 1.15, 0])
        ot = T("dalga boyu ölçer ya da OSA", 16, TXT, BOLD).next_to(osa, DOWN, buff=0.08)
        kc = card_lines("CS = 50 GHz", [("sapma ≤ ±12,5 GHz", GOLD), ("ayar adımı 2,5 GHz (CS/20)", ACC)], PTP, 4.3, 1.45, 21, 18).move_to([-4.55, -1.25, 0])
        o = np.array([-1.3, -2.5, 0])
        Yf = lambda f: -1.85 + f * 0.05
        Xt = lambda t: o[0] + t * 0.98
        axs = VGroup(Line(o, o + [7.6, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 4.2, 0], color=MUTED, stroke_width=2),
                     T("zaman", 14, MUTED).next_to(o + [7.6, 0, 0], DOWN, buff=0.08).align_to(o + [7.6, 0, 0], RIGHT), T("frekans", 14, MUTED).next_to(o + [0, 4.2, 0], RIGHT, buff=0.1))
        grid = VGroup(*[DashedLine([o[0], Yf(f), 0], [o[0] + 7.6, Yf(f), 0], color=LINE, stroke_width=1.5) for f in (0, 50)])
        gl = VGroup(T("kanal n", 14, MUTED).next_to([o[0], Yf(0), 0], LEFT, buff=0.1), T("kanal n+1", 14, MUTED).next_to([o[0], Yf(50), 0], LEFT, buff=0.1))
        wins = VGroup(*[Rectangle(width=7.6, height=25 * 0.05, stroke_width=0, fill_color=GOLD, fill_opacity=0.15).move_to([o[0] + 3.8, Yf(f), 0]) for f in (0, 50)])
        wl = T("±12,5 GHz", 15, GOLD, BOLD).move_to([o[0] + 6.9, Yf(50) + 0.45, 0])
        rng = np.random.default_rng(5)
        def fz(t):
            if t < 3.2:
                return 2.5 * rng.standard_normal() * 0.4
            if t < 4.4:
                u = (t - 3.2) / 1.2
                return 50 * (1 - np.exp(-4 * u) * np.cos(5 * u))
            return 50 + 2.5 * rng.standard_normal() * 0.4
        tr_ = VMobject(stroke_color=PTP, stroke_width=2.5).set_points_as_corners([[Xt(t), Yf(fz(t)), 0] for t in np.linspace(0.05, 7.6, 120)])
        hl = Rectangle(width=Xt(4.6) - Xt(3.0), height=3.6, stroke_color=ACC, stroke_width=2, fill_opacity=0).move_to([(Xt(3.0) + Xt(4.6)) / 2, -0.45, 0])
        hlt = T("ayar sırasında: OOB/OOC'yi\nzaman çözümlü izle", 15, ACC, BOLD, line_spacing=0.85).next_to(hl, RIGHT, buff=0.12).set_y(-0.55)
        tp = pill("§9.3.7: tablolar ayar süresince de geçerli", GOOD, 17).move_to([2.5, -3.05, 0])
        self.at(self.cue("dalga boyu ölçerle", 0.8))
        self.play(FadeIn(osa, shift=UP * 0.1), FadeIn(ot), self.set_src("G.989.2 Tablo A.2–A.7 · §9.3.7"), run_time=0.6)
        self.at(self.cue("çoğullayıcının ızgarasına", 3.9))
        self.play(Create(axs[:2]), FadeIn(axs[2:]), Create(grid), FadeIn(gl), run_time=0.7)
        self.at(self.cue("Elli gigahertz aralıkta", 7.6))
        self.play(FadeIn(wins), FadeIn(wl), FadeIn(kc[0]), FadeIn(kc[1][0]), FadeIn(kc[1][1]), run_time=0.6)
        self.at(self.cue("ayar adımı iki virgül beş", 13.3))
        self.play(FadeIn(kc[1][2]), run_time=0.4)
        self.at(self.cue("Ayar sırasında", 16.6))
        self.play(Create(tr_), run_time=1.4)
        self.play(Create(hl), FadeIn(hlt), run_time=0.5)
        self.at(self.cue("tablolar ayar süresince", 22.1))
        self.play(FadeIn(tp, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep09_labA")


class E9LabB(Act9):
    HDR, MANIFEST, PREV_BADGE = H9["L"], M9("lab"), "lab"

    def construct(self):
        self.beat("g5")
        h = self.show_heading("Düzenek 2: alıcı bütçesi")
        y = 1.05
        b1 = sbox("BERT", "desen üreteci", ACC, 1.5, 0.8, 17, 14).move_to([-5.85, y, 0])
        tx = sbox("Tx", None, PTP, 0.85, 0.6, 16).move_to([-4.45, y, 0])
        wm = VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.1, width=1.35, height=0.7, color=MUTED, stroke_width=2), num_dashes=30), T("WM", 15, MUTED, BOLD))
        wm.move_to([-3.0, y, 0])
        wm[1].move_to(wm[0])
        wmt = T("gerekirse", 13 + 1, MUTED).next_to(wm, DOWN, buff=0.08)
        fb = coil([-1.45, y, 0])
        fbt = T("20 / 40 km", 15, FEED, BOLD).next_to(fb, DOWN, buff=0.1)
        voa = sbox("VOA", "ayarlı", GOLD, 1.25, 0.8, 17, 14).move_to([0.25, y, 0])
        rx = sbox("Rx", None, SIG, 0.85, 0.6, 16).move_to([1.85, y, 0])
        b2 = sbox("BERT", "hata sayacı", GOOD, 1.5, 0.8, 17, 14).move_to([3.5, y, 0])
        ln = VGroup(Line(b1.get_right(), tx.get_left(), color=FEED, stroke_width=2.5), Line(tx.get_right(), wm.get_left(), color=PTP, stroke_width=2.5),
                    Line(wm.get_right(), [fb.get_left()[0], y, 0], color=PTP, stroke_width=2.5), Line([fb.get_right()[0], y, 0], voa.get_left(), color=PTP, stroke_width=2.5),
                    Line(voa.get_right(), rx.get_left(), color=PTP, stroke_width=2.5), Line(rx.get_right(), b2.get_left(), color=FEED, stroke_width=2.5))
        refs = VGroup(pill("FEC'siz: 10⁻¹²", MUTED, 20), pill("FEC'li sınıf 1, 2: 10⁻⁴", GOLD, 20), pill("FEC'li sınıf 3: 10⁻³", GOLD, 20)).arrange(RIGHT, buff=0.35).move_to([0, -0.85, 0])
        rt = T("referans BER", 17, MUTED, BOLD).next_to(refs, UP, buff=0.15)
        cid = pill("CID 72 bit · karıştırılmış NRZ varsayılır", ACC, 19).move_to([0, -2.1, 0])
        self.at(self.cue("Hata oranı test", 2.3))
        self.play(FadeIn(b1), FadeIn(tx), FadeIn(rx), FadeIn(b2), Create(ln[0]), Create(ln[5]), self.set_src("G.989.2 Tablo A.2–A.7 · §A.1.5"), run_time=0.8)
        self.at(self.cue("ayarlı zayıflatıcı", 4.2))
        self.play(FadeIn(voa), Create(ln[4]), run_time=0.5)
        self.at(self.cue("gerekirse çoğullayıcı", 5.8))
        self.play(FadeIn(wm), FadeIn(wmt), Create(ln[1]), run_time=0.5)
        self.at(self.cue("ve yirmi ya da kırk", 7.7))
        self.play(Create(fb), FadeIn(fbt), Create(ln[2]), Create(ln[3]), run_time=0.6)
        self.at(self.cue("Referans hata oranı", 11.0))
        self.play(FadeIn(rt), FadeIn(refs[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("FEC'li birinci", 15.1))
        self.play(FadeIn(refs[1], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("üçüncü sınıfta on", 19.5))
        self.play(FadeIn(refs[2], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Yetmiş iki bitlik", 22.2))
        self.play(FadeIn(cid, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g6 — OPP and closing the budget
        self.beat("g6")
        self.clear(h)
        h = self.show_heading("Yol cezası ve bütçenin kapanışı", h)
        ax, X, Y = ber_axes((-5.6, -2.55, 0), 6.2, 4.5, 0, 10)
        l1, d1 = ber_curve(X, Y, 5.0, Q12, 0.55, 0.4, 5.7, GOOD, seed=2)
        l2, d2 = ber_curve(X, Y, 6.6, Q12, 0.55, 2.0, 7.3, GOLD, seed=3)
        t1 = T("arka arkaya", 16, GOOD, BOLD).next_to(l1.point_from_proportion(0.72), LEFT, buff=0.25)
        t2 = T("fiberli (DD20 / DD40)", 16, GOLD, BOLD).next_to(l2.point_from_proportion(0.45), RIGHT, buff=0.2)
        ref = DashedLine([X(0), Y(Q12), 0], [X(10), Y(Q12), 0], color=MUTED, stroke_width=1.5)
        gap = DoubleArrow([X(5.0), Y(Q12) + 0.25, 0], [X(6.6), Y(Q12) + 0.25, 0], buff=0, color=WARN, stroke_width=2.5, tip_length=0.12)
        gt = T("OPP", 18, WARN, BOLD).next_to(gap, UP, buff=0.05)
        RX = 3.9
        r1 = T("OPP = S_fiberli − S_arka arkaya", 21, GOLD, BOLD).move_to([RX, 1.75, 0])
        r2 = T("≤ 40 km · paylaşılan spektrum için", 18, TXT).move_to([RX, 1.05, 0])
        r3 = T("genişletilmiş: Raman cezası uygulamaya göre", 18, MUTED).move_to([RX, 0.55, 0])
        fit(r3, 5.3)
        f1 = T("P_min − S", 28, TXT, BOLD)
        f2 = T("≥ OPL_maks + OPP", 28, TXT, BOLD)
        fr = VGroup(f1, f2).arrange(RIGHT, buff=0.2).move_to([RX, -0.75, 0])
        fit(fr, 5.4)
        fs = T("§9.3.6.3 · pay yok: sıfırla kapanır", 15, MUTED).next_to(fr, DOWN, buff=0.12)
        self.play(Create(ax[:2]), FadeIn(ax[2:]), Create(ref), self.set_src("G.989.2 Tablo A.2–A.7 (Not 5/6) · §9.3.6.3"), run_time=0.6)
        self.play(Create(l1), FadeIn(d1), FadeIn(t1), run_time=0.6)
        self.at(self.cue("fiberli hassasiyet", 1.0))
        self.play(Create(l2), FadeIn(d2), FadeIn(t2), run_time=0.6)
        self.play(GrowFromCenter(gap), FadeIn(gt), FadeIn(r1), run_time=0.6)
        self.at(self.cue("Ceza değerleri kırk", 6.6))
        self.play(FadeIn(r2), run_time=0.4)
        self.at(self.cue("genişletilmiş spektrumda Raman", 13.0))
        self.play(FadeIn(r3), run_time=0.4)
        self.at(self.cue("en küçük güç eksi hassasiyet", 20.7))
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("en büyük yol kaybı", 23.2))
        self.play(FadeIn(f2, shift=UP * 0.1), FadeIn(fs), run_time=0.5)
        self.end(pad=0.05)

        # g7 — jitter tolerance
        self.beat("g7")
        self.clear(h)
        h = self.show_heading("Titreşim toleransı: PtP'de OLT testi doğrudan", h)
        r1l = T("TWDM ↑", 19, TW_US, BOLD).move_to([-5.7, 1.55, 0])
        r1b = burst_row(-4.7, 0.3, 1.55, TW_US, 6, 0.42)
        r1t = T("OLT toleransı: bilgilendirici", 18, WARN, BOLD).move_to([3.0, 1.75, 0])
        r1n = T("(sürekli ↑ gerektirir)", 16, MUTED).next_to(r1t, DOWN, buff=0.06)
        r2l = T("PtP ↑", 19, PTP, BOLD).move_to([-5.7, 0.45, 0])
        rng = np.random.default_rng(31)
        r2w = VMobject(stroke_color=PTP, stroke_width=2.2).set_points_as_corners(nrz(list(rng.integers(0, 2, 30)), -4.7, 5.0 / 30, 0.25, 0.65, 0.03))
        r2t = T("OLT testi doğrudan ✓", 20, GOOD, BOLD).move_to([3.0, 0.45, 0])
        lax, LX = log_axis(1e4, 1e8, -5.0, 1.6, -2.55, [(1e4, "10 kHz"), (1e5, "100 kHz"), (1e6, "1 MHz"), (1e7, "10 MHz"), (1e8, "100 MHz")], size=14)
        UY = lambda u: -2.45 + (math.log10(u) - math.log10(0.04)) / (math.log10(1.5) - math.log10(0.04)) * 1.9
        mk = VMobject(stroke_color=ACC, stroke_width=3.5).set_points_as_corners([[LX(1e4), UY(0.75), 0], [LX(4e5), UY(0.75), 0], [LX(4e6), UY(0.075), 0], [LX(1e8), UY(0.075), 0]])
        mt = VGroup(T("0,75 UIpp", 14, ACC, BOLD).next_to([LX(1e4), UY(0.75), 0], UP, buff=0.06, aligned_edge=LEFT),
                    T("0,075 UIpp", 14, ACC, BOLD).next_to([LX(1e8), UY(0.075), 0], UP, buff=0.06, aligned_edge=RIGHT),
                    T("f0 = 400 kHz", 14, MUTED).next_to([LX(4e5), UY(0.75), 0], UP, buff=0.06),
                    T("ft = 4000 kHz", 14, MUTED).next_to([LX(4e6), UY(0.075), 0], DOWN, buff=0.08))
        mtt = T("sınıf 3 tolerans maskesi (Şekil A.5)", 15, ACC, BOLD).move_to([-1.7, -0.2, 0])
        cr = card("Ölçüt", "1 dB güç cezasına yol açan\nsinüzoidal titreşim genliği", None, GOLD, w=4.2, h=1.5, tsize=21, bsize=17).move_to([4.4, -1.65, 0])
        self.at(self.cue("TWDM'de OLT'nin", 3.5))
        self.play(FadeIn(r1l), LaggedStart(*[GrowFromEdge(b, DOWN) for b in r1b], lag_ratio=0.1), FadeIn(r1t), self.set_src("G.989.2 §A.1.6.3 · §11.1.5.4"), run_time=0.8)
        self.at(self.cue("çünkü sürekli", 7.9))
        self.play(FadeIn(r1n), run_time=0.4)
        self.at(self.cue("PtP'de yukarı yön", 11.3))
        self.play(FadeIn(r2l), Create(r2w), run_time=0.8)
        self.at(self.cue("OLT testi doğrudan", 14.2))
        self.play(FadeIn(r2t, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("Ölçüt yine", 16.8))
        self.play(Create(lax[0]), FadeIn(lax[1:]), Create(mk), FadeIn(mt), FadeIn(mtt), run_time=0.9)
        self.play(FadeIn(cr, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep09_labB")


class E9LabC(Act9):
    HDR, MANIFEST, PREV_BADGE = H9["L"], M9("lab"), "lab"

    def construct(self):
        self.beat("g8")
        h = self.show_heading("Düzenek 3: AMCC indeksi (üst modülasyon)")
        boxes, arrs = chain([("Tx + AMCC", "üst modülasyon", PTP), ("kuplör", None, MUTED), ("dedektör", "DC kuplajlı\nBW ≪ yük hızı", AMC)], 1.5, -6.3, 2.2, h=1.0, size=17, ssize=14)
        osc = instrument("OSC", 1.8, 1.3).move_to([4.2, 1.7, 0])
        a3 = arrow(boxes[2].get_right(), [osc[0].get_left()[0], 1.6, 0], MUTED, 2.5, 0.13)
        bits = [1, 0, 1, 1, 0, 1]
        x0, x1, yb, hh, dep, er = -6.0, 0.4, -2.65, 2.2, 0.5, 0.15
        cur, et, eb, _ = overmod(x0, x1, yb, hh, bits, nbits=130, depth=dep, er=er, seed=15)
        cur.set_stroke(opacity=0.35)
        me = mean_env(x0, x1, yb, hh, bits, dep, er)
        pa = yb + hh * (1 + er) / 2
        ymax, ymin = pa * 0 + yb + hh * (1 + er) / 2 * (1 + dep / 2), yb + hh * (1 + er) / 2 * (1 - dep / 2)
        cur_l = []
        for yy, s, c, dy in ((ymax, "P_maks", GOLD, 0.16), (pa, "P_ort", TXT, 0.0), (ymin, "P_min", GOLD, -0.16)):
            cur_l.append(VGroup(DashedLine([x0, yy, 0], [x1 + 0.15, yy, 0], color=c, stroke_width=2), T(s, 16, c, BOLD).next_to([x1 + 0.15, yy + dy, 0], RIGHT, buff=0.08)))
        ex = T("görsel ölçek abartılı", 14, MUTED).move_to([(x0 + x1) / 2, -3.0, 0])
        fm = T("M = 100 · (P_maks − P_min) / P_ort", 22, TXT, BOLD).move_to([4.1, -0.35, 0])
        tg = T("hedef: %10", 26, AMC, BOLD).move_to([4.1, -1.15, 0])
        tp = pill("dikdörtgen darbeler · 115 kb/s", AMC, 18).move_to([4.1, -1.95, 0])
        self.at(self.cue("Taban bant üst", 1.5))
        self.play(FadeIn(boxes[0]), GrowArrow(arrs[0]), FadeIn(boxes[1]), self.set_src("G.989.2 Ek B · B.2.1 · Tablo B.1"), run_time=0.6)
        self.at(self.cue("yük hızının çok altında", 4.1))
        self.play(GrowArrow(arrs[1]), FadeIn(boxes[2]), run_time=0.5)
        self.at(self.cue("doğru akım kuplajlı", 8.1))
        self.play(GrowArrow(a3), FadeIn(osc), Create(cur), Create(me), FadeIn(ex), run_time=0.9)
        self.at(self.cue("en büyük,", 12.1))
        self.play(FadeIn(cur_l[0]), run_time=0.4)
        self.at(self.cue("en küçük ve ortalama", 12.9))
        self.play(FadeIn(cur_l[2]), FadeIn(cur_l[1]), run_time=0.5)
        self.at(self.cue("en büyük eksi en küçük bölü", 15.6))
        self.play(FadeIn(fm, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("hedef yüzde on", 19.9))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("dikdörtgen darbelerle", 21.1))
        self.play(FadeIn(tp, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # g9 — pilot tone at the electrical interface
        self.beat("g9")
        self.clear(h)
        h = self.show_heading("Pilot ton: elektriksel arayüzde ölçüm", h)
        lt = T("sürücü girişinde", 19, GOLD, BOLD).move_to([-3.9, 1.8, 0])
        rng = np.random.default_rng(41)
        pw = VMobject(stroke_color=PTP, stroke_width=2.2).set_points_as_corners(nrz(list(rng.integers(0, 2, 20)), -5.9, 3.8 / 20, -0.55, 1.05, 0.03))
        bp = BraceBetweenPoints([-1.95, -0.55, 0], [-1.95, 1.05, 0], RIGHT, color=PTP)
        bpt = T("Vpp,yük", 15, PTP, BOLD).next_to(bp, RIGHT, buff=0.06)
        aw = ask(-5.9, -2.1, -1.6, [0.08] * 3, 3.9, AMC, 2.2)
        awt = T("Vpp,AMCC", 15, AMC, BOLD).next_to(aw, RIGHT, buff=0.15)
        ft = T("M = 100 · Vpp,AMCC / Vpp,yük", 19, TXT, BOLD).move_to([-3.6, -2.4, 0])
        sx0, sx1, sy0, sy1 = 0.7, 6.2, -1.55, 1.35
        scr = Rectangle(width=sx1 - sx0, height=sy1 - sy0, stroke_color="#475569", stroke_width=2, fill_color="#050810", fill_opacity=1).move_to([(sx0 + sx1) / 2, (sy0 + sy1) / 2, 0])
        st = T("spektrum analizörü", 17, TXT, BOLD).next_to(scr, UP, buff=0.1)
        xs = np.linspace(sx0 + 0.1, sx1 - 0.1, 120)
        flo = VMobject(stroke_color=PTP, stroke_width=1.8).set_points_as_corners(
            [[x, sy0 + 0.35 + 0.9 * np.exp(-((x - sx0) / 3.2)) * 0 + 0.55 * (1 - (x - sx0) / (sx1 - sx0)) + 0.05 * rng.standard_normal(), 0] for x in xs])
        xp = sx0 + 1.6
        spike = Line([xp, sy0 + 0.6, 0], [xp, sy1 - 0.35, 0], color=AMC, stroke_width=4)
        spt = T("500 kHz", 16, AMC, BOLD).next_to(spike, RIGHT, buff=0.1).shift(UP * 0.7)
        fl = T("frekans", 13 + 1, MUTED).next_to(scr, DOWN, buff=0.08).align_to(scr, RIGHT)
        tg = pill("hedef: %10 · 128 kb/s", AMC, 19).move_to([3.45, -2.4, 0])
        self.at(self.cue("sürücü girişinde", 3.4))
        self.play(FadeIn(lt), Create(pw), FadeIn(bp), FadeIn(bpt), self.set_src("G.989.2 Ek B · B.2.2 · Tablo B.2"), run_time=0.8)
        self.play(Create(aw), FadeIn(awt), FadeIn(ft), run_time=0.6)
        self.at(self.cue("ya da bir spektrum", 9.2))
        self.play(FadeIn(scr), FadeIn(st), Create(flo), FadeIn(fl), run_time=0.7)
        self.play(GrowFromEdge(spike, DOWN), FadeIn(spt), run_time=0.5)
        self.at(self.cue("Hedef yine", 15.0))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g10 — the AMCC penalty (not defined)
        self.beat("g10")
        self.clear(h)
        h = self.show_heading("Standardın tanımlamadığı ölçüm: AMCC cezası", h)
        ax, X, Y = ber_axes((-5.6, -2.55, 0), 6.0, 4.5, 0, 10)
        l1, d1 = ber_curve(X, Y, 5.0, Q12, 0.55, 0.4, 5.7, GOOD, seed=4)
        l2, d2 = ber_curve(X, Y, 5.9, Q12, 0.55, 1.3, 6.6, AMC, seed=5)
        t1 = T("AMCC kapalı", 16, GOOD, BOLD).next_to(l1.point_from_proportion(0.72), LEFT, buff=0.25)
        t2 = T("AMCC açık", 16, AMC, BOLD).next_to(l2.point_from_proportion(0.45), RIGHT, buff=0.2)
        ref = DashedLine([X(0), Y(Q12), 0], [X(10), Y(Q12), 0], color=MUTED, stroke_width=1.5)
        reft = T("referans BER", 14, MUTED).next_to(ref, RIGHT, buff=0.08)
        gap = DoubleArrow([X(5.0), Y(Q12) + 0.25, 0], [X(5.9), Y(Q12) + 0.25, 0], buff=0, color=WARN, stroke_width=2.5, tip_length=0.12)
        gt = T("AMCC cezası", 17, WARN, BOLD).next_to(gap, UP, buff=0.05)
        yp = pill("yorum — tanım standartta yok", WARN, 18).move_to([3.9, 1.9, 0])
        pan = RoundedRectangle(corner_radius=0.14, width=4.6, height=2.0, stroke_color=GOOD, stroke_width=2.5, fill_color="#050810", fill_opacity=1).move_to([3.9, -0.6, 0])
        pt = T("AMCC bağlantısı", 18, TXT, BOLD).next_to(pan.get_top(), DOWN, buff=0.2)
        s1 = VGroup(T("AMCC senkronu", 18, TXT), T("✓", 22, GOOD, BOLD)).arrange(RIGHT, buff=0.4).move_to([3.9, -0.55, 0])
        s2 = VGroup(T("LOMC (Ind bit 2)", 18, TXT), T("0 ✓", 22, GOOD, BOLD)).arrange(RIGHT, buff=0.4).move_to([3.9, -1.15, 0])
        self.at(self.cue("AMCC cezası.", 2.7))
        self.play(Create(ax[:2]), FadeIn(ax[2:]), Create(ref), FadeIn(reft), FadeIn(yp, shift=DOWN * 0.1), self.set_src("G.989.2 Ek B · G.989.3 §8.2"), run_time=0.7)
        self.at(self.cue("Yükün hassasiyetini", 3.8))
        self.play(Create(l1), FadeIn(d1), FadeIn(t1), run_time=0.7)
        self.at(self.cue("kapalıyken ve açıkken", 7.4))
        self.play(Create(l2), FadeIn(d2), FadeIn(t2), run_time=0.7)
        self.at(self.cue("fark AMCC cezasıdır", 10.1))
        self.play(GrowFromCenter(gap), FadeIn(gt), run_time=0.5)
        self.at(self.cue("Aynı anda AMCC'nin", 11.8))
        self.play(FadeIn(pan), FadeIn(pt), run_time=0.5)
        self.at(self.cue("AMCC senkronu sağlanmalı", 16.2))
        self.play(FadeIn(s1, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("yönetim kanalı kaybı", 18.4))
        self.play(FadeIn(s2, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g11 — reflections
        self.beat("g11")
        self.clear(h)
        h = self.show_heading("Yansımalar", h)
        rows = [["ODN geri dönüş kaybı (ORL)", "≥ 32 dB"], ["ONU verici yansıtıcılığı", "≤ −6 dB"], ["alıcı yansıtıcılığı", "≤ −20 dB"],
                ["vericinin yansıyan güce toleransı", "−15 dB"], ["ODN ayrık yansımalar (§9.3.5.3)", "< −35 dB"]]
        tb = table(["parametre", "sınır"], rows, [5.4, 2.0], size=20, hsize=17, row_h=0.6).move_to([-2.9, 0.55, 0])
        for k in range(1, 6):
            tb[k][2].set_color(GOLD)
        o = np.array([1.8, -2.4, 0])
        oax = VGroup(Line(o, o + [4.6, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 3.9, 0], color=MUTED, stroke_width=2),
                     T("mesafe", 14, MUTED).next_to(o + [4.6, 0, 0], DOWN, buff=0.08).align_to(o + [4.6, 0, 0], RIGHT), T("OTDR", 16, TXT, BOLD).move_to(o + [2.3, 4.1, 0]))
        pts = [o + [0.1, 3.2, 0], o + [1.6, 2.55, 0], o + [1.62, 3.3, 0], o + [1.7, 2.5, 0], o + [3.6, 1.7, 0], o + [3.62, 2.6, 0], o + [3.7, 0.3, 0], o + [4.5, 0.25, 0]]
        trc = VMobject(stroke_color=ACC, stroke_width=2.5).set_points_as_corners(pts)
        thr = DashedLine(o + [0.1, 3.0 + 0.5, 0], o + [4.5, 3.5, 0], color=WARN, stroke_width=2)
        tht = T("ayrık yansıma < −35 dB", 15, WARN, BOLD).next_to(thr, UP, buff=0.06).align_to(thr, RIGHT)
        self.play(FadeIn(tb[0]), self.set_src("G.989.2 Tablo A.2–A.7 · §9.3.5.3"), run_time=0.4)
        for k, (key, d) in enumerate((("geri dönüş kaybı en az", 1.7), ("ONU vericisinin yansıtıcılığı", 5.0), ("alıcılarınki", 9.0), ("vericinin yansıyan güce", 12.2), ("ODN'deki ayrık", 16.7))):
            self.at(self.cue(key, d))
            anims = [FadeIn(tb[k + 1], shift=UP * 0.05)]
            if k == 4:
                anims += [Create(oax[:2]), FadeIn(oax[2:]), Create(trc), Create(thr), FadeIn(tht)]
            self.play(*anims, run_time=0.8 if k == 4 else 0.4)
        self.end(pad=0.05)

        self.note5("g12", [("1", "PtP bütçesinde pay yok", "Ölçtüğünüz her desibel ya verici gücünden\nya da tasarım payından gelir.", "Bir:"),
                           ("2", "AMCC indeksini %10 sanmayın — ölçün", "İndeks hem yükün cezasını hem AMCC'nin\nkendi hata oranını belirler.", "İki:")])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep09_labC")


class E9End(Act9):
    HDR, MANIFEST, FIRST = H9["E"], M9("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 9'un özeti")
        self.at(1.5)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["PtP WDM: her ONU'ya kendi sürekli λ çifti · paylaşılan 1603–1625 nm\nTWDM'den ≥ 3 nm ya da ≥ 100 GHz koruma bandıyla ayrılır",
               "Ek A: üç hız sınıfı · ODN sınıfını iki yönde de OLT taşır, ONU sınıftan bağımsız",
               "FEC'i PMD eklemez: FEC sütunları istemci protokolüne ya da kod dönüştürmeye dayanır",
               "AMCC zorunlu: 115 kb/s üst modülasyon ya da 128 kb/s pilot ton\n%10 indeks · cezası tanımlı değil",
               "Ek C: AWG'li, düşük kayıplı (L1 8–17 · L2 16–25 dB), 16 kanallı başka bir tasarım noktası"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 20, TXT, line_spacing=0.9)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)])
        for it in items:
            fit(it, 12.8)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(DOWN * 0.3)
        self.at(self.cue("Bir:", 1.5))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 20.9))
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
            ("Ek A tablolarında ODN\nsınıfı büyüdükçe hangi\nparametreler değişir,\nhangileri değişmez?", CH[0]),
            ("Taban bant üst\nmodülasyonunda %10 indeks\nnasıl tanımlanır, zarfta\nkaç dB dalgalanma eder?", CH[1]),
            ("TWDM ONU'sunun gördüğü\nY girişimcisi neden\nS + 7 dB'dir?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 10'un başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.2), ("İkinci soru", 9.0), ("Üçüncü soru", 21.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün", 28.6))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        e10 = SERIES["episodes"][9]
        nxt = VGroup(T("SONRAKİ BÖLÜM · SEZON FİNALİ", 22, ACC, BOLD), T(f"Bölüm {e10['n']} · {e10['title']}", 54, TXT, BOLD), T(e10["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.4)
        self.at(self.cue("Sahaya İniş", 2.5))
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.0)
        self.play(FadeIn(nxt[2]), run_time=0.4)
        topics = VGroup(*[pill(s, c, 19) for s, c in (("izleme", ACC), ("koruma", GOLD), ("uyumluluk", PTP), ("baştan sona bir ONU'nun hayatı", GOOD))]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.4)
        fit(topics, 13.0)
        self.at(self.cue("İzleme,", 3.6))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in topics], lag_ratio=0.25), run_time=1.6)
        self.at(self.cue("Görüşmek üzere.", 8.6))
        bye = T("Görüşmek üzere.", 26, TXT, BOLD).move_to(DOWN * 1.7)
        self.play(FadeIn(bye), run_time=0.5)
        self.end(pad=0.5)
        self.play(FadeOut(nxt), FadeOut(topics), FadeOut(bye), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Bölüm {EP9['n']} · {EP9['title']}", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Coqui XTTS-v2 — ses: Damien Black (yerel GPU)", 22, ACC, BOLD),
                    T("(Coqui Public Model License — ticari olmayan kullanım)", 18, ACC),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep09_end")
