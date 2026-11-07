"""S2·B2 (ep12) shared helpers — 'Çerçeve': PHY adaptation and framing (G.989.3 §8, §10, Ek A/B, Ek III/IV).

Builds on the season-2 blocks of ep11_common (field diagrams, ID range bars, pipeline segments, analyzer panels,
episode chips, monospace hex); only episode-specific names and a few frame/burst helpers are added here."""
from ep11_common import *

K12 = 2
EP12 = SERIES["season2"]["episodes"][K12 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep12_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K12}"
H12 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M12(p):
    return f"build/ep12/{p}/audio_proc/manifest.json"


M = M12

# PSBd parts · FS header parts · burst parts
PSC, SFCC, OCC, HECC = "#A78BFA", ACC, GOLD, "#94A3B8"
HLC, BWC, PLDC, PAYC, BIPC = "#94A3B8", EMB, PLC, SAC, "#94A3B8"
PARC = PINK                       # FEC parity bytes
PSYNC = "C5E51840FD59BB49"
PSYNC_BITS = format(int(PSYNC, 16), "064b")
TQNS = "12,86 ns"


def strip(parts, x0, y, h=0.55, size=15):
    """Left-anchored row of segments; parts = [(w, label, color[, op[, dashed]])]."""
    g = VGroup()
    x = x0
    for p in parts:
        w, lab, c = p[:3]
        op = p[3] if len(p) > 3 else 0.22
        dashed = p[4] if len(p) > 4 else False
        g.add(seg(x, w, y, c, lab, h, op, size, BG if op >= 0.5 else TXT, dashed))
        x += w
    return g


def bitcells(bits, w, h=0.32, on=PSC, off="#0B1220", sw=1.2, stroke=None):
    """One square-ish cell per bit (filled for 1), width w in total, centred at origin."""
    n = len(bits)
    cw = w / n
    g = VGroup()
    for i, b in enumerate(bits):
        g.add(Rectangle(width=cw, height=h, stroke_color=stroke or on, stroke_width=sw,
                        fill_color=on if b == "1" else off, fill_opacity=0.85 if b == "1" else 1).move_to([-w / 2 + cw * (i + 0.5), 0, 0]))
    return g


def num_rows(rows, size=18, gap=0.38, w=None, nsize=None):
    """[(tagtext, color, body)] → aligned rows: coloured tag + body text."""
    out = VGroup()
    for t, c, body in rows:
        a = tag(t, c, nsize or size - 2)
        b = T(body, size, TXT)
        out.add(VGroup(a, b))
    tw = max(r[0].width for r in out)
    for r in out:
        r[1].next_to(r[0], RIGHT, buff=0.25)
        r[1].set_x(r[0].get_left()[0] + tw + 0.25 + r[1].width / 2)
    out.arrange(DOWN, aligned_edge=LEFT, buff=gap - 0.3)
    for r in out:
        r[1].set_x(r[0].get_left()[0] + tw + 0.25 + r[1].width / 2)
    if w is not None:
        fit(out, w)
    return out


def ok_line(s, ok=True, size=18, color=None):
    return VGroup(T("✓" if ok else "✗", size + 2, GOOD if ok else WARN, BOLD), T(s, size, color or TXT)).arrange(RIGHT, buff=0.2)


def mtable(headers, rows, widths, size=18, hsize=16, row_h=0.5, mono=()):
    """kit.table with monospace (HX) cells in the columns listed in `mono`."""
    W = sum(widths)
    out = VGroup()

    def row(cells, y, color, weight, fill, sz, head):
        bg = Rectangle(width=W, height=row_h, stroke_width=0, fill_color=fill, fill_opacity=1)
        xs = np.cumsum([0] + widths[:-1])
        g = VGroup(bg)
        for k, (c, x, w) in enumerate(zip(cells, xs, widths)):
            if c == "":
                g.add(VGroup().move_to([x + 0.12 - W / 2, 0, 0]))
                continue
            t = HX(c, sz - 1, color, weight) if (k in mono and not head) else T(c, sz, color, weight)
            if t.width > w - 0.15:
                t.scale_to_fit_width(w - 0.15)
            t.move_to([x + 0.12 - W / 2, 0, 0], aligned_edge=LEFT)
            g.add(t)
        return g.shift(UP * y)
    out.add(row(headers, 0, MUTED, BOLD, "#16213A", hsize, True))
    for i, r in enumerate(rows):
        out.add(row(r, -(i + 1) * row_h, TXT, MEDIUM, PANEL if i % 2 == 0 else "#0E1628", size, False))
    return out


