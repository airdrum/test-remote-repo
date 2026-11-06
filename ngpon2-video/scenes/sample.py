"""NG-PON2 / ITU-T G.989.2 — 1-minute concept sample.

Timing model: every narration beat is a separate TTS clip. `beat(i)` drops the clip on the
timeline, `at(t)` waits until t seconds into the current beat, `end()` waits for the clip to finish.
Phrase cue times (derived from TTS pauses) live in build/audio_proc/manifest.json.
"""
import json
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
MAN = json.loads((ROOT / "build/audio_proc/manifest.json").read_text())

BG, PANEL, LINE = "#0A0F1E", "#111A2E", "#2A3658"
TXT, MUTED, ACC, WARN = "#E6ECFF", "#8A97B8", "#5EEAD4", "#F87171"
CH = ["#8B5CF6", "#22D3EE", "#34D399", "#F59E0B"]  # λ1..λ4
LEGACY = "#64748B"
FONT = "Inter"
config.background_color = BG


def T(s, size=28, color=TXT, weight=NORMAL, **kw):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **kw)


def box(w, h, label=None, color=LINE, size=24, fill=PANEL, weight=SEMIBOLD):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=2.5,
                         fill_color=fill, fill_opacity=1)
    if label is None:
        return r
    return VGroup(r, T(label, size, TXT, weight).move_to(r))


def pill(s, color=ACC, size=22):
    t = T(s, size, color, SEMIBOLD)
    r = RoundedRectangle(corner_radius=0.22, width=t.width + 0.5, height=t.height + 0.32,
                         stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=0.85)
    return VGroup(r, t.move_to(r))


