"""B08 shared helpers (OLT burst receiver / activation / power leveling) — builds on B06."""
import math
import sys

from ep06_common import *

EP8 = SERIES["episodes"][7]
H8 = {1: "BÖLÜM 8 · PERDE 1 — OLT burst alıcısı",
      2: "BÖLÜM 8 · PERDE 2 — Önsöz ekonomisi",
      3: "BÖLÜM 8 · PERDE 3 — Güç dengeleme",
      4: "BÖLÜM 8 · PERDE 4 — TC Köprüsü: ONU'nun ilk adımları",
      "L": "BÖLÜM 8 · LABORATUVARDA — Kalabalığı ölçmek", "E": "BÖLÜM 8 · KAPANIŞ"}

RX = ACC             # OLT receiver
NEAR, FAR = GOOD, WARN   # near ONU (strong) / far ONU (weak)


def M8(p):
    return f"build/ep08/{p}/audio_proc/manifest.json"


class Act8(Act6):
    pass


def burst_train(x0, ybase, heights, color=BURST, bw=0.9, gap=0.55, ramp=0.22):
    """A train of bursts of differing amplitude on a time axis (OLT's view).
    heights: list of 0..1 levels. Returns (VGroup, edges list [(xL,xR)], x_end)."""
    g = VGroup()
    x = x0
    edges = []
    for lev in heights:
        yhi = ybase + lev * 1.0
        pts = [[x, ybase, 0], [x + ramp, yhi, 0], [x + bw - ramp, yhi, 0], [x + bw, ybase, 0]]
        g.add(Polygon(*pts, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.35))
        edges.append((x, x + bw))
        x += bw + gap
    return g, edges, x - gap
