"""B02 · Perde 3 (bütçe denklemi) and Perde 4 (mesafe, dispersiyon, yansıma)."""
from kit import *

H3, H4 = "BÖLÜM 2 · PERDE 3 — Bütçe denklemi", "BÖLÜM 2 · PERDE 4 — Mesafe, dispersiyon, yansıma"
M3, M4 = "build/ep02/p3/audio_proc/manifest.json", "build/ep02/p4/audio_proc/manifest.json"


def calc(parts, size=26):
    """parts: [(text, color, label)] → VGroup of columns (label above number), no label overlap."""
    cols = VGroup()
    for t, c, l in parts:
        n = T(t, size, c, BOLD)
        lab = T(l if l else "·", 15, c if l else BG).next_to(n, UP, buff=0.1)
        cols.add(VGroup(lab, n))
    return cols.arrange(RIGHT, buff=0.32, aligned_edge=DOWN)


class E2P3A(Act):
    HDR, MANIFEST, FIRST = H3, M3, True

    def construct(self):
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Bütçe denklemi")
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("G.989.2 §9.3.6.3")
        q = self.quote("G.989.2 §9.3.6.3", "“The optical link budget for a particular ODN optical loss class is satisfied, only if the difference between the minimum\ntransmitter mean launch optical power and the receiver sensitivity is equal to or exceeds the sum of the maximum OPP\nand the maximum optical path loss specified for the given ODN optical loss class.”",
                       "P_min − hassasiyet  ≥  maks. OPP + maks. yol kaybı", width=12.4).move_to(UP * 0.2)
        self.at(self.cues[2] - 0.3 if len(self.cues) > 2 else 3)
        self.play(FadeIn(q, shift=UP * 0.15), self.set_src("G.989.2 §9.3.6.3"), run_time=1.0)
        self.end(pad=0.05)

        self.beat("d1a")
        self.play(FadeOut(q), run_time=0.4)
        eq = T("P_min − S  ≥  OPL_maks + OPP", 46, GOLD, BOLD).move_to(UP * 0.8)
        ds = VGroup(T("↓ aşağı yön:", 22, TXT, BOLD), T("P_min @ S/R-CG", 22, ACC), T("S @ R/S", 22, ACC)).arrange(RIGHT, buff=0.4)
        us = VGroup(T("↑ yukarı yön:", 22, TXT, BOLD), T("P_min @ R/S", 22, CH[3]), T("S @ S/R-CG", 22, CH[3])).arrange(RIGHT, buff=0.4)
        VGroup(ds, us).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 1.2)
        self.play(Write(eq), run_time=1.2)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 4)
        self.play(FadeIn(ds, shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(us, shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d2")
        self.play(eq.animate.scale(0.6).move_to(UP * 1.95), FadeOut(ds), FadeOut(us), run_time=0.6)
        tb = table(["Tablo 11-4 · 2,5G ↓", "N1", "N2", "E1", "E2"], [["P_min (dBm)", "+0,0", "+2,0", "+4,0", "+6,0"], ["maks. OPP (dB)", "1,0", "1,0", "1,0", "1,0"], ["hassasiyet (dBm)", "−30,0", "−30,0", "−30,0", "−30,0"]],
                   [3.6, 1.6, 1.6, 1.6, 1.6], size=20, hsize=17, row_h=0.55).move_to(UP * 0.2)
        self.play(FadeIn(tb), self.set_src("G.989.2 Tablo 11-4"), run_time=0.8)
        c = calc([("0", ACC, "P_min"), ("− 29", CH[1], "OPL_maks"), ("− 1", MUTED, "OPP"), ("= −30 dBm ✓", GOOD, "hassasiyet")], 30).move_to(DOWN * 2.0)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(c, shift=UP * 0.1), run_time=0.8)
        self.end(pad=0.05)

        # d3/d4 — Type A vs Type B
        self.beat("d3")
        self.clear(h)
        h = self.show_heading("Yukarı yön: A tipi ve B tipi bağlantı", h)
        def link(y, amp, label, color):
            onu = box(1.2, 0.55, "ONU", "#94A3B8", 16).move_to([-5.4, y, 0])
            odn = Line(onu.get_right(), [1.0, y, 0], color=FEED, stroke_width=3)
            cg = DashedLine([1.2, y - 0.5, 0], [1.2, y + 0.5, 0], color=ACC, stroke_width=2)
            parts = VGroup(onu, odn, cg)
            x = 1.6
            if amp:
                a = Triangle(color=GOLD, fill_color=PANEL, fill_opacity=1, stroke_width=2.5).rotate(-PI / 2).scale(0.3).move_to([x + 0.3, y, 0])
                parts.add(a, T("yükselteç", 14, GOLD).next_to(a, UP, buff=0.05))
                x += 0.9
            rx = box(1.4, 0.55, "OLT Rx", color, 16).move_to([x + 1.0, y, 0])
            parts.add(Line([1.2, y, 0], rx.get_left(), color=FEED, stroke_width=3), rx,
                      T(label, 19, color, BOLD).next_to(onu, UP, buff=0.15).align_to(onu, LEFT), T("S/R-CG", 13, ACC).next_to(cg, DOWN, buff=0.05))
            return parts
        A = link(1.0, False, "A tipi — yükselteçsiz OLT alıcısı", CH[1])
        B = link(-1.2, True, "B tipi — S/R-CG'de yükselteç", GOLD)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 3)
        self.play(FadeIn(A), self.set_src("G.989.2 Tablo 11-6, Not 3–4"), run_time=0.8)
        self.at(self.cues[3] - 0.2 if len(self.cues) > 3 else 6)
        self.play(FadeIn(B), run_time=0.8)
        self.end(pad=0.05)

        self.beat("d4")
        pa = pill("ONU P_min: +4 dBm", CH[1], 20).next_to(A[0], DOWN, buff=0.25)
        pb = pill("ONU P_min: 0 dBm", GOLD, 20).next_to(B[0], DOWN, buff=0.25)
        self.play(FadeIn(pa), run_time=0.5)
        self.play(FadeIn(pb), run_time=0.5)
        mv = T("maliyet: evdeki çok sayıda ONU → merkez ofisteki az sayıda alıcı", 20, GOOD, BOLD).to_edge(DOWN, buff=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(mv), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p3A")


class E2P3B(Act):
    HDR, MANIFEST, PREV_BADGE = H3, M3, "std"

    def construct(self):
        self.beat("d5")
        h = self.show_heading("Tablo 11-6 (2,5G ↑) — hesap")
        tb = table(["2,5G ↑ · DD20 · 4 kanal", "N1", "N2", "E1", "E2"],
                   [["P_min A / B (dBm)", "+4 / 0", "+4 / 0", "+4 / 0", "+4 / 0"], ["maks. OPP, Raman dahil (dB)", "1,0", "1,0", "1,5", "1,5"],
                    ["hassasiyet A (dBm)", "−26", "−28", "−30,5", "−32,5"], ["hassasiyet B (dBm)", "−30", "−32", "−34,5", "−36,5"]],
                   [4.4, 1.6, 1.6, 1.6, 1.6], size=19, hsize=16, row_h=0.52).move_to(UP * 0.9)
        self.play(FadeIn(tb), self.set_src("G.989.2 Tablo 11-6"), run_time=0.8)
        c1 = calc([("+4", ACC, "P_min A"), ("− 29", CH[0], "N1"), ("− 1", MUTED, "OPP"), ("= −26 ✓", GOOD, "hassasiyet")], 24).move_to([-3.4, -1.6, 0])
        c2 = calc([("+4", ACC, "P_min A"), ("− 35", CH[3], "E2"), ("− 1,5", MUTED, "OPP"), ("= −32,5 ✓", GOOD, "")], 24).move_to([3.0, -1.6, 0])
        bt = T("B tipi: aynı hesap, 4 dB daha hassas (0 dBm ONU)", 20, GOLD, BOLD).to_edge(DOWN, buff=0.75)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at(self.cues[4] - 0.2 if len(self.cues) > 4 else 8)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(bt), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d5a")
        self.play(*[FadeOut(m) for m in (c1, c2, bt)], run_time=0.4)
        xt = table(["bant içi girişim toleransı (dB)", "N1", "N2", "E1", "E2"], [["A tipi", "26,0", "26,0", "25,1", "24,1"], ["B tipi", "22,0", "22,0", "21,1", "20,1"]],
                   [4.4, 1.6, 1.6, 1.6, 1.6], size=19, hsize=16, row_h=0.52).move_to(DOWN * 1.9)
        nx = T("→ Bölüm 5", 20, ACC, BOLD).next_to(xt, DOWN, buff=0.2).align_to(xt, RIGHT)
        self.play(FadeIn(xt), run_time=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(nx), run_time=0.4)
        self.end(pad=0.05)

        # d6/d7 — Raman OPP
        self.beat("d6")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Yukarı yönde yol cezası ve Raman", h, )
        cond = card("En kötü Raman durumu (Not 10)", "S/R-CG yakınında ayırıcı yok\n+ düşük fiber kaybı\n→ kanallar arası Raman etkileşimi en güçlü",
                    "G.989.2 Tablo 11-6, Not 10", WARN, w=7.0, h=2.4, tsize=24).move_to([-2.4, 0.5, 0])
        dep = VGroup(pill("sınıfa özgü verici gücü", ACC, 18), pill("mesafe", ACC, 18), pill("dalga boyu sayısı", ACC, 18)).arrange(DOWN, buff=0.2).move_to([4.2, 0.5, 0])
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 3)
        self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.2) for d in dep], lag_ratio=0.3), run_time=1.0)
        self.at(self.cues[-1] - 0.5)
        self.play(FadeIn(cond, shift=UP * 0.2), run_time=0.8)
        self.end(pad=0.05)

        self.beat("d7")
        self.play(FadeOut(cond), FadeOut(dep), run_time=0.4)
        opp = table(["maks. OPP (dB) · 2,5G ↑", "N1", "N2", "E1", "E2"],
                    [["DD20 · 4 kanal", "1,0", "1,0", "1,5", "1,5"], ["DD40 · 4 kanal", "1,4", "1,6", "1,9", "1,9"],
                     ["DD20 · 8 kanal", "1,0", "1,3", "1,8", "1,8"], ["DD40 · 8 kanal", "1,7", "2,1", "2,8", "2,8"]],
                    [4.0, 1.6, 1.6, 1.6, 1.6], size=20, hsize=17, row_h=0.55).move_to(UP * 0.4)
        exr = pill("Raman hariç maks. OPP: DD20 → 0,5 dB · DD40 → 1,0 dB", GOLD, 19).next_to(opp, DOWN, buff=0.35)
        self.play(FadeIn(opp), run_time=0.8)
        self.play(FadeIn(exr), run_time=0.5)
        hl = SurroundingRectangle(opp[4][5], color=WARN, buff=0.04)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(Create(hl), run_time=0.5)
        nx = T("→ Raman: Bölüm 3", 20, ACC, BOLD).next_to(exr, DOWN, buff=0.3)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(nx), run_time=0.4)
        self.end(pad=0.05)

        self.beat("d7a")
        self.clear(h)
        rule = card("Not 17 — fazla cezanın telafisi", "Gerçek OPP > belirtilen ise:  P_min += X dB  (X < 1,5 dB)\nyalnızca DD20 · yüksek ceza bölgesi risklidir\n→ gerçek OPP birlikte çalışabilirlik testiyle ölçülmeli",
                    "G.989.2 Tablo 11-6, Not 17", GOLD, w=11.2, h=2.6, tsize=26).move_to(UP * 0.2)
        self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.8)
        self.end(pad=0.05)

        self.beat("d8")
        self.play(FadeOut(rule), run_time=0.4)
        self.set_badge("std")
        h = self.show_heading("Aşırı yük: P_maks − OPL_min", h)
        c1 = calc([("+9", ACC, "P_maks A"), ("− 14", CH[0], "OPL_min N1"), ("= −5 dBm ✓", GOOD, "aşırı yük")], 28).move_to(UP * 0.8)
        c2 = calc([("+9", ACC, "P_maks A"), ("− 20", CH[3], "OPL_min E2"), ("= −11 dBm ✓", GOOD, "aşırı yük")], 28).move_to(DOWN * 0.8)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at(self.cues[3] - 0.2 if len(self.cues) > 3 else 5)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.end(pad=0.05)

        self.beat("d8a")
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
        h = self.show_heading("Marj: tablo ile gerçek arasındaki fark", h)
        sc = 0.24
        x0 = -6.0
        ay = -1.5
        ax = NumberLine(x_range=[-40, 10, 5], length=50 * sc, include_numbers=False, color=MUTED).move_to([x0 + 25 * sc, ay, 0])
        nums = VGroup(*[T(f"{v}", 15, MUTED).next_to(ax.n2p(v), DOWN, buff=0.08) for v in range(-40, 11, 10)], T("dBm", 15, MUTED).next_to(ax, RIGHT, buff=0.15))
        def tick(v, color, label, hgt, side):
            l = Line(ax.n2p(v) + UP * 0.1, ax.n2p(v) + UP * hgt, color=color, stroke_width=3)
            t = T(label, 16, color, BOLD).next_to(l, UP, buff=0.06)
            t.shift((LEFT if side < 0 else RIGHT) * (t.width / 2 - 0.05))
            return VGroup(l, t)
        pmin = tick(4, ACC, "P_min +4 (tablo)", 0.9, -1)
        pact = tick(6, GOOD, "gerçek Tx +6", 1.9, 1)
        sens = tick(-26, CH[1], "S −26 (tablo)", 0.9, 1)
        sact = tick(-29, GOOD, "gerçek Rx −29", 1.9, -1)
        budget = DoubleArrow(ax.n2p(-26) + UP * 0.45, ax.n2p(4) + UP * 0.45, buff=0, color=MUTED, stroke_width=2, tip_length=0.15)
        bl = T("tablo: 30 dB = OPL 29 + OPP 1", 15, MUTED).next_to(budget, UP, buff=0.05)
        path = DoubleArrow(ax.n2p(-29) + UP * 1.45, ax.n2p(6) + UP * 1.45, buff=0, color=WHITE, stroke_width=2, tip_length=0.15)
        pl = T("gerçek: 35 dB → marj ≈ 5 dB", 16, GOOD, BOLD).next_to(path, UP, buff=0.05)
        mt = T("marj = gerçek fark − (OPL + OPP)  · örnek değerler", 20, GOOD, BOLD).move_to(UP * 1.75)
        self.play(Create(ax), FadeIn(nums), FadeIn(pmin), FadeIn(sens), Create(budget), FadeIn(bl), run_time=0.9)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 3)
        self.play(FadeIn(pact), FadeIn(sact), Create(path), FadeIn(pl), run_time=0.8)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 6)
        self.play(FadeIn(mt), run_time=0.5)
        wc = pill("asıl test: en kötü sıcaklık ve ömür sonu", WARN, 19).next_to(ax, DOWN, buff=0.75)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(wc), run_time=0.5)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p3B")


