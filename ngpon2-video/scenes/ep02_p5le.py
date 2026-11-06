"""B02 · Perde 5 (zaman: ranging ve EqD), Laboratuvarda (referans test ODN'i), Kapanış."""
from kit import *

H5, HL, HE = "BÖLÜM 2 · PERDE 5 — Zaman: ranging ve EqD", "BÖLÜM 2 · LABORATUVARDA — Referans test ODN'i", "BÖLÜM 2 · KAPANIŞ"
M5, ML, ME = "build/ep02/p5/audio_proc/manifest.json", "build/ep02/lab/audio_proc/manifest.json", "build/ep02/end/audio_proc/manifest.json"
US_ = 0.0185  # scene units per µs on timing axes


class E2P5A(Act):
    HDR, MANIFEST, FIRST = H5, M5, True

    def construct(self):
        self.beat("f1")
        tc = self.title_card("PERDE 5", "Zaman: ranging ve EqD")
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 2)
        self.to_header(tc)
        self.set_badge("tc")
        h = self.show_heading("ODN'in zaman parametreleri (G.989.3 §13.1)")
        sc = 0.25
        x0 = -5.0
        ax = NumberLine(x_range=[0, 40, 5], length=40 * sc, include_numbers=False, color=MUTED).move_to([x0 + 20 * sc, -1.4, 0])
        nums = VGroup(*[T(str(v), 15, MUTED).next_to(ax.n2p(v), DOWN, buff=0.08) for v in range(0, 41, 10)], T("km", 15, MUTED).next_to(ax, RIGHT, buff=0.15))
        olt = box(1.0, 0.6, "OLT", "#3B4A75", 15).next_to(ax.n2p(0), LEFT, buff=0.3).shift(UP * 1.2)
        lmin, dmax = 6, 20
        onus = VGroup(*[Dot(ax.n2p(v) + UP * 0.35, color=CH[i % 4], radius=0.1) for i, v in enumerate([6, 9, 14, 21, 26])])
        b1 = BraceBetweenPoints(ax.n2p(0) + UP * 0.8, ax.n2p(lmin) + UP * 0.8, direction=UP, color=GOLD)
        b2 = BraceBetweenPoints(ax.n2p(lmin) + UP * 1.5, ax.n2p(lmin + dmax) + UP * 1.5, direction=UP, color=ACC)
        t1 = T("L_min", 20, GOLD, BOLD).next_to(b1, UP, buff=0.05)
        t2 = T("D_maks", 20, ACC, BOLD).next_to(b2, UP, buff=0.05)
        eq = T("L_min ≤ Lᵢ ≤ L_min + D_maks   (13-1)", 26, TXT, BOLD).to_edge(DOWN, buff=0.75)
        self.play(Create(ax), FadeIn(nums), FadeIn(olt), LaggedStart(*[FadeIn(o, scale=1.5) for o in onus], lag_ratio=0.15), self.set_src("G.989.3 §13.1"), run_time=1.2)
        self.at(self.cues[3] - 0.2 if len(self.cues) > 3 else 5)
        self.play(GrowFromCenter(b1), FadeIn(t1), run_time=0.6)
        self.play(GrowFromCenter(b2), FadeIn(t2), run_time=0.6)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 9)
        self.play(Write(eq), run_time=0.9)
        self.end(pad=0.05)

        # f2 — response time
        self.beat("f2")
        self.clear(h)
        h = self.show_heading("ONU yanıt süresi", h)
        x0 = -5.6
        tl = Arrow([x0, 0, 0], [x0 + 9.5, 0, 0], buff=0, color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.02)
        rx = Line([x0 + 0.5, -0.4, 0], [x0 + 0.5, 0.6, 0], color=WHITE, stroke_width=3)
        rxt = T("↓ çerçeve alınır", 17, WHITE).next_to(rx, UP, buff=0.05)
        band = Rectangle(width=2 * 0.12, height=1.0, stroke_width=0, fill_color=GOLD, fill_opacity=0.5).move_to([x0 + 0.5 + 35 * 0.12, 0.1, 0])
        bt = T("35 ± 1 µs", 22, GOLD, BOLD).next_to(band, UP, buff=0.1)
        ar = DoubleArrow([x0 + 0.5, -0.6, 0], [x0 + 0.5 + 35 * 0.12, -0.6, 0], buff=0, color=GOLD, stroke_width=2, tip_length=0.12)
        rsp = T("34 µs (min) · 36 µs (maks)", 18, MUTED).next_to(ar, DOWN, buff=0.1)
        self.play(Create(tl), Create(rx), FadeIn(rxt), run_time=0.7)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(GrowFromCenter(ar), FadeIn(band), FadeIn(bt), run_time=0.8)
        self.play(FadeIn(rsp), run_time=0.4)
        self.end(pad=0.05)

        self.beat("f2a")
        f = T("gidiş-dönüş yayılma = L · (n_dn + n_up) / c", 30, ACC, BOLD).move_to(DOWN * 2.0)
        sub = T("↓ ve ↑ farklı dalga boylarında → farklı grup indisleri", 19, MUTED).next_to(f, DOWN, buff=0.15)
        self.play(Write(f), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f2b")
        self.clear(h)
        steps = VGroup(*[pill(s, ACC, 20) for s in ("↓ PHY çerçevesini al", "BWmap'i çöz", "gerekirse FEC", "yanıtı hazırla")]).arrange(RIGHT, buff=0.25).move_to(UP * 0.4)
        arrs = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.05, color=MUTED, stroke_width=2) for i in range(3)])
        why = T("sistem genelinde sabit → OLT her ONU'nun ne zaman hazır olacağını bilir", 20, GOLD, BOLD).move_to(DOWN * 1.2)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in steps], lag_ratio=0.25), Create(arrs), run_time=1.6)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 6)
        self.play(FadeIn(why), run_time=0.5)
        self.end(pad=0.05)

        # f3/f4 — quiet window
        self.beat("f3")
        self.clear(h)
        h = self.show_heading("Seri numarası toplama: sessiz pencere", h)
        y = 0.6
        x0 = -6.0
        tl = Line([x0, y - 0.35, 0], [x0 + 12.0, y - 0.35, 0], color=MUTED, stroke_width=2)
        reg = VGroup(*[Rectangle(width=0.6, height=0.5, stroke_width=0, fill_color=CH[i % 4], fill_opacity=0.9).move_to([x0 + 0.5 + 0.75 * i, y, 0]) for i in range(4)],
                     *[Rectangle(width=0.6, height=0.5, stroke_width=0, fill_color=CH[i % 4], fill_opacity=0.9).move_to([x0 + 8.8 + 0.75 * i, y, 0]) for i in range(4)])
        qw = Rectangle(width=5.2, height=1.0, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.1).move_to([x0 + 5.8, y + 0.1, 0])
        qt = T("sessiz pencere — çalışan ONU'lar susar", 18, GOLD, BOLD).next_to(qw, UP, buff=0.08)
        sn = Rectangle(width=0.35, height=0.4, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([x0 + 4.2, y, 0])
        snt = T("yeni ONU: SN yanıtı (yeri bilinmiyor)", 16, WHITE).next_to(qw, DOWN, buff=0.15)
        self.play(Create(tl), LaggedStart(*[FadeIn(r) for r in reg], lag_ratio=0.08), run_time=1.0)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 3)
        self.play(FadeIn(qw), FadeIn(qt), run_time=0.7)
        self.play(FadeIn(sn, scale=1.4), FadeIn(snt), run_time=0.6)
        for xx in (x0 + 6.3, x0 + 7.4, x0 + 5.2):
            self.play(sn.animate.move_to([xx, y, 0]), run_time=0.35)
        self.end(pad=0.05)

        self.beat("f4")
        self.play(*[FadeOut(m) for m in (reg, sn, snt, tl)], qw.animate.move_to([0, 1.3, 0]).set_opacity(0.0), FadeOut(qt), run_time=0.5)
        def stack(y, parts, total, color):
            g, x, k = VGroup(), -5.6, 0
            for v, c, t in parts:
                w = v * US_
                r = Rectangle(width=max(w, 0.05), height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x + w / 2, y, 0])
                if w > 1:
                    lt = T(t, 14, BG, BOLD).move_to(r)
                else:
                    lt = T(t, 14, c, BOLD).next_to(r, DOWN if k % 2 == 0 else UP, buff=0.06)
                    k += 1
                g.add(VGroup(r, lt))
                x += w
            return VGroup(g, T(total, 22, color, BOLD).next_to(g, RIGHT, buff=0.25))
        s20 = stack(1.0, [(200, CH[1], "RTD değişimi 200 µs"), (2, GOLD, "2 µs yanıt"), (48, PINK, "48 µs rastgele")], "≈ 250 µs (20 km)", ACC)
        s40 = stack(-0.5, [(400, CH[1], "RTD değişimi 400 µs"), (2, GOLD, "2"), (48, PINK, "48")], "≈ 450 µs (40 km)", WARN)
        lab = T("yanıt süresi değişimi: 2 µs · rastgele gecikme: 0 … 48 µs", 17, MUTED).next_to(s20, UP, buff=0.4).align_to(s20, LEFT)
        self.play(FadeIn(lab), LaggedStart(*[GrowFromEdge(p, LEFT) for p in s20[0]], lag_ratio=0.3), run_time=1.4)
        self.play(FadeIn(s20[1]), self.set_src("G.989.3 §13.1.2"), run_time=0.4)
        self.at(self.cues[-1] - 0.3)
        self.play(LaggedStart(*[GrowFromEdge(p, LEFT) for p in s40[0]], lag_ratio=0.3), FadeIn(s40[1]), run_time=1.2)
        self.end(pad=0.05)

        self.beat("f5")
        cmp_ = VGroup(T("Bölüm 1 hesabı: 196 µs", 21, MUTED), T("→ standart: 200 µs", 21, ACC, BOLD)).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.85)
        rng = pill("ranging penceresi (rastgele gecikme yok): 202 µs (20 km) · 402 µs (40 km)", GOLD, 19).move_to(DOWN * 2.6)
        self.play(FadeIn(cmp_), run_time=0.6)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(FadeIn(rng), self.set_src("G.989.3 §13.1.3"), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p5A")


class E2P5B(Act):
    HDR, MANIFEST, PREV_BADGE = H5, M5, "tc"

    def construct(self):
        self.beat("f5a")
        h = self.show_heading("Sessiz pencerenin bedeli")
        x0 = -5.8
        frames = VGroup(*[Rectangle(width=125 * US_ * 1.6, height=0.5, stroke_color=CH[1], stroke_width=2, fill_color=CH[1], fill_opacity=0.08 + 0.1 * (i % 2)).move_to([x0 + 125 * US_ * (i + 0.5) * 1.6, 0.6, 0]) for i in range(3)])
        ft = VGroup(*[T("125 µs", 15, CH[1]).next_to(f, UP, buff=0.05) for f in frames])
        qw = Rectangle(width=250 * US_ * 1.6, height=0.9, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.15).move_to([x0 + 250 * US_ * 0.8, -0.4, 0])
        qt = T("250 µs = 2 çerçeve boyunca ↑ veri yok", 20, GOLD, BOLD).next_to(qw, DOWN, buff=0.2).align_to(qw, LEFT)
        self.play(FadeIn(frames), FadeIn(ft), run_time=0.7)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 4)
        self.play(GrowFromEdge(qw, LEFT), FadeIn(qt), run_time=0.9)
        dm = pill("diferansiyel mesafe → güç bütçesi + keşif kesintisi", ACC, 19).to_edge(DOWN, buff=0.8)
        self.at(self.cues[-1] - 0.4)
        self.play(FadeIn(dm), run_time=0.5)
        self.end(pad=0.05)

        # f6 / f6a — Teqd and EqD
        self.beat("f6")
        self.clear(h)
        h = self.show_heading("Eşitleme gecikmesi", h)
        f1 = T("T_eqd ≥ RspTime_maks + (L_min + D_maks)·(n_dn + n_up)/c   (13-6)", 24, TXT, BOLD).move_to(UP * 1.9)
        f2 = T("EqDᵢ = T_eqd − RTDᵢ   (13-7)", 28, ACC, BOLD).next_to(f1, DOWN, buff=0.3)
        x0 = -5.6
        teq = 232
        bars = VGroup()
        for k, (rtd, c) in enumerate([(36, CH[1]), (110, CH[2]), (232, CH[3])]):
            y = -0.4 - 0.75 * k
            r = Rectangle(width=rtd * US_, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x0 + rtd * US_ / 2, y, 0])
            e = Rectangle(width=max((teq - rtd) * US_, 0.01), height=0.5, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.2).next_to(r, RIGHT, buff=0)
            bars.add(VGroup(r, e, T(f"RTD {rtd} µs", 14, BG if rtd > 60 else c, BOLD).move_to(r) if rtd > 60 else T(f"RTD {rtd}", 14, c, BOLD).next_to(r, UP, buff=0.04)))
        line = DashedLine([x0 + teq * US_, 0.1, 0], [x0 + teq * US_, -2.2, 0], color=WHITE, stroke_width=2)
        lt = T("T_eqd", 18, WHITE, BOLD).next_to(line, RIGHT, buff=0.1).shift(UP * 1.0)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(FadeIn(f1), self.set_src("G.989.3 §13.1.4"), run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in bars], lag_ratio=0.2), FadeIn(VGroup(*[b[2] for b in bars])), Create(line), FadeIn(lt), run_time=1.2)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(f2), LaggedStart(*[GrowFromEdge(b[1], LEFT) for b in bars], lag_ratio=0.2), run_time=1.2)
        self.end(pad=0.05)

        self.beat("f6a")
        ex = VGroup(T("örnek: L_min = 0, D_maks = 20 km", 20, MUTED), T("36 µs + ≈196 µs = ≈232 µs  ≈ 1,9 × 125 µs", 26, GOLD, BOLD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5).shift(RIGHT * 2.6)
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.8)
        self.at(self.cues[-1] - 0.3)
        self.play(Indicate(bars[0][1], color=WHITE), run_time=0.8)
        self.end(pad=0.05)

        self.clear()
        self.save_timeline("ep02_p5B")


