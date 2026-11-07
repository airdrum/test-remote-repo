"""B07 shared helpers (tunability / channel management) — builds on the B06 framework."""
import math
import sys

from ep06_common import *

EP7 = SERIES["episodes"][6]
H7 = {1: "BÖLÜM 7 · PERDE 1 — Ayarlanabilirlik",
      2: "BÖLÜM 7 · PERDE 2 — Ayar sırasında spektrum",
      3: "BÖLÜM 7 · PERDE 3 — Kalibrasyon",
      4: "BÖLÜM 7 · PERDE 4 — Kanal yönetimi",
      "L": "BÖLÜM 7 · LABORATUVARDA — Ayarı ölçmek", "E": "BÖLÜM 7 · KAPANIŞ"}

TUNE = PINK          # tuning / filter
LOCK = GOOD          # locked / stable


def M7(p):
    return f"build/ep07/{p}/audio_proc/manifest.json"


class Act7(Act6):
    pass


def chan_cells(n, xc, y, w=0.7, h=0.5, tgt=None, color=CH, buff=0.08, size=14):
    """Row of wavelength-channel cells λ1..λn; highlight index tgt (0-based)."""
    cells = VGroup()
    for i in range(n):
        c = color[i % len(color)] if tgt is None or i == tgt else MUTED
        op = 0.85 if (tgt is not None and i == tgt) else (0.5 if tgt is None else 0.25)
        r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=c, stroke_width=2,
                             fill_color=c, fill_opacity=op)
        cells.add(VGroup(r, T(f"λ{i + 1}", size, BG if op > 0.6 else c, BOLD).move_to(r)))
    return cells.arrange(RIGHT, buff=buff).move_to([xc, y, 0])
