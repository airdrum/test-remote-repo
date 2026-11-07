"""S2·B5 (ep15) shared helpers — 'Yönetim Kanalları': PLOAM channel and messages, MIC, OMCC (G.989.3 §11, §6.1.4, §15.3,
§15.6–§15.8, Ek IV.8–IV.12).

Builds on the season-2 blocks chained through ep14_common → ep13_common → ep12_common → ep11_common (bit-proportional
`fields`, `strip`, `seg`, `octets`, `frame_axis`, `queue`, analyzer panels, sequence-chart helpers, S1/S2 chips, `mtable`,
`pmd_head`, `cue_n`, `Act14`); only the episode names, the PLOAM colours, the message catalogue and a few small pieces
are added here."""
from ep14_common import *

K15 = 5
EP15 = SERIES["season2"]["episodes"][K15 - 1]


def _pt(p):
    t = json.loads((ROOT / f"script/ep15_{p}.json").read_text(encoding="utf-8"))["title"]
    return t.split(" — ", 1)[1] if " — " in t else t


_S = f"SEZON 2 · BÖLÜM {K15}"
H15 = {1: f"{_S} · PERDE 1 — {_pt('p1')}", 2: f"{_S} · PERDE 2 — {_pt('p2')}",
       3: f"{_S} · PERDE 3 — {_pt('p3')}", 4: f"{_S} · PERDE 4 — {_pt('p4')}",
       "L": f"{_S} · LABORATUVARDA — {_pt('lab')}", "E": f"{_S} · KAPANIŞ"}


def M15(p):
    return f"build/ep15/{p}/audio_proc/manifest.json"


M = M15

# PLOAM message fields (Table 11-1) · broadcast / unicast · default (public) key / ONU-specific key
OIDC, TYC, SQC, CNC, MICC = ACC, GOLD, "#60A5FA", "#A78BFA", PINK
BCC, UCC = GOLD, ACC
DKC, SKC = "#FB923C", GOOD
P48 = [("ONU-ID", 2, OIDC), ("tür", 1, TYC), ("SeqNo", 1, SQC), ("içerik", 36, CNC), ("MIC", 8, MICC)]
P48_OCT = ["1–2", "3", "4", "5–40", "41–48"]
HLEND = [("BWmap boyu N", 11, BWC), ("PLOAM sayısı P", 8, PLDC), ("HEC", 13, HECC)]
USHDR = [("ONU-ID", 10, ACC), ("Ind", 9, GOLD), ("HEC", 13, HECC)]
DEFKEY = "55 55 55 55 55 55 55 55 55 55 55 55 55 55 55 55"

# message catalogue (Tables 11-2 / 11-3): (type ID, name, family)
FAM = {"prof": ACC, "kim": "#60A5FA", "dis": WARN, "key": PINK, "pm": "#C084FC", "tun": GOLD, "prot": GOOD,
       "pwr": "#FB923C", "rate": "#94A3B8", "alloc": "#38BDF8", "ack": "#CBD5E1", "rb": "#64748B"}
DS_MSGS = [(0x01, "Burst_Profile", "prof"), (0x03, "Assign_ONU-ID", "kim"), (0x04, "Ranging_Time", "kim"),
           (0x05, "Deactivate_ONU-ID", "dis"), (0x06, "Disable_Serial_Number", "dis"), (0x09, "Request_Registration", "kim"),
           (0x0A, "Assign_Alloc-ID", "alloc"), (0x0D, "Key_Control", "key"), (0x12, "Sleep_Allow", "pm"),
           (0x13, "Calibration_Request", "tun"), (0x14, "Adjust_Tx_Wavelength", "tun"), (0x15, "Tuning_Control", "tun"),
           (0x17, "System_Profile", "prof"), (0x18, "Channel_Profile", "prof"), (0x19, "Protection_Control", "prot"),
           (0x1A, "Change_Power_Level", "pwr"), (0x1B, "Power_Consumption_Inquire", "pm"), (0x1C, "Rate_Control", "rate"),
           (0x1D, "Reboot_ONU", "rb"), (0x1E, "Collision_Feedback", "alloc")]
US_MSGS = [(0x01, "Serial_Number_ONU", "kim"), (0x02, "Registration", "kim"), (0x05, "Key_Report", "key"),
           (0x09, "Acknowledgement", "ack"), (0x10, "Sleep_Request", "pm"), (0x1A, "Tuning_Response", "tun"),
           (0x1B, "Power_Consumption_Report", "pm"), (0x1C, "Rate_Response", "rate")]
