"""B01 · Perde 2 — Neden hız değil, renk?"""
from kit import *
from scipy.special import erfc

HDR2 = "BÖLÜM 1 · PERDE 2 — Neden hız değil, renk?"
MAN2 = "build/v4/ep01_p2/audio_proc/manifest.json"


def eye(center, w, h, sigma_ui, color, n=70, seed=1):
    """Eye diagram from a Gaussian-filtered NRZ stream; sigma_ui = pulse spread in unit intervals."""
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, n + 8)
    k = np.arange(-4, 5)
    t = np.linspace(0, 2, 120)
    traces = VGroup()
    for i in range(4, n + 4):
        y = np.zeros_like(t)
        for j in k:
            b = bits[i + j]
            # NRZ bit (rect over [j, j+1]) convolved with Gaussian sigma -> difference of erfc
            a0, a1 = (t - j) / (np.sqrt(2) * sigma_ui), (t - j - 1) / (np.sqrt(2) * sigma_ui)
            y += b * 0.5 * (erfc(-a0) - erfc(-a1)) * 0.5 + 0 * a1
        y = y * 2
        pts = [[center[0] - w / 2 + w * tt / 2, center[1] - h / 2 + h * yy, 0] for tt, yy in zip(t, np.clip(y, -0.1, 1.1))]
        traces.add(VMobject(stroke_color=color, stroke_width=1.2, stroke_opacity=0.35).set_points_smoothly(pts))
    frame = Rectangle(width=w, height=h * 1.25, stroke_color="#334155", stroke_width=1.5).move_to(center)
    return VGroup(frame, traces)


class P2A(Act):
    HDR, MANIFEST, FIRST = HDR2, MAN2, True

    def construct(self):
        self.beat("q1")
        tc = self.title_card("PERDE 2", "Neden hız değil, renk?")
        self.at(self.cues[3] - 0.3)
        self.to_header(tc)
        h = self.show_heading("Nesiller: aynı ağaç, daha hızlı ışık")
        xs = [-4.4, -0.6, 3.2]
        gens = [("GPON", "G.984", 2.5, 1.25), ("XG-PON", "G.987", 10, 2.5), ("XGS-PON", "G.9807.1", 10, 10)]
        base_y = -2.35
        axis = Line([-6.4, base_y, 0], [6.4, base_y, 0], color=LINE, stroke_width=2)
        names = VGroup(*[VGroup(T(n, 26, TXT, BOLD), T(s, 16, MUTED)).arrange(DOWN, buff=0.06).move_to([x, base_y - 0.55, 0])
                         for x, (n, s, _, _) in zip(xs, gens)])
        self.play(Create(axis), LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in names], lag_ratio=0.3), run_time=1.4)
        self.end(pad=0.05)

        # q2 — rate bars
        self.beat("q2")
        k = 0.30  # units per Gbit/s
        bars = VGroup()
        for x, (n, s, ds, us) in zip(xs, gens):
            d = Rectangle(width=0.6, height=ds * k, stroke_width=0, fill_color=WHITE, fill_opacity=0.85).move_to([x - 0.38, base_y + ds * k / 2, 0])
            u = Rectangle(width=0.6, height=us * k, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([x + 0.38, base_y + us * k / 2, 0])
            dl = T(f"↓ {str(ds).replace('.', ',')}", 18, WHITE, BOLD).next_to(d, UP, buff=0.08)
            ul = T(f"↑ {str(us).replace('.', ',')}", 18, GOLD, BOLD).next_to(u, UP, buff=0.08)
            bars.add(VGroup(d, u, dl, ul))
        unit = T("Gbit/s (nominal ~)", 16, MUTED).move_to([5.4, 2.25, 0])
        for i, t0 in enumerate([self.cues[1] - 0.3, self.cues[3] - 0.2, self.cues[5] - 0.2]):
            self.at(t0)
            b = bars[i]
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(b[2]), FadeIn(b[3]),
                      *([FadeIn(unit)] if i == 0 else []), run_time=0.9)
        self.end(pad=0.05)

        # q3 — single wavelength pair in every generation
        self.beat("q3")
        pairs = VGroup()
        for x in xs:
            p = VGroup(Dot(radius=0.11, color=WHITE), Dot(radius=0.11, color=GOLD)).arrange(RIGHT, buff=0.25)
            pairs.add(VGroup(p, T("1 λ çifti", 16, MUTED).next_to(p, DOWN, buff=0.08)).move_to([x, 2.15, 0]))
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in pairs], lag_ratio=0.25), run_time=1.2)
        self.at(self.cues[2] - 0.2)
        cap = pill("hızı artırmak = aynı ışığı daha hızlı modüle etmek", ACC, 20).move_to([0, 1.45, 0])
        self.play(FadeIn(cap, shift=UP * 0.15), *[Indicate(b[0], color=ACC, scale_factor=1.05) for b in bars], run_time=1.0)
        self.end(pad=0.05)

        # q4 — NG-PON2 target
        self.beat("q4")
        self.play(FadeOut(cap), FadeOut(pairs), run_time=0.4)
        q = self.quote("G.989.2 · Özet", "“…a nominal aggregate capacity of 40 Gbit/s in the downstream direction\nand 10 Gbit/s in the upstream direction…”",
                       "Aşağı yönde 40, yukarı yönde 10 Gbit/s nominal toplam kapasite").scale(0.8).to_edge(UP, buff=1.55)
        self.at(self.cues[1])
        self.play(FadeIn(q, shift=UP * 0.15), self.set_src("Kaynak: ITU-T G.989.2 (2019)/Amd.1 (2020), Özet"), run_time=0.8)
        self.play(*[g.animate.shift(LEFT * 1.0) for g in (names, bars)], run_time=0.6)
        x4 = 6.0 - 0.4
        n4 = VGroup(T("NG-PON2", 26, ACC, BOLD), T("G.989", 16, MUTED)).arrange(DOWN, buff=0.06).move_to([x4, base_y - 0.55, 0])
        d4 = DashedVMobject(Rectangle(width=0.7, height=40 * k * 0.25, color=ACC), num_dashes=36).move_to([x4, base_y + 40 * k * 0.25 / 2, 0])
        q4 = T("40 ?", 30, ACC, BOLD).next_to(d4, UP, buff=0.1)
        brk = T("(ölçek kırık)", 14, MUTED).next_to(d4, LEFT, buff=0.1)
        self.at(self.cues[5])
        self.play(FadeIn(n4), Create(d4), FadeIn(q4, scale=1.3), FadeIn(brk), run_time=1.2)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p2A")


