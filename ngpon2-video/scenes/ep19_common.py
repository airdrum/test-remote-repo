"""S2·B9 (ep19) shared helpers — 'Enerji ve Sağlık': TWDM power management, power saving by channel selection, PtP WDM
line-rate adjustment (G.989.3 §16), performance monitoring, defects and the urgent status snapshot (G.989.3 §14).

Builds on the season-2 blocks chained through ep18_common → ep17_common → ep16_common → ep14_common → ep13_common →
ep12_common → ep11_common (bit-proportional `fields`, `octets`, analyzer panels, sequence-chart `lifeline`/`msg3`/`grow_msg`,
S1/S2 chips, `mtable`, `strip`, `pmd_head`, `cue_n`, `frame_axis`, `term`, `reset`/`pmd_reset`/`lanes`, emulator/analyzer icons)
and ep15's PLOAM pieces (`mtile`, `mbox`, `keychip`). Only the episode names, the power-management state machines of
Figs. 16-1/16-2 (tense = yellow, relaxed = grey subgraphs), the state-strip pieces, the Table 14-1 grid and a few small icons
are added here."""
from ep18_common import *
from ep15_common import p48, P48_OCT, OIDC, TYC, SQC, CNC, MICC, US_MSGS, DS_MSGS, inst

K19 = 9
EP19 = SERIES["season2"]["episodes"][K19 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep19_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K19}"
H19 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M19(p):
    return f"build/ep19/{p}/audio_proc/manifest.json"


M = M19

# Figs. 16-1 / 16-2 subgraphs: tense (yellow) · relaxed (grey)
TNC, RLC = GOLD, "#94A3B8"
# signalling: Sleep_Allow ON / OFF · Sleep_Request WSleep / Awake · forced wake-up indication · local stimuli
SAON, SAOFF = GOOD, WARN
SRW, SRA = "#C084FC", ACC
FWIC = PINK
LSC = "#FB923C"
# Table 14-1: mandatory / optional · defects · "no clearing condition"
MANC, OPTC9 = ACC, "#475569"
DEFC, NOCLR = WARN, PINK
EXMC = "#60A5FA"     # example values ("örnek")

ONU_PS = {1: ("etkin tutulan", "ActiveHeld"), 2: ("etkin serbest", "ActiveFree"), 3: ("farkında", "Aware"), 4: ("düşük güç", "LowPower")}
OLT_PS = {1: ("zorla uyanık", "AwakeForced"), 2: ("serbest uyanık", "AwakeFree"), 3: ("düşük güç gözetimi", "LowPowerWatch"),
          4: ("uyarılmış", "Alerted")}
TENSE = {"N": {1, 2}, "L": {1, 4}}


def pcol(side, k):
    return TNC if k in TENSE[side] else RLC


def pname(side, k):
    return (ONU_PS if side == "N" else OLT_PS)[k]


def pst(side, k, w=2.7, h=0.9, tsize=19, ssize=15):
    """Power-management state box: '(k) Turkish name' + the G.989.3 name, coloured by subgraph."""
    a, b = pname(side, k)
    return sbox(f"({k}) {a}", b, pcol(side, k), w, h, tsize, ssize)


