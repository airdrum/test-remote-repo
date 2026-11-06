"""B01 · Perde 1 — PON'un özü. Six scenes (P1A…P1F) sharing one narration manifest; rendered in parallel."""
from lib import *

BADGE = {"std": ("Standart ne diyor", GOLD), "fiz": ("Fizik", ACC), "lab": ("Laboratuvarda", GOOD),
         "not": ("Mühendis notu", "#F472B6")}
FEED = "#CBD5E1"


def nrz(bits, x0, tb, ylo, yhi, rise=0.04):
    """Polyline points for an NRZ waveform."""
    pts, y = [], ylo
    for i, b in enumerate(bits):
        yt = ylo + (yhi - ylo) * float(b)
        xs = x0 + i * tb
        pts += [[xs, y, 0], [xs + rise, yt, 0]]
        y = yt
    pts.append([x0 + len(bits) * tb, y, 0])
    return pts


def scope(w, h, center):
    scr = Rectangle(width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#050810", fill_opacity=1).move_to(center)
    grid = VGroup(*[Line([scr.get_left()[0] + i * w / 10, scr.get_bottom()[1], 0], [scr.get_left()[0] + i * w / 10, scr.get_top()[1], 0],
                         color="#162033", stroke_width=1) for i in range(1, 10)],
                  *[Line([scr.get_left()[0], scr.get_bottom()[1] + j * h / 6, 0], [scr.get_right()[0], scr.get_bottom()[1] + j * h / 6, 0],
                         color="#162033", stroke_width=1) for j in range(1, 6)])
    return VGroup(scr, grid)


def make_tree(x_olt=-5.3, x_sp=-0.9, x_onu=4.9, y0=-0.4, n=4, spread=1.25, names=None, colors=None, onu_w=1.9):
    colors = colors or [CH[k % 4] for k in range(n)]
    names = names or [f"ONU-{'ABCDEFGH'[k]}" for k in range(n)]
    olt = box(1.5, 1.15, "OLT", "#3B4A75", 28).move_to([x_olt, y0, 0])
    sp = Triangle(color=FEED, fill_color=PANEL, fill_opacity=1, stroke_width=2.5).rotate(-PI / 2).scale(0.42).move_to([x_sp, y0, 0])
    feeder = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=5)
    ys = [y0 + spread * (n - 1) / 2 - k * spread for k in range(n)]
    onus = VGroup(*[box(onu_w, 0.66, names[k], colors[k], 20).move_to([x_onu, y, 0]) for k, y in enumerate(ys)])
    drops = VGroup(*[Line(sp.get_right(), o.get_left(), color="#94A3B8", stroke_width=2.5) for o in onus])
    return dict(olt=olt, sp=sp, feeder=feeder, onus=onus, drops=drops, colors=colors,
                all=VGroup(olt, feeder, sp, drops, onus))


class P1Base(Narrated):
    MANIFEST = "build/v4/ep01_p1/audio_proc/manifest.json"
    FIRST = False
    PREV_BADGE = None

    def setup(self):
        super().setup()
        self.hdr = T("BÖLÜM 1 · PERDE 1 — PON'un özü", 20, MUTED, MEDIUM).to_corner(UL, buff=0.4)
        self.badge = self.src = None
        if not self.FIRST:
            self.add(self.hdr)
        if self.PREV_BADGE:
            s, c = BADGE[self.PREV_BADGE]
            self.badge = pill(s, c, 20).to_corner(UR, buff=0.35)
            self.add(self.badge)

    def set_badge(self, key):
        s, c = BADGE[key]
        new = pill(s, c, 20).to_corner(UR, buff=0.35)
        if self.badge is None:
            self.play(FadeIn(new, shift=LEFT * 0.2), run_time=0.4)
        else:
            self.play(FadeTransform(self.badge, new), run_time=0.4)
        self.badge = new

    def set_src(self, s):
        old = self.src
        if not s:
            self.src = None
            return FadeOut(old) if old is not None else Wait(0.05)
        new = T(s, 16, MUTED, MEDIUM).to_corner(DL, buff=0.35)
        self.src = new
        return FadeIn(new) if old is None else FadeTransform(old, new)

    def heading(self, s):
        return T(s, 38, TXT, BOLD).next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)

    def clear(self, *keep, rt=0.5):
        keep = set(keep) | {self.hdr, self.badge}
        out = [m for m in self.mobjects if m not in keep]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=rt)
        if self.src is not None and self.src not in keep:
            self.src = None