PWC = FAM["pwr"]
REUSED = (0x01, 0x05, 0x09, 0x1A, 0x1B, 0x1C)
# Acknowledgement completion codes (Table 11-28)
CCODES = [("0x00", "OK"), ("0x01", "gönderecek mesaj yok"), ("0x02", "meşgul · cevap hazırlanıyor"),
          ("0x03", "bilinmeyen mesaj türü"), ("0x04", "parametre hatası"), ("0x05", "işleme hatası")]


def p48(w=12.4, h=0.6, size=17, octs=True, wl=True, osize=14):
    """The 48-byte PLOAM message (Table 11-1), widths proportional to bytes, the byte count written in each label.
    Narrow header cells get their labels above (ONU-ID left, tür one tier up, SeqNo right) with leader lines.
    Each cell = VGroup(rect, label[, octet range])."""
    x = -w / 2
    cells = VGroup()
    for i, (lab, n, c) in enumerate(P48):
        cw = w * n / 48
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.22).move_to([x + cw / 2, 0, 0])
        x += cw
        s = f"{lab} · {n} B" if wl else lab
        t = T(s, size, TXT, BOLD)
        if t.width <= cw - 0.12:
            lb = t.move_to(r)
        else:
            t = T(s, 15, c, BOLD)
            y = h / 2 + 0.1 + t.height / 2 + (0.36 if i == 1 else 0)
            if i == 0:
                t.move_to([r.get_right()[0] - t.width / 2 + 0.02, y, 0])
            elif i == 2:
                t.move_to([r.get_left()[0] + t.width / 2 - 0.02, y, 0])
            else:
                t.move_to([r.get_x(), y, 0])
            lb = VGroup(t, Line([r.get_x(), h / 2, 0], [r.get_x(), t.get_bottom()[1] - 0.03, 0], color=c, stroke_width=1.2))
        cell = VGroup(r, lb)
        if octs:
            cell.add(T(P48_OCT[i], osize, MUTED, BOLD).next_to(r, DOWN, buff=0.08))
        cells.add(cell)
    return cells


def bbar(spec, w, h=0.6, size=17, below=None, place=None, unit=" B", osize=14, op=0.22):
    """Byte-proportional bar: spec = [(name, n, color)]. Labels '<name> · <n><unit>' inside when they fit, else outside above
    as given by place = {index: (tier, 'l'|'c'|'r')} (default tier 0, centred) with a leader line. below = strings under cells.
    Each cell = VGroup(rect, label[, below])."""
    tot = sum(n for _, n, _ in spec)
    place = place or {}
    x = -w / 2
    cells = VGroup()
    for i, (lab, n, c) in enumerate(spec):
        cw = w * n / tot
        r = Rectangle(width=cw, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=op).move_to([x + cw / 2, 0, 0])
        x += cw
        s_ = f"{lab} · {n}{unit}" if unit is not None else lab
        t = T(s_, size, TXT, BOLD)
        t2 = T(lab, size, TXT, BOLD)
        bl = below[i] if below else None
        if t.width <= cw - 0.12:
            lb = t.move_to(r)
        elif t2.width <= cw - 0.1:
            lb = t2.move_to(r)
            if bl is not None and unit is not None and T(f"{bl} · {n}{unit}", osize, MUTED, BOLD).width <= cw - 0.12:
                bl = f"{bl} · {n}{unit}"
        else:
            t = T(s_, 15, c, BOLD)
            tier, al = place.get(i, (0, "c"))
            y = h / 2 + 0.1 + t.height / 2 + 0.36 * tier
            if al == "r":
                t.move_to([r.get_right()[0] - t.width / 2 + 0.02, y, 0])
            elif al == "l":
                t.move_to([r.get_left()[0] + t.width / 2 - 0.02, y, 0])
            else:
                t.move_to([r.get_x(), y, 0])
            lb = VGroup(t, Line([r.get_x(), h / 2, 0], [r.get_x(), t.get_bottom()[1] - 0.03, 0], color=c, stroke_width=1.2))
        cell = VGroup(r, lb)
        if bl is not None:
            cell.add(T(bl, osize, MUTED, BOLD).next_to(r, DOWN, buff=0.08))
        cells.add(cell)
    return cells


def bar_to(g, x, y):
    """Move a p48/fields-style group so that its row of cell rectangles (not the outside labels) is centred at (x, y)."""
    r = VGroup(*[c[0] for c in g])
    g.shift(np.array([x, y, 0]) - r.get_center())
    return g


def mtile(code, name, fam, w=3.5, h=0.36, size=15, arrow_=None):
    """Catalogue tile: type ID (mono) + message name, coloured by family."""
    c = FAM[fam]
    r = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.13)
    hx = HX(f"0x{code:02X}", size, c, BOLD)
    hx.move_to(r.get_left() + RIGHT * (0.12 + hx.width / 2))
    nm = tf(name, size, TXT, SEMIBOLD, w=w - hx.width - 0.4)
    nm.next_to(hx, RIGHT, buff=0.16)
    return VGroup(r, hx, nm)


