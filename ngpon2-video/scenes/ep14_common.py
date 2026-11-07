"""S2·B4 (ep14) shared helpers — 'Paylaşım': resource allocation and DBA (G.989.3 §7, §6.1.5.7, §13.1, Ek IX, Ek J, Ek K).

Builds on the season-2 blocks chained through ep13_common → ep12_common → ep11_common (bit-proportional `fields`, `strip`,
`seg`, analyzer panels, sequence-chart helpers, S1/S2 chips, `mtable`, `SyncSM`, `pmd_head`, `cue_n`, `tg_icon`, `Act13`);
only the episode names, the traffic-descriptor colours and a few small allocation/timing pieces are added here."""
from ep13_common import *

K14 = 4
EP14 = SERIES["season2"]["episodes"][K14 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep14_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K14}"
H14 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M14(p):
    return f"build/ep14/{p}/audio_proc/manifest.json"


M = M14

# traffic descriptor components (§7.1) · timing parameters · DBA methods (§7.2.3)
FXC, ASC, NAC, BEC, RMC = "#60A5FA", GOOD, GOLD, "#FB923C", WARN
TJC, TBC, TPC = ACC, "#A78BFA", PINK
SRC, TMC, COC = ACC, "#A78BFA", GOLD
TIMC = "#60A5FA"
ALLOC14 = [("Alloc-ID", 14, ACC), ("DBRu", 1, GOLD), ("PLOAMu", 1, GOLD), ("StartTime", 16, TIMC), ("GrantSize", 16, TIMC),
           ("FWI", 1, PINK), ("Profil", 2, "#C084FC"), ("HEC", 13, HECC)]
OVC = "#64748B"   # per-burst overhead (Tplo)
FLOWC = {"A": ACC, "B": "#A78BFA", "C": BEC, "D": FXC, "E": PINK}


def octets(spec, w, h=0.55, size=16, osize=14, op=0.2):
    """PLOAM-style octet map: spec = [(label, rel_w, color, octet_range)] → cells VGroup(rect, label, range); centred at origin."""
    tot = sum(s[1] for s in spec)
    g = VGroup()
    x = -w / 2
    for lab, rw, c, rng in spec:
        cw = w * rw / tot
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=op).move_to([x + cw / 2, 0, 0])
        t = tf(lab, size, TXT, BOLD, w=cw - 0.1).move_to(r) if lab else VGroup()
        o = tf(rng, osize, c, BOLD, w=cw + 0.05).next_to(r, DOWN, buff=0.07) if rng else VGroup()
        g.add(VGroup(r, t, o))
        x += cw
    return g


def frame_axis(n, x0, x1, y, labels=True, size=14, color=MUTED, every=1, fmt=None):
    """Time axis in 125 µs frames: n frames between x0 and x1. Returns (VGroup(line, ticks, labels), X(frame))."""
    X = lambda f: x0 + f / n * (x1 - x0)
    ax = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2)
    tk = VGroup(*[Line([X(k), y - 0.07, 0], [X(k), y + 0.07, 0], color=color, stroke_width=1.5) for k in range(n + 1)])
    lb = VGroup()
    if labels:
        fmt = fmt or (lambda k: str(k))
        lb = VGroup(*[T(fmt(k), size, color).next_to([X(k), y, 0], DOWN, buff=0.08) for k in range(0, n + 1, every)])
    return VGroup(ax, tk, lb), X


def queue(n, color=SAC, cells=5, cw=0.2, h=0.36, sw=1.6):
    """Small FIFO buffer icon (open on the left) with n filled cells on the right."""
    cl = VGroup(*[Rectangle(width=cw, height=h - 0.08, stroke_width=0, fill_color=color, fill_opacity=0.75 if i >= cells - n else 0.0)
                  for i in range(cells)]).arrange(RIGHT, buff=0.03)
    W = cl.width + 0.12
    fr = VGroup(Line([-W / 2, h / 2, 0], [W / 2, h / 2, 0], color=color, stroke_width=sw),
                Line([-W / 2, -h / 2, 0], [W / 2, -h / 2, 0], color=color, stroke_width=sw),
                Line([W / 2, h / 2, 0], [W / 2, -h / 2, 0], color=color, stroke_width=sw))
    return VGroup(fr, cl.move_to([0.02, 0, 0]))


def hbar(x0, y, w, color, h=0.42, op=0.55, label=None, size=16, lcolor=None):
    """Left-anchored horizontal bar (charts); optional value label right of it."""
    r = Rectangle(width=max(w, 0.02), height=h, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=op).move_to([x0 + max(w, 0.02) / 2, y, 0])
    g = VGroup(r)
    if label:
        g.add(T(label, size, lcolor or color, BOLD).next_to(r, RIGHT, buff=0.12))
    return g


def spool(label, color=FEED, r=0.42):
    """Fibre spool icon with a label below."""
    rings = VGroup(*[Circle(radius=r * k, color=color, stroke_width=1.6, stroke_opacity=0.5 + 0.12 * i) for i, k in enumerate((1.0, 0.82, 0.64))])
    hub = Circle(radius=r * 0.3, color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(rings, DOWN, buff=0.1)
    return VGroup(rings, hub, lab)


def sym(name, sub="", color=TXT, size=24, ssize=None):
    """Symbol with a subscript-looking suffix, e.g. sym('R', 'F') → R_F (Inter has no real subscripts)."""
    a = T(name, size, color, BOLD)
    if not sub:
        return VGroup(a)
    b = T(sub, ssize or int(size * 0.62), color, BOLD).next_to(a, RIGHT, buff=0.02).align_to(a, DOWN).shift(DOWN * size * 0.0045)
    return VGroup(a, b)


def term(s, name, color=TXT, size=24, nsize=15, mono=False):
    """Equation term with its name written underneath (reference-model equations as named terms)."""
    t = HX(s, size - 2, color, BOLD) if mono else T(s, size, color, BOLD)
    n = T(name, nsize, color if color != TXT else MUTED, SEMIBOLD).next_to(t, DOWN, buff=0.12)
    return VGroup(t, n)


class Act14(Act13):
    pass