class E2P5B2(Act):
    HDR, MANIFEST, PREV_BADGE = H5, M5, "tc"

    def construct(self):
        h = None
        self.beat("f7")
        self.clear(h)
        h = self.show_heading("Bit doğruluğunda hizalama", h)
        acc = T("EqD çözünürlüğü: 1 bit @ 2,48832 Gbit/s ≈ 0,40 ns", 26, ACC, BOLD).move_to(UP * 1.4)
        grid = VGroup(*[Line([-5.5 + 1.1 * i, -1.6, 0], [-5.5 + 1.1 * i, 0.4, 0], color=LINE, stroke_width=1.5) for i in range(11)])
        b1 = Rectangle(width=2.0, height=0.5, stroke_width=0, fill_color=CH[1], fill_opacity=0.9).move_to([-4.4 + 1.0, -0.2, 0])
        b2 = Rectangle(width=2.0, height=0.5, stroke_width=0, fill_color=CH[3], fill_opacity=0.9).move_to([-4.4 + 3.3, -0.2, 0])
        lb = VGroup(T("20 km ONU", 15, CH[1]).next_to(b1, DOWN, buff=0.1), T("OLT yanındaki ONU", 15, CH[3]).next_to(b2, DOWN, buff=0.1))
        self.play(FadeIn(acc), run_time=0.6)
        self.play(Create(grid), FadeIn(b1, shift=LEFT * 0.5), FadeIn(b2, shift=LEFT * 0.5), FadeIn(lb), run_time=1.0)
        self.end(pad=0.05)

        self.beat("f7a")
        self.clear(h)
        h = self.show_heading("Sürüklenme ve koruma süresi", h)
        msg = table(["Ranging_Time · kontrol oktedi", "Anlamı"], [["P = 1", "EqD mutlak değer"], ["P = 0, S = 0/1", "EqD göreli: + / − artış"], ["X = 1", "belirli bir ↓/↑ dalga boyu çifti için"]],
                    [5.0, 5.6], size=21, hsize=18, row_h=0.58).move_to(UP * 0.6)
        self.play(FadeIn(msg), self.set_src("G.989.3 §11.3.3.3, Tablo 11-7 · §10.1.2.3"), run_time=0.8)
        gt = pill("burst'ler arası koruma süresi: önerilen en az 64 bit (açılma/kapanma + sürüklenme)", GOLD, 19).to_edge(DOWN, buff=0.8)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(gt, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p5B2")


class E2P5C(Act):
    HDR, MANIFEST, PREV_BADGE = H5, M5, "tc"

    def construct(self):
        self.beat("f8")
        h = self.show_heading("Kanal değişince mesafe değişir")
        ct1 = box(1.2, 0.5, "CT1", CH[0], 16).move_to([-5.6, 1.2, 0])
        ct2 = box(1.2, 0.5, "CT2", CH[1], 16).move_to([-5.6, -0.2, 0])
        wm = box(0.6, 2.2, "WM", "#3B4A75", 15).move_to([-3.0, 0.5, 0])
        a1 = Line(ct1.get_right(), [wm.get_left()[0], ct1.get_y(), 0], color=CH[0], stroke_width=3)
        coil = VGroup(*[Circle(radius=0.1 + 0.05 * k, color=CH[1], stroke_width=2) for k in range(3)]).move_to([-4.3, -0.2, 0])
        a2 = VGroup(Line(ct2.get_right(), coil.get_left(), color=CH[1], stroke_width=3), coil, Line(coil.get_right(), [wm.get_left()[0], -0.2, 0], color=CH[1], stroke_width=3))
        feed = Line(wm.get_right(), [1.0, 0.5, 0], color=FEED, stroke_width=4)
        onu = box(1.3, 0.55, "ONU", CH[0], 16).move_to([2.0, 0.5, 0])
        self.play(FadeIn(VGroup(ct1, ct2, wm, a1, a2, feed, onu)), run_time=0.9)
        y = -2.0
        slots = VGroup(*[Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([-4.5 + 1.6 * k, y, 0]) for k, c in enumerate([CH[2], CH[3], CH[2], CH[3]])])
        st = T("hedef kanaldaki zaman dilimleri", 16, MUTED).next_to(slots, UP, buff=0.1).align_to(slots, LEFT)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(onu[0].animate.set_stroke(CH[1]), Indicate(coil, color=WHITE), FadeIn(slots), FadeIn(st), run_time=1.0)
        mine = Rectangle(width=1.4, height=0.5, stroke_color=WHITE, stroke_width=2.5, fill_color=CH[1], fill_opacity=0.5).move_to([-4.5 + 1.6 * 1 + 0.9, y, 0])
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(FadeIn(mine, shift=RIGHT * 0.6), run_time=0.7)
        rog = T("eski EqD → başka ONU'nun dilimine taşar: rogue ONU", 20, WARN, BOLD).next_to(slots, DOWN, buff=0.3)
        self.at(self.cues[-1] - 0.5)
        self.play(Flash(mine.get_center(), color=WARN), FadeIn(rog), self.set_src("G.989.3 Ek VII"), run_time=0.8)
        self.end(pad=0.05)

        self.beat("f9")
        self.clear(h)
        h = self.show_heading("Üç yöntem (G.989.3 Ek VII)", h)
        meth = VGroup(card("1 · Yeniden ranging", "yeni kanalda ranging hibesi\nen basit, en yavaş", "VII.1", CH[0], w=4.0, h=2.0, tsize=22, bsize=18),
                      card("2 · Tutarlı EqD", "CT'ler T_eqd'yi koordine eder\nONU aynı EqD'yi taşır", "VII.2", CH[1], w=4.0, h=2.0, tsize=22, bsize=18),
                      card("3 · Ön yapılandırma", "hedef kanalın EqD'si\nönceden bilinir", "VII.3", CH[2], w=4.0, h=2.0, tsize=22, bsize=18)).arrange(RIGHT, buff=0.3).move_to(UP * 0.2)
        n = len(self.cues)
        for k, t0 in enumerate([self.cues[min(1, n - 1)], self.cues[min(2, n - 1)], self.cues[min(3, n - 1)]]):
            self.at(t0 - 0.2)
            self.play(FadeIn(meth[k], shift=UP * 0.2), run_time=0.6)
        self.end(pad=0.05)

        self.beat("f9a")
        self.play(meth.animate.scale(0.75).arrange(DOWN, buff=0.22).to_edge(LEFT, buff=0.55).shift(DOWN * 0.45), run_time=0.7)
        self.play(*[m.animate.set_opacity(0.35) for k, m in enumerate(meth) if k != 1], run_time=0.4)
        rc = np.array([2.6, -0.35, 0])
        ring = VGroup(*[box(1.1, 0.5, f"CT{i + 1}", CH[i], 15).move_to(rc + 1.45 * np.array([np.cos(PI / 2 - i * PI / 2), np.sin(PI / 2 - i * PI / 2), 0])) for i in range(4)])
        arcs = VGroup(*[CurvedArrow(rc + 0.85 * (ring[i].get_center() - rc), rc + 0.85 * (ring[(i + 1) % 4].get_center() - rc), angle=-PI / 3, color=MUTED, stroke_width=2) for i in range(4)])
        pilot = glow_dot(WHITE, 0.08).move_to(ring[0])
        pl = T("öncü ONU · ICTP ile koordinasyon · 2 tur", 18, WHITE, BOLD).next_to(ring, DOWN, buff=0.3)
        self.play(FadeIn(ring), Create(arcs), FadeIn(pl), run_time=0.9)
        self.add(pilot)
        for t in range(8):
            self.play(pilot.animate.move_to(ring[(t + 1) % 4]), run_time=0.4)
        x1 = pill("Ranging_Time (X = 1): belirli bir λ çifti için EqD", GOLD, 18).next_to(pl, DOWN, buff=0.22)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(x1), run_time=0.5)
        self.remove(pilot)
        self.end(pad=0.05)

        self.beat("f9b")
        self.clear()
        sumc = VGroup(card("G.989.2", "mesafe = kayıp + dispersiyon", None, ACC, w=5.0, h=1.6, tsize=26, bsize=22),
                      card("G.989.3", "mesafe = zaman", None, "#A78BFA", w=5.0, h=1.6, tsize=26, bsize=22)).arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        both = T("doğru güçte ve doğru zamanda", 30, GOOD, BOLD).next_to(sumc, DOWN, buff=0.6)
        self.play(FadeIn(sumc[0], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(sumc[1], shift=UP * 0.2), run_time=0.6)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(both), run_time=0.6)
        self.end(pad=0.2)
        self.clear()
        self.drop_badge()
        self.save_timeline("ep02_p5C")


