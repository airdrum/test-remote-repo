"""S2·B7 (ep17) shared helpers — 'Renk Değiştirmek': channel management, handover, locking and bonding
(G.989.3 §17, Ek F, Ek H, Ek X; Amd.2 changes to O8/O9).

Builds on the season-2 blocks chained through ep16_common → ep14_common → ep13_common → ep12_common → ep11_common
(bit-proportional `fields`, analyzer panels, sequence-chart `lifeline`/`msg`/`ct_box`/`onu_box`, S1/S2 chips, `mtable`,
`strip`, `SyncSM`, `OnuSM`, `pmd_head`, `cue_n`, `frame_axis`, `octets`, `term`, laser/clock icons, fitted title cards,
header shrinking) and borrows a few PLOAM pieces from ep15_common (`keychip`, `mbox`, `inst`, `chk`). Only the episode
names, the handover colours, the NACK/ROLLBACK code tables, the OLT handover state machine and a few small plot pieces
are added here."""
from ep16_common import *
from ep15_common import keychip, mbox, inst, chk, DKC, BCC

K17 = 7
EP17 = SERIES["season2"]["episodes"][K17 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep17_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K17}"
H17 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M17(p):
    return f"build/ep17/{p}/audio_proc/manifest.json"


M = M17

# source / target channel terminations are two wavelength channels → channel colours λ1 / λ3
SRCC, TGTC = CH[0], CH[2]
# OLT wavelength handover states (Table 17-5)
UNC, EXC, HOC, RDC, SOC = "#64748B", GOLD, GOOD, "#60A5FA", "#FB923C"
OST = {1: ("habersiz", "Unaware", UNC), 2: ("bekleme", "Expecting", EXC), 3: ("barındırma", "Hosting", HOC),
       4: ("yönlendirme", "Redirecting", RDC), 5: ("uğurlama", "Seeing-Off", SOC)}
# Tuning_Response operations · ICTP · timers
ACKC, NACKC, RBC, CMPC, ICTC = GOOD, WARN, PINK, ACC, ICT
# code groups of Tables 17-3 / 17-4
GRC = {"INT": "#C084FC", "DS": "#60A5FA", "US": GOLD, "COM": WARN, "—": "#334155"}
# G.989.2 Table 9-2 tuning classes · accuracy classes (§11.2.6.4) · Annex F parts
CLC = {"1": GOOD, "2": GOLD, "3": WARN}
ACCC = ["#64748B", WARN, GOLD, GOOD]
ACCN = ["duyurulmamış", "kalibre değil", "gevşek", "yeterli"]
PREPC, PMDTC, RSYC = "#94A3B8", "#A78BFA", ACC

# Table 17-3 (NACK, before tuning) and Table 17-4 (ROLLBACK, after tuning): (bit value, group, code, short condition)
NACK = [(0x0001, "INT", "INT_SFC", "planlı çerçevede hazır değil"), (0x0002, "DS", "DS_ALBL", "yönetim etiketi"),
        (0x0004, "DS", "DS_VOID", "boş tanım"), (0x0008, "DS", "DS_PART", "bölüm"), (0x0010, "DS", "DS_TUNR", "alıcı ayar aralığı"),
        (0x0020, "DS", "DS_LNRT", "hız"), (0x0040, "DS", "DS_LNCD", "hat kodu"), (0x0080, "US", "US_ALBL", "yönetim etiketi"),
        (0x0100, "US", "US_VOID", "boş tanım"), (0x0200, "US", "US_TUNR", "verici ayar aralığı"), (0x0400, "US", "US_CLBR", "kalibrasyon"),
        (0x0800, "US", "US_LKTP", "bağlantı tipi"), (0x1000, "US", "US_LNRT", "hız"), (0x2000, "US", "US_LNCD", "hat kodu")]
RBK = [(0x0001, "COM", "COM_DS", "hedefte ↓ senkron yok"), (0x0002, "DS", "DS_ALBL", "PSBd etiketi"),
       (0x0004, "DS", "DS_LKTP", "PSBd bağlantı tipi"), (0x0008, "US", "US_ALBL", "yönetim etiketi"), (0x0010, "US", "US_VOID", "boş tanım"),
       (0x0020, "US", "US_TUNR", "verici ayar aralığı"), (0x0040, "US", "US_LKTP", "bağlantı tipi"), (0x0080, "US", "US_LNRT", "hız"),
       (0x0100, "US", "US_LNCD", "hat kodu")]