# ── A: title card + "Standart ne diyor" (p1–p3) ─────────────────────────────
class P1A(P1Base):
    FIRST = True

    def construct(self):
        self.beat("p1")
        kick = T("PERDE 1", 26, ACC, BOLD)
        title = T("PON'un özü", 80, TXT, BOLD)
        tc = VGroup(kick, title).arrange(DOWN, buff=0.2).move_to(UP * 1.6)
        self.play(FadeIn(kick, shift=UP * 0.2), Write(title), run_time=1.3)
        cards = VGroup(*[self.problem_card(k) for k in range(3)]).arrange(RIGHT, buff=0.55).move_to(DOWN * 1.35)
        for k, t0 in enumerate([self.cues[4] - 0.2, self.cues[5] - 0.1, self.cues[5] + 1.9]):
            self.at(t0)
            self.play(FadeIn(cards[k], shift=UP * 0.3), run_time=0.6)
        self.end(pad=0.1)
        self.play(FadeOut(cards), ReplacementTransform(VGroup(kick, title), self.hdr), run_time=0.7)

        # p2 — scope of G.989.2
        self.beat("p2")
        self.set_badge("std")
        q = self.quote("G.989.2 §1 · Kapsam",
                       "“…flexible access networks using optical fibre technology … running at an\naggregate reference downstream rate of 40 Gbit/s.”",
                       "Fiber tabanlı, esnek erişim ağı · aşağı yönde 40 Gbit/s referans toplam hız")
        self.play(FadeIn(q[0]), FadeIn(q[1], shift=UP * 0.15), self.set_src("Kaynak: ITU-T G.989.2 (2019)/Amd.1 (2020) §1"),
                  run_time=0.8)
        self.at(self.cues[2])
        self.play(FadeIn(q[2], shift=UP * 0.15), q[1][0].animate.set_opacity(0.6), run_time=0.7)
        self.at(self.cues[4])
        self.play(Indicate(q[2], color=ACC, scale_factor=1.04), run_time=0.8)
        tr = make_tree(y0=-1.35, spread=0.78, n=4, onu_w=1.6)
        self.at(self.cues[5] - 0.3)
        self.play(q.animate.scale(0.82).to_edge(UP, buff=1.0), FadeIn(tr["olt"], shift=RIGHT * 0.2), run_time=0.8)
        self.at(self.cues[6] + 0.4)
        self.play(Create(tr["feeder"]), FadeIn(tr["sp"]), run_time=0.8)
        self.play(LaggedStart(*[Create(d) for d in tr["drops"]], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(o, shift=LEFT * 0.2) for o in tr["onus"]], lag_ratio=0.12), run_time=1.2)
        self.at(self.cues[8] - 0.2)
        br = BraceBetweenPoints(tr["olt"].get_corner(DR) + DOWN * 1.45, tr["onus"].get_corner(DL) + DOWN * 0.25, direction=DOWN, color=ACC)
        br.next_to(VGroup(tr["feeder"], tr["drops"]), DOWN, buff=0.15)
        br_t = T("ODN — optik dağıtım ağı (noktadan çok noktaya)", 20, ACC, SEMIBOLD).next_to(br, DOWN, buff=0.08)
        self.play(GrowFromCenter(br), FadeIn(br_t), run_time=0.8)
        self.end(pad=0.1)

        # p3 — two directions, same fibre
        self.beat("p3")
        q2 = self.quote("G.989.2 §6",
                        "“Transmission in downstream and upstream directions takes place in the ODN\nthrough the same fibre and components (duplex/diplex configuration).”",
                        "İki yön de aynı fiber ve aynı bileşenler üzerinden taşınır").scale(0.82).to_edge(UP, buff=1.0)
        self.play(FadeOut(q, shift=UP * 0.2), FadeIn(q2[0]), FadeIn(q2[1]), self.set_src("Kaynak: ITU-T G.989.2 §6"), run_time=0.7)
        ds_l = T("aşağı yön ↓", 20, TXT, SEMIBOLD).next_to(tr["feeder"], UP, buff=0.12)
        us_l = T("yukarı yön ↑", 20, GOLD, SEMIBOLD).next_to(tr["feeder"], DOWN, buff=0.12)
        self.at(self.cues[1])
        self.play(FadeIn(ds_l), *self.flow(tr, down=True, color=WHITE), run_time=1.6)
        self.at(self.cues[2])
        self.play(FadeIn(us_l), *self.flow(tr, down=False, color=GOLD), run_time=1.6)
        self.at(self.cues[4] - 0.3)
        self.play(FadeIn(q2[2], shift=UP * 0.15), run_time=0.6)
        self.play(*self.flow(tr, down=True, color=WHITE), *self.flow(tr, down=False, color=GOLD),
                  Indicate(tr["feeder"], color=ACC, scale_factor=1.0), run_time=1.8)
        self.end(pad=0.2)
        self.clear()
        self.save_timeline("ep01_p1A")

    def flow(self, tr, down=True, color=WHITE):
        """Pulses along feeder+drops (down) or drops+feeder (up); returns animations (run as one play)."""
        anims = []
        for k, d in enumerate(tr["drops"]):
            path = VMobject().set_points_as_corners([tr["olt"].get_right(), tr["sp"].get_center(), d.get_end()])
            if not down:
                path = VMobject().set_points_as_corners([d.get_end(), tr["sp"].get_center(), tr["olt"].get_right()])
            dot = glow_dot(color if down else tr["colors"][k], 0.06).move_to(path.get_start())
            delay = 0.12 * k if not down else 0
            seq = ([Wait(delay)] if delay > 0 else []) + [MoveAlongPath(dot, path, rate_func=linear), FadeOut(dot, run_time=0.01)]
            anims.append(Succession(*seq))
        return anims

    def quote(self, ref, en, tr_text):
        r = T(ref, 20, GOLD, BOLD)
        e = T(en, 20, MUTED, slant=ITALIC, line_spacing=0.9)
        t = T(tr_text, 26, TXT, SEMIBOLD)
        g = VGroup(r, e, t).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bar = Rectangle(width=0.06, height=g.height, stroke_width=0, fill_color=GOLD, fill_opacity=1).next_to(g, LEFT, buff=0.25)
        return VGroup(VGroup(bar, r), VGroup(e), t).move_to(UP * 1.2)

    def problem_card(self, k):
        r = RoundedRectangle(corner_radius=0.18, width=3.7, height=2.7, stroke_color=[CH[0], CH[1], GOLD][k], stroke_width=2.5,
                             fill_color=PANEL, fill_opacity=1)
        c = r.get_center() + UP * 0.35
        if k == 0:
            sp = Triangle(color=FEED, stroke_width=2).rotate(-PI / 2).scale(0.25).move_to(c)
            icon = VGroup(Line(c + LEFT * 1.0, sp.get_left(), color=WHITE, stroke_width=7), sp,
                          *[Line(sp.get_right(), c + RIGHT * 1.0 + UP * (0.45 - 0.3 * i), color=WHITE, stroke_width=2) for i in range(4)])
            lab = "Bölünen güç"
        elif k == 1:
            src = Dot(c + LEFT * 1.0, color=WHITE, radius=0.09)
            icon = VGroup(src, *[VGroup(Arrow(src.get_center(), c + RIGHT * 0.7 + UP * (0.45 - 0.3 * i), buff=0.1, stroke_width=2.5,
                                              color=MUTED, max_tip_length_to_length_ratio=0.12),
                                        Square(0.13, stroke_width=0, fill_color=CH[i], fill_opacity=1).move_to(c + RIGHT * 0.95 + UP * (0.45 - 0.3 * i)))
                                 for i in range(4)])
            lab = "Herkese giden aşağı yön"
        else:
            icon = VGroup(Line(c + LEFT * 1.2, c + RIGHT * 1.2, color=MUTED, stroke_width=2),
                          *[Rectangle(width=0.42, height=0.28, stroke_width=0, fill_color=CH[i], fill_opacity=1).move_to(c + RIGHT * (-0.84 + 0.56 * i) + UP * 0.14)
                            for i in range(4)])
            lab = "Sırayla konuşan yukarı yön"
        t = T(lab, 19, TXT, SEMIBOLD).move_to(r.get_center() + DOWN * 0.75)
        return VGroup(r, icon, t)