class P2B(Act):
    HDR, MANIFEST, PREV_BADGE = HDR2, MAN2, None

    def construct(self):
        self.beat("q5")
        self.set_badge("fiz")
        h = self.show_heading("Duvar 1: kromatik dispersiyon")
        e10 = eye([-3.4, -0.4, 0], 4.2, 2.6, 0.18, CH[1], seed=2)
        e40 = eye([3.4, -0.4, 0], 4.2, 2.6, 0.62, WARN, seed=2)
        l10 = T("10 Gbit/s", 24, CH[1], BOLD).next_to(e10, UP, buff=0.15)
        l40 = T("40 Gbit/s · aynı fiber", 24, WARN, BOLD).next_to(e40, UP, buff=0.15)
        cap = T("(temsili göz diyagramları)", 15, MUTED).next_to(VGroup(e10, e40), DOWN, buff=0.15)
        self.at(self.cues[1])
        self.play(FadeIn(e10[0]), FadeIn(l10), LaggedStart(*[Create(t) for t in e10[1]], lag_ratio=0.01), run_time=1.6)
        self.play(FadeIn(e40[0]), FadeIn(l40), LaggedStart(*[Create(t) for t in e40[1]], lag_ratio=0.01), FadeIn(cap), run_time=1.6)
        f = T("L_disp ∝ 1 / ( |D| · B² )", 34, TXT, BOLD).to_edge(DOWN, buff=0.75)
        self.at(self.cues[3] - 0.3)
        self.play(Write(f), run_time=1.0)
        r = pill("B × 4   ⇒   L ÷ 16", GOLD, 24).next_to(f, RIGHT, buff=0.5)
        self.at(self.cues[4])
        self.play(FadeIn(r, scale=1.2), run_time=0.6)
        self.end(pad=0.1)

        # q6 — reach numbers + dispersion vs wavelength
        self.beat("q6")
        self.clear(h)
        bx = -6.2
        b10 = Rectangle(width=6.0, height=0.55, stroke_width=0, fill_color=CH[1], fill_opacity=0.9).move_to([bx + 3.0, 1.2, 0])
        b40 = Rectangle(width=0.4, height=0.55, stroke_width=0, fill_color=WARN, fill_opacity=0.9).move_to([bx + 0.2, 0.3, 0])
        t10 = T("10 Gbit/s  ≈ 60 km", 22, CH[1], BOLD).next_to(b10, RIGHT, buff=0.2)
        t40 = T("40 Gbit/s  ≈ 4 km", 22, WARN, BOLD).next_to(b40, RIGHT, buff=0.2)
        rule = T("kaba kural · chirpsiz NRZ · G.652 fiber · C bandı", 17, MUTED).next_to(b10, UP, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(rule), GrowFromEdge(b10, LEFT), FadeIn(t10), run_time=0.9)
        self.at(self.cues[2] - 0.2)
        self.play(GrowFromEdge(b40, LEFT), FadeIn(t40), run_time=0.7)
        ax = Axes(x_range=[1500, 1630, 25], y_range=[10, 24, 2], x_length=6.0, y_length=2.4,
                  axis_config={"color": MUTED, "include_tip": False, "include_ticks": False, "stroke_width": 2}).move_to([2.6, -2.0, 0])
        D = lambda l: 0.092 / 4 * (l - 1310 ** 4 / l ** 3)
        curve = ax.plot(D, x_range=[1500, 1630], color=TXT, stroke_width=3)
        band = Rectangle(width=ax.c2p(1603, 0)[0] - ax.c2p(1596, 0)[0], height=2.4, stroke_width=0, fill_color=ACC, fill_opacity=0.25).move_to([ax.c2p(1599.5, 0)[0], ax.get_center()[1], 0])
        cband = Rectangle(width=ax.c2p(1565, 0)[0] - ax.c2p(1530, 0)[0], height=2.4, stroke_width=0, fill_color=LEGACY, fill_opacity=0.2).move_to([ax.c2p(1547.5, 0)[0], ax.get_center()[1], 0])
        labs = VGroup(T("1500", 14, MUTED).next_to(ax.c2p(1500, 10), DOWN, buff=0.1), T("1550", 14, MUTED).next_to(ax.c2p(1550, 10), DOWN, buff=0.1),
                      T("1600", 14, MUTED).next_to(ax.c2p(1600, 10), DOWN, buff=0.1), T("nm", 14, MUTED).next_to(ax.c2p(1630, 10), DOWN, buff=0.1),
                      T("D (ps/nm/km)", 15, MUTED).next_to(ax, UP, buff=0.05).align_to(ax, LEFT),
                      T("C bandı", 15, MUTED).next_to(cband, UP, buff=0.04), T("NG-PON2 ↓", 15, ACC, BOLD).next_to(band, UP, buff=0.04))
        d1550 = VGroup(Dot(ax.c2p(1550, D(1550)), color=WHITE, radius=0.06), T(f"≈{D(1550):.0f}", 15, WHITE).next_to(ax.c2p(1550, D(1550)), DR, buff=0.05))
        d1600 = VGroup(Dot(ax.c2p(1600, D(1600)), color=ACC, radius=0.06), T(f"≈{D(1600):.0f}", 15, ACC, BOLD).next_to(ax.c2p(1600, D(1600)), UL, buff=0.05))
        self.at(self.cues[3] - 0.2)
        self.play(Create(ax), FadeIn(cband), FadeIn(band), Create(curve), FadeIn(labs), run_time=1.2)
        self.play(FadeIn(d1550), FadeIn(d1600, scale=1.3), run_time=0.6)
        self.end(pad=0.1)

        # q7 — receiver sensitivity
        self.beat("q7")
        self.clear()
        h2 = self.show_heading("Duvar 2: alıcı hassasiyeti")
        ax2 = Axes(x_range=[-0.6, 1.6, 0.5], y_range=[0, 4.2, 1], x_length=6.0, y_length=3.0,
                   axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-2.6, -0.6, 0])
        def pdfs(sig, color):
            g = lambda m: (lambda x: np.exp(-((x - m) / sig) ** 2 / 2) / (sig * np.sqrt(2 * np.pi)))
            return VGroup(ax2.plot(g(0), x_range=[-0.6, 1.6], color=color, stroke_width=3), ax2.plot(g(1), x_range=[-0.6, 1.6], color=color, stroke_width=3))
        p10, p40 = pdfs(0.12, CH[1]), pdfs(0.24, WARN)
        thr = DashedLine(ax2.c2p(0.5, 0), ax2.c2p(0.5, 4.2), color=WHITE, stroke_width=2)
        lab = VGroup(T("“0”", 18, MUTED).next_to(ax2.c2p(0, 0), DOWN, buff=0.1), T("“1”", 18, MUTED).next_to(ax2.c2p(1, 0), DOWN, buff=0.1),
                     T("karar eşiği", 15, WHITE).next_to(thr, UP, buff=0.05))
        k10 = T("10G: dar gürültü", 18, CH[1], BOLD).move_to([-2.6, 1.6, 0]).shift(LEFT * 1.5)
        k40 = T("40G: 4× bant genişliği → geniş gürültü", 18, WARN, BOLD).next_to(k10, RIGHT, buff=0.4)
        self.play(Create(ax2), FadeIn(lab), Create(thr), Create(p10), FadeIn(k10), run_time=1.0)
        self.at(self.cues[1])
        self.play(TransformFromCopy(p10, p40), FadeIn(k40), run_time=1.2)
        pen = card("Aynı BER için", "kabaca +3 … 6 dB daha fazla güç", "kaba kural", WARN, w=5.2, h=1.6, tsize=22)
        pen.move_to([3.85, 0.4, 0])
        bud = card("PON bütçeleri", "29 … 35 dB (N1 … E2)\nher desibel değerli", "G.989.2 Tablo 6-1", ACC, w=5.2, h=1.8, tsize=22).next_to(pen, DOWN, buff=0.3)
        self.at(self.cues[2])
        self.play(FadeIn(pen, shift=LEFT * 0.2), run_time=0.6)
        self.at(self.cues[3])
        self.play(FadeIn(bud, shift=LEFT * 0.2), run_time=0.6)
        self.end(pad=0.1)

        # q8 — cost
        self.beat("q8")
        self.clear()
        h3 = self.show_heading("Duvar 3: maliyet")
        items = VGroup(*[card(t, b, None, WARN, w=3.7, h=1.6, tsize=22, bsize=18) for t, b in
                         [("40G burst modlu alıcı", "OLT'de, her kanal için"), ("40G SerDes", "OLT ve ONU elektroniği"), ("× her ONU", "evdeki her cihazda")]]
                       ).arrange(RIGHT, buff=0.4).move_to(UP * 0.4)
        houses = VGroup(*[VGroup(Polygon([-0.2, 0, 0], [0.2, 0, 0], [0.2, 0.25, 0], [0, 0.42, 0], [-0.2, 0.25, 0], color=MUTED, stroke_width=2))
                          for _ in range(16)]).arrange(RIGHT, buff=0.18).move_to(DOWN * 1.8)
        tag = T("2013 civarı teknolojiyle ekonomik değil", 22, WARN, BOLD).next_to(houses, DOWN, buff=0.35)
        for i, t0 in enumerate([self.cues[1] - 0.2, self.cues[2] - 0.2, self.cues[2] + 1.2]):
            self.at(t0)
            self.play(FadeIn(items[i], shift=UP * 0.2), *([LaggedStart(*[FadeIn(hh) for hh in houses], lag_ratio=0.05)] if i == 2 else []), run_time=0.7)
        self.at(self.cues[3])
        self.play(FadeIn(tag), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p2B")


class P2C(Act):
    HDR, MANIFEST, PREV_BADGE = HDR2, MAN2, "fiz"

    def construct(self):
        self.beat("q9")
        h = self.show_heading("Cevap: renk sayısını artır")
        ax = Line([-5.5, -1.6, 0], [5.5, -1.6, 0], color=MUTED, stroke_width=2)
        wide = FunctionGraph(lambda x: -1.6 + 3.0 * np.exp(-(x / 1.4) ** 2), x_range=[-4.5, 4.5], color=WHITE, stroke_width=4)
        wl = T("1 × 40 Gbit/s", 26, WHITE, BOLD).move_to([0, 1.8, 0])
        self.play(Create(ax), Create(wide), FadeIn(wl), run_time=1.0)
        cs = [-3.3, -1.1, 1.1, 3.3]
        narrow = VGroup(*[FunctionGraph(lambda x, c=c: -1.6 + 2.6 * np.exp(-((x - c) / 0.35) ** 2), x_range=[c - 1.4, c + 1.4], color=CH[i], stroke_width=4)
                          for i, c in enumerate(cs)])
        nl = VGroup(*[T(f"λ{i + 1} · 10G", 20, CH[i], BOLD).move_to([c, 1.35, 0]) for i, c in enumerate(cs)])
        tot = T("4 × 10 Gbit/s = 40 Gbit/s ↓", 30, ACC, BOLD).move_to([0, 2.15, 0])
        self.at(self.cues[2])
        self.play(ReplacementTransform(wide, narrow), FadeOut(wl), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in nl], lag_ratio=0.2), run_time=1.0)
        self.at(self.cues[5])
        self.play(Write(tot), run_time=0.9)
        mat = pill("her kanal: olgun 10G teknolojisi (XG-PON / XGS-PON bileşenleri)", MUTED, 18).to_edge(DOWN, buff=0.7)
        self.at(self.cues[6])
        self.play(FadeIn(mat, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.1)

        # q10 — TWDM grid
        self.beat("q10")
        self.clear(h)
        h = self.show_heading("TWDM: zaman ve dalga boyu bölmeli çoklama", h)
        x0, y0, cw, rh = -4.2, 1.3, 0.78, 0.82
        rows = VGroup()
        rng = np.random.default_rng(5)
        for r in range(4):
            lab = T(f"λ{r + 1}", 24, CH[r], BOLD).move_to([x0 - 0.6, y0 - r * rh, 0])
            cells = VGroup()
            for c in range(12):
                onu = rng.integers(0, 4)
                cells.add(Rectangle(width=cw - 0.06, height=rh - 0.12, stroke_width=0, fill_color=interpolate_color(ManimColor(CH[r]), ManimColor(BG), 0.15 + 0.2 * onu),
                                    fill_opacity=1).move_to([x0 + cw / 2 + c * cw, y0 - r * rh, 0]))
            rows.add(VGroup(lab, cells))
        tax = Arrow([x0, y0 - 3.6 * rh, 0], [x0 + 12 * cw + 0.3, y0 - 3.6 * rh, 0], buff=0, color=MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.03)
        tl = T("zaman →  (her kanalın içinde TDMA)", 18, MUTED).next_to(tax, DOWN, buff=0.1)
        ll = T("dalga boyu ↓  (kanallar)", 18, MUTED).rotate(PI / 2).next_to(rows, LEFT, buff=0.6)
        self.at(self.cues[2] - 0.2)
        self.play(LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.2) for r in rows], lag_ratio=0.2), FadeIn(ll), run_time=1.0)
        self.at(self.cues[3] - 0.2)
        self.play(Create(tax), FadeIn(tl), LaggedStart(*[LaggedStart(*[FadeIn(c) for c in r[1]], lag_ratio=0.08) for r in rows], lag_ratio=0.1),
                  run_time=2.4)
        self.end(pad=0.1)

        # q11 + q11a — channel count and capacity
        self.beat("q11")
        self.clear(h)
        h = self.show_heading("Kanal sayısı ve kapasite", h)
        slots = VGroup()
        for i in range(8):
            c = CH[i % 4]
            r = RoundedRectangle(corner_radius=0.1, width=1.25, height=1.4, stroke_color=c if i < 4 else LINE, stroke_width=3,
                                 fill_color=c if i < 4 else BG, fill_opacity=0.35 if i < 4 else 0)
            if i >= 4:
                r = DashedVMobject(r, num_dashes=30)
            slots.add(VGroup(r, T(f"CT{i + 1}", 20, TXT if i < 4 else MUTED, BOLD).move_to(r)))
        slots.arrange(RIGHT, buff=0.22).move_to(UP * 0.6)
        tags = VGroup(T("zorunlu: en az 4", 20, ACC, BOLD).next_to(slots[:4], DOWN, buff=0.2),
                      T("isteğe bağlı: 8'e kadar", 20, MUTED, BOLD).next_to(slots[4:], DOWN, buff=0.2))
        self.play(LaggedStart(*[FadeIn(s, scale=0.9) for s in slots[:4]], lag_ratio=0.15), FadeIn(tags[0]),
                  self.set_src("G.989.2 §11.1 — en az 4, isteğe bağlı 8 TWDM kanalı"), run_time=1.0)
        self.play(LaggedStart(*[Create(s[0]) for s in slots[4:]], lag_ratio=0.15), FadeIn(VGroup(*[s[1] for s in slots[4:]])), FadeIn(tags[1]), run_time=1.0)
        cap = T("8 × 10 Gbit/s simetrik  →  80 Gbit/s ↓", 28, GOLD, BOLD).move_to(DOWN * 1.6)
        self.at(self.cues[1])
        self.play(*[s[0].animate.set_stroke(color=CH[i % 4]) for i, s in enumerate(slots[4:])], Write(cap), run_time=1.2)
        self.end(pad=0.1)
        self.beat("q11a")
        us = T("Temel yapılandırma ↑: 4 × 2,5 Gbit/s = 10 Gbit/s  →  nominal hedef", 24, ACC, BOLD).move_to(DOWN * 2.5)
        self.play(FadeIn(us, shift=UP * 0.15), run_time=0.8)
        self.at(self.cues[2])
        self.play(Indicate(us, color=ACC, scale_factor=1.04), run_time=0.8)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p2C")