def bitmap16(table, value=None, cw=0.62, h=0.5, size=15, show_idx=True, isize=14):
    """Tuning_Response octets 6–7 as 16 cells (bit 15 left … bit 0 right), coloured by code group of `table`.
    Set bits of `value` are filled; returns VGroup(cells, index labels). cells[k] is bit 15 − k."""
    grp = {b.bit_length() - 1: g for b, g, _, _ in table}
    cells = VGroup()
    for k in range(16):
        bit = 15 - k
        c = GRC[grp.get(bit, "—")]
        on = value is not None and (value >> bit) & 1
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.85 if on else 0.14)
        t = HX("1" if on else "0", size, BG if on else (TXT if bit in grp else MUTED), BOLD).move_to(r)
        cells.add(VGroup(r, t))
    cells.arrange(RIGHT, buff=0)
    idx = VGroup()
    if show_idx:
        for k, c in enumerate(cells):
            idx.add(T(str(15 - k), isize, MUTED, BOLD).next_to(c, UP, buff=0.06))
    return VGroup(cells, idx)


def set_bits(bm, value, table):
    """Animations that set the cells of a bitmap16 to `value`."""
    grp = {b.bit_length() - 1: g for b, g, _, _ in table}
    out = []
    for k, cell in enumerate(bm[0]):
        bit = 15 - k
        on = (value >> bit) & 1
        new = HX("1" if on else "0", cell[1].font_size, BG if on else (TXT if bit in grp else MUTED), BOLD).move_to(cell[1])
        out += [cell[0].animate.set_fill(opacity=0.85 if on else 0.14), Transform(cell[1], new)]
    return out


def code_chip(bit, code, grp, size=15, w=None, mono=True):
    """'0x0010 DS_TUNR' chip in the group colour."""
    c = GRC[grp]
    g = VGroup(HX(f"0x{bit:04X}", size, c, BOLD), HX(code, size, TXT, BOLD)).arrange(RIGHT, buff=0.14)
    r = RoundedRectangle(corner_radius=0.06, width=(w or g.width + 0.26), height=g.height + 0.16, stroke_color=c, stroke_width=1.5,
                         fill_color=c, fill_opacity=0.12)
    g.move_to(r)
    if w:
        g.align_to(r, LEFT).shift(RIGHT * 0.12)
    return VGroup(r, g)


def ostate(k, w=2.25, h=0.82, tsize=19, ssize=14):
    a, b, c = OST[k]
    return sbox(f"({k}) {a}", b, c, w, h, tsize, ssize)


class OltSM:
    """OLT CT wavelength handover state machine (G.989.3 Table 17-5 / 17-9) on a pentagon:
    (1) habersiz left, (2) bekleme upper left, (3) barındırma upper right, (4) yönlendirme right, (5) uğurlama bottom."""
    POS = {1: (-4.45, -0.55), 2: (-2.3, 1.25), 3: (2.3, 1.25), 4: (4.45, -0.55), 5: (0.0, -2.2)}

    def __init__(self, dy=0.0, w=2.25, h=0.82):
        self.b = {k: ostate(k, w, h).move_to([x, y + dy, 0]) for k, (x, y) in self.POS.items()}

    def boxes(self):
        return VGroup(*[self.b[k] for k in sorted(self.b)])

    def edge(self, a, sa, b, sb, label, color, oa=0.0, ob=0.0, lpos=UP, lbuff=0.06, size=15, angle=0.0, lshift=ORIGIN):
        def pt(k, s, o):
            bx = self.b[k][0]
            return {"L": bx.get_left() + UP * o, "R": bx.get_right() + UP * o, "T": bx.get_top() + RIGHT * o, "B": bx.get_bottom() + RIGHT * o}[s]
        p0, p1 = pt(a, sa, oa), pt(b, sb, ob)
        ar = carrow(p0, p1, angle, color, 2.4, 0.14) if angle else arrow(p0, p1, color, 2.4, 0.14)
        g = VGroup(ar)
        if label:
            t = T(label, size, color, BOLD, line_spacing=0.8)
            t.next_to(ar.point_from_proportion(0.5), lpos, buff=lbuff).shift(lshift)
            g.add(t)
        return g


def tline(x0, x1, y, color=MUTED, sw=2):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=sw)


def tmark(x, y0, y1, label, color=GOLD, size=15, pos=UP, dashed=True):
    """Vertical event marker on a time line with a label above (or below)."""
    ln = (DashedLine if dashed else Line)([x, y0, 0], [x, y1, 0], color=color, stroke_width=1.8)
    t = T(label, size, color, BOLD).next_to(ln, pos, buff=0.06)
    return VGroup(ln, t)