# ── B: split loss (p4–p6) ─────────────────────────────────────────────────
class P1B(P1Base):
    PREV_BADGE = "std"

    def construct(self):
        self.beat("p4")
        self.set_badge("fiz")
        h = self.heading("Bölünen güç")
        self.play(FadeIn(h, shift=RIGHT * 0.2), run_time=0.5)
        bolt = Polygon([0.05, 0.3, 0], [-0.12, -0.02, 0], [0.0, -0.02, 0], [-0.06, -0.3, 0], [0.13, 0.05, 0], [0.0, 0.05, 0],
                       stroke_width=0, fill_color=GOLD, fill_opacity=1)
        ring = Circle(radius=0.33, color=WARN, stroke_width=4)
        icon = VGroup(bolt, ring)
        nop = VGroup(icon, T("enerji yok · yükselteç yok · anahtar yok", 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3)
        nop.next_to(h, DOWN, buff=0.35, aligned_edge=LEFT)
        strike = Line(ring.point_at_angle(3 * PI / 4), ring.point_at_angle(-PI / 4), color=WARN, stroke_width=4)
        self.at(self.cues[1])
        self.play(FadeIn(nop), Create(strike), run_time=0.8)
        # 1:8 splitter as a binary tree of Y-branches; beam width halves at every stage
        x0, y0, dx = -6.2, -0.9, 1.45
        nodes = [[np.array([x0 + dx, y0, 0])]]
        for st in range(1, 4):
            sp = 2.4 / 2 ** (st - 1)
            nodes.append([p + RIGHT * dx + UP * s * sp / 2 for p in nodes[-1] for s in (1, -1)])
        beams = VGroup(Line([x0, y0, 0], nodes[0][0], color=WHITE, stroke_width=16))
        for st in range(1, 4):
            for i, p in enumerate(nodes[st]):
                beams.add(Line(nodes[st - 1][i // 2], p, color=WHITE, stroke_width=16 / 2 ** st))
        outs = VGroup(*[Line(p, p + RIGHT * 0.8, color=WHITE, stroke_width=2) for p in nodes[3]])
        stages = VGroup(*[T("−3 dB", 16, ACC, SEMIBOLD).move_to([x0 + dx * (st + 0.5), y0 - 2.3, 0]) for st in range(1, 4)])
        cap = T("1:8 ayırıcı = 3 kademe Y-ayrımı", 18, MUTED).move_to([x0 + 2.9, y0 - 2.8, 0])
        self.at(self.cues[2])
        self.play(Create(beams[0]), run_time=0.5)
        for st in range(1, 4):
            seg = [b for b in beams[1:] if abs(b.get_end()[0] - (x0 + dx * (st + 1))) < 0.01]
            self.play(*[Create(b) for b in seg], FadeIn(stages[st - 1]), run_time=0.45)
        self.play(Create(outs), FadeIn(cap), run_time=0.4)
        f = T("Lₛ = 10 · log₁₀ N   [dB]", 40, TXT, BOLD).move_to([3.4, 0.3, 0])
        fb = SurroundingRectangle(f, color=ACC, buff=0.25, corner_radius=0.12)
        self.at(self.cues[5] - 0.2)
        self.play(Write(f), Create(fb), run_time=1.2)
        self.end(pad=0.1)
        tree = VGroup(beams, outs, stages, cap)

        # p5 — loss vs N chart
        self.beat("p5")
        self.play(FadeOut(nop), FadeOut(strike), FadeOut(tree), VGroup(f, fb).animate.scale(0.7).move_to([-3.9, 1.85, 0]), run_time=0.6)
        ax = Axes(x_range=[0.5, 7.5, 1], y_range=[0, 25, 5], x_length=8.2, y_length=4.4,
                  axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False}).move_to([0.9, -1.0, 0])
        ynum = VGroup(*[T(str(v), 18, MUTED).next_to(ax.c2p(0.5, v), LEFT, buff=0.12) for v in range(0, 26, 5)])
        xl = VGroup(*[T(f"1:{2 ** k}", 18, MUTED).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k in range(1, 8)])
        yl = T("dB", 18, MUTED).next_to(ax.c2p(0.5, 25), LEFT, buff=0.55)
        ideal = [10 * np.log10(2 ** k) for k in range(1, 8)]
        band = Polygon(*[ax.c2p(k, ideal[k - 1] + 1) for k in range(1, 8)], *[ax.c2p(k, ideal[k - 1] + 3) for k in range(7, 0, -1)],
                       stroke_width=0, fill_color=WARN, fill_opacity=0.18)
        line = VMobject(color=ACC, stroke_width=3).set_points_as_corners([ax.c2p(k, ideal[k - 1]) for k in range(1, 8)])
        dots = VGroup(*[Dot(ax.c2p(k, ideal[k - 1]), color=ACC, radius=0.07) for k in range(1, 8)])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ynum), run_time=0.8)
        self.play(Create(line), FadeIn(dots), run_time=0.8)

        def tag(k, s):
            return VGroup(Dot(ax.c2p(k, ideal[k - 1]), color=WHITE, radius=0.1),
                          T(s, 20, WHITE, BOLD).next_to(ax.c2p(k, ideal[k - 1]), UL, buff=0.12))
        for k, s, t0 in [(1, "3 dB", 0.9), (5, "15 dB", self.cues[1] + 0.2), (6, "18 dB", self.cues[2] + 0.2)]:
            self.at(t0)
            self.play(FadeIn(tag(k, s), scale=0.8), run_time=0.4)
        self.at(self.cues[3])
        bl = T("gerçek ayırıcı: +1…3 dB fazlalık kaybı\n+ kollar arası düzgünsüzlük", 18, WARN, SEMIBOLD).move_to(ax.c2p(5.4, 6.5))
        self.play(FadeIn(band), FadeIn(bl), run_time=0.9)
        self.end(pad=0.1)

        # p6 — splitter dominates the budget; teaser for OPL classes
        self.beat("p6")
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.hdr, self.badge, h)], run_time=0.5)
        sc = 0.33  # units per dB
        x0 = -5.6
        axis = NumberLine(x_range=[0, 36, 5], length=36 * sc, include_numbers=False, color=MUTED).move_to([x0 + 18 * sc, -1.6, 0])
        axis.add(*[T(str(v), 18, MUTED).next_to(axis.n2p(v), DOWN, buff=0.15) for v in range(0, 36, 5)], T("dB", 18, MUTED).next_to(axis, RIGHT, buff=0.15))
        seg1 = Rectangle(width=20.5 * sc, height=0.8, stroke_width=0, fill_color=CH[0], fill_opacity=0.9).move_to([x0 + 20.5 * sc / 2, -0.7, 0])
        seg1_t = T("1:64 ayırıcı ≈ 18 + 2,5 dB", 22, WHITE, BOLD).move_to(seg1)
        seg2 = DashedVMobject(Rectangle(width=7 * sc, height=0.8, color=MUTED), num_dashes=40).next_to(seg1, RIGHT, buff=0)
        seg2_t = T("fiber · ek · konnektör", 18, MUTED).next_to(seg2, UP, buff=0.12)
        bar_t = T("Bir optik yolun kayıp bütçesi (örnek)", 22, TXT, SEMIBOLD).next_to(VGroup(seg1, seg2), UP, buff=0.75, aligned_edge=LEFT)
        self.play(FadeIn(axis), FadeIn(bar_t), GrowFromEdge(seg1, LEFT), run_time=0.9)
        self.play(FadeIn(seg1_t), run_time=0.3)
        self.at(self.cues[1] + 0.3)
        self.play(Create(seg2), FadeIn(seg2_t), run_time=0.7)
        self.at(self.cues[2] + 0.5)
        opl = Rectangle(width=21 * sc, height=0.32, stroke_width=0, fill_color=ACC, fill_opacity=0.35).move_to([x0 + 24.5 * sc, -2.35, 0])
        opl_t = T("Yol kaybı sınıfları: 14 … 35 dB (N1 … E2)  →  Bölüm 2", 20, ACC, SEMIBOLD).next_to(opl, DOWN, buff=0.15)
        ticks = VGroup(*[Line(axis.n2p(v) + UP * 0.25, axis.n2p(v) + DOWN * 0.95, color=ACC, stroke_width=2) for v in (14, 35)])
        self.play(Create(ticks), FadeIn(opl), FadeIn(opl_t, shift=UP * 0.1), self.set_src("G.989.2 §6.2, Tablo 6-1"), run_time=1.0)
        self.end(pad=0.2)
        self.clear()
        self.save_timeline("ep01_p1B")


