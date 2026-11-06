"""Shared building blocks for episode acts (header, badges, cards, timing) — used from B01 Perde 2 onward."""
from lib import *

BADGE = {"std": ("Standart ne diyor", GOLD), "fiz": ("Fizik", ACC), "lab": ("Laboratuvarda", GOOD),
         "not": ("Mühendis notu", "#F472B6"), "tc": ("TC Köprüsü", "#A78BFA"), "ozet": ("Özet", ACC)}
FEED = "#CBD5E1"
PINK = "#F472B6"


def nrz(bits, x0, tb, ylo, yhi, rise=0.04):
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


def splitter(scale=0.42):
    return Triangle(color=FEED, fill_color=PANEL, fill_opacity=1, stroke_width=2.5).rotate(-PI / 2).scale(scale)


def card(title, body, ref=None, color=ACC, w=5.6, h=2.3, tsize=26, bsize=20):
    r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    parts = [T(title, tsize, color, BOLD), T(body, bsize, TXT, line_spacing=0.9)]
    if ref:
        parts.append(T(ref, 15, MUTED))
    g = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    g.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.3)
    return VGroup(r, *g)


def table(headers, rows, widths, size=19, hsize=17, row_h=0.5, hl=None):
    """Simple table: returns VGroup(header_row, row_1, …). Each row = VGroup(bg, cells…)."""
    W = sum(widths)
    out = VGroup()
    def row(cells, y, color, weight, fill, sz):
        bg = Rectangle(width=W, height=row_h, stroke_width=0, fill_color=fill, fill_opacity=1)
        xs = np.cumsum([0] + widths[:-1])
        g = VGroup(bg)
        for c, x, w in zip(cells, xs, widths):
            t = T(c, sz, color, weight)
            if t.width > w - 0.15:
                t.scale_to_fit_width(w - 0.15)
            t.move_to([x + 0.12 - W / 2, 0, 0], aligned_edge=LEFT)
            g.add(t)
        return g.shift(UP * y)
    out.add(row(headers, 0, MUTED, BOLD, "#16213A", hsize))
    for i, r in enumerate(rows):
        out.add(row(r, -(i + 1) * row_h, TXT, MEDIUM, PANEL if i % 2 == 0 else "#0E1628", size))
    return out


class Act(Narrated):
    HDR = ""
    FIRST = False
    PREV_BADGE = None

    def setup(self):
        super().setup()
        self.hdr = T(self.HDR, 20, MUTED, MEDIUM).to_corner(UL, buff=0.4)
        self.badge = self.src = None
        if not self.FIRST:
            self.add(self.hdr)
        if self.PREV_BADGE:
            s, c = BADGE[self.PREV_BADGE]
            self.badge = pill(s, c, 20).to_corner(UR, buff=0.35)
            self.add(self.badge)

    # --- chrome -------------------------------------------------------------
    def title_card(self, kick, title):
        k = T(kick, 26, ACC, BOLD)
        t = T(title, 72, TXT, BOLD)
        g = VGroup(k, t).arrange(DOWN, buff=0.2).move_to(UP * 0.3)
        self.play(FadeIn(k, shift=UP * 0.2), Write(t), run_time=1.3)
        return g

    def to_header(self, g, rt=0.7):
        self.play(ReplacementTransform(g, self.hdr), run_time=rt)

    def set_badge(self, key):
        s, c = BADGE[key]
        new = pill(s, c, 20).to_corner(UR, buff=0.35)
        if self.badge is None or len(self.badge) == 0:
            self.play(FadeIn(new, shift=LEFT * 0.2), run_time=0.4)
        else:
            self.play(FadeTransform(self.badge, new), run_time=0.4)
        self.badge = new

    def drop_badge(self):
        if self.badge is not None and len(self.badge):
            self.play(FadeOut(self.badge), run_time=0.3)
        self.badge = VGroup()

    def set_src(self, s):
        old = self.src
        if not s:
            self.src = None
            return FadeOut(old) if old is not None else Wait(0.05)
        new = T(s, 16, MUTED, MEDIUM).to_corner(DL, buff=0.35)
        self.src = new
        return FadeIn(new) if old is None else FadeTransform(old, new)

    def heading(self, s):
        return T(s, 36, TXT, BOLD).next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)

    def show_heading(self, s, old=None):
        h = self.heading(s)
        self.play(FadeTransform(old, h) if old is not None else FadeIn(h, shift=RIGHT * 0.2), run_time=0.5)
        return h

    def clear(self, *keep, rt=0.5):
        keep = set(keep) | {self.hdr, self.badge}
        out = [m for m in self.mobjects if m not in keep]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=rt)
        if self.src is not None and self.src not in keep:
            self.src = None

    # --- content helpers ----------------------------------------------------
    def quote(self, ref, en, tr_text, width=12.0):
        r = T(ref, 20, GOLD, BOLD)
        e = T(en, 19, MUTED, slant=ITALIC, line_spacing=0.9)
        t = T(tr_text, 25, TXT, SEMIBOLD)
        for m in (e, t):
            if m.width > width:
                m.scale_to_fit_width(width)
        g = VGroup(r, e, t).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        bar = Rectangle(width=0.06, height=g.height, stroke_width=0, fill_color=GOLD, fill_opacity=1).next_to(g, LEFT, buff=0.25)
        return VGroup(VGroup(bar, r), e, t)

    def note(self, num, title, body, w=11.0):
        r = RoundedRectangle(corner_radius=0.18, width=w, height=1.9, stroke_color=PINK, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
        n = T(num, 54, PINK, BOLD).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.5)
        g = VGroup(T(title, 26, TXT, BOLD), T(body, 21, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        g.next_to(n, RIGHT, buff=0.5)
        return VGroup(r, n, g)

    def bridge(self, label, question):
        q = VGroup(T(label, 22, ACC, BOLD), T(question, 30, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, buff=0.2)
        if q[1].width > 12.5:
            q[1].scale_to_fit_width(12.5)
        return q.move_to(ORIGIN)

    def engineer_note(self, beat_id, lines):
        """lines: [(num, title, body, cue_index)]"""
        self.beat(beat_id)
        self.clear()
        self.set_badge("not")
        notes = VGroup(*[self.note(n, t, b) for n, t, b, _ in lines]).arrange(DOWN, buff=0.4).move_to(DOWN * 0.3)
        for k, (_, _, _, ci) in enumerate(lines):
            self.at(self.cues[ci] if ci < len(self.cues) else 0)
            self.play(FadeIn(notes[k], shift=UP * 0.25), run_time=0.7)
        self.end(pad=0.15)
        return notes
