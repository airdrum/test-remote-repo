"""B05 shared helpers: headers, manifests, axes, BER/jitter plots, state boxes."""
import math
import sys

from ep03_common import *

EP5 = SERIES["episodes"][4]
H5 = {1: "BÖLÜM 5 · PERDE 1 — Bütçenin alıcı tarafı", 2: "BÖLÜM 5 · PERDE 2 — X/S toleransı",
      3: "BÖLÜM 5 · PERDE 3 — Zaman ve ayar", 4: "BÖLÜM 5 · PERDE 4 — Senkron, FEC ve ilk adımlar",
      "L": "BÖLÜM 5 · LABORATUVARDA — Alıcı testleri", "E": "BÖLÜM 5 · KAPANIŞ"}
SIG, XC, YC, ZC = GOOD, WARN, GOLD, "#FB923C"   # target S · TWDM interferer X · reflected PtP Y · PtP downstream Z
STATE = "#A78BFA"


def M5(p):
    return f"build/ep05/{p}/audio_proc/manifest.json"


def tr(x, fmt="{:g}"):
    return fmt.format(x).replace(".", ",").replace("-", "−")


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


class Act5(Act3):
    def q(self, sub, default=0.0):
        """Start time (−0.2 s) of `sub` inside the current beat, interpolated within its phrase."""
        b = self.bmap[self.timeline[-1]["id"]]
        cues = b["cues"]
        for k, c in enumerate(cues):
            if sub in c["text"]:
                t1 = cues[k + 1]["t"] if k + 1 < len(cues) else b["duration"]
                frac = c["text"].index(sub) / max(len(c["text"]), 1)
                return max(0.0, c["t"] + frac * (t1 - c["t"]) - 0.2)
        print(f"CUE MISS [{b['id']}] {sub!r}", file=sys.stderr)
        return default

    def cue(self, sub, default=0.0):
        return self.q(sub, default)

    def ci(self, bid, sub, default=1):
        for i, c in enumerate(self.bmap[bid]["cues"]):
            if sub in c["text"]:
                return i
        print(f"CUE MISS [{bid}] {sub!r}", file=sys.stderr)
        return default

    def note5(self, bid, lines):
        return self.engineer_note(bid, [(n, t, b, self.ci(bid, s)) for n, t, b, s in lines])

    def bridge_beat(self, bid, text, label="Sıradaki", pad=0.4):
        self.beat(bid)
        self.clear()
        self.drop_badge()
        b = self.bridge(label, text)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.8)
        self.end(pad=pad)
        self.play(FadeOut(b), run_time=0.5)


# ---------- axes --------------------------------------------------------------
def lin_axis(v0, v1, x0, x1, y, ticks, labels=None, size=14, color=MUTED, fmt=None, unit=None):
    """Horizontal linear axis. Returns (VGroup(line, ticks, labels[, unit]), X)."""
    fmt = fmt or (lambda v: tr(v))
    X = lambda v: x0 + (v - v0) / (v1 - v0) * (x1 - x0)
    ax = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2)
    tk = VGroup(*[Line([X(v), y - 0.06, 0], [X(v), y + 0.06, 0], color=color, stroke_width=1.5) for v in ticks])
    lb = VGroup(*[T(fmt(v), size, color).next_to([X(v), y, 0], DOWN, buff=0.1) for v in (ticks if labels is None else labels)])
    g = VGroup(ax, tk, lb)
    if unit:
        g.add(T(unit, size, color).next_to(lb, DOWN, buff=0.12).set_x((x0 + x1) / 2))
    return g, X


def v_axis(v0, v1, y0, y1, x, ticks, labels=None, size=14, color=MUTED, fmt=None):
    """Vertical linear axis with labels on the left. Returns (VGroup, Y)."""
    fmt = fmt or (lambda v: tr(v))
    Y = lambda v: y0 + (v - v0) / (v1 - v0) * (y1 - y0)
    ax = Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=2)
    tk = VGroup(*[Line([x - 0.06, Y(v), 0], [x + 0.06, Y(v), 0], color=color, stroke_width=1.5) for v in ticks])
    lb = VGroup(*[T(fmt(v), size, color).next_to([x, Y(v), 0], LEFT, buff=0.1) for v in (ticks if labels is None else labels)])
    return VGroup(ax, tk, lb), Y


