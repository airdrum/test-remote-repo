"""S2·B6 (ep16) shared helpers — 'Uyanış': ONU activation, ranging and time of day (G.989.3 §12, §13, Ek II, Ek VII).

Builds on the season-2 blocks chained through ep14_common → ep13_common → ep12_common → ep11_common (bit-proportional
`fields`, `octets`, `strip`, analyzer panels, sequence-chart `lifeline`/`msg`/`ct_box`/`onu_box`, S1/S2 chips, `mtable`,
`pmd_head`, `cue_n`, `frame_axis`, `term`, `hbar`, `spool`, fitted title cards, header shrinking); only the episode names,
the state/timer colours and a few activation pieces (the ONU state machine, laser/clock/counter icons) are added here."""
from ep14_common import *

K16 = 6
EP16 = SERIES["season2"]["episodes"][K16 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep16_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K16}"
H16 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M16(p):
    return f"build/ep16/{p}/audio_proc/manifest.json"


M = M16

# activation states (Table 12-1) · timers · quiet window · EqD · time of day
O1C, SNC, RGC, OPC, LDC, ESC, TUC = STATE, GOLD, ACC, GOOD, "#FB923C", WARN, "#60A5FA"
TMRC = TIMC                    # timers
QWC = "#94A3B8"                # quiet window (nobody transmits)
EQC = "#C084FC"                # equalization delay
TODC = "#FB923C"               # time of day
AMDC = PINK                    # amendment marks
SETC = ["#F59E0B", ACC, "#A78BFA", "#60A5FA", GOOD, WARN, "#F472B6"]   # discard sets I … VII
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]

SM_SUB = {"O1.1": "çevrim dışı", "O1.2": "profil öğrenme", "O2-3": "seri numarası", "O4": "ranging", "O5.1": "bağlı",
          "O5.2": "bekleyen", "O6": "aralıklı LODS", "O7": "acil durdurma", "O8.1": "çevrim dışı", "O8.2": "profil öğrenme",
          "O9": "↑ ayar"}
SM_COL = {"O1.1": O1C, "O1.2": O1C, "O2-3": SNC, "O4": RGC, "O5.1": OPC, "O5.2": OPC, "O6": LDC, "O7": ESC,
          "O8.1": TUC, "O8.2": TUC, "O9": TUC}
SM_POS = {"O1.1": (-5.6, 1.5), "O1.2": (-5.6, -0.45), "O2-3": (-2.55, 0.55), "O4": (0.2, 0.55), "O5.1": (2.95, 1.5),
          "O5.2": (2.95, -0.45), "O6": (5.8, 1.5), "O7": (-5.6, -1.85), "O8.1": (5.8, -1.85), "O8.2": (2.95, -1.85),
          "O9": (0.2, -1.85)}


