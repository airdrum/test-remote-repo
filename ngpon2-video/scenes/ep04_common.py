"""B04 shared helpers: headers, manifests, eye diagrams, laser spectra, frame bars."""
import sys

from ep03_common import *

EP4 = SERIES["episodes"][3]
EP5 = SERIES["episodes"][4]
H4 = {1: "BÖLÜM 4 · PERDE 1 — Hız, saat ve hat kodu", 2: "BÖLÜM 4 · PERDE 2 — Güç ve sönüm oranı", 3: "BÖLÜM 4 · PERDE 3 — Spektrum",
      4: "BÖLÜM 4 · PERDE 4 — Göz maskesi ve titreşim", 5: "BÖLÜM 4 · PERDE 5 — TC köprüsü: 125 µs çerçeve",
      "L": "BÖLÜM 4 · LABORATUVARDA — Verici testleri", "E": "BÖLÜM 4 · KAPANIŞ"}
OC_C, PSY_C, SFC_C, FEC_C = "#A78BFA", GOLD, ACC, PINK


def M4(p):
    return f"build/ep04/{p}/audio_proc/manifest.json"


def tr(x, fmt):
    return fmt.format(x).replace(".", ",")


def mini_axes(x0, y0, w, h, xl, yl, color=MUTED, xbuff=0.42, size=15):
    """Hand-drawn axes; the x title sits centred below the tick labels, the y title above the axis."""
    o = np.array([x0, y0, 0])
    g = VGroup(Line(o, o + [w, 0, 0], color=color, stroke_width=2), Line(o, o + [0, h, 0], color=color, stroke_width=2))
    g.add(T(xl, size, color).next_to(o + [w / 2, 0, 0], DOWN, buff=xbuff) if xl else VGroup())
    g.add(T(yl, size, color).next_to(o + [0, h, 0], UP, buff=0.08).align_to(o, LEFT) if yl else VGroup())
    return g


class Act4(Act3):
    def cue(self, sub, default=0.0):
        for c in self.bmap[self.timeline[-1]["id"]]["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        print(f"CUE MISS {self.timeline[-1]['id']}: {sub!r}", file=sys.stderr)
        return default

    def ci(self, bid, sub, default=1):
        for k, c in enumerate(self.bmap[bid]["cues"]):
            if sub in c["text"]:
                return k
        print(f"CUE MISS {bid}: {sub!r}", file=sys.stderr)
        return default

    def note2(self, bid, n1, n2):
        """Two-point engineer note; points start at the 'Bir:' and 'İki:' phrases."""
        return self.engineer_note(bid, [("1", n1[0], n1[1], self.ci(bid, "Bir:")), ("2", n2[0], n2[1], self.ci(bid, "İki:"))])

    def bridge_beat(self, bid, text, label="Sıradaki", pad=0.4):
        self.beat(bid)
        self.clear()
        self.drop_badge()
        b = self.bridge(label, text)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.8)
        self.end(pad=pad)
        self.play(FadeOut(b), run_time=0.5)


# ---------- eye diagram ----------------------------------------------------------
def step2(t, ov=0.12, tr10=0.25):
    """Second-order step response (t in UI, 0 before the edge)."""
    if t <= 0:
        return 0.0
    z = 0.56 if ov > 0.005 else 1.0
    if ov > 0.005:
        z = -np.log(ov) / np.sqrt(np.pi ** 2 + np.log(ov) ** 2)
    wn = (1 - 0.4167 * z + 2.917 * z ** 2) / tr10
    if z >= 0.999:
        return 1 - np.exp(-wn * t) * (1 + wn * t)
    wd = wn * np.sqrt(1 - z ** 2)
    return 1 - np.exp(-z * wn * t) * (np.cos(wd * t) + z / np.sqrt(1 - z ** 2) * np.sin(wd * t))