class P2D(Act):
    HDR, MANIFEST, PREV_BADGE = HDR2, MAN2, "fiz"

    def construct(self):
        # q12 — pay as you grow
        self.beat("q12")
        h = self.show_heading("Renk eklemenin diğer kazançları")
        olt = RoundedRectangle(corner_radius=0.14, width=2.6, height=4.0, stroke_color="#3B4A75", stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-5.0, -0.6, 0])
        ot = T("OLT", 22, TXT, BOLD).next_to(olt.get_top(), DOWN, buff=0.15)
        cts = VGroup(*[box(2.1, 0.6, f"CT{i + 1}", LINE, 18).move_to([-5.0, 0.6 - i * 0.8, 0]) for i in range(4)])
        sp = splitter(0.35).move_to([0.6, -0.6, 0])
        feed = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=4)
        onus = VGroup(*[box(1.4, 0.5, "ONU", "#94A3B8", 16).move_to([4.6, 1.4 - i * 0.68, 0]) for i in range(7)])
        drops = VGroup(*[Line(sp.get_right(), o.get_left(), color="#94A3B8", stroke_width=1.8) for o in onus])
        self.play(FadeIn(olt), FadeIn(ot), FadeIn(cts), Create(feed), FadeIn(sp), Create(drops), FadeIn(onus), run_time=1.2)
        self.at(self.cues[3] - 0.2)
        self.play(cts[0][0].animate.set_stroke(CH[0]).set_fill(CH[0], opacity=0.35), *[o[0].animate.set_stroke(CH[0]) for o in onus], run_time=0.6)
        self.at(self.cues[4])
        for i in range(1, 4):
            self.play(cts[i][0].animate.set_stroke(CH[i]).set_fill(CH[i], opacity=0.35),
                      *[onus[j][0].animate.set_stroke(CH[i]) for j in range(7) if j % 4 == i], run_time=0.55)
        lock = pill("ONU donanımı aynı kalır", GOOD, 20).next_to(onus, DOWN, buff=0.3)
        self.at(self.cues[5])
        self.play(FadeIn(lock, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.1)

        # q13 — load balancing, protection, sharing
        self.beat("q13")
        self.clear(h)
        panels = VGroup(*[RoundedRectangle(corner_radius=0.16, width=4.0, height=4.3, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
                          for c in (CH[1], WARN, GOLD)]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.55)
        titles = VGroup(*[T(t, 22, c, BOLD).next_to(p.get_top(), DOWN, buff=0.2) for t, c, p in
                          zip(["Yük dengeleme", "Koruma", "Paylaşım"], [CH[1], WARN, GOLD], panels)])
        # 1) load balancing: ONU moves from λ1 to λ2
        p0 = panels[0].get_center()
        l1 = VGroup(*[Rectangle(width=0.32, height=0.32, stroke_width=0, fill_color=CH[0], fill_opacity=0.9) for _ in range(6)]).arrange(RIGHT, buff=0.08).move_to(p0 + UP * 0.5)
        l2 = VGroup(*[Rectangle(width=0.32, height=0.32, stroke_width=0, fill_color=CH[1], fill_opacity=0.9) for _ in range(2)]).arrange(RIGHT, buff=0.08).move_to(p0 + DOWN * 0.5).align_to(l1, LEFT)
        ll = VGroup(T("λ1 dolu", 16, CH[0]).next_to(l1, UP, buff=0.08), T("λ2", 16, CH[1]).next_to(l2, UP, buff=0.08).align_to(l2, LEFT))
        # 2) protection
        p1 = panels[1].get_center()
        ctA = box(1.3, 0.5, "CT1", CH[0], 16).move_to(p1 + UP * 0.6 + LEFT * 0.9)
        ctB = box(1.3, 0.5, "CT2", CH[1], 16).move_to(p1 + DOWN * 0.4 + LEFT * 0.9)
        on = VGroup(*[box(0.9, 0.42, "ONU", CH[0], 13).move_to(p1 + RIGHT * 1.1 + UP * (0.7 - 0.55 * i)) for i in range(3)])
        cx = Cross(Square(0.5), stroke_color=WARN, stroke_width=6).move_to(ctA)
        # 3) sharing
        p2 = panels[2].get_center()
        share = VGroup(*[VGroup(Dot(radius=0.1, color=CH[i]), T(s, 18, TXT)).arrange(RIGHT, buff=0.2) for i, s in
                         enumerate(["λ1 · konut", "λ2 · kurumsal", "λ3 · mobil şebeke", "λ4 · ikinci operatör"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(p2 + DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.15), FadeIn(titles), run_time=0.8)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(ll), run_time=0.5)
        self.at(self.cues[2])
        self.play(l1[-1].animate.next_to(l2, RIGHT, buff=0.08).set_fill(CH[1]), l1[-2].animate.next_to(l2, RIGHT, buff=0.48).set_fill(CH[1]), run_time=1.0)
        self.at(self.cues[3])
        self.play(FadeIn(ctA), FadeIn(ctB), FadeIn(on), run_time=0.6)
        self.at(self.cues[4] + 0.6)
        self.play(Create(cx), run_time=0.5)
        self.play(*[o[0].animate.set_stroke(CH[1]) for o in on], run_time=0.8)
        self.at(self.cues[6])
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in share], lag_ratio=0.25), run_time=1.4)
        self.end(pad=0.1)

        # q14 — the price: tunable ONU
        self.beat("q14")
        self.clear(h)
        h2 = self.show_heading("Bedel: ayarlanabilir ONU", h)
        onu = RoundedRectangle(corner_radius=0.2, width=7.4, height=3.6, stroke_color=TXT, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 0.6)
        ot = T("ONU", 28, TXT, BOLD).next_to(onu.get_top(), DOWN, buff=0.15)
        tx = RoundedRectangle(corner_radius=0.12, width=3.2, height=2.2, stroke_color=GOLD, stroke_width=2.5).move_to(onu.get_center() + LEFT * 1.75 + DOWN * 0.25)
        rx = RoundedRectangle(corner_radius=0.12, width=3.2, height=2.2, stroke_color=CH[1], stroke_width=2.5).move_to(onu.get_center() + RIGHT * 1.75 + DOWN * 0.25)
        txt_ = T("ayarlanabilir verici", 18, GOLD, BOLD).next_to(tx.get_top(), DOWN, buff=0.1)
        rxt = T("ayarlanabilir alıcı", 18, CH[1], BOLD).next_to(rx.get_top(), DOWN, buff=0.1)
        def grid(c, col):
            xs = [c[0] - 1.05 + 0.7 * i for i in range(4)]
            return VGroup(*[Line([x, c[1] - 0.65, 0], [x, c[1] + 0.25, 0], color=CH[i], stroke_width=2) for i, x in enumerate(xs)]), xs
        gt, xt = grid(tx.get_center(), GOLD)
        gr, xr = grid(rx.get_center(), CH[1])
        pk = ValueTracker(0)
        laser = always_redraw(lambda: FunctionGraph(lambda x: tx.get_center()[1] - 0.65 + 0.85 * np.exp(-((x - (xt[0] + 0.7 * pk.get_value())) / 0.06) ** 2),
                                                    x_range=[xt[0] + 0.7 * pk.get_value() - 0.25, xt[0] + 0.7 * pk.get_value() + 0.25], color=WHITE, stroke_width=3))
        flt = always_redraw(lambda: Rectangle(width=0.36, height=0.95, stroke_color=WHITE, stroke_width=2, fill_color=WHITE, fill_opacity=0.12)
                            .move_to([xr[0] + 0.7 * pk.get_value(), rx.get_center()[1] - 0.2, 0]))
        self.play(FadeIn(onu), FadeIn(ot), run_time=0.6)
        self.at(self.cues[1])
        self.play(FadeIn(tx), FadeIn(rx), FadeIn(txt_), FadeIn(rxt), FadeIn(gt), FadeIn(gr), run_time=0.7)
        self.add(laser, flt)
        self.play(pk.animate.set_value(3), run_time=2.0, rate_func=rate_functions.there_and_back_with_pause)
        q = T("§6: “Each ONU … is equipped with a tunable transmitter and a tunable receiver.”", 18, MUTED, slant=ITALIC).next_to(onu, UP, buff=0.2)
        self.play(FadeIn(q), self.set_src("G.989.2 §6"), run_time=0.6)
        self.at(self.cues[4])
        cost = pill("en zor problem · en büyük maliyet kalemi", WARN, 22).next_to(onu, DOWN, buff=0.25)
        self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.6)
        self.play(pk.animate.set_value(2), run_time=1.0)
        self.end(pad=0.15)
        laser.clear_updaters(); flt.clear_updaters()
        self.clear()
        self.save_timeline("ep01_p2D")


