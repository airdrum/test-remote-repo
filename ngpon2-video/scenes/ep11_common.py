"""S2·B1 (ep11) shared helpers — 'Işığın Dili': TC layer intro (G.989.3 §6, App VIII).

Protocol-season building blocks: bit-exact field diagrams, ID range bars, message-sequence charts,
protocol-analyzer panels, season back-reference chips."""
from ep05_common import *

K11 = 1
EP11 = SERIES["season2"]["episodes"][K11 - 1]


def _ptitle(p):
    t = json.loads((ROOT / f"script/ep11_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K11}"
H11 = {1: f"{_S} · PERDE 1 — {_ptitle('p1')}", 2: f"{_S} · PERDE 2 — {_ptitle('p2')}",
       3: f"{_S} · PERDE 3 — {_ptitle('p3')}", 4: f"{_S} · PERDE 4 — {_ptitle('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_ptitle('lab')}", "E": f"{_S} · KAPANIŞ"}


def M11(p):
    return f"build/ep11/{p}/audio_proc/manifest.json"


M = M11

MONO = "JetBrains Mono"
OLTC, ONUC = "#94A3B8", SIG
SAC, FSC, PHC, PMDC = "#A78BFA", ACC, GOLD, "#64748B"      # service adaptation · framing · PHY adaptation · PMD
EMB, PLC, OMC, ICT = ACC, GOLD, "#A78BFA", "#FB923C"       # embedded OAM · PLOAM · OMCC · ICTP
R10, R25 = ACC, "#FB923C"                                   # 9.95328 vs 2.48832 Gbit/s
PTPC = PINK
S1C = "#A78BFA"


def HX(s, size=18, color=TXT, weight=NORMAL, **kw):
    """Monospace text (hex dumps, field values)."""
    return Text(s, font=MONO, font_size=size, color=color, weight=weight, **kw)


def tf(s, size=20, color=TXT, weight=NORMAL, w=None, **kw):
    t = T(s, size, color, weight, **kw)
    if w is not None and t.width > w:
        t.scale_to_fit_width(w)
    return t


def tag(s, color=MUTED, size=15):
    t = T(s, size, color, SEMIBOLD)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.24, height=t.height + 0.14, stroke_color=color, stroke_width=1.5,
                         fill_color=BG, fill_opacity=0.9)
    return VGroup(r, t.move_to(r))


def xmark(m, color=WARN, sw=5, pad=0.05):
    c, w, h = m.get_center(), m.width / 2 + pad, m.height / 2 + pad
    return VGroup(Line(c + [-w, -h, 0], c + [w, h, 0], color=color, stroke_width=sw),
                  Line(c + [-w, h, 0], c + [w, -h, 0], color=color, stroke_width=sw))


def strike(m, color=WARN, sw=3):
    return Line(m.get_left() + LEFT * 0.05, m.get_right() + RIGHT * 0.05, color=color, stroke_width=sw)


def lamp(on, r=0.11):
    if on:
        return glow_dot(GOLD, r * 0.8, 4)
    return VGroup(Circle(radius=r, stroke_color="#64748B", stroke_width=2, fill_color="#0B1220", fill_opacity=1))


def tile(label, color=ACC, w=0.95, h=0.46, size=16, op=0.2, tcolor=TXT):
    r = RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)
    return VGroup(r, tf(label, size, tcolor, BOLD, w=w - 0.12).move_to(r))


def s1chip(n, size=17):
    return pill(f"S1·B{n} · {SERIES['episodes'][n - 1]['title']}", S1C, size)


def s2chip(n, size=17):
    return pill(f"S2·B{n} · {SERIES['season2']['episodes'][n - 1]['title']}", ACC, size)


def ct_box(name, color=OLTC, w=1.3, h=0.5, size=16):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.2, fill_color=PANEL, fill_opacity=1)
    return VGroup(r, tf(name, size, TXT, BOLD, w=w - 0.15).move_to(r))


