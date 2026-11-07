"""S2·B10 (ep20) shared helpers — 'Ayakta Kalmak' (season and series finale): 1:1 Type B protection (G.989.3 §18, Tables 18-1…18-4,
Figs. 18-1…18-3), ONU-side wavelength channel protection (§11.3.3.15, Tables 12-1…12-5, Annex J.2.2, TPST), Appendix V/VI (ICTP),
§19 rogue behaviour, Disable_Serial_Number + Appendix XI (emergency stop), the life of one packet, and the series wrap.

Builds on the whole season-2 chain through ep19_common (bit-proportional `fields`, `octets`, analyzer panels, sequence charts,
`OnuSM`, `OltSM`, `KeySM`, `PmSM`, state strips, S1/S2 chips, `mtable`, `strip`, `frame_axis`, `term`, icons, ep17 chrome
`reset`/`pmd_reset`/`lanes`/`msg3`, ep19 `pmd_reset2`). Only the episode names, the Type B state pieces (10 states with their
transmitter lamps, state-strip segments, the Table 18-4 grid), a small dual-parented topology and a stage reset that keeps a
persistent diagram are added here."""
from ep19_common import *

K20 = 10
EP20 = SERIES["season2"]["episodes"][K20 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep20_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K20}"
H20 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M20(p):
    return f"build/ep20/{p}/audio_proc/manifest.json"


M = M20

# ---------------- Type B colours ------------------------------------------------------------------------------------------
STBC, ACTC, EXCC = "#60A5FA", GOLD, WARN      # standby states (Tx off) · active states (Tx on, shaded in Fig. 18-2) · exceptional
TXON, TXOFF = GOLD, "#334155"
CT1C, CT2C = ACC, "#A78BFA"                    # CT 1 (birincil) · CT 2 (ikincil) — the two Type B peers of one channel pair
ICTPC = ICT                                    # ICTP messages
PROTC, UNPC = GOOD, "#475569"                  # protected / unprotected segments
CUTC = WARN

# Table 18-1: (Turkish name, G.989.3 name)
TB = {1: ("başlatma", "Initialization"), 2: ("koruma öncesi", "Pre-Protecting"), 3: ("koruyan", "Protecting"),
      4: ("LOS-P", "koruyan · sinyal kaybı"), 5: ("çalışma öncesi", "Pre-Working"), 6: ("çalışan", "Working"),
      7: ("LOS-W", "çalışan · sinyal kaybı"), 8: ("yardım isteme", "Helpme"), 9: ("iletişim arızası", "COMM-FAIL"),
      10: ("donanım arızası", "EQPT-FAIL")}
TB_SHORT = {1: "Init", 2: "Pre-Prot", 3: "Prot", 4: "LOS-P", 5: "Pre-Work", 6: "Working", 7: "LOS-W", 8: "Helpme",
            9: "COMM-F", 10: "EQPT-F"}


def tbcol(k):
    return STBC if k <= 4 else (ACTC if k <= 7 else EXCC)


def tx_on(k):
    return 5 <= k <= 7


def txlamp(on, r=0.09):
    """Transmitter lamp: glowing gold when on, dark when off."""
    if on:
        return glow_dot(TXON, r * 0.8, 4)
    return VGroup(Circle(radius=r, stroke_color="#64748B", stroke_width=1.8, fill_color="#0B1220", fill_opacity=1))


def tbbox(k, w=2.9, h=0.84, tsize=18, ssize=14, dashed=False):
    """Type B state box: '(k) Turkish name' + G.989.3 name, group colour, Tx lamp at the right (shaded fill when Tx on)."""
    a, b = TB[k]
    c = tbcol(k)
    on = tx_on(k)
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=c, stroke_width=2.4,
                         fill_color=c if on else PANEL, fill_opacity=0.18 if on else 1)
    if dashed:
        r = VGroup(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_width=0, fill_color=PANEL, fill_opacity=1),
                   DashedVMobject(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=c, stroke_width=2.4), num_dashes=40))
    t = VGroup(T(f"({k}) {a}", tsize, TXT, BOLD), T(b, ssize, c, SEMIBOLD)).arrange(DOWN, buff=0.05)
    fit(t, w - 0.62)
    t.move_to([0, 0, 0]).shift(LEFT * 0.16)
    lm = txlamp(on, 0.085).move_to([w / 2 - 0.25, 0, 0])
    return VGroup(r, t, lm)


