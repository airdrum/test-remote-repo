"""S2·B3 (ep13) shared helpers — 'XGEM': encapsulation, delineation, fragmentation, service mapping
(G.989.3 §9, Ek I, §15.4).

Builds on the season-2 blocks of ep11_common / ep12_common (bit-proportional `fields`, `seg`, `strip`, `xgem_run`,
analyzer panels, episode chips, monospace hex, tables); only the episode names and a few XGEM pieces are added here."""
import sys

from ep12_common import *

K13 = 3
EP13 = SERIES["season2"]["episodes"][K13 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep13_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K13}"
H13 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M13(p):
    return f"build/ep13/{p}/audio_proc/manifest.json"


M = M13

# XGEM header fields (Fig. 9-2) · payload / padding / idle
PLIC, KIC, PIDC, OPTC, LFC = GOLD, PINK, ACC, "#64748B", GOOD
PADC, IDC = "#FB923C", "#64748B"
XH = [("PLI", 14, PLIC), ("KI", 2, KIC), ("XGEM Port-ID", 16, PIDC), ("Options", 18, OPTC), ("LF", 1, LFC), ("HEC", 13, HECC)]
IDLE_HDR = "0000FFFF0000299E"


def xhdr(w=12.4, h=0.6, size=18, wsize=14, show_w=True, unit=" bit", lpos=DOWN):
    """The 64-bit XGEM header, field widths proportional to bit counts (narrow-field labels below by default)."""
    return fields(XH, w, h, size, wsize, show_w=show_w, unit=unit, lpos=lpos)


def frame_box(title, color, w, h, tsize=19):
    """Panel with a title in its top-left corner. Returns VGroup(rect, title)."""
    r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=2.2, fill_color=PANEL, fill_opacity=1)
    t = T(title, tsize, color, BOLD).move_to(r.get_corner(UL) + [0.3, -0.3, 0], aligned_edge=LEFT)
    return VGroup(r, t)


def pay(L):
    """Formula (9-1): XGEM payload size P for a non-idle frame with PLI = L."""
    return 0 if L == 0 else (8 if L < 8 else 4 * -(-L // 4))


# ---------- strip parts (for ep12 `strip`) -------------------------------------------
def H_(w=0.34, lab="H", c=SAC):
    return (w, lab, c, 0.55)


def P_(w, lab="", c=SAC):
    return (w, lab, c, 0.14)


def PAD_(w, lab=""):
    return (w, lab, PADC, 0.45)


def IH_(w=0.34, lab="H"):
    return (w, lab, IDC, 0.55)


def IP_(w, lab="boş"):
    return (w, lab, IDC, 0.12)


def FS_(w, lab, c=HLC, op=0.3):
    return (w, lab, c, op)


def words(kinds, cw=0.42, h=0.42, size=14):
    """One square per 4-byte word; kinds = [(label, color, opacity)]. Left-to-right, centred at origin."""
    g = VGroup()
    for lab, c, op in kinds:
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=op)
        cell = VGroup(r)
        if lab:
            cell.add(tf(lab, size, BG if op >= 0.5 else TXT, BOLD, w=cw - 0.06).move_to(r))
        g.add(cell)
    return g.arrange(RIGHT, buff=0)


def hop(x0, x1, y, color=GOLD, sw=2.5, angle=-1.1, tip=0.12):
    """Curved PLI 'jump' arrow above a strip, from x0 to x1 at height y."""
    return CurvedArrow(np.array([x0, y, 0.0]), np.array([x1, y, 0.0]), angle=angle, color=color, stroke_width=sw, tip_length=tip)


def lock(color=GOLD, s=0.32, opened=False):
    """Small padlock icon."""
    body = RoundedRectangle(corner_radius=0.04, width=s, height=s * 0.78, stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.25)
    arc = Arc(radius=s * 0.3, start_angle=0, angle=PI, color=color, stroke_width=2.6).next_to(body, UP, buff=0)
    if opened:
        arc.shift(RIGHT * s * 0.32 + UP * s * 0.08)
    return VGroup(body, arc)


def tg_icon(w=2.15, h=1.55, label="Trafik üreteci"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.82, height=h * 0.56, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.1)
    hs = [0.15, 0.22, 0.4, 0.62, 0.9]
    bars = VGroup(*[Rectangle(width=scr.width * 0.11, height=scr.height * 0.8 * v, stroke_width=0, fill_color=GOOD, fill_opacity=0.85) for v in hs])
    bars.arrange(RIGHT, buff=scr.width * 0.06, aligned_edge=DOWN).move_to(scr).align_to(scr, DOWN).shift(UP * 0.06)
    ports = VGroup(*[Square(0.09, stroke_color="#94A3B8", stroke_width=1.5) for _ in range(4)]).arrange(RIGHT, buff=0.07).move_to(body).shift(DOWN * h * 0.33)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, bars, ports, lab)


def doc_card(title, lines, color=GOLD, w=2.6, h=1.7, tsize=19, lsize=15):
    r = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - 0.3, 0], [w / 2 - 0.3, h / 2, 0], [-w / 2, h / 2, 0],
                stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    g = VGroup(T(title, tsize, color, BOLD), *[T(s, lsize, TXT, BOLD) for s in lines]).arrange(DOWN, buff=0.08)
    fit(g, w - 0.3).move_to(r)
    return VGroup(r, g)


def ok_x(ok, size=22):
    return T("✓" if ok else "✗", size, GOOD if ok else WARN, BOLD)


def eqline(*parts, size=22, buff=0.15):
    """Row of (text, color[, mono]) items."""
    g = VGroup()
    for p in parts:
        s, c = p[0], p[1]
        g.add(HX(s, size - 1, c, BOLD) if len(p) > 2 and p[2] else T(s, size, c, BOLD))
    return g.arrange(RIGHT, buff=buff)


class Act13(Act12):
    def cue_n(self, sub, n, default=0.0):
        """Start time (−0.2 s) of the n-th phrase (1-based) of the current beat containing `sub`."""
        b = self.bmap[self.timeline[-1]["id"]]
        k = 0
        for c in b["cues"]:
            if sub in c["text"]:
                k += 1
                if k == n:
                    return max(0.0, c["t"] - 0.2)
        print(f"CUE MISS [{b['id']}] {sub!r} #{n}", file=sys.stderr)
        return default

    def pmd_head(self, title, chip, old=None):
        """PMD Köprüsü beat chrome: badge, heading and the season-1 chip at the right end of the heading row."""
        self.set_badge("pmd")
        h = self.show_heading(title, old)
        ch = self.chip_at(chip, h)
        return h, ch