# ---------- bit-exact field diagrams ------------------------------------------------
def fields(spec, w, h=0.55, size=17, wsize=14, show_w=True, op=0.22, min_label=14, wpos=DOWN, unit="", lpos=UP):
    """spec = [(label, n, color)] → VGroup of cells (VGroup(rect, label, width_label)), widths ∝ n, centred at origin.
    Labels that do not fit inside at >= min_label size are placed outside (lpos side, tiered, with leader lines)."""
    tot = sum(n for _, n, _ in spec)
    cells = VGroup()
    x = -w / 2
    outside = []
    for lab, n, c in spec:
        cw = w * n / tot
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=op).move_to([x + cw / 2, 0, 0])
        wl = T(f"{n}{unit}", wsize, c, BOLD).next_to(r, wpos, buff=0.07) if show_w else VGroup()
        if show_w and wl.width > cw + 0.25:
            wl.scale_to_fit_width(cw + 0.25)
        t = VGroup()
        if lab:
            t = T(lab, size, TXT, BOLD)
            if t.width > cw - 0.08:
                sc = (cw - 0.08) / t.width
                if sc * size >= min_label:
                    t.scale(sc)
                    t.move_to(r)
                else:
                    t = T(lab, min_label, c, BOLD)
                    outside.append((t, r, c))
            else:
                t.move_to(r)
        cells.add(VGroup(r, t, wl))
        x += cw
    # place outside labels in tiers
    sgn = 1 if lpos[1] > 0 else -1
    base = h / 2 + 0.12 + (0.3 if (show_w and np.allclose(wpos, lpos)) else 0)
    last_right = {}
    for t, r, c in outside:
        tier = 0
        while last_right.get(tier, -99) > r.get_x() - t.width / 2 - 0.06:
            tier += 1
        t.move_to([r.get_x(), sgn * (base + t.height / 2 + tier * 0.3), 0])
        last_right[tier] = t.get_right()[0]
        if tier > 0:
            ln = Line([r.get_x(), sgn * h / 2, 0], [r.get_x(), t.get_y() - sgn * t.height / 2 - 0.03, 0], color=c, stroke_width=1.2)
            t.add(ln)
    return cells


def brace_lbl(m, text, color=MUTED, direction=DOWN, size=16, buff=0.06):
    b = Brace(m, direction, color=color, buff=buff)
    t = T(text, size, color, BOLD).next_to(b, direction, buff=0.06)
    return VGroup(b, t)


# ---------- ID range bars ---------------------------------------------------------------
def range_bar(segs, w, h=0.6, size=16, lsize=14):
    """segs = [(label, lo, hi, color, rel_width)] → VGroup of segments; each = VGroup(rect, label, lo_tick, hi_tick)."""
    tot = sum(s[4] for s in segs)
    g = VGroup()
    x = -w / 2
    for lab, lo, hi, c, rw in segs:
        cw = w * rw / tot
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.25).move_to([x + cw / 2, 0, 0])
        t = tf(lab, size, TXT, BOLD, w=cw - 0.1).move_to(r)
        lo_t = T(lo, lsize, c, BOLD).next_to(r.get_corner(DL), DOWN, buff=0.08)
        lo_t.align_to(r, LEFT)
        parts = [r, t, lo_t]
        if hi is not None and hi != lo:
            hi_t = T(hi, lsize, c, BOLD).next_to(r.get_corner(DR), DOWN, buff=0.08)
            hi_t.align_to(r, RIGHT)
            parts.append(hi_t)
        g.add(VGroup(*parts))
        x += cw
    return g


# ---------- message-sequence chart ---------------------------------------------------------
def lifeline(name, x, y0, y1, color, w=1.7, h=0.55, size=17):
    head = ct_box(name, color, w, h, size).move_to([x, y0, 0])
    ln = DashedLine([x, y0 - h / 2, 0], [x, y1, 0], color=color, stroke_width=2, dash_length=0.1)
    return VGroup(head, ln)


def msg(xa, xb, y, text, color=GOLD, size=16, dashed=False, above=True, sw=3):
    a = Arrow([xa, y, 0], [xb, y, 0], buff=0.05, color=color, stroke_width=sw, tip_length=0.18,
              max_tip_length_to_length_ratio=0.1, max_stroke_width_to_length_ratio=20)
    if dashed:
        a = VGroup(DashedLine([xa, y, 0], [xb - np.sign(xb - xa) * 0.18, y, 0], color=color, stroke_width=sw, dash_length=0.12),
                   Arrow([xb - np.sign(xb - xa) * 0.3, y, 0], [xb, y, 0], buff=0.05, color=color, stroke_width=sw, tip_length=0.18,
                         max_tip_length_to_length_ratio=0.6))
    t = tf(text, size, color, BOLD, w=abs(xb - xa) - 0.3).next_to([(xa + xb) / 2, y, 0], UP if above else DOWN, buff=0.08)
    return VGroup(a, t)


