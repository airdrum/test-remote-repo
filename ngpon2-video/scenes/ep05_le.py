"""B05 · Laboratuvarda (alıcı testleri) and Kapanış."""
from ep05_common import *

Q3 = q_of(1e-3)


def ber_axes(o, w, h, p0, p1, q0=2.0, q1=7.2, exps=(-2, -3, -4, -6, -9, -12), xl="alınan güç (dBm)"):
    o = np.array(o, dtype=float)
    X = lambda p: o[0] + (p - p0) / (p1 - p0) * w
    Y = lambda q: o[1] + (q - q0) / (q1 - q0) * h
    g = VGroup(Line(o, o + [w, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, h, 0], color=MUTED, stroke_width=2))
    for e in exps:
        y = Y(q_of(10.0 ** e))
        g.add(Line([o[0] - 0.06, y, 0], [o[0] + 0.06, y, 0], color=MUTED, stroke_width=1.5), T(sup(e), 15, MUTED).next_to([o[0], y, 0], LEFT, buff=0.1))
    g.add(T(xl, 14, MUTED).next_to(o + [w * 0.72, 0, 0], DOWN, buff=0.12), T("BER (Q ölçeği)", 14, MUTED).next_to(o + [0, h, 0], RIGHT, buff=0.12))
    return g, X, Y


def ber_points(X, Y, ps, slope, pts, color, seed=1, r=0.065):
    rng = np.random.default_rng(seed)
    dots = VGroup(*[Dot([X(p), Y(Q3 + slope * (p - ps) + 0.07 * rng.standard_normal()), 0], radius=r, color=color) for p in pts])
    line = Line([X(pts[0] - 0.3), Y(Q3 + slope * (pts[0] - 0.3 - ps)), 0], [X(pts[-1] + 0.3), Y(Q3 + slope * (pts[-1] + 0.3 - ps)), 0], color=color, stroke_width=2.5)
    return dots, line