def chain(y=0.6):
    names = [("CT + WM", GOLD), ("kuplör", MUTED), ("VOA", MUTED), ("makara\n20/40 km", CH[1]), ("ayırıcı", FEED), ("ONU'lar", "#94A3B8")]
    g = VGroup(*[box(1.55, 0.8, n, c, 15) for n, c in names]).arrange(RIGHT, buff=0.42).move_to([0, y, 0])
    lines = VGroup(*[Line(a.get_right(), b.get_left(), color=FEED, stroke_width=3) for a, b in zip(g[:-1], g[1:])])
    return g, lines


class E2LabA(Act):
    HDR, MANIFEST, FIRST = HL, ML, True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Referans test ODN'i")
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Amaç: standardın sınırlarını yeniden yaratmak")
        goals = VGroup(card("Kayıp", "OPL_min … OPL_maks\nher sınıfın iki ucu", None, CH[1], w=3.9, h=1.7, tsize=24, bsize=19),
                       card("Yansıma", "ORL ≥ 32 dB\nayrık < −35 dB", None, WARN, w=3.9, h=1.7, tsize=24, bsize=19),
                       card("Mesafe", "20 / 40 km makara\ndiferansiyel kayıp ≤ 15 dB", None, GOLD, w=3.9, h=1.7, tsize=24, bsize=19)).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        sv = T("saha değil, sınırlar: tekrarlanabilir ve belgelenmiş", 22, GOOD, BOLD).next_to(goals, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in goals], lag_ratio=0.25), run_time=1.2)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(sv), run_time=0.5)
        self.end(pad=0.05)
        self.play(FadeOut(goals), FadeOut(sv), run_time=0.4)

        self.beat("g2")
        g, lines = chain()
        n = len(self.cues)
        self.play(FadeIn(g[0], shift=UP * 0.15), run_time=0.5)
        for k in range(1, 6):
            self.at(self.cues[min(n - 1, k + 1)] - 0.2 if n > 2 else k)
            self.play(Create(lines[k - 1]), FadeIn(g[k], shift=UP * 0.15), run_time=0.45)
        self.end(pad=0.05)

        self.beat("g2a")
        cg = DashedLine(g[1].get_left() + LEFT * 0.21 + DOWN * 0.8, g[1].get_left() + LEFT * 0.21 + UP * 0.8, color=ACC, stroke_width=2.5)
        cgt = T("S/R-CG", 16, ACC, BOLD).next_to(cg, UP, buff=0.05)
        tap = VGroup(Line(g[1].get_bottom(), g[1].get_bottom() + DOWN * 1.1, color=FEED, stroke_width=2), box(1.6, 0.55, "güç ölçer / OSA", GOOD, 14).next_to(g[1].get_bottom() + DOWN * 1.1, DOWN, buff=0))
        nt = pill("kuplör kaybı → bütçeye ve okumalara dahil", WARN, 18).to_edge(DOWN, buff=0.6)
        self.play(Create(cg), FadeIn(cgt), run_time=0.6)
        self.play(FadeIn(tap), run_time=0.6)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(nt), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g3")
        self.play(FadeOut(nt), FadeOut(tap), run_time=0.4)
        dc = np.array([g[2].get_x(), -1.5, 0])
        dial = VGroup(Circle(radius=0.55, color=GOLD, stroke_width=3).move_to(dc), Line(dc, dc + UP * 0.45, color=GOLD, stroke_width=4),
                      T("VOA", 14, GOLD, BOLD).next_to(dc + DOWN * 0.55, DOWN, buff=0.08))
        lmax = T("OPL_maks → hassasiyet testi", 19, CH[1], BOLD).next_to(dial, RIGHT, buff=0.4).shift(UP * 0.25)
        lmin = T("OPL_min → aşırı yük testi", 19, CH[3], BOLD).next_to(lmax, DOWN, buff=0.2, aligned_edge=LEFT)
        f = T("VOA = OPL_hedef − (makara + ayırıcı + kuplör + konnektörler)", 21, GOLD, BOLD).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(dial), run_time=0.4)
        self.play(Rotate(dial[1], -PI * 0.7, about_point=dial[0].get_center()), FadeIn(lmax), run_time=0.8)
        self.play(Rotate(dial[1], PI * 0.5, about_point=dial[0].get_center()), FadeIn(lmin), run_time=0.8)
        self.at(self.cues[2] - 0.3 if len(self.cues) > 2 else 6)
        self.play(Write(f), run_time=1.0)
        self.end(pad=0.05)

        self.beat("g4")
        self.clear(h)
        h = self.show_heading("Ekleme kaybı: iki yön, iki bant", h)
        ls = box(1.6, 0.7, "ışık kaynağı", GOLD, 16).move_to([-5.0, 0.8, 0])
        dut = box(3.0, 0.9, "referans ODN", ACC, 18).move_to([0, 0.8, 0])
        pm = box(1.6, 0.7, "güç ölçer", GOOD, 16).move_to([5.0, 0.8, 0])
        l1 = Line(ls.get_right(), dut.get_left(), color=FEED, stroke_width=3)
        l2 = Line(dut.get_right(), pm.get_left(), color=FEED, stroke_width=3)
        tb = table(["Bant", "Örnek ölçüm"], [["↑ 1524–1544 nm", "27,4 dB"], ["↓ 1596–1603 nm", "28,1 dB"]], [4.0, 3.0], size=21, hsize=18, row_h=0.6).move_to(DOWN * 1.3)
        tag = T("(örnek değerler)", 15, MUTED).next_to(tb, RIGHT, buff=0.2)
        self.play(FadeIn(VGroup(ls, dut, pm, l1, l2)), run_time=0.8)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(FadeIn(tb), FadeIn(tag), run_time=0.7)
        cal = pill("kalibrasyon dalga boyu = ölçülen bant", WARN, 18).to_edge(DOWN, buff=0.55)
        self.at(self.cues[-1] - 0.4)
        self.play(FadeIn(cal), run_time=0.5)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_labA")


