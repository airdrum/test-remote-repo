"""Shared visual language + narration-sync helpers for the LAMBDA series."""
import json
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
BG, PANEL, LINE = "#0A0F1E", "#111A2E", "#2A3658"
TXT, MUTED, ACC, WARN, GOOD, GOLD = "#E6ECFF", "#8A97B8", "#5EEAD4", "#F87171", "#86EFAC", "#FBBF24"
CH = ["#8B5CF6", "#22D3EE", "#34D399", "#F59E0B"]  # λ1..λ4 — fixed for the whole season
LEGACY = "#64748B"
FONT = "Inter"
config.background_color = BG
SERIES = json.loads((ROOT / "plan/episodes.json").read_text())


def T(s, size=28, color=TXT, weight=NORMAL, **kw):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **kw)


def box(w, h, label=None, color=LINE, size=24, fill=PANEL, weight=SEMIBOLD, r=0.12):
    rr = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=2.5,
                          fill_color=fill, fill_opacity=1)
    return rr if label is None else VGroup(rr, T(label, size, TXT, weight).move_to(rr))


def pill(s, color=ACC, size=22, fill=BG):
    t = T(s, size, color, SEMIBOLD)
    r = RoundedRectangle(corner_radius=0.22, width=t.width + 0.5, height=t.height + 0.32,
                         stroke_color=color, stroke_width=2, fill_color=fill, fill_opacity=0.9)
    return VGroup(r, t.move_to(r))


def glow_dot(color, r=0.08, layers=5):
    """Soft glowing point (stacked translucent discs)."""
    return VGroup(*[Dot(radius=r * (1 + 1.6 * k), color=color, fill_opacity=0.9 / (1 + 2.2 * k))
                    for k in reversed(range(layers))])


class Narrated(Scene):
    """Scene whose timing is driven by per-beat TTS clips (manifest from tools/prep_audio.py)."""
    MANIFEST = None  # path relative to ROOT

    def setup(self):
        self.man = json.loads((ROOT / self.MANIFEST).read_text()) if self.MANIFEST else None
        self.bmap = {b["id"]: b for b in self.man["beats"]} if self.man else {}
        self.timeline, self.bi = [], -1

    def beat(self, key=None):
        self.bi += 1
        b = self.bmap[key] if key else self.man["beats"][self.bi]
        self.add_sound(b["file"])
        self.b0, self.bdur = self.renderer.time, b["duration"]
        self.cues = [c["t"] for c in b["cues"]]
        self.timeline.append({"id": b["id"], "start": round(self.b0, 3), "dur": b["duration"], "text": b["text"]})

    def at(self, t):
        dt = self.b0 + t - self.renderer.time
        if dt > 1 / 30:
            self.wait(dt)

    EXTRA_PAD = float(__import__('os').environ.get('EXTRA_PAD', '0.35'))

    def end(self, pad=0.25):
        self.at(self.bdur + pad + self.EXTRA_PAD)

    def save_timeline(self, name):
        (ROOT / f"build/{name}_timeline.json").write_text(json.dumps(self.timeline, ensure_ascii=False, indent=1))


# ---------- reusable instrument tiles (test bench) ----------
def _screen(w, h):
    return Rectangle(width=w, height=h, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1)


def instrument(kind, w=2.15, h=1.55):
    """Small stylised instrument: OSA, DCA, BERT, PM (burst power meter), VOA, OSC."""
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2,
                            fill_color="#0D1426", fill_opacity=1)
    scr = _screen(w * 0.78, h * 0.52).move_to(body).shift(UP * h * 0.1)
    x0, x1 = scr.get_left()[0] + 0.08, scr.get_right()[0] - 0.08
    y0, y1 = scr.get_bottom()[1] + 0.06, scr.get_top()[1] - 0.06
    g = VGroup()
    if kind == "OSA":
        for i, c in enumerate(CH):
            cx = x0 + (i + 1) * (x1 - x0) / 5
            g.add(FunctionGraph(lambda x, cx=cx: y0 + (y1 - y0) * np.exp(-((x - cx) / 0.035) ** 2),
                                x_range=[cx - 0.15, cx + 0.15], color=c, stroke_width=2))
        g.add(Line([x0, y0, 0], [x1, y0, 0], color="#64748B", stroke_width=1))
        name = "OSA"
    elif kind == "DCA":
        xs = np.linspace(x0, x1, 60); mid, a = (y0 + y1) / 2, (y1 - y0) / 2 * 0.85
        for s in (1, -1):
            g.add(VMobject(color=GOOD, stroke_width=1.6).set_points_smoothly(
                [[x, mid + s * a * np.cos(np.pi * (x - x0) / (x1 - x0) * 2), 0] for x in xs]))
        g.add(Line([x0, mid + a, 0], [x1, mid + a, 0], color=GOOD, stroke_width=1.6),
              Line([x0, mid - a, 0], [x1, mid - a, 0], color=GOOD, stroke_width=1.6))
        name = "DCA (göz)"
    elif kind == "BERT":
        g.add(T("BER 1,0E-12", 13, GOOD, BOLD).move_to(scr).shift(UP * 0.08), T("PRBS31", 10, MUTED).move_to(scr).shift(DOWN * 0.16))
        name = "BERT"
    elif kind == "PM":
        g.add(T("−18,2 dBm", 16, ACC, BOLD).move_to(scr).shift(UP * 0.06), T("burst · 1536 nm", 9, MUTED).move_to(scr).shift(DOWN * 0.17))
        name = "Güç ölçer"
    elif kind == "VOA":
        g.add(T("12,0 dB", 16, GOLD, BOLD).move_to(scr))
        knob = Circle(radius=0.13, color="#94A3B8", stroke_width=2).move_to(body).shift(DOWN * h * 0.3 + RIGHT * w * 0.3)
        g.add(knob, Line(knob.get_center(), knob.get_center() + 0.12 * UR / np.sqrt(2), color="#94A3B8", stroke_width=2))
        name = "VOA"
    else:  # OSC
        pts = [[x0, y0 + 0.05, 0], [x0 + 0.35 * (x1 - x0), y0 + 0.05, 0]]
        for k in range(30):
            tt = k / 29
            xx = x0 + (0.35 + 0.65 * tt) * (x1 - x0)
            yy = y0 + 0.05 + (y1 - y0 - 0.15) * (1 - np.exp(-6 * tt) * np.cos(18 * tt))
            pts.append([xx, yy, 0])
        g.add(VMobject(color=CH[1], stroke_width=1.8).set_points_as_corners(pts))
        name = "Osiloskop"
    leds = VGroup(*[Dot(radius=0.025, color=c) for c in (GOOD, GOLD, "#64748B")]).arrange(RIGHT, buff=0.06)
    leds.move_to(body).shift(DOWN * h * 0.3 + LEFT * w * 0.3)
    lab = T(name, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, g, leds, lab)