def log_axis(f0, f1, x0, x1, y, ticks, size=14, color=MUTED):
    """Horizontal log axis; ticks = [(value, label)]. Returns (VGroup, X)."""
    X = lambda f: x0 + (math.log10(f) - math.log10(f0)) / (math.log10(f1) - math.log10(f0)) * (x1 - x0)
    ax = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2)
    tk = VGroup(*[Line([X(v), y - 0.06, 0], [X(v), y + 0.06, 0], color=color, stroke_width=1.5) for v, _ in ticks])
    lb = VGroup(*[T(s, size, color).next_to([X(v), y, 0], DOWN, buff=0.1) for v, s in ticks])
    return VGroup(ax, tk, lb), X


def lobe(X, c, y0, h, sig, color, op=0.3, sw=2.5):
    """Gaussian-ish channel spectrum around c (in axis units)."""
    xs = np.linspace(c - 3 * sig, c + 3 * sig, 36)
    pts = [[X(x), y0 + h * np.exp(-((x - c) / sig) ** 2 / 2), 0] for x in xs]
    curve = VMobject(stroke_color=color, stroke_width=sw).set_points_smoothly(pts)
    fill = Polygon(*([[X(xs[0]), y0, 0]] + pts + [[X(xs[-1]), y0, 0]]), stroke_width=0, fill_color=color, fill_opacity=op)
    return VGroup(fill, curve)


# ---------- BER on a Q scale ----------------------------------------------------
def q_of(ber):
    lo, hi = 0.0, 12.0
    for _ in range(60):
        m = (lo + hi) / 2
        if 0.5 * math.erfc(m / math.sqrt(2)) > ber:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def sup(n):
    return "10" + "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(d)] if d.isdigit() else "⁻" for d in str(n))


# ---------- eye diagram ---------------------------------------------------------
def eye(cx, cy, w, h, color, isi=0.0, sw=2.2, op=0.75):
    st = lambda u: 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0, 1))
    g = VGroup()
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                lb = b + isi * ((a + c) / 2 - b)
                la = a + isi * ((b) - a) * 0.5
                lc = c + isi * ((b) - c) * 0.5
                lvl = lambda x, la=la, lb=lb, lc=lc: la + (lb - la) * st((x + 0.25) / 0.5) + (lc - lb) * st((x - 0.75) / 0.5)
                pts = [[cx + w * (x - 0.5) / 2, cy + h * (lvl(x) - 0.5), 0] for x in np.linspace(-0.5, 1.5, 70)]
                g.add(VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=op, fill_opacity=0).set_points_smoothly(pts))
    return g


# ---------- diagram pieces --------------------------------------------------------
def sbox(title, sub=None, color=STATE, w=2.3, h=0.85, tsize=20, ssize=15, fill=PANEL):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    parts = [T(title, tsize, TXT, BOLD)]
    if sub:
        parts.append(T(sub, ssize, color, SEMIBOLD))
    t = VGroup(*parts).arrange(DOWN, buff=0.06)
    if t.width > w - 0.2:
        t.scale_to_fit_width(w - 0.2)
    return VGroup(r, t.move_to(r))


def arrow(p0, p1, color=MUTED, sw=2.5, tip=0.16, buff=0.0):
    return Arrow(np.array(p0, dtype=float), np.array(p1, dtype=float), buff=buff, color=color, stroke_width=sw,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=20)


def carrow(p0, p1, angle, color=MUTED, sw=2.5, tip=0.16):
    return CurvedArrow(np.array(p0, dtype=float), np.array(p1, dtype=float), angle=angle, color=color, stroke_width=sw, tip_length=tip)


def instr(kind, w=2.15, h=1.55, l1=None, l2=None, c1=ACC):
    """lib.instrument with replaceable screen text (PM/BERT)."""
    g = instrument(kind, w, h)
    if l1 is not None:
        scr = g[1]
        new = VGroup(T(l1, 15 * w / 2.15, c1, BOLD).move_to(scr).shift(UP * 0.07 * h / 1.55))
        if l2:
            new.add(T(l2, 10 * w / 2.15, MUTED).move_to(scr).shift(DOWN * 0.17 * h / 1.55))
        for m in new:
            if m.width > scr.width - 0.1:
                m.scale_to_fit_width(scr.width - 0.1)
        g.submobjects[2] = new
    return g


def bitrow(bits, cols, size=0.42, fs=18):
    cells = VGroup(*[VGroup(Square(size, stroke_color=c, stroke_width=2, fill_color=PANEL, fill_opacity=1), T(b, fs, c, BOLD)) for b, c in zip(bits, cols)])
    for c in cells:
        c[1].move_to(c[0])
    return cells.arrange(RIGHT, buff=0.04)


def check_list(lines, size=21, mark="✓", mcolor=GOOD, buff=0.3):
    return VGroup(*[VGroup(T(mark, size + 2, mcolor, BOLD), T(s, size, TXT)).arrange(RIGHT, buff=0.25) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def fit(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m