def gauss_curve(X, Y, f0, f1, loss_at, at_ghz, color=ACC, n=60, sw=3):
    """Transmission (dB, ≤ 0) of a Gaussian filter: loss(f) = loss_at·(f/at_ghz)²; drawn over [f0, f1]."""
    fs = np.linspace(f0, f1, n)
    pts = [[X(f), Y(-loss_at * (f / at_ghz) ** 2), 0] for f in fs]
    return VMobject(stroke_color=color, stroke_width=sw).set_points_smoothly(pts)


def onu_tag(s, color=ONUC, size=15):
    return tag(s, color, size)


def msg3(xa, xb, y, text, color=GOLD, lx=None, size=15, dashed=False, above=True, sw=2.6):
    """Sequence-chart message xa → xb at y; the label is centred over the segment lx = (x0, x1) (default: the whole arrow)."""
    g = msg(xa, xb, y, "", color, size, dashed, above, sw)
    a = g[0]
    x0, x1 = lx if lx else (min(xa, xb), max(xa, xb))
    t = tf(text, size, color, BOLD, w=abs(x1 - x0) - 0.2).next_to([(x0 + x1) / 2, y, 0], UP if above else DOWN, buff=0.07)
    return VGroup(a, t)


def grow_msg(m):
    """Animations that draw a msg/msg3 group (solid or dashed arrow) and its label."""
    a = m[0]
    out = [GrowArrow(a)] if isinstance(a, Arrow) else [Create(a[0]), GrowArrow(a[1])]
    return out + [FadeIn(m[1])]


def ictp_bar(x0, x1, y, text, color=ICT, size=15, h=0.16):
    """ICTP interaction between two OLT CTs: a horizontal bar (Figure 17-1 legend) with its label above."""
    r = RoundedRectangle(corner_radius=h / 2, width=abs(x1 - x0), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([(x0 + x1) / 2, y, 0])
    t = tf(text, size, color, BOLD, w=abs(x1 - x0) + 0.4).next_to(r, UP, buff=0.07)
    return VGroup(r, t)


def chamber_icon(w=1.6, h=1.15, label="Sıcaklık kabini"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    door = RoundedRectangle(corner_radius=0.06, width=w * 0.55, height=h * 0.7, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1)
    door.move_to(body).shift(LEFT * w * 0.14)
    th = VGroup(RoundedRectangle(corner_radius=0.03, width=0.07, height=h * 0.45, stroke_color=WARN, stroke_width=1.5),
                Circle(radius=0.07, stroke_color=WARN, fill_color=WARN, fill_opacity=0.9, stroke_width=1.5))
    th[1].next_to(th[0], DOWN, buff=-0.02)
    th.move_to(body).shift(RIGHT * w * 0.3)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, door, th, lab)


class Act17(Act16):
    def heading17(self, s, old=None, w=10.0):
        return self.heading12(s, old, w)

    def reset(self, s, badge=None, rt=0.6, w=10.0, extra=()):
        """Clear the stage, swap the heading (and the badge) in one play — saves the beat-start time of clear + badge + heading."""
        keep = {self.hdr, self.badge}
        out = [m for m in self.mobjects if m not in keep]
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

    def to_header_badge(self, g, key, rt=0.7, extra=()):
        """Title card → header and the first badge in one play."""
        bs, bc = BADGE[key]
        new = pill(bs, bc, 20).to_corner(UR, buff=0.35)
        self.play(ReplacementTransform(g, self.hdr), FadeIn(new, shift=LEFT * 0.2), *extra, run_time=rt)
        self.badge = new

    def pmd_reset(self, title, chip, rt=0.6):
        """PMD Köprüsü beat chrome in one play: clear, badge → pmd, new heading and the season-1 chip at its right."""
        h = self.heading(title)
        fit(h, 10.0)
        h.next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
        ch = self.chip_at(chip, h)
        return self.reset(title, "pmd", rt, extra=[FadeIn(ch, shift=LEFT * 0.1)]), ch

    def lanes(self, xs=(-5.4, -2.3, 0.8), top=2.2, bot=-3.35, names=("Kaynak CT", "Hedef CT", "ONU"), cols=(SRCC, TGTC, ONUC), w=1.6):
        """Three-lane sequence chart heads + lifelines: Source CT · Target CT · ONU."""
        return VGroup(*[lifeline(n, x, top, bot, c, w, 0.5, 16) for n, x, c in zip(names, xs, cols)])

    def num(self, k, x, y, color=GOLD, r=0.19):
        c = VGroup(Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1), T(str(k), 15, color, BOLD))
        c[1].move_to(c[0])
        return c.move_to([x, y, 0])