class PmSM:
    """ONU (Fig. 16-1, side 'N') or OLT CT (Fig. 16-2, side 'L') power-management machine on a 2 × 2 grid:
    tense (yellow) states in the left column, relaxed (grey) states in the right column, state (1) top left.
    ONU: (1) TL, (2) BL, (3) BR, (4) TR · OLT: (1) TL, (4) BL, (2) TR, (3) BR."""

    def __init__(self, side, cx=0.0, cy=-0.4, dx=2.75, dy=1.3, w=2.7, h=0.9, tsize=19, ssize=15):
        self.side = side
        if side == "N":
            pos = {1: (-1, 1), 2: (-1, -1), 3: (1, -1), 4: (1, 1)}
        else:
            pos = {1: (-1, 1), 4: (-1, -1), 2: (1, 1), 3: (1, -1)}
        self.b = {k: pst(side, k, w, h, tsize, ssize).move_to([cx + sx * dx, cy + sy * dy, 0]) for k, (sx, sy) in pos.items()}

    def boxes(self):
        return VGroup(*[self.b[k] for k in sorted(self.b)])

    def pt(self, k, s, o=0.0):
        bx = self.b[k][0]
        return {"L": bx.get_left() + UP * o, "R": bx.get_right() + UP * o, "T": bx.get_top() + RIGHT * o, "B": bx.get_bottom() + RIGHT * o}[s]

    def edge(self, a, sa, b, sb, label, color, oa=0.0, ob=0.0, lpos=UP, lbuff=0.06, size=15, angle=0.0, lshift=ORIGIN, sw=2.4):
        p0, p1 = self.pt(a, sa, oa), self.pt(b, sb, ob)
        ar = carrow(p0, p1, angle, color, sw, 0.14) if angle else arrow(p0, p1, color, sw, 0.14)
        g = VGroup(ar)
        if label:
            t = T(label, size, color, BOLD, line_spacing=0.8)
            t.next_to(ar.point_from_proportion(0.5), lpos, buff=lbuff).shift(lshift)
            g.add(t)
        return g

    def loop(self, k, label, color=MUTED, where="T", size=14, off=0.0):
        bx = self.b[k][0]
        if where in "TB":
            s = 1 if where == "T" else -1
            e = bx.get_top() if s > 0 else bx.get_bottom()
            p0, p1 = e + LEFT * 0.42 + RIGHT * off, e + RIGHT * 0.42 + RIGHT * off
            a = CurvedArrow(p0, p1, angle=-s * PI * 1.05, color=color, stroke_width=2.2, tip_length=0.11)
            t = T(label, size, color, BOLD).next_to(a, UP if s > 0 else DOWN, buff=0.04)
        else:
            s = 1 if where == "R" else -1
            e = bx.get_right() if s > 0 else bx.get_left()
            p0, p1 = e + UP * 0.22, e + DOWN * 0.22
            a = CurvedArrow(p0, p1, angle=-s * PI * 1.05, color=color, stroke_width=2.2, tip_length=0.11)
            t = T(label, size, color, BOLD).next_to(a, RIGHT if s > 0 else LEFT, buff=0.06)
        return VGroup(a, t)

    def region(self, tense=True, pad=0.28, label=True, size=15, lpos=UP, extra=()):
        ks = sorted(k for k in self.b if (k in TENSE[self.side]) == tense)
        g = VGroup(*[self.b[k] for k in ks], *extra)
        c = TNC if tense else RLC
        r = RoundedRectangle(corner_radius=0.2, width=g.width + 2 * pad, height=g.height + 2 * pad, stroke_width=0,
                             fill_color=c, fill_opacity=0.08).move_to(g)
        d = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=g.width + 2 * pad, height=g.height + 2 * pad, stroke_color=c,
                                            stroke_width=1.8), num_dashes=56).move_to(g)
        out = VGroup(r, d)
        if label:
            out.add(T("sarı alt çizge · tense" if tense else "gri alt çizge · relaxed", size, c, BOLD).next_to(d, lpos, buff=0.06))
        return out


# ---------------- state strips (both machines on one time axis) --------------------------------------------------------
def sseg(x0, x1, y, side, k, h=0.5, size=15, short=False, name=True):
    """State segment on a strip: coloured by subgraph, labelled '(k) name' (or '(k)' when it does not fit / short)."""
    c = pcol(side, k)
    r = Rectangle(width=max(x1 - x0, 0.02), height=h, stroke_color=c, stroke_width=1.6, fill_color=c,
                  fill_opacity=0.3 if k in TENSE[side] else 0.16).move_to([(x0 + x1) / 2, y, 0])
    g = VGroup(r)
    if name:
        s = f"({k})" if short else f"({k}) {pname(side, k)[0]}"
        t = T(s, size, TXT, BOLD)
        if t.width > (x1 - x0) - 0.1:
            t = T(f"({k})", size, TXT, BOLD)
            if t.width > (x1 - x0) - 0.06:
                t = VGroup()
        if len(t):
            t.move_to(r)
        g.add(t)
    return g


def vmsg(x, y0, y1, text, color, size=15, side=RIGHT, buff=0.06, sw=2.4, dashed=False, lshift=ORIGIN):
    """Vertical message arrow between two strips (y0 → y1) with a label beside it."""
    if dashed:
        a = VGroup(DashedLine([x, y0, 0], [x, y1 - np.sign(y1 - y0) * 0.14, 0], color=color, stroke_width=sw, dash_length=0.07),
                   arrow([x, y1 - np.sign(y1 - y0) * 0.2, 0], [x, y1, 0], color, sw, 0.12))
    else:
        a = arrow([x, y0, 0], [x, y1, 0], color, sw, 0.13)
    g = VGroup(a)
    if text:
        g.add(T(text, size, color, BOLD).next_to(a, side, buff=buff).shift(lshift))
    return g


def tick_row(xs, y, color, h=0.22, sw=2.2):
    return VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=color, stroke_width=sw) for x in xs])


