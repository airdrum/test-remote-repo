"""S2·B8 (ep18) shared helpers — 'Güven': threat model, authentication, key derivation, XGEM payload encryption, key exchange,
PLOAM/OMCI integrity and what §15 leaves open (G.989.3 §15, Ek C, Ek D, Ek IV.6–IV.12; Amd.1/Amd.2 changes to §15.5.3).

Builds on the season-2 blocks chained through ep17_common → ep16_common → ep14_common → ep13_common → ep12_common →
ep11_common (bit-proportional `fields`, `bbar`, analyzer panels, sequence-chart `lifeline`/`msg3`/`grow_msg`, S1/S2 chips,
`mtable`, `xhdr`, `lock`, `frame_axis`, `tmark`, `reset`/`pmd_reset`/`lanes` chrome) and ep15's PLOAM pieces (`keychip`,
`mbox`, `cmac_box`, `hexrow`). Only the episode names, the key-tree / threat / key-state colours, the key-exchange state
machines, the initial counter block and a few small icons are added here."""
from ep17_common import *
from ep15_common import cmac_box, hexrow, SKC, UCC, MICC, OIDC, TYC, SQC, CNC, bbar, bar_to, mtile, FAM

K18 = 8
EP18 = SERIES["season2"]["episodes"][K18 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep18_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K18}"
H18 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M18(p):
    return f"build/ep18/{p}/audio_proc/manifest.json"


M = M18

# the four threats of §15.1 · key tree (§15.3) · default (public) key = DKC from ep15 · data key
THC = ["#60A5FA", GOLD, WARN, "#C084FC"]
THN = ["dinleme", "taklit", "araya giren cihaz", "tekrar · bit çevirme"]
MSKC, SKC8, OIKC, PIKC, KEKC, DEKC = GOLD, "#C084FC", "#60A5FA", PINK, ACC, GOOD
KTC = {"MSK": MSKC, "SK": SKC8, "OMCI_IK": OIKC, "PLOAM_IK": PIKC, "KEK": KEKC, "DEK": DEKC}
ATKC = WARN            # attacker / rogue device
CLRC = "#94A3B8"       # clear text (not protected)
# ICB fields (Fig. 15-2)
SFCC8, IFCC8, NOTC = ACC, GOLD, PINK
# key exchange states (Figs. 15-4 / 15-5): 0 inactive · 1 · 2 · 3 · 4 active
KSC = ["#64748B", GOLD, ACC, "#60A5FA", GOOD]
KL = [("KL0", "anahtar yok"), ("KL1", "istek"), ("KL2", "onay"), ("KL3", "onay bekleme"), ("KL4", "etkin")]
KN = [("KN0", "anahtar yok"), ("KN1", "üretim"), ("KN2", "alındı bekleme"), ("KN3", "alındı"), ("KN4", "etkin")]
# golden-vector values (App IV, reproduced in the fact sheet §9)
IV6_ICB = "00040a0e160d0078 00040a0e160d0078"
IV7_ICB = "00040a0e160d097c fffbf5f1e9f2f683"
IV8 = {"SK": "795fcf6cb215224087430600dd170f07", "OMCI_IK": "184b8ad4d1ac4af4dd4b339ecc0d3370",
       "PLOAM_IK": "e256ce76785c78717c7b3044ab28e2cd", "KEK": "6f9c99b8361768937e453b165f609710"}
LBL = {"OMCI_IK": ("OMCIIntegrityKey", "4f4d4349496e746567726974794b6579"),
       "PLOAM_IK": ("PLOAMIntegrtyKey", "504c4f414d496e7465677274794b6579"),
       "KEK": ("KeyEncryptionKey", "4b6579456e6372797074696f6e4b6579")}


def ytag(s="yorum", color=GOLD, size=15):
    """Interpretation / derivation label ('yorum', 'bizim çıkarımımız', 'bizim hesabımız' …)."""
    return interp(s, color, size)