# ── C: downstream broadcast (p7–p8) ──────────────────────────────────────
class P1C(P1Base):
    PREV_BADGE = "fiz"

    def construct(self):
        self.beat("p7")
        self.set_badge("fiz")
        h = self.heading("Aşağı yön: herkese yayın")
        tr = make_tree(y0=-0.2, spread=1.2)
        self.play(FadeIn(h, shift=RIGHT * 0.2), FadeIn(tr["all"]), run_time=0.9)
        rng = np.random.default_rng(3)
        dest = [0, 2, 1, 3, 0, 1, 3, 2]

        def frame():
            return VGroup(*[Square(0.17, stroke_width=0, fill_color=CH[d], fill_opacity=1) for d in dest]).arrange(RIGHT, buff=0.03)
        self.at(self.cues[1])
        f1 = frame().move_to(tr["olt"].get_right() + RIGHT * 0.6)
        self.play(FadeIn(f1), run_time=0.3)
        self.play(f1.animate.move_to(tr["sp"].get_left() + LEFT * 0.75), run_time=1.6, rate_func=linear)
        self.at(self.cues[2])
        copies = [f1.copy() for _ in range(4)]
        self.remove(f1)
        self.play(*[c.animate.scale(0.8).next_to(o, LEFT, buff=0.2) for c, o in zip(copies, tr["onus"])], run_time=1.4)
        self.at(self.cues[4] - 0.3)
        self.play(*[Indicate(c, color=WHITE, scale_factor=1.08) for c in copies], run_time=0.8)
        self.at(self.cues[5])
        marks = VGroup()
        anims = []
        for k, c in enumerate(copies):
            for i, d in enumerate(dest):
                if d != k:
                    anims.append(c[i].animate.set_fill(opacity=0.12))
                else:
                    marks.add(SurroundingRectangle(c[i], color=WHITE, buff=0.03, stroke_width=2))
        self.play(*anims, Create(marks), run_time=1.0)
        self.at(self.cues[6] - 0.3)
        self.play(*[tr["onus"][k][0].animate.set_fill(CH[k], opacity=0.25) for k in range(4)], run_time=0.6)
        self.end(pad=0.1)

        # p8 — consequences: security + timing
        self.beat("p8")
        self.play(VGroup(tr["all"], *copies, marks).animate.scale(0.62).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1), run_time=0.7)
        c1 = self.card("1 · Güvenlik", "Yayın ortamında gizlilik = şifreleme\nNG-PON2'de TC katmanının işi", "G.989.3 §15 (XGEM yükü şifreleme)", CH[0])
        c2 = self.card("2 · Zamanlama", "Aşağı yön sinyali = sistemin saati\n125 µs çerçeve referansı", "G.989.3 §6.1.2", CH[1])
        VGroup(c1, c2).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        lock = self.lock_icon().scale(0.5).next_to(c1[0].get_corner(UR), DL, buff=0.25)
        self.at(self.cues[1])
        self.play(FadeIn(c1, shift=LEFT * 0.3), FadeIn(lock), run_time=0.7)
        self.at(self.cues[3])
        self.play(*[c.animate.set_opacity(0.15) for c in copies], Indicate(c1[2], color=CH[0]), run_time=0.8)
        self.at(self.cues[6])
        self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=0.7)
        tl_y = c2[0].get_bottom()[1] - 0.45
        x0, x1 = c2[0].get_left()[0] + 0.2, c2[0].get_right()[0] - 0.2
        tl = Line([x0, tl_y, 0], [x1, tl_y, 0], color=MUTED, stroke_width=2)
        ticks = VGroup(*[Line([x, tl_y - 0.12, 0], [x, tl_y + 0.12, 0], color=CH[1], stroke_width=3) for x in np.linspace(x0, x1, 7)])
        tlab = T("125 µs", 16, CH[1]).next_to(VGroup(ticks[0], ticks[1]), DOWN, buff=0.08)
        self.at(self.cues[7])
        self.play(Create(tl), LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.15), FadeIn(tlab),
                  self.set_src("G.989.3 §6.1.2 · §15"), run_time=1.4)
        self.play(LaggedStart(*[Indicate(t, color=WHITE, scale_factor=1.6) for t in ticks], lag_ratio=0.2), run_time=1.6)
        self.end(pad=0.2)
        self.clear()
        self.save_timeline("ep01_p1C")

    def card(self, title, body, ref, color):
        r = RoundedRectangle(corner_radius=0.16, width=5.6, height=2.35, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
        g = VGroup(T(title, 26, color, BOLD), T(body, 20, TXT, line_spacing=0.9), T(ref, 15, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        g.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.3)
        return VGroup(r, g[0], g[1], g[2])

    def lock_icon(self):
        body = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.8, color=CH[0], fill_color=CH[0], fill_opacity=0.25, stroke_width=4)
        arc = Arc(radius=0.32, start_angle=0, angle=PI, color=CH[0], stroke_width=8).next_to(body, UP, buff=-0.02)
        return VGroup(body, arc)


# ── D: upstream — collision, TDMA, leakage (p9–p11) ─────────────────────────
class P1D(P1Base):
    PREV_BADGE = "fiz"

    def construct(self):
        self.beat("p9")
        self.set_badge("fiz")
        h = self.heading("Yukarı yön: sıraya girmek")
        tr = make_tree(x_olt=-3.0, x_sp=0.9, x_onu=5.3, y0=-0.4, spread=1.2, onu_w=1.6)
        sc = scope(3.0, 2.0, [-5.3, -0.4, 0])
        sc_t = T("OLT alıcısı", 16, MUTED).next_to(sc, UP, buff=0.1)
        link = Line(sc.get_right(), tr["olt"].get_left(), color="#64748B", stroke_width=2)
        self.play(FadeIn(h, shift=RIGHT * 0.2), FadeIn(tr["all"]), FadeIn(sc), FadeIn(sc_t), Create(link), run_time=1.0)
        comb = T("birleştirici", 18, GOLD, SEMIBOLD).next_to(tr["sp"], DOWN, buff=0.3)
        self.at(self.cues[1])
        self.play(FadeIn(comb), Indicate(tr["sp"], color=GOLD), run_time=0.8)
        self.at(self.cues[2])
        self.play(*self.bursts(tr, [0, 1, 2, 3], stagger=0.0, collide=False), run_time=1.8)
        # collision: B and D at the same time
        self.at(self.cues[3])
        self.play(*self.bursts(tr, [1, 3], stagger=0.0), run_time=1.6)
        x0, x1 = sc[0].get_left()[0] + 0.15, sc[0].get_right()[0] - 0.15
        yb = sc[0].get_bottom()[1] + 0.25
        rng = np.random.default_rng(7)
        b1, b2 = rng.integers(0, 2, 24), rng.integers(0, 2, 24)
        tb = (x1 - x0) / 24
        mix = VMobject(color=WARN, stroke_width=2.5).set_points_as_corners(nrz((b1 + 0.6 * b2) / 1.6, x0, tb, yb, yb + 1.45))
        self.at(self.cues[4])
        cross = T("✕ çarpışma", 22, WARN, BOLD).next_to(sc, DOWN, buff=0.15)
        self.play(Create(mix), FadeIn(cross, scale=1.2), run_time=1.2)
        self.end(pad=0.1)

        # p10 — TDMA grants
        self.beat("p10")
        self.play(FadeOut(mix), FadeOut(cross), run_time=0.4)
        gy = -3.05
        gx0 = -2.6
        slots = VGroup()
        for k, (s, w) in enumerate([(0.0, 1.4), (1.7, 0.9), (2.9, 1.8), (5.0, 1.1)]):
            slots.add(Rectangle(width=w, height=0.42, stroke_width=0, fill_color=CH[k], fill_opacity=0.85).move_to([gx0 + s + w / 2, gy, 0]))
        slot_l = VGroup(*[T("ABCD"[k], 18, BG, BOLD).move_to(s) for k, s in enumerate(slots)])
        gtitle = T("OLT'nin izin haritası: kim · ne zaman · ne kadar", 18, TXT, SEMIBOLD).next_to(slots, UP, buff=0.15).align_to(slots, LEFT)
        taxis = Arrow([gx0 - 0.2, gy - 0.35, 0], [gx0 + 6.6, gy - 0.35, 0], buff=0, color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        tlab = T("zaman", 15, MUTED).next_to(taxis, RIGHT, buff=0.1)
        self.at(self.cues[1])
        self.play(FadeIn(gtitle), Create(taxis), FadeIn(tlab), run_time=0.6)
        self.at(self.cues[3])
        self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in slots], lag_ratio=0.25), FadeIn(slot_l), run_time=1.6)
        self.at(self.cues[4])
        cursor = Line([gx0, gy - 0.3, 0], [gx0, gy + 0.3, 0], color=WHITE, stroke_width=3)
        self.add(cursor)
        rx = VGroup()
        for k in range(4):
            s = slots[k]
            self.play(cursor.animate.move_to([s.get_left()[0], gy, 0]), run_time=0.25, rate_func=linear)
            led = tr["onus"][k][0]
            self.play(led.animate.set_fill(CH[k], opacity=0.55), cursor.animate.move_to([s.get_right()[0], gy, 0]),
                      *self.bursts(tr, [k]), run_time=0.9, rate_func=linear)
            led.set_fill(PANEL, opacity=1)
            seg = Rectangle(width=s.width * 0.42, height=0.55 + 0.0 * k, stroke_width=0, fill_color=CH[k], fill_opacity=0.9)
            seg.move_to([x0 + 0.25 + (s.get_center()[0] - gx0) * 0.42, yb + 0.28, 0])
            rx.add(seg)
            self.add(seg)
        self.remove(cursor)
        ok = T("✓ sıralı burst'ler", 20, GOOD, BOLD).next_to(sc, DOWN, buff=0.15)
        self.play(FadeIn(ok), run_time=0.4)
        self.end(pad=0.1)

        # p11 — leakage of 63 idle transmitters
        self.beat("p11")
        self.play(FadeOut(VGroup(tr["all"], sc, sc_t, link, comb, slots, slot_l, gtitle, taxis, tlab, rx, ok)), run_time=0.5)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 40, 10], x_length=7.4, y_length=4.6,
                  axis_config={"color": MUTED, "include_tip": False, "stroke_width": 2, "include_ticks": False}).move_to([-1.3, -0.75, 0])
        ax.add(*[T(f"{v - 40}", 17, MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in range(0, 41, 10)])
        yl = T("OLT'de alınan güç (dB, göreli)", 17, MUTED).next_to(ax.y_axis, UP, buff=0.15).shift(RIGHT * 1.2)
        xl = T("zaman", 17, MUTED).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        burst = Rectangle(width=ax.c2p(7, 0)[0] - ax.c2p(3, 0)[0], height=ax.c2p(0, 38)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                          fill_color=CH[1], fill_opacity=0.9).move_to(ax.c2p(5, 19))
        b_t = T("konuşan ONU", 18, BG, BOLD).move_to(ax.c2p(5, 32))
        n = ValueTracker(1)
        floor = always_redraw(lambda: Rectangle(width=ax.c2p(10, 0)[0] - ax.c2p(0, 0)[0],
                                                height=max(0.01, ax.c2p(0, 4 + 10 * np.log10(n.get_value()))[1] - ax.c2p(0, 0)[1]),
                                                stroke_width=0, fill_color=WARN, fill_opacity=0.45).align_to(ax.c2p(0, 0), DL))
        n_t = always_redraw(lambda: T(f"sızan kapalı verici: {int(round(n.get_value()))}\n→ taban +{10 * np.log10(n.get_value()):.0f} dB", 19, WARN, BOLD)
                            .next_to(ax.c2p(10, 4 + 10 * np.log10(n.get_value())), RIGHT, buff=0.15))
        self.at(self.cues[1])
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(burst), FadeIn(b_t), run_time=0.9)
        self.at(self.cues[3])
        self.add(floor, n_t)
        self.bring_to_front(burst, b_t)
        self.play(n.animate.set_value(63), run_time=4.5, rate_func=rate_functions.ease_in_quad)
        self.play(Indicate(n_t, color=WARN, scale_factor=1.05), run_time=0.6)
        self.at(self.cues[5])
        lim = pill("Etkin değilken verici PSD limiti (WNE-PSD) · G.989.2 §11.1.5.2.9  →  Bölüm 6", GOLD, 18).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(lim, shift=UP * 0.2), self.set_src(""), run_time=0.7)
        self.end(pad=0.2)
        floor.clear_updaters(); n_t.clear_updaters()
        self.clear()
        self.save_timeline("ep01_p1D")

    def bursts(self, tr, idx, stagger=0.0, collide=True):
        anims = []
        for j, k in enumerate(idx):
            d = tr["drops"][k]
            path = VMobject().set_points_as_corners([d.get_end(), tr["sp"].get_center(), tr["olt"].get_right()])
            b = Rectangle(width=0.36, height=0.18, stroke_width=0, fill_color=CH[k], fill_opacity=1).move_to(path.get_start())
            seq = ([Wait(stagger * j)] if stagger * j > 0 else []) + [MoveAlongPath(b, path, rate_func=linear), FadeOut(b, run_time=0.01)]
            anims.append(Succession(*seq))
        return anims