def burst_row(xs, y, color=ONUC, w=0.16, h=0.28, op=0.75):
    return VGroup(*[Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, y, 0]) for x in xs])


def tbar(x0, x1, y, label, color=TMRC, h=0.18, size=14, lpos=UP, op=0.55):
    """Timer bar on a strip (left-anchored), label above / below."""
    r = Rectangle(width=max(x1 - x0, 0.02), height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])
    g = VGroup(r)
    if label:
        g.add(T(label, size, color, BOLD).next_to(r, lpos, buff=0.05))
    return g


def side_lbl(s, y, color, x=-6.35, size=17):
    return T(s, size, color, BOLD).move_to([x, y, 0], aligned_edge=LEFT)


# ---------------- Table 14-1 grid ---------------------------------------------------------------------------------------
# (group, Turkish name, mandatory, optional) — 111 rows = 37 M + 74 O in 11 groups (fact sheet §11, our count)
PMG = [("PHY", "fiziksel katman", 6, 3), ("LODS", "senkron kaybı", 7, 0), ("XGEM", "XGEM", 4, 4), ("UTIL", "kullanım", 2, 1),
       ("PLOAM", "PLOAM", 4, 30), ("ACT", "aktivasyon", 0, 8), ("TUN", "ayar denetimi", 13, 21), ("PWR", "güç dengeleme", 0, 2),
       ("OMCI", "OMCI", 0, 4), ("MON", "güç izleme", 1, 0), ("ENE", "enerji koruma", 0, 1)]


def pm_cell(m, cw=0.24, h=0.3):
    c = MANC if m else OPTC9
    return Rectangle(width=cw, height=h, stroke_color=c, stroke_width=1.3, fill_color=c, fill_opacity=0.75 if m else 0.12)


def pm_grid(x_lab=-6.35, x0=-3.95, y0=1.9, dy=0.42, cw=0.24, gap=0.04, h=0.3, size=15):
    """11 rows: label (left) · one cell per Table 14-1 row (M filled, O outline) · 'nM · nO' count (right of the cells).
    Returns VGroup of rows; row = VGroup(label, cells, count)."""
    rows = VGroup()
    for i, (_, name, m, o) in enumerate(PMG):
        y = y0 - i * dy
        lab = T(name, size, TXT, BOLD).move_to([x_lab, y, 0], aligned_edge=LEFT)
        cells = VGroup(*[pm_cell(k < m, cw, h).move_to([x0 + (cw + gap) * k + cw / 2, y, 0]) for k in range(m + o)])
        cnt = T(f"{m + o}", size, MUTED, BOLD).next_to(cells, RIGHT, buff=0.15)
        rows.add(VGroup(lab, cells, cnt))
    return rows


def yn(s, size=15):
    """Table 14-1 cell value coloured: Evet / Hayır / N/A."""
    c = {"Evet": GOOD, "Hayır": WARN, "N/A": MUTED}.get(s.split(" ")[0].rstrip(","), TXT)
    return T(s, size, c, BOLD)


# ---------------- small icons ---------------------------------------------------------------------------------------------
def rx_icon(on=True, s=0.3, color=ACC):
    """Receiver (photodiode-like) icon: a small box with an incoming arrow; dim when off."""
    c = color if on else MUTED
    body = RoundedRectangle(corner_radius=0.04, width=s, height=s * 0.62, stroke_color=c, stroke_width=1.8, fill_color=PANEL, fill_opacity=1)
    a = Arrow(body.get_left() + LEFT * s * 1.1, body.get_left(), buff=0.0, color=c, stroke_width=2.2, tip_length=0.08,
              max_tip_length_to_length_ratio=0.5)
    return VGroup(body, a)


def zz(color=RLC, size=18):
    return T("z z", size, color, BOLD)


def nvm_icon(n=10, filled=0, w=2.4, h=1.15, color=GOLD, label="kalıcı bellek"):
    """Non-volatile memory with n record slots (`filled` of them in colour)."""
    body = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    cols = 5
    rows = (n + cols - 1) // cols
    sw_, sh = (w - 0.4) / cols, (h - 0.45) / rows
    slots = VGroup()
    for k in range(n):
        r, c = divmod(k, cols)
        slots.add(Rectangle(width=sw_ - 0.06, height=sh - 0.06, stroke_color=color, stroke_width=1.2, fill_color=color,
                            fill_opacity=0.55 if k < filled else 0.08)
                  .move_to(body.get_corner(UL) + [0.2 + sw_ * (c + 0.5), -0.32 - sh * (r + 0.5), 0]))
    lab = T(label, 15, color, BOLD).move_to(body.get_top() + DOWN * 0.17)
    return VGroup(body, slots, lab)