class OnuSM:
    """TWDM ONU activation-cycle state machine (G.989.3 Table 12-1, Figure 12-1) laid out for the 14.2 × 8 frame.
    Boxes in `b[name]`; group frames for O1, O5, O8 in `fr[...]`; edges built on demand by `edge()` / `edges`."""

    def __init__(self, w=2.0, h=0.72, tsize=19, ssize=14):
        self.w, self.h = w, h
        self.b = {k: sbox(k, SM_SUB[k], SM_COL[k], w, h, tsize, ssize).move_to([x, y, 0]) for k, (x, y) in SM_POS.items()}
        self.fr = {}
        for name, a, c, lab, up in (("O1", "O1.1", "O1.2", "O1 · Başlangıç", True), ("O5", "O5.1", "O5.2", "O5 · Çalışma", True)):
            g = VGroup(self.b[a], self.b[c])
            r = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=g.width + 0.3, height=g.height + 0.3, stroke_color=SM_COL[a],
                                                stroke_width=1.8), num_dashes=48).move_to(g)
            t = T(lab, 16, SM_COL[a], BOLD).next_to(r, UP, buff=0.06)
            self.fr[name] = VGroup(r, t)
        g = VGroup(self.b["O8.2"], self.b["O8.1"])
        r = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=g.width + 0.3, height=g.height + 0.3, stroke_color=TUC, stroke_width=1.8),
                           num_dashes=60).move_to(g)
        self.fr["O8"] = VGroup(r, T("O8 · ↓ ayar", 16, TUC, BOLD).next_to(r, DOWN, buff=0.06))

    def pt(self, k, side, off=0.0):
        """Point on a box edge: side in 'L','R','T','B'; off shifts along the edge."""
        bx = self.b[k][0]
        if side == "L":
            return bx.get_left() + UP * off
        if side == "R":
            return bx.get_right() + UP * off
        if side == "T":
            return bx.get_top() + RIGHT * off
        return bx.get_bottom() + RIGHT * off

    def edge(self, a, sa, b, sb, label=None, color=MUTED, oa=0.0, ob=0.0, lpos=UP, lbuff=0.06, size=14, lshift=ORIGIN):
        ar = arrow(self.pt(a, sa, oa), self.pt(b, sb, ob), color, 2.2, 0.13)
        g = VGroup(ar)
        if label:
            g.add(T(label, size, color, BOLD).next_to(ar, lpos, buff=lbuff).shift(lshift))
        return g

    def main_edges(self):
        e = {}
        e["dsync"] = self.edge("O1.1", "B", "O1.2", "T", "DSYNC", MUTED, -0.4, -0.4, LEFT, 0.08)
        e["lods1"] = self.edge("O1.2", "T", "O1.1", "B", "LODS", MUTED, 0.4, 0.4, RIGHT, 0.08)
        e["act"] = VGroup(arrow(self.pt("O1.2", "R"), self.pt("O2-3", "L", -0.15), SNC, 2.4, 0.14))
        e["onuid"] = self.edge("O2-3", "R", "O4", "L", "ONU-ID", SNC, 0.15, 0.15, UP, 0.06)
        e["to1"] = self.edge("O4", "L", "O2-3", "R", "TO1", RGC, -0.15, -0.15, DOWN, 0.06)
        e["eqd"] = VGroup(arrow(self.pt("O4", "T", 0.6), self.pt("O5.1", "L", -0.1), RGC, 2.4, 0.14),
                          T("EqD", 14, RGC, BOLD).move_to([1.05, 1.42, 0]))
        e["tune"] = self.edge("O5.1", "B", "O5.2", "T", "ayar isteği", OPC, 0.0, 0.0, RIGHT, 0.08)
        e["lods5"] = self.edge("O5.1", "R", "O6", "L", "LODS", LDC, 0.17, 0.17, UP, 0.05)
        e["dsync6"] = self.edge("O6", "L", "O5.1", "R", "DSYNC", LDC, -0.17, -0.17, DOWN, 0.05)
        e["to3"] = self.edge("O6", "B", "O8.1", "T", "TO3", LDC, 0.0, 0.0, RIGHT, 0.08)
        e["sfcrx"] = VGroup(arrow(self.pt("O5.2", "B", 0.7), self.pt("O8.1", "T", -0.7), TUC, 2.2, 0.13))
        e["sfctx"] = VGroup(arrow(self.pt("O5.2", "B", -0.7), self.pt("O9", "T", 0.7), TUC, 2.2, 0.13))
        e["sfcl"] = T("SFC", 14, TUC, BOLD).move_to([2.95, -1.15, 0])
        e["o82"] = VGroup(arrow(self.pt("O8.1", "L"), self.pt("O8.2", "R"), TUC, 2.2, 0.12))
        e["o89"] = VGroup(arrow(self.pt("O8.2", "L"), self.pt("O9", "R"), TUC, 2.2, 0.12))
        e["o95"] = VGroup(arrow(self.pt("O9", "R", 0.25), [1.85, 1.2, 0], TUC, 2.2, 0.13))
        e["en"] = self.edge("O7", "T", "O1.2", "B", None, ESC, 0.0, 0.0)
        e["en"][0].put_start_and_end_on(self.pt("O7", "T"), self.fr["O1"][0].get_bottom() + DOWN * 0.02)
        e["en"].add(T("Enable SN", 14, ESC, BOLD).next_to(e["en"][0], RIGHT, buff=0.1))
        e["dis"] = VGroup(T("← Disable SN · her durumdan", 15, ESC, BOLD).next_to(self.b["O7"], RIGHT, buff=0.2))
        return e

    def boxes(self, *names):
        return VGroup(*[self.b[n] for n in names])


def laser(on=True, color=GOLD, s=0.32):
    """Small laser emitter icon: body + beam (on) or a crossed-out aperture (off)."""
    body = RoundedRectangle(corner_radius=0.04, width=s, height=s * 0.62, stroke_color=TXT if on else MUTED, stroke_width=1.8,
                            fill_color=PANEL, fill_opacity=1)
    if on:
        beam = VGroup(*[Line(body.get_right(), body.get_right() + np.array([s * 1.1, dy * s, 0]), color=color, stroke_width=2.4)
                        for dy in (-0.25, 0, 0.25)])
        return VGroup(body, beam)
    xm = xmark(Square(s * 0.36).next_to(body, RIGHT, buff=0.08), WARN, 2.2, 0.0)
    return VGroup(body, xm)


