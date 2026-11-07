"""B10 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to the B09 quiz."""
from ep10_common import *

AGENDA = ["İzleme: cihaz kendini ölçer", "Koruma: ONU'ya dokunmadan", "Uyumluluk: 42 tablo, tek matris",
          "Bir ONU'nun hayatı", "Sahada: arızalar, ölçüm çantası"]
PX, PY = 3.4, -0.45


class Ep10Open(Act10):
    MANIFEST, FIRST = M10("open"), True

    def construct(self):
        self.beat("o1")
        tag_ = T(f"BÖLÜM {EP10['n']} · {tr_upper(EP10['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        fin = pill("SEZON FİNALİ", GOLD, 18).move_to([PX + 0.2, PY + 2.25, 0])
        num = T(f"{EP10['n']:02d}", 120, ACC, BOLD)
        sub = fit(T(EP10["sub"], 24, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP10["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX + 0.2, PY + 0.35, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(fin), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        eps = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.07, width=0.5, height=0.5, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                              T(str(i + 1), 18, MUTED, BOLD)) for i in range(9)])
        for e in eps:
            e[1].move_to(e[0])
        eps.arrange(RIGHT, buff=0.12).move_to([PX + 0.2, PY - 2.1, 0])
        etl = T("tablolar → saha", 16, GOLD, BOLD).next_to(eps, DOWN, buff=0.14)
        self.at(self.cue("Dokuz bölüm boyunca", 2.9))
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in eps], lag_ratio=0.1), run_time=1.2)
        self.at(self.cue("sahaya taşıyoruz", 7.8))
        self.play(*[e[0].animate.set_stroke(GOLD) for e in eps], *[e[1].animate.set_color(GOLD) for e in eps], FadeIn(etl, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(cover, eps, etl, fin)

        # o2 — monitoring
        self.beat("o2")
        cx = PX + 0.2
        olt = sbox("OLT", None, OLTC, 1.3, 0.7, 19).move_to([cx - 2.0, PY + 1.35, 0])
        onu = sbox("ONU", None, ONUC, 1.3, 0.7, 19).move_to([cx + 2.0, PY + 1.35, 0])
        fib = Line(olt.get_right(), onu.get_left(), color=FEED, stroke_width=3)
        g1 = gauge(0.3, ACC).next_to(olt, DOWN, buff=0.2)
        g2 = gauge(0.3, ACC).next_to(onu, DOWN, buff=0.2)
        axg, X = lin_axis(-56, 0, cx - 2.8, cx + 2.8, PY - 1.55, [-50, -40, -30, -20, -10, 0], size=13, unit="alınan güç (dBm)")
        win = Rectangle(width=X(-4.9) - X(-53), height=0.4, stroke_width=0, fill_color=ACC, fill_opacity=0.75).move_to([(X(-53) + X(-4.9)) / 2, PY - 1.05, 0])
        wl = T("−53 … −4,9 dBm", 16, BG, BOLD).move_to(win)
        trust = pill("ne kadar güvenilir?  ±3 dB", GOLD, 17).move_to([cx, PY + 0.2, 0])
        self.focus(0, VGroup(olt, onu, fib, g1, g2, axg, win, wl, trust))
        self.play(FadeIn(olt), FadeIn(onu), Create(fib), run_time=0.6)
        self.at(self.cue("kendi optik durumunu", 1.0))
        self.play(FadeIn(g1, scale=0.8), FadeIn(g2, scale=0.8), run_time=0.5)
        self.play(Create(axg[0]), FadeIn(axg[1:]), GrowFromEdge(win, LEFT), FadeIn(wl), run_time=0.8)
        self.at(self.cue("ne kadar güvenebiliriz", 5.3))
        self.play(FadeIn(trust, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o3 — protection
        self.beat("o3")
        ya, yb, ys = PY + 1.25, PY - 0.25, PY + 0.5
        cta = ct_box("CT 1", CT_A, 1.3, 0.5, 16, on=True).move_to([cx - 2.35, ya, 0])
        ctb = ct_box("CT 2", CT_B, 1.3, 0.5, 16, on=False).move_to([cx - 2.35, yb, 0])
        spl = splitter(0.26).move_to([cx + 0.45, ys, 0])
        fa = Line(cta.get_right(), spl.get_left() + UP * 0.08, color=FEED, stroke_width=3)
        fb = Line(ctb.get_right(), spl.get_left() + DOWN * 0.08, color=FEED, stroke_width=3)
        onu = onu_icon("ONU", ONUC, 1.1, 0.55, 16).move_to([cx + 2.3, ys, 0])
        fo = Line(spl.get_right(), onu.get_left(), color=FEED, stroke_width=3)
        cut = xmark(Square(0.28).move_to(fa.point_from_proportion(0.5)), WARN, 4)
        ok = T("ONU: ayar yok ✓", 19, GOOD, BOLD).next_to(onu, DOWN, buff=0.2)
        cap = T("1:1 B tipi koruma", 20, ACC, BOLD).move_to([cx, PY - 1.7, 0])
        self.focus(1, VGroup(cta, ctb, spl, fa, fb, onu, fo, cut, ok, cap))
        self.play(FadeIn(cta), FadeIn(ctb), Create(fa), Create(fb), FadeIn(spl), Create(fo), FadeIn(onu), run_time=0.8)
        self.at(self.cue("besleyici fiber kesildiğinde", 1.1))
        self.play(Create(cut), fa.animate.set_color(WARN).set_opacity(0.5), run_time=0.5)
        self.play(Transform(cta[2], lamp(False, 0.08).move_to(cta[2])), Transform(ctb[2], lamp(True, 0.08).move_to(ctb[2])),
                  fb.animate.set_color(GOOD), FadeIn(cap), run_time=0.7)
        self.at(self.cue("hiç dokunmaz", 4.5))
        self.play(FadeIn(ok, shift=UP * 0.1), Indicate(onu, color=GOOD, scale_factor=1.05), run_time=0.7)
        self.end(pad=0.05)

        # o4 — conformance
        self.beat("o4")
        sq = VGroup(*[Square(0.36, stroke_color=ACC if i < 19 else CH[1], stroke_width=1.8, fill_color=ACC if i < 19 else CH[1], fill_opacity=0.25) for i in range(42)])
        sq.arrange_in_grid(rows=6, cols=7, buff=0.1).move_to([cx, PY + 0.55, 0])
        lg = VGroup(T("19 ana metin", 16, ACC, BOLD), T("23 ek", 16, CH[1], BOLD)).arrange(RIGHT, buff=0.5).next_to(sq, DOWN, buff=0.2)
        res = T("42 normatif tablo → 1 test matrisi", 20, GOOD, BOLD).move_to([cx, PY - 2.25, 0])
        self.focus(2, VGroup(sq, lg, res))
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in sq], lag_ratio=0.03), run_time=1.4)
        self.play(FadeIn(lg), run_time=0.4)
        self.at(self.cue("tek bir test matrisine", 1.6))
        frame = SurroundingRectangle(sq, color=GOOD, buff=0.12, corner_radius=0.1)
        self.play(Create(frame), FadeIn(res, shift=UP * 0.1), run_time=0.7)
        self.cur.add(frame)
        self.end(pad=0.05)

        # o5 — life of an ONU
        self.beat("o5")
        xs = np.linspace(cx - 2.8, cx + 2.8, 16)
        yl = PY + 0.4
        base = Line([xs[0], yl, 0], [xs[-1], yl, 0], color=MUTED, stroke_width=2.5)
        dots = VGroup(*[Dot([x, yl, 0], radius=0.075, color=MUTED) for x in xs])
        l0 = T("fiş", 17, ACC, BOLD).next_to(dots[0], UP, buff=0.18)
        l1 = T("acil durdurma", 17, WARN, BOLD).next_to(dots[-1], UP, buff=0.18).shift(LEFT * 0.4)
        nums = VGroup(T("0", 14, MUTED).next_to(dots[0], DOWN, buff=0.14), T("15", 14, MUTED).next_to(dots[-1], DOWN, buff=0.14))
        story = T("bütün sezon · tek hikâye", 20, GOLD, BOLD).move_to([cx, PY - 1.4, 0])
        self.focus(3, VGroup(base, dots, l0, l1, nums, story))
        self.play(Create(base), FadeIn(dots), FadeIn(nums), run_time=0.6)
        self.at(self.cue("fişe takıldığı", 1.8))
        self.play(FadeIn(l0), dots[0].animate.set_color(ACC).scale(1.5), run_time=0.4)
        self.play(LaggedStart(*[d.animate.set_color(ACC) for d in dots[1:]], lag_ratio=0.12), run_time=1.6)
        self.play(FadeIn(l1), dots[-1].animate.set_color(WARN).scale(1.5), run_time=0.4)
        self.at(self.cue("bütün sezonu", 6.0))
        self.play(FadeIn(story, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o6 — field + season 2
        self.beat("o6")
        pm = instr("PM", 1.7, 1.25, "RSSI ↔ ölçer", "±3 dB", ACC).move_to([cx - 1.6, PY + 1.3, 0])
        osa = instrument("OSA", 1.7, 1.25).move_to([cx + 1.6, PY + 1.3, 0])
        cases = VGroup(*[tag(s, c, 16) for s, c in (("LODS", WARN), ("son nefes", GOLD), ("başıboş ONU", WARN), ("acil durdurma", PINK))]).arrange(RIGHT, buff=0.15)
        fit(cases, 6.0).move_to([cx, PY - 0.55, 0])
        s2 = pill("Sezon 2 · G.989.3", ACC, 19).move_to([cx, PY - 1.85, 0])
        self.focus(4, VGroup(pm, osa, cases, s2))
        self.play(FadeIn(pm, shift=UP * 0.1), FadeIn(osa, shift=UP * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cases], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("ikinci sezona", 6.1))
        self.play(FadeIn(s2, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep10_open")

    def focus(self, k, teaser):
        it = self.items[k]
        anims = [it.animate.set_opacity(1), it[0].animate.set_color(ACC)]
        if k:
            anims += [self.items[k - 1].animate.set_opacity(0.4), self.items[k - 1][0].animate.set_color(MUTED)]
        tgt = self.bar.copy().next_to(it, LEFT, buff=0.22)
        anims.append(FadeIn(tgt) if k == 0 else Transform(self.bar, tgt))
        if k == 0:
            self.bar = tgt
        if self.cur is not None:
            anims.append(FadeOut(self.cur, shift=LEFT * 0.3))
        self.play(*anims, run_time=0.5)
        self.cur = teaser


class Ep10Recap(Act10):
    HDR, MANIFEST, FIRST = "BÖLÜM 10 · ÖNCEKİ BÖLÜMDE", M10("recap"), True

    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.25)

    def construct(self):
        # a1 — Q1: Annex A, who absorbs the ODN class
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 9 · Özel Hat")
        self.at(self.cue("Birinci soru", 1.9))
        self.to_header(tc)
        self.set_badge("ozet")
        q1 = self.qhead(1, "Ek A tablolarında ODN sınıfı büyüdükçe hangi parametreler değişir, hangileri değişmez?", CH[0])
        rows = [["↓ OLT başlatma gücü (en küçük)", "0", "+2", "+4", "+6"], ["↓ ONU hassasiyeti", "−30", "−30", "−30", "−30"],
                ["↑ ONU başlatma gücü (en küçük)", "0", "0", "0", "0"], ["↑ OLT hassasiyeti", "−30", "−32", "−34", "−36"]]
        tb = table(["dBm · Ek A sınıf 1, FEC'li", "N1", "N2", "E1", "E2"], rows, [5.0, 1.35, 1.35, 1.35, 1.35], size=21, hsize=17, row_h=0.55)
        tb.move_to([-0.9, -0.15, 0])
        for r, c in ((1, TW_DS), (4, TW_US)):
            for k in range(2, 6):
                tb[r][k].set_color(c)
        for r in (2, 3):
            tb[r].set_opacity(0.35)
        ar1 = T("+2 dB / sınıf", 18, TW_DS, BOLD).next_to(tb[1], RIGHT, buff=0.25)
        ar2 = T("−2 dB / sınıf", 18, TW_US, BOLD).next_to(tb[4], RIGHT, buff=0.25)
        same = T("aynı", 18, GOOD, BOLD).next_to(tb[2:4], RIGHT, buff=0.25)
        olt = pill("ODN sınıfını iki yönde de OLT taşır", GOLD, 19).move_to([-3.1, -2.35, 0])
        bud = VGroup(T("0 + 30 = 30 = 29 + 1,0", 18, TXT, BOLD), T("pay = 0 dB", 18, GOOD, BOLD)).arrange(RIGHT, buff=0.3).move_to([3.3, -2.35, 0])
        self.play(FadeIn(q1, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(tb[0]), FadeIn(tb[1:]), self.set_src("G.989.2 Ek A · Tablo A.2 / A.3"), run_time=0.6)
        self.at(self.cue("Aşağı yönde OLT", 6.9))
        self.play(Indicate(tb[1], color=TW_DS, scale_factor=1.02), FadeIn(ar1, shift=LEFT * 0.1), run_time=0.7)
        self.at(self.cue("yukarı yönde OLT", 12.7))
        self.play(Indicate(tb[4], color=TW_US, scale_factor=1.02), FadeIn(ar2, shift=LEFT * 0.1), run_time=0.7)
        self.at(self.cue("ONU'nun vericisi ve alıcısı", 18.2))
        self.play(tb[2].animate.set_opacity(1), tb[3].animate.set_opacity(1), FadeIn(same), run_time=0.6)
        self.at(self.cue("ODN sınıfını iki yönde", 21.6))
        self.play(FadeIn(olt, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("sıfır payla", 24.6))
        self.play(FadeIn(bud, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        # a2 — Q2: overmodulation index
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "Taban bant üst modülasyonunda %10'luk indeks nasıl tanımlanır? Zarfta kaç dB?", CH[1])
        x0, x1, yb = -6.3, -1.3, -1.0
        yav = yb + 1.25
        yhi, ylo = yav + 0.4, yav - 0.4
        pts = []
        lv = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
        w = (x1 - x0) / len(lv)
        for i, b in enumerate(lv):
            y = yhi if b else ylo
            pts += [[x0 + i * w, y, 0], [x0 + (i + 1) * w, y, 0]]
        env = VMobject(stroke_color=GOLD, stroke_width=3).set_points_as_corners(pts)
        rng = np.random.default_rng(3)
        fill = VGroup(*[Line([x0 + j * 0.06, yb, 0], [x0 + j * 0.06, (yhi if lv[min(int(j * 0.06 / w), 9)] else ylo) * 0.999 - 0.02 * rng.random(), 0],
                             color=CH[1], stroke_width=1.2, stroke_opacity=0.5) for j in range(int((x1 - x0) / 0.06))])
        lines_ = VGroup(*[DashedLine([x0, y, 0], [x1 + 0.15, y, 0], color=c, stroke_width=1.8) for y, c in ((yhi, WARN), (yav, ACC), (ylo, GOOD))])
        labs = VGroup(T("P_maks", 16, WARN, BOLD).next_to([x1 + 0.15, yhi, 0], RIGHT, buff=0.1).shift(UP * 0.08),
                      T("P_ort", 16, ACC, BOLD).next_to([x1 + 0.15, yav, 0], RIGHT, buff=0.1),
                      T("P_min", 16, GOOD, BOLD).next_to([x1 + 0.15, ylo, 0], RIGHT, buff=0.1).shift(DOWN * 0.08))
        base = Line([x0, yb, 0], [x1, yb, 0], color=MUTED, stroke_width=2)
        bl = T("115 kb/s AMCC zarfı · dikdörtgen darbeler", 15, MUTED).next_to(base, DOWN, buff=0.1)
        exa = tag("ölçek abartılı", MUTED, 14).next_to([x0, yhi, 0], UP, buff=0.25, aligned_edge=LEFT)
        f = T("M = 100 · (P_maks − P_min) / P_ort   [%]", 22, TXT, BOLD)
        fit(f, 5.6).move_to([3.7, 0.9, 0])
        m10 = T("M = %10", 26, GOLD, BOLD).move_to([3.7, 0.15, 0])
        pm5 = T("P_ort × 1,05  ·  P_ort × 0,95", 20, TXT).move_to([3.7, -0.5, 0])
        db = T("≈ ±0,2 dB", 34, GOLD, BOLD).move_to([3.7, -1.25, 0])
        pen = pill("ceza: standartta tanımsız — ölçmek size kalır", WARN, 18).move_to([0, -2.55, 0])
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.2 Ek B.2.1 · Tablo B.1"), run_time=0.6)
        self.at(self.cue("üst modülasyon indeksi", 1.0))
        self.play(Create(base), FadeIn(bl), FadeIn(fill), Create(env), FadeIn(exa), run_time=1.0)
        self.at(self.cue("zarfın en büyük", 2.9))
        self.play(Create(lines_), FadeIn(labs), run_time=0.7)
        self.play(FadeIn(f, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Yüzde on", 10.3))
        self.play(FadeIn(m10, scale=0.9), run_time=0.4)
        self.at(self.cue("simetrik bir zarfta", 11.0))
        self.play(FadeIn(pm5, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("artı eksi sıfır virgül iki", 17.2))
        self.play(FadeIn(db, scale=0.9), run_time=0.5)
        self.at(self.cue("Standart bunun", 20.9))
        self.play(FadeIn(pen, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        # a3 — Q3: why Y = S + 7
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "TWDM ONU'sunun gördüğü Y girişimcisi neden S + 7 dB?", CH[3])
        ag, Y = v_axis(-34, 12, -2.9, 1.45, -4.6, [-30, -20, -10, 0, 10], fmt=lambda v: ("+" if v > 0 else "") + tr(v))
        un = T("dBm", 15, MUTED).next_to(ag[0], UP, buff=0.08)
        DX = -2.6
        p9 = VGroup(Dot([DX, Y(9), 0], radius=0.09, color=YC), T("+9 dBm · en büyük PtP ONU gücü", 18, YC, BOLD).next_to([DX, Y(9), 0], RIGHT, buff=0.2))
        orl = arrow([DX, Y(9) - 0.12, 0], [DX, Y(-23) + 0.12, 0], WARN, 3, 0.16)
        orlt = T("− 32 dB  (ODN ORL)", 18, WARN, BOLD).next_to(orl, RIGHT, buff=0.2)
        p23 = VGroup(Dot([DX, Y(-23), 0], radius=0.09, color=YC), T("−23 dBm · geri yansıyan Y", 18, YC, BOLD).next_to([DX, Y(-23), 0], RIGHT, buff=0.2))
        s30 = VGroup(DashedLine([-4.6, Y(-30), 0], [0.2, Y(-30), 0], color=SIG, stroke_width=2.5),
                     T("S = −30 dBm · TWDM ONU hassasiyeti", 18, SIG, BOLD).next_to([0.2, Y(-30), 0], RIGHT, buff=0.15))
        br = BraceBetweenPoints([DX - 0.2, Y(-23), 0], [DX - 0.2, Y(-30), 0], LEFT, color=GOLD)
        brt = T("7 dB", 20, GOLD, BOLD).next_to(br, LEFT, buff=0.08)
        sk = VGroup(T("Y = S + 6 dB", 24, MUTED, BOLD))
        sk.add(strike(sk[0]))
        fix = VGroup(sk, Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=MUTED, stroke_width=2.5), T("S + 7 dB", 26, GOOD, BOLD), pill("Cor.1 (2019)", GOLD, 16)).arrange(RIGHT, buff=0.22)
        fix.move_to([3.55, 0.2, 0])
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.2 Tablo 10-1, Not 2 (Cor.1) · Tablo A.7"), run_time=0.6)
        self.play(Create(ag[0]), FadeIn(ag[1:]), FadeIn(un), run_time=0.5)
        self.at(self.cue("artı dokuz dBm", 6.8))
        self.play(FadeIn(p9, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("eksi otuz iki desibellik", 9.9))
        self.play(GrowArrow(orl), FadeIn(orlt), run_time=0.6)
        self.play(FadeIn(p23, shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("TWDM ONU'sunun", 15.9))
        self.play(Create(s30[0]), FadeIn(s30[1]), run_time=0.6)
        self.play(FadeIn(br), FadeIn(brt), run_time=0.4)
        self.at(self.cue("Birinci düzeltme", 21.7))
        self.play(FadeIn(fix[0][0]), run_time=0.4)
        self.play(Create(fix[0][1]), FadeIn(fix[1:], shift=LEFT * 0.1), run_time=0.7)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep10_recap")