def logger_icon(w=2.15, h=1.55, label="Veri kaydedici"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.82, height=h * 0.56, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.1)
    x0, x1 = scr.get_left()[0] + 0.08, scr.get_right()[0] - 0.08
    y0, y1 = scr.get_bottom()[1] + 0.08, scr.get_top()[1] - 0.08
    pts = []
    n = 24
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        hi = (k % 8) in (0, 1)
        spike = (k % 8) == 4
        y = y1 - 0.02 if hi else (y0 + (y1 - y0) * (0.55 if spike else 0.18))
        pts.append([x, y, 0])
    tr_ = VMobject(stroke_color=GOLD, stroke_width=1.8).set_points_as_corners(pts)
    port = VGroup(*[Square(0.09, stroke_color="#94A3B8", stroke_width=1.5) for _ in range(2)]).arrange(RIGHT, buff=0.08).move_to(body).shift(DOWN * h * 0.33)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, tr_, port, lab)


def oswitch_icon(s=0.5, color=FEED, label="optik anahtar", open_=False):
    a = Dot(radius=0.05, color=color).move_to(LEFT * s / 2)
    b = Dot(radius=0.05, color=color).move_to(RIGHT * s / 2)
    lv = Line(a.get_center(), b.get_center() + (UP * s * 0.45 if open_ else ORIGIN), color=WARN if open_ else color, stroke_width=3)
    lab = T(label, 15, MUTED, BOLD).next_to(VGroup(a, b), DOWN, buff=0.12)
    return VGroup(a, b, lv, lab)


def code_row(code, name, color, size=17, w=4.2, mono=True, note=None):
    """'0x03  WSleep · dikkatli uyku' row in a thin frame."""
    a = HX(code, size, color, BOLD) if mono else T(code, size, color, BOLD)
    b = T(name, size - 1, TXT, BOLD)
    g = VGroup(a, b).arrange(RIGHT, buff=0.25)
    r = RoundedRectangle(corner_radius=0.06, width=w, height=g.height + 0.2, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.1)
    fit(g, w - 0.3)
    g.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.15)
    return VGroup(r, g)


def ex_tag(s="örnek değerler", size=15):
    return tag(s, EXMC, size)


def ed_chips(size=15, color=MUTED):
    """'2021 · Amd.1 · Amd.2' edition chips."""
    return VGroup(*[tag(s, color, size) for s in ("2021", "Amd.1 · 2023", "Amd.2 · 2025")]).arrange(RIGHT, buff=0.12)


def log_ax(v0, v1, x0, x1, y, ticks, size=14, color=MUTED):
    """Log axis (values in arbitrary positive units), ticks = [(value, label)]. Returns (VGroup, X)."""
    import math as _m
    X = lambda v: x0 + (_m.log10(v) - _m.log10(v0)) / (_m.log10(v1) - _m.log10(v0)) * (x1 - x0)
    ax = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2)
    tk = VGroup(*[Line([X(v), y - 0.07, 0], [X(v), y + 0.07, 0], color=color, stroke_width=1.5) for v, _ in ticks])
    lb = VGroup(*[T(s, size, color, BOLD).next_to([X(v), y, 0], DOWN, buff=0.1) for v, s in ticks])
    return VGroup(ax, tk, lb), X


class Act19(Act18):
    def src_in(self, s):
        """Source line for use inside a combined play (e.g. reset extras): the old line is left to the stage clear."""
        self.src = None
        return self.set_src(s)

    def heading19(self, s, old=None, w=10.0):
        return self.heading12(s, old, w)

    def chips_at(self, chips, h):
        """Several season chips stacked at the right end of the heading row (PMD Köprüsü with two references)."""
        g = VGroup(*chips).arrange(LEFT, buff=0.15)
        return g.to_edge(RIGHT, buff=0.45).set_y(h.get_y())

    def pmd_reset2(self, title, chips, rt=0.6, w=None):
        """pmd_reset with one or more chips; the heading is fitted so it never runs into the chips."""
        ch = VGroup(*chips).arrange(RIGHT, buff=0.15)
        ch.to_edge(RIGHT, buff=0.45)
        hw = w or (ch.get_left()[0] - (-7.1 + 0.4) - 0.35)
        h = self.reset(title, "pmd", rt, w=min(hw, 10.0), extra=[])
        ch.set_y(h.get_y())
        self.play(FadeIn(ch, shift=LEFT * 0.1), run_time=0.3)
        return h, ch
