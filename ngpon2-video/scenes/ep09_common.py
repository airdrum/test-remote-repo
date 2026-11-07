"""B09 shared helpers (PtP WDM · AMCC · Ek C) — builds on B05."""
import math
import sys

from ep05_common import *

EP9 = SERIES["episodes"][8]
H9 = {1: "BÖLÜM 9 · PERDE 1 — Mimari ve spektrum", 2: "BÖLÜM 9 · PERDE 2 — A ekinin tabloları",
      3: "BÖLÜM 9 · PERDE 3 — AMCC", 4: "BÖLÜM 9 · PERDE 4 — Düşük kayıplı PtP WDM",
      "L": "BÖLÜM 9 · LABORATUVARDA — PtP WDM ve AMCC ölçümleri", "E": "BÖLÜM 9 · KAPANIŞ"}

AMC = GOLD            # AMCC
OLTC = "#94A3B8"      # OLT boxes
CLS = ["N1", "N2", "E1", "E2"]
OPLMAX = [29, 31, 33, 35]
OPLMIN = [14, 16, 18, 20]


def M9(p):
    return f"build/ep09/{p}/audio_proc/manifest.json"


class Act9(Act5):
    pass


def sgn(v, d=None):
    """+3 / −1,5 / 0 with Turkish decimal comma and real minus sign."""
    s = tr(v) if d is None else tr(v, "{:." + str(d) + "f}")
    return ("+" + s) if v > 0 else s


# ---------- icons -------------------------------------------------------------
def awg_icon(w=1.2, h=1.5, color=PTP, label="AWG", n=4):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    c = r.get_center()
    fan = VGroup(*[Line(c + LEFT * w * 0.32, c + RIGHT * w * 0.32 + UP * h * (0.32 - 0.64 * k / (n - 1)), color=CH[k % 4], stroke_width=2)
                   for k in range(n)])
    t = T(label, 15, color, BOLD).next_to(r, DOWN, buff=0.08)
    return VGroup(r, fan, t)


def antenna(h=0.9, color=TXT):
    mast = Line(DOWN * h / 2, UP * h / 2, color=color, stroke_width=3)
    legs = VGroup(Line(DOWN * h / 2 + LEFT * 0.25, UP * h * 0.1, color=color, stroke_width=2.5),
                  Line(DOWN * h / 2 + RIGHT * 0.25, UP * h * 0.1, color=color, stroke_width=2.5))
    arcs = VGroup(*[Arc(radius=0.14 + 0.12 * k, start_angle=-PI / 4, angle=PI / 2, color=color, stroke_width=2).move_arc_center_to(UP * h / 2) for k in range(2)],
                  *[Arc(radius=0.14 + 0.12 * k, start_angle=3 * PI / 4, angle=PI / 2, color=color, stroke_width=2).move_arc_center_to(UP * h / 2) for k in range(2)])
    return VGroup(mast, legs, arcs)


def building(w=0.8, h=1.0, color=TXT):
    b = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    win = VGroup(*[Square(0.12, stroke_width=0, fill_color=color, fill_opacity=0.7).move_to(b.get_center() + [(-0.18 + 0.18 * i), (h / 2 - 0.22 - 0.25 * j), 0])
                   for i in range(3) for j in range(3)])
    return VGroup(b, win)


def xmark(m, color=WARN, sw=4):
    return VGroup(Line(m.get_corner(UL), m.get_corner(DR), color=color, stroke_width=sw),
                  Line(m.get_corner(DL), m.get_corner(UR), color=color, stroke_width=sw))


def tag(s, color, size=16):
    return T(s, size, color, BOLD)


