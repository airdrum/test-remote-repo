"""S2·B4 · Laboratuvarda (durağan atama, aşırı yük, geri gelme, yakınsama, gecikme, yoklama, DBRu, trafik izleme, altın vektör) and Kapanış."""
from ep14_common import *

MODEL = [["A", "NA", "100", "225"], ["B", "NA", "300", "675"], ["C", "BE", "0", "0"], ["D", "yok", "50", "50"], ["E", "BE", "100", "50"]]
POLL = [("32 ONU", 6.3, "%6,3"), ("64 ONU", 12.5, "%12,5"), ("128 ONU", 25.0, "%25"), ("256 ONU", 50.0, "%50")]


class E14LabA(Act14):
    HDR, MANIFEST, FIRST = H14["L"], M14("lab"), True

    def construct(self):
        # g1 — bench: analyzer (DS BWmaps + US bursts), OLT/ONU emulator, timestamping traffic generator, 0/20/40 km spools
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "DBA gecikmesi, verim ve yoklama")
        self.at(self.cue("Düzenek", 1.2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Düzenek")
        pa = pa_icon(2.3, 1.55, "Analizör · ↓ BWmap · ↑ burst").move_to([-4.9, 1.1, 0])
        em = emu_icon(2.3, 1.55, "OLT + ONU emülatörü").move_to([-1.75, 1.1, 0])
        tg = tg_icon(2.3, 1.55, "Trafik üreteci · zaman damgalı").move_to([1.4, 1.1, 0])
        sp = VGroup(*[spool(s) for s in ("0 km", "20 km", "40 km")]).arrange(RIGHT, buff=0.25).move_to([4.95, 1.1, 0])
        st = VGroup(T("standart:", 18, MUTED, BOLD), VGroup(T("ölçütleri verir", 18, TXT, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.1),
                    VGroup(T("yöntemleri vermez", 18, TXT, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.4).move_to([0, -1.0, 0])
        rest = VGroup(interp("yorum"), T("aşağıdaki yöntemler mühendislik pratiğidir", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.0, 0])
        self.at(self.cue("protokol analizörü", 4.0))
        self.play(self.set_src("G.989.3 §7.4 · tezgâh ve yöntemler: yorum"), FadeIn(pa, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("OLT ve ONU emülatörü", 8.9))
        self.play(FadeIn(em, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("zaman damgalı bir trafik", 11.0))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ve sıfır,", 13.8))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in sp], lag_ratio=0.3), run_time=0.9)
        self.at(self.cue("Standart ölçütleri verir", 18.3))
        self.play(FadeIn(st[:2], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("yöntemleri vermez", 20.4))
        self.play(FadeIn(st[2], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("mühendislik pratiğidir", 21.9))
        self.play(FadeIn(rest, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # g2 — TEST 1: stationary assignment vs the reference model (§7.4.1): Σ GrantSize × 4 B / 16 B − DBRu; ≥ RF+RA, within e.g. 10 %
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "Durağan atama — §7.4.1")
        tb = mtable(["akış", "tür", "RF + RA", "model R"], MODEL, [1.0, 1.1, 1.5, 1.6], size=18, hsize=15, row_h=0.42).move_to([-4.0, 0.0, 0])
        for r, k in zip(tb[1:], "ABCDE"):
            r[1].set_color(FLOWC[k])
            r[4].set_color(GOLD)
        tbl = T("İkinci perdenin örneği · Mbit/s", 15, MUTED, BOLD).next_to(tb, UP, buff=0.1).align_to(tb, LEFT)
        p = apanel(6.4, 1.75, "Analizör · K çerçevelik pencere", ACC).move_to([3.0, 1.05, 0])
        f1 = VGroup(T("Σ GrantSize ×", 19, TXT, BOLD), tag("4 B · 2,5G", R25, 16), tag("16 B · 10G", R10, 16)).arrange(RIGHT, buff=0.15)
        f2 = VGroup(T("− DBRu baytları", 19, BWC, BOLD), T("→ Alloc-ID başına bit/s", 17, MUTED, BOLD)).arrange(RIGHT, buff=0.2)
        ff = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(p[0]).shift(DOWN * 0.18)
        x0, U = 0.4, 0.0072
        bars = VGroup()
        for i, (k, v) in enumerate((("A", 225), ("B", 675))):
            yy = -1.0 - i * 0.85
            band = Rectangle(width=v * 0.2 * U, height=0.5, stroke_width=0, fill_color=GOOD, fill_opacity=0.25).move_to([x0 + v * U, yy, 0])
            mb = Rectangle(width=v * U, height=0.3, stroke_color=FLOWC[k], stroke_width=1.5, fill_color=FLOWC[k], fill_opacity=0.45).move_to([x0 + v * U / 2, yy, 0])
            gm = DashedLine([x0 + {"A": 100, "B": 300}[k] * U, yy - 0.3, 0], [x0 + {"A": 100, "B": 300}[k] * U, yy + 0.3, 0], color=GOOD, stroke_width=2.5)
            lab = T(k, 17, FLOWC[k], BOLD).next_to([x0, yy, 0], LEFT, buff=0.15)
            bars.add(VGroup(lab, mb, gm, band))
        bl = VGroup(VGroup(DashedLine(ORIGIN, RIGHT * 0.3, color=GOOD, stroke_width=2.5), T("≥ RF + RA", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.1),
                    VGroup(Rectangle(width=0.3, height=0.22, stroke_width=0, fill_color=GOOD, fill_opacity=0.3), T("model ± %10 (örn.)", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.1))
        bl.arrange(RIGHT, buff=0.4).move_to([3.3, -2.75, 0])
        self.at(self.cue("beş akışı tanımlayın", 2.0))
        self.play(self.set_src("G.989.3 §7.4.1 · §8.1.1.2.4 · örnek: hesap"), FadeIn(tbl), FadeIn(tb[0]), LaggedStart(*[FadeIn(r[:4]) for r in tb[1:]], lag_ratio=0.12), run_time=0.9)
        self.at(self.cue("sabit yükler sunun", 5.1))
        self.play(LaggedStart(*[FadeIn(r[4]) for r in tb[1:]], lag_ratio=0.12), run_time=0.6)
        self.at(self.cue("haritaları bir pencere", 6.7))
        self.play(FadeIn(p), run_time=0.4)
        self.at(self.cue("iki buçuk gigabitte dört", 10.2))
        self.play(FadeIn(f1, shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("raporları düşün", 19.4))
        self.play(FadeIn(f2, shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("en az garantili payı", 20.9))
        self.play(*[FadeIn(b[0]) for b in bars], *[GrowFromEdge(b[1], LEFT) for b in bars], *[Create(b[2]) for b in bars], FadeIn(bl[0]), run_time=0.8)
        self.at(self.cue("yüzde on içinde", 24.7))
        self.play(*[FadeIn(b[3]) for b in bars], FadeIn(bl[1]), run_time=0.5)
        self.end(pad=0.05)

        # g3 — TEST 2: overload — BE gets 0 while NA unsaturated; idle fixed share is granted and filled with idle XGEM; violate (7-3) → congestion counter
        self.beat("g3")
        self.play(FadeOut(VGroup(tb, tbl, p, ff, bars, bl)), run_time=0.4)
        h = step_head(self, 2, "Aşırı yük", h)
        y = 1.0
        U = 0.0118
        x0 = -5.9
        cap = Rectangle(width=1000 * U, height=0.55, stroke_color=TXT, stroke_width=2).move_to([x0 + 500 * U, y, 0])
        segs = VGroup()
        xx = x0
        for k, v in (("A", 225), ("B", 675), ("D", 50), ("E", 50)):
            r = Rectangle(width=v * U, height=0.55, stroke_color=FLOWC[k], stroke_width=1.5, fill_color=FLOWC[k], fill_opacity=0.45).move_to([xx + v * U / 2, y, 0])
            segs.add(VGroup(r, T(k, 15, TXT, BOLD).move_to(r)) if v * U > 0.35 else VGroup(r, T(k, 15, FLOWC[k], BOLD).next_to(r, UP, buff=0.06)))
            xx += v * U
        capl = T("C = 1000 Mbit/s", 15, TXT, BOLD).next_to(cap, UP, buff=0.06).align_to(cap, LEFT)
        c0 = VGroup(tag("C · en iyi çaba", BEC, 16), T("= 0", 20, TXT, BOLD), T("A, B doymamışken", 16, MUTED, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.15).move_to([-2.6, -0.05, 0])
        dz = segs[2][0]
        idl = VGroup(*[Line(dz.get_corner(DL) + RIGHT * 0.1 * i, dz.get_corner(DL) + RIGHT * 0.1 * i + UP * 0.55, color=IDC, stroke_width=2) for i in range(1, 6)])
        dl = VGroup(tag("D · sabit pay, trafik yok", FXC, 16), T("→ boş XGEM ile dolar · boşa giden payı ölç", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([2.4, -0.75, 0])
        da = arrow(dl.get_top() + LEFT * 2.0, dz.get_bottom() + DOWN * 0.05, FXC, 1.8, 0.1)
        y2 = -1.75
        U2 = 0.0105
        ov = VGroup(*[Rectangle(width=w * U2, height=0.4, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.45) for w, c in ((420, ASC), (360, ASC), (320, ASC))]).arrange(RIGHT, buff=0.02)
        ov.move_to([x0, y2, 0], aligned_edge=LEFT)
        capl2 = DashedLine([x0 + 1000 * U2, y2 + 0.4, 0], [x0 + 1000 * U2, y2 - 0.4, 0], color=TXT, stroke_width=2.5)
        over = Rectangle(width=ov.get_right()[0] - (x0 + 1000 * U2), height=0.46, stroke_color=WARN, stroke_width=2.5).move_to([(ov.get_right()[0] + x0 + 1000 * U2) / 2, y2, 0])
        ovl = VGroup(T("Σ (RF + RA) > C", 18, WARN, BOLD), tag("(7-3) bilerek çiğnenir", WARN, 15)).arrange(RIGHT, buff=0.2).next_to(ov, UP, buff=0.1).align_to(ov, LEFT)
        cnt = VGroup(tag("Tablo 14-1 · talep varken garantili pay atanamadı", MUTED, 16), T("sayaç ↑", 20, WARN, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -2.7, 0])
        self.play(self.set_src("G.989.3 §7.3.3 · (7-3) · Tablo 14-1 · §9.1.4"), Create(cap), FadeIn(capl), LaggedStart(*[FadeIn(s) for s in segs], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("doymadıkça sıfır", 3.4))
        self.play(FadeIn(c0, shift=UP * 0.06), run_time=0.6)
        self.at(self.cue("Trafiği olmayan sabit paylı", 7.3))
        self.play(FadeIn(dl[0], shift=UP * 0.06), GrowArrow(da), Indicate(segs[2], color=FXC, scale_factor=1.2), run_time=0.7)
        self.at(self.cue("boş çerçevelerle doldurmalıdır", 11.6))
        self.play(Create(idl), run_time=0.5)
        self.at(self.cue("boşa giden payı ölçün", 15.2))
        self.play(FadeIn(dl[1], shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("kararlılık koşulunu bilerek", 17.0))
        self.play(LaggedStart(*[GrowFromEdge(o, LEFT) for o in ov], lag_ratio=0.2), Create(capl2), FadeIn(ovl), run_time=0.8)
        self.play(Create(over), run_time=0.3)
        self.at(self.cue("tıkanıklık sayacı artmalıdır", 20.7))
        self.play(FadeIn(cnt, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # g4 — TEST 3: assured bandwidth restoration time (§7.4.2): step 0 → above RF+RA; to first US frame of the K-window meeting it; target 2 ms; three spools
        self.beat("g4")
        self.play(FadeOut(VGroup(cap, capl, segs, c0, idl, dl, da, ov, capl2, over, ovl, cnt)), run_time=0.4)
        h = step_head(self, 3, "Geri gelme süresi — §7.4.2", h)
        ox, oy, sx, sy = -5.8, -2.2, 0.27, 0.9
        P = lambda f, r: np.array([ox + f * sx, oy + r * sy, 0])
        xa = arrow(P(0, 0), P(25, 0), MUTED, 2, 0.1)
        ya = arrow(P(0, 0), P(0, 3.6), MUTED, 2, 0.1)
        xal = T("↑ çerçeveler (ONU'da)", 14, MUTED, BOLD).next_to(xa, DOWN, buff=0.06).align_to(xa, RIGHT)
        g = DashedLine(P(0, 2.0), P(24, 2.0), color=GOOD, stroke_width=2)
        gl = T("RF + RA", 14, GOOD, BOLD).next_to(P(0, 2.0), LEFT, buff=0.08)
        ld = VMobject(stroke_color=GOLD, stroke_width=3).set_points_as_corners([P(0, 0.05), P(3, 0.05), P(3, 3.0), P(24, 3.0)])
        ldl = T("sunulan yük", 14, GOLD, BOLD).next_to(P(24, 3.0), UP, buff=0.06).shift(LEFT * 0.4)
        pts = [P(f, 2.15 * (1 - np.exp(-(f - 3) / 4.5)) if f > 3 else 0.12) for f in np.linspace(0, 24, 49)]
        asg = VMobject(stroke_color=ACC, stroke_width=3).set_points_smoothly(pts)
        asl = T("atanan (ortalama)", 14, ACC, BOLD).move_to(P(18.5, 1.45))
        mk = VGroup(DashedLine(P(3, -0.05), P(3, 3.3), color=GOLD, stroke_width=1.6), DashedLine(P(15, -0.05), P(15, 3.3), color=ACC, stroke_width=1.6))
        br = BraceBetweenPoints(P(3, 3.4), P(15, 3.4), UP, color=GOOD)
        brl = T("geri gelme süresi · hedef 2 ms = 16 çerçeve", 15, GOOD, BOLD).next_to(br, UP, buff=0.04)
        kw = T("K penceresinin ilk ↑ çerçevesi", 14, ACC, BOLD).next_to(P(15, 0.65), RIGHT, buff=0.1)
        sp = VGroup(*[spool(s, FEED, 0.3) for s in ("0 km", "20 km", "40 km")]).arrange(RIGHT, buff=0.45).move_to([4.3, 0.95, 0])
        dd = VGroup()
        for i, (d, a) in enumerate(((0.15, 1.2), (0.7, 1.2), (1.3, 1.2))):
            yy = -0.6 - i * 0.6
            r1 = Rectangle(width=d, height=0.36, stroke_width=0, fill_color=FEED, fill_opacity=0.55).move_to([2.3 + d / 2, yy, 0])
            r2 = Rectangle(width=a, height=0.36, stroke_width=0, fill_color=ACC, fill_opacity=0.45).next_to(r1, RIGHT, buff=0)
            dd.add(VGroup(T(("0", "20", "40")[i] + " km", 14, MUTED, BOLD).next_to(r1, LEFT, buff=0.12), r1, r2))
        ddl = VGroup(VGroup(Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=FEED, fill_opacity=0.55), T("mesafe", 14, FEED, BOLD)).arrange(RIGHT, buff=0.08),
                     VGroup(Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=ACC, fill_opacity=0.45), T("algoritma", 14, ACC, BOLD)).arrange(RIGHT, buff=0.08)).arrange(RIGHT, buff=0.3)
        ddl.next_to(dd, DOWN, buff=0.2).align_to(dd, LEFT)
        self.play(self.set_src("G.989.3 §7.4.2 · yöntem: yorum"), Create(xa), Create(ya), FadeIn(xal), Create(g), FadeIn(gl), run_time=0.6)
        self.at(self.cue("yükünü sıfırdan garantili", 2.5))
        self.play(Create(ld), FadeIn(ldl), Create(mk[0]), run_time=0.8)
        self.at(self.cue("ilk yukarı yön çerçevesine", 10.0))
        self.play(Create(asg), FadeIn(asl), run_time=1.2)
        self.play(Create(mk[1]), FadeIn(kw), run_time=0.5)
        self.at(self.cue("Hedef iki milisaniyedir", 17.0))
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.6)
        self.at(self.cue("Üç makarada", 19.0))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.06) for s in sp], lag_ratio=0.2), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.06) for d in dd], lag_ratio=0.2), FadeIn(ddl), run_time=0.8)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep14_labA")


class E14LabB(Act14):
    HDR, MANIFEST, PREV_BADGE = H14["L"], M14("lab"), "lab"

    def construct(self):
        # g5 — TEST 4: convergence (§7.4.3): single change → all unsaturated within e.g. 20 %; target 6 ms, expected 10 ms; measured on the DS frame
        self.beat("g5")
        h = step_head(self, 4, "Yakınsama — §7.4.3")
        ox, oy, sx, sy = -5.8, -1.95, 0.08, 1.0
        P = lambda f, r: np.array([ox + f * sx, oy + r * sy, 0])
        xa = arrow(P(0, 0), P(96, 0), MUTED, 2, 0.1)
        xal = T("↓ çerçeveler (BWmap)", 14, MUTED, BOLD).next_to(xa, DOWN, buff=0.06).align_to(xa, RIGHT)
        cols = [ACC, PINK, GOLD]
        lv = [2.6, 1.7, 0.8]
        bands = VGroup(*[Rectangle(width=P(96, 0)[0] - P(0, 0)[0], height=0.2 * v * sy * 0.5, stroke_width=0, fill_color=c, fill_opacity=0.15).move_to(
            [(P(0, 0)[0] + P(96, 0)[0]) / 2, P(0, v)[1], 0]) for v, c in zip(lv, cols)])
        lines = VGroup()
        for k, (v, c) in enumerate(zip(lv, cols)):
            amp = (0.7, -0.6, 0.45)[k]
            pts = [P(f, v + (0 if f < 8 else amp * np.exp(-(f - 8) / 11.0) * np.cos((f - 8) / 6.0))) for f in np.linspace(0, 95, 96)]
            lines.add(VMobject(stroke_color=c, stroke_width=2.6).set_points_smoothly(pts))
        ev = VGroup(DashedLine(P(8, -0.05), P(8, 3.75), color=WARN, stroke_width=2), T("tek ONU'da yük değişir", 14, WARN, BOLD).next_to(P(8, 3.75), RIGHT, buff=0.08))
        t6 = VGroup(DashedLine(P(56, -0.05), P(56, 3.3), color=GOOD, stroke_width=2), T("6 ms = 48 çerçeve · hedef", 14, GOOD, BOLD).next_to(P(56, 3.3), UP, buff=0.04))
        t10 = VGroup(DashedLine(P(88, -0.05), P(88, 3.3), color=GOLD, stroke_width=2), T("10 ms · beklenen", 14, GOLD, BOLD).next_to(P(88, 3.3), UP, buff=0.04))
        bl = VGroup(Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=ACC, fill_opacity=0.3), T("model ± %20 (örn.)", 15, TXT, BOLD)).arrange(RIGHT, buff=0.1)
        bl.move_to([4.3, 1.0, 0])
        cmp_ = VGroup(VGroup(tag("yakınsama", GOLD, 15), T("↓ BWmap çerçevesinde · OLT", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                      VGroup(tag("geri gelme", GOOD, 15), T("↑ çerçevede · ONU'da", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cmp_.move_to([4.35, -0.5, 0])
        self.play(self.set_src("G.989.3 §7.4.2 · §7.4.3 · yöntem: yorum"), Create(xa), FadeIn(xal), run_time=0.5)
        self.at(self.cue("tek bir ONU'nun yükünü", 2.0))
        self.play(Create(ev[0]), FadeIn(ev[1]), *[Create(l) for l in lines], run_time=1.2)
        self.at(self.cue("yüzde yirmisi içine", 9.0))
        self.play(*[FadeIn(b) for b in bands], FadeIn(bl), run_time=0.6)
        self.at(self.cue("Hedef altı", 15.0))
        self.play(Create(t6[0]), FadeIn(t6[1]), run_time=0.5)
        self.at(self.cue("beklenen on", 15.9))
        self.play(Create(t10[0]), FadeIn(t10[1]), run_time=0.5)
        self.at(self.cue("aşağı yön çerçevesinde ölçülür", 18.5))
        self.play(FadeIn(cmp_[0], shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("geri gelme süresi ise ONU'da", 22.7))
        self.play(FadeIn(cmp_[1], shift=LEFT * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # g6 — TEST 5: delay and jitter UNI → SNI with RF only / SR only / both; vary polling; model worst case ≈ 700 µs (20 km), 1 ms (40 km)
        self.beat("g6")
        self.play(FadeOut(VGroup(xa, xal, bands, lines, ev, t6, t10, bl, cmp_)), run_time=0.4)
        h = step_head(self, 5, "Gecikme ve titreşim", h)
        y = 0.95
        tg = tg_icon(1.8, 1.25, "Trafik üreteci").move_to([-5.3, y, 0])
        onu = onu_box("ONU", ONUC, 1.2, 0.55, 16).move_to([-2.6, y, 0])
        sp = spool("20 / 40 km", FEED, 0.32).move_to([-0.6, y - 0.1, 0])
        olt = ct_box("OLT", OLTC, 1.2, 0.55, 16).move_to([1.4, y, 0])
        a1 = arrow(tg[0].get_right(), onu.get_left(), SAC, 2, 0.1)
        a2 = Line(onu.get_right(), sp[0].get_left(), color=FEED, stroke_width=2.5)
        a3 = Line(sp[0].get_right(), olt.get_left(), color=FEED, stroke_width=2.5)
        back = CurvedArrow(olt.get_bottom() + DOWN * 0.05, tg[0].get_right() + DOWN * 0.42, angle=-0.35, color=SAC, stroke_width=2, tip_length=0.12)
        t1 = tag("t₁ · UNI", GOLD, 14).next_to(a1, UP, buff=0.08)
        t2 = tag("t₂ · SNI", GOLD, 14).next_to(olt, RIGHT, buff=0.2)
        modes = VGroup(*[tag(s, c, 17) for s, c in (("yalnızca sabit tahsis (RF)", FXC), ("yalnızca raporlama (SR)", SRC), ("ikisi birlikte", GOLD))]).arrange(RIGHT, buff=0.3)
        modes.move_to([0, -1.25, 0])
        pol = VGroup(T("yoklama aralığı:", 17, MUTED, BOLD), Line(LEFT * 1.0, RIGHT * 1.0, color=TBC, stroke_width=4),
                     T("125 µs … 1 ms", 17, TBC, BOLD)).arrange(RIGHT, buff=0.2).move_to([3.3, -0.15, 0])
        knob = Circle(radius=0.11, color=TXT, fill_color=TXT, fill_opacity=1).move_to(pol[1].get_left())
        exp = VGroup(T("model · en kötü · her çerçeve yoklama:", 16, MUTED, BOLD), pill("20 km ≈ 700 µs", ACC, 18), pill("40 km ≈ 1 ms", WARN, 18)).arrange(RIGHT, buff=0.25)
        exp.move_to([0, -2.4, 0])
        self.play(self.set_src("G.989.3 §7.3.7 · §13.1 · model: hesap"), FadeIn(tg), FadeIn(onu), FadeIn(sp), FadeIn(olt), Create(a2), Create(a3), run_time=0.6)
        self.at(self.cue("Zaman damgalı paketleri", 2.8))
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.5)
        self.play(Create(back), FadeIn(t2), run_time=0.6)
        for k, (key, d) in enumerate((("yalnızca sabit tahsisle", 8.3), ("yalnızca raporlamayla", 10.4), ("ve ikisi birlikte", 12.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(modes[k], shift=UP * 0.06), run_time=0.35)
        self.at(self.cue("yoklama aralığını değiştirin", 13.7))
        self.play(FadeIn(pol), FadeIn(knob), run_time=0.4)
        self.play(knob.animate.move_to(pol[1].get_right()), run_time=0.8)
        self.at(self.cue("Bizim modelimiz", 16.2))
        self.play(FadeIn(exp[0]), run_time=0.4)
        self.at(self.cue("yedi yüz mikrosaniye", 21.0))
        self.play(FadeIn(exp[1], scale=0.9), run_time=0.4)
        self.at(self.cue("kırk kilometrede bir milisaniye", 25.0))
        self.play(FadeIn(exp[2], scale=0.9), run_time=0.4)
        self.end(pad=0.05)

        # g7 — TEST 6: polling cost: 32 → 256 polled ONUs, one DBRu-only burst each per frame; our table (2,5G, FEC off): 6 / 12,5 / 25 / 50 %
        self.beat("g7")
        self.play(FadeOut(VGroup(tg, onu, sp, olt, a1, a2, a3, back, t1, t2, modes, pol, knob, exp)), run_time=0.4)
        h = step_head(self, 6, "Yoklamanın bedeli", h)
        x0, W = -2.2, 7.6
        ax, X = lin_axis(0, 100, x0, x0 + W, -2.15, [0, 25, 50, 75, 100], size=15, fmt=lambda v: f"%{v}")
        axl = T("verim kaybı · yukarı yön zamanı", 15, MUTED, BOLD).next_to(ax, DOWN, buff=0.08)
        rows = VGroup()
        for i, (n, v, vt) in enumerate(POLL):
            yy = 1.2 - i * 0.78
            rl = T(n, 19, TXT, BOLD).move_to([x0 - 0.3, yy, 0], aligned_edge=RIGHT)
            b = hbar(x0, yy, X(v) - x0, (GOOD, GOLD, WARN, WARN)[i], 0.46, 0.5, vt, 18, (GOOD, GOLD, WARN, WARN)[i])
            rows.add(VGroup(rl, b))
        dbl = T("× 2", 16, MUTED, BOLD).next_to(rows[0][0], LEFT, buff=0.4).shift(DOWN * 0.4)
        bi = VGroup(Rectangle(width=0.64, height=0.4, stroke_width=0, fill_color=OVC, fill_opacity=0.6), Rectangle(width=0.12, height=0.4, stroke_width=0, fill_color=BWC, fill_opacity=0.7)).arrange(RIGHT, buff=0)
        bil = VGroup(bi, T("her ONU · her çerçeve: yalnızca DBRu taşıyan burst (19 TQ)", 16, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0.4, 1.95, 0])
        hk = tag("tablomuz · 2,5G · FEC kapalı", GOLD, 15).next_to(ax, UP, buff=0.12).align_to(ax, RIGHT)
        self.play(self.set_src("G.989.2 Tablo 11-11 · G.989.3 §8.1.1.3 · hesap"), run_time=0.3)
        self.at(self.cue("otuz ikiden başlayıp", 2.6))
        self.play(LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.06) for r in rows], lag_ratio=0.15), Create(ax), FadeIn(axl), run_time=0.9)
        self.at(self.cue("yalnızca rapor taşıyan", 10.4))
        self.play(FadeIn(bil, shift=DOWN * 0.06), run_time=0.5)
        self.at(self.cue("Bizim tablomuz", 15.9))
        self.play(FadeIn(hk), run_time=0.4)
        for k, (key, d) in enumerate((("yüzde altı", 20.1), ("on iki buçuk", 21.0), ("yirmi beş ve", 22.1), ("ve elli verim", 23.0))):
            self.at(self.cue(key, d))
            self.play(GrowFromEdge(rows[k][1][0], LEFT), FadeIn(rows[k][1][1]), run_time=0.35)
        self.end(pad=0.05)

        # g8 — TEST 7: report signal: known BufOcc values, < 8 B = 2 units, 0 empty, all-ones invalid; corrupt CRC → discard; no double grant
        self.beat("g8")
        self.play(FadeOut(VGroup(ax, axl, rows, bil, hk)), run_time=0.4)
        h = step_head(self, 7, "Rapor sinyali — DBRu", h)
        rows_ = [["SDU 6 B kuyrukta", "BufOcc'ta 2 birim"], ["BufOcc 0x000000", "boş"], ["BufOcc 0xFFFFFF", "geçersiz ölçüm"], ["CRC-8 bozuk", "rapor atılır"],
                 ["rapor + aynı tahsisteki veri", "aynı bayt iki kez tahsis edilmez"]]
        tb = mtable(["ONU emülatörü gönderir", "OLT'den beklenen"], rows_, [5.0, 5.4], size=18, hsize=16, row_h=0.5).move_to([-0.4, 0.15, 0])
        ck = VGroup(*[ok_x(True, 20).move_to([tb.get_right()[0] + 0.35, r.get_y(), 0]) for r in tb[1:]])
        self.play(self.set_src("G.989.3 §8.1.2.2 · (8-1) · yorum"), FadeIn(tb[0]), run_time=0.4)
        self.at(self.cue("bilinen doluluklar", 2.3))
        self.play(FadeIn(tb[1][:2]), run_time=0.4)
        cues = (("küçük birimler iki", 5.9), ("sıfır boş", 8.9), ("hepsi bir geçersizdir", 9.7), ("OLT raporu atmalıdır", 13.2), ("iki kez tahsis etmediğini", 17.0))
        for k, (key, d) in enumerate(cues):
            self.at(self.cue(key, d))
            if k in (1, 2):
                self.play(FadeIn(tb[k + 1], shift=UP * 0.05), FadeIn(ck[k]), run_time=0.35)
            elif k == 0:
                self.play(FadeIn(tb[1][2], shift=LEFT * 0.05), FadeIn(ck[0]), run_time=0.35)
            else:
                self.play(FadeIn(tb[k + 1], shift=UP * 0.05), FadeIn(ck[k]), run_time=0.4)
            if k == 2:
                self.at(self.cue("Sonra CRC'yi bozun", 11.6))
                self.play(FadeIn(tb[4][:2], shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep14_labB")


class E14LabC(Act14):
    HDR, MANIFEST, PREV_BADGE = H14["L"], M14("lab"), "lab"

    def construct(self):
        # g9 — TEST 8: traffic monitoring (data vs idle fill at equal DBRu) + BWmap rule audit
        self.beat("g9")
        h = step_head(self, 8, "Trafik izleme ve harita kuralları")
        rows = VGroup()
        for i, (lab, c, ws) in enumerate((("veriyle doldur", SAC, (2.4, 2.4, 2.4)), ("boş XGEM ile doldur", IDC, (2.4, 1.5, 0.8)))):
            yy = 1.2 - i * 1.0
            l_ = tag(lab, c, 16).move_to([-5.2, yy, 0])
            gs = VGroup(*[Rectangle(width=w, height=0.42, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.4 if c == SAC else 0.55) for w in ws])
            for k, gg in enumerate(gs):
                gg.move_to([-3.4 + k * 2.9, yy, 0], aligned_edge=LEFT)
            rows.add(VGroup(l_, gs))
        same = T("aynı DBRu değerleri", 15, BWC, BOLD).next_to(rows, UP, buff=0.1).align_to(rows[1][1], LEFT)
        res = VGroup(T("tahsis küçülüyor mu?", 16, TXT, BOLD), T("→ TM çalışıyor", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.15).next_to(rows[1][1], DOWN, buff=0.15).align_to(rows[1][1][2], LEFT)
        rules = check_list(["≤ 512 yapı / BWmap · ≤ 16 seri ve ≤ 64 yapı / ONU", "artan StartTime", "burst'ler arası koruma aralığı", "FEC bloklarına hizalama"], 18, buff=0.18)
        rules.move_to([-0.6, -1.75, 0])
        for r in rules:
            r[0].set_opacity(0)
        self.play(self.set_src("G.989.3 §7.2.3 · §9.1.4 · §8.1.1.3 · §10.1.3.2.3"), FadeIn(same), run_time=0.4)
        self.at(self.cue("bir kez veriyle", 2.5))
        self.play(FadeIn(rows[0][0]), LaggedStart(*[FadeIn(g) for g in rows[0][1]], lag_ratio=0.2), run_time=0.7)
        self.at(self.cue("bir kez boş çerçevelerle", 6.7))
        self.play(FadeIn(rows[1][0]), LaggedStart(*[FadeIn(g) for g in rows[1][1]], lag_ratio=0.2), run_time=0.7)
        self.at(self.cue("küçülüp küçülmediğini", 9.6))
        self.play(FadeIn(res, shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("harita kurallarını denetleyin", 13.4))
        self.play(FadeIn(VGroup(*[r[1] for r in rules]), shift=UP * 0.06), run_time=0.5)
        for k, (key, d) in enumerate((("yapı sınırları", 16.4), ("artan başlangıç", 17.7), ("burst'ler arası koruma", 19.9), ("FEC bloklarına hizalama", 22.0))):
            self.at(self.cue(key, d))
            self.play(rules[k][0].animate.set_opacity(1), run_time=0.3)
        self.end(pad=0.05)

        # g10 — TEST 9: golden vector IV.9 (Assign_Alloc-ID, ONU-ID 19, SeqNo 3, Alloc-ID 1093, type 1): published MIC matches only with scope 0x0000 (calc)
        self.beat("g10")
        self.clear(h)
        h = step_head(self, 9, "Altın vektör — Ek IV.9", h)
        p = apanel(6.6, 2.6, "Assign_Alloc-ID · Ek IV.9 · oktetler", GOLD).move_to([-3.05, 0.85, 0])
        hx = VGroup(VGroup(HX("00 13", 20, ACC, BOLD), HX("0A", 20, GOLD, BOLD), HX("03", 20, MUTED, BOLD), HX("04 45", 20, ACC, BOLD), HX("01", 20, PINK, BOLD),
                           HX("?? ??", 20, CH[1], BOLD)).arrange(RIGHT, buff=0.22),
                    HX("00 … 00 (oktet 10–40)", 18, MUTED, BOLD),
                    VGroup(T("MIC:", 16, MUTED, BOLD), HX("46 39 87 56 28 08 14 e6", 20, HECC, BOLD)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        hx.move_to(p[0]).shift(DOWN * 0.2)
        dec = VGroup(kv("ONU-ID", "0x0013 = 19", kw=1.7), kv("SeqNo", "0x03 = 3", kw=1.7), kv("Alloc-ID", "0x0445 = 1093", kw=1.7), kv("tür", "0x01", kw=1.7)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        dec.move_to([3.6, 0.85, 0])
        r0 = VGroup(T("kapsam", 17, MUTED, BOLD), HX("0x0000", 20, GOOD, BOLD), T("→ MIC tutar", 17, GOOD, BOLD), ok_x(True, 20)).arrange(RIGHT, buff=0.2)
        r1 = VGroup(T("kapsam", 17, MUTED, BOLD), HX("0xFFFF", 20, WARN, BOLD), T("→", 17, MUTED), HX("70 8d 8d d1 79 4c 0e 8c", 18, WARN, BOLD), ok_x(False, 20)).arrange(RIGHT, buff=0.2)
        rr = VGroup(r0, r1).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-1.2, -1.35, 0])
        hk = tag("hesap · AES-CMAC-64", GOLD, 15).next_to(rr, RIGHT, buff=0.4)
        fix = VGroup(T("vektör, metnin yazmadığı değeri sabitliyor:", 17, TXT, BOLD), HX("kapsam = 0x0000 · bütün kanallar geçerli", 18, GOOD, BOLD)).arrange(RIGHT, buff=0.2)
        fit(fix, 12.6).move_to([0, -2.65, 0])
        self.play(self.set_src("G.989.3 Ek IV.9 · Tablo 11-11 · MIC: hesap"), FadeIn(p), run_time=0.4)
        self.at(self.cue("ekin dokuzuncu örneği", 2.7))
        self.play(FadeIn(hx[0][:2]), FadeIn(hx[1]), FadeIn(hx[2]), run_time=0.6)
        for k, (key, d) in enumerate((("ONU kimliği on dokuz", 8.3), ("sıra numarası üç", 10.1), ("bin doksan üç", 12.0), ("tür bir", 14.0))):
            self.at(self.cue(key, d))
            anims = [FadeIn(dec[k], shift=LEFT * 0.06)]
            anims.append(FadeIn(hx[0][k + 1]) if k else Indicate(hx[0][0], color=ACC, scale_factor=1.15))
            self.play(*anims, run_time=0.4)
        self.at(self.cue("yayımlanan bütünlük kodu", 15.5))
        self.play(FadeIn(hx[0][5]), Indicate(hx[2][1], color=HECC, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("yalnızca kapsam alanı sıfırken", 18.3))
        self.play(FadeIn(r0, shift=UP * 0.06), FadeIn(hk), run_time=0.5)
        self.play(FadeIn(r1, shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("bütün kanallar geçerliyken", 21.5))
        self.play(Transform(hx[0][5], HX("00 00", 20, GOOD, BOLD).move_to(hx[0][5])), run_time=0.5)
        self.at(self.cue("metnin yazmadığı", 24.7))
        self.play(FadeIn(fix, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # g11 — invalid Alloc-ID in the ONU's own channel → silence; contention only if contracted: capability fields, forced SN collisions, ≈ 4,5 rounds, 50 ms
        self.beat("g11")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = self.heading12("Kapsam ve çekişme (sözleşmedeyse)", None, 10.0)
        L = frame_box("kapsam: kendi kanalında geçersiz", CH[1], 6.0, 3.4, 17).move_to([-3.2, -0.15, 0])
        bits = VGroup(*[VGroup(Rectangle(width=0.34, height=0.36, stroke_color=CH[1], stroke_width=1.3, fill_color=WARN if i == 13 else PANEL,
                                         fill_opacity=0.55 if i == 13 else 1)) for i in range(16)]).arrange(RIGHT, buff=0).move_to([-3.2, 0.65, 0])
        bl = T("UWLCH 0010 → bit = 1", 15, WARN, BOLD).next_to(bits, DOWN, buff=0.1)
        gr = VGroup(tile("BWmap: Alloc-ID 1100", BWC, 2.6, 0.45, 15, 0.2), T("→", 18, MUTED, BOLD), DashedVMobject(Rectangle(width=1.2, height=0.42, stroke_color=MUTED, stroke_width=1.6), num_dashes=14))
        gr.arrange(RIGHT, buff=0.15).move_to([-3.4, -0.65, 0])
        sil = VGroup(T("ONU cevap vermez", 17, GOOD, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.1).move_to([-3.2, -1.35, 0])
        R = frame_box("çekişme · Ek J / Ek K", GOLD, 6.0, 3.4, 17).move_to([3.2, -0.15, 0])
        cap = VGroup(tag("Ack · oktet 10–13", GOOD, 15), tag("Tuning_Response · 36–39", GOOD, 15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.2, 0.45, 0])
        capl = T("yetenek alanları", 15, GOOD, BOLD).next_to(cap, RIGHT, buff=0.2)
        col = VGroup(onu_box("ONU 1", ONUC, 1.0, 0.42, 14), onu_box("ONU 2", ONUC, 1.0, 0.42, 14)).arrange(RIGHT, buff=0.3).move_to([1.6, -0.6, 0])
        sn = tile("SN tahsisi · 1021", GOLD, 2.0, 0.42, 14, 0.2).move_to([4.5, -0.6, 0])
        ca = VGroup(arrow(col[1].get_right(), sn.get_left(), WARN, 1.6, 0.08),
                    CurvedArrow(col[0].get_bottom(), sn.get_bottom() + LEFT * 0.4, angle=0.45, color=WARN, stroke_width=1.6, tip_length=0.08))
        cx = xmark(Square(0.2).move_to(sn.get_left() + LEFT * 0.35), WARN, 3)
        ms = VGroup(pill("≈ 4,5 tur (ort.)", GOLD, 17), pill("aralık ≥ 50 ms", WARN, 17)).arrange(RIGHT, buff=0.2).move_to([3.2, -1.45, 0])
        self.play(self.set_src("G.989.3 Tablo 11-11 · Ek J · Ek K · benzetim: hesap"), FadeIn(L), FadeIn(bits), FadeIn(bl), run_time=0.6)
        self.at(self.cue("kendi kanalında geçersiz", 3.0))
        self.play(FadeIn(gr, shift=RIGHT * 0.06), run_time=0.5)
        self.play(FadeIn(sil, shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("yalnızca sözleşmedeyse", 8.0))
        self.play(FadeIn(R), run_time=0.4)
        self.at(self.cue("yetenek alanlarını okuyun", 11.6))
        self.play(FadeIn(cap, shift=UP * 0.06), FadeIn(capl), run_time=0.5)
        self.at(self.cue("bilerek çarpıştırın", 15.0))
        self.play(FadeIn(col), FadeIn(sn), GrowArrow(ca[0]), Create(ca[1]), Create(cx), run_time=0.6)
        self.at(self.cue("dört buçuk turu", 18.4))
        self.play(FadeIn(ms[0], scale=0.9), run_time=0.4)
        self.at(self.cue("elli milisaniyelik aralığı", 21.0))
        self.play(FadeIn(ms[1], scale=0.9), run_time=0.4)
        self.end(pad=0.05)

        # g12 — lab note
        self.note11("g12", [("1", "Her DBA ölçümünü bağlamıyla kaydedin",
                             "mesafe · FEC durumu · burst profili: aynı algoritma 40 km'de başka bir gecikme verir", "her DBA ölçümünü"),
                            ("2", "İş birlikli yöntemin standart arayüzü yok",
                             "sınamak için üreticinin Ek IX'taki üç referans noktasından birine açtığı arayüz gerekir", "iş birlikli yöntem için")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep14_labC")


POINTS = [("Alloc-ID 14 bit, bütün sistemde tek · bir ODN'de ≤ 1021 ONU\ntanımlayıcı: RF · RA · RM · χAB · P · ω + değersiz TJT · TBDT · TPST", "§6.1.5.7 · §7.1"),
          ("DBA zorunlu (SR + TM birlikte);\nalgoritma ve zamanlayıcı üreticinin", "§7.2"),
          ("Katı sıra: sabit > güvenceli > güvencesiz > en iyi çaba;\nNA doymadıkça BE sıfır alabilir", "§7.3"),
          ("Kıt kaynak burst sayısı · mesafe boru hattı kurar:\n40 km'de salt raporlamanın tabanı ≈ 1 ms (model)", "§13.1 · hesap"),
          ("Çekişmeli işletim koşullu; çarpışma çözümünün\ntek zaman sayısı gerekçesiz 50 ms", "Ek J · Ek K")]


class E14End(Act14):
    HDR, MANIFEST, FIRST = H14["E"], M14("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header(tc)
        self.set_badge("ozet")
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.4)
            ch = tag(c, GOLD, 16)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.75, -2.4, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.6, y, 0])
        for k, (key, d) in enumerate((("tahsis kimliği on dört bittir", 1.5), ("DBA zorunludur", 21.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((2, 3, 4), (("referans model katı", 0.3), ("kıt kaynak burst", 8.9), ("çekişmeli işletim koşulludur", 20.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Tam yüklü kanalda RM = 1 Gbit/s\nolan BE T-CONT hiç pay almıyor,\nNA T-CONT doymamış.\nOLT bozuk mu?", CH[0]),
            ("1 kuantum / çerçeve neden\n2,5G'de 256 kbit/s,\n10G'de 1,024 Mbit/s?\nEn küçük yük tahsisi?", CH[1]),
            ("Tahsisleri geri çekilmiş\nboştaki bir ONU, trafiği gelince\nonları nasıl geri ister?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 13.6), ("Üçüncü soru", 27.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 38.0))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: Yönetim Kanalları (48-byte PLOAM, MIC, SeqNo, catalogue, OMCC)
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e5 = SERIES["season2"]["episodes"][4]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e5['n']} · {e5['title']}", 50, TXT, BOLD), T(e5["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        fit(nxt[1], 12.6)
        pl = octets([("ONU-ID", 2, ACC, "1–2"), ("tür", 1.3, GOLD, "3"), ("SeqNo", 1.3, MUTED, "4"), ("mesaj içeriği · 36 B", 6.0, PLC, "5–40"), ("MIC · 8 B", 2.4, HECC, "41–48")],
                    10.4, 0.6, 17, 14).move_to([0, -1.15, 0])
        pll = T("PLOAM mesajı · 48 bayt", 16, PLC, BOLD).next_to(pl, UP, buff=0.1).align_to(pl, LEFT)
        tg_ = VGroup(tag("bütünlük kodu", HECC, 15), tag("sıra numaraları", MUTED, 15), tag("mesaj kataloğu", PLC, 15), tag("OMCC", OMC, 15)).arrange(RIGHT, buff=0.2)
        tg_.next_to(pl, DOWN, buff=0.55)
        bb = VGroup(tag("Assign_Alloc-ID", GOLD, 15), tag("Acknowledgement", GOLD, 15), T("→ bayt bayt", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.2).next_to(tg_, DOWN, buff=0.25)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("kırk sekiz baytlık", 3.0))
        self.play(FadeIn(nxt[2]), FadeIn(pll), LaggedStart(*[FadeIn(c) for c in pl], lag_ratio=0.1), run_time=0.8)
        self.at(self.cue("bütünlük kodu ve sıra", 6.8))
        self.play(FadeIn(tg_[:2], shift=UP * 0.06), Indicate(pl[4], color=HECC), run_time=0.6)
        self.at(self.cue("mesaj kataloğu", 9.6))
        self.play(FadeIn(tg_[2], shift=UP * 0.06), run_time=0.35)
        self.at(self.cue("ve OMCC", 10.9))
        self.play(FadeIn(tg_[3], shift=UP * 0.06), run_time=0.35)
        self.at(self.cue("atama ve onay mesajlarını", 13.0))
        self.play(FadeIn(bb, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(pl, pll, tg_, bb)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP14['n']} · {EP14['title']}", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Coqui XTTS-v2 — ses: Ana Florence (yerel GPU)", 22, ACC, BOLD),
                    T("(Coqui Public Model License — ticari olmayan kullanım)", 18, ACC),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.3 (2021)/Amd.1 (2023)/Amd.2 (2025) · ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020)", 18, MUTED)).arrange(DOWN, buff=0.3)
        fit(cr, 13.2)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep14_end")