def knode(name, color=None, w=1.75, h=0.56, size=18, sub=None, ssize=14):
    """Key node: lock + key name (+ optional small subtitle) in a rounded box coloured by the key tree."""
    c = color or KTC.get(name, ACC)
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=c, stroke_width=2.4, fill_color=c, fill_opacity=0.13)
    lk = lock(c, 0.22)
    t = T(name, size, TXT, BOLD)
    row = VGroup(lk, t).arrange(RIGHT, buff=0.12)
    if sub:
        row = VGroup(row, T(sub, ssize, c, BOLD)).arrange(DOWN, buff=0.04)
    fit(row, w - 0.16)
    return VGroup(r, row.move_to(r))


def hexbox(s, color=TXT, size=16, stroke=None, w=None, h=0.42, op=0.08):
    """Monospace value in a thin frame (hex keys, MICs)."""
    t = HX(s, size, color, BOLD)
    c = stroke or color
    r = RoundedRectangle(corner_radius=0.06, width=w or t.width + 0.26, height=h, stroke_color=c, stroke_width=1.4, fill_color=c, fill_opacity=op)
    if w:
        fit(t, w - 0.16)
    return VGroup(r, t.move_to(r))


def icb(us=False, w=12.2, h=0.6, size=17, wsize=14, show_w=True, short=False):
    """Initial counter block (Fig. 15-2): 50 | 14 | 50 | 14 bits; lower half complemented upstream."""
    a, b = ("SFC", "IFC") if short else ("SFC(49..0)", "IFC(13..0)")
    lo = [("¬ " + a, 50, NOTC), ("¬ " + b, 14, NOTC)] if us else [(a, 50, SFCC8), (b, 14, IFCC8)]
    spec = [(a, 50, SFCC8), (b, 14, IFCC8)] + lo
    return fields(spec, w, h, size, wsize, show_w=show_w, unit=" bit")


def kstate(k, onu=False, w=2.15, h=0.78, tsize=19, ssize=15):
    code, name = (KN if onu else KL)[k]
    return sbox(code, name, KSC[k], w, h, tsize, ssize)


class KeySM:
    """OLT (KL0…KL4) and ONU (KN0…KN4) unicast key-exchange state machines (Figs. 15-4 / 15-5) as two rows."""

    def __init__(self, y_olt=1.2, y_onu=-1.0, x0=-4.75, dx=2.6, w=2.15, h=0.78):
        self.y = (y_olt, y_onu)
        self.b = {}
        for side, y in (("L", y_olt), ("N", y_onu)):
            for k in range(5):
                self.b[side + str(k)] = kstate(k, side == "N", w, h).move_to([x0 + k * dx, y, 0])
        self.fwd = {}
        for side in "LN":
            for k in range(4):
                a, b_ = self.b[f"{side}{k}"][0], self.b[f"{side}{k + 1}"][0]
                self.fwd[f"{side}{k}"] = arrow(a.get_right(), b_.get_left(), KSC[k + 1], 2.2, 0.12)

    def row(self, side):
        return VGroup(*[self.b[f"{side}{k}"] for k in range(5)])

    def loop(self, key, label, color=TMRC, up=True, size=15):
        bx = self.b[key][0]
        s = 1 if up else -1
        p0 = (bx.get_top() if up else bx.get_bottom()) + LEFT * 0.42
        p1 = (bx.get_top() if up else bx.get_bottom()) + RIGHT * 0.42
        a = CurvedArrow(p0, p1, angle=-s * PI * 1.05, color=color, stroke_width=2.2, tip_length=0.11)
        t = T(label, size, color, BOLD).next_to(a, UP if up else DOWN, buff=0.04)
        return VGroup(a, t)

    def back(self, side, label, color=WARN, depth=0.55, size=15, up=False):
        """Bracket from states 1–3 back to state 0 (TK1 / TK4 expiry)."""
        y0 = self.y[0 if side == "L" else 1]
        s = 1 if up else -1
        b1, b3, b0 = self.b[side + "1"][0], self.b[side + "3"][0], self.b[side + "0"][0]
        ey = (b1.get_top() if up else b1.get_bottom())[1]
        yy = ey + s * depth
        x1, x3 = b1.get_x(), b3.get_x()
        stubs = VGroup(*[Line([x, ey, 0], [x, yy, 0], color=color, stroke_width=2) for x in (x1, self.b[side + "2"][0].get_x(), x3)])
        hl = Line([x3, yy, 0], [b0.get_x(), yy, 0], color=color, stroke_width=2)
        ar = arrow([b0.get_x(), yy, 0], [b0.get_x(), (b0.get_top() if up else b0.get_bottom())[1], 0], color, 2.2, 0.12)
        t = T(label, size, color, BOLD).next_to(hl, UP if up else DOWN, buff=0.05).set_x((x1 + x3) / 2)
        return VGroup(stubs, hl, ar, t)