class E2P3C(Act):
    HDR, MANIFEST, PREV_BADGE = H3, M3, "std"

    def construct(self):
        self.beat("d8b")
        h = self.show_heading("Tablo 11-7 (10G ↑)")
        tb = table(["10G ↑ · DD20 · 4 kanal", "N1", "N2", "E1", "E2"],
                   [["P_min A (dBm)", "+4,0", "+4,0", "+4,0", "NA"], ["P_min B (dBm)", "+2,0", "+2,0", "+2,0", "+4,0"],
                    ["hassasiyet A (dBm)", "−26,0", "−28,0", "−30,5", "NA"], ["hassasiyet B (dBm)", "−28,0", "−30,0", "−32,5", "−32,5"]],
                   [4.4, 1.6, 1.6, 1.6, 1.6], size=19, hsize=16, row_h=0.52).move_to(UP * 0.8)
        self.play(FadeIn(tb), self.set_src("G.989.2 Tablo 11-7"), run_time=0.8)
        c = calc([("+2", ACC, "P_min B"), ("− 29", CH[0], "N1"), ("− 1", MUTED, "OPP"), ("= −28 ✓", GOOD, "hassasiyet B")], 24).move_to(DOWN * 1.3)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 4)
        self.play(FadeIn(c), run_time=0.7)
        na = VGroup(SurroundingRectangle(tb[1][5], color=WARN, buff=0.03), SurroundingRectangle(tb[3][5], color=WARN, buff=0.03))
        nt = T("10G ↑ E2: yalnızca yükselteçli (B tipi) alıcıyla", 20, WARN, BOLD).to_edge(DOWN, buff=0.7)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 8)
        self.play(Create(na), FadeIn(nt), run_time=0.7)
        self.end(pad=0.05)

        self.beat("d8c")
        self.clear(h)
        h = self.show_heading("En küçük sönüm oranı", h)
        sc = 0.55
        b1 = Rectangle(width=8.2 * sc, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([-6.0 + 8.2 * sc / 2, 0.6, 0])
        b2 = Rectangle(width=6.0 * sc, height=0.7, stroke_width=0, fill_color=CH[1], fill_opacity=0.85).move_to([-6.0 + 6.0 * sc / 2, -0.6, 0])
        l1 = T("2,5G ↑: 8,2 dB", 22, GOLD, BOLD).next_to(b1, RIGHT, buff=0.2)
        l2 = T("10G ↑: 6,0 dB", 22, CH[1], BOLD).next_to(b2, RIGHT, buff=0.2)
        why = T("yüksek hızda burst modlu lazerden yüksek ER zor → daha düşük sınır", 19, MUTED).to_edge(DOWN, buff=0.9)
        self.play(GrowFromEdge(b1, LEFT), FadeIn(l1), run_time=0.7)
        self.play(GrowFromEdge(b2, LEFT), FadeIn(l2), self.set_src("G.989.2 Tablo 11-6, 11-7"), run_time=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(why), run_time=0.5)
        self.end(pad=0.05)

        self.engineer_note("d9", [("1", "Her hassasiyetin bir varsayımı var", "Mesafe (DD20/DD40) ve kanal sayısı (4/8) değişince yol cezası da değişir.", 1),
                                  ("2", "Dipnotları okuyun", "Not 10, 12, 17: Raman, 40 km + 8 kanal yaklaşımı, ceza telafisi.", 3)])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep02_p3C")


class E2P4A(Act):
    HDR, MANIFEST, FIRST = H4, M4, True

    def construct(self):
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Mesafe, dispersiyon, yansıma")
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Fiber mesafe sınıfları — Tablo 6-2")
        tb = table(["Sınıf", "En küçük (km)", "En büyük (km)"], [["DD20", "0", "20"], ["DD40", "0", "40"]], [3.0, 3.2, 3.2], size=24, hsize=19, row_h=0.65).move_to(UP * 0.3)
        self.play(FadeIn(tb), self.set_src("G.989.2 §6.3, Tablo 6-2"), run_time=0.8)
        self.end(pad=0.05)

        self.beat("e1a")
        q = self.quote("G.989.2 §6.3", "“…PSD values in the PMD tables in clause 11 have been optimized for TWDM 4-channel and 20 km.\nInvestigations for TWDM 8 channel and/or DD40 (40 km) are for further study.”",
                       "Mesafe sınıfı, girişim (PSD) limitlerinin geçerliliğini de etkiler", width=12.0).move_to(DOWN * 1.8)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.end(pad=0.05)

        self.beat("e2")
        self.clear(h)
        h = self.show_heading("Dispersiyon aralığı (ps/nm)", h)
        tb = table(["Yön", "DD20", "DD40"], [["↓ aşağı (Tablo 11-4/11-5)", "0 – 420", "0 – 840"], ["↑ yukarı (Tablo 11-6/11-7)", "0 – 355", "0 – 710"]], [5.0, 2.6, 2.6], size=23, hsize=19, row_h=0.65).move_to(UP * 0.4)
        self.play(FadeIn(tb[0]), FadeIn(tb[1], shift=UP * 0.1), self.set_src("G.989.2 Tablo 11-4 … 11-7"), run_time=0.8)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 6)
        self.play(FadeIn(tb[2], shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e3")
        self.play(tb.animate.scale(0.58).move_to([4.0, 1.5, 0]), run_time=0.6)
        ax = Axes(x_range=[1500, 1620, 20], y_range=[14, 23, 2], x_length=7.0, y_length=3.4, axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-2.4, -0.6, 0])
        D = lambda l: 0.092 / 4 * (l - 1310 ** 4 / l ** 3)
        cv = ax.plot(D, x_range=[1500, 1620], color=TXT, stroke_width=3)
        us = Rectangle(width=ax.c2p(1544, 0)[0] - ax.c2p(1524, 0)[0], height=3.4, stroke_width=0, fill_color=CH[3], fill_opacity=0.18).move_to([ax.c2p(1534, 0)[0], ax.get_center()[1], 0])
        dsb = Rectangle(width=ax.c2p(1603, 0)[0] - ax.c2p(1596, 0)[0], height=3.4, stroke_width=0, fill_color=ACC, fill_opacity=0.25).move_to([ax.c2p(1599.5, 0)[0], ax.get_center()[1], 0])
        labs = VGroup(*[T(str(v), 14, MUTED).next_to(ax.c2p(v, 14), DOWN, buff=0.08) for v in (1500, 1540, 1580, 1620)], T("nm", 14, MUTED).next_to(ax.c2p(1620, 14), RIGHT, buff=0.1),
                      T("D (ps/nm/km) — G.652 tipik eğri", 14, MUTED).next_to(ax, DOWN, buff=0.4).align_to(ax, LEFT), T("↑ 1524–1544", 14, CH[3], BOLD).next_to(us, UP, buff=0.04), T("↓ 1596–1603", 14, ACC, BOLD).next_to(dsb, UP, buff=0.04))
        r1 = T("420 / 20 = 21 ps/nm/km", 22, ACC, BOLD).move_to([4.2, -0.6, 0])
        r2 = T("355 / 20 ≈ 17,75 ps/nm/km", 22, CH[3], BOLD).next_to(r1, DOWN, buff=0.3)
        self.play(Create(ax), FadeIn(us), FadeIn(dsb), Create(cv), FadeIn(labs), run_time=1.1)
        self.play(FadeIn(r1), run_time=0.5)
        self.play(FadeIn(r2), run_time=0.5)
        wc = T("en kötü dispersiyon katsayısı (§9.3.5.4)", 17, MUTED).next_to(r2, DOWN, buff=0.25)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 6)
        self.play(FadeIn(wc), run_time=0.4)
        self.end(pad=0.05)

        self.clear()
        self.save_timeline("ep02_p4A")


