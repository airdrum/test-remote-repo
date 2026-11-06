"""B02 · worked-example inserts: reverse budget (P2), 10G dispersion (P4), quiet-window position vs width (P5), lab test sequence."""
from math import erf
from kit import *

H2 = "BÖLÜM 2 · PERDE 2 — Yol kaybı sınıfları"
H4 = "BÖLÜM 2 · PERDE 4 — Mesafe, dispersiyon, yansıma"
H5 = "BÖLÜM 2 · PERDE 5 — Zaman: ranging ve EqD"
HL = "BÖLÜM 2 · LABORATUVARDA — Referans test ODN'i"
MX = "build/ep02/x/audio_proc/manifest.json"


class XAct(Act):
    def cue(self, sub, default=0.0):
        """Time of the first phrase cue in the current beat whose text contains `sub`."""
        for c in self.bmap[self.timeline[-1]["id"]]["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        return default


class E2X1(XAct):
    HDR, MANIFEST, PREV_BADGE = H2, MX, "fiz"

    def construct(self):
        self.beat("x1")
        h = self.show_heading("Ters hesap: sınıftan ayırıcıya")
        sc, x0, y = 0.36, -5.9, 0.3
        ax = NumberLine(x_range=[0, 32, 2], length=32 * sc, include_numbers=False, color=MUTED).move_to([x0 + 16 * sc, -1.0, 0])
        nums = VGroup(*[T(str(v), 15, MUTED).next_to(ax.n2p(v), DOWN, buff=0.08) for v in range(0, 33, 4)], T("dB", 15, MUTED).next_to(ax, RIGHT, buff=0.15))
        lim = DashedLine(ax.n2p(29) + UP * 0.1, ax.n2p(29) + UP * 2.6, color=CH[0], stroke_width=2.5)
        limt = T("N1 üst sınırı: 29 dB", 18, CH[0], BOLD).next_to(lim, UP, buff=0.08)
        def seg(a, b, color, label, op=0.9, tc=BG):
            r = Rectangle(width=(b - a) * sc, height=0.62, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x0 + (a + b) / 2 * sc, y, 0])
            return VGroup(r, T(label, 15, tc, BOLD).move_to(r))
        fib = seg(0, 5, ACC, "20 km = 5")
        spl = seg(5, 6.5, PINK, "1,5")
        room = DashedVMobject(Rectangle(width=22.5 * sc, height=0.62, color=CH[0], stroke_width=2), num_dashes=60).move_to([x0 + (6.5 + 29) / 2 * sc, y, 0])
        roomt = T("ayırıcıya kalan: 22,5 dB", 18, CH[0], BOLD).move_to(room)
        self.play(Create(ax), FadeIn(nums), run_time=0.6)
        self.at(self.cue("üst sınırı", 2))
        self.play(Create(lim), FadeIn(limt), run_time=0.6)
        self.at(self.cue("Yirmi kilometre", 4))
        self.play(GrowFromEdge(fib, LEFT), run_time=0.5)
        self.play(GrowFromEdge(spl, LEFT), run_time=0.4)
        self.at(self.cue("kalır", 7))
        self.play(Create(room), FadeIn(roomt), run_time=0.7)
        s64 = seg(6.5, 27.0, CH[0], "1:64 ≈ 20,5 dB", 0.85)
        pay = T("pay 2 dB ✓", 18, GOOD, BOLD).next_to(s64, UP, buff=0.12).align_to(s64, RIGHT)
        self.at(self.cue("altmış dört", 10))
        self.play(FadeOut(roomt), GrowFromEdge(s64, LEFT), run_time=0.8)
        self.play(FadeIn(pay, shift=DOWN * 0.1), run_time=0.4)
        s128 = seg(6.5, 30.0, WARN, "1:128 ≈ 23,5 dB", 0.85).shift(DOWN * 0.8)
        over = T("1 dB aşar ✗", 18, WARN, BOLD).next_to(s128, RIGHT, buff=0.15)
        self.at(self.cue("yüz yirmi sekiz", 14))
        self.play(GrowFromEdge(s128, LEFT), run_time=0.8)
        self.play(FadeIn(over), run_time=0.4)
        self.end(pad=0.05)

        self.beat("x2")
        self.clear(h)
        h = self.show_heading("Sınıf ↔ mesafe ↔ bölünme", h)
        tb = table(["Sınıf (üst sınır)", "Mesafe", "Ayırıcıya kalan", "Sığan oran", "Pay"],
                   [["N1 (29 dB)", "20 km", "22,5 dB", "1:64", "≈ 2 dB"], ["N2 (31 dB)", "20 km", "24,5 dB", "1:128", "≈ 1 dB"],
                    ["E1 (33 dB)", "40 km", "21,5 dB", "1:64", "≈ 1 dB"], ["E2 (35 dB)", "40 km", "23,5 dB", "1:128", "≈ 0"]],
                   [3.2, 1.8, 2.6, 2.2, 1.6], size=21, hsize=17, row_h=0.6).move_to(UP * 0.55)
        asm = T("varsayım: fiber ≈ 0,25 dB/km · ekler + konnektörler 1,5 dB · 1:64 ≈ 20,5 dB · 1:128 ≈ 23,5 dB", 16, MUTED).next_to(tb, DOWN, buff=0.25)
        self.play(FadeIn(tb[0]), FadeIn(asm), run_time=0.6)
        self.play(FadeIn(tb[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("N2", 3))
        self.play(FadeIn(tb[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("E1", 7))
        self.play(FadeIn(tb[3], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(tb[4].set_opacity(0.55), shift=UP * 0.1), run_time=0.5)
        tk = pill("sınıf seçimi = mesafe ile bölünme oranı arasında takas", GOOD, 20).to_edge(DOWN, buff=1.05)
        pk = T("pay → onarım ekleri ve yaşlanma için bütçe", 19, GOLD, BOLD).next_to(tk, DOWN, buff=0.2)
        self.at(self.cue("takas", 10))
        self.play(FadeIn(tk, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("aradaki pay", 12))
        self.play(FadeIn(pk), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep02_x1")


def _blur(bits, sigma):
    """NRZ bit sequence convolved with a Gaussian (unit bit period) → smooth function of t."""
    s2 = sigma * np.sqrt(2)
    def f(t):
        return sum(b * 0.5 * (erf((t - k) / s2) - erf((t - k - 1) / s2)) for k, b in enumerate(bits))
    return f


class E2X3(XAct):
    HDR, MANIFEST, PREV_BADGE = H4, MX, "std"

    def construct(self):
        self.beat("x3")
        self.set_badge("fiz")
        h = self.show_heading("10G'de dispersiyon neden önemli?")
        bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
        tb, x0 = 1.05, -5.6
        def wave(sigma, y0, color, amp=1.1):
            f = _blur(bits, sigma)
            return FunctionGraph(lambda x: y0 + amp * f((x - x0) / tb), x_range=[x0, x0 + len(bits) * tb], color=color, stroke_width=3.5)
        clean = VMobject(color=ACC, stroke_width=3.5).set_points_as_corners(np.array(nrz(bits, x0, tb, 0.7, 1.8, rise=0.03)))
        slots = VGroup(*[DashedLine([x0 + k * tb, 0.55, 0], [x0 + k * tb, 1.95, 0], color=LINE, stroke_width=1) for k in range(len(bits) + 1)])
        bt = T("1 bit ≈ 100 ps (≈ 9,95 Gbit/s)", 20, ACC, BOLD).next_to(slots, UP, buff=0.12).align_to(slots, LEFT)
        blur = wave(0.33, -1.5, WARN)
        slots2 = slots.copy().shift(DOWN * 2.2)
        dt = T("20 km × ≈ 21 ps/nm/km = 420 ps/nm → geniş / çırpıntılı spektrumda semboller karışır (ISI)", 18, WARN, BOLD).next_to(slots2, DOWN, buff=0.15).align_to(slots2, LEFT)
        self.play(Create(slots), Create(clean), run_time=1.0)
        self.at(self.cue("yüz pikosaniye", 2))
        self.play(FadeIn(bt), run_time=0.5)
        self.at(self.cue("Yirmi kilometrede", 5))
        self.play(Create(slots2), Create(blur), run_time=1.4)
        self.play(FadeIn(dt), run_time=0.5)
        tx = VGroup(pill("↓ OLT: düşük çırpıntılı EML (tipik)", ACC, 19), pill("↑ ONU: doğrudan modüle, burst modlu lazer (tipik) → 10G ↑ daha zorlu", GOLD, 19))
        self.at(self.cue("Bu yüzden", 9))
        self.play(*[FadeOut(m) for m in (slots, clean, bt)], VGroup(slots2, blur, dt).animate.shift(UP * 2.0), run_time=0.6)
        tx.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 1.9).align_to(dt, LEFT)
        self.play(FadeIn(tx[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at(self.cue("Yukarı yönde", 12))
        self.play(FadeIn(tx[1], shift=RIGHT * 0.2), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.set_badge("std")
        self.save_timeline("ep02_x3")


class E2X4(XAct):
    HDR, MANIFEST, PREV_BADGE = H5, MX, "tc"

    def construct(self):
        self.beat("x4")
        h = self.show_heading("Pencerenin konumu ve genişliği")
        f1 = T("konum:  W0 = RspTime_min + L_min·(n_dn + n_up)/c + StartTime   (13-2)", 19, ACC, BOLD)
        f2 = T("genişlik:  W = RspTime_var + D_maks·(n_dn + n_up)/c + Rand_maks + T_SN   (13-3)", 19, GOLD, BOLD)
        VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(h, DOWN, buff=0.35, aligned_edge=LEFT)
        k, x0 = 0.0165, -5.4
        ax = NumberLine(x_range=[0, 700, 50], length=700 * k, include_numbers=False, color=MUTED).move_to([x0 + 350 * k, -2.3, 0])
        nums = VGroup(*[T(str(v), 14, MUTED).next_to(ax.n2p(v), DOWN, buff=0.08) for v in range(0, 701, 100)], T("µs", 14, MUTED).next_to(ax, RIGHT, buff=0.12))
        def win(a, w, y, color, label):
            r = Rectangle(width=w * k, height=0.55, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.18).move_to([x0 + (a + w / 2) * k, y, 0])
            lab = T(label, 17, color, BOLD).next_to([x0, y, 0], LEFT, buff=0.15)
            return VGroup(r, T(f"{w} µs", 16, GOLD, BOLD).move_to(r)), lab
        wa, la = win(34, 250, -0.3, CH[1], "0–20 km")
        wb, lb = win(230, 250, -1.3, CH[3], "20–40 km")
        self.play(FadeIn(f1, shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("genişliği", 4))
        self.play(FadeIn(f2, shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("Bu yüzden", 7))
        self.play(Create(ax), FadeIn(nums), FadeIn(la), FadeIn(wa), run_time=0.8)
        self.play(TransformFromCopy(wa, wb), FadeIn(lb), run_time=0.9)
        sh = Arrow([x0 + 34 * k, -1.75, 0], [x0 + 230 * k, -1.75, 0], buff=0, color=CH[3], stroke_width=3, max_tip_length_to_length_ratio=0.12)
        sht = T("+ ≈ 196 µs (L_min = 20 km)", 16, CH[3], BOLD).next_to(sh, DOWN, buff=0.04)
        self.at(self.cue("ileri kayar", 9))
        self.play(GrowArrow(sh), FadeIn(sht), run_time=0.6)
        self.end(pad=0.05)

        self.beat("x5")
        self.clear(h)
        h = self.show_heading("T_eqd ise toplam mesafeye bağlı", h)
        k2, x1 = 0.022, -5.6
        def bar(v, y, color, label):
            r = Rectangle(width=v * k2, height=0.6, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x1 + v * k2 / 2, y, 0])
            return VGroup(r, T(label, 17, BG, BOLD).move_to(r))
        b1 = bar(232, 1.0, CH[1], "0–20 km: ≥ ≈ 232 µs")
        b2 = bar(428, -0.2, CH[3], "20–40 km: ≥ ≈ 428 µs")
        calc = T("36 µs + 40 km × ≈ 9,8 µs/km ≈ 36 + 392 ≈ 428 µs  ≈ 3,4 × 125 µs", 21, CH[3], BOLD).move_to(DOWN * 1.35).align_to(b2, LEFT)
        std = VGroup(DashedLine([x1 + 236 * k2, 0.55, 0], [x1 + 236 * k2, 1.75, 0], color=GOLD, stroke_width=2.5))
        std.add(T("standart örneği: 236 µs (§13.1.7)", 17, GOLD, BOLD).next_to(std[0], RIGHT, buff=0.12).shift(UP * 0.45))
        self.play(GrowFromEdge(b1, LEFT), run_time=0.6)
        self.at(self.cue("kırk kilometrededir", 2))
        self.play(GrowFromEdge(b2, LEFT), run_time=0.8)
        self.at(self.cue("Gidiş dönüş", 3))
        self.play(FadeIn(calc), run_time=0.6)
        self.at(self.cue("Standardın", 6))
        self.play(Create(std[0]), FadeIn(std[1]), self.set_src("G.989.3 §13.1.2, §13.1.4, §13.1.7"), run_time=0.7)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep02_x4")


class E2X6(XAct):
    HDR, MANIFEST, PREV_BADGE = HL, MX, "lab"

    def construct(self):
        self.beat("x6")
        h = self.show_heading("Önerilen test sırası")
        steps = [("1 · Kalibrasyon", "iki bant · iki yön\nreferans ODN kaydı", ACC),
                 ("2 · OPL_min", "aşırı yük testi", CH[3]),
                 ("3 · VOA ↑", "referans BER'e kadar\n→ gerçek bütçe", GOLD),
                 ("4 · Sıcaklık", "en kötü sıcaklıkta\naynı ölçüm", WARN)]
        cards = VGroup(*[card(t, b, None, c, w=2.85, h=1.9, tsize=20, bsize=17) for t, b, c in steps]).arrange(RIGHT, buff=0.42).move_to(UP * 0.45)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, color=MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.35) for a, b in zip(cards[:-1], cards[1:])])
        cues = [self.cue("Bir:", 1), self.cue("İki:", 4), self.cue("Üç:", 6), self.cue("Dört:", 10)]
        for i, t0 in enumerate(cues):
            self.at(t0)
            anims = [FadeIn(cards[i], shift=UP * 0.2)]
            if i:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.55)
        mg = T("marj = ölçülen bütçe − sınıf üst sınırı", 26, GOOD, BOLD).move_to(DOWN * 1.75)
        self.at(self.cue("Ölçülen bütçe", 13))
        self.play(FadeIn(mg, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep02_x6")