# ── E: near–far, burst-mode Rx, timing, ranging (p12–p15) ──────────────────
class P1E(P1Base):
    PREV_BADGE = "fiz"

    def construct(self):
        self.beat("p12")
        self.set_badge("fiz")
        h = self.heading("Burst'lerin iki zorluğu: güç ve zaman")
        self.play(FadeIn(h, shift=RIGHT * 0.2), run_time=0.5)
        olt = box(1.3, 1.0, "OLT", "#3B4A75", 24).move_to([-5.6, 0.9, 0])
        near = box(1.9, 0.62, "ONU yakın", CH[1], 18).move_to([-1.2, 1.7, 0])
        far = box(1.9, 0.62, "ONU uzak", CH[3], 18).move_to([4.9, 0.1, 0])
        ln = Line(olt.get_right(), near.get_left(), color="#94A3B8", stroke_width=3)
        lf = Line(olt.get_right(), far.get_left(), color="#94A3B8", stroke_width=3)
        tn = T("yol kaybı 14 dB", 18, CH[1], SEMIBOLD).next_to(ln, UP, buff=0.05)
        tf = T("yol kaybı 29 dB", 18, CH[3], SEMIBOLD).next_to(lf.point_from_proportion(0.6), DOWN, buff=0.12)
        self.at(self.cues[1])
        self.play(FadeIn(olt), FadeIn(near), Create(ln), run_time=0.7)
        self.at(self.cues[2])
        self.play(FadeIn(tn), run_time=0.4)
        self.at(self.cues[3])
        self.play(FadeIn(far), Create(lf), FadeIn(tf), run_time=0.8)
        # received burst amplitudes on a scope
        sc = scope(9.0, 2.4, [0.7, -2.15, 0])
        x0 = sc[0].get_left()[0] + 0.3
        yb = sc[0].get_bottom()[1] + 0.25
        rng = np.random.default_rng(11)
        tb = 0.13
        big = VMobject(color=CH[1], stroke_width=2.5).set_points_as_corners(nrz(rng.integers(0, 2, 28), x0, tb, yb, yb + 1.85))
        small = VMobject(color=CH[3], stroke_width=2.5).set_points_as_corners(nrz(rng.integers(0, 2, 28), x0 + 4.6, tb, yb, yb + 1.85 / 31.6 * 4))
        scale_note = T("(uzak burst 4× büyütülerek çizildi)", 14, MUTED).move_to(sc[0].get_corner(DR) + LEFT * 1.75 + UP * 0.95)
        diff = T("15 dB  =  31,6 × güç farkı", 20, TXT, BOLD).move_to(sc[0].get_corner(UR) + LEFT * 1.9 + DOWN * 0.3)
        self.play(FadeIn(sc), Create(big), run_time=1.0)
        self.play(Create(small), FadeIn(scale_note), run_time=0.8)
        self.at(self.cues[5])
        src = pill("Tablo 6-1: maks. diferansiyel yol kaybı = 15 dB", GOLD, 18).next_to(sc, UP, buff=0.1).align_to(sc, LEFT)
        self.play(FadeIn(src), FadeIn(diff), self.set_src("G.989.2 §6.2, Tablo 6-1"), run_time=0.8)
        self.end(pad=0.1)

        # p13 — fixed threshold vs burst-mode threshold
        self.beat("p13")
        self.play(FadeOut(VGroup(olt, near, far, ln, lf, tn, tf, src, diff)), VGroup(sc, big, small, scale_note).animate.shift(UP * 2.35), run_time=0.7)
        yb2 = yb + (0.2 - (-2.15))
        th_fixed = DashedLine([x0 - 0.2, yb2 + 0.92, 0], [x0 + 8.4, yb2 + 0.92, 0], color=WARN, stroke_width=3, dash_length=0.1)
        th_t = T("sabit eşik", 18, WARN, BOLD).next_to(th_fixed, UP, buff=0.05).align_to(th_fixed, RIGHT)
        bad = T("✕ uzak ONU'nun tüm bitleri '0'", 20, WARN, BOLD).next_to(sc, DOWN, buff=0.2)
        self.at(self.cues[1] - 0.6)
        self.play(Create(th_fixed), FadeIn(th_t), run_time=0.7)
        self.play(FadeIn(bad), Indicate(small, color=WARN), run_time=0.8)
        self.at(self.cues[3])
        x_sw = x0 + 4.6
        th_bm = VMobject(color=WHITE, stroke_width=3.5).set_points_as_corners(
            [[x0 - 0.2, yb2 + 0.4, 0], [x0 + 0.25, yb2 + 0.92, 0], [x_sw - 0.25, yb2 + 0.92, 0], [x_sw, yb2 + 0.92, 0],
             [x_sw + 0.25, yb2 + 0.12, 0], [x0 + 8.4, yb2 + 0.12, 0]])
        bm_t = T("burst modlu alıcı: eşik ve kazanç her burst'te yeniden", 20, WHITE, BOLD).next_to(sc, DOWN, buff=0.25)
        acq = VGroup(*[Rectangle(width=0.4, height=sc[0].height, stroke_width=0, fill_color=GOLD, fill_opacity=0.18).move_to([xx + 0.1, sc[0].get_y(), 0])
                       for xx in (x0, x_sw)])
        self.play(FadeOut(bad), FadeOut(th_t), th_fixed.animate.set_opacity(0.25), run_time=0.4)
        self.play(Create(th_bm), FadeIn(acq), FadeIn(bm_t), run_time=1.4)
        self.at(self.cues[5] + 0.3)
        acq_t = T("edinim süresi", 17, GOLD, BOLD).next_to(acq[1], UP, buff=0.08)
        ref = pill("Ölçüm yöntemi: G.989.2 Ek V (bilgilendirici)  →  Bölüm 8", GOLD, 18).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(acq_t), FadeIn(ref, shift=UP * 0.2), self.set_src(""), run_time=0.8)
        self.end(pad=0.1)

        # p14 — round-trip delay difference
        self.beat("p14")
        self.play(FadeOut(VGroup(sc, big, small, scale_note, th_fixed, th_bm, bm_t, acq, acq_t, ref)), run_time=0.5)
        us = 0.0265  # units per µs
        X0 = -5.0
        ax = NumberLine(x_range=[0, 375, 25], length=375 * us, include_numbers=False, color=MUTED).move_to([X0 + 375 * us / 2, -2.4, 0])
        nums = VGroup(*[T(f"{v}", 16, MUTED).next_to(ax.n2p(v), DOWN, buff=0.12) for v in range(0, 376, 125)])
        unit = T("µs", 16, MUTED).next_to(ax, RIGHT, buff=0.15)
        frames = VGroup(*[Rectangle(width=125 * us, height=0.25, stroke_color=CH[1], stroke_width=1.5, fill_color=CH[1], fill_opacity=0.08 + 0.1 * (i % 2))
                          .move_to([ax.n2p(62.5 + 125 * i)[0], -2.05, 0]) for i in range(3)])
        fr_t = T("125 µs çerçeveler", 15, CH[1]).next_to(frames, UP, buff=0.05).align_to(frames, LEFT)
        speed = T("ışık hızı fiberde ≈ 4,9 µs/km   (n_g ≈ 1,47)", 22, TXT, SEMIBOLD).move_to([0, 1.9, 0])
        self.at(self.cues[1] + 2.0)
        self.play(FadeIn(speed, shift=UP * 0.1), run_time=0.7)
        def rtd_bar(km, y, color, label):
            t = 2 * km * 4.893
            bar = Rectangle(width=max(0.03, t * us), height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([X0 + t * us / 2, y, 0])
            lab = T(f"{label}: {km} km  →  gidiş-dönüş {t:.1f} µs".replace(".", ","), 19, color, SEMIBOLD).next_to(bar, RIGHT, buff=0.15)
            return VGroup(bar, lab), t
        bn, tn_ = rtd_bar(0.5, 0.6, CH[2], "yakın ONU")
        bf, tf_ = rtd_bar(20.5, -0.3, CH[3], "uzak ONU")
        bf[1].next_to(bf[0], UP, buff=0.08).align_to(bf[0], RIGHT)
        self.at(self.cues[2])
        self.play(Create(ax), FadeIn(nums), FadeIn(unit), FadeIn(frames), FadeIn(fr_t), run_time=0.7)
        self.play(GrowFromEdge(bn[0], LEFT), FadeIn(bn[1]), run_time=0.5)
        self.play(GrowFromEdge(bf[0], LEFT), FadeIn(bf[1]), run_time=1.0)
        self.at(self.cues[3] + 0.6)
        br = BraceBetweenPoints([X0 + tn_ * us, -0.55, 0], [X0 + tf_ * us, -0.55, 0], direction=DOWN, color=WHITE)
        br_t = T("Δ ≈ 196 µs  ≈  1,6 çerçeve", 22, WHITE, BOLD).next_to(br, DOWN, buff=0.06)
        self.play(GrowFromCenter(br), FadeIn(br_t), run_time=0.8)
        self.end(pad=0.1)

        # p15 — ranging + equalisation delay
        self.beat("p15")
        teq = 2 * 20.5 * 4.893 + 30
        eq_n = Rectangle(width=(teq - tn_) * us, height=0.42, stroke_color=CH[2], stroke_width=2, fill_color=CH[2], fill_opacity=0.25).next_to(bn[0], RIGHT, buff=0)
        eq_f = Rectangle(width=(teq - tf_) * us, height=0.42, stroke_color=CH[3], stroke_width=2, fill_color=CH[3], fill_opacity=0.25).next_to(bf[0], RIGHT, buff=0)
        eq_t = T("EqD (eşitleme gecikmesi)", 18, TXT, SEMIBOLD).next_to(eq_n, UP, buff=0.08)
        tline = DashedLine([X0 + teq * us, 1.1, 0], [X0 + teq * us, -0.75, 0], color=WHITE, stroke_width=2)
        tl_t = T("RTD + EqD = sabit", 20, WHITE, BOLD).next_to(tline, RIGHT, buff=0.15).shift(DOWN * 0.1)
        self.at(self.cues[1])
        rang = pill("ranging: aktivasyonda gidiş-dönüş gecikmesi ölçülür", ACC, 18).move_to([0, 1.9, 0])
        self.play(FadeOut(speed), FadeIn(rang), FadeOut(br), FadeOut(br_t), FadeOut(bn[1]), FadeOut(bf[1]), run_time=0.6)
        self.at(self.cues[3])
        self.play(GrowFromEdge(eq_n, LEFT), GrowFromEdge(eq_f, LEFT), FadeIn(eq_t), run_time=1.2)
        self.play(Create(tline), FadeIn(tl_t), run_time=0.6)
        self.at(self.cues[5])
        # bursts now land in their slots at the OLT with guard gaps
        y_rx = -1.25
        slots = [(0, 70), (85, 140), (155, 230), (245, 300)]
        bs = VGroup(*[Rectangle(width=(b - a) * us, height=0.36, stroke_width=0, fill_color=CH[k], fill_opacity=0.9).move_to([ax.n2p((a + b) / 2)[0], y_rx, 0])
                      for k, (a, b) in enumerate(slots)])
        g_lab = T("koruma", 14, MUTED).next_to(VGroup(bs[0], bs[1]), DOWN, buff=0.06)
        rx_t = T("OLT'de: burst'ler sırasında, araları koruma boşluğu", 17, TXT, SEMIBOLD).next_to(bs, UP, buff=0.1).align_to(bs, LEFT)
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.4) for b in bs], lag_ratio=0.25), FadeIn(rx_t), run_time=1.4)
        self.play(FadeIn(g_lab), self.set_src("G.989.3 §13.1 — ONU iletim zamanlaması ve EqD  →  Bölüm 2"), run_time=0.5)
        self.end(pad=0.2)
        self.clear()
        self.save_timeline("ep01_p1E")