def odn(x_olt=-5.6, y=0.0, n=4, x_sp=-2.6, x_onu=0.4, dy=0.85, olt_label="OLT CT", onu_w=1.1, size=16, spare=None):
    """Small power-splitter ODN: OLT box → feeder → splitter → n drops → ONU boxes (index `spare` drawn as an empty port).
    Returns dict(olt, feeder, sp, drops, onus, all)."""
    olt = ct_box(olt_label, OLTC, 1.35, 0.55, size).move_to([x_olt, y, 0])
    sp = splitter(0.32).move_to([x_sp, y, 0])
    feeder = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=2.5)
    ys = [y + dy * (n - 1) / 2 - dy * k for k in range(n)]
    drops, onus = VGroup(), VGroup()
    for k, yy in enumerate(ys):
        end = [x_onu - onu_w / 2, yy, 0]
        drops.add(Line(sp.get_right(), end, color=FEED, stroke_width=2))
        if spare is not None and k == spare:
            port = VGroup(Circle(radius=0.09, stroke_color=MUTED, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(end),
                          T("boş port", 15, MUTED, BOLD).next_to(end, RIGHT, buff=0.18))
            onus.add(port)
        else:
            onus.add(onu_box(f"ONU {k + 1}", ONUC, onu_w, 0.46, 15).move_to([x_onu, yy, 0]))
    return {"olt": olt, "feeder": feeder, "sp": sp, "drops": drops, "onus": onus, "all": VGroup(olt, feeder, sp, drops, onus)}


def attacker(label="saldırgan", size=15, r=0.2, lpos=DOWN):
    """Red device icon (rogue / attacker); label below (or at `lpos`)."""
    b = RoundedRectangle(corner_radius=0.06, width=r * 3.2, height=r * 2.1, stroke_color=ATKC, stroke_width=2.2, fill_color=ATKC, fill_opacity=0.18)
    led = Dot(radius=0.04, color=ATKC).move_to(b.get_corner(UR) + [-0.12, -0.1, 0])
    t = T(label, size, ATKC, BOLD).next_to(b, lpos, buff=0.08)
    return VGroup(b, led, t)


def eye_icon(color=WARN, s=0.32):
    outer = VGroup(ArcBetweenPoints(LEFT * s, RIGHT * s, angle=-PI * 0.55, color=color, stroke_width=2.4),
                   ArcBetweenPoints(LEFT * s, RIGHT * s, angle=PI * 0.55, color=color, stroke_width=2.4))
    pupil = Dot(radius=s * 0.25, color=color)
    return VGroup(outer, pupil)


def flow_box(title, sub=None, color=ACC, w=2.6, h=0.78, tsize=17, ssize=14):
    return sbox(title, sub, color, w, h, tsize, ssize)


def ptr_box(title, body, color=GOLD, w=4.4, h=1.15, tsize=19, bsize=16):
    """Pointer box for an annex whose body is only a reference (Annex C / D)."""
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=2.2, fill_color=PANEL, fill_opacity=1)
    g = VGroup(T(title, tsize, color, BOLD), T(body, bsize, TXT, SEMIBOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fit(g, w - 0.4).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.22)
    return VGroup(r, g)


def ascii_hex(label, hexs, color, size=16, hsize=15, w=None):
    """'ASCII label' over its hex (two rows), left-aligned."""
    a = T(f"“{label}”", size, color, BOLD)
    b = HX("0x" + hexs, hsize, MUTED, BOLD)
    g = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
    if w:
        fit(g, w)
    return g


class Act18(Act17):
    def rev(self, items, rt=0.4, shift=UP * 0.06):
        """Reveal [(mobject, cue_substring, default)] one by one at their cues."""
        for m, sub, d in items:
            self.at(self.cue(sub, d))
            self.play(FadeIn(m, shift=shift), run_time=rt)

    def heading18(self, s, old=None, w=10.0):
        return self.heading12(s, old, w)
