"""B06 shared helpers: burst envelope, eye mask, ER/power region — builds on B05 framework."""
import math
import sys

from ep05_common import *

EP6 = SERIES["episodes"][5]
H6 = {1: "BÖLÜM 6 · PERDE 1 — Burst modunun temeli",
      2: "BÖLÜM 6 · PERDE 2 — Karanlıkta güç",
      3: "BÖLÜM 6 · PERDE 3 — Burst'ün şekli",
      4: "BÖLÜM 6 · PERDE 4 — Burst'ün içi: PSBu, profil, FEC",
      "L": "BÖLÜM 6 · LABORATUVARDA — Burst'ü ölçmek", "E": "BÖLÜM 6 · KAPANIŞ"}

# color roles for the episode (do NOT shadow manim's UP/DOWN/LEFT/RIGHT)
BURST = TW_US          # upstream burst (purple)
LEAK = "#FB923C"       # leakage / dark power (amber-orange)
DARK = "#64748B"       # idle / silent ONU (slate)
ONE, ZERO = GOOD, WARN  # '1' and '0' levels


def M6(p):
    return f"build/ep06/{p}/audio_proc/manifest.json"


class Act6(Act5):
    pass


# ---------- burst power-vs-time envelope -------------------------------------
def burst_env(x0, ybase, yhi, color=BURST, widths=None):
    """Trapezoidal burst envelope: guard→on-ramp→preamble→delimiter→payload→off-ramp→guard.
    Returns (VGroup drawing, edges dict {name:(xL,xR)}, x_end)."""
    W = widths or {"g0": 0.55, "on": 0.5, "pre": 1.45, "dlm": 0.5, "pay": 3.0, "off": 0.5, "g1": 0.55}
    seq = [("g0", 0, 0), ("on", 0, 1), ("pre", 1, 1), ("dlm", 1, 1), ("pay", 1, 1), ("off", 1, 0), ("g1", 0, 0)]
    x, pts, edges = x0, [], {}
    for name, l0, l1 in seq:
        w = W[name]
        edges[name] = (x, x + w)
        pts.append([x, ybase + (yhi - ybase) * l0, 0])
        pts.append([x + w, ybase + (yhi - ybase) * l1, 0])
        x += w
    curve = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(pts)
    poly = Polygon(*([[x0, ybase, 0]] + pts + [[x, ybase, 0]]), stroke_width=0, fill_color=color, fill_opacity=0.16)
    return VGroup(poly, curve), edges, x


def seg_label(edges, name, text, color, y, size=15, up=True, buff=0.12):
    xL, xR = edges[name]
    xc = (xL + xR) / 2
    t = T(text, size, color, BOLD)
    t.next_to([xc, y, 0], UP if up else DOWN, buff=buff)
    return t


def brace_seg(edges, name, y, text, color=MUTED, size=14, direction=DOWN):
    xL, xR = edges[name]
    br = BraceBetweenPoints([xL, y, 0], [xR, y, 0], direction, color=color)
    return VGroup(br, T(text, size, color, BOLD).next_to(br, direction, buff=0.05))


# ---------- transmitter eye mask (representative) ----------------------------
def eye_mask(cx, cy, w, h, color=GOLD):
    """Central keep-out box (0.2 UI × 0.25..0.75) + top/bottom overshoot bands.
    Coordinates match lib/ep05 eye(cx, cy, w, h): one UI spans w/2, level 0..1 over h."""
    uiw = w / 2.0
    cbox = Rectangle(width=0.2 * uiw, height=0.5 * h, stroke_color=color, stroke_width=2.5,
                     fill_color=color, fill_opacity=0.16).move_to([cx, cy, 0])
    top = Rectangle(width=uiw, height=0.25 * h, stroke_width=0, fill_color=color, fill_opacity=0.13).move_to([cx, cy + 0.625 * h, 0])
    bot = Rectangle(width=uiw, height=0.25 * h, stroke_width=0, fill_color=color, fill_opacity=0.13).move_to([cx, cy - 0.625 * h, 0])
    return VGroup(cbox, top, bot)


# ---------- NRZ bit pattern (filled) -----------------------------------------
def nrz_fill(bits, x0, tb, ylo, yhi, color=BURST, op=0.16):
    pts = nrz(bits, x0, tb, ylo, yhi)
    curve = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(pts)
    poly = Polygon(*([[x0, ylo, 0]] + pts + [[x0 + len(bits) * tb, ylo, 0]]), stroke_width=0, fill_color=color, fill_opacity=op)
    return VGroup(poly, curve)