# ---------- protocol analyzer / emulator ---------------------------------------------------------
def apanel(w, h, title, color=ACC, tsize=16):
    """Analyzer window: frame + title bar. Returns VGroup(frame, bar, title). Content area below bar."""
    fr = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2, fill_color="#050810", fill_opacity=1)
    bar = Rectangle(width=w - 0.04, height=0.38, stroke_width=0, fill_color=color, fill_opacity=0.18)
    bar.move_to(fr.get_top() + DOWN * 0.21)
    t = tf(title, tsize, color, BOLD, w=w - 0.5).move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.15)
    dots = VGroup(*[Dot(radius=0.035, color=c) for c in (WARN, GOLD, GOOD)]).arrange(RIGHT, buff=0.07).move_to(bar).align_to(bar, RIGHT).shift(LEFT * 0.15)
    return VGroup(fr, bar, t, dots)


def panel_top(p, pad=0.25):
    return p[1].get_bottom()[1] - pad


def kv(k, v, ksize=16, vsize=17, kcolor=MUTED, vcolor=TXT, kw=2.2):
    """key: value row; value in monospace."""
    a = T(k, ksize, kcolor, BOLD)
    b = HX(v, vsize, vcolor, BOLD)
    g = VGroup(a, b)
    b.next_to(a, RIGHT, buff=0.2)
    b.set_x(a.get_left()[0] + kw + b.width / 2)
    return g


def pa_icon(w=2.15, h=1.55, label="Protokol analizörü"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.82, height=h * 0.56, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.1)
    rows = VGroup(*[HX(s, 10, c) for s, c in (("C5E51840 FD59BB49", GOLD), ("PON-ID 12345673", ACC), ("PLOAM 0x17 ·3FF", TXT))]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
    fit(rows, scr.width - 0.12)
    if rows.height > scr.height - 0.08:
        rows.scale_to_fit_height(scr.height - 0.08)
    rows.move_to(scr)
    leds = VGroup(*[Dot(radius=0.025, color=c) for c in (GOOD, ACC, "#64748B")]).arrange(RIGHT, buff=0.06)
    leds.move_to(body).shift(DOWN * h * 0.33 + LEFT * w * 0.3)
    ports = VGroup(*[Square(0.09, stroke_color="#94A3B8", stroke_width=1.5) for _ in range(2)]).arrange(RIGHT, buff=0.08).move_to(body).shift(DOWN * h * 0.33 + RIGHT * w * 0.3)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, rows, leds, ports, lab)


def emu_icon(w=2.15, h=1.55, label="OLT emülatörü"):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.82, height=h * 0.56, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.1)
    rows = VGroup(*[HX(s, 10, c) for s, c in (("▶ Assign_ONU-ID", GOLD), ("▶ SN grant 1021", ACC), ("▶ BWmap …", TXT))]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
    fit(rows, scr.width - 0.12)
    if rows.height > scr.height - 0.08:
        rows.scale_to_fit_height(scr.height - 0.08)
    rows.move_to(scr)
    keys = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.16, height=0.1, stroke_color="#94A3B8", stroke_width=1.2) for _ in range(4)]).arrange(RIGHT, buff=0.06)
    keys.move_to(body).shift(DOWN * h * 0.33)
    lab = T(label, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, rows, keys, lab)


def onu_box(label="ONU", color=ONUC, w=1.2, h=0.6, size=17, sub=None):
    return sbox(label, sub, color, w, h, size, 14)


class Act11(Act5):
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

    def note11(self, bid, lines, badge="not", h=None, heading=None):
        """Engineer note: lines = [(num, title, body, cue_substring)]."""
        self.beat(bid)
        self.clear()
        self.set_badge(badge)
        k = len(lines)
        h = h or (2.0 if k <= 2 else 1.62)
        cards = VGroup(*[self.ncard(n, t, b, h=h) for n, t, b, _ in lines]).arrange(DOWN, buff=0.4 if k <= 2 else 0.28).move_to(DOWN * 0.35)
        if heading:
            hd = self.heading(heading)
            self.play(FadeIn(hd, shift=RIGHT * 0.2), run_time=0.4)
        for c, (_, _, _, sub) in zip(cards, lines):
            self.at(self.cue(sub, 0.5))
            self.play(FadeIn(c, shift=UP * 0.25), run_time=0.7)
        self.end(pad=0.15)
        return cards

    def chip_at(self, chip, h=None):
        """Place a season chip at the right end of the heading row."""
        y = h.get_y() if h is not None else self.heading("X").get_y()
        return chip.to_edge(RIGHT, buff=0.45).set_y(y)