def step_head(scene, n, s, old=None):
    t = VGroup(pill(f"TEST {n}", GOOD, 18), T(s, 32, TXT, BOLD)).arrange(RIGHT, buff=0.3)
    t.next_to(scene.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
    fit(t, 11.6)
    scene.play(FadeTransform(old, t) if old is not None else FadeIn(t, shift=RIGHT * 0.2), run_time=0.5)
    return t


def zoom_lines(src, dst, color=MUTED):
    """Two dashed lines from the bottom corners of src to the top corners of dst."""
    return VGroup(DashedLine(src.get_corner(DL), dst.get_corner(UL), color=color, stroke_width=1.5, dash_length=0.08),
                  DashedLine(src.get_corner(DR), dst.get_corner(UR), color=color, stroke_width=1.5, dash_length=0.08))


def interp(s="yorum", color=GOLD, size=15):
    return tag(s, color, size)


class SyncSM:
    """G.989.3 Fig. 10-4 reference DS sync machine on one row: Av → Ön senkron → Senkron ⇄ Yeniden senkron."""

    def __init__(self, y=0.85, xs=(-5.05, -1.7, 1.65, 5.0), w=2.55, h=0.9):
        names = [("Av", "Hunt"), ("Ön senkron", "Pre-Sync"), ("Senkron", "Sync"), ("Yeniden senkron", "Re-Sync")]
        self.y = y
        self.b = [sbox(a, b, STATE, w, h, 20, 15).move_to([x, y, 0]) for (a, b), x in zip(names, xs)]
        H, P, S, R = self.b
        u, d = UP * 0.18, DOWN * 0.18
        lab = lambda s, c, p: T(s, 15, c, BOLD).move_to(p)
        m1, m2, m3 = (xs[0] + xs[1]) / 2, (xs[1] + xs[2]) / 2, (xs[2] + xs[3]) / 2
        self.hp = VGroup(arrow(H.get_right() + u, P.get_left() + u, GOOD, 2.5, 0.12), lab("64/64 + SFC ✓", GOOD, [m1, y + 0.76, 0]))
        self.ph = VGroup(arrow(P.get_left() + d, H.get_right() + d, WARN, 2.5, 0.12), lab("biri ✗", WARN, [m1, y - 0.72, 0]))
        self.ps = VGroup(arrow(P.get_right() + u, S.get_left() + u, GOOD, 2.5, 0.12), lab("ikisi ✓", GOOD, [m2, y + 0.76, 0]))
        loop = CurvedArrow(S.get_top() + LEFT * 0.5, S.get_top() + RIGHT * 0.5, angle=-PI * 1.1, color=GOOD, stroke_width=2.5, tip_length=0.12)
        self.ss = VGroup(loop, lab("ikisi ✓", GOOD, [S.get_x(), y + 1.3, 0]))
        self.sr = VGroup(arrow(S.get_right() + u, R.get_left() + u, WARN, 2.5, 0.12), lab("biri ✗", WARN, [m3, y + 0.76, 0]))
        self.rs = VGroup(arrow(R.get_left() + d, S.get_right() + d, GOOD, 2.5, 0.12), lab("ikisi ✓", GOOD, [m3, y - 0.72, 0]))
        arc = CurvedArrow(R.get_bottom() + RIGHT * 0.3, H.get_bottom() + LEFT * 0.3, angle=-0.62, color=WARN, stroke_width=3, tip_length=0.15)
        self.rh = VGroup(arc, lab("M − 1 ardışık ✗", WARN, [0, y - 1.62, 0]))
        self.hh = VGroup(CurvedArrow(H.get_top() + LEFT * 0.5, H.get_top() + RIGHT * 0.5, angle=-PI * 1.1, color=MUTED, stroke_width=2.2, tip_length=0.11),
                         lab("ara", MUTED, [H.get_x(), y + 1.3, 0]))

    def boxes(self):
        return VGroup(*self.b)

    def all(self):
        return VGroup(*self.b, self.hp, self.ph, self.ps, self.ss, self.sr, self.rs, self.rh)


def glow(m, color=GOLD, buff=0.08):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=4, corner_radius=0.16)


class Act12(Act11):
    def title_card(self, kick, title):
        k = T(kick, 26, ACC, BOLD)
        t = fit(T(title, 72, TXT, BOLD), 12.8)
        g = VGroup(k, t).arrange(DOWN, buff=0.2).move_to(UP * 0.3)
        self.play(FadeIn(k, shift=UP * 0.2), Write(t), run_time=1.3)
        return g

    def heading12(self, s, old=None, w=None):
        h = self.heading(s)
        if w:
            fit(h, w)
            h.next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeTransform(old, h) if old is not None else FadeIn(h, shift=RIGHT * 0.2), run_time=0.5)
        return h