def clock_icon(r=0.42, color=TODC, hh=2.0, mm=50.0):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.4, fill_color=PANEL, fill_opacity=1)
    ticks = VGroup(*[Line(c.get_center() + r * 0.82 * np.array([np.cos(a), np.sin(a), 0]),
                          c.get_center() + r * 0.95 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=1.6)
                     for a in np.linspace(0, TAU, 12, endpoint=False)])
    ah = PI / 2 - TAU * (hh % 12) / 12
    am = PI / 2 - TAU * mm / 60
    hand_h = Line(c.get_center(), c.get_center() + r * 0.5 * np.array([np.cos(ah), np.sin(ah), 0]), color=TXT, stroke_width=3)
    hand_m = Line(c.get_center(), c.get_center() + r * 0.78 * np.array([np.cos(am), np.sin(am), 0]), color=TXT, stroke_width=2.2)
    return VGroup(c, ticks, hand_h, hand_m, Dot(c.get_center(), radius=0.03, color=TXT))


def counter_icon(w=2.15, h=1.55, label="Zaman aralığı sayacı", reading="± 3,1 ns"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.8, height=h * 0.42, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.12)
    rd = fit(T(reading, 18, TODC, BOLD), scr.width - 0.12).move_to(scr)
    ins = VGroup(*[VGroup(Circle(radius=0.07, stroke_color="#94A3B8", stroke_width=1.5), T(s, 14, MUTED, BOLD)).arrange(DOWN, buff=0.04)
                   for s in ("A", "B")]).arrange(RIGHT, buff=0.35).move_to(body).shift(DOWN * h * 0.27)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, rd, ins, lab)


def otdr_icon(w=2.15, h=1.55, label="OTDR"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.82, height=h * 0.56, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.1)
    x0, x1 = scr.get_left()[0] + 0.08, scr.get_right()[0] - 0.08
    y0, y1 = scr.get_bottom()[1] + 0.08, scr.get_top()[1] - 0.08
    pts = [[x0, y1, 0], [x0 + 0.05, y1 - 0.05, 0]]
    xs = np.linspace(x0 + 0.05, x1 - 0.25, 12)
    for k, x in enumerate(xs):
        pts.append([x, y1 - 0.05 - (y1 - y0 - 0.25) * k / 11 * 0.7, 0])
    pts += [[x1 - 0.22, y1 - 0.05 - (y1 - y0 - 0.25) * 0.7 + 0.18, 0], [x1 - 0.18, y0 + 0.02, 0], [x1, y0 + 0.02, 0]]
    tr_ = VMobject(stroke_color=GOOD, stroke_width=1.8).set_points_as_corners(pts)
    port = Square(0.1, stroke_color="#94A3B8", stroke_width=1.5).move_to(body).shift(DOWN * h * 0.33 + RIGHT * w * 0.3)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, tr_, port, lab)


def bitbox(spec, cw=0.5, h=0.5, size=18, mono=True):
    """Row of single-bit cells: spec = [(char, color)], centred at origin."""
    g = VGroup()
    for s, c in spec:
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.18)
        t = (HX(s, size, TXT, BOLD) if mono else T(s, size, TXT, BOLD)).move_to(r)
        g.add(VGroup(r, t))
    return g.arrange(RIGHT, buff=0)


def stack_bar(parts, x0, y, h=0.5, size=15, scale=1.0):
    """Left-anchored stacked bar: parts = [(value, label, color)] with widths value × scale; labels inside if they fit."""
    g = VGroup()
    x = x0
    for v, lab, c in parts:
        w = v * scale
        r = Rectangle(width=max(w, 0.02), height=h, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.4).move_to([x + w / 2, y, 0])
        cell = VGroup(r)
        if lab:
            t = T(lab, size, TXT, BOLD)
            if t.width <= w - 0.08:
                t.move_to(r)
            else:
                t.set_color(c).next_to(r, UP, buff=0.06)
            cell.add(t)
        g.add(cell)
        x += w
    return g


class Act16(Act14):
    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.2)

    def heading16(self, s, old=None, w=10.0):
        return self.heading12(s, old, w)
