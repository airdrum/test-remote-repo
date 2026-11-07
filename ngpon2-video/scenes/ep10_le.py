"""B10 · Sahada (ölçüm çantası ve arıza vakaları) and Kapanış (sezon finali)."""
from ep10_common import *


def otdr_icon(w=2.0, h=1.45):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    scr = Rectangle(width=w * 0.78, height=h * 0.52, stroke_color="#334155", stroke_width=1.5, fill_color="#050810", fill_opacity=1).move_to(body).shift(UP * h * 0.1)
    x0, x1 = scr.get_left()[0] + 0.08, scr.get_right()[0] - 0.08
    y0, y1 = scr.get_bottom()[1] + 0.06, scr.get_top()[1] - 0.06
    pts = []
    for k in range(40):
        u = k / 39
        y = y1 - (y1 - y0) * 0.85 * u
        if 0.45 < u < 0.48:
            y += 0.12
        if 0.46 < u < 0.5:
            y -= 0.08
        pts.append([x0 + u * (x1 - x0), y, 0])
    tr_ = VMobject(stroke_color=GOOD, stroke_width=2).set_points_as_corners(pts)
    lab = T("OTDR", 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1)
    return VGroup(body, scr, tr_, lab)


ODN_C = "#FB923C"


def bolt(h=0.55, color=WARN):
    pts = [[0.08, 0.5], [-0.22, 0.02], [0.0, 0.02], [-0.1, -0.5], [0.22, 0.06], [0.0, 0.06]]
    return Polygon(*[[x * h * 1.6, y * h * 1.6, 0] for x, y in pts], stroke_width=0, fill_color=color, fill_opacity=1)


def case_tag(n, color=WARN):
    return pill(f"VAKA {n}", color, 18)