class E2LabB(Act):
    HDR, MANIFEST, PREV_BADGE = HL, ML, "lab"

    def construct(self):
        self.beat("g5")
        h = self.show_heading("Geri dönüş kaybı ve yansıma")
        ax = Axes(x_range=[0, 25, 5], y_range=[0, 24, 5], x_length=8.0, y_length=3.2, axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-1.8, -0.4, 0])
        def trace(x):
            y = 14 - 0.25 * x
            for p, hgt in ((0.6, 10), (5, 4), (12, 5), (20.5, 8)):
                y += hgt * np.exp(-((x - p) / 0.08) ** 2)
            return y - (6 if x > 20.6 else 0)
        tr = ax.plot(trace, x_range=[0.1, 24, 0.01], color=CH[1], stroke_width=2.5)
        lab = VGroup(T("OTDR izi (temsili)", 15, MUTED).next_to(ax, UP, buff=0.05).align_to(ax, LEFT), T("mesafe (km)", 14, MUTED).next_to(ax.c2p(25, 0), DOWN, buff=0.08).shift(LEFT * 0.4))
        lims = VGroup(pill("ODN ORL ≥ 32 dB", ACC, 18), pill("tek konnektör < −35 dB", WARN, 18), pill("bakım λ: ITU-T L.313", GOLD, 18)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.8, 0.2, 0])
        self.play(Create(ax), FadeIn(lab), Create(tr), run_time=1.2)
        n = len(self.cues)
        for k, t0 in enumerate([self.cues[min(1, n - 1)], self.cues[min(2, n - 1)], self.cues[-2] if n > 2 else 6]):
            self.at(t0 - 0.2)
            self.play(FadeIn(lims[k], shift=LEFT * 0.15), run_time=0.45)
        self.play(self.set_src("G.989.2 §9.3.5 · Tablo 11-3"), run_time=0.3)
        self.end(pad=0.05)

        self.beat("g5a")
        self.clear(h)
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 10, 2], x_length=7.0, y_length=2.6, axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-2.4, 0.2, 0])
        ab = ax.plot(lambda x: 8.3 - 0.25 * x - (0.5 if x > 8 else 0), x_range=[0.1, 19.9, 0.05], color=CH[1], stroke_width=2.5)
        ba = ax.plot(lambda x: 7.9 - 0.25 * x - (-0.3 if x > 8 else 0), x_range=[0.1, 19.9, 0.05], color=CH[3], stroke_width=2.5)
        avg = ax.plot(lambda x: 8.1 - 0.25 * x - (0.1 if x > 8 else 0), x_range=[0.1, 19.9, 0.05], color=WHITE, stroke_width=3)
        lg = VGroup(T("A → B", 17, CH[1], BOLD), T("B → A", 17, CH[3], BOLD), T("ortalama → gerçek ek kaybı", 17, WHITE, BOLD), T("(temsili)", 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, RIGHT, buff=0.3)
        self.play(Create(ax), Create(ab), FadeIn(lg[0]), run_time=0.8)
        self.play(Create(ba), FadeIn(lg[1]), run_time=0.7)
        self.play(Create(avg), FadeIn(lg[2]), FadeIn(lg[3]), run_time=0.7)
        rr = pill("ayırıcı arkasındaki kollar: OTDR'de ayırt etmek zor → kol sonu referans yansıtıcılar", WARN, 18).to_edge(DOWN, buff=0.7)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(rr), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g6")
        self.clear()
        h = self.show_heading("Diferansiyel kayıp düzeneği", h if False else None)
        olt = box(1.4, 0.8, "OLT Rx", "#3B4A75", 16).move_to([-5.4, 0.3, 0])
        sp = splitter(0.3).move_to([-2.6, 0.3, 0])
        l0 = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=3)
        arms = VGroup()
        for k, (val, c, nm) in enumerate([("OPL_min", CH[1], "ONU 1"), ("OPL_maks", CH[3], "ONU 2")]):
            y = 1.3 - 2.0 * k
            att = box(1.6, 0.55, f"VOA · {val}", c, 14).move_to([0.6, y, 0])
            onu = box(1.3, 0.55, nm, c, 15).move_to([3.6, y, 0])
            arms.add(VGroup(Line(sp.get_right(), att.get_left(), color=FEED, stroke_width=2.5), att, Line(att.get_right(), onu.get_left(), color=FEED, stroke_width=2.5), onu))
        d = T("Δ = 15 dB → burst alıcı dinamik aralığı · Bölüm 8", 21, GOLD, BOLD).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(VGroup(olt, sp, l0)), LaggedStart(*[FadeIn(a) for a in arms], lag_ratio=0.3), run_time=1.2)
        self.at(self.cues[-2] - 0.3 if len(self.cues) > 2 else 5)
        self.play(FadeIn(d), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g7")
        self.clear()
        sc = scope(7.0, 2.2, [0.6, -0.6, 0])
        x0 = sc[0].get_left()[0] + 0.3
        yb = sc[0].get_bottom()[1] + 0.3
        b1 = Rectangle(width=2.0, height=1.2, stroke_width=0, fill_color=CH[1], fill_opacity=0.85).move_to([x0 + 1.0, yb + 0.6, 0])
        b2 = Rectangle(width=2.0, height=1.2, stroke_width=0, fill_color=CH[3], fill_opacity=0.85).move_to([x0 + 3.4, yb + 0.6, 0])
        g_ = T("koruma", 15, MUTED).move_to([x0 + 2.2, yb - 0.1, 0])
        lab = VGroup(T("0 km", 16, CH[1], BOLD).move_to(b1), T("20 km", 16, CH[3], BOLD).move_to(b2))
        top = T("iki uzunlukta fiber → ranging + EqD doğrulaması (osiloskop)", 21, TXT, BOLD).move_to(UP * 1.6)
        self.play(FadeIn(top), FadeIn(sc), run_time=0.7)
        self.play(FadeIn(b1, shift=RIGHT * 0.4), FadeIn(b2, shift=LEFT * 0.4), FadeIn(lab), FadeIn(g_), run_time=1.0)
        self.end(pad=0.05)

        self.beat("g7a")
        self.clear()
        tb = table(["İzleme parametresi (Ek II)", "Doğruluk", "Tekrarlanabilirlik"],
                   [["ONU alınan güç", "±3 dB", "±0,5 dB"], ["OLT alınan güç (burst ortalaması)", "±2 dB", "±0,5 dB"], ["ONU / OLT verici gücü", "±3 / ±2 dB", "±0,5 dB"]],
                   [5.6, 2.4, 3.0], size=21, hsize=18, row_h=0.6).move_to(UP * 0.4)
        self.play(FadeIn(tb), self.set_src("G.989.2 Ek II, Tablo II.1"), run_time=0.9)
        use = VGroup(pill("eğilim izleme için değerli", GOOD, 19), pill("sınıf belgelemek için kalibre ölçer gerekir", WARN, 19)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(use), run_time=0.6)
        self.end(pad=0.05)

        self.clear()
        self.save_timeline("ep02_labB")


class E2LabC(Act):
    HDR, MANIFEST, PREV_BADGE = HL, ML, "lab"

    def construct(self):
        h = None
        self.engineer_note("g8", [("1", "Test ODN'ini belgeleyin", "İki banttaki kayıp · ORL · konnektör tipi · fiber uzunluğu ve dispersiyonu.", 1),
                                  ("2", "Tartışmalı sonuç?", "İlk bakılacak yer test ODN'inin kendisidir.", 2)])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep02_labC")


class E2End(Act):
    HDR, MANIFEST, FIRST = HE, ME, True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 2'nin özeti")
        self.at(1.5)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["ODN: kanal bağlantı + besleme + dağıtım · G.652 · 20/40 km · ≤ 15 dB diferansiyel",
               "Dört sınıf N1 … E2: 15 dB genişlik, 2 dB aralık",
               "Bütçe: P_min − S ≥ OPL_maks + OPP — tablolar bu denklemle kapanır",
               "Dispersiyon ve yansıma ayrı sınırlar: ORL ≥ 32 dB, ayrık < −35 dB",
               "Mesafenin zaman yüzü: sessiz pencere, ranging, EqD"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 21, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        n = len(self.cues)
        self.at(self.cues[min(1, n - 1)])
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cues[-2] - 0.3 if n > 2 else 8)
        self.play(FadeIn(items[1], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        n = len(self.cues)
        for k, t0 in zip([2, 3, 4], [0.3, self.cues[min(3, n - 1)] if n > 3 else 5, self.cues[-2] if n > 2 else 9]):
            self.at(t0)
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("20 km fiber + 1:128 ayırıcı\n(Perde 2 varsayımları):\nhangi sınıf?", CH[0]),
            ("Yükselteçli OLT alıcısı,\nONU'nun en küçük gücünü\nkaç dB düşürür?", CH[1]),
            ("40 km diferansiyel mesafede\nSN toplama için önerilen\nsessiz pencere?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 3'ün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        n = len(self.cues)
        for k, t0 in enumerate([self.cues[min(1, n - 1)], self.cues[min(3, n - 1)] if n > 3 else 6, self.cues[min(5, n - 1)] if n > 5 else 10]):
            self.at(t0)
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cues[-1])
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T("Bölüm 3 · Renk Haritası", 54, TXT, BOLD),
                     T("dalga boyu planı · ızgaralar · birlikte çalışma · Raman", 22, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 0.9)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        X = lambda nm: -5.8 + (nm - 1260) / (1625 - 1260) * 11.6
        strip = Line([-5.8, -1.6, 0], [5.8, -1.6, 0], color=MUTED, stroke_width=2)
        bands = VGroup(*[Rectangle(width=X(b) - X(a), height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([(X(a) + X(b)) / 2, -1.38, 0])
                         for a, b, c in [(1260, 1280, LEGACY), (1290, 1330, LEGACY), (1480, 1500, LEGACY), (1524, 1544, "#A78BFA"), (1550, 1560, LEGACY), (1575, 1581, LEGACY), (1596, 1603, ACC), (1603, 1625, PINK)]])
        self.play(Create(strip), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bands], lag_ratio=0.1), run_time=1.2)
        self.end(pad=0.6)
        self.play(FadeOut(VGroup(nxt, strip, bands)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 2 · Işığın Yolu", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Google Gemini TTS — ses: Sadaltager", 22, ACC, BOLD),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep02_end")