class E5LabA(Act5):
    HDR, MANIFEST, FIRST = H5["L"], M5("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Alıcı testleri")
        self.at(self.cue("Üç ana ölçüm", 2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Üç ölçüm")
        cs = VGroup(card("BER eğrisi", "hassasiyet · aşırı yük", None, ACC, w=3.95, h=1.45, tsize=25, bsize=19),
                    card("Yol cezası", "kısa ↔ en kötü fiber", None, GOLD, w=3.95, h=1.45, tsize=25, bsize=19),
                    card("X/S toleransı", "7 girişimci · sapma uçları", None, XC, w=3.95, h=1.45, tsize=25, bsize=19)).arrange(RIGHT, buff=0.3).move_to(UP * 1.0)
        voa = instrument("VOA", 1.8, 1.3).move_to([-1.6, -1.95, 0])
        pm = instr("PM", 1.8, 1.3, "−28,0 dBm", "R noktası").move_to([1.6, -1.95, 0])
        com = T("ortak nokta: kalibre zayıflatıcı + güvenilir güç ölçümü", 21, GOOD, BOLD).move_to(DOWN * 0.45)
        self.at(self.cue("hata oranı eğrisi", 3.3))
        self.play(FadeIn(cs[0], shift=UP * 0.15), run_time=0.5)
        self.at(self.cue("yol cezası ve", 4.7))
        self.play(LaggedStart(FadeIn(cs[1], shift=UP * 0.15), FadeIn(cs[2], shift=UP * 0.15), lag_ratio=0.4), run_time=0.8)
        self.at(self.cue("Hepsinin ortak", 7.3))
        self.play(FadeIn(com), run_time=0.5)
        self.play(FadeIn(voa, shift=UP * 0.1), FadeIn(pm, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Düzenek", h)
        y = 0.75
        tx = sbox("referans OLT Tx", "ya da test vericisi", TW_DS, 2.5, 1.0, 19, 15).move_to([-5.5, y, 0])
        voa = instrument("VOA", 1.6, 1.2).move_to([-2.85, y + 0.05, 0])
        cpl = sbox("kuplör", None, MUTED, 1.2, 0.65, 17).move_to([-0.85, y, 0])
        onu = sbox("ONU alıcısı", None, SIG, 2.0, 0.9, 19).move_to([1.85, y, 0])
        bert = instr("BERT", 1.6, 1.2, "BER 1,0E-3", "FEC öncesi", GOOD).move_to([5.3, y + 0.05, 0])
        pm = instr("PM", 1.6, 1.2, "−28,0 dBm", "R noktası").move_to([-0.85, -1.15, 0])
        l1 = Line(tx.get_right(), [voa[0].get_left()[0], y, 0], color=FEED, stroke_width=2.5)
        l2 = Line([voa[0].get_right()[0], y, 0], cpl.get_left(), color=FEED, stroke_width=2.5)
        l3 = Line(cpl.get_right(), onu.get_left(), color=FEED, stroke_width=2.5)
        l4 = Line(cpl.get_bottom(), pm[0].get_top(), color=GOLD, stroke_width=2.5)
        l5 = Line(onu.get_right(), [bert[0].get_left()[0], y, 0], color=FEED, stroke_width=2.5)
        rr = VGroup(DashedLine([0.25, y - 0.6, 0], [0.25, y + 0.6, 0], color=GOLD, stroke_width=2), T("R", 18, GOLD, BOLD).move_to([0.25, y + 0.8, 0]))
        fp = pill("BER: FEC öncesi (referans FEC öncesi tanımlı)", ACC, 18).move_to([3.4, -0.55, 0])
        o1 = VGroup(T("1", 20, GOOD, BOLD), T("BERT ile ham hata sayımı", 19, TXT)).arrange(RIGHT, buff=0.2)
        o2 = VGroup(T("2", 20, GOLD, BOLD), T("FEC çözücünün düzeltme sayaçlarından tahmin", 19, TXT)).arrange(RIGHT, buff=0.2)
        ops = VGroup(o1, o2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, -1.85, 0])
        self.at(self.cue("bir referans OLT", 0.9))
        self.play(FadeIn(tx, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("değişken optik", 4.4))
        self.play(Create(l1), FadeIn(voa), run_time=0.6)
        self.at(self.cue("R noktasında", 6.4))
        self.play(Create(l2), FadeIn(cpl), Create(l4), FadeIn(pm), FadeIn(rr), run_time=0.8)
        self.at(self.cue("ve ONU alıcısı", 9.6))
        self.play(Create(l3), FadeIn(onu), run_time=0.5)
        self.at(self.cue("Hata oranı FEC", 10.7))
        self.play(Create(l5), FadeIn(bert), FadeIn(fp, shift=UP * 0.1), run_time=0.7)
        self.at(self.cue("Bunun için ya", 17))
        self.play(FadeIn(o1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ya da FEC", 20.6))
        self.play(FadeIn(o2, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g2a")
        self.clear(h)
        h = self.show_heading("FEC sayaçlarından BER: dikkat", h)
        f = T("bayt düzeyinde sembol hata oranı  =  düzeltilen bayt / toplam bayt", 23, ACC, BOLD).move_to(UP * 1.75)

        def byte(errs):
            return VGroup(*[Square(0.22, stroke_color=MUTED, stroke_width=1.5, fill_color=WARN if i in errs else PANEL, fill_opacity=1) for i in range(8)]).arrange(RIGHT, buff=0.03)
        sc = VGroup(byte({2}), byte({6}), byte({4})).arrange(RIGHT, buff=0.25).move_to([-3.4, 0.45, 0])
        scl = VGroup(T("dağınık", 21, TXT, BOLD), T("her hatalı baytta 1 bit → BER ≈ SER / 8", 18, TXT)).arrange(DOWN, buff=0.08).next_to(sc, DOWN, buff=0.25)
        bu = byte(set(range(8))).move_to([3.4, 0.45, 0])
        bul = VGroup(T("öbek", 21, TXT, BOLD), T("bir baytta 8 bit → BER ≈ SER", 18, TXT)).arrange(DOWN, buff=0.08).next_to(bu, DOWN, buff=0.25)
        rng_ = T("SER / 8   ≤   BER   ≤   SER", 34, GOLD, BOLD).move_to(DOWN * 1.45)
        pr = pill("kesin hassasiyet ölçümü: ham hata sayımı (BERT)", GOOD, 20).move_to(DOWN * 2.5)
        self.at(self.cue("Düzeltilen bayt", 4.2))
        self.play(FadeIn(f, shift=DOWN * 0.1), run_time=0.6)
        self.at(self.cue("Bit hata oranı", 11.5))
        self.play(FadeIn(sc), FadeIn(scl), run_time=0.6)
        self.play(FadeIn(bu), FadeIn(bul), run_time=0.6)
        self.at(self.cue("bu oranın sekizde", 16.3))
        self.play(FadeIn(rng_, scale=0.95), run_time=0.6)
        self.at(self.cue("Kesin hassasiyet", 20.6))
        self.play(FadeIn(pr, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g3")
        self.clear(h)
        h = self.show_heading("BER eğrisi ve hassasiyet", h)
        ax, X, Y = ber_axes([-5.6, -2.7, 0], 6.8, 4.5, -31, -25)
        pts = [-30.4, -29.9, -29.4, -28.9, -28.4, -27.9, -27.4, -26.9]
        dots, line = ber_points(X, Y, -29.15, 0.85, pts, GOLD, seed=4)
        ref = DashedLine([X(-31), Y(Q3), 0], [X(-25), Y(Q3), 0], color=ACC, stroke_width=2)
        reft = T("BER ref 10⁻³ (10G)", 16, ACC, BOLD).next_to(ref, RIGHT, buff=0.1)
        sx = X(-29.15)
        sens = VGroup(DashedLine([sx, Y(Q3), 0], [sx, -2.7, 0], color=GOLD, stroke_width=2), Dot([sx, Y(Q3), 0], radius=0.09, color=GOLD))
        lim = VGroup(DashedLine([X(-28), -2.7, 0], [X(-28), Y(6.5), 0], color=WARN, stroke_width=2), T("sınır −28 dBm", 15, WARN, BOLD).move_to([X(-28) + 0.75, Y(6.8), 0]))
        st = T("hassasiyet", 15, GOLD, BOLD).next_to([sx, -2.7, 0], DOWN, buff=0.12)
        floor = VMobject(stroke_color=WARN, stroke_width=2.5).set_points_smoothly([[X(p), Y(min(Q3 + 0.85 * (p + 29.15), 4.4 + 0.25 * np.tanh((p + 27.6)))), 0] for p in np.linspace(-30.6, -25.2, 30)])
        floor = DashedVMobject(floor, num_dashes=40)
        flt = T("hata tabanı → eğri gösterir", 16, WARN, BOLD).move_to([X(-25.9), Y(3.75), 0])
        steps = VGroup(T("1  gücü adım adım azalt", 19, TXT), T("2  her noktada BER ölç", 19, TXT), T("3  Q ölçeğinde ≈ doğru", 19, TXT),
                       T("4  referansı kestiği güç", 19, TXT), T("    = hassasiyet", 19, GOLD, BOLD), T("eğri: gürültüyü ortalar,\nhata tabanını gösterir", 18, ACC, BOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([4.9, -0.3, 0])
        self.play(Create(ax[:2]), FadeIn(ax[2:]), FadeIn(steps[0]), run_time=0.6)
        self.play(FadeIn(steps[1]), LaggedStart(*[FadeIn(d, scale=0.5) for d in reversed(dots)], lag_ratio=0.25), run_time=2.4)
        self.at(self.cue("Q ölçeğinde", 4.1))
        self.play(Create(line), FadeIn(steps[2]), run_time=0.8)
        self.at(self.cue("Hassasiyet", 8.5))
        self.play(Create(ref), FadeIn(reft), run_time=0.5)
        self.at(self.cue("eğrinin referans", 9.3))
        self.play(Create(sens), FadeIn(st), FadeIn(steps[3:5]), run_time=0.6)
        self.at(self.cue("on gigabitte on", 12.4))
        self.play(Create(lim[0]), FadeIn(lim[1]), run_time=0.5)
        self.at(self.cue("Tek noktada", 14.7))
        self.play(FadeIn(steps[5]), run_time=0.5)
        self.at(self.cue("ölçüm gürültüsünü", 17.6))
        self.play(Create(floor), FadeIn(flt), run_time=0.9)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep05_labA")


class E5LabB(Act5):
    HDR, MANIFEST, PREV_BADGE = H5["L"], M5("lab"), "lab"

    def construct(self):
        self.beat("g4")
        h = self.show_heading("Yol cezası: aynı eğri, iki kez")
        ax, X, Y = ber_axes([-5.6, -2.7, 0], 7.0, 4.5, -31, -24)
        pts = [-30.3, -29.7, -29.1, -28.5, -27.9, -27.3]
        d1, l1 = ber_points(X, Y, -29.15, 0.85, pts, GOOD, seed=2)
        d2, l2 = ber_points(X, Y, -27.75, 0.85, [p + 1.4 for p in pts], GOLD, seed=3)
        ref = DashedLine([X(-31), Y(Q3), 0], [X(-24), Y(Q3), 0], color=ACC, stroke_width=2)
        reft = T("BER ref", 15, ACC, BOLD).next_to(ref, RIGHT, buff=0.1)
        lg = VGroup(T("kısa bağlantı", 17, GOOD, BOLD), T("en kötü dispersiyon:", 17, GOLD, BOLD), T("40 km · 840 ps/nm", 17, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 1.3, 0])
        da = DoubleArrow([X(-29.15), Y(Q3), 0], [X(-27.75), Y(Q3), 0], buff=0, color=WARN, stroke_width=3, tip_length=0.12)
        dat = T("OPP", 18, WARN, BOLD).next_to(da, UP, buff=0.12)
        r1 = T("OPP = fark @ BER ref", 22, WARN, BOLD).move_to([4.6, -0.2, 0])
        r2 = T("10G: < 2 dB olmalı", 24, TXT, BOLD).move_to([4.6, -0.85, 0])
        r3 = card("aşarsa", "farkı verici gücüyle kapat\n(Tablo 11-5, Not 6)", None, GOLD, w=4.2, h=1.35, tsize=20, bsize=18).move_to([4.6, -2.15, 0])
        self.play(Create(ax[:2]), FadeIn(ax[2:]), Create(ref), FadeIn(reft), run_time=0.7)
        self.at(self.cue("bir kez kısa", 3.2))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in d1], lag_ratio=0.15), Create(l1), FadeIn(lg[0]), run_time=1.1)
        self.at(self.cue("bir kez de en kötü", 5.4))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in d2], lag_ratio=0.15), Create(l2), FadeIn(lg[1]), run_time=1.1)
        self.at(self.cue("örneğin kırk", 8.5))
        self.play(FadeIn(lg[2]), run_time=0.4)
        self.at(self.cue("İki eğri arasındaki", 13.1))
        self.play(GrowFromCenter(da), FadeIn(dat), FadeIn(r1), run_time=0.6)
        self.at(self.cue("On gigabitte bu", 18.9))
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("kalmıyorsa standart", 22.6))
        self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g5")
        self.clear(h)
        h = self.show_heading("Aşırı yük: gücü artırın", h)
        ax, X, Y = ber_axes([-5.6, -2.7, 0], 9.6, 4.5, -32, -3, q1=7.6)
        qf = lambda p: min(Q3 + 0.9 * (p + 29.2), Q3 + 1.3 * (-5.4 - p), 7.3)
        ps = np.linspace(-30.0, -4.6, 120)
        cv = VMobject(stroke_color=GOLD, stroke_width=3).set_points_smoothly([[X(p), Y(qf(p)), 0] for p in ps])
        ref = DashedLine([X(-32), Y(Q3), 0], [X(-3), Y(Q3), 0], color=ACC, stroke_width=2)
        reft = T("BER ref", 15, ACC, BOLD).next_to(ref, RIGHT, buff=0.1)
        v28 = VGroup(DashedLine([X(-28), -2.7, 0], [X(-28), Y(7.0), 0], color=MUTED, stroke_width=1.5), T("−28", 15, MUTED, BOLD).next_to([X(-28), Y(7.0), 0], UP, buff=0.06))
        v7 = VGroup(DashedLine([X(-7), -2.7, 0], [X(-7), Y(7.0), 0], color=WARN, stroke_width=2), T("−7 dBm", 16, WARN, BOLD).next_to([X(-7), Y(7.0), 0], UP, buff=0.06))
        dot = Dot([X(-7), Y(qf(-7)), 0], radius=0.1, color=GOOD)
        okt = T("✓ BER hâlâ referansın altında", 18, GOOD, BOLD).next_to(dot, LEFT, buff=0.2).shift(DOWN * 0.15)
        arr = arrow([X(-20), Y(5.6), 0], [X(-10), Y(5.6), 0], GOLD, 3)
        arrt = T("güç ↑", 17, GOLD, BOLD).next_to(arr, UP, buff=0.06)
        apd = pill("APD: bu bölgede kazanç kontrolü kritik", PINK, 19).move_to([-0.4, Y(4.0), 0])
        self.play(Create(ax[:2]), FadeIn(ax[2:]), Create(ref), FadeIn(reft), FadeIn(v28), run_time=0.7)
        self.at(self.cue("gücü artırın", 2.0))
        self.play(GrowArrow(arr), FadeIn(arrt), Create(cv), run_time=1.6)
        self.at(self.cue("On gigabitte eksi", 6.6))
        self.play(Create(v7[0]), FadeIn(v7[1]), FadeIn(dot, scale=0.5), run_time=0.6)
        self.play(FadeIn(okt), run_time=0.4)
        self.at(self.cue("APD'li", 12.3))
        self.play(FadeIn(apd, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g5a")
        self.clear(h)
        h = self.show_heading("Alıcı ayar süresini ölçmek", h)
        y = 0.75
        tl = Arrow([-6.3, y, 0], [6.3, y, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.18)
        tlt = T("zaman", 14, MUTED).next_to(tl, DOWN, buff=0.08).align_to(tl, RIGHT)
        m0 = VGroup(Line([-4.6, y - 0.3, 0], [-4.6, y + 0.6, 0], color=GOLD, stroke_width=4), T("kanal değişikliği komutu", 17, GOLD, BOLD).move_to([-4.6, y + 0.85, 0]))
        m1 = VGroup(Line([2.4, y - 0.3, 0], [2.4, y + 0.6, 0], color=GOOD, stroke_width=4), T("yeni kanalda ↓ senkron kuruldu", 17, GOOD, BOLD).move_to([2.4, y + 0.85, 0]))
        seg = Rectangle(width=7.0, height=0.3, stroke_width=0, fill_color=ACC, fill_opacity=0.35).move_to([-1.1, y, 0])
        br = BraceBetweenPoints([-4.6, y - 0.35, 0], [2.4, y - 0.35, 0], DOWN, color=ACC)
        brt = T("TC katmanı ayar süresi (G.989.3 Ek F)", 19, ACC, BOLD).next_to(br, DOWN, buff=0.08)
        osc = instrument("OSC", 2.3, 1.65).move_to([-3.6, -2.0, 0])
        ol = VGroup(T("fiziksel katman ayar süresi", 20, PINK, BOLD), T("alıcı çıkışındaki optik / elektriksel\nsinyali osiloskopla izle", 18, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([1.4, -2.0, 0])
        self.play(GrowArrow(tl), FadeIn(tlt), FadeIn(m0), run_time=0.7)
        self.at(self.cue("yeni kanalda aşağı", 5.6))
        self.play(GrowFromEdge(seg, LEFT), FadeIn(m1), run_time=0.8)
        self.at(self.cue("F ekindeki", 10.3))
        self.play(FadeIn(br), FadeIn(brt), run_time=0.5)
        self.at(self.cue("Fiziksel katmandaki", 13.1))
        self.play(FadeIn(osc, shift=UP * 0.1), FadeIn(ol[0]), run_time=0.6)
        self.at(self.cue("alıcının çıkışındaki", 17.6))
        self.play(FadeIn(ol[1], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g6")
        self.clear(h)
        h = self.show_heading("X/S testi", h)
        ya = -1.75
        axg, X = lin_axis(-560, 560, -6.0, 6.0, ya, list(range(-500, 501, 100)), size=14, fmt=lambda v: "C" if v == 0 else ("+" if v > 0 else "−") + str(abs(int(v))), unit="ONU filtresinin merkezine göre (GHz)")
        tg = lobe(X, 0, ya, 1.3, 9, SIG, op=0.4)
        ks = [-2, -1, 1, 2, 3, 4, 5]
        nom = VGroup(*[lobe(X, 100 * k, ya, 1.9, 9, XC, op=0.22) for k in ks])
        tl = T("S = hassasiyet + OPP", 19, SIG, BOLD).move_to([-3.2, 1.85, 0])
        xl = T("7 × X = S + 4 dB · aynı hız", 19, XC, BOLD).move_to([3.0, 1.85, 0])
        st = T("S", 18, SIG, BOLD).move_to([X(0), ya + 1.55, 0])
        self.at(self.cue("Hedef kanalı S", 2.5))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(tg), FadeIn(st), FadeIn(tl), run_time=0.8)
        self.at(self.cue("Yedi TWDM", 7.7))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in nom], lag_ratio=0.1), FadeIn(xl), run_time=1.0)
        self.at(self.cue("Hedefi ve komşularını", 12.7))
        tg2 = lobe(X, 20, ya, 1.3, 9, SIG, op=0.4)
        nom2 = VGroup(*[lobe(X, 100 * k - 20 * np.sign(k), ya, 1.9, 9, XC, op=0.22) for k in ks])
        self.play(Transform(tg, tg2), st.animate.move_to([X(20), ya + 1.55, 0]), *[Transform(a, b) for a, b in zip(nom, nom2)], run_time=1.2)
        self.at(self.cue("hedef artı ya da", 17.1))
        pb = Rectangle(width=X(20) - X(-20), height=2.3, stroke_width=0, fill_color=SIG, fill_opacity=0.15).move_to([X(0), ya + 1.15, 0])
        pbt = T("hedef: S+ = C + 20", 16, SIG, BOLD).move_to([X(-150), ya + 2.6, 0])
        self.play(FadeIn(pb), FadeIn(pbt), run_time=0.5)
        self.at(self.cue("en yakın girişimci", 20.2))
        da = DoubleArrow([X(0), ya + 2.25, 0], [X(80), ya + 2.25, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.1)
        dat = T("X+1: C + 80 GHz", 16, GOLD, BOLD).next_to(da, RIGHT, buff=0.12)
        self.play(GrowFromCenter(da), FadeIn(dat), run_time=0.5)
        self.at(self.cue("Alıcının hata oranı", 23.4))
        ok = pill("alıcının BER'i referansta kalmalı", GOOD, 19).move_to(DOWN * 3.0)
        self.play(FadeIn(ok, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep05_labB")


class E5LabC(Act5):
    HDR, MANIFEST, PREV_BADGE = H5["L"], M5("lab"), "lab"

    def construct(self):
        self.beat("g6a")
        h = self.show_heading("Girişimcileri üretmek")
        ca = card("Ayarlanabilir lazerler + modülatör", "7 dalga boyu · tek modülatör", None, XC, w=5.4, h=1.45, tsize=21, bsize=19)
        cb = card("Gerçek OLT kanal sonlandırıcıları", "kendi vericileriyle", None, TW_DS, w=5.4, h=1.45, tsize=21, bsize=19)
        VGroup(ca, cb).arrange(RIGHT, buff=1.0).move_to(UP * 1.05)
        orr = T("ya da", 18, MUTED, BOLD).move_to(UP * 1.05)
        p1 = pill("girişim sinyali: hedefle aynı hızda · NRZ · sözde rastgele dizi (madde 10)", ACC, 19).move_to(DOWN * 0.6)
        lad = VGroup(*[VGroup(Rectangle(width=0.5, height=hh, stroke_width=0, fill_color=c, fill_opacity=0.85), T(n, 16, c, BOLD))
                       for n, c, hh in (("S", SIG, 0.6), ("X", XC, 1.0), ("Y", YC, 1.3), ("Z", ZC, 1.4))])
        for b in lad:
            b[1].next_to(b[0], DOWN, buff=0.08)
        lad.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([-3.6, -2.25, 0])
        p2 = VGroup(T("PtP girişimcileri de eklenir:", 20, TXT, BOLD), T("Y (yansıyan ↑) ve Z (PtP ↓) düzeylerinde", 20, YC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([1.9, -2.2, 0])
        self.play(FadeIn(ca, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("ya da gerçek", 4.2))
        self.play(FadeIn(orr), FadeIn(cb, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("girişim sinyali", 9.1))
        self.play(FadeIn(p1, shift=UP * 0.1), self.set_src("G.989.2 madde 10"), run_time=0.5)
        self.at(self.cue("PtP girişimcileri", 15.6))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in lad], lag_ratio=0.15), FadeIn(p2), run_time=0.9)
        self.end(pad=0.05)

        self.beat("g7")
        self.clear(h)
        h = self.show_heading("Titreşim toleransı testi", h)
        steps = ["BERT'in titreşim üreteci", "güç = hassasiyet + 1 dB", "bir frekansta sinüzoidal titreşimi artır", "BER referansa çıktığı genliği bul",
                 "bu genlik > o frekanstaki maske değeri", "birkaç frekansta tekrarla → eğri"]
        sl = VGroup(*[VGroup(T(str(i + 1), 21, ACC, BOLD), T(s, 19, TXT)).arrange(RIGHT, buff=0.25) for i, s in enumerate(steps)]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.7, -0.3, 0])
        xa0, xa1, ya = 1.1, 6.6, -2.4
        lax, LX = log_axis(1e4, 1e8, xa0, xa1, ya, [(1e4, "10k"), (1e5, "100k"), (1e6, "1M"), (1e7, "10M"), (1e8, "100M")], size=13)
        UY = lambda u: ya + (math.log10(u) + 1.45) * 1.6
        yax = Line([xa0, ya, 0], [xa0, UY(2.5), 0], color=MUTED, stroke_width=2)
        yl = T("UIpp", 14, MUTED).next_to(yax, UP, buff=0.06)
        fl = T("Hz", 13, MUTED).next_to(lax[0], RIGHT, buff=0.08)
        mk = VMobject(stroke_color=ACC, stroke_width=3.5).set_points_as_corners([[LX(1e4), UY(0.75), 0], [LX(4e5), UY(0.75), 0], [LX(4e6), UY(0.075), 0], [LX(1e8), UY(0.075), 0]])
        mkt = T("maske (10G)", 14, ACC, BOLD).move_to([LX(2e7), UY(0.075) - 0.25, 0])
        ms = [(3e4, 1.6), (2e5, 1.3), (1e6, 0.45), (3e6, 0.17), (1e7, 0.12), (4e7, 0.11)]
        dots = VGroup(*[Dot([LX(f), UY(u), 0], radius=0.08, color=GOOD) for f, u in ms])
        keys = [("Titreşim toleransı için", 0), ("Alıcı gücünü", 4.4), ("belirli bir frekansta", 8.5), ("ve hata oranının", 12.4), ("o frekanstaki", 16.9), ("Birkaç frekansta", 20.6)]
        self.play(Create(lax[0]), FadeIn(lax[1:]), Create(yax), FadeIn(yl), FadeIn(fl), Create(mk), FadeIn(mkt), run_time=0.8)
        for i, (key, d) in enumerate(keys):
            self.at(self.cue(key, d))
            anims = [FadeIn(sl[i], shift=RIGHT * 0.1)]
            if i == 3:
                anims.append(FadeIn(dots[2], scale=0.5))
            if i == 5:
                anims.append(LaggedStart(*[FadeIn(d, scale=0.5) for k, d in enumerate(dots) if k != 2], lag_ratio=0.15))
            self.play(*anims, run_time=0.8 if i == 5 else 0.45)
        self.end(pad=0.05)

        self.beat("g7a")
        self.clear(h)
        h = self.show_heading("Ardışık özdeş rakam testi", h)
        gen = instr("BERT", 2.0, 1.45, "desen üreteci", "CID deseni", GOLD).move_to([-5.4, 0.8, 0])
        bits = [1, 0, 1, 1, 0, 1] + [0] * 16 + [1, 0, 1, 0] + [1] * 16 + [0, 1, 0]
        x0, x1 = -4.0, 5.6
        tb = (x1 - x0) / len(bits)
        w = VMobject(stroke_color=TW_DS, stroke_width=3).set_points_as_corners(nrz(bits, x0, tb, 0.45, 1.15))
        r0 = Rectangle(width=16 * tb, height=0.95, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.1).move_to([x0 + (6 + 8) * tb, 0.8, 0])
        r1 = Rectangle(width=16 * tb, height=0.95, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.1).move_to([x0 + (26 + 8) * tb, 0.8, 0])
        t0 = T("72 × 0", 18, GOLD, BOLD).next_to(r0, UP, buff=0.08)
        t1 = T("72 × 1", 18, GOLD, BOLD).next_to(r1, UP, buff=0.08)
        ok = VGroup(T("ONU alıcısı:", 21, TXT, BOLD), T("BER bozulmamalı ✓", 24, GOOD, BOLD)).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.75)
        pl = pill("özellikle saat çıkarıcının döngü bant genişliği sorunlarını gösterir", ACC, 19).move_to(DOWN * 2.0)
        self.play(FadeIn(gen, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Yetmiş iki bitlik", 4.9))
        self.play(Create(w), run_time=1.0)
        self.play(FadeIn(r0), FadeIn(r1), FadeIn(t0), FadeIn(t1), run_time=0.5)
        self.at(self.cue("ve hata oranının", 9.8))
        self.play(FadeIn(ok, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Bu test özellikle", 13))
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g7b")
        self.clear(h)
        h = self.show_heading("Senkron dayanıklılığı testi", h)
        o = np.array([-5.5, -0.75, 0])
        ax = VGroup(Line(o, o + [7.6, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 2.6, 0], color=MUTED, stroke_width=2),
                    T("zaman (uzun süre)", 14, MUTED).next_to(o + [3.8, 0, 0], DOWN, buff=0.08), T("BER", 14, MUTED).next_to(o + [0, 2.6, 0], RIGHT, buff=0.1))
        ref = DashedLine(o + [0, 1.3, 0], o + [7.6, 1.3, 0], color=ACC, stroke_width=2)
        reft = T("≈ 10⁻³", 16, ACC, BOLD).next_to(ref, LEFT, buff=0.1)
        rng = np.random.default_rng(9)
        tr_ = VMobject(stroke_color=GOLD, stroke_width=2).set_points_as_corners([o + [x, 1.3 + 0.18 * rng.standard_normal(), 0] for x in np.linspace(0.05, 7.55, 90)])
        voa = instrument("VOA", 1.5, 1.1).move_to([-5.9 + 0.75, 2.0, 0]).shift(RIGHT * 0.2)
        ctr = VGroup(RoundedRectangle(corner_radius=0.12, width=2.2, height=1.5, stroke_color=GOOD, stroke_width=2.5, fill_color="#050810", fill_opacity=1),
                     T("LODS", 18, MUTED, BOLD), T("0", 48, GOOD, BOLD))
        ctr[1].move_to(ctr[0]).shift(UP * 0.45)
        ctr[2].move_to(ctr[0]).shift(DOWN * 0.15)
        ctr.move_to([4.9, 0.55, 0])
        p1 = pill("referans makine: BER 10⁻³'te yanlış senkron kaybı yok", ACC, 19).move_to(DOWN * 1.9)
        p2 = pill("sayaçta tek bir LODS bile bir uyarıdır", WARN, 20).move_to(DOWN * 2.75)
        self.at(self.cue("Zayıflatıcıyla", 2.9))
        self.play(Create(ax), Create(ref), FadeIn(reft), run_time=0.6)
        self.at(self.cue("hata oranı on üzeri", 4.4))
        self.play(Create(tr_), run_time=3.0)
        self.at(self.cue("ve uzun bir süre", 8.8))
        self.play(FadeIn(ctr, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("referans senkron", 13.9))
        self.play(FadeIn(p1, shift=UP * 0.1), self.set_src("G.989.3 §10.1.1.3"), run_time=0.5)
        self.at(self.cue("sayaçlarınızda", 21.1))
        self.play(FadeIn(p2, shift=UP * 0.1), Indicate(ctr, color=WARN, scale_factor=1.05), run_time=0.7)
        self.end(pad=0.05)

        self.note5("g8", [("1", "Güç ölçerin doğruluğu sonucu kaydırır", "R noktasındaki kuplörün oranını kalibre edin.", "Bir:"),
                          ("2", "Sıcaklık uçlarında tekrarlayın", "Tablo değerleri sıcaklık ve yaşlanma dahil en kötü koşul içindir.", "İki:")])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep05_labC")


class E5End(Act5):
    HDR, MANIFEST, FIRST = H5["E"], M5("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 5'in özeti")
        self.at(1.4)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["Her sınıfta aynı pencere: 2,5G −30 … −10 · 10G −28 … −7 dBm — sınıf farkı OLT vericisinde",
               "Hassasiyet FEC öncesi BER referansında: 10⁻⁴ (2,5G) · 10⁻³ (10G)",
               "X/S: filtre yalıtımı değil, alıcı toleransı — TWDM S + 4 · PtP S + 7 / 8 dB",
               "Titreşim toleransı: 1 dB güç cezası ölçütü",
               "Önce senkron, sonra profiller, sonra konuşma — LODS: tek kusur"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 20, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        for it in items:
            fit(it, 13.2)
        self.at(self.cue("Bir:", 1.2))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 14.4))
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
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("10G ↓ E2 sınıfında aşırı\nyük neden −7 değil,\n−9 dBm?", CH[0]),
            ("2,5G bir ONU için S, X\nve Z düzeyleri kaç dBm?", CH[1]),
            ("Önerilen M ile: senkron\ndurumdaki ONU kaç ardışık\nkötü çerçeveden sonra\nLODS ilan eder?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 6'nın başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, key in enumerate(["Birinci soru", "İkinci soru", "Üçüncü soru"]):
            self.at(self.cue(key, 1 + 7 * k))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün", 24))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        e6 = SERIES["episodes"][5]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Bölüm {e6['n']} · {e6['title']}", 54, TXT, BOLD), T(e6["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.0)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        y0, y1 = -2.6, -1.3
        dark = y0 + 0.12
        x = [-5.2, -3.6, -3.3, -1.3, -0.6, 2.6, 2.9, 4.8]
        env = VGroup(Line([-6.0, dark, 0], [x[1], dark, 0], color=MUTED, stroke_width=2.5),
                     Line([x[1], dark, 0], [x[2], y1, 0], color=TW_US, stroke_width=2.5))
        pre = VMobject(stroke_color=GOLD, stroke_width=2.5).set_points_as_corners(nrz([1, 0] * 6, x[2], (x[3] - x[2]) / 12, y1 - 0.45, y1, rise=0.02))
        dl = Rectangle(width=x[4] - x[3], height=0.45, stroke_color=PINK, stroke_width=2, fill_color=PINK, fill_opacity=0.25).move_to([(x[3] + x[4]) / 2, y1 - 0.225, 0])
        dat = VMobject(stroke_color=TW_US, stroke_width=2.5).set_points_as_corners(nrz([1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1], x[4], (x[5] - x[4]) / 16, y1 - 0.45, y1, rise=0.02))
        fall = VGroup(Line([x[5], y1 - 0.45, 0], [x[6], dark, 0], color=TW_US, stroke_width=2.5), Line([x[6], dark, 0], [6.0, dark, 0], color=MUTED, stroke_width=2.5))
        lbl = VGroup(T("önsöz", 15, GOLD, BOLD).next_to(pre, UP, buff=0.08), T("sınırlayıcı", 15, PINK, BOLD).next_to(dl, UP, buff=0.1),
                     T("karanlıkta bile güç", 15, MUTED, BOLD).move_to([4.8, dark + 0.25, 0]))
        burst = VGroup(env, pre, dl, dat, fall, lbl)
        self.at(self.cue("açılma ve kapanma", 4))
        self.play(Create(env), Create(pre), run_time=0.8)
        self.at(self.cue("önsöz ve", 5.4))
        self.play(FadeIn(dl), FadeIn(lbl[:2]), Create(dat), Create(fall), run_time=0.9)
        self.at(self.cue("kapalı bir vericinin", 7))
        self.play(FadeIn(lbl[2]), Indicate(fall[1], color=WARN), run_time=0.7)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(burst), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 5 · Ayarlanabilir Kulak", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Google Gemini TTS — ses: Sadaltager", 22, ACC, BOLD),
                    T("(2.5 Flash: açılış – Perde 1 · 3.1 Flash: Perde 2’den itibaren)", 18, ACC),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep05_end")