def eye_traces(o, W, H, color=TW_DS, ov=0.12, tr10=0.25, u0=-0.3, u1=1.3, sw=2.0, op=0.5, seed=4, jit=0.025, noise=0.015):
    """Overlaid NRZ traces. o = scene point of (0 UI, level 0); W units per UI; H units per unit level."""
    rng = np.random.default_rng(seed)
    out = VGroup()
    us = np.linspace(u0, u1, 90)
    lead = 0.12
    for k in range(32):
        bits = [(k >> j) & 1 for j in range(5)]  # bits for UI −3 … 1
        dj = jit * rng.standard_normal(5)
        dn = noise * rng.standard_normal()
        pts = []
        for u in us:
            v = bits[0]
            for j in range(1, 5):
                e = (j - 3) - lead + dj[j]
                v += (bits[j] - bits[j - 1]) * step2(u - e, ov, tr10)
            pts.append(o + np.array([u * W, (v + dn) * H, 0]))
        out.add(VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=op, fill_opacity=0).set_points_smoothly(pts))
    return out


def eye_mask(o, W, H, x2=0.4, x3=0.6, y1=0.25, y2=0.75, y3=0.25, y4=0.25, u0=-0.3, u1=1.3, vtop=1.5, vbot=-0.5, color=WARN, op=0.32):
    P = lambda u, v: o + np.array([u * W, v * H, 0])
    inner = Polygon(P(x2, y1), P(x3, y1), P(x3, y2), P(x2, y2), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)
    top = Polygon(P(u0, 1 + y3), P(u1, 1 + y3), P(u1, vtop), P(u0, vtop), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)
    bot = Polygon(P(u0, -y4), P(u1, -y4), P(u1, vbot), P(u0, vbot), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)
    return VGroup(inner, top, bot)


def eye_frame(o, W, H, u0=-0.3, u1=1.3, vtop=1.5, vbot=-0.5):
    """Dark screen rectangle behind an eye."""
    a, b = o + np.array([u0 * W, vbot * H, 0]), o + np.array([u1 * W, vtop * H, 0])
    return Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_color="#334155", stroke_width=1.5, fill_color="#050810",
                     fill_opacity=1).move_to((a + b) / 2)


# ---------- laser spectrum in dB ---------------------------------------------------
def spec_db(o, sx, sy, modes, xr, floor=-55.0, w=0.05, color=TW_DS, sw=3.0, top=0.0, n=400):
    """Spectrum curve: modes = [(x, dB)], Lorentzian lines on a floor. Plots dB relative to `top` (0 at axis top)."""
    xs = np.linspace(xr[0], xr[1], n)
    p = np.full_like(xs, 10 ** (floor / 10))
    for x0, db in modes:
        p += 10 ** (db / 10) / (1 + ((xs - x0) / w) ** 2)
    ydb = 10 * np.log10(p)
    pts = [o + np.array([x * sx, (y - floor) * sy, 0]) for x, y in zip(xs, ydb)]
    return VMobject(color=color, stroke_width=sw).set_points_as_corners(pts)


# ---------- downstream frame helpers ------------------------------------------------
def seg_bar(parts, y, x0, h=0.6, size=16, sw=2):
    """parts: [(label, width, color, fill_opacity)] laid left→right from x0. Returns VGroup of VGroup(rect, label)."""
    g, x = VGroup(), x0
    for lab, w, c, op in parts:
        r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=sw, fill_color=c, fill_opacity=op).move_to([x + w / 2, y, 0])
        t = T(lab, size, TXT if op < 0.5 else BG, BOLD) if lab else VGroup()
        if lab:
            t.move_to(r)
            if t.width > w - 0.08:
                t.scale_to_fit_width(max(w - 0.08, 0.1))
        g.add(VGroup(r, t))
        x += w
    return g


def nrz_wave(bits, x0, tb, ylo, yhi, color=TW_DS, sw=3, rise=0.04):
    return VMobject(color=color, stroke_width=sw).set_points_as_corners(nrz(bits, x0, tb, ylo, yhi, rise))