# ── F: lab, engineer's note, recap (p16–p19) ──────────────────────────────
class P1F(P1Base):
    PREV_BADGE = "fiz"

    def construct(self):
        self.beat("p16")
        self.set_badge("lab")
        h = self.heading("Burst gücünü ölçmek")
        self.play(FadeIn(h, shift=RIGHT * 0.2), run_time=0.5)
        ax = Axes(x_range=[0, 30, 5], y_range=[0, 1.2, 0.5], x_length=8.0, y_length=3.4,
                  axis_config={"color": MUTED, "include_tip": False, "include_ticks": False, "stroke_width": 2}).move_to([-2.2, -0.6, 0])
        yl = T("optik güç (doğrusal)", 16, MUTED).next_to(ax.y_axis, UP, buff=0.1).shift(RIGHT * 0.9)
        xl = T("zaman", 16, MUTED).next_to(ax.x_axis, DOWN, buff=0.1).align_to(ax.x_axis, RIGHT)
        pts = []
        for p in range(3):
            a = p * 10 + 2
            pts += [ax.c2p(p * 10, 0.02), ax.c2p(a, 0.02), ax.c2p(a + 0.05, 1.0), ax.c2p(a + 1.0, 1.0), ax.c2p(a + 1.05, 0.02)]
        pts.append(ax.c2p(30, 0.02))
        wave = VMobject(color=CH[1], stroke_width=3).set_points_as_corners(pts)
        avg = DashedLine(ax.c2p(0, 0.1), ax.c2p(30, 0.1), color=WARN, stroke_width=3, dash_length=0.1)
        avg_t = T("ortalama = %10 × burst", 17, WARN, BOLD).next_to(avg, UP, buff=0.05).align_to(avg, RIGHT)
        pk = DashedLine(ax.c2p(0, 1.0), ax.c2p(30, 1.0), color=GOOD, stroke_width=2, dash_length=0.1)
        pk_t = T("burst gücü", 17, GOOD, BOLD).next_to(pk, UP, buff=0.05).align_to(pk, RIGHT)
        m1 = self.meter("CW güç ölçer", "−28,2 dBm", "ortalama", WARN).move_to([4.5, 0.7, 0])
        m2 = self.meter("Burst güç ölçer", "−18,2 dBm", "burst", GOOD).move_to([4.5, -1.6, 0])
        self.at(self.cues[2])
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), run_time=0.6)
        self.play(Create(wave), run_time=1.6, rate_func=linear)
        self.at(self.cues[3])
        self.play(FadeIn(m1, shift=LEFT * 0.2), run_time=0.6)
        self.at(self.cues[4])
        self.play(Create(avg), FadeIn(avg_t), run_time=0.8)
        self.at(self.cues[5])
        self.play(Create(pk), FadeIn(pk_t), FadeIn(m2, shift=LEFT * 0.2), run_time=0.8)
        f = T("P_ort = P_burst + 10·log₁₀ D   ·   D = 0,1  ⇒  −10 dB", 24, TXT, BOLD).to_edge(DOWN, buff=0.6)
        self.at(self.cues[6])
        self.play(Write(f), run_time=1.3)
        self.end(pad=0.1)

        # p17 — burst-aware meter, test mode, pass-through in the field
        self.beat("p17")
        self.play(FadeOut(VGroup(ax, yl, xl, wave, avg, avg_t, pk, pk_t, m1, f)), m2.animate.move_to([0, 0.2, 0]), run_time=0.7)
        mode = pill("alternatif: ONU test modu → sürekli yayın (CW)", MUTED, 18).move_to([0, -1.1, 0])
        self.at(self.cues[2])
        self.play(FadeIn(mode, shift=UP * 0.15), run_time=0.6)
        self.at(self.cues[3] - 0.2)
        olt = box(1.4, 0.9, "OLT", "#3B4A75", 22).move_to([-5.3, -2.3, 0])
        onu = box(1.4, 0.9, "ONU", CH[1], 22).move_to([5.3, -2.3, 0])
        ppm = box(2.6, 1.0, "araya giren PON ölçer", GOOD, 17).move_to([0, -2.3, 0])
        l1 = Line(olt.get_right(), ppm.get_left(), color=FEED, stroke_width=4)
        l2 = Line(ppm.get_right(), onu.get_left(), color=FEED, stroke_width=4)
        self.play(FadeOut(mode), m2.animate.scale(0.75).move_to([0, 0.9, 0]), FadeIn(olt), FadeIn(onu), Create(l1), Create(l2), run_time=0.8)
        # downstream off -> ONU silent
        x = Cross(Square(0.5), stroke_color=WARN, stroke_width=6).move_to(l1)
        silent = T("aşağı yön yok → ONU susar", 20, WARN, BOLD).next_to(onu, UP, buff=0.25)
        self.at(self.cues[5] - 0.4)
        self.play(Create(x), FadeIn(silent), onu[0].animate.set_stroke(color=MUTED), run_time=0.8)
        self.at(self.cues[6])
        lnk = DashedLine(ppm.get_top(), m2.get_bottom(), color=GOOD, stroke_width=2, dash_length=0.08)
        self.play(FadeOut(x), FadeOut(silent), onu[0].animate.set_stroke(color=CH[1]), FadeIn(ppm, scale=0.9), Create(lnk), run_time=0.7)
        dsl = Line(olt.get_right(), onu.get_left())
        usl = Line(onu.get_left(), olt.get_right())
        for _ in range(2):
            d = glow_dot(WHITE, 0.06).move_to(dsl.get_start())
            u = Rectangle(width=0.36, height=0.18, stroke_width=0, fill_color=CH[1], fill_opacity=1).move_to(usl.get_start())
            self.play(MoveAlongPath(d, dsl), MoveAlongPath(u, usl), Circumscribe(ppm, color=GOOD, buff=0.08), run_time=1.1, rate_func=linear)
            self.remove(d, u)
        self.end(pad=0.1)

        # p18 — engineer's note
        self.beat("p18")
        self.clear(rt=0.5)
        self.set_badge("not")
        n1 = self.note("1", "Ayırıcı kaybı", "İdeal 10·log₁₀N değil: üreticinin en kötü durum\nekleme kaybı + kollar arası düzgünsüzlük.")
        n2 = self.note("2", "Burst gücü", "İlk soru: bu ölçer ortalamayı mı,\nyoksa burst'ü mü okuyor?")
        VGroup(n1, n2).arrange(DOWN, buff=0.45).move_to(DOWN * 0.3)
        self.at(self.cues[1])
        self.play(FadeIn(n1, shift=UP * 0.25), run_time=0.7)
        self.at(self.cues[3])
        self.play(FadeIn(n2, shift=UP * 0.25), run_time=0.7)
        self.end(pad=0.1)

        # p19 — recap + bridge to Perde 2
        self.beat("p19")
        self.clear(rt=0.5)
        self.play(FadeOut(self.badge), run_time=0.3)
        self.badge = VGroup()
        cards = VGroup(*[P1A.problem_card(self, k) for k in range(3)]).arrange(RIGHT, buff=0.55).move_to(UP * 0.5)
        checks = VGroup(*[T("✓", 40, GOOD, BOLD).next_to(c[0].get_corner(UR), DL, buff=0.15) for c in cards])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=1.3)
        self.at(self.cues[2])
        self.play(LaggedStart(*[FadeIn(c, scale=1.4) for c in checks], lag_ratio=0.35), run_time=1.6)
        self.at(self.cues[3])
        q = VGroup(T("Sıradaki soru", 22, ACC, BOLD), T("Daha fazla hız gerektiğinde: tek dalga boyunu hızlandırmak mı,\nyoksa yeni renkler eklemek mi?", 26, TXT, SEMIBOLD, line_spacing=0.9)
                   ).arrange(DOWN, buff=0.15).move_to(DOWN * 2.45)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.5)
        self.play(FadeOut(VGroup(cards, checks, q)), run_time=0.6)
        self.save_timeline("ep01_p1F")

    def meter(self, name, val, sub, color):
        b = RoundedRectangle(corner_radius=0.14, width=3.6, height=1.6, stroke_color=color, stroke_width=2.5, fill_color="#0D1426", fill_opacity=1)
        g = VGroup(T(name, 18, MUTED, SEMIBOLD), T(val, 36, color, BOLD), T(sub, 15, MUTED)).arrange(DOWN, buff=0.08).move_to(b)
        return VGroup(b, g)

    def note(self, num, title, body):
        r = RoundedRectangle(corner_radius=0.18, width=11.0, height=1.9, stroke_color="#F472B6", stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
        n = T(num, 54, "#F472B6", BOLD).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.5)
        g = VGroup(T(title, 26, TXT, BOLD), T(body, 21, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g.next_to(n, RIGHT, buff=0.5)
        return VGroup(r, n, g)
