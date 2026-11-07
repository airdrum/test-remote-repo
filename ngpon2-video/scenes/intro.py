"""LAMBDA series intro — 10.0 s, music-locked. Episode chosen with env EP=<n>."""
import os

from lib import *

EP = int(os.environ.get("EP", "1"))  # internal number: 1–10 season 1, 11–20 season 2
if EP > 10:
    _S2 = SERIES["season2"]
    EPI = next(e for e in _S2["episodes"] if e["n"] == EP - 10)
    TAGLINE, SEASON, KICK = _S2["tagline"], _S2["season"], f"SEZON 2 · BÖLÜM {EP - 10}"
else:
    EPI = next(e for e in SERIES["episodes"] if e["n"] == EP)
    TAGLINE, SEASON, KICK = SERIES["tagline"], SERIES["season"], f"BÖLÜM {EP}"
HIT = SERIES["intro_hit"]  # music impact time (s)


class Intro(Scene):
    def construct(self):
        self.add_sound(str(ROOT / SERIES["intro_music"]))
        t = lambda: self.renderer.time

        def until(x):
            if x - t() > 1 / 30:
                self.wait(x - t())

        # 1) a single white pulse runs down the fibre into the wavelength multiplexer
        node = np.array([-0.9, 0, 0])
        fibre = Line([-7.6, 0, 0], node, color=WHITE, stroke_width=2, stroke_opacity=0.35)
        pulse = glow_dot(WHITE, 0.07).move_to(fibre.get_start())
        until(0.15)
        self.play(Create(fibre), run_time=0.9, rate_func=linear)
        self.add(pulse)
        self.play(MoveAlongPath(pulse, fibre), run_time=1.5, rate_func=rate_functions.ease_in_quad)
        prism = Square(0.42, color=TXT, stroke_width=2, fill_color=PANEL, fill_opacity=1).rotate(PI / 4).move_to(node)
        self.remove(pulse)
        self.play(FadeIn(prism, scale=0.6), Flash(node, color=WHITE, line_length=0.25, flash_radius=0.35), run_time=0.4)

        # 2) it splits into the four channel colours
        ends = [np.array([6.8, y, 0]) for y in (1.35, 0.45, -0.45, -1.35)]
        rays = VGroup(*[Line(node, e, color=CH[i], stroke_width=4) for i, e in enumerate(ends)])
        dots = [glow_dot(CH[i], 0.06).move_to(node) for i in range(4)]
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.12), run_time=0.8, rate_func=smooth)
        self.add(*dots)
        self.play(*[MoveAlongPath(d, r) for d, r in zip(dots, rays)], FadeOut(fibre), run_time=0.9, rate_func=linear)
        self.remove(*dots)

        # 3) the colours fold into λ exactly on the musical impact
        lam = T("λ", 330, TXT, BOLD).move_to(ORIGIN)
        lam[0].set_fill(color=[CH[0], CH[1], CH[2], CH[3]], opacity=1).set_sheen_direction(DR)
        until(HIT - 1.05)
        self.play(ReplacementTransform(VGroup(rays, prism), lam), run_time=1.0, rate_func=rate_functions.ease_in_cubic)
        until(HIT)
        ring = Circle(radius=0.6, color=WHITE, stroke_width=6).move_to(lam)
        self.play(ring.animate.scale(6).set_stroke(opacity=0), lam.animate.scale(1.08), run_time=0.35,
                  rate_func=rate_functions.ease_out_cubic)
        self.remove(ring)

        # 4) wordmark
        letters = VGroup(*[T(c, 104, TXT, BOLD) for c in "LAMBDA"]).arrange(RIGHT, buff=0.32)
        tag = T(TAGLINE, 30, MUTED, MEDIUM)
        season = T(SEASON, 20, ACC, SEMIBOLD)
        lam_small = lam.copy().scale(0.42)
        mark = VGroup(lam_small, letters).arrange(RIGHT, buff=0.55, aligned_edge=DOWN)
        VGroup(mark, tag, season).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(Transform(lam, lam_small), LaggedStart(*[FadeIn(c, shift=LEFT * 0.4) for c in letters], lag_ratio=0.07),
                  run_time=0.7, rate_func=rate_functions.ease_out_cubic)
        self.play(FadeIn(tag, shift=UP * 0.15), FadeIn(season, shift=UP * 0.15), run_time=0.5)

        # 5) episode card
        until(HIT + 1.75)
        logo = VGroup(lam, letters, tag, season)
        kick = T(KICK, 24, ACC, BOLD)
        title = T(EPI["title"], 76, TXT, BOLD)
        sub = T(EPI["sub"], 26, MUTED, MEDIUM)
        refs = T(EPI["refs"], 18, LEGACY, MEDIUM)
        card = VGroup(kick, title, sub, refs).arrange(DOWN, buff=0.22).move_to(DOWN * 0.9)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=LINE, stroke_width=2).next_to(card, UP, buff=0.35)
        self.play(logo.animate.scale(0.5).to_edge(UP, buff=0.9), run_time=0.55, rate_func=smooth)
        self.play(Create(rule), FadeIn(kick, shift=UP * 0.15), FadeIn(title, shift=UP * 0.2), run_time=0.55)
        self.play(FadeIn(sub), FadeIn(refs), run_time=0.4)
        until(9.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        until(10.0)