class Sample(Scene):
    # ---------- timing helpers ----------
    def beat(self, i):
        b = MAN["beats"][i]
        self.add_sound(b["file"])
        self.b0, self.bdur = self.renderer.time, b["duration"]
        self.cues = [c["t"] for c in b["cues"]]
        self.timeline.append({"id": b["id"], "start": round(self.b0, 3), "dur": b["duration"], "text": b["text"]})

    def at(self, t):
        dt = self.b0 + t - self.renderer.time
        if dt > 1 / 30:
            self.wait(dt)

    def end(self, pad=0.25):
        self.at(self.bdur + pad)

    def set_chip(self, s):
        new = pill(s, ACC, 20).to_corner(UR, buff=0.35)
        if self.chip is None:
            self.play(FadeIn(new, shift=LEFT * 0.2), run_time=0.4)
        else:
            self.play(FadeTransform(self.chip, new), run_time=0.4)
        self.chip = new

    # ---------- scene ----------
    def construct(self):
        self.timeline, self.chip = [], None
        self.s1_title()
        header = T("ITU-T G.989.2 · NG-PON2 PMD", 20, MUTED, MEDIUM).to_corner(UL, buff=0.38)
        self.add(header)
        self.s2_arch()
        self.s3_plan()
        self.s4_tuning()
        self.s5_test()
        self.s6_outro(header)
        (ROOT / "build/timeline.json").write_text(json.dumps(self.timeline, ensure_ascii=False, indent=1))

    # 1 ── title ───────────────────────────────────────────────────────────
    def s1_title(self):
        bg = ImageMobject(str(ROOT / "assets/title_bg.jpg")).set_height(config.frame_height * 1.02)
        shade = Rectangle(width=16, height=9, fill_color=BG, fill_opacity=0.35, stroke_width=0)
        left = VGroup(*[Rectangle(width=w, height=9, fill_color=BG, fill_opacity=0.28, stroke_width=0).to_edge(LEFT, buff=0)
                        for w in (5.5, 6.6, 7.6, 8.6)])
        bg.add_updater(lambda m, dt: m.scale(1 + 0.006 * dt))
        kicker = T("ITU-T TAVSİYESİ", 22, ACC, SEMIBOLD)
        title = T("G.989.2", 110, TXT, BOLD)
        sub = VGroup(T("NG-PON2", 34, TXT, BOLD), T("Fiziksel ortama bağımlı (PMD) katman", 28, TXT, MEDIUM)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tag = T("Konsept önizleme", 22, MUTED)
        g = VGroup(kicker, title, sub, tag).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(LEFT, buff=0.9).shift(UP * 0.6)
        chips = VGroup(*[pill(s, c, 22) for s, c in
                         [("01  Mimari", CH[0]), ("02  Dalga boyu planı", CH[1]), ("03  Test yöntemi", CH[2])]])
        chips.arrange(RIGHT, buff=0.3).next_to(g, DOWN, buff=0.7, aligned_edge=LEFT)

        self.beat(0)
        self.play(FadeIn(bg), FadeIn(shade), FadeIn(left), run_time=1.0)
        self.play(FadeIn(kicker, shift=RIGHT * 0.3), Write(title), run_time=1.2)
        self.at(self.cues[1])
        self.play(FadeIn(sub, shift=UP * 0.2), FadeIn(tag, shift=UP * 0.2), run_time=0.8)
        self.at(self.cues[2])
        for k, t0 in enumerate([self.cues[2] + 0.4, self.cues[2] + 1.3, self.cues[3] + 0.3]):
            self.at(t0)
            self.play(FadeIn(chips[k], shift=UP * 0.25, scale=0.9), run_time=0.45)
        self.end(pad=0.1)
        bg.clear_updaters()
        self.play(FadeOut(Group(bg, shade, left, g, chips)), run_time=0.6)

    # 2 ── TWDM architecture ───────────────────────────────────────────────
    def s2_arch(self):
        self.beat(1)
        self.set_chip("01 · Mimari")
        head = T("TWDM-PON mimarisi", 40, TXT, BOLD).to_edge(UP, buff=0.95).to_edge(LEFT, buff=0.8)
        olt = box(3.1, 4.6, color="#3B4A75").move_to([-5.2, -0.45, 0])
        olt_t = T("OLT", 26, TXT, BOLD).next_to(olt.get_top(), DOWN, buff=0.22)
        cts = VGroup()
        for i in range(4):
            r = box(2.6, 0.62, color=CH[i]).move_to([-5.2, 0.85 - i * 0.8, 0])
            lab = T(f"CT{i + 1}", 22, TXT, SEMIBOLD).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.2)
            lam = T(f"λ{i + 1}↓ / λ{i + 1}′↑", 19, CH[i], MEDIUM).move_to(r).align_to(r, RIGHT).shift(LEFT * 0.18)
            cts.add(VGroup(r, lab, lam))
        note = T("4–8 dalga boyu çifti", 18, MUTED).next_to(olt, DOWN, buff=0.18)
        wm = box(0.85, 3.6, "WM", "#3B4A75", 20).move_to([-2.75, -0.45, 0])
        ct_lines = VGroup(*[Line(cts[i][0].get_right(), [wm.get_left()[0], cts[i][0].get_y(), 0],
                                 color=CH[i], stroke_width=3) for i in range(4)])
        y_f = -0.45
        fiber = Line([wm.get_right()[0], y_f, 0], [1.55, y_f, 0], color="#CBD5E1", stroke_width=5)
        fiber_t = T("Tek fiber (ODN)", 20, MUTED).next_to(fiber, UP, buff=0.15)
        split = Triangle(color="#CBD5E1", fill_color=PANEL, fill_opacity=1, stroke_width=2.5).rotate(-PI / 2).scale(0.45)
        split.move_to([2.0, y_f, 0])
        split_t = T("Pasif ayırıcı 1:N", 18, MUTED).next_to(split, DOWN, buff=0.3).shift(LEFT * 0.75)
        onu_lam = [0, 1, 0, 2]
        onus, onu_lines = VGroup(), VGroup()
        for k, li in enumerate(onu_lam):
            y = 1.35 - k * 1.2
            r = box(2.3, 0.78, color=LINE).move_to([5.3, y + y_f + 0.45 - 0.45, 0])
            lab = T("ONU", 22, TXT, SEMIBOLD).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.22)
            dot = Dot(radius=0.11, color=CH[li]).move_to(r).align_to(r, RIGHT).shift(LEFT * 0.75)
            lam = T(f"λ{li + 1}", 20, CH[li], SEMIBOLD).next_to(dot, RIGHT, buff=0.12)
            onus.add(VGroup(r, lab, dot, lam))
            onu_lines.add(Line(split.get_right(), r.get_left(), color="#94A3B8", stroke_width=2.5))
        onu_note = T("Her dalga boyu zamanda paylaşılır (TDMA)", 18, MUTED).next_to(onus, DOWN, buff=0.25).align_to(onus, RIGHT)

        self.play(FadeIn(head, shift=RIGHT * 0.2), Create(olt), FadeIn(olt_t), run_time=0.9)
        self.at(self.cues[1])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cts], lag_ratio=0.3), FadeIn(note), run_time=1.6)
        self.at(self.cues[1] + 2.6)
        self.play(LaggedStart(*[Indicate(c[2], color=CH[i], scale_factor=1.15) for i, c in enumerate(cts)],
                              lag_ratio=0.2), run_time=1.4)
        self.at(self.cues[1] + 4.7)
        self.play(FadeIn(wm), LaggedStart(*[Create(l) for l in ct_lines], lag_ratio=0.15), run_time=0.8)
        self.play(Create(fiber), FadeIn(fiber_t), run_time=0.8)
        self.at(self.cues[2])
        self.play(FadeIn(split), FadeIn(split_t), LaggedStart(*[Create(l) for l in onu_lines], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(o, shift=LEFT * 0.2) for o in onus], lag_ratio=0.15), run_time=1.3)
        # downstream: all λ broadcast through the splitter, each ONU locks to its own channel
        pulses = VGroup(*[Dot(radius=0.09, color=CH[i]).move_to(fiber.get_start()) for i in range(4)])
        self.play(LaggedStart(*[MoveAlongPath(p, fiber) for p in pulses], lag_ratio=0.22, rate_func=linear),
                  run_time=1.2)
        self.remove(*pulses)
        fan = VGroup(*[Dot(radius=0.09, color=CH[onu_lam[k]]).move_to(split.get_right()) for k in range(4)])
        self.play(*[MoveAlongPath(fan[k], onu_lines[k]) for k in range(4)], FadeIn(onu_note), run_time=0.8,
                  rate_func=linear)
        self.remove(*fan)
        self.play(*[Flash(o[2], color=o[2].get_color(), line_length=0.15, flash_radius=0.2) for o in onus], run_time=0.5)
        self.end(pad=0.1)
        self.play(FadeOut(VGroup(head, olt, olt_t, cts, note, wm, ct_lines, fiber, fiber_t, split, split_t, onus,
                                 onu_lines, onu_note)), run_time=0.5)

    # 3 ── wavelength plan ────────────────────────────────────────────────
    def s3_plan(self):
        self.beat(2)
        self.set_chip("02 · Dalga boyu planı")
        head = T("Dalga boyu planı ve birlikte çalışma", 40, TXT, BOLD).to_edge(UP, buff=0.95).to_edge(LEFT, buff=0.8)
        ya, k = 0.15, 0.05  # axis y, units per nm

        def X(nm):  # broken axis: 1255–1335 | 1470–1630
            return -6.4 + (nm - 1255) * k if nm <= 1340 else -1.85 + (nm - 1470) * k

        axA = Line([X(1255), ya, 0], [X(1335), ya, 0], color=MUTED, stroke_width=2)
        axB = Line([X(1470), ya, 0], [X(1630), ya, 0], color=MUTED, stroke_width=2)
        brk = VGroup(*[Line([x - 0.06, ya - 0.12, 0], [x + 0.06, ya + 0.12, 0], color=MUTED, stroke_width=2)
                       for x in (X(1335) + 0.2, X(1470) - 0.2)])
        ticks = VGroup()
        for nm in list(range(1260, 1340, 20)) + list(range(1480, 1631, 20)):
            major = nm % 100 == 0
            ticks.add(Line([X(nm), ya, 0], [X(nm), ya - (0.16 if major else 0.08), 0], color=MUTED, stroke_width=2))
            if nm % 40 == 0 or nm in (1260, 1300, 1500, 1600):
                ticks.add(T(str(nm), 16, MUTED).move_to([X(nm), ya - 0.36, 0]))
        ax_t = T("nm", 16, MUTED).next_to(axB, RIGHT, buff=0.15)

        def band(lo, hi, h, color, op=0.85):
            return Rectangle(width=X(hi) - X(lo), height=h, stroke_width=0, fill_color=color, fill_opacity=op
                             ).move_to([(X(lo) + X(hi)) / 2, ya + h / 2, 0])

        legacy = [(1260, 1280, "XG-PON ↑", 0), (1290, 1330, "GPON ↑", 0), (1480, 1500, "GPON ↓", 0),
                  (1550, 1560, "RF video", 0), (1575, 1581, "XG-PON ↓", 0)]
        leg = VGroup()
        for lo, hi, lab, _ in legacy:
            b = band(lo, hi, 0.8, LEGACY, 0.75)
            leg.add(VGroup(b, T(lab, 16, "#CBD5E1", MEDIUM).next_to(b, UP, buff=0.12)))
        ds = band(1596, 1603, 1.5, ACC, 0.95)
        ds_t = VGroup(T("NG-PON2 ↓", 18, ACC, BOLD), T("1596–1603 nm", 15, ACC)).arrange(DOWN, buff=0.06)
        ds_t.next_to(ds, UP, buff=0.12)
        us = band(1524, 1544, 1.5, "#A78BFA", 0.9)
        us_t = VGroup(T("NG-PON2 ↑", 18, "#C4B5FD", BOLD), T("1524–1544 nm (geniş)", 15, "#C4B5FD")
                      ).arrange(DOWN, buff=0.06).next_to(us, UP, buff=0.12)
        ptp = band(1603, 1625, 0.55, "#0EA5E9", 0.35)
        ptp_t = T("PtP WDM", 15, "#7DD3FC").next_to(ptp, UP, buff=0.08).align_to(ptp, RIGHT)

        # zoom inset: DS 100 GHz grid (187.8 … 187.1 THz)
        panel = box(6.3, 2.85, color="#244055").move_to([3.3, -2.45, 0])
        p_t = T("TWDM ↓ kanal ızgarası", 18, ACC, SEMIBOLD).next_to(panel.get_top(), DOWN, buff=0.16)
        gx = lambda i: panel.get_left()[0] + 0.75 + i * 0.68  # channel i (0..7) → x
        gy0 = panel.get_bottom()[1] + 0.62
        base = Line([gx(0) - 0.45, gy0, 0], [gx(7) + 0.45, gy0, 0], color=MUTED, stroke_width=2)
        peaks, labels = VGroup(), VGroup()
        for i in range(8):
            f = 187.8 - 0.1 * i
            if i < 4:
                pk = FunctionGraph(lambda x, c=gx(i): gy0 + 1.0 * np.exp(-((x - c) / 0.07) ** 2),
                                   x_range=[gx(i) - 0.3, gx(i) + 0.3], color=CH[i], stroke_width=3.5)
            else:
                pk = DashedLine([gx(i), gy0, 0], [gx(i), gy0 + 1.0, 0], color=LINE, dash_length=0.06)
            peaks.add(pk)
            labels.add(T(f"{f:.1f}".replace(".", ","), 13, MUTED).move_to([gx(i), gy0 - 0.22, 0]))
        thz = T("THz", 13, MUTED).next_to(labels, RIGHT, buff=0.12)
        brace = BraceBetweenPoints([gx(0), gy0 + 1.08, 0], [gx(1), gy0 + 1.08, 0], direction=UP, color=TXT)
        brace_t = T("100 GHz", 15, TXT).next_to(brace, UP, buff=0.04)
        opt = T("5–8: opsiyonel", 13, MUTED).move_to([(gx(5) + gx(6)) / 2, gy0 + 1.2, 0])
        zy = ya - 0.58
        zl = VGroup(DashedLine([X(1596), zy, 0], panel.get_corner(UL), color=ACC, stroke_width=1.5, dash_length=0.07),
                    DashedLine([X(1603), zy, 0], panel.get_corner(UR), color=ACC, stroke_width=1.5, dash_length=0.07))
        badge = pill("✓  GPON · XG-PON · RF video · NG-PON2 → aynı ODN", "#86EFAC", 19)
        badge.move_to([-3.3, -2.1, 0])

        self.play(FadeIn(head, shift=RIGHT * 0.2), Create(axA), Create(axB), FadeIn(brk), FadeIn(ticks),
                  FadeIn(ax_t), LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in leg], lag_ratio=0.1), run_time=1.1)
        self.at(self.cues[1])
        self.play(GrowFromEdge(ds, DOWN), FadeIn(ds_t, shift=UP * 0.15), run_time=0.9)
        self.at(self.cues[2])
        self.play(Create(zl), FadeIn(panel), FadeIn(p_t), Create(base), FadeIn(labels), FadeIn(thz), run_time=0.8)
        self.play(LaggedStart(*[Create(p) for p in peaks], lag_ratio=0.12), run_time=1.2)
        self.play(GrowFromCenter(brace), FadeIn(brace_t), FadeIn(opt), run_time=0.6)
        self.at(self.cues[4] - 0.2)
        self.play(GrowFromEdge(us, DOWN), FadeIn(us_t, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(ptp), FadeIn(ptp_t), run_time=0.5)
        self.at(self.cues[5])
        self.play(LaggedStart(*[Indicate(l[0], color="#CBD5E1", scale_factor=1.06) for l in leg], lag_ratio=0.12),
                  FadeIn(badge, shift=UP * 0.2), run_time=1.6)
        self.end(pad=0.1)
        self.play(FadeOut(VGroup(head, axA, axB, brk, ticks, ax_t, leg, ds, ds_t, us, us_t, ptp, ptp_t, panel, p_t,
                                 base, peaks, labels, thz, brace, brace_t, opt, zl, badge)), run_time=0.5)

    # 4 ── tunable ONU + tuning-time classes ──────────────────────────────
    def s4_tuning(self):
        self.beat(3)
        self.set_chip("03 · Ayarlanabilirlik")
        head = T("Ayarlanabilir ONU ve ayar süresi sınıfları", 40, TXT, BOLD).to_edge(UP, buff=0.95).to_edge(LEFT, buff=0.8)
        onu = box(2.6, 1.3, color="#3B4A75").move_to([-5.0, 1.2, 0])
        onu_t = VGroup(T("ONU", 24, TXT, BOLD), T("ayarlanabilir Tx/Rx", 16, MUTED)).arrange(DOWN, buff=0.08).move_to(onu)
        sy, sx = 0.55, [-2.4 + i * 1.25 for i in range(4)]
        sbase = Line([sx[0] - 0.7, sy, 0], [sx[3] + 0.7, sy, 0], color=MUTED, stroke_width=2)
        slots = VGroup(*[VGroup(DashedLine([x, sy, 0], [x, sy + 1.45, 0], color=CH[i], stroke_width=2, dash_length=0.06),
                                T(f"λ{i + 1}′", 16, CH[i]).move_to([x, sy - 0.22, 0])) for i, x in enumerate(sx)])
        pos = ValueTracker(sx[1])
        laser = always_redraw(lambda: FunctionGraph(
            lambda x: sy + 1.3 * np.exp(-((x - pos.get_value()) / 0.09) ** 2),
            x_range=[pos.get_value() - 0.4, pos.get_value() + 0.4], color=WHITE, stroke_width=4))
        cmd = pill("OLT → ONU : Tuning_Control  (λ2′ → λ3′)", "#FBBF24", 18).move_to([3.7, 1.35, 0])
        arr = Arrow(sx[1] * RIGHT + (sy + 1.6) * UP, sx[2] * RIGHT + (sy + 1.6) * UP, buff=0.05, color="#FBBF24",
                    stroke_width=3, max_tip_length_to_length_ratio=0.2)

        # log time axis 1 µs … 10 s
        ay, x0, dec = -2.85, -4.0, 1.45

        def LX(t):
            return x0 + (np.log10(t) + 6) * dec

        tax = Line([LX(1e-6), ay, 0], [LX(10), ay, 0], color=MUTED, stroke_width=2)
        tl = VGroup()
        for e, s in zip(range(-6, 2), ["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms", "1 s", "10 s"]):
            tl.add(Line([LX(10 ** e), ay, 0], [LX(10 ** e), ay - 0.12, 0], color=MUTED, stroke_width=2))
            tl.add(T(s, 15, MUTED).move_to([LX(10 ** e), ay - 0.34, 0]))
        rows = [("Sınıf 1", 1e-6, 10e-6, "< 10 µs", "tipik: elektronik ayar", CH[2]),
                ("Sınıf 2", 10e-6, 25e-3, "10 µs – 25 ms", "tipik: termal ayar", CH[1]),
                ("Sınıf 3", 25e-3, 1.0, "25 ms – 1 s", "tipik: yavaş termal ayar", CH[0])]
        bars = []
        for j, (name, a, b, rng, note, c) in enumerate(rows):
            y = -0.75 - j * 0.66
            r = Rectangle(width=LX(b) - LX(a), height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85
                          ).move_to([(LX(a) + LX(b)) / 2, y, 0])
            nm = VGroup(T(name, 20, TXT, SEMIBOLD), T(note, 13, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            nm.next_to([-6.45, y, 0], RIGHT, buff=0)
            rl = T(rng, 17, BG, BOLD).move_to(r) if r.width > 2.2 else T(rng, 17, c, BOLD).next_to(r, RIGHT, buff=0.15)
            nt = VGroup()
            bars.append((nm, r, rl, nt))

        self.play(FadeIn(head, shift=RIGHT * 0.2), FadeIn(onu), FadeIn(onu_t), Create(sbase), FadeIn(slots), run_time=0.9)
        self.add(laser)
        self.play(FadeIn(cmd, shift=DOWN * 0.2), run_time=0.5)
        self.at(1.9)
        self.play(GrowArrow(arr), run_time=0.4)
        self.play(pos.animate.set_value(sx[2]), run_time=1.2, rate_func=smooth)
        self.at(self.cues[1])
        self.play(Create(tax), FadeIn(tl), run_time=0.8)
        for j, t0 in enumerate([self.cues[2], self.cues[3], self.cues[3] + 1.5]):
            self.at(t0)
            nm, r, rl, nt = bars[j]
            self.play(FadeIn(nm), GrowFromEdge(r, LEFT), run_time=0.6)
            self.play(FadeIn(rl), FadeIn(nt), run_time=0.3)
        self.end(pad=0.1)
        laser.clear_updaters()
        self.play(FadeOut(VGroup(head, onu, onu_t, sbase, slots, cmd, arr, tax, tl, laser, *[VGroup(*b) for b in bars])),
                  run_time=0.5)

    # 5 ── test method: tuning-time measurement ───────────────────────────
    def s5_test(self):
        self.beat(4)
        self.set_chip("04 · Test yöntemi")
        head = T("Ayar süresi ölçümü — tipik düzenek", 40, TXT, BOLD).to_edge(UP, buff=0.95).to_edge(LEFT, buff=0.8)
        onu = box(2.0, 1.0, "ONU (DUT)", "#3B4A75", 20).move_to([-5.4, -0.35, 0])
        dmx = Polygon([-0.5, 0.75, 0], [0.5, 1.15, 0], [0.5, -1.15, 0], [-0.5, -0.75, 0], color="#CBD5E1",
                      fill_color=PANEL, fill_opacity=1, stroke_width=2.5).move_to([-2.6, -0.35, 0])
        dmx_t = T("DEMUX", 17, TXT, SEMIBOLD).move_to(dmx)
        f1 = Line(onu.get_right(), dmx.get_left(), color="#CBD5E1", stroke_width=4)
        pds, outs = VGroup(), VGroup()
        for i, (y, li, s) in enumerate([(0.4, 1, "λ2′  eski"), (-1.1, 2, "λ3′  yeni")]):
            pd = box(0.9, 0.62, "PD", CH[li], 18).move_to([-0.55, y, 0])
            ln = Line([dmx.get_right()[0], y, 0], pd.get_left(), color=CH[li], stroke_width=3)
            lab = T(s, 16, CH[li], MEDIUM).next_to(ln, UP, buff=0.08)
            pds.add(pd); outs.add(VGroup(ln, lab))
        # oscilloscope
        scr = Rectangle(width=4.8, height=3.4, stroke_color="#475569", stroke_width=2, fill_color="#050810",
                        fill_opacity=1).move_to([3.7, -0.65, 0])
        osc = box(5.3, 4.3, color="#475569", fill="#0D1426").move_to([3.7, -0.5, 0])
        osc_t = T("Osiloskop", 16, MUTED).next_to(scr, DOWN, buff=0.1).align_to(scr, LEFT)
        grid = VGroup(*[Line([scr.get_left()[0] + i * 0.48, scr.get_bottom()[1], 0],
                             [scr.get_left()[0] + i * 0.48, scr.get_top()[1], 0], color="#1E293B", stroke_width=1)
                        for i in range(1, 10)],
                      *[Line([scr.get_left()[0], scr.get_bottom()[1] + j * 0.425, 0],
                             [scr.get_right()[0], scr.get_bottom()[1] + j * 0.425, 0], color="#1E293B", stroke_width=1)
                        for j in range(1, 8)])
        wires = VGroup(*[Line(pds[i].get_right(), [scr.get_left()[0], pds[i].get_y(), 0], color="#64748B",
                              stroke_width=2) for i in range(2)])
        ax = Axes(x_range=[-1.5, 10, 1], y_range=[-0.5, 1.3, 1], x_length=4.6, y_length=3.2,
                  axis_config={"stroke_opacity": 0, "include_ticks": False}).move_to(scr)
        t0, tau = 0.0, 0.55
        old = lambda t: 1.0 if t < t0 + 0.25 else 0.02 + 0.98 * np.exp(-(t - t0 - 0.25) / 0.35)
        new = lambda t: 0.02 if t < t0 + 0.9 else 1 - np.exp(-(t - t0 - 0.9) / tau) * np.cos(2.6 * (t - t0 - 0.9))
        ts = np.linspace(t0 + 0.9, 10, 4000)
        out_band = np.abs(np.array([new(t) for t in ts]) - 1) > 0.05
        t_set = ts[np.where(out_band)[0][-1] + 1]
        c_old = ax.plot(old, x_range=[-1.5, 10, 0.01], color=CH[1], stroke_width=3)
        c_new = ax.plot(new, x_range=[-1.5, 10, 0.01], color=CH[2], stroke_width=3)
        band = Rectangle(width=ax.c2p(10, 0)[0] - ax.c2p(t0, 0)[0], height=ax.c2p(0, 1.05)[1] - ax.c2p(0, 0.95)[1],
                         stroke_width=0, fill_color=CH[2], fill_opacity=0.18).move_to(ax.c2p((t0 + 10) / 2, 1.0))
        m0 = DashedLine(ax.c2p(t0, -0.12), ax.c2p(t0, 1.3), color="#FBBF24", dash_length=0.06, stroke_width=2)
        m1 = DashedLine(ax.c2p(t_set, -0.12), ax.c2p(t_set, 1.3), color=TXT, dash_length=0.06, stroke_width=2)
        trig_t = T("TRIG", 14, "#FBBF24", BOLD).next_to(m0.get_top(), RIGHT, buff=0.08).shift(DOWN * 0.12)
        br = BraceBetweenPoints(ax.c2p(t0, -0.05), ax.c2p(t_set, -0.05), direction=DOWN, color=TXT)
        br_t = T("t_ayar", 18, TXT, BOLD).next_to(br, DOWN, buff=0.04)
        legend = VGroup(T("CH1 λ2′", 14, CH[1], MEDIUM), T("CH2 λ3′", 14, CH[2], MEDIUM)).arrange(RIGHT, buff=0.3)
        legend.next_to(scr, UP, buff=0.12).align_to(scr, RIGHT)
        # trigger source
        pc = box(2.0, 0.8, "Kontrol / tetik", "#FBBF24", 16).move_to([-5.4, 1.3, 0])
        cmd = Arrow(pc.get_bottom(), onu.get_top(), buff=0.05, color="#FBBF24", stroke_width=3,
                    max_tip_length_to_length_ratio=0.25)
        trig = VMobject(color="#FBBF24", stroke_width=2.5).set_points_as_corners(
            [pc.get_right(), [-4.0, pc.get_y(), 0], [-4.0, 2.05, 0], [m0.get_x(), 2.05, 0], [m0.get_x(), scr.get_top()[1], 0]])
        res = pill("örnek: t_ayar ≈ 7 µs  →  Sınıf 1 ✓", "#86EFAC", 19).next_to(osc, DOWN, buff=0.2)

        self.play(FadeIn(head, shift=RIGHT * 0.2), FadeIn(onu), run_time=0.6)
        self.play(Create(f1), FadeIn(dmx), FadeIn(dmx_t), run_time=0.8)
        self.at(3.4)
        self.play(LaggedStart(*[Create(o[0]) for o in outs], lag_ratio=0.2), FadeIn(pds),
                  LaggedStart(*[FadeIn(o[1]) for o in outs], lag_ratio=0.2), run_time=0.9)
        self.play(FadeIn(osc), FadeIn(scr), FadeIn(grid), FadeIn(osc_t), FadeIn(legend), Create(wires), run_time=0.9)
        self.at(self.cues[1] - 0.6)
        self.play(FadeIn(pc), GrowArrow(cmd), Create(trig), run_time=0.7)
        self.play(Create(m0), FadeIn(trig_t), Flash(m0.get_top(), color="#FBBF24", flash_radius=0.25), run_time=0.5)
        self.at(self.cues[2])
        self.play(Create(c_old), Create(c_new), run_time=2.0, rate_func=linear)
        self.play(FadeIn(band), Create(m1), run_time=0.6)
        self.play(GrowFromCenter(br), FadeIn(br_t), run_time=0.6)
        self.at(self.cues[3] - 0.3)
        self.play(FadeIn(res, shift=UP * 0.2), Indicate(br_t, color=ACC), run_time=0.8)
        self.end(pad=0.2)
        self.play(FadeOut(VGroup(head, onu, dmx, dmx_t, f1, pds, outs, osc, scr, grid, osc_t, wires, c_old, c_new, band,
                                 m0, m1, trig_t, br, br_t, legend, pc, cmd, trig, res)), run_time=0.5)

    # 6 ── outro ──────────────────────────────────────────────────────────
    def s6_outro(self, header):
        self.beat(5)
        self.set_chip("Seri yapısı")
        head = T("Tam seri: 4 bölüm × ~60 dk", 40, TXT, BOLD).move_to(UP * 1.9)
        cards = VGroup()
        for s, sub, c in [("Tanım", "parametre neyi ifade eder", CH[0]), ("Limit", "G.989.2 tablo değeri", CH[1]),
                          ("Ölçüm düzeneği", "nasıl test edilir", CH[2])]:
            r = RoundedRectangle(corner_radius=0.18, width=3.6, height=1.9, stroke_color=c, stroke_width=3,
                                 fill_color=PANEL, fill_opacity=1)
            cards.add(VGroup(r, VGroup(T(s, 30, c, BOLD), T(sub, 17, MUTED)).arrange(DOWN, buff=0.15).move_to(r)))
        cards.arrange(RIGHT, buff=0.9).shift(DOWN * 0.3)
        arrows = VGroup(*[Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.1, color=MUTED, stroke_width=3)
                          for i in range(2)])
        self.play(FadeIn(head, shift=UP * 0.2), run_time=0.7)
        for i, t0 in enumerate([self.cues[1] - 0.1, self.cues[2] - 0.1, self.cues[2] + 0.6]):
            self.at(t0)
            anims = [FadeIn(cards[i], shift=UP * 0.25)] + ([GrowArrow(arrows[i - 1])] if i else [])
            self.play(*anims, run_time=0.45)
        self.end(pad=0.6)
        self.wait(1.2)
        self.play(FadeOut(VGroup(head, cards, arrows, header, self.chip)), run_time=1.0)
        self.wait(0.6)