# ---------- waveforms ----------------------------------------------------------
def overmod(x0, x1, ybase, h, amcc_bits, nbits=150, depth=0.18, er=0.15, color=PTP, seed=3, sw=1.4):
    """Over-modulated NRZ (optical power): payload levels (1 / er) scaled by (1 ± depth/2) per AMCC bit.
    Returns (payload_curve, envelope_top, envelope_bottom, env(x))."""
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, nbits)
    tb = (x1 - x0) / nbits
    na = len(amcc_bits)

    def env(x):
        k = min(int((x - x0) / (x1 - x0) * na), na - 1)
        return 1 + depth / 2 * (1 if amcc_bits[k] else -1)

    pts = []
    y = ybase + h * er * env(x0)
    for i, b in enumerate(bits):
        xs = x0 + i * tb
        e = env(xs + tb / 2)
        yt = ybase + h * (1.0 if b else er) * e
        pts += [[xs, y, 0], [xs + tb * 0.15, yt, 0]]
        y = yt
    pts.append([x1, y, 0])
    curve = VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(pts)
    top, bot = [], []
    for k in range(na):
        xa, xb = x0 + k * (x1 - x0) / na, x0 + (k + 1) * (x1 - x0) / na
        e = 1 + depth / 2 * (1 if amcc_bits[k] else -1)
        top += [[xa, ybase + h * e, 0], [xb, ybase + h * e, 0]]
        bot += [[xa, ybase + h * er * e, 0], [xb, ybase + h * er * e, 0]]
    et = VMobject(stroke_color=AMC, stroke_width=3).set_points_as_corners(top)
    eb = VMobject(stroke_color=AMC, stroke_width=2, stroke_opacity=0.7).set_points_as_corners(bot)
    return curve, et, eb, env


def ask(x0, x1, yc, amps, cycles_per_bit=3.9, color=AMC, sw=2.2, n=40):
    """ASK on a sinusoidal carrier: amps per bit (scene units)."""
    nb = len(amps)
    tb = (x1 - x0) / nb
    pts = []
    for i, a in enumerate(amps):
        for x in np.linspace(0, 1, n, endpoint=False):
            xx = x0 + (i + x) * tb
            ph = 2 * np.pi * cycles_per_bit * (i + x)
            pts.append([xx, yc + a * np.sin(ph), 0])
    pts.append([x1, yc + amps[-1] * np.sin(2 * np.pi * cycles_per_bit * nb), 0])
    return VMobject(stroke_color=color, stroke_width=sw).set_points_smoothly(pts)


def frame_bar(segs, x0, y, h=0.62, size=16):
    """segs: [(label, width, color)] → VGroup of VGroup(rect, label) laid left→right from x0."""
    g = VGroup()
    x = x0
    for lab, w, c in segs:
        r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.22).move_to([x + w / 2, y, 0])
        t = T(lab, size, TXT, BOLD)
        if t.width > w - 0.08:
            t.scale_to_fit_width(max(w - 0.08, 0.1))
        g.add(VGroup(r, t.move_to(r)))
        x += w
    return g


# ---------- BER curves (Q scale) -------------------------------------------------
Q12 = q_of(1e-12)


def ber_axes(o, w, h, p0, p1, q0=3.0, q1=7.6, exps=(-3, -4, -6, -9, -12), xl="alınan güç (dBm)"):
    o = np.array(o, dtype=float)
    X = lambda p: o[0] + (p - p0) / (p1 - p0) * w
    Y = lambda q: o[1] + (q - q0) / (q1 - q0) * h
    g = VGroup(Line(o, o + [w, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, h, 0], color=MUTED, stroke_width=2))
    for e in exps:
        y = Y(q_of(10.0 ** e))
        g.add(Line([o[0] - 0.06, y, 0], [o[0] + 0.06, y, 0], color=MUTED, stroke_width=1.5), T(sup(e), 15, MUTED).next_to([o[0], y, 0], LEFT, buff=0.1))
    g.add(T(xl, 14, MUTED).next_to(o + [w * 0.72, 0, 0], DOWN, buff=0.12), T("BER (Q ölçeği)", 14, MUTED).next_to(o + [0, h, 0], RIGHT, buff=0.12))
    return g, X, Y


def ber_curve(X, Y, ps, qs, slope, p_lo, p_hi, color, npts=5, seed=1, r=0.06):
    """Straight line on the Q scale through (ps, Q(qs)) with `slope` (Q per dB), plus measured dots."""
    rng = np.random.default_rng(seed)
    q = lambda p: qs + slope * (p - ps)
    line = Line([X(p_lo), Y(q(p_lo)), 0], [X(p_hi), Y(q(p_hi)), 0], color=color, stroke_width=2.6)
    pts = np.linspace(p_lo + 0.3, p_hi - 0.3, npts)
    dots = VGroup(*[Dot([X(p), Y(q(p) + 0.05 * rng.standard_normal()), 0], radius=r, color=color) for p in pts])
    return line, dots
