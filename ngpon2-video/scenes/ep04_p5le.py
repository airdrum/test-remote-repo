"""B04 · Perde 5 (TC köprüsü: 125 µs çerçeve), Laboratuvarda, Kapanış."""
from ep03_common import *
from ep04_common import *

PSYNC_HEX = "0xC5E51840 FD59BB49"
DS_NM = [thz_to_nm(f) for f in (187.8, 187.7, 187.6, 187.5)]


def pm_ds(w=2.15, h=1.55):
    """Power meter tile with a downstream (L-band) display instead of the upstream example reading."""
    ins = instrument("PM", w, h)
    scr = ins[1]
    g = VGroup(T("kanal gücü", 15, ACC, BOLD), T("dBm · ↓ L bandı", 10, MUTED)).arrange(DOWN, buff=0.06).move_to(scr)
    ins.submobjects[2] = g
    return ins


def bits_row(labels, colors, w=0.75, size=22):
    cells = VGroup(*[VGroup(Square(w, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), T(s, size, c, BOLD)) for s, c in zip(labels, colors)])
    for c in cells:
        c[1].move_to(c[0])
    return cells.arrange(RIGHT, buff=0.05)


def connect(a, b, color=MUTED):
    """Two thin lines from the bottom corners of a to the top corners of b (zoom)."""
    return VGroup(Line(a.get_corner(DL), b.get_corner(UL), color=color, stroke_width=1.5), Line(a.get_corner(DR), b.get_corner(UR), color=color, stroke_width=1.5))