class E10LabA(Act10):
    HDR, MANIFEST, FIRST = H10["L"], M10("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("SAHADA", "Ölçüm çantası ve arıza vakaları")
        self.at(2.4)
        self.to_header(tc)
        self.set_badge("saha")
        h = self.show_heading("ODN kabulü")
        ax0, ax1, ya = -6.2, -0.7, -0.75
        axg, X = lin_axis(10, 38, ax0, ax1, ya, [10, 14, 18, 22, 26, 30, 34, 38], size=14, fmt=lambda v: str(int(v)), unit="optik yol kaybı (dB)")
        cls = [("N1", 14, 29), ("N2", 16, 31), ("E1", 18, 33), ("E2", 20, 35)]
        bars = VGroup()
        for i, (n, a, b) in enumerate(cls):
            y = 1.75 - i * 0.55
            r = Rectangle(width=X(b) - X(a), height=0.38, stroke_width=0, fill_color=ODN_C, fill_opacity=0.7).move_to([(X(a) + X(b)) / 2, y, 0])
            bars.add(VGroup(r, T(f"{n}  {a} … {b}", 15, BG, BOLD).move_to(r)))
        bt = T("sınıf pencereleri · Tablo 6-1", 15, ODN_C, BOLD).next_to(bars, UP, buff=0.12).align_to(bars, LEFT)
        low = VGroup(arrow([X(10.6), 1.75, 0], [X(13.6), 1.75, 0], WARN, 3, 0.14), T("altında", 14, WARN, BOLD).move_to([X(11.8), 2.0, 0]))
        att = VGroup(RoundedRectangle(corner_radius=0.08, width=1.05, height=0.5, stroke_color=GOLD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), T("dB", 18, GOLD, BOLD))
        att[1].move_to(att[0])
        att.move_to([-5.4, -1.85, 0])
        attt = T("zayıflatıcı ile en küçük kaybı sağla (§6.2)", 17, GOLD, BOLD).next_to(att, RIGHT, buff=0.2)
        ck = RoundedRectangle(corner_radius=0.16, width=5.9, height=3.6, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([3.65, 0.35, 0])
        ckt = T("kabul listesi", 20, GOOD, BOLD).move_to(ck.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        its = [("OPL sınıf penceresinde", None), ("diferansiyel OPL ≤", "15 dB"), ("ORL ≥", "32 dB"), ("ayrık yansıma <", "−35 dB")]
        items = VGroup(*[VGroup(T("✓", 21, GOOD, BOLD), T(a, 19, TXT), *([T(b, 19, GOLD, BOLD)] if b else [])).arrange(RIGHT, buff=0.15) for a, b in its]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        items.next_to(ckt, DOWN, buff=0.3, aligned_edge=LEFT)
        refs = T("Tablo 6-1 · 11-4…11-7 · §9.3.5.3", 14, MUTED).move_to(ck.get_corner(DL) + [0.3, 0.25, 0], aligned_edge=LEFT)
        self.at(self.cue("Önce ODN kabulü", 4.0))
        self.play(Create(axg[0]), FadeIn(axg[1:]), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.15), FadeIn(bt),
                  self.set_src("G.989.2 §6.2 · Tablo 6-1 · Tablo 11-4…11-7 · §9.3.5.3"), run_time=1.0)
        self.play(FadeIn(ck), FadeIn(ckt), FadeIn(refs), run_time=0.4)
        self.at(self.cue("sınıf penceresinin", 5.4))
        self.play(FadeIn(items[0], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("En küçük kaybın", 8.0))
        self.play(GrowArrow(low[0]), FadeIn(low[1]), run_time=0.5)
        self.at(self.cue("zayıflatıcı içermelidir", 11.0))
        self.play(FadeIn(att, shift=UP * 0.1), FadeIn(attt), run_time=0.6)
        for i, (key, d) in enumerate((("Diferansiyel yol", 16.0), ("geri dönüş kaybı", 19.8), ("ayrık yansımalar", 23.1)), 1):
            self.at(self.cue(key, d))
            self.play(FadeIn(items[i], shift=RIGHT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # g2 — distance and OTDR
        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Mesafe ve OTDR", h)
        kax, K = lin_axis(0, 40, -6.0, -0.8, -0.2, [0, 10, 20, 30, 40], size=14, fmt=lambda v: str(int(v)), unit="km")
        d20 = VGroup(Rectangle(width=K(20) - K(0), height=0.45, stroke_width=0, fill_color=ACC, fill_opacity=0.7), T("DD20 · 0 … 20 km", 16, BG, BOLD))
        d20[0].move_to([(K(0) + K(20)) / 2, 1.2, 0])
        d20[1].move_to(d20[0])
        d40 = VGroup(Rectangle(width=K(40) - K(0), height=0.45, stroke_width=0, fill_color=TW_US, fill_opacity=0.7), T("DD40 · 0 … 40 km", 16, BG, BOLD))
        d40[0].move_to([(K(0) + K(40)) / 2, 0.55, 0])
        d40[1].move_to(d40[0])
        dt = T("mesafe sınıfları · Tablo 6-2", 15, MUTED).next_to(d20, UP, buff=0.12).align_to(d20, LEFT)
        ot = otdr_icon().move_to([-3.4, -2.05, 0])
        r1 = VGroup(T("bakım dalga boyu:", 19, MUTED, BOLD), T("L.313'e uygun (Tablo 11-3)", 19, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        r2 = VGroup(T("madde 10:", 19, MUTED, BOLD), T("OTDR = geniş bant girişimci", 19, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        r3 = VGroup(T("✓", 20, GOOD, BOLD), T("NG-PON2 alıcısı bu girişime dayanmalı", 19, TXT)).arrange(RIGHT, buff=0.15)
        r4 = VGroup(T("✓", 20, GOOD, BOLD), T("bakım λ planlanmış bantta kalmalı", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        rs = VGroup(r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 0.0, 0])
        fit(rs, 6.1)
        self.play(Create(kax[0]), FadeIn(kax[1:]), GrowFromEdge(d20[0], LEFT), FadeIn(d20[1]), GrowFromEdge(d40[0], LEFT), FadeIn(d40[1]), FadeIn(dt),
                  self.set_src("G.989.2 Tablo 6-2 · Tablo 11-3 · madde 10"), run_time=0.9)
        self.at(self.cue("OTDR bakım dalga boyu", 3.7))
        self.play(FadeIn(ot, shift=UP * 0.1), FadeIn(r1, shift=RIGHT * 0.1), run_time=0.6)
        self.at(self.cue("geniş bant girişimciler", 8.6))
        self.play(FadeIn(r2, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("dayanması beklenir", 13.0))
        self.play(FadeIn(r3, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("planlanmış bantta", 17.2))
        self.play(FadeIn(r4, shift=RIGHT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g3 — power readings
        self.beat("g3")
        self.clear(h)
        h = self.show_heading("Güç okumaları", h)
        onu = sbox("ONU", "RSSI bildirir", ONUC, 2.0, 1.0, 21, 15).move_to([-5.2, 0.75, 0])
        pm = instr("PM", 2.0, 1.45, "Rx gücü", "PON güç ölçer").move_to([-2.0, 0.8, 0])
        cab = Line(onu.get_right(), pm[0].get_left(), color=FEED, stroke_width=3)
        dif = DoubleArrow([-5.2, -0.45, 0], [-2.0, -0.45, 0], buff=0, color=GOLD, stroke_width=3, tip_length=0.15)
        dft = VGroup(T("≤ 3 dB fark: normal", 20, GOLD, BOLD), T("Ek II doğruluğu (±3 dB)", 16, MUTED)).arrange(DOWN, buff=0.06).next_to(dif, DOWN, buff=0.12)
        sep = DashedLine([-0.2, 1.9, 0], [-0.2, -2.6, 0], color=LINE, stroke_width=2)
        olt = sbox("OLT", "başlatma gücü", OLTC, 2.0, 1.0, 21, 15).move_to([1.25, 0.75, 0])
        c1 = card("PSBd · TOL", "0,1 dB adım · −30 dBm referans", None, GOLD, w=4.2, h=1.0, tsize=19, bsize=16).move_to([4.7, 1.25, 0])
        c2 = card("izleme sayacı", "Tablo 14-1 · Tx optik güç düzeyi", None, OLTC, w=4.2, h=1.0, tsize=19, bsize=16).move_to([4.7, 0.05, 0])
        c3 = card("C biti: hangi referans noktası?", "S/R-CG (0) · S/R-CP (1)", None, ACC, w=5.8, h=1.0, tsize=19, bsize=17).move_to([3.4, -1.55, 0])
        self.at(self.cue("kendi bildirdiği", 1.2))
        self.play(FadeIn(onu, shift=UP * 0.1), Create(cab), FadeIn(pm, shift=UP * 0.1), self.set_src("G.989.2 Ek II · G.989.3 §10.1.1.1.3 · Tablo 14-1"), run_time=0.7)
        self.at(self.cue("üç desibele kadar", 7.2))
        self.play(GrowFromCenter(dif), FadeIn(dft, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("OLT'nin başlatma gücünü", 11.8))
        self.play(Create(sep), FadeIn(olt), FadeIn(c1, shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("izleme sayaçlarından", 16.5))
        self.play(FadeIn(c2, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("referans noktasına ait", 20.4))
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g4 — case 1: ONU not visible
        self.beat("g4")
        self.clear(h)
        h = self.show_heading("Vaka 1 · ONU görünmüyor", h)
        tg = case_tag(1).move_to([-5.6, 1.95, 0])
        sy = T("OLT'nin listesinde yok", 19, MUTED).next_to(tg, RIGHT, buff=0.3)
        steps = VGroup(sbox("1 · LODS sayaçları", "Tablo 14-1", STATE, 3.9, 1.0, 19, 15), sbox("2 · Activation Debug", "SN mesajı · oktet 40", TW_US, 3.9, 1.0, 19, 15),
                       sbox("3 · C bayrağı", "kanal değişti mi?", GOLD, 3.9, 1.0, 19, 15)).arrange(RIGHT, buff=0.5).move_to([0, 0.75, 0])
        sa = VGroup(*[arrow(steps[i].get_right(), steps[i + 1].get_left(), MUTED, 2.5, 0.14) for i in range(2)])
        codes = VGroup(*[VGroup(T(a, 18, GOLD, BOLD), T(b, 17, TXT)).arrange(RIGHT, buff=0.2) for a, b in
                         (("0110 / 0111", "senkron kaybı (O2-3 / O4)"), ("1000 … 1100", "zamanlayıcı (TOZ, TO1, TO2, TO4, TO5)"), ("1101", "güç kaybı"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        codes.next_to(steps[1], DOWN, buff=0.4).shift(LEFT * 0.6)
        self.at(self.cue("bir ONU görünmüyor", 0.8))
        self.play(FadeIn(tg, shift=RIGHT * 0.1), FadeIn(sy), self.set_src("G.989.3 Tablo 14-1 · Serial_Number_ONU (Activation Debug, C bayrağı)"), run_time=0.5)
        self.at(self.cue("senkron kaybı sayaçlarına", 2.4))
        self.play(FadeIn(steps[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("hata ayıklama kodu", 5.5))
        self.play(GrowArrow(sa[0]), FadeIn(steps[1], shift=UP * 0.1), run_time=0.5)
        for i, (key, d) in enumerate((("senkron kaybı mı", 12.5), ("bir zamanlayıcı mı", 13.9), ("güç kaybı mı", 15.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(codes[i], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("Kanal değişti bayrağı", 16.6))
        self.play(GrowArrow(sa[1]), FadeIn(steps[2], shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_labA")


class E10LabB(Act10):
    HDR, MANIFEST, PREV_BADGE = H10["L"], M10("lab"), "saha"

    def construct(self):
        # g5 — case 2: dying gasp
        self.beat("g5")
        h = self.show_heading("Vaka 2 · ONU sessizce gidiyor")
        tg = case_tag(2, GOLD).move_to([-5.6, 1.95, 0])
        onu = sbox("ONU", "elektrik gidiyor", ONUC, 2.0, 1.0, 21, 15).move_to([-5.1, 0.55, 0])
        bolt_ = bolt().next_to(onu, UP, buff=0.08).shift(RIGHT * 0.75)
        hb = VGroup(*[VGroup(Rectangle(width=w, height=0.6, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.2), T(n, 16, TXT, BOLD))
                      for n, w, c in (("PSBu", 1.3, MUTED), ("FS başlığı", 2.6, TW_US), ("yük", 3.2, MUTED))])
        for b in hb:
            b[1].move_to(b[0])
        hb.arrange(RIGHT, buff=0).move_to([1.85, 1.05, 0])
        hbt = T("↑ burst", 15, MUTED).next_to(hb, UP, buff=0.08).align_to(hb, LEFT)
        ind = VGroup(RoundedRectangle(corner_radius=0.08, width=4.6, height=0.55, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.2),
                     T("Ind · bit 0 = son nefes (DG)", 18, TXT, BOLD))
        ind[1].move_to(ind[0])
        ind.move_to([1.6, 0.0, 0])
        zl = VGroup(DashedLine(hb[1].get_corner(DL), ind.get_corner(UL), color=GOLD, stroke_width=1.5), DashedLine(hb[1].get_corner(DR), ind.get_corner(UR), color=GOLD, stroke_width=1.5))
        da = arrow(onu.get_right(), ind.get_left() + LEFT * 0.1, GOLD, 2.5, 0.14)
        f1 = card("fiber sorunu?", "ODN tarafı", None, MUTED, w=3.6, h=1.0, tsize=19, bsize=16).move_to([-4.6, -1.55, 0])
        f2 = card("müşteri tarafı?", "yerel sorun · DG ipucu", None, GOLD, w=3.6, h=1.0, tsize=19, bsize=16).move_to([-0.8, -1.55, 0])
        ru = card("OLT", "tahsisleri yalnız DG'ye\ndayanarak geri çekmez", None, WARN, w=3.9, h=1.3, tsize=19, bsize=16).move_to([4.6, -1.55, 0])
        hint = pill("son nefes: bir ipucu, bir komut değil", GOLD, 19).move_to([0, -2.8, 0])
        self.play(FadeIn(tg, shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("Ölmekte olan", 2.9))
        self.play(FadeIn(onu, shift=UP * 0.1), FadeIn(bolt_, scale=0.6), self.set_src("G.989.3 §8.1.2.1.2 · Tablo 14-2"), run_time=0.6)
        self.at(self.cue("son nefes biti", 4.6))
        self.play(FadeIn(hb), FadeIn(hbt), run_time=0.5)
        self.play(Create(zl), FadeIn(ind, shift=DOWN * 0.1), GrowArrow(da), run_time=0.7)
        self.at(self.cue("fiber sorununu", 12.0))
        self.play(FadeIn(f1, shift=UP * 0.1), FadeIn(f2, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(f2, color=GOLD, scale_factor=1.04), run_time=0.6)
        self.at(self.cue("bant genişliği tahsislerini", 18.9))
        self.play(FadeIn(ru, shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("bir ipucudur", 25.0))
        self.play(FadeIn(hint, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g6 — DG qualifies loss reports
        self.beat("g6")
        self.clear(h)
        h = self.show_heading("Son nefes kayıpları niteler", h)
        sw, x0, ys = 1.0, -5.9, 1.05
        slots = VGroup(*[DashedVMobject(Rectangle(width=0.62, height=0.5, stroke_color=TW_US, stroke_width=2), num_dashes=14).move_to([x0 + i * sw, ys, 0]) for i in range(8)])
        got = VGroup(*[Rectangle(width=0.62, height=0.5, stroke_width=0, fill_color=TW_US, fill_opacity=0.75).move_to(slots[i]) for i in range(3)])
        miss = VGroup(*[xmark(slots[i], WARN, 3, -0.08) for i in range(3, 7)])
        st = T("↑ tahsisler (tek ONU)", 15, MUTED).next_to(slots, UP, buff=0.55).align_to(slots, LEFT)
        mb = BraceBetweenPoints(slots[3].get_corner(DL), slots[6].get_corner(DR), DOWN, color=WARN)
        mbt = T("LOBi: 4 ardışık kaçırılmış burst (varsayılan)", 17, WARN, BOLD).next_to(mb, DOWN, buff=0.06)
        dgm = VGroup(RoundedRectangle(corner_radius=0.06, width=0.55, height=0.38, stroke_width=0, fill_color=GOLD, fill_opacity=1), T("DG", 15, BG, BOLD))
        dgm[1].move_to(dgm[0])
        dgm.next_to(got[2], UP, buff=0.1)
        q = VGroup(T("rapor:", 18, MUTED, BOLD), T("DG ile nitelenir", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([4.6, ys, 0])
        grp = VGroup(*[onu_icon("ONU", ONUC, 0.95, 0.45, 14) for _ in range(6)]).arrange(RIGHT, buff=0.22).move_to([-1.7, -1.75, 0])
        gl = T("B tipi · nitelikli LOS (QLOS)", 18, ACC, BOLD).next_to(grp, UP, buff=0.55).align_to(grp, LEFT)
        dgs = VGroup(*[dgm.copy().next_to(grp[i], UP, buff=0.06) for i in (1, 4)])
        ns = pill("birkaç ONU'nun elektriği kesildi → grup anahtarlanmaz", GOOD, 18).move_to([0.6, -2.8, 0])
        self.play(self.set_src("G.989.3 Tablo 14-2 (LOBi) · Tablo 18-3 (QLOS)"), run_time=0.3)
        self.at(self.cue("Burst kaybı varsayılan", 3.5))
        self.play(FadeIn(slots), FadeIn(st), FadeIn(got), run_time=0.6)
        self.play(LaggedStart(*[Create(m) for m in miss], lag_ratio=0.2), FadeIn(mb), FadeIn(mbt), run_time=0.9)
        self.at(self.cue("son nefes bildirimleriyle", 8.8))
        self.play(FadeIn(dgm, shift=DOWN * 0.1), FadeIn(q, shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("B tipi korumadaki", 14.2))
        self.play(FadeIn(gl), LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in grp], lag_ratio=0.1), run_time=0.8)
        self.at(self.cue("elektriği kesildi", 21.3))
        self.play(FadeIn(dgs, shift=DOWN * 0.1), grp[1].animate.set_opacity(0.4), grp[4].animate.set_opacity(0.4), run_time=0.5)
        self.play(FadeIn(ns, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g7 — case 3: rogue ONU in time and in wavelength
        self.beat("g7")
        self.clear(h)
        h = self.show_heading("Vaka 3 · Başıboş ONU", h)
        tg = case_tag(3).move_to([-5.6, 1.95, 0])
        lp = RoundedRectangle(corner_radius=0.16, width=6.4, height=3.9, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([-3.35, -0.55, 0])
        rp = RoundedRectangle(corner_radius=0.16, width=6.4, height=3.9, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([3.35, -0.55, 0])
        lt = T("zaman alanı", 20, TXT, BOLD).move_to(lp.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        rt = T("dalga boyu alanı · NG-PON2'ye özgü", 20, GOLD, BOLD).move_to(rp.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        yt = 0.15
        tax = Arrow([-6.2, yt - 0.3, 0], [-0.5, yt - 0.3, 0], buff=0, color=MUTED, stroke_width=2, tip_length=0.12)
        sl = VGroup(*[VGroup(Rectangle(width=1.1, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.7), T(n, 15, BG, BOLD)) for n, c in (("A", CH[0]), ("B", CH[1]), ("C", CH[2]), ("D", CH[3]))])
        for i, s in enumerate(sl):
            s[0].move_to([-5.5 + i * 1.35, yt, 0])
            s[1].move_to(s[0])
        rog = VGroup(Rectangle(width=1.1, height=0.5, stroke_color=WARN, stroke_width=2.5, fill_color=CH[1], fill_opacity=0.5), T("B", 15, BG, BOLD))
        rog.move_to(sl[2]).shift(RIGHT * 0.5 + UP * 0.12)
        rog[1].move_to(rog[0])
        tdf = VGroup(tag("LOBi", WARN, 16), tag("TIWi", WARN, 16)).arrange(RIGHT, buff=0.2).move_to([-4.6, -1.0, 0])
        t3 = T("3 × Ranging_Time sonrası hâlâ kayıyor → TIWi", 16, TXT).move_to([-3.35, -1.65, 0])
        fit(t3, 5.9)
        lax = Line([0.6, -0.475, 0], [6.1, -0.475, 0], color=MUTED, stroke_width=2)
        chs = VGroup(*[Rectangle(width=1.05, height=1.25, stroke_color=CH[i], stroke_width=2, fill_color=CH[i], fill_opacity=0.12).move_to([1.3 + i * 1.35, 0.15, 0]) for i in range(4)])
        chl = VGroup(*[T(f"λ{i + 1}", 15, CH[i], BOLD).next_to(c, DOWN, buff=0.08).shift(DOWN * 0.08) for i, c in enumerate(chs)])
        lb = lobe(lambda v: v, chs[1].get_x(), -0.475, 0.8, 0.12, TW_US, op=0.4)
        hop = CurvedArrow(np.array([chs[1].get_x(), 0.5, 0]), np.array([chs[3].get_x(), 0.5, 0]), angle=-0.6, color=WARN, stroke_width=3, tip_length=0.14)
        hb_ = T("(b) yanlış kanala atlar", 17, WARN, BOLD).move_to([3.35, -1.3, 0])
        hc = T("(c) yanlış kanala ayarlanır", 17, WARN, BOLD).move_to([3.35, -1.7, 0])
        sref = T("G.989.3 §19.1 a / b / c", 14, MUTED).move_to([3.35, -2.2, 0])
        self.play(FadeIn(tg, shift=RIGHT * 0.1), self.set_src("G.989.3 §19.1 · Tablo 14-2 · Tablo 13-1"), run_time=0.4)
        self.at(self.cue("yanlış dilimde", 1.7))
        self.play(FadeIn(lp), FadeIn(lt), GrowArrow(tax), FadeIn(sl), run_time=0.7)
        self.play(FadeIn(rog, shift=RIGHT * 0.3), Indicate(sl[2], color=WARN), run_time=0.8)
        self.at(self.cue("burst kaybı ve zamanlama", 5.6))
        self.play(FadeIn(tdf, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("üç düzeltme denemesinden", 10.2))
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yeni bir türü vardır", 16.0))
        self.play(FadeIn(rp), FadeIn(rt), Create(lax), FadeIn(chs), FadeIn(chl), FadeIn(lb), FadeIn(sref), run_time=0.8)
        self.at(self.cue("yanlış kanala atlayabilir", 21.8))
        self.play(Create(hop), lb.animate.move_to([chs[3].get_x(), lb.get_y(), 0]), FadeIn(hb_), run_time=0.9)
        self.at(self.cue("yanlış kanala ayarlanabilir", 24.6))
        self.play(FadeIn(hc), run_time=0.4)
        self.end(pad=0.05)

        # g8 — the physical defence
        self.beat("g8")
        self.clear(h)
        h = self.show_heading("Fiziksel savunma — G.989.2", h)
        ya = -1.95
        axg, X = lin_axis(-150, 150, -6.2, 0.8, ya, [-150, -100, -50, 0, 50, 100, 150], size=14,
                          fmt=lambda v: "C" if v == 0 else ("+" if v > 0 else "−") + str(abs(int(v))), unit="↑ kanal merkezine göre (GHz)")
        mpts = [[X(-150), ya + 0.7, 0], [X(-60), ya + 0.7, 0], [X(-60), ya + 2.6, 0], [X(60), ya + 2.6, 0], [X(60), ya + 0.7, 0], [X(150), ya + 0.7, 0]]
        mask = DashedVMobject(VMobject(stroke_color=WARN, stroke_width=3).set_points_as_corners(mpts), num_dashes=60)
        mt = VGroup(T("kanal dışı PSD maskesi", 16, WARN, BOLD), tag("şekil temsili", MUTED, 14)).arrange(DOWN, aligned_edge=RIGHT, buff=0.1).move_to([X(-66), ya + 1.35, 0], aligned_edge=RIGHT)
        mse = Rectangle(width=X(20) - X(-20), height=2.3, stroke_width=0, fill_color=GOOD, fill_opacity=0.14).move_to([X(0), ya + 1.15, 0])
        mst = T("MSE ±20 GHz", 15, GOOD, BOLD).next_to(mse, UP, buff=0.05)
        lb = lobe(X, -20, ya, 1.9, 6, TW_US, op=0.35)
        c1 = card("§9.3.7", "ayar süresince bütün\nspesifikasyonlar sağlanmalı", None, GOLD, w=5.2, h=1.35, tsize=19, bsize=17).move_to([4.0, 1.35, 0])
        c2 = card("§9.3.9", "maske, MSE içinde her konumda\nsağlanmalı", None, WARN, w=5.2, h=1.35, tsize=19, bsize=17).move_to([4.0, -0.15, 0])
        c3 = card("OLT: DOTXi (Tablo 14-2)", "düzeltme isteklerinin sayısı / genliği\n> yapılandırılmış eşik → kusur", None, ACC, w=5.2, h=1.35, tsize=19, bsize=17).move_to([4.0, -1.65, 0])
        self.at(self.cue("ayar süresince bütün", 3.2))
        self.play(FadeIn(c1, shift=LEFT * 0.1), self.set_src("G.989.2 §9.3.7 · §9.3.9 · G.989.3 Tablo 14-2"), run_time=0.6)
        self.at(self.cue("kanal dışı güç maskesi", 7.6))
        self.play(Create(axg[0]), FadeIn(axg[1:]), Create(mask), FadeIn(mt), run_time=0.8)
        self.at(self.cue("spektral sapma aralığının", 9.7))
        self.play(FadeIn(mse), FadeIn(mst), FadeIn(lb), FadeIn(c2, shift=LEFT * 0.1), run_time=0.6)
        self.play(lb.animate.shift(RIGHT * (X(20) - X(-20))), run_time=1.6, rate_func=there_and_back)
        self.at(self.cue("Dalga boyu kayması ise", 16.5))
        self.play(FadeIn(c3, shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("eşikleri aştığında", 22.0))
        self.play(Indicate(c3, color=ACC, scale_factor=1.03), run_time=0.7)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_labB")


class E10LabC(Act10):
    HDR, MANIFEST, PREV_BADGE = H10["L"], M10("lab"), "saha"

    def construct(self):
        # g9 — emergency stop
        self.beat("g9")
        h = self.show_heading("Son çare: acil durdurma")
        olt = sbox("OLT", "Disable_Serial_Number", OLTC, 3.0, 0.95, 20, 15).move_to([-4.9, 1.2, 0])
        o1 = pill("0xFF · tek seri numarası", WARN, 17)
        o2 = pill("0x0F · kanala ayarlı bütün ONU'lar", WARN, 17)
        os_ = VGroup(o1, o2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(olt, DOWN, buff=0.3).align_to(olt, LEFT)
        onu = VGroup(RoundedRectangle(corner_radius=0.12, width=2.4, height=1.1, stroke_color=WARN, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), T("ONU · O7", 20, TXT, BOLD),
                     VGroup(T("Tx", 15, MUTED, BOLD), lamp(True, 0.1)).arrange(RIGHT, buff=0.12))
        onu[1].move_to(onu[0]).shift(UP * 0.2)
        onu[2].move_to(onu[0]).shift(DOWN * 0.25)
        onu.move_to([-0.6, 1.2, 0])
        ar = arrow(olt.get_right(), onu.get_left(), WARN, 2.5, 0.14)
        rb = VGroup(tag("yeniden başlatma: durum korunur", WARN, 16)).next_to(onu, DOWN, buff=0.25)
        K = 0.17
        bars = VGroup()
        x = 1.9
        for i, wv in enumerate([1, 2, 4, 8, 16]):
            r = Rectangle(width=0.42, height=wv * K + 0.05, stroke_width=0, fill_color=GOLD, fill_opacity=0.8).move_to([x + i * 0.62, -2.5 + (wv * K + 0.05) / 2, 0])
            bars.add(r)
        cap = DashedLine([1.7, -2.5 + 16 * K + 0.05, 0], [5.0, -2.5 + 16 * K + 0.05, 0], color=WARN, stroke_width=2)
        capt = T("≈ 1 dk", 20, WARN, BOLD).next_to(cap, RIGHT, buff=0.15)
        bl = T("her başarısız tarama turunda bekleme × 2", 17, GOLD, BOLD).move_to([3.4, -2.85, 0])
        scan = VGroup(T("yeniden başlayınca: kanalları tarar", 18, TXT, BOLD), T("Ek XI (bilgilendirici): O7.2", 15, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-3.6, -1.45, 0])
        self.at(self.cue("tek bir seri numarasını", 2.2))
        self.play(FadeIn(olt), FadeIn(o1, shift=UP * 0.1), self.set_src("G.989.3 §11.3.3.5 · Tablo 12-1 (O7) · Ek XI · §12.1.5"), run_time=0.6)
        self.at(self.cue("kanala ayarlı bütün", 4.5))
        self.play(FadeIn(o2, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("vericisini kapatır", 9.3))
        self.play(GrowArrow(ar), FadeIn(onu), run_time=0.5)
        self.play(Transform(onu[2][1], lamp(False, 0.1).move_to(onu[2][1])), run_time=0.5)
        self.at(self.cue("yeniden başlatmada bile", 12.2))
        self.play(FadeIn(rb, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("kanalları tarar", 15.8))
        self.play(FadeIn(scan, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ikiye katlayarak", 19.7))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), FadeIn(bl), run_time=1.2)
        self.play(Create(cap), FadeIn(capt), run_time=0.5)
        self.end(pad=0.05)

        # g10 — global disable, then one by one
        self.beat("g10")
        self.clear(h)
        h = self.show_heading("Toplu başıboşluk: küresel devre dışı", h)
        ons = VGroup(*[onu_icon(f"ONU {i + 1}", ONUC, 1.3, 0.6, 16) for i in range(8)]).arrange(RIGHT, buff=0.2).move_to([0, 0.6, 0])
        p1 = pill("1 · hepsi devre dışı", WARN, 18).move_to([-3.3, -0.75, 0])
        p2 = pill("2 · uyumlular tek tek geri", GOOD, 18).move_to([2.6, -0.75, 0])
        bad = 5
        culprit = T("suçlu", 20, WARN, BOLD).next_to(ons[bad], DOWN, buff=0.2)
        sysm = pill("sahada suçluyu bulmanın sistematik yolu", GOLD, 20).move_to([0, -2.4, 0])
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in ons], lag_ratio=0.06), self.set_src("G.989.3 §12.1.5"), run_time=0.8)
        self.at(self.cue("küresel olarak", 2.9))
        self.play(*[o[0].animate.set_stroke(WARN, 3) for o in ons], FadeIn(p1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("tek tek yeniden", 7.5))
        self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.3)
        for i in range(8):
            if i != bad:
                self.play(ons[i][0].animate.set_stroke(GOOD, 3), run_time=0.28)
        self.at(self.cue("suçluyu bulmanın", 11.4))
        self.play(FadeIn(culprit, shift=UP * 0.1), Indicate(ons[bad], color=WARN, scale_factor=1.1), FadeIn(sysm, shift=UP * 0.1), run_time=0.7)
        self.end(pad=0.05)

        # g11 — case 4: power levelling has no effect
        self.beat("g11")
        self.clear(h)
        h = self.show_heading("Vaka 4 · Güç dengeleme yanıt vermiyor", h)
        tg = case_tag(4, PINK).move_to([-5.6, 1.95, 0])
        xo, xu = -5.3, -1.6
        lo = VGroup(sbox("OLT", None, OLTC, 1.4, 0.55, 18).move_to([xo, 1.15, 0]), DashedLine([xo, 0.85, 0], [xo, -1.35, 0], color=MUTED, stroke_width=2))
        lu = VGroup(sbox("ONU", None, ONUC, 1.4, 0.55, 18).move_to([xu, 1.15, 0]), DashedLine([xu, 0.85, 0], [xu, -1.35, 0], color=MUTED, stroke_width=2))
        m1 = VGroup(arrow([xo, 0.45, 0], [xu, 0.45, 0], GOLD, 2.5, 0.14), T("Change_Power_Level", 15, GOLD, BOLD).move_to([(xo + xu) / 2, 0.65, 0]))
        m2 = VGroup(arrow([xu, -0.25, 0], [xo, -0.25, 0], GOOD, 2.5, 0.14), T("onay (ACK)", 15, GOOD, BOLD).move_to([(xo + xu) / 2, -0.05, 0]))
        px0, px1, py = 0.4, 6.4, -0.6
        pax = VGroup(Line([px0, py, 0], [px1, py, 0], color=MUTED, stroke_width=2), Line([px0, py, 0], [px0, py + 1.9, 0], color=MUTED, stroke_width=2),
                     T("OLT'de alınan güç", 15, MUTED).next_to([px0, py + 1.9, 0], RIGHT, buff=0.1), T("zaman", 14, MUTED).next_to([px1, py, 0], DOWN, buff=0.08).shift(LEFT * 0.3))
        exp = DashedVMobject(VMobject(stroke_color=GOLD, stroke_width=2.5).set_points_as_corners([[px0 + 0.1, py + 1.3, 0], [3.2, py + 1.3, 0], [3.2, py + 0.65, 0], [px1 - 0.1, py + 0.65, 0]]), num_dashes=40)
        expt = T("beklenen", 15, GOLD, BOLD).move_to([5.0, py + 0.42, 0])
        meas = Line([px0 + 0.1, py + 1.3, 0], [px1 - 0.1, py + 1.3, 0], color=TW_US, stroke_width=3.5)
        meast = T("ölçülen: değişmedi", 15, TW_US, BOLD).move_to([4.9, py + 1.55, 0])
        al = pill("ALRFi kusuru (Tablo 14-2)", WARN, 19).move_to([3.4, -1.35, 0])
        c1 = card("neden 1", "ONU'nun zayıflatıcısı çalışmıyor", None, PINK, w=5.6, h=1.0, tsize=18, bsize=17).move_to([-3.3, -2.45, 0])
        c2 = card("neden 2", "OLT ölçümü yeterince uzun burst'te değil (Ek II Not 3)", None, ACC, w=6.4, h=1.0, tsize=18, bsize=16).move_to([3.3, -2.45, 0])
        self.play(FadeIn(tg, shift=RIGHT * 0.1), FadeIn(lo), FadeIn(lu), self.set_src("G.989.3 §11 (Change_Power_Level) · Tablo 14-2 · G.989.2 Ek II"), run_time=0.6)
        self.at(self.cue("gücünü değiştirmesini", 3.3))
        self.play(GrowArrow(m1[0]), FadeIn(m1[1]), run_time=0.5)
        self.at(self.cue("ONU onaylar", 7.0))
        self.play(GrowArrow(m2[0]), FadeIn(m2[1]), run_time=0.5)
        self.at(self.cue("gelen güç değişmez", 8.0))
        self.play(Create(pax[:2]), FadeIn(pax[2:]), Create(exp), FadeIn(expt), Create(meas), FadeIn(meast), run_time=0.9)
        self.at(self.cue("ayrı bir kusur", 10.5))
        self.play(FadeIn(al, scale=0.9), run_time=0.5)
        self.at(self.cue("zayıflatıcısı çalışmıyordur", 15.4))
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ya da OLT'nin", 18.4))
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g12 — counters to pull
        self.beat("g12")
        self.clear(h)
        h = self.show_heading("Toplanacak sayaçlar — Tablo 14-1", h)
        names = [("FEC", "düzeltilen / düzeltilemeyen kod sözcüğü", TW_DS), ("BIP-32", "hatalar (FEC kapalıyken)", TW_DS), ("LODS", "olaylar + nasıl geri geldi", STATE),
                 ("λ düzeltme", "Adjust_Tx_Wavelength genliği", CH[2]), ("son nefes", "DG sayısı", GOLD), ("güç değişimi", "Change_Power_Level retleri", PINK)]
        tiles = VGroup()
        for a, b, c in names:
            r = RoundedRectangle(corner_radius=0.12, width=4.15, height=1.05, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            g = VGroup(T(a, 20, c, BOLD), tf(b, 16, TXT, w=3.8)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.22)
            tiles.add(VGroup(r, g))
        tiles.arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.25)).move_to([0, 0.95, 0])
        snap = RoundedRectangle(corner_radius=0.16, width=12.9, height=1.35, stroke_color=WARN, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([0, -1.75, 0])
        snt = T("olay sonrası: acil durum anlık görüntüsü (§14.2.3)", 20, WARN, BOLD).move_to(snap.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        sn = VGroup(tag("ONU kalıcı belleği", MUTED, 16), tag("son nefes sırasında alınır", GOLD, 16), tag("≥ 10 kayıt", GOOD, 16)).arrange(RIGHT, buff=0.25)
        sn.next_to(snt, DOWN, buff=0.16, aligned_edge=LEFT)
        self.play(self.set_src("G.989.3 Tablo 14-1 · §14.2.3"), run_time=0.3)
        for i, (key, d) in enumerate((("FEC ile düzeltilen", 1.7), ("BIP-32", 6.0), ("senkron kaybı olayları", 8.6), ("dalga boyu düzeltme", 12.7), ("son nefes sayısı", 15.0),
                                      ("güç değişimi retleri", 16.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(tiles[i], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Olay sonrası analiz", 18.4))
        self.play(FadeIn(snap), FadeIn(snt), FadeIn(sn[0]), run_time=0.6)
        self.at(self.cue("son nefes sırasında", 25.4))
        self.play(FadeIn(sn[1], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("en az on kayıt", 27.7))
        self.play(FadeIn(sn[2], shift=RIGHT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # g13 — field note
        self.beat("g13")
        self.clear()
        self.set_badge("not")
        hd = T("Saha notu: standardın sayı vermediği yerler", 30, TXT, BOLD).next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
        n1 = self.ncard("1", "OLT koruma anahtarlama süresi", "standartta değer yok → kendi ağınızda ölçün ve belgeleyin", h=1.6)
        n2 = self.ncard("2", "ONU'nun yeniden ayar sabrı (TO2 / TO3)", "standartta değer yok → ölçün ve belgeleyin", h=1.6)
        ns = VGroup(n1, n2).arrange(DOWN, buff=0.3).move_to([0, 0.05, 0])
        cust = pill("tanımsız — ama müşteriniz ikisini de hisseder", GOLD, 20).move_to([0, -2.6, 0])
        self.play(FadeIn(hd, shift=RIGHT * 0.2), run_time=0.5)
        self.at(self.cue("OLT'nin koruma", 6.9))
        self.play(FadeIn(n1, shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("yeniden ayara karar", 9.7))
        self.play(FadeIn(n2, shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("müşteriniz ikisini", 15.9))
        self.play(FadeIn(cust, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.2)
        self.clear()
        self.drop_badge()
        self.save_timeline("ep10_labC")


# =================================== KAPANIŞ ======================================
POINTS = [("NG-PON2: aynı ODN'de 4 ya da 8 TWDM kanal çifti + PtP WDM hatları", [1, 3, 9]),
          ("ODN sınıfını OLT taşır; ONU alıcısı her sınıfta aynı pencereyi görür", [2, 4, 5]),
          ("Ayarlanabilir verici ve alıcı: sistemin hem gücü hem en büyük riski", [5, 7]),
          ("↑ her burst sıfırdan edinilir; güç dengeleme ve X/S kalabalığı yönetir", [5, 6, 8]),
          ("Sahada her şey ölçülür — ama doğruluk sınırlarıyla okunur", [10]),
          ("Koruma ve kanal yönetimi TC'de; ama optiğin hızına ve temizliğine bağlı", [7, 10])]
S2 = [("çerçeveleme · XGEM", "§8 · §9"), ("PLOAM · OMCI", "§11 · §6.1.4.3"), ("dinamik bant genişliği (DBA)", "§7"), ("aktivasyon · mesafe ölçümü", "§12 · §13"),
      ("kanal yönetimi · ayar dizileri", "§17 · Ek F"), ("güvenlik", "§15"), ("güç yönetimi", "§16"), ("koruma", "§18")]


class E10End(Act10):
    HDR, MANIFEST, FIRST = H10["E"], M10("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Sezonun özeti")
        self.at(1.2)
        self.to_header(tc)
        self.set_badge("ozet")
        eps = VGroup()
        for e in SERIES["episodes"]:
            r = RoundedRectangle(corner_radius=0.12, width=2.48, height=0.92, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
            g = VGroup(T(f"B{e['n']}", 16, ACC, BOLD), tf(e["title"], 17, TXT, BOLD, w=2.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.15)
            eps.add(VGroup(r, g))
        eps.arrange_in_grid(rows=2, cols=5, buff=(0.14, 0.16)).move_to([0, 1.75, 0])
        pts = VGroup(*[VGroup(T(f"{i + 1}", 26, ACC, BOLD), T(s, 21, TXT)).arrange(RIGHT, buff=0.3) for i, (s, _) in enumerate(POINTS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        for p in pts:
            fit(p, 12.6)
        pts.move_to([0, -1.6, 0]).to_edge(LEFT, buff=0.9)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in eps], lag_ratio=0.06), run_time=1.0)

        def light(k):
            on = POINTS[k][1]
            anims = []
            for i, e in enumerate(eps):
                c = ACC if (i + 1) in on else LINE
                anims += [e[0].animate.set_stroke(c, 3 if (i + 1) in on else 2), e[1].animate.set_opacity(1 if (i + 1) in on else 0.45)]
            return anims
        for k, (key, d) in enumerate((("NG-PON2,", 1.5), ("ODN sınıfını OLT", 11.2), ("ayarlanabilir verici ve alıcı", 17.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(pts[k], shift=RIGHT * 0.2), *light(k), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((3, 4, 5), (("yukarı yönde her burst", 0.4), ("sahada her şey", 10.1), ("koruma ve kanal yönetimi", 16.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(pts[k], shift=RIGHT * 0.2), *light(k), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("B tipi korumada ONU neden\nyeniden ayarlanmaz? Etkili\nolması için hangi koşul\ngerekir?", CH[0]),
            ("OLT'nin alınan güç ölçümü\nneden burst'ün uzunluğuna\nbağlıdır?", CH[1]),
            ("Acil durdurmadaki bir ONU,\ngücü kesilip geri gelince\nne yapar?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: 2. sezonun ilk bölümünün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 9.5), ("Üçüncü soru", 16.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("ikinci sezonun ilk", 24.7))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — season 2 preview
        self.beat("h4")
        self.clear()
        self.drop_badge()
        top = VGroup(T("SEZON 2", 22, ACC, BOLD), T("G.989.3 — iletim yakınsama (TC) katmanı", 40, TXT, BOLD)).arrange(DOWN, buff=0.2).move_to(UP * 2.05)
        fit(top[1], 12.6)
        chips = VGroup()
        for i, (a, b) in enumerate(S2):
            r = RoundedRectangle(corner_radius=0.14, width=3.0, height=1.0, stroke_color=CH[i % 4], stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            g = VGroup(tf(a, 18, TXT, BOLD, w=2.75), T(b, 15, CH[i % 4], SEMIBOLD)).arrange(DOWN, buff=0.08).move_to(r)
            chips.add(VGroup(r, g))
        chips.arrange_in_grid(rows=2, cols=4, buff=(0.2, 0.22)).move_to([0, -0.05, 0])
        l1 = VGroup(T("Sezon 1:", 22, MUTED, BOLD), T("ışığın kendisi (G.989.2)", 22, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        l2 = VGroup(T("Sezon 2:", 22, ACC, BOLD), T("ışığın taşıdığı dil (G.989.3)", 22, ACC, BOLD)).arrange(RIGHT, buff=0.2)
        ls = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, -2.45, 0])
        self.play(FadeIn(top[0]), Write(top[1]), run_time=1.2)
        keys = [("çerçeveleme ve XGEM", 5.2, [0]), ("PLOAM ve OMCI", 6.9, [1]), ("dinamik bant", 9.0, [2]), ("aktivasyon ve mesafe", 11.6, [3]),
                ("kanal yönetimi ve ayar", 14.0, [4]), ("güvenlik,", 16.7, [5]), ("güç yönetimi ve koruma", 17.4, [6, 7])]
        for key, d, ix in keys:
            self.at(self.cue(key, d))
            self.play(*[FadeIn(chips[i], shift=UP * 0.12) for i in ix], run_time=0.4)
        self.at(self.cue("Bu sezon ışığın", 19.4))
        self.play(FadeIn(l1, shift=RIGHT * 0.15), run_time=0.5)
        self.at(self.cue("gelecek sezon", 22.3))
        self.play(FadeIn(l2, shift=RIGHT * 0.15), run_time=0.5)
        self.end(pad=0.1)

        # h5 — end of season 1, then credits
        self.beat("h5")
        self.play(FadeOut(top), FadeOut(chips), FadeOut(ls), FadeOut(self.hdr), run_time=0.6)
        fin = VGroup(T("LAMBDA", 72, ACC, BOLD), T("Sezon 1 sonu", 40, TXT, BOLD), T("İzlediğiniz için teşekkürler · görüşmek üzere", 24, MUTED)).arrange(DOWN, buff=0.3)
        lam = VGroup(*[Line([-1.6 + 0.32 * i, -1.9, 0], [-1.6 + 0.32 * i, -1.4, 0], color=CH[i % 4], stroke_width=5) for i in range(11)]).next_to(fin, DOWN, buff=0.45)
        self.play(FadeIn(fin[0], scale=0.9), run_time=0.8)
        self.play(FadeIn(fin[1], shift=UP * 0.15), LaggedStart(*[Create(l) for l in lam], lag_ratio=0.08), run_time=1.0)
        self.at(self.cue("İzlediğiniz için", 3.4))
        self.play(FadeIn(fin[2], shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.6)
        self.play(FadeOut(fin), FadeOut(lam), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Bölüm {EP10['n']} · {EP10['title']}", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Coqui XTTS-v2 — ses: Damien Black (yerel GPU)", 22, ACC, BOLD),
                    T("(Coqui Public Model License — ticari olmayan kullanım)", 18, ACC),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep10_end")
