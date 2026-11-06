"""B03 · Perde 1 (spektrum haritası) and Perde 2 (komşular)."""
from ep03_common import *

DS_THZ = [187.8, 187.7, 187.6, 187.5, 187.4, 187.3, 187.2, 187.1]


class E3P1A(Act3):
    HDR, MANIFEST, FIRST = H3[1], M3("p1"), True

    def construct(self):
        self.beat("b1")
        tc = self.title_card("PERDE 1", "Spektrum haritası")
        self.at(self.cue("bu fiberde", 2))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Tablo 9-1 — NG-PON2 dalga boyu bantları")
        q = pill("bu fiberde başka hangi ışıklar var?", GOLD, 22).move_to(UP * 0.9)
        axg, X = nm_axis(1515, 1635, y=-2.0, step=5, label_every=20)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Tablo dokuz", 5))
        self.play(FadeOut(q), Create(axg[0]), FadeIn(axg[1:]), self.set_src("G.989.2 §9.2, Tablo 9-1"), run_time=0.9)
        self.end(pad=0.05)

        self.beat("b2")
        ds = band(X, 1596, 1603, -1.45, 0.7, TW_DS, None)
        dsl = VGroup(T("TWDM ↓", 20, TW_DS, BOLD), T("1596–1603 nm", 17, TW_DS)).arrange(DOWN, buff=0.06).next_to(ds, UP, buff=0.15)
        lb = BraceBetweenPoints([X(1565), 1.15, 0], [X(1625), 1.15, 0], UP, color=MUTED)
        lbt = T("L bandı", 17, MUTED).next_to(lb, UP, buff=0.05)
        zoom = VGroup(*[Line([X(1596) + (X(1603) - X(1596)) * (thz_to_nm(f) - 1596) / 7, -1.1, 0], [X(1596) + (X(1603) - X(1596)) * (thz_to_nm(f) - 1596) / 7, -1.8, 0], color=BG, stroke_width=1.5) for f in DS_THZ])
        n8 = T("8 kanal × 100 GHz", 18, TW_DS, BOLD).next_to(dsl, RIGHT, buff=0.35).align_to(dsl, DOWN)
        self.play(GrowFromEdge(ds, DOWN), FadeIn(dsl), run_time=0.8)
        self.play(FadeIn(lb), FadeIn(lbt), run_time=0.5)
        self.at(self.cue("sekiz kanalı", 6))
        self.play(Create(zoom), FadeIn(n8), run_time=0.7)
        self.end(pad=0.05)

        self.beat("b2b")
        self.set_badge("fiz")
        cost = VGroup(T("L bandının bedeli", 22, WARN, BOLD), T("G.652: D ≈ 21 ps/nm/km (Bölüm 2)", 19, TXT),
                      T("→ 10G ↓ OPP = 2 dB (Tablo 11-5)", 19, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        box_ = RoundedRectangle(corner_radius=0.15, width=cost.width + 0.6, height=cost.height + 0.45, stroke_color=WARN, stroke_width=2, fill_color=PANEL, fill_opacity=1)
        cb = VGroup(box_, cost.move_to(box_)).move_to([-2.4, 0.45, 0])
        self.play(FadeIn(cb, shift=UP * 0.15), run_time=0.7)
        self.end(pad=0.05)

        self.beat("b2a")
        self.set_badge("std")
        self.play(FadeOut(cb), run_time=0.4)
        opts = [(1524, 1544, "geniş 1524–1544", 1.0, -1.45), (1528, 1540, "azaltılmış 1528–1540", 0.7, -0.75), (1532, 1540, "dar 1532–1540", 0.5, -0.05)]
        us = VGroup()
        for a, b_, lab, op, y in opts:
            r = band(X, a, b_, y, 0.5, TW_US, None, op=op)
            us.add(VGroup(r, T(lab + " nm", 17, TW_US, BOLD).next_to(r, RIGHT, buff=0.2)))
        ust = T("TWDM ↑ — üç seçenek", 20, TW_US, BOLD).move_to([X(1534), 0.7, 0])
        cb2 = BraceBetweenPoints([X(1530), 1.15, 0], [X(1565), 1.15, 0], UP, color=MUTED)
        cbt = T("C bandı", 17, MUTED).next_to(cb2, UP, buff=0.05)
        self.play(FadeIn(cb2), FadeIn(cbt), FadeIn(ust), run_time=0.5)
        for k, key in enumerate(["Geniş", "Azaltılmış", "Dar bant"]):
            self.at(self.cue(key, 2 + 3 * k))
            self.play(GrowFromEdge(us[k][0], LEFT), FadeIn(us[k][1]), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p1A")


class E3P1B(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[1], M3("p1"), "std"

    def construct(self):
        self.beat("b3")
        self.set_badge("fiz")
        h = self.show_heading("Bant genişliği × kanal aralığı")
        k, x0, y = 0.0052, -5.6, -0.2
        nb = Rectangle(width=1017 * k, height=1.3, stroke_color=TW_US, stroke_width=2.5, fill_color=TW_US, fill_opacity=0.12).move_to([x0 + 1017 * k / 2, y, 0])
        nbt = T("dar bant 1532–1540 nm ≈ 1,02 THz", 19, TW_US, BOLD).next_to(nb, UP, buff=0.12).align_to(nb, LEFT)
        lines = VGroup(*[Line([x0 + (25 + 200 * i) * k, y - 0.55, 0], [x0 + (25 + 200 * i) * k, y + 0.55, 0], color=CH[i % 4], stroke_width=3.5) for i in range(8)])
        over = Rectangle(width=(1450 - 1017) * k, height=1.3, stroke_width=0, fill_color=WARN, fill_opacity=0.25).move_to([x0 + (1017 + 1450) / 2 * k, y, 0])
        ovt = T("8 × 200 GHz + 2·MSE ≈ 1,45 THz  ✗", 21, WARN, BOLD).next_to(nb, DOWN, buff=0.35).align_to(nb, LEFT)
        self.play(Create(nb), FadeIn(nbt), run_time=0.7)
        self.at(self.cue("İki yüz", 6))
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.15), run_time=1.4)
        self.play(FadeIn(over), FadeIn(ovt), run_time=0.6)
        self.end(pad=0.05)

        self.beat("b3a")
        self.clear(h)
        h = self.show_heading("Ek VIII örnek ızgaraları (Tablo VIII.5)", h)
        axg, X = nm_axis(1526, 1542, y=-2.0, step=1, label_every=2)
        red = outline_band(X, 1528, 1540, 0.35, 0.7, TW_US, "azaltılmış bant 1528–1540  ·  200 GHz ızgara: 1528,8 … 1539,8 nm", lsize=16)
        nar = outline_band(X, 1532, 1540, -1.05, 0.7, GOLD, "dar bant 1532–1540  ·  50 GHz ızgara ≈ 2,8 nm", lsize=16, where="down")
        g200 = comb(X, [thz_to_nm(f) for f in (196.1, 195.9, 195.7, 195.5, 195.3, 195.1, 194.9, 194.7)], 0.35, 0.5, TW_US, 3)
        g50 = comb(X, [thz_to_nm(f) for f in (195.25, 195.2, 195.15, 195.1, 195.05, 195.0, 194.95, 194.9)], -1.05, 0.5, GOLD, 2.5)
        self.play(Create(axg[0]), FadeIn(axg[1:]), Create(red[0]), FadeIn(red[1]), self.set_src("G.989.2 Ek VIII.4, Tablo VIII.5"), run_time=0.8)
        self.play(LaggedStart(*[Create(l) for l in g200], lag_ratio=0.1), run_time=1.0)
        self.at(self.cue("Elli gigahertz", 6))
        self.play(Create(nar[0]), FadeIn(nar[1]), run_time=0.5)
        self.play(LaggedStart(*[Create(l) for l in g50], lag_ratio=0.1), run_time=0.9)
        self.end(pad=0.05)

        self.beat("b4")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Noktadan noktaya WDM (PtP WDM)", h)
        axg, X = nm_axis(1515, 1635, y=-2.0, step=5, label_every=20)
        ghost = VGroup(band(X, 1524, 1544, -1.45, 0.6, TW_US, None, op=0.3), band(X, 1596, 1603, -1.45, 0.6, TW_DS, None, op=0.3))
        sh = band(X, 1603, 1625, -0.6, 0.6, PTP, None)
        sht = T("paylaşılan 1603–1625 nm", 18, PTP, BOLD).next_to(sh, UP, buff=0.1)
        ex = outline_band(X, 1524, 1625, 0.2, 0.6, PTP, "genişletilmiş 1524–1625 nm — bir eski sistem yoksa", lsize=18)
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(ghost), run_time=0.6)
        self.at(self.cue("Paylaşılan", 2))
        self.play(GrowFromEdge(sh, DOWN), FadeIn(sht), run_time=0.6)
        self.at(self.cue("Genişletilmiş", 5))
        self.play(Create(ex[0]), FadeIn(ex[1]), run_time=0.8)
        self.end(pad=0.05)

        self.beat("b4a")
        p1 = pill("genişletilmiş spektrum: G.694.1 / G.698.3 DWDM ızgaraları", ACC, 19)
        p2 = pill("Not 1: boş alt bant serbest — ama yalıtım hesaba katılmalı", WARN, 19)
        ps = VGroup(p1, p2).arrange(DOWN, buff=0.15).move_to([0.4, 1.72, 0])
        self.play(FadeOut(sht), FadeIn(p1, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.cue("Birinci not", 4))
        self.play(FadeIn(p2, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("b5")
        self.clear(h)
        h = self.show_heading("Not 2 — TWDM ile PtP yan yana", h)
        def row(y, gap_label, color, gap=1.1):
            a = Rectangle(width=3.2, height=0.6, stroke_width=0, fill_color=TW_US, fill_opacity=0.85).move_to([-3.2, y, 0])
            b = Rectangle(width=3.2, height=0.6, stroke_width=0, fill_color=PTP, fill_opacity=0.85).move_to([-3.2 + 3.2 + gap, y, 0])
            ga = DoubleArrow(a.get_right(), b.get_left(), buff=0, color=color, stroke_width=2.5, tip_length=0.12)
            return VGroup(a, T("TWDM", 16, BG, BOLD).move_to(a), b, T("PtP WDM", 16, BG, BOLD).move_to(b), ga, T(gap_label, 19, color, BOLD).next_to(b, RIGHT, buff=0.3))
        r1 = row(1.3, "ayrı mux/demux: ≥ 3 nm", GOLD)
        r2 = row(0.2, "tek cihaz: ≥ 100 GHz", ACC, gap=0.6)
        il = VGroup(*[Rectangle(width=0.32, height=0.6, stroke_width=0, fill_color=(TW_US if i % 2 == 0 else PTP), fill_opacity=0.85).move_to([-4.6 + i * 0.4, -0.9, 0]) for i in range(10)])
        x = Cross(il, stroke_color=WARN, stroke_width=5)
        ilt = T("iç içe geçmek yok", 19, WARN, BOLD).next_to(il, RIGHT, buff=0.4)
        sp = T("paylaşılan spektrumda PtP ↑ kanalları kısa dalga boylarında", 19, PTP, BOLD).move_to(DOWN * 2.1)
        self.play(FadeIn(il), run_time=0.4)
        self.play(Create(x), FadeIn(ilt), run_time=0.5)
        self.at(self.cue("Ayrı çoklayıcılar", 3))
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("tek bir cihaz", 5))
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Paylaşılan spektrumda", 8))
        self.play(FadeIn(sp), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p1B")


class E3P1C(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[1], M3("p1"), "std"

    def construct(self):
        self.beat("b6")
        h = self.show_heading("Frekans normatif, dalga boyu bilgi amaçlı")
        l = VGroup(T("187,8 THz", 54, GOOD, BOLD), T("normatif", 22, GOOD)).arrange(DOWN, buff=0.15).move_to([-3.2, 0.4, 0])
        r = VGroup(T("≈ 1596,34 nm", 54, MUTED, BOLD), T("bilgi amaçlı", 22, MUTED)).arrange(DOWN, buff=0.15).move_to([3.2, 0.4, 0])
        eq = T("λ = c / f", 34, GOLD, BOLD).move_to(DOWN * 1.6)
        ar = Arrow(l.get_right(), r.get_left(), buff=0.3, color=MUTED, stroke_width=3)
        self.play(FadeIn(l, shift=UP * 0.2), self.set_src("G.989.2 Tablo 11-2"), run_time=0.7)
        self.play(GrowArrow(ar), FadeIn(r, shift=UP * 0.2), run_time=0.7)
        self.at(self.cue("Standart ızgarayı", 3))
        self.play(Write(eq), run_time=0.8)
        self.end(pad=0.05)

        self.beat("b6a")
        self.play(*[FadeOut(m) for m in (l, r, ar)], eq.animate.move_to(UP * 1.6), run_time=0.5)
        eq2 = T("Δλ = λ² · Δf / c", 30, GOLD, BOLD).next_to(eq, DOWN, buff=0.3)
        k = 5.0
        r1 = VGroup(T("1530 nm", 22, TW_US, BOLD), Rectangle(width=0.78 * k, height=0.45, stroke_width=0, fill_color=TW_US, fill_opacity=0.85), T("100 GHz ≈ 0,78 nm", 20, TW_US)).arrange(RIGHT, buff=0.35)
        r2 = VGroup(T("1600 nm", 22, TW_DS, BOLD), Rectangle(width=0.85 * k, height=0.45, stroke_width=0, fill_color=TW_DS, fill_opacity=0.85), T("100 GHz ≈ 0,85 nm", 20, TW_DS)).arrange(RIGHT, buff=0.35)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 1.0)
        self.play(FadeIn(eq2), run_time=0.5)
        self.at(self.cue("Yüz gigahertz", 2))
        self.play(FadeIn(r1[0]), GrowFromEdge(r1[1], LEFT), FadeIn(r1[2]), run_time=0.7)
        self.play(FadeIn(r2[0]), GrowFromEdge(r2[1], LEFT), FadeIn(r2[2]), run_time=0.7)
        self.end(pad=0.05)

        self.beat("b6b")
        self.clear(h)
        h = self.show_heading("Aşağı yön bandında sekiz kanal", h)
        axg, X = nm_axis(1595.5, 1603.5, y=-2.0, step=1, label_every=1)
        bd = band(X, 1596, 1603, -0.7, 1.6, TW_DS, None, op=0.12)
        nms = [thz_to_nm(f) for f in DS_THZ]
        ch = VGroup(*[Line([X(v), -1.45, 0], [X(v), 0.05, 0], color=TW_DS, stroke_width=3) for v in nms])
        dl = 0.17
        wh = VGroup(*[DoubleArrow([X(v - dl), 0.25, 0], [X(v + dl), 0.25, 0], buff=0, color=GOLD, stroke_width=2, tip_length=0.08) for v in nms])
        wt = T("± 20 GHz ≈ ± 0,17 nm", 17, GOLD, BOLD).next_to(wh, UP, buff=0.12)
        m1 = T("0,34 nm", 16, MUTED).move_to([(X(1596) + X(nms[0])) / 2, -1.75, 0])
        m2 = T("0,69 nm", 16, MUTED).move_to([(X(1603) + X(nms[-1])) / 2, -1.75, 0])
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(bd), run_time=0.6)
        self.play(LaggedStart(*[Create(c) for c in ch], lag_ratio=0.1), run_time=1.0)
        self.at(self.cue("Bandın iki", 3))
        self.play(FadeIn(wh), FadeIn(wt), FadeIn(m1), FadeIn(m2), run_time=0.7)
        self.end(pad=0.05)

        self.beat("b7")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bu bantlar neden tam burada?\nCevap: fiberi paylaştığımız komşularda.")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep03_p1C")


LEG = [(1260, 1280, LEGACY, "XG-PON1 ↑", 0), (1290, 1330, LEGACY, "G-PON ↑", 1), (1480, 1500, LEGACY, "G-PON ↓", 0),
       (1575, 1580, LEGACY, "XG-PON1 ↓", 2)]


class E3P2A(Act3):
    HDR, MANIFEST, FIRST = H3[2], M3("p2"), True

    def construct(self):
        self.beat("c1")
        tc = self.title_card("PERDE 2", "Komşular")
        self.at(self.cue("Standardın", 2))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Ek I — birlikte çalışma")
        sysp = VGroup(pill("G-PON", LEGACY, 20), pill("RF video", VIDEO, 20), pill("XG-PON1", LEGACY, 20), pill("OTDR", MUTED, 20)).arrange(RIGHT, buff=0.3).move_to(UP * 1.6)
        axg, X = nm_axis(1250, 1680, y=-1.9, step=10, label_every=50)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in sysp], lag_ratio=0.2), self.set_src("G.989.2 Ek I · G.984.5 · G.987.2"), run_time=1.0)
        self.play(Create(axg[0]), FadeIn(axg[1:]), run_time=0.7)
        self.end(pad=0.05)

        self.beat("c2")
        self.play(FadeOut(sysp), run_time=0.4)
        bands = VGroup()
        for a, b, c, lab, up in LEG:
            g = band(X, a, b, -1.35, 0.6, c, None, op=0.9)
            g.add(T(lab, 15, TXT, BOLD).next_to(g[0], UP, buff=0.1 + 0.32 * up))
            bands.add(g)
        for k, key in enumerate(["G-PON aşağı", "Yukarı yönde", "XG-PON1 ise", "aşağı yönde bin beş yüz yetmiş"]):
            self.at(self.cue(key, 1 + 3 * k))
            idx = [2, 1, 0, 3][k]
            self.play(GrowFromEdge(bands[idx][0], DOWN), FadeIn(bands[idx][1]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c2b")
        old = outline_band(X, 1260, 1360, 0.6, 0.5, WARN, "G-PON ↑ ilk tanım 1260–1360", lsize=15)
        new = T("→ birlikte çalışma için 1290–1330 nm", 17, GOOD, BOLD).next_to(old, RIGHT, buff=0.25)
        self.play(Create(old[0]), FadeIn(old[1]), run_time=0.7)
        self.at(self.cue("XG-PON1'in", 3))
        self.play(Indicate(bands[0], color=WHITE), run_time=0.7)
        self.at(self.cue("daraltıldı", 5))
        self.play(FadeIn(new), Indicate(bands[1], color=GOOD), run_time=0.8)
        self.end(pad=0.05)
        self.play(FadeOut(old), FadeOut(new), run_time=0.4)

        self.beat("c2a")
        vid = band(X, 1550, 1560, -1.35, 0.6, VIDEO, None)
        vt = T("RF video", 15, VIDEO, BOLD).next_to(vid, UP, buff=0.42).shift(RIGHT * 0.45)
        ot = outline_band(X, 1625, 1675, -1.35, 0.6, MUTED, "OTDR · U bandı (L.313)", lsize=15)
        self.play(GrowFromEdge(vid, DOWN), FadeIn(vt), run_time=0.6)
        self.at(self.cue("OTDR", 2))
        self.play(Create(ot[0]), FadeIn(ot[1]), run_time=0.7)
        self.end(pad=0.05)

        self.beat("c3")
        ng = VGroup(band(X, 1524, 1544, -1.35, 0.6, TW_US, None), band(X, 1596, 1603, -1.35, 0.6, TW_DS, None), band(X, 1603, 1625, -1.35, 0.6, PTP, None))
        ngl = VGroup(T("TWDM ↑", 15, TW_US, BOLD).move_to([X(1534), -2.55, 0]), T("TWDM ↓", 15, TW_DS, BOLD).move_to([X(1594), -2.55, 0]), T("PtP", 15, PTP, BOLD).move_to([X(1622), -2.55, 0]))
        g6 = VGroup(Line([X(1544), -1.0, 0], [X(1544), 0.45, 0], color=WARN, stroke_width=1.5), Line([X(1550), -1.0, 0], [X(1550), 0.45, 0], color=WARN, stroke_width=1.5),
                    T("6 nm", 17, WARN, BOLD).move_to([X(1530), 0.6, 0]))
        g16 = VGroup(DoubleArrow([X(1580), 0.45, 0], [X(1596), 0.45, 0], buff=0, color=GOOD, stroke_width=2, tip_length=0.08), T("16 nm", 17, GOOD, BOLD).move_to([X(1588), 0.7, 0]))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ng], lag_ratio=0.25), FadeIn(ngl), run_time=1.1)
        self.at(self.cue("altı nanometre", 4))
        self.play(FadeIn(g6), run_time=0.5)
        self.at(self.cue("TWDM aşağı yön", 6))
        self.play(FadeIn(g16), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c3a")
        self.set_badge("fiz")
        logic = VGroup(T("en az çakışma · en geniş koruma bandı", 22, GOOD, BOLD), T("dar bant (1532–1540) → videoya 10 nm", 19, TW_US, BOLD)).arrange(DOWN, buff=0.18).move_to(UP * 1.75)
        self.play(FadeIn(logic[0], shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Yukarı yönün üç", 5))
        self.play(FadeIn(logic[1], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p2A")


class E3P2B(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[2], M3("p2"), "fiz"

    def construct(self):
        self.beat("c4")
        h = self.show_heading("CEx — birlikte çalışma elemanı")
        srcs = VGroup(box(1.9, 0.5, "G-PON OLT", LEGACY, 15), box(1.9, 0.5, "XG-PON1 OLT", LEGACY, 15), box(1.9, 0.5, "NG-PON2 (WM)", TW_DS, 15), box(1.9, 0.5, "RF video", VIDEO, 15)).arrange(DOWN, buff=0.18).move_to([-5.2, 0.3, 0])
        cex = box(1.0, 2.6, "CEx", GOLD, 18).move_to([-2.9, 0.3, 0])
        ins = VGroup(*[Line(s.get_right(), [cex.get_left()[0], s.get_y(), 0], color=FEED, stroke_width=2) for s in srcs])
        fib = Line(cex.get_right(), [-1.2, 0.3, 0], color=FEED, stroke_width=4)
        sp = splitter(0.25).move_to([-0.95, 0.3, 0])
        # filter edges
        ax0 = np.array([0.6, -1.5, 0])
        def edge(x0, steep, color, label):
            pts = [ax0 + [0, 2.4, 0]]
            xs = np.linspace(0, 5.6, 80)
            curve = VMobject(color=color, stroke_width=3).set_points_smoothly([ax0 + [x, 2.2 / (1 + np.exp((x - x0) * steep)), 0] for x in xs])
            return VGroup(curve, T(label, 16, color, BOLD).move_to(ax0 + [x0 + 1.4, 1.4, 0]))
        axes = VGroup(Line(ax0, ax0 + [5.8, 0, 0], color=MUTED, stroke_width=2), Line(ax0, ax0 + [0, 2.5, 0], color=MUTED, stroke_width=2),
                      T("λ", 16, MUTED).next_to(ax0 + [5.8, 0, 0], RIGHT, buff=0.08), T("geçirgenlik", 14, MUTED).next_to(ax0 + [0, 2.5, 0], UP, buff=0.06))
        e1 = edge(2.0, 1.4, GOOD, "geniş boşluk → yumuşak kenar")
        e2 = edge(3.6, 9.0, WARN, "6 nm → dik kenar")
        self.play(LaggedStart(*[FadeIn(s) for s in srcs], lag_ratio=0.15), run_time=0.8)
        self.play(FadeIn(cex), Create(ins), Create(fib), FadeIn(sp), run_time=0.8)
        self.at(self.cue("Filtrenin kenar", 3))
        self.play(Create(axes), Create(e1[0]), FadeIn(e1[1]), run_time=0.8)
        self.at(self.cue("Altı nanometrelik", 5))
        self.play(Create(e2[0]), FadeIn(e2[1].shift(DOWN * 0.9 + RIGHT * 0.3)), run_time=0.8)
        self.end(pad=0.05)

        self.beat("c5")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Dalga boyu çoklayıcı — Ek VIII, Tablo VIII.1 (örnek)", h)
        tb = table(["Özellik", "Koşul", "Değer"],
                   [["Ekleme kaybı (konnektörsüz)", "S/R-CPn → S/R-CG", "< 2,0 dB (düşük) · < 4,0 dB (yüksek)"],
                    ["Geri dönüş kaybı", "her port", "> 50 dB"], ["Yönlülük", "CPn → CPn", "> 50 dB"], ["En büyük optik güç", "her port", "+23 dBm"]],
                   [4.0, 3.0, 4.6], size=20, hsize=17, row_h=0.6).move_to(UP * 0.2)
        self.play(FadeIn(tb[0]), FadeIn(tb[1], shift=UP * 0.1), self.set_src("G.989.2 Ek VIII.1"), run_time=0.7)
        self.at(self.cue("Geri dönüş", 4))
        self.play(FadeIn(tb[2], shift=UP * 0.1), FadeIn(tb[3], shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("en büyük optik", 6))
        self.play(FadeIn(tb[4], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c5a")
        c = VGroup(T("E2 ↓ kanal başına P_maks = +10 dBm", 22, TXT), T("8 × 10 mW = 80 mW ≈ +19 dBm", 26, ACC, BOLD), T("< +23 dBm WM sınırı → birkaç dB pay", 22, GOOD, BOLD)).arrange(DOWN, buff=0.2).move_to(DOWN * 2.1)
        self.play(tb.animate.shift(UP * 0.6), run_time=0.4)
        self.play(FadeIn(c[0]), run_time=0.5)
        self.at(self.cue("Sekiz kanal", 2))
        self.play(FadeIn(c[1]), run_time=0.5)
        self.at(self.cue("Çoklayıcının sınırı", 3))
        self.play(FadeIn(c[2]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c6")
        self.clear(h)
        h = self.show_heading("Kayıp sınıfı ve S/R-CP", h)
        cts = VGroup(*[box(0.9, 0.42, f"CT{i + 1}", CH[i], 14).move_to([-4.6, 1.0 - i * 0.6, 0]) for i in range(4)])
        wm = box(1.2, 2.6, "WM", "#3B4A75", 18).move_to([-1.8, 0.1, 0])
        lns = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=FEED, stroke_width=2) for c in cts])
        out = Line(wm.get_right(), [1.6, 0.1, 0], color=FEED, stroke_width=4)
        cp = DashedLine([-3.1, -1.6, 0], [-3.1, 1.7, 0], color=GOLD, stroke_width=2)
        cg = DashedLine([-0.6, -1.6, 0], [-0.6, 1.7, 0], color=ACC, stroke_width=2)
        lab = VGroup(T("S/R-CP", 17, GOLD, BOLD).next_to(cp, UP, buff=0.05), T("S/R-CG", 17, ACC, BOLD).next_to(cg, UP, buff=0.05))
        cls = VGroup(T("WM kayıp sınıfı", 20, TXT, BOLD), T("düşük < 2 dB  ·  yüksek < 4 dB", 19, TXT), T("AWG ↔ ince film filtre", 19, MUTED),
                     T("CP − CG = WM kaybı", 22, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.4, 0.1, 0])
        self.play(FadeIn(cts), Create(lns), FadeIn(wm), Create(out), run_time=0.8)
        self.play(FadeIn(cls[0:3]), run_time=0.6)
        self.at(self.cue("S bölü R CP", 4))
        self.play(Create(cp), Create(cg), FadeIn(lab), run_time=0.7)
        self.play(FadeIn(cls[3]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c6a")
        self.clear(h)
        h = self.show_heading("Toplam güç: bir fiber, çok sistem", h)
        parts = [("RF video yükselteci", VIDEO, 2.8), ("8 × TWDM ↓", TW_DS, 2.2), ("G-PON ↓", LEGACY, 1.5), ("XG-PON1 ↓", LEGACY, 1.7)]
        stack, x = VGroup(), -4.8
        for name, c, w in parts:
            r = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x + w / 2, 0.4, 0])
            stack.add(VGroup(r, T(name, 15, BG, BOLD).move_to(r)))
            x += w
        lab = T("temsili oranlar", 15, MUTED).next_to(stack, DOWN, buff=0.15).align_to(stack, LEFT)
        concl = VGroup(pill("doğrusal olmayan etkiler", WARN, 20), pill("göz güvenliği", GOLD, 20)).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.4)
        ek = T("Ek VI ikisini birlikte ele alır", 19, MUTED).next_to(concl, DOWN, buff=0.2)
        self.play(LaggedStart(*[GrowFromEdge(s, LEFT) for s in stack], lag_ratio=0.25), FadeIn(lab), run_time=1.3)
        self.at(self.cue("Altıncı ek", 2))
        self.play(FadeIn(concl, shift=UP * 0.1), FadeIn(ek), self.set_src("G.989.2 Ek VI"), run_time=0.6)
        self.end(pad=0.05)

        self.engineer_note("c7", [("1", "Birlikte çalışma = filtre meselesi", "Lisans değil, spektrum ve yalıtım.", 1),
                                  ("2", "Önce bant listesi, sonra yalıtım", "Her bant kenarında gereken yalıtımı hesaplayın.", 2)])
        self.beat("c8")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bantların içindeki ızgara:\nkanallar nereye oturur, ne kadar kayabilir?")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep03_p2B")
