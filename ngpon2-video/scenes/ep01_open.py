"""B01 — 'Bu bölümde' opening summary (precedes the series intro)."""
from lib import *

EP = SERIES["episodes"][0]
AGENDA = ["PON'un özü: yayın ve burst", "Neden hız değil, renk?", "G.989 ailesi: PMD ↔ TC sınırı",
          "Referans mimari ve ölçüm noktaları", "Test tezgâhı"]
PX, PY = 3.4, -0.45  # teaser panel centre


class Ep01Open(Narrated):
    MANIFEST = "build/ep01_open/audio_proc/manifest.json"

    def construct(self):
        # ── o1: title + agenda ─────────────────────────────────────────
        self.beat("o1")
        tag = T(f"BÖLÜM {EP['n']} · {EP['title'].upper()}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup()
        for i, s in enumerate(AGENDA):
            num = T(f"{i + 1:02d}", 22, MUTED, BOLD)
            txt = T(s, 23, TXT, MEDIUM)
            items.add(VGroup(num, txt).arrange(RIGHT, buff=0.3))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=7.0, height=6.0, stroke_color=LINE, stroke_width=1.5,
                                 fill_color="#0C1324", fill_opacity=1).move_to([PX, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.at(self.cues[2] + 0.2)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel),
                  run_time=1.8)
        self.play(items.animate.set_opacity(0.4), run_time=0.4)
        self.end(pad=0.05)
        self.items, self.bar, self.cur = items, bar, None

        self.o2_pon()
        self.o3_colour()
        self.o4_layers()
        self.o5_arch()
        self.o6_bench()
        self.save_timeline("ep01_open")

    def focus(self, k, teaser_in):
        it = self.items[k]
        anims = [it.animate.set_opacity(1), self.items[k][0].animate.set_color(ACC)]
        if k:
            anims += [self.items[k - 1].animate.set_opacity(0.4), self.items[k - 1][0].animate.set_color(MUTED)]
        tgt = self.bar.copy().next_to(it, LEFT, buff=0.22)
        anims.append(FadeIn(tgt) if k == 0 else Transform(self.bar, tgt))
        if k == 0:
            self.bar = tgt
        if self.cur is not None:
            anims.append(FadeOut(self.cur, shift=LEFT * 0.3))
        self.play(*anims, run_time=0.5)
        self.cur = teaser_in

    # ── o2: PON essence — broadcast down, TDMA bursts up ─────────────────
    def o2_pon(self):
        self.beat("o2")
        olt = box(1.1, 0.95, "OLT", "#3B4A75", 22).move_to([PX - 2.75, PY, 0])
        sp = Triangle(color="#CBD5E1", fill_color=PANEL, fill_opacity=1, stroke_width=2).rotate(-PI / 2).scale(0.32)
        sp.move_to([PX + 0.95, PY, 0])
        trunk = Line(olt.get_right(), sp.get_left(), color="#CBD5E1", stroke_width=4)
        ys = [PY + 1.65 - k * 1.1 for k in range(4)]
        onus = VGroup(*[box(1.1, 0.55, "ONU", CH[k], 17).move_to([PX + 2.75, y, 0]) for k, y in enumerate(ys)])
        drops = VGroup(*[Line(sp.get_right(), o.get_left(), color="#94A3B8", stroke_width=2) for o in onus])
        lab_f = T("tek fiber", 17, MUTED).next_to(trunk, UP, buff=0.1).align_to(trunk, LEFT).shift(RIGHT * 0.1)
        lab_s = T("pasif ayırıcı", 17, MUTED).next_to(sp, UP, buff=0.35).shift(LEFT * 0.55)
        self.focus(0, VGroup())
        self.play(FadeIn(olt, shift=RIGHT * 0.2), run_time=0.5)
        self.at(self.cues[1])
        self.play(Create(trunk), FadeIn(lab_f), run_time=0.7)
        self.at(self.cues[2])
        self.play(FadeIn(sp), FadeIn(lab_s), LaggedStart(*[Create(d) for d in drops], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(o, shift=LEFT * 0.2) for o in onus], lag_ratio=0.12), run_time=1.2)
        # downstream: one frame carrying data for everybody, copied to every ONU
        self.at(self.cues[3] - 0.1)
        ds_lab = T("↓ yayın", 18, TXT, SEMIBOLD).next_to(trunk, UP, buff=0.1).align_to(trunk, RIGHT).shift(LEFT * 0.1)
        frame = VGroup(*[Square(0.16, stroke_width=0, fill_color=CH[k], fill_opacity=1) for k in range(4)]
                       ).arrange(RIGHT, buff=0.03).move_to(trunk.get_start())
        self.play(FadeIn(ds_lab), MoveAlongPath(frame, trunk), run_time=0.9, rate_func=linear)
        copies = [frame.copy() for _ in range(4)]
        self.remove(frame)
        self.play(*[MoveAlongPath(c, d) for c, d in zip(copies, drops)], run_time=0.6, rate_func=linear)
        self.play(*[c.animate.next_to(o, LEFT, buff=0.08).set_opacity(0.25) for c, o in zip(copies, onus)],
                  *[copies[k][k].animate.set_opacity(1) for k in range(4)], run_time=0.35)
        # upstream: each ONU's burst slots into its own time window
        self.at(self.cues[4])
        us_lab = T("↑ sıralı burst'ler (TDMA)", 18, TXT, SEMIBOLD).next_to(trunk, DOWN, buff=0.2)
        bursts = [Rectangle(width=0.42, height=0.16, stroke_width=0, fill_color=CH[k], fill_opacity=1).move_to(o.get_left())
                  for k, o in enumerate(onus)]
        back = [Line(o.get_left(), sp.get_right()) for o in onus]
        self.play(FadeOut(VGroup(*copies)), FadeIn(us_lab), run_time=0.3)
        tr_rev = Line(sp.get_left(), olt.get_right())
        self.play(LaggedStart(*[Succession(MoveAlongPath(b, l, rate_func=linear, run_time=0.45),
                                           MoveAlongPath(b, tr_rev, rate_func=linear, run_time=0.8))
                                for b, l in zip(bursts, back)], lag_ratio=0.32), run_time=2.0)
        self.remove(*bursts)
        self.cur = VGroup(olt, sp, trunk, onus, drops, lab_f, lab_s, ds_lab, us_lab)
        self.end(pad=0.05)

    # ── o3: why add colours instead of speeding up one wavelength ─────────
    def o3_colour(self):
        self.beat("o3")
        evo = VGroup(pill("GPON  2,5G", LEGACY, 18), T("→", 22, MUTED), pill("XG-PON  10G", LEGACY, 18),
                     T("→", 22, MUTED), pill("NG-PON2  ?", ACC, 18)).arrange(RIGHT, buff=0.18).move_to([PX, PY + 2.25, 0])

        def spectrum(y, peaks, width, colors, label, lc):
            ax = Line([PX - 2.9, y, 0], [PX + 2.9, y, 0], color=MUTED, stroke_width=1.5)
            g = VGroup(ax)
            for cx, c in zip(peaks, colors):
                g.add(FunctionGraph(lambda x, cx=cx: y + 1.05 * np.exp(-((x - cx) / width) ** 2),
                                    x_range=[cx - 4 * width, cx + 4 * width], color=c, stroke_width=3))
            g.add(T(label, 20, lc, BOLD).next_to(ax, DOWN, buff=0.15))
            return g

        one = spectrum(PY + 0.25, [PX], 0.42, [WHITE], "1 λ × 40 Gbit/s ?", TXT)
        four = spectrum(PY - 2.05, [PX - 1.8, PX - 0.6, PX + 0.6, PX + 1.8], 0.12, CH, "4 λ × 10 Gbit/s", ACC)
        self.focus(1, VGroup(evo, one, four))
        self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.15) for e in evo], lag_ratio=0.15), run_time=1.2)
        self.at(self.cues[2])
        self.play(Create(one[0]), Create(one[1]), FadeIn(one[2]), run_time=1.0)
        self.at(self.cues[2] + 3.0)
        self.play(Create(four[0]), LaggedStart(*[Create(p) for p in four[1:5]], lag_ratio=0.15), FadeIn(four[5]),
                  run_time=1.3)
        self.play(Indicate(evo[4], color=ACC), run_time=0.6)
        self.end(pad=0.05)

    # ── o4: G.989 family as a layer stack, PMD ↔ TC boundary ─────────────
    def o4_layers(self):
        self.beat("o4")
        W = 5.4
        rows = [("G.988 · OMCI — yönetim", LEGACY), ("G.989.3 · TC katmanı", CH[1]), ("G.989.2 · PMD katmanı", ACC),
                ("ODN · fiber ve pasif bileşenler", "#475569")]
        stack = VGroup()
        for s, c in rows:
            r = RoundedRectangle(corner_radius=0.1, width=W, height=0.68, stroke_color=c, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=1)
            stack.add(VGroup(r, T(s, 21, TXT, SEMIBOLD).move_to(r)))
        stack.arrange(DOWN, buff=0.35).move_to([PX, PY - 0.35, 0])
        stack[2:].shift(DOWN * 0.45); stack.move_to([PX, PY - 0.3, 0])
        top = VGroup(pill("G.989 · tanımlar", MUTED, 16), pill("G.989.1 · genel gereksinimler", MUTED, 16)
                     ).arrange(RIGHT, buff=0.25).next_to(stack, UP, buff=0.35)
        yb = (stack[1].get_bottom()[1] + stack[2].get_top()[1]) / 2
        border = DashedLine([PX - W / 2 - 0.2, yb, 0], [PX + W / 2 + 0.2, yb, 0], color=GOLD, stroke_width=3,
                            dash_length=0.12)
        blab = pill("PMD ↔ TC   ↓ 125 µs çerçeve  ·  ↑ burst", GOLD, 15, fill="#0C1324").move_to(border)
        self.focus(2, VGroup(stack, top, border, blab))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in reversed(stack)], lag_ratio=0.2),
                  FadeIn(top, shift=DOWN * 0.15), run_time=1.8)
        self.at(self.cues[1] - 0.2)
        self.play(Create(border), FadeIn(blab), stack[2][0].animate.set_fill(ACC, opacity=0.18), run_time=0.9)
        self.end(pad=0.05)

    # ── o5: reference architecture, measurement points, line rates ───────
    def o5_arch(self):
        self.beat("o5")
        y = PY + 0.85
        cts = VGroup(*[box(1.05, 0.42, s, c, 14) for s, c in
                       [("TWDM CT", CH[0]), ("TWDM CT", CH[1]), ("PtP CT", CH[3])]]).arrange(DOWN, buff=0.14)
        cts.move_to([PX - 2.95, y, 0])
        wm = box(0.5, 1.55, "WM", "#3B4A75", 15).move_to([PX - 1.75, y, 0])
        ce = box(0.6, 0.8, "CE", "#3B4A75", 15).move_to([PX - 0.15, y, 0])
        legacy = T("GPON · XG-PON · RF", 13, LEGACY).next_to(ce, UP, buff=0.42)
        lg_line = Line(legacy.get_bottom(), ce.get_top(), color=LEGACY, stroke_width=2)
        spl = Triangle(color="#CBD5E1", fill_color=PANEL, fill_opacity=1, stroke_width=2).rotate(-PI / 2).scale(0.22)
        spl.move_to([PX + 1.75, y, 0])
        onu = box(1.0, 0.62, "ONU", "#94A3B8", 15).move_to([PX + 3.0, y, 0])
        ln = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color="#94A3B8", stroke_width=2) for c in cts],
                    Line(wm.get_right(), ce.get_left(), color="#CBD5E1", stroke_width=3),
                    Line(ce.get_right(), spl.get_left(), color="#CBD5E1", stroke_width=3),
                    Line(spl.get_right(), onu.get_left(), color="#94A3B8", stroke_width=2))
        def marker(x, s, c, up=True):
            l = DashedLine([x, y - 1.0, 0], [x, y + 1.0, 0], color=c, stroke_width=2, dash_length=0.07)
            t = T(s, 14, c, BOLD).next_to(l, DOWN if not up else UP, buff=0.05)
            return VGroup(l, t)
        m_cp = marker(cts.get_right()[0] + 0.12, "S/R-CP", GOLD, up=False)
        m_cg = marker((wm.get_right()[0] + ce.get_left()[0]) / 2, "S/R-CG", ACC, up=False)
        m_rs = marker(onu.get_left()[0] - 0.12, "R/S", ACC, up=False)
        rates = VGroup(pill("9,95328 Gbit/s", TXT, 16), pill("2,48832 Gbit/s", TXT, 16)).arrange(RIGHT, buff=0.25)
        rates_t = T("G.989.3 Tablo 6-1/6-2 · hat hızı kombinasyonları", 14, MUTED)
        doc = VGroup(*[pill(s, LEGACY, 14) for s in ("§6", "§9", "§10", "§11", "Ek A–D", "Ek I–XI")]).arrange(RIGHT, buff=0.12)
        doc_t = T("G.989.2 haritası", 14, MUTED)
        low = VGroup(VGroup(rates, rates_t).arrange(DOWN, buff=0.1), VGroup(doc, doc_t).arrange(DOWN, buff=0.1)
                     ).arrange(DOWN, buff=0.35).move_to([PX, PY - 1.85, 0])
        arch = VGroup(cts, wm, ce, legacy, lg_line, spl, onu, ln)
        self.focus(3, VGroup(arch, m_cp, m_cg, m_rs, low))
        self.play(FadeIn(arch, lag_ratio=0.05), run_time=1.3)
        self.at(self.cues[1])
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in (m_cg, m_rs, m_cp)], lag_ratio=0.3), run_time=1.2)
        self.at(self.cues[1] + 2.4)
        self.play(FadeIn(low[0], shift=UP * 0.15), run_time=0.7)
        self.at(self.cues[2] - 0.1)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in doc], lag_ratio=0.1), FadeIn(doc_t), run_time=1.0)
        self.end(pad=0.05)

    # ── o6: the test bench ─────────────────────────────────────────────
    def o6_bench(self):
        self.beat("o6")
        tiles = VGroup(*[instrument(k) for k in ("OSA", "DCA", "BERT", "PM", "VOA", "OSC")])
        tiles.arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.45)).move_to([PX, PY - 0.05, 0])
        self.focus(4, tiles)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2, scale=0.95) for t in tiles], lag_ratio=0.12), run_time=1.6)
        self.at(self.cues[2])
        self.play(Indicate(self.items[4], color=ACC, scale_factor=1.05), run_time=0.6)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
