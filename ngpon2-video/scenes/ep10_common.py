"""B10 shared helpers (season finale: supervision, protection, conformance, the life of an ONU, field cases)."""
from ep05_common import *

EP10 = SERIES["episodes"][9]
H10 = {1: "BÖLÜM 10 · PERDE 1 — Optik katmanı izlemek", 2: "BÖLÜM 10 · PERDE 2 — Koruma",
       3: "BÖLÜM 10 · PERDE 3 — Uyumluluk: test matrisi", 4: "BÖLÜM 10 · PERDE 4 — Bir ONU'nun hayatı",
       "L": "BÖLÜM 10 · SAHADA — Ölçüm çantası ve arıza vakaları", "E": "BÖLÜM 10 · KAPANIŞ"}

# in-process extension of the shared badge table (kit.py itself is untouched)
BADGE.setdefault("saha", ("Sahada", GOOD))

TXON, TXOFF = GOLD, "#334155"     # transmitter lamp on / dark
PROT, UNPROT = GOOD, "#475569"    # protected / unprotected segment
CT_A, CT_B = ACC, "#A78BFA"       # Type B peers (Active-side / Standby-side)
OLTC, ONUC = "#94A3B8", SIG


def M10(p):
    return f"build/ep10/{p}/audio_proc/manifest.json"


def ep_name(n):
    return SERIES["episodes"][n - 1]["title"]


# ---------- small building blocks ---------------------------------------------
def tf(s, size=20, color=TXT, weight=NORMAL, w=None, **kw):
    """T() that is fitted to width w (never below the house minimum)."""
    t = T(s, size, color, weight, **kw)
    if w is not None and t.width > w:
        t.scale_to_fit_width(w)
    return t


def lamp(on, r=0.11):
    """Transmitter indicator: glowing gold when on, dark ring when off."""
    if on:
        return glow_dot(TXON, r * 0.8, 4)
    return VGroup(Circle(radius=r, stroke_color="#64748B", stroke_width=2, fill_color="#0B1220", fill_opacity=1))


def gauge(r=0.32, color=ACC, frac=0.62):
    arc = Arc(radius=r, start_angle=PI, angle=-PI, stroke_color=MUTED, stroke_width=2.5)
    ang = PI - frac * PI
    nd = Line(ORIGIN, r * 0.85 * np.array([np.cos(ang), np.sin(ang), 0]), color=color, stroke_width=3)
    return VGroup(arc, nd, Dot(ORIGIN, radius=0.04, color=color))


def xmark(m, color=WARN, sw=5, pad=0.05):
    c, w, h = m.get_center(), m.width / 2 + pad, m.height / 2 + pad
    return VGroup(Line(c + [-w, -h, 0], c + [w, h, 0], color=color, stroke_width=sw),
                  Line(c + [-w, h, 0], c + [w, -h, 0], color=color, stroke_width=sw))


def strike(m, color=WARN, sw=3):
    return Line(m.get_left() + LEFT * 0.05, m.get_right() + RIGHT * 0.05, color=color, stroke_width=sw)


def tile(label, color=ACC, w=0.95, h=0.46, size=16, op=0.2, sub=None, ssize=14):
    r = RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)
    t = tf(label, size, TXT, BOLD, w=w - 0.1).move_to(r)
    g = VGroup(r, t)
    if sub:
        g.add(tf(sub, ssize, color, SEMIBOLD, w=w + 0.3).next_to(r, DOWN, buff=0.06))
    return g


def dtile(label, color=MUTED, w=0.95, h=0.46, size=15):
    r = DashedVMobject(RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=2), num_dashes=22)
    return VGroup(r, tf(label, size, color, BOLD, w=w - 0.1).move_to(r))


def tag(s, color=MUTED, size=15):
    """Small framed label (e.g. 'yorum', 'temsili')."""
    t = T(s, size, color, SEMIBOLD)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.24, height=t.height + 0.14, stroke_color=color, stroke_width=1.5,
                         fill_color=BG, fill_opacity=0.9)
    return VGroup(r, t.move_to(r))


def epill(n, size=17):
    """Season back-reference badge, e.g. 'B5 · Ayarlanabilir Kulak'."""
    if n is None:
        return VGroup()
    if n == "S2":
        return pill("→ Sezon 2", MUTED, size)
    return pill(f"B{n} · {ep_name(n)}", PINK, size)


def numline(rows, size=20, buff=0.18):
    """Rows of (text, color, bold?) left-aligned."""
    return VGroup(*[T(s, size, c, BOLD if b else NORMAL) for s, c, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def lane(x0, x1, y, color=FEED, sw=3):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=sw)


def ct_box(name, color, w=1.25, h=0.42, size=15, on=None):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.2, fill_color=PANEL, fill_opacity=1)
    t = tf(name, size, TXT, BOLD, w=w - 0.35).move_to(r).shift(LEFT * 0.12)
    g = VGroup(r, t)
    if on is not None:
        g.add(lamp(on, 0.08).move_to(r.get_right() + LEFT * 0.17))
    return g


def onu_icon(label="ONU", color=ONUC, w=1.15, h=0.62, size=17):
    return sbox(label, None, color, w, h, size)


def frames_row(n, x0, y, w, h=0.42, color=TW_DS, labels=None, size=14, op=0.12):
    """n equal frame cells (125 µs each) starting at x0."""
    cells = VGroup()
    for i in range(n):
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=op)
        r.move_to([x0 + w * (i + 0.5), y, 0])
        cells.add(r)
    return cells


class Act10(Act5):
    def ncard(self, num, title, body, w=11.6, h=1.9):
        r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=PINK, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
        n = T(num, 50, PINK, BOLD).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.5)
        g = VGroup(T(title, 25, TXT, BOLD), T(body, 20, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if g.width > w - 1.6:
            g.scale_to_fit_width(w - 1.6)
        if g.height > h - 0.3:
            g.scale_to_fit_height(h - 0.3)
        g.next_to(n, RIGHT, buff=0.45)
        return VGroup(r, n, g)

    def note10(self, bid, lines, badge="not", h=None):
        """Engineer note: lines = [(num, title, body, cue_substring)] — 2 or 3 cards."""
        self.beat(bid)
        self.clear()
        self.set_badge(badge)
        k = len(lines)
        h = h or (1.9 if k <= 2 else 1.62)
        cards = VGroup(*[self.ncard(n, t, b, h=h) for n, t, b, _ in lines]).arrange(DOWN, buff=0.4 if k <= 2 else 0.28).move_to(DOWN * 0.35)
        for c, (_, _, _, sub) in zip(cards, lines):
            self.at(self.cue(sub, 0.5))
            self.play(FadeIn(c, shift=UP * 0.25), run_time=0.7)
        self.end(pad=0.15)
        return cards