class P2E(Act):
    HDR, MANIFEST, PREV_BADGE = HDR2, MAN2, "fiz"

    def construct(self):
        self.beat("q15")
        h = self.show_heading("İkinci bileşen: PtP WDM")
        olt = box(1.6, 3.0, None, "#3B4A75").move_to([-5.2, -0.5, 0])
        ot = T("OLT", 22, TXT, BOLD).next_to(olt.get_top(), DOWN, buff=0.15)
        tw = box(1.3, 0.5, "TWDM", CH[0], 15).move_to(olt.get_center() + UP * 0.35)
        pt = box(1.3, 0.5, "PtP", PINK, 15).move_to(olt.get_center() + DOWN * 0.55)
        sp = splitter(0.35).move_to([0.2, -0.5, 0])
        feed = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=4)
        onus = VGroup(*[box(1.6, 0.52, "ONU", CH[0] if i != 3 else PINK, 15).move_to([4.6, 1.3 - i * 0.72, 0]) for i in range(5)])
        drops = VGroup(*[Line(sp.get_right(), o.get_left(), color="#94A3B8", stroke_width=1.8) for o in onus])
        self.play(FadeIn(olt), FadeIn(ot), FadeIn(tw), FadeIn(pt), Create(feed), FadeIn(sp), Create(drops), FadeIn(onus), run_time=1.2)
        self.at(self.cues[2])
        path = VMobject().set_points_as_corners([pt.get_right(), sp.get_center(), onus[3].get_left()])
        ded = VMobject(color=PINK, stroke_width=6).set_points_as_corners([pt.get_right(), [olt.get_right()[0], pt.get_y(), 0], olt.get_right() + DOWN * 0.05,
                                                                        sp.get_center(), onus[3].get_left()])
        self.play(Create(ded), run_time=1.2)
        labs = VGroup(T("TWDM: λ çifti zamanla paylaşılır", 18, CH[0], BOLD), T("PtP WDM: λ çifti tek ONU'ya ayrılır", 18, PINK, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        labs.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(labs), run_time=0.6)
        self.at(self.cues[4] - 0.2)
        v = pill("sanal noktadan noktaya bağlantı", PINK, 20).move_to([1.6, -2.2, 0])
        self.play(FadeIn(v, shift=UP * 0.1), Indicate(ded, color=WHITE, scale_factor=1.0), run_time=0.9)
        self.end(pad=0.1)

        # q16 — services, channel count
        self.beat("q16")
        self.clear(h)
        cards = VGroup(card("Kurumsal hat", "garanti edilmiş, şeffaf kanal", None, PINK, w=4.6, h=1.6, tsize=24),
                       card("Mobil şebeke bağlantısı", "baz istasyonu taşıma", None, PINK, w=4.6, h=1.6, tsize=24)).arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        cnt = pill("G.989.2 §6: en az 4 PtP WDM kanalı · üst sınır tanımlı değil", GOLD, 20).move_to(DOWN * 1.2)
        nxt = T("→ Bölüm 9: Özel Hat", 22, ACC, BOLD).move_to(DOWN * 2.2)
        self.at(self.cues[1] - 0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), run_time=1.0)
        self.at(self.cues[3])
        self.play(FadeIn(cnt), self.set_src("G.989.2 §6, Ek A"), run_time=0.6)
        self.at(self.cues[4])
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        # q17 — engineer's note
        self.engineer_note("q17", [("1", "Kaba kurallar tasarım değildir",
                                    "60 km / 4 km ve +3…6 dB yalnızca büyüklük mertebesi verir.\nTasarım için verici chirp'i, fiber tipi ve alıcı ölçülmelidir.", 1),
                                   ("2", "Ama mesaj nettir",
                                    "4× hız → menzil ÷16, bütçe −3…6 dB.\nNG-PON2 duvara çarpmak yerine yanından geçti: renk ekledi.", 3)])
        # q18 — bridge
        self.beat("q18")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bu kadar renk, kanal ve ayarlanabilir ONU\nstandartta nasıl organize edilmiş?")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep01_p2E")