def catalog(xs=(-4.55, -0.85, 3.85), y0=1.55, dy=0.41, w=3.55, size=15):
    """Returns (ds, us, heads): 20 downstream tiles in two columns, 8 upstream tiles in one, column heads."""
    ds = VGroup(*[mtile(c, n, f, w, 0.36, size) for c, n, f in DS_MSGS])
    us = VGroup(*[mtile(c, n, f, w, 0.36, size) for c, n, f in US_MSGS])
    for i, t in enumerate(ds):
        t.move_to([xs[i // 10], y0 - dy * (i % 10), 0])
    for i, t in enumerate(us):
        t.move_to([xs[2], y0 - dy * i, 0])
    hd = T("↓ aşağı yön · 20 tür", 18, TXT, BOLD).move_to([(xs[0] + xs[1]) / 2, y0 + 0.5, 0])
    hu = T("↑ yukarı yön · 8 tür", 18, TXT, BOLD).move_to([xs[2], y0 + 0.5, 0])
    return ds, us, VGroup(hd, hu)


def hexrow(s, size=17, color=TXT, per=None, buff=0.14):
    """'00 13 0a …' → row(s) of monospace byte groups (VGroup of rows, each a VGroup of bytes)."""
    bs = s.split()
    per = per or len(bs)
    rows = VGroup()
    for k in range(0, len(bs), per):
        rows.add(VGroup(*[HX(b, size, color, BOLD) for b in bs[k:k + per]]).arrange(RIGHT, buff=buff))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)


def keychip(default=True, size=15, text=None):
    """Lock + key name: orange = default (0x55)16, green = ONU-specific."""
    c = DKC if default else SKC
    s = text or ("varsayılan · 0x55 × 16" if default else "ONU'ya özgü")
    lk = lock(c, 0.24)
    t = T(s, size, c, BOLD)
    return VGroup(lk, t).arrange(RIGHT, buff=0.12)


def inst(kind, label, w=1.9, h=1.35, l1=None, l2=None, c1=ACC):
    """Instrument tile with our own caption (lib.instrument's caption replaced)."""
    g = instr(kind, w, h)
    if l1 is not None:
        scr = g[1]
        g.submobjects[2] = VGroup(fit(T(l1, 20, c1, BOLD), scr.width - 0.15).move_to(scr))
    g.submobjects[4] = T(label, 16, TXT, SEMIBOLD).next_to(g[0], DOWN, buff=0.1)
    return g


def frame_cells(n, x0, w, y, h, color, labels=None, size=14, op=0.08, lpos=DOWN):
    """n frame cells (125 µs) from x0, each w wide; optional labels below/above. Returns (cells, labels)."""
    cells = VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=op)
                     .move_to([x0 + w * (i + 0.5), y, 0]) for i in range(n)])
    lb = VGroup()
    if labels:
        lb = VGroup(*[T(s, size, MUTED, BOLD).next_to(c, lpos, buff=0.06) for s, c in zip(labels, cells)])
    return cells, lb


def nlabels(n, start=0):
    return ["N" if k == 0 else f"N+{k}" for k in range(start, start + n)]


def mbox(text, color, w=None, h=0.36, size=15, op=0.25, mono=False):
    """Small filled message chip (a PLOAM in a partition, a grant, a reply)."""
    t = HX(text, size - 1, TXT, BOLD) if mono else T(text, size, TXT, BOLD)
    w = w or t.width + 0.24
    r = RoundedRectangle(corner_radius=0.05, width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=op)
    fit(t, w - 0.1)
    return VGroup(r, t.move_to(r))


def cmac_box(w=2.4, h=1.0, title="AES-CMAC", sub=None, color=MICC):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    parts = [T(title, 20, color, BOLD)]
    if sub:
        parts.append(T(sub, 15, MUTED, BOLD))
    t = VGroup(*parts).arrange(DOWN, buff=0.06)
    fit(t, w - 0.2)
    return VGroup(r, t.move_to(r))


def chk(s, ok=True, size=17, color=None):
    return VGroup(ok_x(ok, size + 2), T(s, size, color or TXT, BOLD)).arrange(RIGHT, buff=0.15)


class Act15(Act14):
    def card_row(self, items, y, w=None, size=17):
        """Row of tags placed centred at y (fits the frame)."""
        g = VGroup(*items).arrange(RIGHT, buff=0.2)
        fit(g, w or 12.6)
        return g.move_to([0, y, 0])
