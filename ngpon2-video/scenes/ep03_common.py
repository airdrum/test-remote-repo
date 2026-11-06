"""B03 shared helpers: headers, manifests, spectrum axes and bands."""
from kit import *

EP3 = SERIES["episodes"][2]
H3 = {1: "BÖLÜM 3 · PERDE 1 — Spektrum haritası", 2: "BÖLÜM 3 · PERDE 2 — Komşular", 3: "BÖLÜM 3 · PERDE 3 — Izgaralar",
      4: "BÖLÜM 3 · PERDE 4 — Raman", 5: "BÖLÜM 3 · PERDE 5 — Kanal profilleri",
      "L": "BÖLÜM 3 · LABORATUVARDA — Kanal haritası ve yalıtım", "E": "BÖLÜM 3 · KAPANIŞ"}


def M3(p):
    return f"build/ep03/{p}/audio_proc/manifest.json"


TW_US, TW_DS, PTP, VIDEO = "#A78BFA", ACC, PINK, "#FB923C"


class Act3(Act):
    def cue(self, sub, default=0.0):
        """Start time (−0.2 s) of the first phrase cue of the current beat containing `sub`."""
        for c in self.bmap[self.timeline[-1]["id"]]["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        return default


def nm_axis(nm0, nm1, x0=-6.2, x1=6.2, y=-1.6, step=10, label_every=None, size=14):
    """Horizontal wavelength axis. Returns (VGroup(axis, ticks, labels), X) where X(nm) → scene x."""
    X = lambda nm: x0 + (nm - nm0) / (nm1 - nm0) * (x1 - x0)
    ax = Line([x0, y, 0], [x1, y, 0], color=MUTED, stroke_width=2)
    ticks, labs = VGroup(), VGroup()
    label_every = label_every or step
    v = int(np.ceil(nm0 / step) * step)
    while v <= nm1:
        ticks.add(Line([X(v), y - 0.06, 0], [X(v), y + 0.06, 0], color=MUTED, stroke_width=1.5))
        if v % label_every == 0:
            labs.add(T(str(v), size, MUTED).next_to([X(v), y, 0], DOWN, buff=0.1))
        v += step
    unit = T("nm", size, MUTED).next_to([x1, y, 0], RIGHT, buff=0.12)
    return VGroup(ax, ticks, labs, unit), X


def band(X, a, b, y, h, color, label=None, op=0.85, lsize=14, lcolor=None, where="in"):
    r = Rectangle(width=max(X(b) - X(a), 0.03), height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to([(X(a) + X(b)) / 2, y, 0])
    g = VGroup(r)
    if label:
        t = T(label, lsize, lcolor or (BG if where == "in" else color), BOLD)
        if where == "in":
            t.move_to(r)
            if t.width > r.width - 0.06:
                t.scale_to_fit_width(max(r.width - 0.06, 0.2))
        elif where == "up":
            t.next_to(r, UP, buff=0.06)
        else:
            t.next_to(r, DOWN, buff=0.06)
        g.add(t)
    return g


def outline_band(X, a, b, y, h, color, label=None, lsize=14, where="up"):
    r = DashedVMobject(Rectangle(width=X(b) - X(a), height=h, color=color, stroke_width=2), num_dashes=40).move_to([(X(a) + X(b)) / 2, y, 0])
    g = VGroup(r)
    if label:
        g.add(T(label, lsize, color, BOLD).next_to(r, UP if where == "up" else DOWN, buff=0.06))
    return g


def comb(X, nms, y, h, color, sw=2.5):
    return VGroup(*[Line([X(v), y - h / 2, 0], [X(v), y + h / 2, 0], color=color, stroke_width=sw) for v in nms])


def thz_to_nm(f):
    return 299792.458 / f