class E2P4A2(Act):
    HDR, MANIFEST, PREV_BADGE = H4, M4, "std"

    def construct(self):
        h = None
        self.beat("e3a")
        self.clear(h)
        h = self.show_heading("Kaynak: tek boylamsal modlu lazer", h)
        ax = Line([-5.5, -1.2, 0], [0.0, -1.2, 0], color=MUTED)
        slm = VGroup(FunctionGraph(lambda x: -1.2 + 2.0 * np.exp(-((x + 2.75) / 0.08) ** 2), x_range=[-3.3, -2.2], color=ACC, stroke_width=3),
                     *[FunctionGraph(lambda x, c=c: -1.2 + 0.06 * np.exp(-((x - c) / 0.06) ** 2), x_range=[c - 0.25, c + 0.25], color=ACC, stroke_width=2) for c in (-4.0, -1.5)])
        smsr = DoubleArrow([-1.5, -1.1, 0], [-1.5, 0.8, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12)
        st = T("SMSR ≥ 30 dB", 20, GOLD, BOLD).next_to(smsr, RIGHT, buff=0.15)
        info = VGroup(T("Standart kaynak tipini zorunlu kılmaz,", 19, TXT), T("ama yalnızca SLM lazerler uygun (§11.1.5.1)", 19, TXT),
                      T("mod bölüşme gürültüsü → en küçük SMSR (§9.3.8)", 19, TXT), T("sınırlanan: sonuçtaki yol cezası (OPP)", 19, ACC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 0.0, 0]).align_to(np.array([0.9, 0, 0]), LEFT)
        self.play(Create(ax), Create(slm), run_time=0.9)
        self.play(GrowArrow(smsr), FadeIn(st), run_time=0.5)
        for k, t0 in enumerate([self.cues[1], self.cues[1] + 2.0, self.cues[2], self.cues[-1]] if len(self.cues) > 2 else [1, 3, 5, 7]):
            self.at(t0 - 0.2)
            self.play(FadeIn(info[k], shift=LEFT * 0.15), run_time=0.45)
        self.play(self.set_src("G.989.2 §9.3.8, §11.1.5.1"), run_time=0.3)
        self.end(pad=0.05)

        self.beat("e4")
        self.clear(h)
        n6 = card("Tablo 11-5, Not 6", "Belirtilen OPP (2,0 dB) 40 km'ye kadar geçerli.\nGerçek OPP daha kötüyse → verici gücü artırılarak telafi\n(maks. başlatma gücü sınırı içinde).", "G.989.2 Tablo 11-5", GOLD, w=11.0, h=2.4, tsize=26).move_to(UP * 0.3)
        self.play(FadeIn(n6, shift=UP * 0.2), run_time=0.8)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p4A2")


class E2P4B(Act):
    HDR, MANIFEST, PREV_BADGE = H4, M4, "std"

    def construct(self):
        self.beat("e5")
        self.set_badge("fiz")
        h = self.show_heading("Yansımalar: üç ayrı sınır")
        fib = Line([-6.0, 1.0, 0], [6.0, 1.0, 0], color=FEED, stroke_width=5)
        olt = box(1.0, 0.6, "OLT", "#3B4A75", 15).move_to([-6.2, 1.0, 0])
        cons = VGroup(*[Rectangle(width=0.2, height=0.5, stroke_color=GOLD, stroke_width=2, fill_color=BG, fill_opacity=1).move_to([x, 1.0, 0]) for x in (-3.5, -0.5, 2.5)])
        refl = VGroup(*[Arrow([c.get_x(), 1.45, 0], [c.get_x() - 1.2, 1.45, 0], buff=0, color=WARN, stroke_width=2.5, max_tip_length_to_length_ratio=0.2) for c in cons])
        lims = VGroup(card("ODN ORL", "≥ 32 dB", "Tablo 11-4 … 11-7", ACC, w=3.6, h=1.6, tsize=22, bsize=26),
                      card("Ayrık yansıma", "< −35 dB", "§9.3.5.3", WARN, w=3.6, h=1.6, tsize=22, bsize=26),
                      card("Tx yansıma toleransı", "−15 dB", "§9.3.4", GOLD, w=3.6, h=1.6, tsize=22, bsize=26)).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.4)
        self.play(FadeIn(olt), Create(fib), FadeIn(cons), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(r) for r in refl], lag_ratio=0.3), run_time=1.0)
        n = len(self.cues)
        for k, t0 in enumerate([self.cues[min(n - 1, 3)], self.cues[min(n - 1, 4)], self.cues[-1]]):
            self.at(t0 - 0.2)
            self.play(FadeIn(lims[k], shift=UP * 0.2), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e5a")
        rx = pill("ONU alıcı dalga boyunda ekipman yansıması ≤ −20 dB", CH[1], 19).next_to(lims, UP, buff=0.3)
        self.play(FadeIn(rx, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e6")
        self.clear(h)
        tx = card("ONU verici dalga boyunda ekipman yansıması", "≤ −32 dB  (R/S)\nneden: birden çok yukarı yön ONU yankısı (Not 19)", "G.989.2 Tablo 11-6, 11-7", PINK, w=10.0, h=2.2, tsize=24).move_to(UP * 0.4)
        self.play(FadeIn(tx, shift=UP * 0.2), self.set_src("G.989.2 Tablo 11-6, Not 19"), run_time=0.8)
        self.end(pad=0.05)

        # e7 — echo path
        self.beat("e7")
        self.clear(h)
        h = self.show_heading("Yankı: bant içi girişim", h)
        olt = box(1.3, 0.8, "OLT Rx", "#3B4A75", 16).move_to([-5.6, 0.6, 0])
        con = Rectangle(width=0.22, height=0.55, stroke_color=GOLD, stroke_width=2.5, fill_color=BG, fill_opacity=1).move_to([-2.4, 0.6, 0])
        sp = splitter(0.3).move_to([0.6, 0.6, 0])
        f1 = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=4)
        onus = VGroup(*[box(1.3, 0.48, "ONU", c, 14).move_to([4.2, 1.6 - 0.95 * i, 0]) for i, c in enumerate([CH[1], "#94A3B8", "#94A3B8"])])
        drops = VGroup(*[Line(sp.get_right(), o.get_left(), color="#94A3B8", stroke_width=2) for o in onus])
        self.play(FadeIn(olt), Create(f1), FadeIn(con), FadeIn(sp), Create(drops), FadeIn(onus), run_time=1.0)
        p_up = VMobject().set_points_as_corners([onus[0].get_left(), sp.get_center(), con.get_center()])
        p_back = VMobject().set_points_as_corners([con.get_center(), sp.get_center(), onus[1].get_left()])
        p_re = VMobject().set_points_as_corners([onus[1].get_left(), sp.get_center(), olt.get_right()])
        d1 = glow_dot(CH[1], 0.07).move_to(p_up.get_start())
        self.add(d1)
        self.play(MoveAlongPath(d1, p_up), run_time=1.0, rate_func=linear)
        r1 = T("1. yansıma (konnektör)", 15, GOLD, BOLD).next_to(con, UP, buff=0.15)
        self.play(FadeIn(r1), run_time=0.3)
        d1.set_opacity(0.5)
        self.play(MoveAlongPath(d1, p_back), run_time=1.0, rate_func=linear)
        r2 = T("2. yansıma (ONU)", 15, PINK, BOLD).next_to(onus[1], DOWN, buff=0.1)
        self.play(FadeIn(r2), run_time=0.3)
        d1.set_opacity(0.3)
        self.play(MoveAlongPath(d1, p_re), run_time=1.1, rate_func=linear)
        self.remove(d1)
        sc = scope(3.0, 1.5, [-4.6, -1.9, 0])
        rng = np.random.default_rng(3)
        x0 = sc[0].get_left()[0] + 0.1
        yb = sc[0].get_bottom()[1] + 0.15
        main = VMobject(color=CH[1], stroke_width=2.5).set_points_as_corners(nrz(rng.integers(0, 2, 20), x0, 0.14, yb, yb + 1.0))
        echo = VMobject(color=WARN, stroke_width=2).set_points_as_corners(nrz(rng.integers(0, 2, 20), x0 + 0.3, 0.14, yb + 0.02, yb + 0.12))
        el = T("aynı λ → filtreyle ayrılamaz", 17, WARN, BOLD).next_to(sc, RIGHT, buff=0.3)
        self.at(self.cues[-2] - 0.3 if len(self.cues) > 2 else 8)
        self.play(FadeIn(sc), Create(main), Create(echo), FadeIn(el), run_time=1.2)
        self.end(pad=0.05)

        self.beat("e7a")
        sm = VGroup(*[Rectangle(width=0.12, height=0.05 + 0.02 * k, stroke_width=0, fill_color=WARN, fill_opacity=0.8) for k in range(24)]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN).move_to([2.6, -1.9, 0])
        st = T("onlarca küçük yankı → bant içi girişim bütçesi", 17, WARN, BOLD).next_to(sm, UP, buff=0.15)
        self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in sm], lag_ratio=0.05), FadeIn(st), run_time=1.4)
        self.end(pad=0.05)

        self.beat("e8")
        self.clear(h)
        h = self.show_heading("Aynı denklemin parçaları", h)
        nodes = VGroup(*[card(t, b, None, c, w=3.8, h=1.3, tsize=20, bsize=18) for t, b, c in [("ODN ORL", "≥ 32 dB", ACC), ("Konnektör yansıması", "< −35 dB", GOLD),
                                                                                             ("ONU Tx yansıması", "≤ −32 dB", PINK), ("OLT bant içi tolerans", "Tablo 11-6/11-7", CH[1])]])
        nodes.arrange_in_grid(2, 2, buff=(0.6, 0.5)).move_to(DOWN * 0.2)
        center = Circle(radius=0.35, color=WHITE, stroke_width=2).move_to(nodes.get_center())
        links = VGroup(*[Line(center.get_center(), n.get_center(), color=MUTED, stroke_width=1.5).set_z_index(-1) for n in nodes])
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.2), run_time=1.2)
        self.play(Create(links), FadeIn(center), run_time=0.6)
        nx = T("→ Bölüm 5 ve 8: girişim toleransı ölçümü", 19, ACC, BOLD).to_edge(DOWN, buff=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(nx), run_time=0.4)
        self.end(pad=0.05)

        self.beat("e8a")
        self.clear(h)
        h = self.show_heading("Sahadan bir örüntü", h)
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 26, 5], x_length=8.0, y_length=3.4, axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-1.6, -0.9, 0])
        def trace(x):
            y = 10 - 0.25 * x
            for p, hgt in ((3, 6), (9.5, 16), (14, 5)):
                y += hgt * np.exp(-((x - p) / 0.08) ** 2)
            return y
        tr = ax.plot(trace, x_range=[0.1, 18, 0.01], color=CH[1], stroke_width=2.5)
        lab = VGroup(T("OTDR izi (temsili)", 15, MUTED).next_to(ax, UP, buff=0.05).align_to(ax, LEFT), T("mesafe (km)", 14, MUTED).next_to(ax.c2p(20, 0), DOWN, buff=0.08).shift(LEFT * 0.4))
        spike = Circle(radius=0.3, color=WARN, stroke_width=3).move_to(ax.c2p(9.5, trace(9.5) - 1.5))
        st = VGroup(T("yüksek yansıma olayı:", 19, WARN, BOLD), T("UPC konnektör APC hattında / kirli bağlantı", 17, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 0.6, 0]).align_to(np.array([6.8, 0, 0]), RIGHT)
        fix = T("temizle / değiştir → hata kaybolur", 19, GOOD, BOLD).next_to(st, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Create(ax), FadeIn(lab), Create(tr), run_time=1.2)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(Create(spike), FadeIn(st), run_time=0.7)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 9)
        self.play(FadeIn(fix), run_time=0.5)
        self.end(pad=0.05)

        self.engineer_note("e9", [("1", "En sık yansıma kaynağı", "Kirli ya da hasarlı konnektörler.", 1),
                                  ("2", "Görünmez ama kritik kalem", "Açılı cilalı (APC) konnektörler ve temizlik disiplini.", 2)])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep02_p4B")