def set_lamp(box, on):
    """Animation: switch the Tx lamp of a tbbox / ctu."""
    return Transform(box[2], txlamp(on, 0.085).move_to(box[2].get_center()))


def ctu(name, color, on=False, w=1.75, h=0.56, size=17):
    """OLT CT unit: rounded box with name and a Tx lamp at the right edge."""
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.3, fill_color=PANEL, fill_opacity=1)
    t = tf(name, size, TXT, BOLD, w=w - 0.5).move_to(r).shift(LEFT * 0.15)
    lm = txlamp(on, 0.085).move_to(r.get_right() + LEFT * 0.22)
    return VGroup(r, t, lm)


# ---------------- state strips (Type B lanes on one time axis) ------------------------------------------------------------
def tbseg(x0, x1, y, k, h=0.46, size=15, short=False):
    """Type B state segment on a strip, coloured by group; '(k) name' when it fits, else '(k)'."""
    c = tbcol(k)
    r = Rectangle(width=max(x1 - x0, 0.02), height=h, stroke_color=c, stroke_width=1.6, fill_color=c,
                  fill_opacity=0.32 if tx_on(k) else 0.16).move_to([(x0 + x1) / 2, y, 0])
    g = VGroup(r)
    t = T(f"({k})" if short else f"({k}) {TB[k][0]}", size, TXT, BOLD)
    if t.width > (x1 - x0) - 0.1:
        t = T(f"({k})", size, TXT, BOLD)
        if t.width > (x1 - x0) - 0.06:
            t = VGroup()
    if len(t):
        t.move_to(r)
    g.add(t)
    return g


def oseg(x0, x1, y, name, h=0.46, size=15, label=None):
    """ONU activation-state segment (colours of S2·B6 Table 12-1)."""
    c = SM_COL.get(name, MUTED)
    r = Rectangle(width=max(x1 - x0, 0.02), height=h, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.22).move_to([(x0 + x1) / 2, y, 0])
    t = T(label or name, size, TXT, BOLD)
    if t.width > (x1 - x0) - 0.1:
        t = T(name, size, TXT, BOLD)
    return VGroup(r, t.move_to(r) if t.width < (x1 - x0) - 0.05 else VGroup())


def txbar(x0, x1, y, h=0.09, color=TXON):
    """Thin gold bar under a strip segment: the transmitter is on."""
    return Rectangle(width=max(x1 - x0, 0.02), height=h, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([(x0 + x1) / 2, y, 0])


def ictp_arrow(x0, y0, x1, y1, text=None, size=14, side=RIGHT, buff=0.06, dashed=False):
    """ICTP message between two CT lanes (orange)."""
    if dashed:
        a = VGroup(DashedLine([x0, y0, 0], [x1, y1 - np.sign(y1 - y0) * 0.14, 0], color=ICTPC, stroke_width=2.4, dash_length=0.07),
                   arrow([x1, y1 - np.sign(y1 - y0) * 0.2, 0], [x1, y1, 0], ICTPC, 2.4, 0.12))
    else:
        a = arrow([x0, y0, 0], [x1, y1, 0], ICTPC, 2.4, 0.13)
    g = VGroup(a)
    if text:
        g.add(T(text, size, ICTPC, BOLD).next_to(a, side, buff=buff))
    return g


def ev(x, y, text, color=GOLD, size=14, pos=UP, buff=0.06):
    """Event label pinned to x on a lane (small tick + text)."""
    tk = Line([x, y - 0.1, 0], [x, y + 0.1, 0], color=color, stroke_width=2.2)
    t = T(text, size, color, BOLD).next_to(tk, pos, buff=buff)
    return VGroup(tk, t)


def cutmark(p, color=CUTC, s=0.17):
    """Fibre cut: red X."""
    c = np.array(p, dtype=float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=5), Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=5))