class E4P5A(Act4):
    HDR, MANIFEST, FIRST = H4[5], M4("p5"), True

    def construct(self):
        self.beat("f1")
        tc = self.title_card("PERDE 5", "TC köprüsü")
        self.at(self.cue("Çalışan bir OLT", 2))
        self.to_header(tc)
        self.set_badge("tc")
        h = self.show_heading("Aşağı yön PHY çerçevesi — G.989.3 §10.1.1")
        fw, x0, y = 1.7, -6.1, 1.0
        frames = VGroup()
        for i in range(7):
            fr = Rectangle(width=fw - 0.06, height=0.7, stroke_color=TW_DS, stroke_width=2, fill_color=TW_DS, fill_opacity=0.15).move_to([x0 + fw * (i + 0.5), y, 0])
            ps = Rectangle(width=0.16, height=0.7, stroke_width=0, fill_color=PSY_C, fill_opacity=0.9).align_to(fr, LEFT).set_y(y)
            frames.add(VGroup(fr, ps))
        arr = Arrow([x0, y + 0.65, 0], [x0 + fw * 7, y + 0.65, 0], buff=0, color=TW_DS, stroke_width=2.5, max_tip_length_to_length_ratio=0.03)
        arrt = T("OLT CT → sürekli", 16, TW_DS, BOLD).next_to(arr, UP, buff=0.06).align_to(arr, LEFT)
        br = BraceBetweenPoints(frames[2].get_corner(DL), frames[2].get_corner(DR), DOWN, color=GOLD, buff=0.06)
        brt = T("125 µs", 20, GOLD, BOLD).next_to(br, DOWN, buff=0.06)
        c10 = card("10G ↓", "155 520 bayt / çerçeve", None, TW_DS, w=5.2, h=1.35, tsize=24, bsize=24).move_to([-3.0, -1.75, 0])
        c25 = card("2,5G ↓", "38 880 bayt / çerçeve", None, GOLD, w=5.2, h=1.35, tsize=24, bsize=24).move_to([3.0, -1.75, 0])
        self.at(self.cue("aşağı yönde sürekli", 3.5))
        self.play(GrowArrow(arr), FadeIn(arrt), LaggedStart(*[FadeIn(f, shift=LEFT * 0.3) for f in frames], lag_ratio=0.12), self.set_src("G.989.3 §10.1.1"), run_time=1.3)
        self.at(self.cue("Her yüz yirmi beş", 6))
        self.play(FadeIn(br), FadeIn(brt), run_time=0.5)
        self.at(self.cue("on gigabitte", 9))
        self.play(FadeIn(c10, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("iki buçuk gigabitte", 13))
        self.play(FadeIn(c25, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f1a")
        self.clear(h)
        h = self.show_heading("Çerçevenin yapısı", h)
        fb = seg_bar([("PSBd · 24 B", 2.2, PSY_C, 0.85), ("PHY çerçeve yükü", 10.2, TW_DS, 0.25)], 1.6, -6.2, h=0.7, size=19)
        z = seg_bar([("PSync · 8 B", 2.4, PSY_C, 0.85), ("SFC yapısı · 8 B", 2.4, SFC_C, 0.8), ("OC yapısı · 8 B", 2.4, OC_C, 0.8)], 0.0, -6.2, h=0.6, size=17)
        zl = connect(fb[0][0], VGroup(z[0][0], z[2][0]))
        pipe = VGroup(box(2.5, 0.65, "FS çerçevesi", MUTED, 17), box(2.8, 0.65, "FEC (isteğe bağlı)", FEC_C, 17), box(2.4, 0.65, "karıştırıcı", ACC, 17), box(2.3, 0.65, "PHY yükü", TW_DS, 17)).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.9)
        pa = VGroup(*[Arrow(pipe[i].get_right(), pipe[i + 1].get_left(), buff=0.04, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        self.at(self.cue("yirmi dört baytlık", 0.8))
        self.play(GrowFromEdge(fb[0], LEFT), run_time=0.5)
        self.at(self.cue("Ardından yük", 4))
        self.play(GrowFromEdge(fb[1], LEFT), run_time=0.6)
        self.at(self.cue("çerçeve yapısı önce", 6))
        self.play(FadeIn(pipe[0]), GrowArrow(pa[0]), FadeIn(pipe[1]), run_time=0.7)
        self.at(self.cue("sonra karıştırıcıdan", 9))
        self.play(GrowArrow(pa[1]), FadeIn(pipe[2]), GrowArrow(pa[2]), FadeIn(pipe[3]), run_time=0.7)
        self.at(self.cue("PSBd'nin üç", 12))
        self.play(Create(zl), LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in z], lag_ratio=0.25), run_time=1.0)
        self.end(pad=0.05)

        self.beat("f1b")
        self.clear(h)
        h = self.show_heading("OLT hep gönderir", h)
        y = 0.9
        frames = VGroup()
        kinds = ["d", "d", "i", "i", "i", "d", "i"]
        for i, k in enumerate(kinds):
            xc = -6.1 + 1.7 * (i + 0.5)
            fr = Rectangle(width=1.64, height=0.8, stroke_color=TW_DS, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([xc, y, 0])
            ps = Rectangle(width=0.16, height=0.8, stroke_width=0, fill_color=PSY_C, fill_opacity=0.9).align_to(fr, LEFT).set_y(y)
            body = Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=TW_DS if k == "d" else MUTED, fill_opacity=0.8 if k == "d" else 0.35).move_to([xc + 0.07, y, 0])
            frames.add(VGroup(fr, ps, body))
        lg = VGroup(T("■ trafik", 17, TW_DS, BOLD), T("■ boş XGEM çerçeveleri", 17, MUTED, BOLD)).arrange(RIGHT, buff=0.5).next_to(frames, DOWN, buff=0.25)
        onu = VGroup(box(1.5, 0.8, "ONU", "#94A3B8", 20), VGroup(T("senkron", 18, GOOD, BOLD), T("saat çıkarımı", 18, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)).arrange(RIGHT, buff=0.3).move_to([-2.6, -1.35, 0])
        sil = pill("↓ sessizlik = hata durumu", WARN, 24).move_to([3.4, -1.35, 0])
        self.play(LaggedStart(*[FadeIn(f[0:2]) for f in frames], lag_ratio=0.1), *[FadeIn(f[2]) for f, k in zip(frames, kinds) if k == "d"], run_time=0.9)
        self.at(self.cue("Trafik olmadığında", 3))
        self.play(*[FadeIn(f[2], scale=0.8) for f, k in zip(frames, kinds) if k == "i"], FadeIn(lg), run_time=0.7)
        self.at(self.cue("ONU'ların senkronda", 7))
        self.play(FadeIn(onu, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("aşağı yönde sessizlik", 12))
        self.play(FadeIn(sil, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f2")
        self.clear(h)
        h = self.show_heading("PSync ve süper çerçeve sayacı (SFC)", h)
        ps = VGroup(T("PSync · 64 bit · sabit", 22, PSY_C, BOLD), T(PSYNC_HEX, 46, TXT, BOLD)).arrange(DOWN, buff=0.18).move_to(UP * 1.35)
        psb = SurroundingRectangle(ps[1], color=PSY_C, buff=0.18, corner_radius=0.1)
        same = VGroup(pill("her iki hızda aynı", PSY_C, 19), pill("XG-PON1 ile aynı desen", MUTED, 19)).arrange(RIGHT, buff=0.3).move_to(UP * 0.05)
        cnt = VGroup(T("SFC · 51 bit", 22, SFC_C, BOLD), T("n", 36, TXT, BOLD)).arrange(RIGHT, buff=0.5).move_to([-3.0, -1.45, 0])
        inc = T("her çerçevede +1", 18, MUTED).next_to(cnt, DOWN, buff=0.15)
        wrap = VGroup(T("2⁵¹ × 125 µs", 24, TXT, BOLD), T("≈ 9 000 yıl", 32, GOLD, BOLD)).arrange(DOWN, buff=0.12).move_to([3.4, -1.55, 0])
        self.at(self.cue("onaltılık", 3))
        self.play(FadeIn(ps), Create(psb), self.set_src("G.989.3 §10.1.1.1"), run_time=0.8)
        self.at(self.cue("Her iki hızda", 6))
        self.play(FadeIn(same[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("ve XG-PON1", 8))
        self.play(FadeIn(same[1], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Süper çerçeve sayacı", 10))
        self.play(FadeIn(cnt), FadeIn(inc), run_time=0.5)
        for s in ("n + 1", "n + 2", "n + 3"):
            new = T(s, 36, TXT, BOLD).move_to(cnt[1], aligned_edge=LEFT)
            self.play(Transform(cnt[1], new), run_time=0.35)
        self.at(self.cue("Bu hızla", 15))
        self.play(FadeIn(wrap, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("f2a")
        self.clear(h)
        h = self.show_heading("SFC yapısı: 51 + 13 bit", h)
        sb = seg_bar([("süper çerçeve sayacı · 51 bit", 51 * 0.2, SFC_C, 0.75), ("HEC · 13 bit", 13 * 0.2, GOLD, 0.85)], 1.5, -6.4, h=0.7, size=19)
        hec = VGroup(T("HEC = BCH(63,12) + 1 eşlik biti", 24, GOLD, BOLD), T("2 hata düzeltir · 3 hata algılar", 22, TXT),
                     T("→ sayaç tek bit hatasıyla kaybolmaz", 20, GOOD, BOLD)).arrange(DOWN, aligned_edge=RIGHT, buff=0.14).move_to([3.0, 0.15, 0])
        blk = seg_bar([("PSync", 2.0, PSY_C, 0.85), ("SFC", 2.0, SFC_C, 0.8), ("OC", 2.0, OC_C, 0.8)], -1.65, -6.2, h=0.6, size=18)
        xb = BraceBetweenPoints(blk[1][0].get_corner(DL), blk[2][0].get_corner(DR), DOWN, color=WARN, buff=0.06)
        xo = VGroup(xb, T("⊕ 0x0F0F0F0F 0F0F0F0F", 19, WARN, BOLD).next_to(xb, DOWN, buff=0.06))
        xt = T("HEC hesaplandıktan sonra XOR", 18, WARN, BOLD).next_to(blk, RIGHT, buff=0.4)
        pt = T("PSync: olduğu gibi", 17, PSY_C, BOLD).next_to(blk[0], UP, buff=0.12)
        self.play(GrowFromEdge(sb[0], LEFT), GrowFromEdge(sb[1], LEFT), self.set_src("G.989.3 §10.1.1.1.2 · §10.1.1.2 · Ek A.1"), run_time=0.8)
        self.at(self.cue("BCH altmış", 2.5))
        self.play(FadeIn(hec[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("İki hatayı", 6))
        self.play(FadeIn(hec[1]), run_time=0.4)
        self.at(self.cue("böylece sayaç", 9))
        self.play(FadeIn(hec[2]), run_time=0.4)
        self.at(self.cue("Süper çerçeve sayacı ve", 12))
        self.play(FadeIn(blk), run_time=0.5)
        self.at(self.cue("HEC hesaplandıktan", 15))
        self.play(FadeIn(xo), FadeIn(xt), run_time=0.6)
        self.at(self.cue("PSync ise", 19))
        self.play(FadeIn(pt), run_time=0.4)
        self.end(pad=0.05)

        self.beat("f2b")
        self.clear(h)
        h = self.show_heading("SFC'nin üç işi", h)
        cs = VGroup(card("1 · Senkron doğrulaması", "alıcı: geçerli HEC + beklenen sayaç (bir öncekinin bir fazlası)", None, SFC_C, w=11.6, h=1.1, tsize=22, bsize=19),
                    card("2 · Karıştırıcı", "ön yükleme deseni → her çerçevede farklı dizi", None, ACC, w=11.6, h=1.1, tsize=22, bsize=19),
                    card("3 · Dalga boyu değişimi", "Tuning_Control: SFC değeriyle hedef çerçeve\nONU: kendi SFC'sinin en düşük 16 biti = hedef → ayar başlar", None, GOLD, w=11.6, h=1.45, tsize=22, bsize=19)).arrange(DOWN, buff=0.28).move_to(DOWN * 0.35)
        for i, key in enumerate(["Alıcı onu", "Karıştırıcı onu", "Ve dalga boyu"]):
            self.at(self.cue(key, 2 + 5 * i))
            self.play(FadeIn(cs[i], shift=UP * 0.12), run_time=0.5)
        self.at(self.cue("ve ONU kendi", 18))
        self.play(Indicate(cs[2][2], color=GOLD, scale_factor=1.03), run_time=0.8)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p5A")


OC_FIELDS = [("PIT", 8, OC_C), ("PON-ID", 32, ACC), ("R", 1, MUTED), ("C", 1, GOLD), ("TOL", 9, GOOD), ("HEC", 13, WARN)]


def oc_bar(y=1.55, k=0.2, x0=-6.4):
    g = seg_bar([(n if b > 2 else "", b * k, c, 0.6) for n, b, c in OC_FIELDS], y, x0, h=0.62, size=18)
    for i in (2, 3):
        g[i].add(T(OC_FIELDS[i][0], 15, OC_FIELDS[i][2], BOLD).next_to(g[i][0], UP, buff=0.06))
    return g


class E4P5B(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[5], M4("p5"), "tc"

    def construct(self):
        self.beat("f3")
        h = self.show_heading("İşletim kontrol (OC) yapısı — 64 bit")
        ob = oc_bar()
        bl = T("51 bit gövde + 13 bit HEC", 16, MUTED).next_to(ob, DOWN, buff=0.1).align_to(ob, RIGHT)
        pit = bits_row(["RE", "O", "O", "O", "F", "P", "L", "L"], [GOLD, ACC, ACC, ACC, PINK, OC_C, TW_US, TW_US], w=0.72, size=19).move_to([-3.4, 0.05, 0])
        pz = connect(ob[0][0], pit)
        pl = VGroup(T("menzil\nuzatıcı", 14, GOLD, line_spacing=0.8).next_to(pit[0], DOWN, buff=0.1), T("ODN sınıfı (3 bit)", 14, ACC).next_to(pit[1:4], DOWN, buff=0.1),
                    T("↓ FEC", 14, PINK).next_to(pit[4], DOWN, buff=0.1), T("TC\nsürümü", 14, OC_C, line_spacing=0.8).next_to(pit[5], DOWN, buff=0.1),
                    T("bağlantı tipi", 14, TW_US).next_to(pit[6:8], DOWN, buff=0.1))
        pid = seg_bar([("yönetim etiketi · 28 bit", 28 * 0.3, ACC, 0.45), ("DWLCH ID · 4", 4 * 0.3, TW_DS, 0.85)], -2.25, -4.8, h=0.6, size=17)
        idt = T("PON-ID · 32 bit", 18, ACC, BOLD).next_to(pid, UP, buff=0.12).align_to(pid, LEFT)
        self.play(LaggedStart(*[FadeIn(s) for s in ob], lag_ratio=0.1), FadeIn(bl), self.set_src("G.989.3 §10.1.1.1.3"), run_time=1.0)
        self.at(self.cue("Önce sekiz bitlik", 2.5))
        self.play(Create(pz), FadeIn(pit[0:1]), run_time=0.5)
        for keys, sl, li in (("bir menzil", slice(0, 1), 0), ("üç bitlik ODN", slice(1, 4), 1), ("aşağı yön FEC", slice(4, 5), 2)):
            self.at(self.cue(keys, 4))
            self.play(FadeIn(pit[sl]), FadeIn(pl[li]), run_time=0.4)
        self.at(self.cue("TC sürümü bayrağı ve", 10))
        self.play(FadeIn(pit[5:]), FadeIn(pl[3:]), run_time=0.5)
        self.at(self.cue("Ardından otuz iki", 14))
        self.play(Indicate(ob[1], color=ACC, scale_factor=1.05), FadeIn(idt), GrowFromEdge(pid[0], LEFT), run_time=0.8)
        self.at(self.cue("dört bitlik aşağı", 18))
        self.play(GrowFromEdge(pid[1], LEFT), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f3c")
        self.play(*[FadeOut(m) for m in (pz, pl, pid, idt, bl)], pit.animate.scale(0.9).move_to([-3.4, 0.35, 0]), run_time=0.5)
        c1 = card("P · TC sürümü", "1 → G.989.3 TC\n0 → G.987.3 TC", None, OC_C, w=3.9, h=1.8, tsize=22, bsize=20)
        c2 = card("bağlantı tipi · 2 bit", "10 → yalnız A tipi\n01 → yalnız B tipi\n11 → ikisi birden", None, TW_US, w=3.9, h=1.8, tsize=22, bsize=20)
        c3 = card("RE · menzil uzatıcı", "TOL kimin?\n0 → OLT CT\n1 → menzil uzatıcı", None, GOLD, w=3.9, h=1.8, tsize=22, bsize=20)
        cs = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.75)
        for i, key, idx in ((0, "TC sürümü bayrağı bir", 5), (1, "Bağlantı tipi", 6), (2, "Menzil uzatıcı", 0)):
            self.at(self.cue(key, 2 + 7 * i))
            sel = pit[idx:idx + 2] if i == 1 else pit[idx]
            self.play(FadeIn(cs[i], shift=UP * 0.12), Indicate(sel, color=WHITE, scale_factor=1.1), run_time=0.8)
        self.end(pad=0.05)

        self.beat("f3a")
        self.clear(h, *ob)
        h = self.show_heading("TOL: iletim optik düzeyi", h)
        self.play(*[ob[i].animate.set_opacity(0.25) for i in (0, 1, 2, 5)], run_time=0.4)
        tf = VGroup(T("9 bit · 0,1 dB adım · referans −30 dBm", 22, GOOD, BOLD), T("P = −30 dBm + 0,1 dB × TOL", 26, TXT, BOLD)).arrange(DOWN, buff=0.14).move_to(UP * 0.55)
        X = lambda d: -5.0 + (d + 30) * (10.0 / 51)
        yr = -1.15
        rule = VGroup(Line([X(-30), yr, 0], [X(21), yr, 0], color=MUTED, stroke_width=2.5),
                      *[Line([X(d), yr - 0.07, 0], [X(d), yr + 0.07, 0], color=MUTED, stroke_width=1.5) for d in range(-30, 22, 10)])

        def mark(d, top, bot, col):
            return VGroup(Dot([X(d), yr, 0], radius=0.08, color=col), T(top, 19, col, BOLD).next_to([X(d), yr, 0], UP, buff=0.18),
                          T(bot, 18, TXT).next_to([X(d), yr, 0], DOWN, buff=0.18))
        m0, m3, m5 = mark(-30, "0", "−30 dBm", GOOD), mark(0, "300 (0x12C)", "0 dBm", GOOD), mark(21, "510 (0x1FE)", "+21 dBm", GOOD)
        ns = pill("511 (0x1FF) → desteklenmiyor", MUTED, 18).move_to([-3.0, -2.6, 0])
        cb = pill("C biti: 0 → S/R-CG · 1 → S/R-CP", GOLD, 18).move_to([3.0, -2.6, 0])
        self.at(self.cue("Dokuz bitlik", 4))
        self.play(FadeIn(tf[0], shift=UP * 0.1), self.set_src("G.989.3 §10.1.1.1.3"), run_time=0.5)
        self.at(self.cue("ve eksi otuz", 7))
        self.play(FadeIn(tf[1], shift=UP * 0.1), Create(rule), run_time=0.7)
        self.at(self.cue("Sıfır değeri", 13))
        self.play(FadeIn(m0), run_time=0.4)
        self.at(self.cue("üç yüz değeri", 16))
        self.play(FadeIn(m3), run_time=0.4)
        self.at(self.cue("beş yüz on", 18))
        self.play(FadeIn(m5), run_time=0.4)
        self.at(self.cue("en büyük değer", 21))
        self.play(FadeIn(ns, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Bir bit de", 25))
        self.play(FadeIn(cb, shift=UP * 0.1), ob[3].animate.set_opacity(1), Indicate(ob[3], color=GOLD), run_time=0.8)
        self.end(pad=0.05)

        self.beat("f3b")
        self.clear(h)
        h = self.show_heading("TOL ne işe yarar?", h)
        q = T("ONU bu değerle ne yapmalı? — standart söylemez", 22, MUTED).move_to(UP * 1.75)
        yb = 0.0
        win = Rectangle(width=8.0, height=0.7, stroke_color=TW_DS, stroke_width=2, fill_color=TW_DS, fill_opacity=0.15).move_to([0, yb, 0])
        ends = VGroup(T("P_min", 18, GOOD, BOLD).next_to(win, LEFT, buff=0.15), T("P_maks", 18, WARN, BOLD).next_to(win, RIGHT, buff=0.15))
        br = BraceBetweenPoints(win.get_corner(DL), win.get_corner(DR), DOWN, color=TW_DS)
        brt = T("4 dB pencere", 18, TW_DS, BOLD).next_to(br, DOWN, buff=0.06)
        mk = VGroup(Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1).scale(0.14).rotate(PI), T("TOL", 18, GOLD, BOLD)).arrange(UP, buff=0.06).move_to([-1.5, yb + 0.65, 0])
        cap = T("OLT pencerenin neresinde çalıştığını her çerçevede yayınlar", 21, GOLD, BOLD).move_to(DOWN * 1.55)
        acc = pill("Ek II örnekleri: OLT verici gücü izleme doğruluğu ± 2 dB", ACC, 19).move_to(DOWN * 2.55)
        self.play(FadeIn(q), run_time=0.5)
        self.at(self.cue("Ama bilgi", 4))
        self.play(FadeIn(win), FadeIn(ends), FadeIn(br), FadeIn(brt), FadeIn(mk, shift=DOWN * 0.1), run_time=0.7)
        self.at(self.cue("dört desibellik", 7))
        self.play(mk.animate.shift(RIGHT * 2.6), FadeIn(cap), run_time=0.9)
        self.play(mk.animate.shift(LEFT * 1.1), run_time=0.6)
        self.at(self.cue("İkinci ekteki", 12))
        self.play(FadeIn(acc, shift=UP * 0.1), self.set_src("G.989.2 Ek II, Tablo II.1"), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p5B")


class E4P5C(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[5], M4("p5"), "tc"

    def construct(self):
        self.beat("f4")
        h = self.show_heading("Aşağı yön FEC — 10G: RS(248,216)")
        ps = VGroup(pill("destek zorunlu", GOOD, 19), pill("statik: açık / kapalı", GOLD, 19), pill("bütün ONU'lar için aynı", ACC, 19)).arrange(RIGHT, buff=0.3).move_to(UP * 1.95)
        y = 0.75
        psb = Rectangle(width=0.5, height=0.65, stroke_width=0, fill_color=PSY_C, fill_opacity=0.9).move_to([-6.15, y, 0])
        cws = VGroup(*[Rectangle(width=0.9, height=0.65, stroke_color=FEC_C, stroke_width=1.5, fill_color=FEC_C, fill_opacity=0.18).move_to([-5.4 + 0.94 * i, y, 0]) for i in range(12)])
        dots = T("…", 28, FEC_C, BOLD).move_to([-5.4 + 0.94 * 12.2, y, 0])
        cwl = T("627 kod sözcüğü / çerçeve", 18, FEC_C, BOLD).next_to(cws, UP, buff=0.12).align_to(cws, LEFT)
        cw = seg_bar([("216 veri baytı", 216 * 0.042, TW_DS, 0.6), ("32 eşlik", 32 * 0.042, FEC_C, 0.85)], -0.85, -5.6, h=0.6, size=18)
        cz = connect(cws[2], cw)
        eq = T("627 × 248 = 155 496 bayt = yük", 28, TXT, BOLD).move_to(DOWN * 2.1)
        eq2 = T("(155 520 − 24 bayt PSBd)", 18, MUTED).next_to(eq, DOWN, buff=0.1)
        self.play(FadeIn(ps[0], shift=UP * 0.1), self.set_src("G.989.3 §10.1.3"), run_time=0.5)
        self.at(self.cue("ama statik", 2.5))
        self.play(FadeIn(ps[1], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bütün ONU'lar", 5))
        self.play(FadeIn(ps[2], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("On gigabitte RS", 7))
        self.play(FadeIn(psb), LaggedStart(*[FadeIn(c) for c in cws], lag_ratio=0.06), FadeIn(dots), run_time=0.9)
        self.at(self.cue("her çerçevede altı", 11))
        self.play(FadeIn(cwl), run_time=0.4)
        self.at(self.cue("her biri iki yüz", 14))
        self.play(Create(cz), GrowFromEdge(cw[0], LEFT), run_time=0.6)
        self.play(GrowFromEdge(cw[1], LEFT), run_time=0.4)
        self.at(self.cue("Altı yüz yirmi yedi çarpı", 19))
        self.play(FadeIn(eq, shift=UP * 0.1), FadeIn(eq2), run_time=0.6)
        self.end(pad=0.05)

        self.beat("f4a")
        self.clear(h)
        h = self.show_heading("2,5G: RS(248,232)", h)
        y = 1.2
        psb = Rectangle(width=0.5, height=0.65, stroke_width=0, fill_color=PSY_C, fill_opacity=0.9).move_to([-6.15, y, 0])
        cws = VGroup(*[Rectangle(width=0.9, height=0.65, stroke_color=FEC_C, stroke_width=1.5, fill_color=FEC_C, fill_opacity=0.18).move_to([-5.4 + 0.94 * i, y, 0]) for i in range(8)])
        dots = T("…", 28, FEC_C, BOLD).move_to([-5.4 + 0.94 * 8.1, y, 0])
        last = Rectangle(width=0.61, height=0.65, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.3).move_to([-5.4 + 0.94 * 9 + 0.1, y, 0])
        l1 = T("156 × 248 B", 18, FEC_C, BOLD).next_to(cws, UP, buff=0.12).align_to(cws, LEFT)
        l2 = T("+ 168 B (kısa)", 18, WARN, BOLD).next_to(last, UP, buff=0.12)
        k = 0.03
        lz = VGroup(seg_bar([("152 veri", 152 * k, TW_DS, 0.6)], -0.75, -5.6, h=0.6, size=17)[0],
                    DashedVMobject(Rectangle(width=80 * k, height=0.6, color=MUTED, stroke_width=2), num_dashes=30).move_to([-5.6 + 152 * k + 40 * k, -0.75, 0]),
                    seg_bar([("16", 16 * k, FEC_C, 0.85)], -0.75, -5.6 + 232 * k, h=0.6, size=15)[0])
        lzt = T("80 sıfır bayt", 16, MUTED, BOLD).move_to(lz[1])
        lzn = T("kodlamadan önce eklenir, gönderilmez", 17, MUTED).next_to(lz[1], DOWN, buff=0.15)
        lzp = T("16 eşlik", 15, FEC_C, BOLD).next_to(lz[2], UP, buff=0.08)
        cz = connect(last, VGroup(lz[0], lz[2]))
        eq = T("156 × 248 + 168 = 38 856 bayt = yük", 26, TXT, BOLD).move_to([0, -2.1, 0])
        pnote = pill("PSBd hiçbir zaman FEC'e dahil değil", PSY_C, 20).move_to(DOWN * 2.85)
        self.play(FadeIn(psb), LaggedStart(*[FadeIn(c) for c in cws], lag_ratio=0.06), FadeIn(dots), run_time=0.8)
        self.at(self.cue("yüz elli altı tam", 3))
        self.play(FadeIn(l1), run_time=0.4)
        self.at(self.cue("ve yüz altmış sekiz", 6))
        self.play(FadeIn(last), FadeIn(l2), run_time=0.5)
        self.at(self.cue("Son veri bloğu", 10))
        self.play(Create(cz), FadeIn(lz[0]), run_time=0.5)
        self.at(self.cue("kodlamadan önce seksen", 12))
        self.play(Create(lz[1]), FadeIn(lzt), FadeIn(lz[2]), FadeIn(lzp), run_time=0.7)
        self.at(self.cue("ve bu dolgu", 15))
        self.play(FadeIn(lzn), FadeIn(eq), run_time=0.5)
        self.at(self.cue("PSBd hiçbir", 17))
        self.play(FadeIn(pnote, shift=UP * 0.1), Indicate(psb, color=PSY_C), run_time=0.8)
        self.end(pad=0.05)

        self.beat("f4b")
        self.clear(h)
        h = self.show_heading("FEC'in bedeli ve kazancı", h)
        k = 0.036
        bx = -5.2
        b10 = seg_bar([("veri 216", 216 * k, TW_DS, 0.6), ("32", 32 * k, FEC_C, 0.85)], 1.6, bx, h=0.55, size=16)
        b25 = seg_bar([("veri 232", 232 * k, GOLD, 0.6), ("16", 16 * k, FEC_C, 0.85)], 0.1, bx, h=0.55, size=16)
        r10 = VGroup(T("10G", 24, TW_DS, BOLD).next_to(b10, LEFT, buff=0.3), b10)
        r25 = VGroup(T("2,5G", 24, GOLD, BOLD).next_to(b25, LEFT, buff=0.3), b25)
        t10 = VGroup(T("eşlik %12,9", 20, FEC_C, BOLD), T("135 432 veri baytı / çerçeve ≈ 8,67 Gbit/s", 18, TXT)).arrange(RIGHT, buff=0.35).next_to(b10, DOWN, buff=0.14).align_to(b10, LEFT)
        t25 = VGroup(T("eşlik %6,5", 20, FEC_C, BOLD), T("≈ 2,33 Gbit/s", 18, TXT)).arrange(RIGHT, buff=0.35).next_to(b25, DOWN, buff=0.14).align_to(b25, LEFT)
        gain = card("Kazanç (G.989.3 §6.1.3.3)", "alıcı daha yüksek hata oranında çalışabilir\n→ hassasiyet ve aşırı yük etkin olarak iyileşir", None, GOOD, w=11.0, h=1.55, tsize=22, bsize=20).move_to(DOWN * 2.2)
        self.at(self.cue("On gigabitte eşlik", 2))
        self.play(FadeIn(r10[0]), GrowFromEdge(r10[1], LEFT), FadeIn(t10[0]), run_time=0.7)
        self.at(self.cue("çerçeve başına yüz", 6))
        self.play(FadeIn(t10[1]), run_time=0.5)
        self.at(self.cue("İki buçuk gigabitte pay", 12))
        self.play(FadeIn(r25[0]), GrowFromEdge(r25[1], LEFT), FadeIn(t25[0]), run_time=0.7)
        self.at(self.cue("yaklaşık iki virgül", 15))
        self.play(FadeIn(t25[1]), run_time=0.4)
        self.at(self.cue("Standart kazancı", 18))
        self.play(FadeIn(gain, shift=UP * 0.12), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p5C")


class E4P5D(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[5], M4("p5"), "tc"

    def construct(self):
        self.beat("f5")
        h = self.show_heading("Karıştırıcı: x⁵⁸ + x³⁹ + 1")
        labs = ["1", "2", "3", "…", "39", "…", "56", "57", "58"]
        y = 1.1
        cells = VGroup(*[VGroup(Square(0.55, stroke_color=ACC if s != "…" else LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1), T(s, 16, ACC if s != "…" else MUTED, BOLD)) for s in labs])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0.07).move_to([-2.9, y, 0])
        regt = T("kaydırmalı yazmaç · 58 hücre", 17, MUTED).next_to(cells, UP, buff=0.12)
        xr = np.array([0.9, 0.1, 0])
        x1 = VGroup(Circle(radius=0.2, color=GOLD, stroke_width=2.5).move_to(xr), T("⊕", 26, GOLD, BOLD).move_to(xr))
        t39 = VMobject(color=GOLD, stroke_width=2).set_points_as_corners([cells[4].get_bottom(), [cells[4].get_x(), 0.1, 0], xr + LEFT * 0.2])
        t58 = VMobject(color=GOLD, stroke_width=2).set_points_as_corners([cells[8].get_right(), [xr[0], y, 0], xr + UP * 0.2])
        fbk = VGroup(VMobject(color=GOLD, stroke_width=2).set_points_as_corners([xr + DOWN * 0.2, [xr[0], -0.45, 0], [-6.3, -0.45, 0], [-6.3, y, 0]]),
                     Arrow([-6.3, y, 0], cells[0].get_left(), buff=0, color=GOLD, stroke_width=2, max_tip_length_to_length_ratio=0.4))
        x2c = np.array([3.4, 0.1, 0])
        x2 = VGroup(Circle(radius=0.22, color=ACC, stroke_width=2.5).move_to(x2c), T("⊕", 28, ACC, BOLD).move_to(x2c))
        ks = Arrow(xr + RIGHT * 0.2, x2c + LEFT * 0.22, buff=0, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
        dat = VGroup(T("PHY yükü", 16, TXT, BOLD).move_to(x2c + UP * 1.05), Arrow(x2c + UP * 0.85, x2c + UP * 0.22, buff=0, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3))
        out = VGroup(Arrow(x2c + RIGHT * 0.22, x2c + RIGHT * 1.6, buff=0, color=ACC, stroke_width=2.5, max_tip_length_to_length_ratio=0.2), T("hat", 17, ACC, BOLD).next_to(x2c + RIGHT * 1.6, RIGHT, buff=0.1))
        fs = T("çerçeveye senkron", 18, GOLD, BOLD).move_to([2.2, -0.75, 0])
        pre = seg_bar([("süper çerçeve sayacı · 51 bit (en anlamlı)", 51 * 0.2, SFC_C, 0.7), ("1111111", 7 * 0.2, GOOD, 0.85)], -1.75, -5.8, h=0.6, size=17)
        pret = T("ön yükleme deseni (58 bit) · PSBd'den sonraki ilk bitte", 17, MUTED).next_to(pre, UP, buff=0.1).align_to(pre, LEFT)
        res = T("→ karıştırma dizisi her çerçevede farklı", 22, GOOD, BOLD).move_to(DOWN * 2.75)
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.05), FadeIn(regt), self.set_src("G.989.3 §10.1.4.1"), run_time=0.8)
        self.at(self.cue("artı x üzeri otuz", 3))
        self.play(Create(t39), Create(t58), FadeIn(x1), run_time=0.7)
        self.play(Create(fbk[0]), GrowArrow(fbk[1]), run_time=0.6)
        self.at(self.cue("çerçeveye senkron", 7))
        self.play(GrowArrow(ks), FadeIn(x2), FadeIn(dat), GrowArrow(out[0]), FadeIn(out[1]), FadeIn(fs), run_time=0.8)
        self.at(self.cue("PSBd'den sonraki", 11))
        self.play(FadeIn(pret), run_time=0.4)
        self.at(self.cue("Yükleme deseninin", 14))
        self.play(GrowFromEdge(pre[0], LEFT), run_time=0.6)
        self.at(self.cue("kalan yedi", 18))
        self.play(GrowFromEdge(pre[1], LEFT), run_time=0.4)
        self.at(self.cue("Yani karıştırma", 21))
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f5a")
        self.clear(h)
        h = self.show_heading("Sıralama ve ardışık özdeş rakamlar", h)
        pipe = VGroup(box(2.3, 0.7, "FS çerçevesi", MUTED, 17), box(1.6, 0.7, "FEC", FEC_C, 18), box(2.2, 0.7, "karıştırıcı", ACC, 17), box(1.7, 0.7, "+ PSBd", PSY_C, 17),
                      box(1.2, 0.7, "hat", TW_DS, 17)).arrange(RIGHT, buff=0.45).move_to(UP * 1.5)
        pa = VGroup(*[Arrow(pipe[i].get_right(), pipe[i + 1].get_left(), buff=0.04, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        ord_ = T("önce FEC, sonra karıştırma", 20, GOLD, BOLD).next_to(pipe, DOWN, buff=0.2)
        c = card("Boş XGEM çerçeveleri (§9.1.4)", "içerik vericinin takdirinde — ama hat deseni kontrolü\nve ardışık özdeş rakamların önlenmesi gözetilmeli", None, ACC, w=11.0, h=1.6, tsize=22, bsize=20).move_to(DOWN * 0.6)
        cid = pill("ONU alıcısı: 72 bit CID bağışıklığı — zincirin sonundaki güvence", GOOD, 21).move_to(DOWN * 2.3)
        self.play(LaggedStart(*[FadeIn(p) for p in pipe], lag_ratio=0.12), Create(pa), self.set_src("G.989.3 §10.1.3 · §9.1.4 · G.989.2 Tablo 11-4, 11-5"), run_time=1.0)
        self.at(self.cue("FEC karıştırmadan", 1.5))
        self.play(FadeIn(ord_), Indicate(pipe[1], color=FEC_C), run_time=0.8)
        self.at(self.cue("boş XGEM", 7))
        self.play(FadeIn(c, shift=UP * 0.12), run_time=0.6)
        self.at(self.cue("Alıcıdaki yetmiş", 18))
        self.play(FadeIn(cid, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f5b")
        self.clear(h)
        h = self.show_heading("Test vektörleri — Ek A", h)
        tv = VGroup(T("SFC = 0 → karıştırıcının ilk 256 biti (Tablo A.5)", 22, SFC_C, BOLD),
                    T("0x 0000 0000 0000  1FC0 0000 003F  …", 34, TXT, BOLD)).arrange(DOWN, buff=0.22).move_to(UP * 1.2)
        tvb = SurroundingRectangle(tv[1], color=SFC_C, buff=0.18, corner_radius=0.1)
        hx = pill("HEC örnekleri: Ek A.1", GOLD, 21).move_to(DOWN * 0.35)
        do = T("kendi karıştırıcınızı ve HEC'inizi bu vektörlerle doğrulayın", 22, GOOD, BOLD).move_to(DOWN * 1.35)
        wn = pill("bir bitlik hata → bütün aşağı yön trafiği anlamsız", WARN, 22).move_to(DOWN * 2.3)
        self.at(self.cue("süper çerçeve sayacı sıfırken", 3))
        self.play(FadeIn(tv[0]), self.set_src("G.989.3 Ek A"), run_time=0.5)
        self.play(Write(tv[1]), Create(tvb), run_time=1.0)
        self.at(self.cue("HEC için", 10))
        self.play(FadeIn(hx, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Kendi karıştırıcınızı", 13))
        self.play(FadeIn(do), run_time=0.5)
        self.at(self.cue("bir bitlik bir hata", 17))
        self.play(FadeIn(wn, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.note2("f6", ("TOL'u izleme sisteminize bağlayın", "Bildirilen ile ölçülen güç farkı: kalibrasyon ya da donanım sorununun erken işareti."),
                   ("Canlı kanalda ↓ FEC'i açıp kapatmayın", "Standart: aralıklı trafik kaybına yol açabilir."))
        self.bridge_beat("f7", "Şimdi bunları laboratuvarda ölçelim.", pad=0.3)
        self.save_timeline("ep04_p5D")


# ================================ LABORATUVAR ==================================
class E4LabA(Act4):
    HDR, MANIFEST, FIRST = H4["L"], M4("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Verici testleri")
        self.at(self.cue("İki ana cihaz", 2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Tezgâh")
        ins = VGroup(instrument("DCA", 3.0, 2.2), instrument("OSA", 3.0, 2.2), pm_ds(3.0, 2.2)).arrange(RIGHT, buff=0.9).move_to(UP * 0.2)
        cap = VGroup(T("göz · sönüm oranı", 20, GOOD, BOLD), T("spektrum", 20, GOOD, BOLD), T("kalibre güç ölçer", 20, GOOD, BOLD))
        for c, i in zip(cap, ins):
            c.next_to(i, DOWN, buff=0.25)
        self.at(self.cue("göz ve sönüm", 3.5))
        self.play(FadeIn(ins[0], shift=UP * 0.15), FadeIn(cap[0]), run_time=0.6)
        self.at(self.cue("spektrum için OSA", 7))
        self.play(FadeIn(ins[1], shift=UP * 0.15), FadeIn(cap[1]), run_time=0.6)
        self.at(self.cue("Bir de kalibre", 9))
        self.play(FadeIn(ins[2], shift=UP * 0.15), FadeIn(cap[2]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Sönüm oranı: CG'de filtre, CP'de doğrudan", h)
        y = 1.2
        cts = VGroup(*[box(0.8, 0.3, f"CT{i + 1}", CH[i], 12).move_to([-6.25, y + 0.55 - 0.37 * i, 0]) for i in range(4)])
        wm = box(0.6, 1.5, "WM", "#3B4A75", 14).move_to([-5.15, y, 0])
        l1 = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=FEED, stroke_width=1.5) for c in cts])
        cg = DashedLine([-4.45, y - 0.9, 0], [-4.45, y + 0.9, 0], color=ACC, stroke_width=2)
        cgt = T("S/R-CG", 15, ACC, BOLD).next_to(cg, DOWN, buff=0.05)
        bpf = box(2.4, 0.75, "ayarlanabilir BPF", GOLD, 16).move_to([-2.4, y, 0])
        dca = instrument("DCA", 2.0, 1.45).move_to([0.8, y + 0.1, 0])
        ln = VGroup(Line(wm.get_right(), bpf.get_left(), color=FEED, stroke_width=2.5), Arrow(bpf.get_right(), [dca[0].get_left()[0], y, 0], buff=0.02, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.2))
        sx0, sb = 3.0, y - 0.55
        sbase = Line([sx0, sb, 0], [6.6, sb, 0], color=MUTED, stroke_width=1.5)
        sch = VGroup(*[Line([sx0 + 0.5 + 0.85 * i, sb, 0], [sx0 + 0.5 + 0.85 * i, sb + 1.1, 0], color=CH[i], stroke_width=4) for i in range(4)])
        pb = VMobject(color=GOLD, stroke_width=2.5).set_points_smoothly([[sx0 + 0.5 + 0.85 + x, sb + 1.3 * np.exp(-(x / 0.33) ** 4), 0] for x in np.linspace(-0.75, 0.75, 40)])
        st = T("komşular bastırılır · modülasyon korunur", 15, GOLD, BOLD).move_to([4.8, sb - 0.3, 0])
        y2 = -1.75
        ct = box(1.1, 0.6, "CT", TW_DS, 16).move_to([-5.6, y2, 0])
        cp = DashedLine([-4.6, y2 - 0.6, 0], [-4.6, y2 + 0.6, 0], color=GOLD, stroke_width=2)
        cpt = T("S/R-CP", 15, GOLD, BOLD).next_to(cp, DOWN, buff=0.05)
        dca2 = instrument("DCA", 2.0, 1.45).move_to([-1.8, y2 + 0.1, 0])
        l2 = Arrow(ct.get_right(), [dca2[0].get_left()[0], y2, 0], buff=0.02, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.1)
        dt = T("tek kanal → doğrudan", 20, GOOD, BOLD).move_to([2.2, y2, 0])
        self.play(FadeIn(cts), Create(l1), FadeIn(wm), Create(cg), FadeIn(cgt), self.set_src("G.989.2 §9.3.2"), run_time=0.8)
        self.at(self.cue("DCA'nın önüne", 2.5))
        self.play(Create(ln[0]), FadeIn(bpf), GrowArrow(ln[1]), FadeIn(dca), run_time=0.8)
        self.at(self.cue("Filtre komşu", 8))
        self.play(Create(sbase), FadeIn(sch), Create(pb), run_time=0.7)
        self.play(*[sch[i].animate.set_stroke(opacity=0.25) for i in (0, 2, 3)], run_time=0.5)
        self.at(self.cue("ama ölçülen kanalın", 11))
        self.play(FadeIn(st), run_time=0.4)
        self.at(self.cue("CP noktasında ise", 14))
        self.play(FadeIn(ct), Create(cp), FadeIn(cpt), GrowArrow(l2), FadeIn(dca2), run_time=0.8)
        self.play(FadeIn(dt), run_time=0.4)
        self.end(pad=0.05)

        self.beat("g3")
        self.clear(h)
        h = self.show_heading("DCA: referans filtre, maske, marj", h)
        o, W, H = np.array([-4.7, -1.45, 0]), 3.0, 2.2
        scr = eye_frame(o, W, H)
        eye = eye_traces(o, W, H, ov=0.1, op=0.45)
        mk = eye_mask(o, W, H, 0.4, 0.6)
        big = eye_mask(o, W, H, 0.31, 0.69, y1=0.18, y2=0.82, y3=0.17, y4=0.17, color=GOLD)
        steps = VGroup(T("1 · 4. derece Thomson, 0,75 × nominal hız", 21, TXT, BOLD), T("2 · göz maskesini uygula", 21, TXT, BOLD),
                       T("3 · maskeyi ihlalsiz büyüt → marjı kaydet", 21, GOLD, BOLD), T("standart marjı tanımlamaz —", 19, MUTED),
                       T("üretimde vericinin sağlığını izlemenin en hızlı yolu", 19, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.0, 0.0, 0])
        steps[3:].shift(DOWN * 0.25)
        self.play(FadeIn(scr), FadeIn(eye), FadeIn(steps[0]), self.set_src("G.989.2 §11.1.5.3 · Şekil 11-4"), run_time=0.8)
        self.at(self.cue("Göz maskesini", 7))
        self.play(FadeIn(mk), FadeIn(steps[1]), run_time=0.6)
        self.at(self.cue("ve maske ihlali", 9))
        self.play(Transform(mk, big), FadeIn(steps[2]), run_time=1.2)
        self.at(self.cue("Standart marjı", 15))
        self.play(FadeIn(steps[3]), run_time=0.4)
        self.at(self.cue("ama üretimde", 17))
        self.play(FadeIn(steps[4]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g4")
        self.clear(h)
        h = self.show_heading("Sönüm oranı: karanlık düzey kalibrasyonu", h)
        yb, H1 = -2.2, 3.6
        base = Line([-6.0, yb, 0], [-0.6, yb, 0], color=MUTED, stroke_width=2)
        b1 = Rectangle(width=1.1, height=H1, stroke_width=0, fill_color=TW_DS, fill_opacity=0.8).move_to([-4.6, yb + H1 / 2, 0])
        b0 = Rectangle(width=1.1, height=H1 * 0.151, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([-2.2, yb + H1 * 0.151 / 2, 0])
        lb = VGroup(T("P1", 22, TW_DS, BOLD).next_to(b1, UP, buff=0.1), T("P0", 22, GOLD, BOLD).next_to(b0, UP, buff=0.1))
        pct = T("≈ %15", 22, GOLD, BOLD).next_to(lb[1], UP, buff=0.12)
        off = Rectangle(width=1.1, height=0.2, stroke_width=0, fill_color=WARN, fill_opacity=0.85).next_to(b0, UP, buff=0)
        offt = T("küçük ofset", 17, WARN, BOLD).next_to(off, RIGHT, buff=0.15)
        txt = VGroup(pill("önce: DCA karanlık düzey kalibrasyonu", ACC, 20), T("ER 8,2 dB → P0 ≈ %15 · P1", 26, GOLD, BOLD),
                     T("sıfır düzeyindeki küçük hata", 21, TXT), T("→ büyük ER ölçüm hatası", 21, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.2, 0])
        self.play(FadeIn(txt[0], shift=UP * 0.1), Create(base), self.set_src("G.989.2 §9.3.2"), run_time=0.6)
        self.at(self.cue("Sıfır düzeyindeki", 5))
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b0, DOWN), FadeIn(lb), run_time=0.8)
        self.at(self.cue("sekiz virgül iki desibellik", 9))
        self.play(FadeIn(txt[1]), FadeIn(pct), run_time=0.5)
        self.at(self.cue("küçük bir ofset", 15))
        self.play(GrowFromEdge(off, DOWN), FadeIn(offt), FadeIn(txt[2:]), pct.animate.shift(UP * 0.2), lb[1].animate.shift(UP * 0.2), run_time=0.7)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_labA")


def osa_screen(cx, cy, w, h):
    s = scope(w, h, [cx, cy, 0])
    return s


class E4LabB(Act4):
    HDR, MANIFEST, PREV_BADGE = H4["L"], M4("lab"), "lab"

    def construct(self):
        self.beat("g5")
        h = self.show_heading("OSA: SMSR ve merkez frekans")
        cx, cy, w, hh = -2.9, -0.4, 6.6, 4.2
        scr = osa_screen(cx, cy, w, hh)
        o = np.array([cx, cy - hh / 2 + 0.15, 0])
        fl, sy = -62.0, 0.062
        spec = spec_db(o, 1.0, sy, [(0, 0), (-1.0, -38), (1.0, -35), (-2.0, -48), (2.0, -46)], (-3.2, 3.2), floor=fl, w=0.012, n=700, color=GOOD, sw=2.5)
        ytop, ys = o[1] + (0 - fl) * sy, o[1] + (-35 - fl) * sy
        ax_ = o[0] + 2.4
        sm = VGroup(DashedLine([o[0] + 0.1, ytop, 0], [ax_ + 0.1, ytop, 0], color=GOLD, stroke_width=1.5), DashedLine([o[0] + 1.05, ys, 0], [ax_ + 0.1, ys, 0], color=GOLD, stroke_width=1.5),
                    DoubleArrow([ax_, ys, 0], [ax_, ytop, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12), T("> 30 dB", 18, GOLD, BOLD).next_to([ax_, (ys + ytop) / 2, 0], RIGHT, buff=0.08))
        info = VGroup(T("lazer çıkışında (S/R-CP)", 21, TXT, BOLD), T("ana mod − en güçlü yan mod > 30 dB", 20, GOLD, BOLD), T("merkez frekans ↔ Tablo 11-2", 21, TXT, BOLD),
                      T("fark ± 20 GHz içinde", 20, TW_DS, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.2, 0.9, 0])
        info[2:].shift(DOWN * 0.2)
        temps = VGroup(pill("T_min", TW_US, 19), pill("T_maks", WARN, 19)).arrange(RIGHT, buff=0.3)
        tt = VGroup(T("sıcaklık aralığının iki ucunda tekrarla", 18, MUTED), temps).arrange(DOWN, buff=0.15).move_to([4.2, -1.6, 0])
        f0 = DashedLine([o[0], o[1], 0], [o[0], ytop + 0.25, 0], color=TW_DS, stroke_width=2)
        self.play(FadeIn(scr), Create(spec), FadeIn(info[0]), self.set_src("G.989.2 §9.3.8 · §11.1.5.2.4 · Tablo 11-2"), run_time=1.0)
        self.at(self.cue("ana mod ile", 3))
        self.play(FadeIn(sm), FadeIn(info[1]), run_time=0.6)
        self.at(self.cue("Merkez frekansı", 9))
        self.play(Create(f0), FadeIn(info[2]), run_time=0.5)
        self.at(self.cue("fark artı eksi", 13))
        self.play(FadeIn(info[3]), run_time=0.4)
        self.at(self.cue("Bu ölçümü", 17))
        self.play(FadeIn(tt, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g5a")
        self.clear(h)
        h = self.show_heading("Dalga boyu kararlılığı: sıcaklık kabini", h)
        ch = RoundedRectangle(corner_radius=0.15, width=3.4, height=3.2, stroke_color=MUTED, stroke_width=2.5, fill_color="#0C1324", fill_opacity=1).move_to([-4.9, -0.3, 0])
        cht = T("sıcaklık kabini", 17, MUTED).next_to(ch, UP, buff=0.08)
        card_ = box(2.2, 0.9, "OLT kartı", TW_DS, 18).move_to(ch.get_center() + DOWN * 0.3)
        th = VGroup(RoundedRectangle(corner_radius=0.08, width=0.16, height=0.9, stroke_color=WARN, stroke_width=2), Circle(radius=0.14, color=WARN, fill_color=WARN, fill_opacity=1)).arrange(DOWN, buff=-0.05).move_to(ch.get_center() + UP * 0.9 + RIGHT * 1.1)
        x0, y0, w, hh = -2.1, -0.4, 8.4, 1.4
        band_ = Rectangle(width=w, height=2 * hh, stroke_width=0, fill_color=TW_DS, fill_opacity=0.1).move_to([x0 + w / 2, y0, 0])
        lim = VGroup(DashedLine([x0, y0 + hh, 0], [x0 + w, y0 + hh, 0], color=TW_DS, stroke_width=2), DashedLine([x0, y0 - hh, 0], [x0 + w, y0 - hh, 0], color=TW_DS, stroke_width=2),
                     T("+20 GHz", 15, TW_DS, BOLD).next_to([x0, y0 + hh, 0], LEFT, buff=0.08), T("−20 GHz", 15, TW_DS, BOLD).next_to([x0, y0 - hh, 0], LEFT, buff=0.08),
                     Line([x0, y0, 0], [x0 + w, y0, 0], color=LINE, stroke_width=1.5), T("Δf", 16, MUTED).next_to([x0, y0, 0], LEFT, buff=0.1))
        tl = T("zaman", 15, MUTED).next_to([x0 + w / 2, y0 - hh, 0], DOWN, buff=0.12)
        ts = np.linspace(0, 1, 160)

        def df(t):
            warm = -0.75 * np.exp(-t / 0.05)
            step = 0.0 if t < 0.4 else (-0.35 * (1 - np.exp(-(t - 0.4) / 0.04)) if t < 0.7 else -0.35 * np.exp(-(t - 0.7) / 0.03) + 0.4 * (1 - np.exp(-(t - 0.7) / 0.04)))
            return warm + step + 0.03 * np.sin(60 * t)
        tr_ = VMobject(color=GOLD, stroke_width=3).set_points_smoothly([[x0 + w * t, y0 + hh * df(t), 0] for t in ts])
        phase = VGroup(T("açılış / ısınma", 15, MUTED).move_to([x0 + w * 0.12, y0 + hh + 0.25, 0]), T("T_min", 15, TW_US, BOLD).move_to([x0 + w * 0.55, y0 + hh + 0.25, 0]),
                       T("T_maks", 15, WARN, BOLD).move_to([x0 + w * 0.86, y0 + hh + 0.25, 0]))
        cap = T("sınır ısınma dahil her an sağlanmalı", 21, GOOD, BOLD).move_to([x0 + w / 2, -2.6, 0])
        self.play(FadeIn(ch), FadeIn(cht), FadeIn(card_), FadeIn(th), self.set_src("G.989.2 §11.1 · §11.1.5.2.4"), run_time=0.7)
        self.at(self.cue("çalışma aralığının", 3))
        self.play(FadeIn(band_), FadeIn(lim), FadeIn(tl), run_time=0.6)
        self.play(Create(tr_), FadeIn(phase), run_time=1.5)
        self.at(self.cue("Kart açılıştan", 9))
        self.play(Indicate(phase[0], color=GOLD), run_time=0.8)
        self.at(self.cue("artı eksi yirmi", 14))
        self.play(FadeIn(cap), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g6")
        self.clear(h)
        h = self.show_heading("Güç yoğunluğu: CG'de, tek kanal açık", h)
        cx, cy, w, hh = -2.3, -0.35, 8.6, 4.1
        scr = osa_screen(cx, cy, w, hh)
        x0, x1 = cx - w / 2 + 0.25, cx + w / 2 - 0.25
        X = lambda nm: x0 + (nm - 1595) / 32 * (x1 - x0)
        yb, sy, fl = cy - hh / 2 + 0.1, 0.05, -70.0
        Y = lambda db: yb + (db - fl) * sy
        o = np.array([X(DS_NM[1]), yb, 0])
        k_ = (x1 - x0) / 32
        pk, wl, nf = 5.0, 0.005, -66.0
        lvl = lambda nm: 10 * np.log10(10 ** (pk / 10) / (1 + ((nm - DS_NM[1]) / wl) ** 2) + 10 ** (nf / 10))
        spec = spec_db(o, k_, sy, [(0, pk)], ((x0 - o[0]) / k_, (x1 - o[0]) / k_), floor=nf, w=wl, n=500, color=GOOD, sw=2.5).shift(UP * (nf - fl) * sy)
        ooc = DashedLine([X(1595.5), Y(-34.5), 0], [X(1600.2), Y(-34.5), 0], color=ACC, stroke_width=2.5)
        oob = DashedLine([X(1603), Y(-44.9), 0], [X(1625), Y(-44.9), 0], color=PTP, stroke_width=2.5)
        oot = VGroup(T("OOC sınırı −34,5", 15, ACC, BOLD).next_to(ooc, RIGHT, buff=0.12), T("OOB sınırı −44,9 dBm / 15 GHz (4 kanal)", 15, PTP, BOLD).next_to(oob, UP, buff=0.06).align_to(oob, RIGHT))
        mk = VGroup(*[Dot([X(v), Y(lvl(v)), 0], radius=0.07, color=ACC) for v in (DS_NM[0], DS_NM[2], DS_NM[3])],
                    *[Dot([X(v), Y(lvl(v)), 0], radius=0.07, color=PTP) for v in (1606, 1612, 1618, 1624)])
        steps = VGroup(T("1 · yalnızca ölçülen kanal açık", 19, TXT, BOLD), T("2 · RBW 0,1 nm → 15 GHz: ≈ +1 dB", 19, GOLD, BOLD), T("3 · komşu kanallarda ve PtP", 19, TXT, BOLD),
                       T("    bandında oku → tablo sınırı", 19, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        steps.scale_to_fit_width(min(steps.width, 4.1)).move_to([4.7, 0.4, 0])
        self.play(FadeIn(scr), Create(spec), FadeIn(steps[0]), self.set_src("G.989.2 Tablo 11-4, 11-5 · Bölüm 3"), run_time=1.0)
        self.at(self.cue("Okuduğunuz değeri", 9))
        self.play(FadeIn(steps[1]), run_time=0.5)
        self.at(self.cue("Komşu kanal frekanslarında", 18))
        self.play(Create(ooc), Create(oob), FadeIn(oot), FadeIn(steps[2:]), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mk], lag_ratio=0.1), run_time=0.8)
        self.end(pad=0.05)

        self.beat("g6a")
        self.clear(h)
        h = self.show_heading("SMSR için OSA çözünürlüğü", h)

        def panel(cx, wl, title, col, note):
            sc = osa_screen(cx, -0.45, 5.8, 3.7)
            o = np.array([cx, -0.45 - 1.85 + 0.15, 0])
            sp = spec_db(o, 1.0, 0.055, [(0, 0), (1.2, -36), (-1.2, -40)], (-2.7, 2.7), floor=-60, w=wl, n=600, color=col, sw=2.5)
            tt = T(title, 20, col, BOLD).move_to([cx, 1.75, 0])
            nt = T(note, 17, col).move_to([cx, -2.75, 0])
            return VGroup(sc, sp, tt, nt)
        fine = panel(-3.2, 0.012, "ince çözünürlük", GOOD, "yan mod ayrışır → doğru SMSR")
        coarse = panel(3.2, 0.3, "kaba çözünürlük", WARN, "ana modun eteği yan modu örter")
        nm1 = VGroup(DoubleArrow([-3.2, 0.95, 0], [-2.0, 0.95, 0], buff=0, color=GOLD, stroke_width=2, tip_length=0.1), T("≈ 1 nm", 15, GOLD, BOLD).move_to([-2.6, 1.2, 0]))
        self.play(FadeIn(fine[0]), Create(fine[1]), FadeIn(fine[2]), self.set_src("G.989.2 §9.3.8"), run_time=1.0)
        self.at(self.cue("Tipik bir DFB", 7))
        self.play(FadeIn(nm1), FadeIn(fine[3]), run_time=0.5)
        self.at(self.cue("Çözünürlük çok kaba", 12))
        self.play(FadeIn(coarse[0]), Create(coarse[1]), FadeIn(coarse[2]), run_time=1.0)
        self.at(self.cue("ana modun eteği", 14))
        self.play(FadeIn(coarse[3]), run_time=0.4)
        self.end(pad=0.05)

        self.beat("g7")
        self.clear(h)
        h = self.show_heading("Başlatma gücü ve TOL", h)
        y = 0.9
        cts = VGroup(*[box(0.8, 0.3, f"CT{i + 1}", CH[i], 12).move_to([-6.25, y + 0.55 - 0.37 * i, 0]) for i in range(4)])
        wm = box(0.6, 1.5, "WM", "#3B4A75", 14).move_to([-5.15, y, 0])
        l1 = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=FEED, stroke_width=1.5) for c in cts])
        cg = DashedLine([-4.45, y - 0.9, 0], [-4.45, y + 0.9, 0], color=ACC, stroke_width=2)
        cgt = T("S/R-CG", 15, ACC, BOLD).next_to(cg, DOWN, buff=0.05)
        flt = box(2.3, 0.75, "filtre / OSA", GOLD, 16).move_to([-2.3, y, 0])
        pm = pm_ds(2.0, 1.45).move_to([0.9, y + 0.1, 0])
        ln = VGroup(Line(wm.get_right(), flt.get_left(), color=FEED, stroke_width=2.5), Arrow(flt.get_right(), [pm[0].get_left()[0], y, 0], buff=0.02, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.2))
        each = T("her kanal ayrı ayrı\ntoplam gücü okumayın", 19, GOLD, BOLD, line_spacing=0.9).move_to([4.7, y, 0])
        cmp_ = VGroup(card("ölçülen", "kalibre güç ölçer", None, GOOD, w=3.6, h=1.3, tsize=24, bsize=18), T("↔", 36, TXT, BOLD),
                      card("TOL", "OC alanı · her çerçevede", None, OC_C, w=3.6, h=1.3, tsize=24, bsize=18)).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.65)
        self.play(FadeIn(cts), Create(l1), FadeIn(wm), Create(cg), FadeIn(cgt), self.set_src("G.989.2 §11.1.5.2.8 · G.989.3 §10.1.1.1.3"), run_time=0.8)
        self.play(Create(ln[0]), FadeIn(flt), GrowArrow(ln[1]), FadeIn(pm), run_time=0.8)
        self.at(self.cue("çok kanallı noktada", 6))
        self.play(FadeIn(each), run_time=0.5)
        self.at(self.cue("Ölçtüğünüz değeri", 12))
        self.play(FadeIn(cmp_, shift=UP * 0.12), run_time=0.7)
        self.end(pad=0.05)

        self.note2("g8", ("Referans noktayı yazın: CG mi, CP mi?", "Aynı vericinin iki noktada farklı sonuç vermesi normaldir."),
                   ("Göz marjını üretim boyunca izleyin", "Marjdaki yavaş düşüş: lazerin yaşlandığının ilk işareti."))
        self.clear()
        self.drop_badge()
        self.save_timeline("ep04_labB")


# ================================ KAPANIŞ ======================================
class E4End(Act4):
    HDR, MANIFEST, FIRST = H4["E"], M4("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 4'ün özeti")
        self.at(1.5)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["OLT = bütün PON'un saati · normalde Stratum-1 · ONU ↑ aynı doğrulukla",
               "Başlatma gücü: sınıf başına 4 dB pencere (10G E2: 2 dB) · ER ≥ 8,2 dB, güçle takas",
               "SMSR → lazer · OOB (PtP WDM) / OOC (diğer TWDM) → arayüz",
               "Göz maskesi ve titreşim: OTN ve SDH mirası",
               "125 µs çerçeve: PSBd · FEC → karıştırıcı · TOL her çerçevede"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 20, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        self.at(self.cue("Bir:", 1.5))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 9))
        self.play(FadeIn(items[1], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, key in zip([2, 3, 4], ["Üç:", "Dört:", "Beş:"]):
            self.at(self.cue(key, 0.3 + 8 * (k - 2)))
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=18) for i, (q, c) in enumerate([
            ("10G OLT · N1 · en küçük\nbaşlatma gücünde:\nTOL alanında hangi sayı?", CH[0]),
            ("10G E2: en büyük güç ile\n4 kanallı kanal dışı sınır\narasındaki fark kaç dB?", CH[1]),
            ("2,5G ↓ çerçevesinde\nson kod sözcüğü\nneden kısa?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 5'in başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, key in enumerate(["Birinci soru", "İkinci soru", "Üçüncü soru"]):
            self.at(self.cue(key, 1 + 8 * k))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("Cevaplar", 25))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        sub = EP5["sub"]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Bölüm {EP5['n']} · {EP5['title']}", 54, TXT, BOLD),
                     T(sub, 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 0.9)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        base = Line([-3.0, -2.4, 0], [3.0, -2.4, 0], color=MUTED, stroke_width=1.5)
        chs = VGroup(*[Line([-2.25 + 1.5 * i, -2.4, 0], [-2.25 + 1.5 * i, -1.3, 0], color=CH[i], stroke_width=4) for i in range(4)])
        flt = VMobject(color=GOLD, stroke_width=3).set_points_smoothly([[-2.25 + x, -2.4 + 1.4 * np.exp(-(x / 0.42) ** 4), 0] for x in np.linspace(-0.9, 0.9, 40)])
        self.play(Create(base), FadeIn(chs), Create(flt), run_time=0.8)
        for i in (1, 2):
            self.play(flt.animate.shift(RIGHT * 1.5), run_time=0.6)
        self.end(pad=0.6)
        self.play(FadeOut(VGroup(nxt, base, chs, flt)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 4 · Kaynak", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Google Gemini TTS — ses: Sadaltager", 22, ACC, BOLD),
                    T("(Gemini 2.5 Flash TTS)", 18, ACC),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep04_end")