# ---------------- Table 18-4 (transition grid) -----------------------------------------------------------------------------
TB_IN = [("SLOS", "SLOS"), ("QLOS", "QLOS"), ("LOSc", "LOS temizlendi"), ("Tss", "Tsstart doldu"), ("Tpf", "Tpfail doldu"),
         ("Thw", "Thold & Twfail"), ("Tra", "Tract doldu"), ("Tic", "Tictp doldu"), ("Act", "ICTP: Active()"),
         ("SbL", "ICTP: Standby-LOS()"), ("SbC", "ICTP: Standby-Clear()"), ("EQ", "EQPT arızası"), ("CTr", "EMS: CTreset()"),
         ("For", "EMS: Forced()")]
_X = "."
TB_M = {"SLOS": ["*", 1, 4, "*", _X, _X, _X, "*", "*", "*"],
        "QLOS": [_X, _X, _X, _X, "*", 7, "*", _X, _X, _X],
        "LOSc": [2, "*", "*", 3, 6, "*", 6, 3, 2, "*"],
        "Tss": [5, _X, _X, _X, _X, _X, _X, _X, _X, _X],
        "Tpf": [_X, _X, _X, 5, _X, _X, _X, _X, _X, _X],
        "Thw": [_X, _X, _X, _X, _X, _X, 8, _X, _X, _X],
        "Tra": [_X, _X, _X, _X, 9, _X, _X, _X, _X, _X],
        "Tic": [_X, 3, _X, _X, _X, _X, _X, 3, _X, _X],
        "Act": [5, "N1", "N1", 5, "*", "*", "*", "N3", "*", "*"],
        "SbL": [3, 3, "*", "* Tpfail", "N2", "N2", "N2", 3, "*", "*"],
        "SbC": [3, 3, "*", 9, "N2", "N2", "N2", 9, "*", "*"],
        "EQ": [10] * 10,
        "CTr": ["* Tsstart", 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "For": [_X, _X, _X, _X, _X, 8, _X, _X, _X, _X]}
SHADE = "#1B2438"


class TbTable:
    """Table 18-4 as a grid: header (10 states, group colours), 14 input rows; shaded = impossible / violation.
    `fixed` = '*' and note cells (shown with the grid); `cell(r, c)` = transition text '→k' (revealed as narrated)."""

    def __init__(self, x0=-6.6, top=2.42, lw=2.55, cw=1.06, hh=0.58, rh=0.33, size=15, csize=15):
        self.x0, self.lw, self.cw = x0, lw, cw
        self.head, self.labels, self.bg, self.fixed = VGroup(), VGroup(), VGroup(), VGroup()
        self.rect, self.txt, self.rowy, self.tcol = {}, {}, {}, {}
        W = lw + 10 * cw
        hy = top - hh / 2
        corner = Rectangle(width=lw, height=hh, stroke_width=0, fill_color="#16213A", fill_opacity=1).move_to([x0 + lw / 2, hy, 0])
        ct = VGroup(T("olay ↓", 14, MUTED, BOLD), T("durum →", 14, MUTED, BOLD)).arrange(RIGHT, buff=0.25).move_to(corner)
        self.head.add(VGroup(corner, ct))
        self.colhead = {}
        for c in range(1, 11):
            x = x0 + lw + cw * (c - 0.5)
            r = Rectangle(width=cw - 0.03, height=hh, stroke_width=0, fill_color=tbcol(c), fill_opacity=0.22).move_to([x, hy, 0])
            t = VGroup(T(f"({c})", 15, TXT, BOLD), tf(TB_SHORT[c], 14, tbcol(c), BOLD, w=cw - 0.1)).arrange(DOWN, buff=0.03).move_to(r)
            self.colhead[c] = VGroup(r, t)
            self.head.add(self.colhead[c])
        for i, (key, name) in enumerate(TB_IN):
            y = top - hh - rh * (i + 0.5)
            self.rowy[key] = y
            lb = Rectangle(width=lw, height=rh - 0.02, stroke_width=0, fill_color=PANEL if i % 2 == 0 else "#0E1628", fill_opacity=1).move_to([x0 + lw / 2, y, 0])
            lt = tf(name, size, ICTPC if name.startswith("ICTP") else (TMRC if "doldu" in name or "&" in name else TXT), BOLD, w=lw - 0.2)
            lt.move_to([x0 + 0.12, y, 0], aligned_edge=LEFT)
            self.labels.add(VGroup(lb, lt))
            for c in range(1, 11):
                v = TB_M[key][c - 1]
                x = x0 + lw + cw * (c - 0.5)
                sh = v == _X
                r = Rectangle(width=cw - 0.03, height=rh - 0.03, stroke_color=LINE, stroke_width=0.8,
                              fill_color=SHADE if sh else BG, fill_opacity=1).move_to([x, y, 0])
                self.rect[(key, c)] = r
                self.bg.add(r)
                if sh:
                    continue
                if isinstance(v, int):
                    t = T(f"→{v}", csize, tbcol(v), BOLD).move_to(r)
                    self.txt[(key, c)] = t
                    self.tcol[(key, c)] = tbcol(v)
                else:
                    col = PINK if v.startswith("N") else MUTED
                    t = tf(v, csize - (1 if len(v) > 2 else 0), col, BOLD, w=cw - 0.1).move_to(r)
                    if v.startswith("* T"):
                        self.txt[(key, c)] = t
                        self.tcol[(key, c)] = MUTED
                    else:
                        self.fixed.add(t)
        self.bottom = top - hh - rh * len(TB_IN)
        self.width = W

    def grid(self):
        return VGroup(self.head, self.labels, self.bg)

    def cell(self, key, c):
        return self.txt[(key, c)]

    def col(self, c):
        return VGroup(self.colhead[c], *[self.rect[(k, c)] for k, _ in TB_IN])


class Act20(Act19):
    def reset_keep(self, s, badge=None, keep=(), rt=0.6, w=10.0, extra=()):
        """Act17.reset that keeps `keep` (a persistent diagram) on stage."""
        keepset = set(keep) | {self.hdr, self.badge}
        out = [m for m in self.mobjects if m not in keepset]
        h = self.heading(s)
        fit(h, w)
        h.next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
        anims = [FadeOut(m) for m in out] + [FadeIn(h, shift=RIGHT * 0.2)] + list(extra)
        if badge:
            bs, bc = BADGE[badge]
            new = pill(bs, bc, 20).to_corner(UR, buff=0.35)
            anims.append(FadeIn(new, shift=LEFT * 0.2) if self.badge is None or len(self.badge) == 0 else FadeTransform(self.badge, new))
            self.badge = new
        self.play(*anims, run_time=rt)
        if self.src is not None and self.src in out:
            self.src = None
        return h

    def pmd_keep(self, title, chips, keep=(), rt=0.6):
        """PMD Köprüsü chrome (badge, fitted heading, season-1 chips at its right) that keeps a persistent diagram."""
        ch = VGroup(*chips).arrange(RIGHT, buff=0.15).to_edge(RIGHT, buff=0.45)
        hw = ch.get_left()[0] - (-7.1 + 0.4) - 0.35
        h = self.reset_keep(title, "pmd", keep, rt, w=min(hw, 10.0))
        ch.set_y(h.get_y())
        self.play(FadeIn(ch, shift=LEFT * 0.1), run_time=0.3)
        return h, ch

    def cells_in(self, tb, keys, rt=0.45, flash=GOLD):
        """Reveal Table 18-4 transition cells [(row, col)], tinting each cell by its target group."""
        anims = []
        for key, c in keys:
            t = tb.cell(key, c)
            anims += [FadeIn(t, scale=1.3), tb.rect[(key, c)].animate.set_fill(tb.tcol[(key, c)], 0.16).set_stroke(flash, 2)]
        self.play(*anims, run_time=rt)
        self.play(*[tb.rect[(key, c)].animate.set_stroke(LINE, 0.8) for key, c in keys], run_time=0.2)
