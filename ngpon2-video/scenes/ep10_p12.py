"""B10 · Perde 1 (optik katmanı izlemek — G.989.2 Ek II) and Perde 2 (koruma — G.989.3 §18)."""
from ep10_common import *

# ---------------------------------------------------------------- Table II.1 --
II1_H = ["Parametre", "Tipik aralık", "Çözünürlük", "Doğruluk", "Tekrarlanabilirlik", "Tepki süresi"]
II1_W = [3.1, 2.7, 1.7, 2.2, 1.9, 1.2]
II1_R = [["Sıcaklık", "−45 … +90 °C", "0,25 °C", "±3 °C", "±1 °C", "1 s"],
         ["Besleme gerilimi", "0 … 6,55 V", "%0,5 nom.", "±%3 nom.", "±%1 nom.", "1 s"],
         ["Öngerilim akımı", "0 … 819 mA", "%1 nom.", "±%10 nom.", "±%5 nom.", "1 s"],
         ["ONU gönderilen güç", "−28 … +20 dBm", "0,1 dB", "±3 dB", "±0,5 dB", "300 ns"],
         ["ONU alınan güç", "−53 … −4,9 dBm", "0,1 dB", "±3 dB (Not 5)", "±0,5 dB", "300 ns"],
         ["OLT gönderilen güç", "−28 … +20 dBm", "0,1 dB", "±2 dB", "±0,5 dB", "300 ns"],
         ["OLT alınan güç (Not 3)", "−53 … −4,9 dBm", "0,1 dB", "±2 dB (Not 5)", "±0,5 dB", "300 ns"]]
RNG, RES, ACCU, REP, RSP = 1, 2, 3, 4, 5


def ii1(row_h=0.5, y=0.3):
    return table(II1_H, II1_R, II1_W, size=19, hsize=16, row_h=row_h).move_to([0, y, 0])


class TableAct(Act10):
    def cell(self, r, c):
        return self.tb[r][1 + c]

    def show(self, cells, rt=0.5, color=GOLD, extra=()):
        """Fade in cells highlighted; previously highlighted cells settle to TXT."""
        anims = [m.animate.set_color(TXT) for m in getattr(self, "hot", [])]
        for m in cells:
            m.set_color(color)
        anims += [FadeIn(m, shift=UP * 0.05) for m in cells]
        self.play(*anims, *extra, run_time=rt)
        self.hot = list(cells)


# ================================ PERDE 1 ======================================
class E10P1A(TableAct):
    HDR, MANIFEST, FIRST = H10[1], M10("p1"), True

    def construct(self):
        self.beat("b1")
        tc = self.title_card("PERDE 1", "Optik katmanı izlemek")
        self.at(self.cue("Sahadaki bir ağ", 2.7))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Sahada ölçen: cihazın kendisi")
        pm = instrument("PM", 1.9, 1.4).move_to([-5.0, 0.55, 0])
        osc = instrument("OSC", 1.9, 1.4).move_to([-2.75, 0.55, 0])
        lab = VGroup(pm, osc)
        labt = T("laboratuvar", 21, MUTED, BOLD).next_to(lab, UP, buff=0.3)
        olt = sbox("OLT", "kendi ölçümü", OLTC, 1.9, 0.95, 21, 15).move_to([1.4, 0.75, 0])
        onu = sbox("ONU", "kendi ölçümü", ONUC, 1.9, 0.95, 21, 15).move_to([5.5, 0.75, 0])
        spl = splitter(0.22).move_to([3.45, 0.75, 0])
        fib = VGroup(Line(olt.get_right(), spl.get_left(), color=FEED, stroke_width=3), Line(spl.get_right(), onu.get_left(), color=FEED, stroke_width=3))
        g1, g2 = gauge(0.36).next_to(olt, DOWN, buff=0.28), gauge(0.36).next_to(onu, DOWN, buff=0.28)
        fld = VGroup(olt, onu, spl, fib, g1, g2)
        fldt = T("saha", 21, GOOD, BOLD).next_to(VGroup(olt, onu), UP, buff=0.3)
        p = pill("G.989.2 Ek II — optik katman denetimini destekleyen fiziksel katman ölçümleri", ACC, 19).move_to(DOWN * 2.3)
        fit(p, 13.0)
        self.at(self.cue("laboratuvardaki gibi", 4.0))
        self.play(FadeIn(lab, shift=UP * 0.1), FadeIn(labt), run_time=0.6)
        self.at(self.cue("osiloskopla değil", 7.3))
        x = xmark(lab, WARN, 5, 0.1)
        self.play(Create(x), lab.animate.set_opacity(0.35), run_time=0.6)
        self.at(self.cue("cihazların kendi", 8.7))
        self.play(FadeIn(fld, shift=UP * 0.1), FadeIn(fldt), run_time=0.8)
        self.play(Wiggle(g1[1], scale_value=1.15), Wiggle(g2[1], scale_value=1.15), run_time=0.8)
        self.at(self.cue("G.989.2 bunu ikinci ekte", 12.1))
        self.play(FadeIn(p, shift=UP * 0.1), self.set_src("G.989.2 Ek II (Appendix II)"), run_time=0.6)
        self.at(self.cue("optik katman denetimini", 14.9))
        self.play(Indicate(VGroup(g1, g2), color=ACC, scale_factor=1.15), run_time=0.8)
        self.end(pad=0.05)

        self.beat("b1a")
        self.clear(h)
        h = self.show_heading("Ek II: bilgilendirici", h)
        cN = card("Bağlayıcı (normatif)", "ana metin · Ek A, B, C, D", None, GOOD, w=5.5, h=1.35, tsize=22, bsize=19).move_to([-3.35, 1.45, 0])
        cI = card("Bilgilendirici", "Ek I … XI  —  Ek II burada", None, GOLD, w=5.5, h=1.35, tsize=22, bsize=19).move_to([3.35, 1.45, 0])
        neq = T("≠", 40, MUTED, BOLD).move_to([0, 1.45, 0])
        qt = T("“This appendix does not form an integral part of this Recommendation.”", 17, MUTED, slant=ITALIC).move_to([0, 0.4, 0])
        s1 = sbox("G.984.2 Amd.2", "Ek IV", MUTED, 2.7, 0.95, 20, 16).move_to([-4.55, -0.85, 0])
        d1 = sbox("G.989.2", "Ek II", GOLD, 2.7, 0.95, 20, 16).move_to([-0.55, -0.85, 0])
        ar = arrow(s1.get_right() + RIGHT * 0.1, d1.get_left() + LEFT * 0.1, MUTED, 3)
        chg = T("bazı aralıklar ve hesap yöntemleri değişti", 17, GOLD, BOLD).move_to([-2.55, -1.75, 0])
        ptp = card("PtP WDM", "aynı ölçümler geçerli\nuyarlama: ayrıca incelenecek", None, CH[1], w=4.3, h=1.55, tsize=22, bsize=18).move_to([4.5, -1.15, 0])
        pq = T("“further study is needed to tailor the requirements for PtP WDM PON”", 15, MUTED, slant=ITALIC).move_to([0.6, -2.65, 0])
        fit(pq, 12.0)
        self.at(self.cue("bilgilendiricidir", 1.6))
        self.play(FadeIn(cI, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("bağlayıcı bir parçası", 3.6))
        self.play(FadeIn(cN, shift=UP * 0.1), FadeIn(neq), run_time=0.6)
        self.play(FadeIn(qt), run_time=0.5)
        self.at(self.cue("İçeriği G.984.2", 7.1))
        self.play(FadeIn(s1, shift=RIGHT * 0.1), run_time=0.5)
        self.play(GrowArrow(ar), FadeIn(d1, shift=RIGHT * 0.1), run_time=0.6)
        self.at(self.cue("bazı aralıklar", 13.0))
        self.play(FadeIn(chg, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("aynı ölçümlerin PtP", 18.7))
        self.play(FadeIn(ptp, shift=LEFT * 0.15), run_time=0.6)
        self.at(self.cue("ayrıca inceleneceğini", 22.8))
        self.play(FadeIn(pq), run_time=0.5)
        self.end(pad=0.05)

        self.beat("b2")
        self.clear(h)
        h = self.show_heading("Tablo II.1 — elektriksel ve ısıl satırlar", h)
        self.tb = tb = ii1()
        names = [self.cell(r, 0) for r in range(1, 8)]
        for n in names:
            n.set_color(MUTED)
        self.play(FadeIn(tb[0]), *[FadeIn(tb[r][0]) for r in range(1, 8)], LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.1),
                  self.set_src("G.989.2 Ek II · Tablo II.1 (bilgilendirici)"), run_time=0.9)
        self.at(self.cue("üçü elektriksel", 2.0))
        self.play(*[n.animate.set_color(TXT) for n in names[:3]], run_time=0.5)
        self.at(self.cue("hem OLT'de hem ONU'da", 7.5))
        both = pill("OLT'de ve ONU'da ölçülür", ACC, 19).move_to(DOWN * 2.35)
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Tipik aralıklar", 10.9))
        self.show([self.cell(1, RNG)])
        self.at(self.cue("altı virgül elli beş", 16.2))
        self.show([self.cell(2, RNG)])
        self.at(self.cue("sekiz yüz on dokuz", 19.2))
        self.show([self.cell(3, RNG)])
        self.at(self.cue("Tepki süreleri", 23.5))
        self.show([self.cell(r, RSP) for r in (1, 2, 3)])
        self.end(pad=0.05)

        self.beat("b2a")
        h2 = self.heading("Doğruluk: gevşek")
        self.play(FadeTransform(h, h2), run_time=0.4)
        h = h2
        self.at(self.cue("sıcaklıkta artı eksi", 1.9))
        self.show([self.cell(1, ACCU)])
        self.at(self.cue("gerilimde nominal", 4.5))
        self.show([self.cell(2, ACCU)])
        self.at(self.cue("öngerilim akımında", 7.6))
        dim = [self.cell(r, c) for r in (1, 2, 3) for c in (RES, REP)]
        for m in dim:
            m.set_color(MUTED)
        self.show([self.cell(3, ACCU)], extra=[FadeIn(m) for m in dim])
        al = VGroup(pill("alarm · eğilim  ✓", GOOD, 20), pill("kalibrasyon  ✗", WARN, 20)).arrange(RIGHT, buff=0.5).move_to(DOWN * 2.35)
        self.at(self.cue("alarm ve eğilim", 10.0))
        self.play(FadeOut(both), FadeIn(al[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("kalibrasyon aracı", 13.5))
        self.play(FadeIn(al[1], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("b3")
        h2 = self.heading("Tablo II.1 — optik güçler")
        self.play(FadeTransform(h, h2), FadeOut(al), *[m.animate.set_opacity(0.35) for r in (1, 2, 3) for m in tb[r]], run_time=0.5)
        h = h2
        self.hot = []
        self.play(*[n.animate.set_color(TXT) for n in names[3:]], run_time=0.5)
        self.at(self.cue("gönderdiği ve aldığı", 2.2))
        self.play(Indicate(VGroup(*names[3:]), color=ACC, scale_factor=1.04), run_time=0.7)
        self.at(self.cue("Gönderilen güç eksi", 5.9))
        self.show([self.cell(4, RNG), self.cell(6, RNG)])
        self.at(self.cue("alınan güç eksi elli", 10.3))
        self.show([self.cell(5, RNG), self.cell(7, RNG)])
        self.at(self.cue("Çözünürlük", 16.1))
        self.show([self.cell(r, RES) for r in range(4, 8)])
        self.at(self.cue("tekrarlanabilirlik", 20.1))
        self.show([self.cell(r, REP) for r in range(4, 8)])
        self.at(self.cue("tepki süresi üç yüz", 24.6))
        self.show([self.cell(r, RSP) for r in range(4, 8)])
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p1A")


class E10P1B(TableAct):
    HDR, MANIFEST, PREV_BADGE = H10[1], M10("p1"), "std"

    def construct(self):
        self.beat("b3a")
        h = self.show_heading("Doğruluk — ve tablonun 5. notu")
        self.tb = tb = ii1(row_h=0.46, y=0.55)
        pre = [tb[0]] + [tb[r][0] for r in range(1, 8)] + [self.cell(r, c) for r in range(1, 8) for c in range(6) if not (r >= 4 and c == ACCU)]
        for r in (1, 2, 3):
            tb[r].set_opacity(0.35)
        self.play(*[FadeIn(m) for m in pre], self.set_src("G.989.2 Ek II · Tablo II.1, Not 5"), run_time=0.7)
        self.at(self.cue("ONU tarafında", 0.5))
        self.show([self.cell(4, ACCU), self.cell(5, ACCU)])
        self.at(self.cue("OLT tarafında artı eksi iki", 3.6))
        self.show([self.cell(6, ACCU), self.cell(7, ACCU)])
        nr = RoundedRectangle(corner_radius=0.16, width=12.6, height=1.25, stroke_color=GOLD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([0, -2.1, 0])
        n1 = T("Not 5 · alınan güç: −35 dBm'e kadar 3 dB, daha aşağıda 5 dB mutlak doğruluk", 20, TXT, BOLD)
        n2 = T("“Absolute accuracy is 3 dB down to –35 dBm received optical power, and 5 dB beyond –35 dBm.”", 15, MUTED, slant=ITALIC)
        ng = VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fit(ng, 8.6).move_to(nr).align_to(nr, LEFT).shift(RIGHT * 0.3)
        con = VGroup(T("OLT: ±2 dB", 19, WARN, BOLD), T("≠ 3 / 5 dB", 19, WARN, BOLD)).arrange(DOWN, buff=0.08).move_to([5.25, -2.1, 0])
        sep = Line([4.15, -1.65, 0], [4.15, -2.55, 0], color=LINE, stroke_width=2)
        self.at(self.cue("beşinci notu", 8.2))
        self.play(FadeIn(nr), FadeIn(ng, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("eksi otuz beş dBm'e kadar", 10.4))
        rx = VGroup(SurroundingRectangle(tb[5], color=GOLD, buff=0.02, stroke_width=2.5), SurroundingRectangle(tb[7], color=GOLD, buff=0.02, stroke_width=2.5))
        self.play(Create(rx), run_time=0.6)
        self.at(self.cue("bu notla çelişir", 17.6))
        bad = SurroundingRectangle(self.cell(7, ACCU), color=WARN, buff=0.06, stroke_width=3.5)
        self.play(Create(bad), FadeIn(sep), FadeIn(con, shift=LEFT * 0.1), self.cell(7, ACCU).animate.set_color(WARN), run_time=0.7)
        self.at(self.cue("notları da okumak", 21.3))
        self.play(Indicate(nr, color=GOLD, scale_factor=1.02), Indicate(ng[0], color=GOLD, scale_factor=1.03), run_time=0.9)
        self.end(pad=0.05)

        # b4 / b4a — the monitor window against the PMD tables
        self.beat("b4")
        self.clear(h)
        h = self.show_heading("İzleme penceresi ↔ PMD tabloları", h)
        ya = -1.95
        axg, X = lin_axis(-56, 0, -6.0, 6.0, ya, list(range(-55, 1, 5)), labels=[-50, -40, -30, -20, -10, 0], unit="optik güç (dBm)")
        yb = 1.2
        mon = Rectangle(width=X(-4.9) - X(-53), height=0.55, stroke_width=0, fill_color=ACC, fill_opacity=0.8).move_to([(X(-53) + X(-4.9)) / 2, yb, 0])
        mont = T("izleme penceresi · Tablo II.1", 19, BG, BOLD).move_to(mon)
        e_hi = VGroup(DashedLine([X(-4.9), ya, 0], [X(-4.9), yb + 0.28, 0], color=ACC, stroke_width=2), T("−4,9", 18, ACC, BOLD).next_to([X(-4.9), yb + 0.28, 0], UP, buff=0.08))
        e_lo = VGroup(DashedLine([X(-53), ya, 0], [X(-53), yb + 0.28, 0], color=ACC, stroke_width=2), T("−53", 18, ACC, BOLD).next_to([X(-53), yb + 0.28, 0], UP, buff=0.08))
        ov = VGroup(DashedLine([X(-5), ya, 0], [X(-5), 0.62, 0], color=WARN, stroke_width=2.5), Dot([X(-5), 0.35, 0], radius=0.07, color=WARN),
                    T("en yüksek aşırı yük −5 dBm · OLT Rx A tipi N1", 16, WARN, BOLD).next_to([X(-5), 0.35, 0], LEFT, buff=0.15))
        why = VGroup(T("“to facilitate tuning of the ONU tunable transmitter”", 16, MUTED, slant=ITALIC),
                     T("→ ONU'nun ayarlanabilir vericisinin ayarına yardım", 19, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-2.4, -0.25, 0])
        weak = VGroup(lobe(lambda v: X(v), -49.5, ya, 0.35, 0.9, WARN, op=0.35), T("yanlış kanala ayarlı ONU: zayıf ışık", 16, WARN, BOLD))
        weak[1].next_to(weak[0], RIGHT, buff=0.15).shift(UP * 0.12)
        tmp = tag("konum temsili", MUTED, 14).next_to(weak[1], RIGHT, buff=0.15)
        self.play(Create(axg[0]), FadeIn(axg[1:]), self.set_src("G.989.2 Tablo II.1 · Tablo 11-4…11-7"), run_time=0.6)
        self.play(GrowFromEdge(mon, LEFT), FadeIn(mont), run_time=0.8)
        self.at(self.cue("dört virgül dokuz", 3.0))
        self.play(Create(e_hi[0]), FadeIn(e_hi[1]), run_time=0.5)
        self.at(self.cue("en yüksek aşırı yükü", 6.4))
        self.play(Create(ov[0]), FadeIn(ov[1:]), run_time=0.6)
        self.at(self.cue("Eksi elli üçlük", 11.7))
        self.play(Create(e_lo[0]), FadeIn(e_lo[1]), run_time=0.5)
        self.at(self.cue("nedenini açıkça", 15.9))
        self.play(FadeIn(why[0]), run_time=0.5)
        self.at(self.cue("ayarına yardım", 18.2))
        self.play(FadeIn(why[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Yanlış kanala", 22.8))
        self.play(FadeIn(weak[0], shift=UP * 0.1), FadeIn(weak[1]), FadeIn(tmp), run_time=0.7)
        self.end(pad=0.05)

        self.beat("b4a")
        h2 = self.heading("Doğruluk bölgeleri — Not 5")
        self.play(FadeTransform(h, h2), FadeOut(why), FadeOut(weak), FadeOut(tmp), run_time=0.5)
        h = h2
        z5 = Rectangle(width=X(-35) - X(-53), height=0.55, stroke_width=0, fill_color=WARN, fill_opacity=0.85).move_to([(X(-53) + X(-35)) / 2, yb, 0])
        z3 = Rectangle(width=X(-4.9) - X(-35), height=0.55, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to([(X(-35) + X(-4.9)) / 2, yb, 0])
        zt = VGroup(T("±5 dB", 20, BG, BOLD).move_to(z5), T("±3 dB", 20, BG, BOLD).move_to(z3))
        d35 = VGroup(DashedLine([X(-35), ya, 0], [X(-35), yb + 0.28, 0], color=GOLD, stroke_width=2.5), T("−35", 18, GOLD, BOLD).next_to([X(-35), yb + 0.28, 0], UP, buff=0.08))
        e2 = VGroup(DashedLine([X(-36.5), ya, 0], [X(-36.5), yb - 0.28, 0], color=TW_US, stroke_width=2.5), Dot([X(-36.5), -0.45, 0], radius=0.08, color=TW_US),
                    T("OLT Rx 2,5G · B tipi · E2\n−36,5 dBm (Tablo 11-6)", 16, TW_US, BOLD, line_spacing=0.85))
        e2[2].next_to([X(-36.5), -0.45, 0], LEFT, buff=0.18)
        os_ = VGroup(Dot([X(-30), -0.45, 0], radius=0.08, color=SIG), Dot([X(-28), -0.45, 0], radius=0.08, color=SIG),
                     T("ONU S: −30 (2,5G) · −28 (10G) dBm", 16, SIG, BOLD))
        os_[2].next_to(os_[1], RIGHT, buff=0.18)
        w25 = Rectangle(width=X(-10) - X(-30), height=0.17, stroke_width=0, fill_color=TW_DS, fill_opacity=0.9).move_to([(X(-30) + X(-10)) / 2, -1.05, 0])
        w10 = Rectangle(width=X(-7) - X(-28), height=0.17, stroke_width=0, fill_color=GOOD, fill_opacity=0.9).move_to([(X(-28) + X(-7)) / 2, -1.35, 0])
        wl = T("ONU: hep ±3 dB", 16, GOOD, BOLD).next_to(VGroup(w25, w10), RIGHT, buff=0.2)
        self.play(FadeIn(z5), FadeIn(z3), FadeOut(mont), FadeIn(zt), Create(d35[0]), FadeIn(d35[1]), run_time=0.8)
        self.at(self.cue("yükselteçli bağlantı", 10.4))
        self.play(Create(e2[0]), FadeIn(e2[1], scale=0.5), FadeIn(e2[2], shift=LEFT * 0.1), run_time=0.7)
        self.play(Indicate(z5, color=WARN, scale_factor=1.03), run_time=0.6)
        self.at(self.cue("ONU hassasiyetleri", 18.8))
        self.play(FadeIn(os_), run_time=0.6)
        self.at(self.cue("bütün çalışma penceresinde", 23.5))
        self.play(GrowFromEdge(w25, LEFT), GrowFromEdge(w10, LEFT), FadeIn(wl), run_time=0.7)
        self.end(pad=0.05)

        # b5 — burst measurement
        self.beat("b5")
        self.clear(h)
        h = self.show_heading("OLT alınan güç = burst ölçümü (Not 3)", h)
        yt = -0.75
        tax = Arrow([-6.3, yt, 0], [6.4, yt, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.18)
        taxl = T("zaman", 15, MUTED).next_to(tax, DOWN, buff=0.08).align_to(tax, RIGHT)

        def burst(xa, xb, hgt=1.05, c=TW_US):
            return Polygon([xa, yt, 0], [xa + 0.15, yt + hgt, 0], [xb - 0.15, yt + hgt, 0], [xb, yt, 0], stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.3)
        b1, b2 = burst(-5.8, -0.9), burst(1.9, 2.8, 0.8)
        bl1 = T("uzun burst", 17, TW_US, BOLD).next_to(b1, UP, buff=0.1)
        bl2 = T("kısa burst", 17, TW_US, BOLD).next_to(b2, UP, buff=0.1)
        note = card("Not 3", "ölçüm burst'e göre doğru anda · burst, dedektörün tepki süresine yetecek kadar uzun", None, GOLD, w=12.6, h=1.05, tsize=20, bsize=18).move_to([0, 1.75, 0])
        win1 = Rectangle(width=3.0, height=0.42, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.3).move_to([-3.3, yt + 0.45, 0])
        wt1 = T("300 ns tepki ✓", 17, GOLD, BOLD).next_to(win1, DOWN, buff=0.08)
        win2 = Rectangle(width=3.0, height=0.42, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.2).move_to([3.4, yt + 0.4, 0])
        wt2 = T("burst bitti, pencere dolmadı ✗", 17, WARN, BOLD).move_to([3.4, yt - 0.45, 0])
        bits = VGroup(T("300 ns = 746 bit @ 2,48832 Gbit/s", 21, TXT, BOLD), T("300 ns ≈ 2986 bit @ 9,95328 Gbit/s", 21, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-2.4, -2.35, 0])
        bad = T("çok kısa burst: güç okunamaz", 20, WARN, BOLD).move_to([3.6, -2.35, 0])
        self.play(GrowArrow(tax), FadeIn(taxl), FadeIn(b1), FadeIn(b2), FadeIn(bl1), FadeIn(bl2), self.set_src("G.989.2 Ek II · Tablo II.1, Not 3"), run_time=0.8)
        self.at(self.cue("Üçüncü not", 3.8))
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
        self.at(self.cue("Üç yüz nanosaniye", 14.4))
        self.play(GrowFromEdge(win1, LEFT), FadeIn(wt1), run_time=0.6)
        self.at(self.cue("yedi yüz kırk altı", 15.9))
        self.play(FadeIn(bits[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("üç bin bittir", 19.5))
        self.play(FadeIn(bits[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Çok kısa bir burst", 22.5))
        self.play(GrowFromEdge(win2, LEFT), FadeIn(wt2), run_time=0.6)
        self.play(FadeIn(bad, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # b6 — the dual-purpose bias register
        self.beat("b6")
        self.clear(h)
        h = self.show_heading("Tek kayıt, iki verici tipi — Tablo II.2", h)
        cw = 0.66
        cells = VGroup(*[Square(cw - 0.06, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1) for _ in range(16)]).arrange(RIGHT, buff=0.06).move_to([0, 0.45, 0])
        bn = VGroup(*[T(str(16 - i), 14, MUTED).next_to(c, UP, buff=0.08) for i, c in enumerate(cells)])
        rl = T("verici akımı kaydı · 16 bit", 19, MUTED, BOLD).move_to([-6.3, 1.95, 0], aligned_edge=LEFT)
        dev = VGroup(sbox("lazer (EML)", "öngerilim akımı", CH[0], 2.6, 0.85, 19, 15), sbox("SOA", "yükselteç akımı", CH[2], 2.6, 0.85, 19, 15)).arrange(RIGHT, buff=0.6).move_to([3.0, 1.95, 0])
        tbr = BraceBetweenPoints(cells[0].get_corner(UL) + UP * 0.32, cells[1].get_corner(UR) + UP * 0.32, UP, color=GOLD)
        tbt = T("tip", 18, GOLD, BOLD).next_to(tbr, UP, buff=0.06)
        vbr = BraceBetweenPoints(cells[2].get_corner(DL), cells[15].get_corner(DR), DOWN, color=ACC)
        vbt = T("14 bit · adım 50 µA", 19, ACC, BOLD).next_to(vbr, DOWN, buff=0.08)
        ty = table(["bit 16 · 15", "anlamı"], [["0 0", "tanımsız"], ["0 1", "lazer öngerilimi"], ["1 0", "SOA akımı"], ["1 1", "tanımsız"]], [1.8, 3.0], size=18, hsize=15, row_h=0.42)
        ty.move_to([-3.95, -1.95, 0])
        for r in (1, 4):
            ty[r].set_opacity(0.4)
        ty[2][2].set_color(CH[0])
        ty[3][2].set_color(CH[2])
        n1 = T("2¹⁴ = 16 384 değer", 22, TXT, BOLD)
        n2 = T("16 383 × 0,05 mA = 819,15 mA", 22, TXT, BOLD)
        n3 = T("→ aralık 0 … 819 mA (Tablo II.1)", 20, GOLD, BOLD)
        nums = VGroup(n1, n2, n3).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.35, -2.0, 0])
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), FadeIn(bn), FadeIn(rl), self.set_src("G.989.2 Ek II · Tablo II.2"), run_time=0.9)
        self.at(self.cue("iki tip vericiyi", 4.1))
        self.play(FadeIn(dev, shift=DOWN * 0.1), run_time=0.6)
        self.at(self.cue("En anlamlı iki bit", 7.6))
        self.play(*[c.animate.set_stroke(GOLD, 3).set_fill(GOLD, 0.35) for c in cells[:2]], FadeIn(tbr), FadeIn(tbt), run_time=0.6)
        self.at(self.cue("lazer öngerilimi mi", 9.2))
        self.play(FadeIn(ty[0]), FadeIn(ty[2], shift=UP * 0.05), Indicate(dev[0], color=CH[0], scale_factor=1.05), run_time=0.6)
        self.at(self.cue("SOA'nın akımı", 14.7))
        self.play(FadeIn(ty[3], shift=UP * 0.05), FadeIn(ty[1]), FadeIn(ty[4]), Indicate(dev[1], color=CH[2], scale_factor=1.05), run_time=0.6)
        self.at(self.cue("Kalan on dört bit", 17.9))
        self.play(*[c.animate.set_stroke(ACC, 2.5).set_fill(ACC, 0.25) for c in cells[2:]], FadeIn(vbr), run_time=0.6)
        self.at(self.cue("elli mikroamperlik", 19.4))
        self.play(FadeIn(vbt), FadeIn(n1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("sekiz yüz on dokuz", 25.4))
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(n3, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p1B")


class E10P1C(Act10):
    HDR, MANIFEST, PREV_BADGE = H10[1], M10("p1"), "std"

    def construct(self):
        self.beat("b6a")
        h = self.show_heading("Güç kayıtları: yeni adım boyları")

        def reg(y, title, step, lo, hi, c):
            tt = T(title, 21, c, BOLD).move_to([-6.3, y + 0.7, 0], aligned_edge=LEFT)
            bar = Rectangle(width=6.6, height=0.5, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.22).move_to([0.2, y, 0])
            st = T(step, 19, TXT, BOLD).move_to(bar)
            l = VGroup(Line(bar.get_corner(DL), bar.get_corner(DL) + DOWN * 0.25, color=c, stroke_width=2), T(lo, 18, TXT, BOLD))
            l[1].next_to(l[0], DOWN, buff=0.06).align_to(bar, LEFT)
            r = VGroup(Line(bar.get_corner(DR), bar.get_corner(DR) + DOWN * 0.25, color=c, stroke_width=2), T(hi, 18, TXT, BOLD))
            r[1].next_to(r[0], DOWN, buff=0.06).align_to(bar, RIGHT)
            return tt, VGroup(bar, st), l, r
        tx = reg(1.05, "Gönderilen güç · Tablo II-3", "16 bit × 1,5 µW", "0x0001 = 1,5 µW → −28,24 dBm", "0xFFFF → ≈ +20 dBm (100 mW)", TW_DS)
        rx = reg(-1.15, "Alınan güç · Tablo II.4", "16 bit × 0,005 µW", "0x0001 = 0,005 µW → −53 dBm", "0xFFFF = 327,7 µW → −4,84 dBm", GOOD)
        tail = pill("Tablo II.1 aralıkları:  −28 … +20 dBm  ·  −53 … −4,9 dBm", ACC, 19).move_to([0, -2.85, 0])
        self.at(self.cue("bir virgül beş mikrovatlık", 3.2))
        self.play(FadeIn(tx[0], shift=RIGHT * 0.1), FadeIn(tx[1]), self.set_src("G.989.2 Ek II · Tablo II-3, II.4"), run_time=0.6)
        self.at(self.cue("eksi yirmi sekiz virgül", 8.3))
        self.play(FadeIn(tx[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("artı yirmi dBm", 12.4))
        self.play(FadeIn(tx[3], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("sıfır virgül sıfır sıfır beş", 17.1))
        self.play(FadeIn(rx[0], shift=RIGHT * 0.1), FadeIn(rx[1]), run_time=0.6)
        self.at(self.cue("bir adım eksi elli üç", 23.0))
        self.play(FadeIn(rx[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("eksi dört virgül sekiz", 24.9))
        self.play(FadeIn(rx[3], shift=UP * 0.1), FadeIn(tail, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # b7 — normative text leans on the informative appendix
        self.beat("b7")
        self.clear(h)
        h = self.show_heading("Bilgilendirici ekten bağlayıcı sayıya", h)
        cI = card("Ek II · bilgilendirici", "ONU RSSI doğruluğu ±3 dB", None, GOLD, w=4.9, h=1.3, tsize=22, bsize=20).move_to([-4.0, 1.35, 0])
        cD = card("Ek D · normatif", "D.3 özerk güç dengeleme", None, GOOD, w=4.9, h=1.3, tsize=22, bsize=20).move_to([3.9, 1.35, 0])
        ar = arrow(cI.get_right() + RIGHT * 0.1, cD.get_left() + LEFT * 0.1, MUTED, 3)
        art = T("dayanır", 17, MUTED, BOLD).next_to(ar, UP, buff=0.08)
        tok = pill("±3 dB", GOLD, 18).move_to(cI.get_right() + RIGHT * 0.5 + DOWN * 0.45)
        K = 0.55
        x0, yb = -4.4, -0.75
        b15 = Rectangle(width=15 * K, height=0.55, stroke_width=0, fill_color=MUTED, fill_opacity=0.5).move_to([x0 + 7.5 * K, yb, 0])
        b15t = T("15 dB · en büyük diferansiyel OPL (Tablo 6-1)", 18, TXT, BOLD).move_to(b15)
        b3 = Rectangle(width=3 * K, height=0.55, stroke_width=0, fill_color=WARN, fill_opacity=0.85).move_to([x0 + 13.5 * K, yb - 0.85, 0])
        b3t = T("− 3 dB", 18, WARN, BOLD).next_to(b3, RIGHT, buff=0.15)
        b12 = Rectangle(width=12 * K, height=0.55, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to([x0 + 6 * K, yb - 0.85, 0])
        b12t = T("12 dB izin verilen dengeleme", 19, BG, BOLD).move_to(b12)
        eq = T("15 − 3 = 12 dB", 28, GOLD, BOLD).move_to([0, -2.75, 0])
        self.play(FadeIn(cI, shift=UP * 0.1), self.set_src("G.989.2 Ek D.3 · Tablo 6-1 · Ek II"), run_time=0.6)
        self.at(self.cue("ama bağlayıcı metin", 3.8))
        self.play(GrowArrow(ar), FadeIn(art), FadeIn(cD, shift=LEFT * 0.1), run_time=0.7)
        self.at(self.cue("göstergesinin", 9.2))
        self.play(FadeIn(tok, scale=0.8), run_time=0.3)
        self.play(tok.animate.move_to(cD.get_left() + LEFT * 0.5 + DOWN * 0.45), run_time=1.2)
        self.at(self.cue("on beş desibellik", 16.1))
        self.play(GrowFromEdge(b15, LEFT), FadeIn(b15t), run_time=0.7)
        self.play(GrowFromEdge(b3, RIGHT), FadeIn(b3t), run_time=0.5)
        self.at(self.cue("on iki desibele", 21.4))
        self.play(GrowFromEdge(b12, LEFT), FadeIn(b12t), FadeIn(eq, shift=UP * 0.1), run_time=0.7)
        self.end(pad=0.05)

        # b7a — TC bridge: where the numbers travel
        self.beat("b7a")
        self.clear(h)
        self.set_badge("tc")
        h = self.show_heading("Nerede taşınır? — G.989.3", h)
        fy = 1.75
        psb = Rectangle(width=0.5, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([-6.15, fy, 0])
        pay = Rectangle(width=5.1, height=0.5, stroke_color=TW_DS, stroke_width=1.5, fill_color=TW_DS, fill_opacity=0.15).next_to(psb, RIGHT, buff=0)
        payt = T("125 µs aşağı yön çerçevesi", 16, TW_DS).move_to(pay)
        blocks = VGroup(*[VGroup(Rectangle(width=1.75, height=0.6, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.2), T(n, 17, TXT, BOLD))
                          for n, c in (("PSync", STATE), ("SFC", ACC), ("OC", GOLD))])
        for b in blocks:
            b[1].move_to(b[0])
        blocks.arrange(RIGHT, buff=0).move_to([-3.55, 0.75, 0])
        zl = VGroup(DashedLine(psb.get_corner(DL), blocks.get_corner(UL), color=GOLD, stroke_width=1.5), DashedLine(psb.get_corner(DR), blocks.get_corner(UR), color=GOLD, stroke_width=1.5))
        tol = VGroup(RoundedRectangle(corner_radius=0.08, width=3.9, height=0.6, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.25),
                     T("TOL · 9 bit · 0,1 dB / adım", 18, TXT, BOLD))
        tol[1].move_to(tol[0])
        tol.move_to([-3.55, -0.25, 0])
        tl = Line(blocks[2].get_bottom(), tol.get_top(), color=GOLD, stroke_width=2)
        mp = table(["TOL", "OLT başlatma gücü"], [["0x000", "−30 dBm"], ["0x12C", "0 dBm"], ["0x1FE", "+21 dBm"], ["0x1FF", "desteklenmiyor"]], [1.3, 2.6], size=17, hsize=14, row_h=0.36)
        mp.move_to([-3.55, -1.55, 0])
        cbit = T("C biti: S/R-CG (0) · S/R-CP (1)", 16, ACC, BOLD).move_to([-3.55, -2.6, 0])
        bc = T("→ bütün ONU'lara yayın", 17, GOLD, BOLD).next_to(pay, RIGHT, buff=0.2)
        c1 = card("ONU optik güçleri", "OMCI ile okunur\nG.988 yönetim varlıkları (§14.1)", None, ONUC, w=5.4, h=1.55, tsize=22, bsize=18).move_to([3.85, 0.4, 0])
        c2 = card("OLT CT izler", "her çalışan ONU: RSSI · faz · BER\n(§12.1.3)", None, OLTC, w=5.4, h=1.55, tsize=22, bsize=18).move_to([3.85, -1.5, 0])
        self.at(self.cue("nerede taşındığını", 0.9))
        self.play(FadeIn(psb), FadeIn(pay), FadeIn(payt), self.set_src("G.989.3 §10.1.1.1.3 · §14.1 · §12.1.3"), run_time=0.6)
        self.at(self.cue("OLT'nin başlatma gücü", 4.9))
        self.play(Create(zl), LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in blocks], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("TOL alanında", 6.8))
        self.play(Indicate(blocks[2], color=GOLD), Create(tl), FadeIn(tol, shift=DOWN * 0.1), run_time=0.8)
        self.at(self.cue("eksi otuz dBm'e göre", 11.2))
        self.play(FadeIn(mp[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in mp[1:]], lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(cbit), FadeIn(bc, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("OMCI ile", 18.3))
        self.play(FadeIn(c1, shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("OLT de çalışan", 25.7))
        self.play(FadeIn(c2, shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.note10("b8", [("1", "ONU RSSI ↔ saha güç ölçeri", "3 dB'e kadar fark normal — Ek II doğruluğu.", "Bir:"),
                           ("2", "Güç dengeleme açıkken: ölçerin araya giriş kaybı", "ONU bir eşiğin altına iner → vericisi 3 dB yükselebilir (Ek D.6).", "İki:"),
                           ("3", "OLT gelen güç okuması", "Yalnızca yeterince uzun burst'lerde değerlendirin (Tablo II.1 Not 3).", "Üç:")])
        self.bridge_beat("b9", "Ölçebiliyoruz.\nPeki bir fiber kesildiğinde ağ nasıl ayakta kalır?")
        self.save_timeline("ep10_p1C")


# ================================ PERDE 2 ======================================
class TypeB:
    """1:1 Type B, dual-parented: 2 chassis × 4 CTs → WM → feeder → 2:N splitter → ONUs."""

    def __init__(self):
        self.cts1, self.cts2 = VGroup(), VGroup()
        ys1, ys2 = [1.75, 1.33, 0.91, 0.49], [-1.05, -1.47, -1.89, -2.31]
        for i in range(4):
            self.cts1.add(ct_box(f"CT λ{i + 1}", CH[i], 1.45, 0.34, 14, on=True).move_to([-5.35, ys1[i], 0]))
            self.cts2.add(ct_box(f"CT λ{i + 1}'", CH[i], 1.45, 0.34, 14, on=False).move_to([-5.35, ys2[i], 0]))
        self.ch1 = VGroup(RoundedRectangle(corner_radius=0.12, width=1.85, height=2.2, stroke_color=MUTED, stroke_width=2, fill_opacity=0).move_to([-5.35, 1.03, 0]),
                          T("Şasi 1", 14, MUTED, BOLD).move_to([-5.35, 2.0, 0]))
        self.ch2 = VGroup(RoundedRectangle(corner_radius=0.12, width=1.85, height=2.2, stroke_color=MUTED, stroke_width=2, fill_opacity=0).move_to([-5.35, -1.77, 0]),
                          T("Şasi 2", 14, MUTED, BOLD).move_to([-5.35, -0.8, 0]))
        self.wm1 = sbox("WM", None, FEED, 0.75, 1.55, 17).move_to([-3.05, 1.12, 0])
        self.wm2 = sbox("WM", None, FEED, 0.75, 1.55, 17).move_to([-3.05, -1.68, 0])
        self.att1 = VGroup(*[Line(c.get_right(), [self.wm1.get_left()[0], 1.12 + (c.get_y() - 1.12) * 0.75, 0], color=CH[i], stroke_width=2.5) for i, c in enumerate(self.cts1)])
        self.att2 = VGroup(*[Line(c.get_right(), [self.wm2.get_left()[0], -1.68 + (c.get_y() + 1.68) * 0.75, 0], color=CH[i], stroke_width=2.5) for i, c in enumerate(self.cts2)])
        self.spl = splitter(0.3).move_to([0.95, -0.28, 0])
        sl = self.spl.get_left()
        self.fd1 = VMobject(stroke_color=FEED, stroke_width=3.5).set_points_as_corners([self.wm1.get_right(), [-0.6, 1.12, 0], sl + UP * 0.1])
        self.fd2 = VMobject(stroke_color=FEED, stroke_width=3.5).set_points_as_corners([self.wm2.get_right(), [-0.6, -1.68, 0], sl + DOWN * 0.1])
        self.onus = VGroup(*[onu_icon("ONU", ONUC, 1.2, 0.5, 16).move_to([5.75, y, 0]) for y in (1.25, -0.28, -1.81)])
        sr = self.spl.get_right()
        self.dist = VGroup(*[VMobject(stroke_color=FEED, stroke_width=2.5).set_points_as_corners([sr, [2.7, o.get_y(), 0], o.get_left()]) for o in self.onus])
        self.lbl_att = T("kanal bağlantı fiberleri", 15, MUTED, BOLD).move_to([-3.75, -0.28, 0])
        self.lbl_fd = VGroup(T("besleyici", 15, MUTED, BOLD).next_to([-1.4, 1.12, 0], UP, buff=0.08), T("besleyici", 15, MUTED, BOLD).next_to([-1.4, -1.68, 0], DOWN, buff=0.08))
        self.lbl_spl = T("ayırıcı 2:N", 15, MUTED, BOLD).next_to(self.spl, DOWN, buff=0.12)
        self.lbl_dist = T("dağıtım / düşüm", 15, MUTED, BOLD).move_to([3.75, 0.55, 0])

    def all(self):
        return VGroup(self.ch1, self.ch2, self.cts1, self.cts2, self.att1, self.att2, self.wm1, self.wm2, self.fd1, self.fd2, self.spl, self.dist, self.onus,
                      self.lbl_att, self.lbl_fd, self.lbl_spl, self.lbl_dist)


def set_lamp(ct, on):
    return Transform(ct[2], lamp(on, 0.08).move_to(ct[2].get_center()))


class E10P2A(Act10):
    HDR, MANIFEST, FIRST = H10[2], M10("p2"), True

    def construct(self):
        self.beat("c1")
        tc = self.title_card("PERDE 2", "Koruma")
        self.at(self.cue("Önce şunu belirtelim", 1.4))
        self.to_header(tc)
        self.set_badge("tc")
        h = self.show_heading("Koruma nerede tanımlı?")
        d1 = card("G.989.2 · fiziksel katman", "koruma: tanımsız", None, MUTED, w=5.6, h=1.6, tsize=23, bsize=21).move_to([-3.3, 0.8, 0])
        srch = VGroup(RoundedRectangle(corner_radius=0.1, width=4.9, height=0.55, stroke_color=LINE, stroke_width=2, fill_color="#0B1220", fill_opacity=1),
                      T("arama: \"protection\" → teknik metinde yok", 17, WARN, BOLD))
        srch[1].move_to(srch[0])
        fit(srch[1], 4.6)
        srch.move_to([-3.3, -0.65, 0])
        d2 = card("G.989.3 · TC katmanı", "§18 — TWDM sistem koruması", None, GOOD, w=5.6, h=1.6, tsize=23, bsize=21).move_to([3.3, 0.8, 0])
        br = pill("bu perde: bir TC köprüsü — fiziksel katman sonuçlarıyla", ACC, 20).move_to(DOWN * 2.1)
        self.at(self.cue("G.989.2 koruma tanımlamaz", 3.2))
        self.play(FadeIn(d1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("sözcüğü bile", 5.4))
        self.play(FadeIn(srch, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("on sekizinci maddesindedir", 9.7))
        self.play(FadeIn(d2, shift=UP * 0.1), self.set_src("G.989.3 §18"), run_time=0.6)
        self.at(self.cue("TC köprüsüdür", 12.9))
        self.play(FadeIn(br, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # c2 — the 1:1 Type B architecture
        self.beat("c2")
        self.clear(h)
        h = self.show_heading("1:1 B tipi koruma — §18.1", h)
        tb = self.tb = TypeB()
        tag1 = pill("1:1 · B tipi", ACC, 19).move_to([3.4, 2.15, 0])
        self.at(self.cue("B tipi korumadır", 2.1))
        self.play(FadeIn(tag1, shift=DOWN * 0.1), self.set_src("G.989.3 §18.1 · Şekil 18-1"), run_time=0.5)
        self.at(self.cue("iki OLT kanal sonlandırıcısı", 3.5))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in tb.cts1], lag_ratio=0.12), Create(tb.att1), FadeIn(tb.wm1), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in tb.cts2], lag_ratio=0.12), Create(tb.att2), FadeIn(tb.wm2), run_time=0.9)
        self.play(Create(tb.fd1), Create(tb.fd2), FadeIn(tb.spl), FadeIn(tb.lbl_fd), FadeIn(tb.lbl_spl), run_time=0.8)
        self.play(Create(tb.dist), LaggedStart(*[FadeIn(o) for o in tb.onus], lag_ratio=0.2), FadeIn(tb.lbl_dist), FadeIn(tb.lbl_att), run_time=0.9)
        peer = VGroup(*[DashedLine(a.get_left() + LEFT * 0.12, b.get_left() + LEFT * 0.12, color=CH[i], stroke_width=1.5, dash_length=0.06)
                        for i, (a, b) in enumerate(zip(tb.cts1, tb.cts2))])
        self.at(self.cue("Çift ebeveynli", 9.7))
        self.play(Create(tb.ch1[0]), Create(tb.ch2[0]), FadeIn(tb.ch1[1]), FadeIn(tb.ch2[1]), run_time=0.7)
        dp = T("çift ebeveynli: iki şasi", 17, ACC, BOLD).move_to([-1.0, 2.15, 0])
        self.play(FadeIn(dp), run_time=0.4)
        sp = card("tek ebeveynli", "iki CT aynı şasi · aynı SNI paylaşılabilir", None, MUTED, w=5.5, h=0.95, tsize=18, bsize=17).move_to([3.6, -2.95, 0])
        self.at(self.cue("tek ebeveynli", 15.3))
        self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # c3 — what is protected
        self.beat("c3")
        h2 = self.heading("Neyi korur?")
        lg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=PROT, stroke_width=5), T("korunur", 16, PROT, BOLD)).arrange(RIGHT, buff=0.15),
                    VGroup(Line(ORIGIN, RIGHT * 0.5, color=UNPROT, stroke_width=5), T("korunmaz", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5).move_to([3.4, 2.15, 0])
        self.play(FadeTransform(h, h2), FadeOut(tag1), FadeOut(sp), FadeOut(dp), FadeIn(lg), run_time=0.5)
        h = h2
        self.play(Indicate(tb.att1, color=PROT, scale_factor=1.0), run_time=0.6)
        self.play(tb.att1.animate.set_stroke(PROT, 4), tb.att2.animate.set_stroke(PROT, 4), tb.lbl_att.animate.set_color(PROT), run_time=0.5)
        self.at(self.cue("Besleyici fiberi", 9.5))
        self.play(tb.fd1.animate.set_stroke(PROT, 5), tb.fd2.animate.set_stroke(PROT, 5), tb.lbl_fd.animate.set_color(PROT), run_time=0.6)
        self.at(self.cue("Çoğullayıcının kendisini", 14.8))
        self.play(tb.wm1[0].animate.set_stroke(PROT, 3.5), tb.wm2[0].animate.set_stroke(PROT, 3.5), run_time=0.5)
        self.at(self.cue("kanal sonlandırıcısını", 16.9))
        self.play(*[c[0].animate.set_stroke(PROT, 3) for c in (*tb.cts1, *tb.cts2)], run_time=0.5)
        self.at(self.cue("bütün şasiyi", 18.9))
        self.play(tb.ch1[0].animate.set_stroke(PROT, 3.5), tb.ch2[0].animate.set_stroke(PROT, 3.5), tb.ch1[1].animate.set_color(PROT), tb.ch2[1].animate.set_color(PROT), run_time=0.5)
        self.at(self.cue("Dağıtım ve düşüm", 21.7))
        self.play(tb.dist.animate.set_stroke(UNPROT, 2.5), tb.spl.animate.set_stroke(UNPROT), tb.lbl_dist.animate.set_color(UNPROT), tb.lbl_spl.animate.set_color(UNPROT),
                  *[o.animate.set_opacity(0.45) for o in tb.onus], run_time=0.7)
        nl = T("listede yok", 17, WARN, BOLD).next_to(tb.lbl_dist, UP, buff=0.12)
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # c3a — switching granularity
        self.beat("c3a")
        h2 = self.heading("Anahtarlama inceliği")
        self.play(FadeTransform(h, h2), FadeOut(lg), FadeOut(nl), run_time=0.5)
        h = h2
        ind = pill("her kanal çifti bağımsız korunur", ACC, 18).move_to([3.4, 2.15, 0])
        self.at(self.cue("bağımsız korunur", 3.2))
        self.play(FadeIn(ind, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.cue("Besleyici fiber", 5.9))
        cut = xmark(Square(0.3).move_to([-1.4, 1.12, 0]), WARN, 5)
        self.play(Create(cut), tb.fd1.animate.set_stroke(WARN, 3.5).set_opacity(0.5), run_time=0.5)
        r1 = T("besleyici / WM / şasi arızası → gruptaki bütün çiftler", 17, GOLD, BOLD).move_to([3.4, -2.6, 0])
        fit(r1, 6.6)
        self.at(self.cue("aynı anda anahtarlanır", 10.0))
        self.play(*[set_lamp(c, False) for c in tb.cts1], *[set_lamp(c, True) for c in tb.cts2], FadeIn(r1, shift=DOWN * 0.1), run_time=0.8)
        self.at(self.cue("Yalnızca bir kanal", 14.5))
        self.play(FadeOut(cut), tb.fd1.animate.set_stroke(PROT, 5).set_opacity(1), *[set_lamp(c, True) for c in tb.cts1], *[set_lamp(c, False) for c in tb.cts2],
                  r1.animate.set_opacity(0.35), run_time=0.7)
        cut2 = xmark(Square(0.24).move_to(tb.att1[1].get_center()), WARN, 4)
        self.play(Create(cut2), tb.att1[1].animate.set_stroke(WARN).set_opacity(0.5), run_time=0.5)
        r2 = T("tek CT / bağlantı fiberi arızası → yalnızca o çift", 17, GOLD, BOLD).move_to([3.4, -3.05, 0])
        fit(r2, 6.6)
        self.at(self.cue("yalnızca etkilenen çift", 20.7))
        self.play(set_lamp(tb.cts1[1], False), set_lamp(tb.cts2[1], True), FadeIn(r2, shift=DOWN * 0.1),
                  Indicate(VGroup(tb.cts1[1], tb.cts2[1]), color=GOLD, scale_factor=1.05), run_time=0.8)
        self.end(pad=0.05)

        # c4 — the PMD-relevant sentence
        self.beat("c4")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("ONU: aynı kanal çifti — yeniden ayar yok", h)
        qt = self.quote("G.989.3 §18.1", "“The Type B protection does not require ONU tuning … the ONU connectivity is maintained using one and the same channel pair.”",
                        "B tipi koruma ONU'nun yeniden ayarlanmasını gerektirmez", width=12.4).move_to([0, 1.55, 0])
        onu = onu_icon("ONU", ONUC, 1.5, 0.75, 20).move_to([-4.9, -0.25, 0])
        chs = VGroup(pill("↓ λ2", CH[1], 18), pill("↑ λ2", CH[1], 18)).arrange(RIGHT, buff=0.2).next_to(onu, RIGHT, buff=0.35)
        same = T("anahtarlama boyunca değişmez", 19, GOOD, BOLD).next_to(chs, RIGHT, buff=0.35)
        yt = -1.3
        t0 = -4.6
        tax = Arrow([t0 - 0.3, yt, 0], [6.4, yt, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.16)
        cutm = VGroup(Line([t0, yt - 0.15, 0], [t0, yt + 0.25, 0], color=WARN, stroke_width=4), T("kesinti", 15, WARN, BOLD).next_to([t0, yt + 0.25, 0], UP, buff=0.05))
        ba = VGroup(Rectangle(width=4.0, height=0.42, stroke_width=0, fill_color=GOOD, fill_opacity=0.75), T("↓ senkron geri gelir", 17, BG, BOLD))
        ba[0].move_to([t0 + 2.0, yt - 0.55, 0])
        ba[1].move_to(ba[0])
        bb = VGroup(DashedVMobject(Rectangle(width=7.6, height=0.42, stroke_color=WARN, stroke_width=2), num_dashes=50),
                    T("ONU yeniden ayara karar verir (TO2 / TO3 — değer yok)", 16, WARN, BOLD))
        bb[0].move_to([t0 + 3.8, yt - 1.1, 0])
        bb[1].move_to(bb[0])
        cond = T("koşul:  ↓ senkron geri gelme süresi  <  ONU'nun sabrı", 21, GOLD, BOLD).move_to([0.9, -3.0, 0])
        self.play(FadeIn(qt[0]), FadeIn(qt[1]), self.set_src("G.989.3 §18.1"), run_time=0.6)
        self.at(self.cue("yeniden ayarlanmasını gerektirmez", 3.6))
        self.play(FadeIn(qt[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("aynı kanal çiftinde", 8.3))
        self.play(FadeIn(onu), FadeIn(chs, shift=LEFT * 0.1), run_time=0.6)
        self.play(FadeIn(same), run_time=0.4)
        self.at(self.cue("korumanın etkili olması", 12.6))
        self.play(GrowArrow(tax), FadeIn(cutm), run_time=0.6)
        self.at(self.cue("aşağı yön senkronunun", 15.8))
        self.play(GrowFromEdge(ba[0], LEFT), FadeIn(ba[1]), run_time=0.7)
        self.at(self.cue("karar vermeden önce", 17.7))
        self.play(Create(bb[0]), FadeIn(bb[1]), run_time=0.7)
        self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p2A")


def ct_unit(name, color):
    """Larger CT block with a Tx lamp and an Rx 'ear'."""
    r = RoundedRectangle(corner_radius=0.12, width=2.4, height=1.15, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    t = T(name, 19, TXT, BOLD).move_to(r).shift(UP * 0.28)
    tx = VGroup(T("Tx", 15, MUTED, BOLD), lamp(False, 0.1)).arrange(RIGHT, buff=0.15).move_to(r).shift(DOWN * 0.22 + LEFT * 0.5)
    rx = VGroup(T("Rx", 15, MUTED, BOLD), gauge(0.16, TW_US, 0.4)).arrange(RIGHT, buff=0.15).move_to(r).shift(DOWN * 0.22 + RIGHT * 0.5)
    return VGroup(r, t, tx, rx)


def unit_lamp(u, on):
    return Transform(u[2][1], lamp(on, 0.1).move_to(u[2][1].get_center()))


STATES = [("1", "Başlangıç", "Initialization", 0), ("2", "Ön koruma", "Pre-Protecting", 0), ("3", "Koruma", "Protecting", 0), ("4", "LOS-P", "koruma tarafı LOS", 0),
          ("5", "Ön çalışma", "Pre-Working", 1), ("6", "Çalışma", "Working", 1), ("7", "LOS-W", "çalışma tarafı LOS", 1), ("8", "Helpme", "devir isteği", 0),
          ("9", "COMM-FAIL", "iletişim arızası", None), ("10", "EQPT-FAIL", "donanım arızası", None)]


def state_card(num, tr_, en, tx, w=2.45, h=1.25):
    c = {0: MUTED, 1: TXON, None: WARN}[tx]
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=STATE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    n = T(num, 16, STATE, BOLD).move_to(r.get_corner(UL) + [0.22, -0.2, 0])
    a = tf(tr_, 19, TXT, BOLD, w=w - 0.5).move_to(r).shift(UP * 0.15)
    b = tf(en, 14, MUTED, w=w - 0.2).next_to(a, DOWN, buff=0.06)
    if tx is None:
        lm = VGroup(T("Tx —", 15, WARN, BOLD))
    else:
        lm = VGroup(T("Tx", 15, c, BOLD), lamp(bool(tx), 0.09)).arrange(RIGHT, buff=0.1)
    lm.move_to(r.get_corner(DR) + [-0.45, 0.2, 0])
    return VGroup(r, n, a, b, lm)


class E10P2B(Act10):
    HDR, MANIFEST, PREV_BADGE = H10[2], M10("p2"), "fiz"

    def construct(self):
        # c5 — exactly one transmitter on
        self.beat("c5")
        self.set_badge("tc")
        h = self.show_heading("Hiçbir anda iki verici birlikte değil")
        u1 = ct_unit("CT 1 · λ1", CT_A).move_to([-4.9, 1.3, 0])
        u2 = ct_unit("CT 2 · λ1", CT_B).move_to([-4.9, -1.3, 0])
        wm = sbox("WM", None, FEED, 0.7, 1.2, 16).move_to([-2.3, 0, 0])
        l1 = VMobject(stroke_color=FEED, stroke_width=3).set_points_as_corners([u1.get_right(), [-3.1, 1.3, 0], wm.get_left() + UP * 0.25])
        l2 = VMobject(stroke_color=FEED, stroke_width=3).set_points_as_corners([u2.get_right(), [-3.1, -1.3, 0], wm.get_left() + DOWN * 0.25])
        spl = splitter(0.28).move_to([1.0, 0, 0])
        fd = Line(wm.get_right(), spl.get_left(), color=FEED, stroke_width=3.5)
        onus = VGroup(*[onu_icon("ONU", ONUC, 1.2, 0.5, 16).move_to([5.4, y, 0]) for y in (1.0, 0.0, -1.0)])
        ds = VGroup(*[Line(spl.get_right(), o.get_left(), color=FEED, stroke_width=2.5) for o in onus])
        pair = T("aynı kanal çifti", 17, ACC, BOLD).move_to([-4.9, 2.2, 0])
        self.at(self.cue("aynı kanal çiftine", 1.8))
        self.play(FadeIn(u1, shift=RIGHT * 0.1), FadeIn(u2, shift=RIGHT * 0.1), FadeIn(pair), self.set_src("G.989.3 §18.1"), run_time=0.6)
        self.play(Create(l1), Create(l2), FadeIn(wm), Create(fd), FadeIn(spl), Create(ds), FadeIn(onus), run_time=0.9)
        self.at(self.cue("ikisi birlikte", 5.3))
        both = T("✗ iki verici birlikte: asla", 20, WARN, BOLD).move_to([-1.2, 2.15, 0])
        self.play(unit_lamp(u1, True), unit_lamp(u2, True), FadeIn(both), run_time=0.5)
        self.play(Indicate(VGroup(u1[2], u2[2]), color=WARN, scale_factor=1.2), run_time=0.7)
        self.play(unit_lamp(u2, False), unit_lamp(u1, False), run_time=0.4)
        self.at(self.cue("Tam olarak biri", 9.2))
        r1 = pill("Etkin (Active)", TXON, 17).move_to([-4.9, 0.36, 0])
        dsl = VGroup(*[arrow(a, b, TXON, 3, 0.14) for a, b in (([-3.65, 1.5, 0], [-3.15, 1.5, 0]), ([-1.6, 0.25, 0], [0.4, 0.25, 0]), ([2.2, 0.62, 0], [3.4, 1.05, 0]))])
        self.play(unit_lamp(u1, True), FadeIn(r1), FadeOut(both), run_time=0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in dsl], lag_ratio=0.3), run_time=0.8)
        self.at(self.cue("bekleme rolündedir", 14.2))
        r2 = pill("Bekleme (Standby)", MUTED, 17).move_to([-4.9, -0.36, 0])
        self.play(FadeIn(r2), run_time=0.4)
        self.at(self.cue("vericisi kapalıdır", 16.4))
        self.play(Indicate(u2[2], color=MUTED, scale_factor=1.3), run_time=0.6)
        self.at(self.cue("yukarı yönü dinler", 18.0))
        usl = VGroup(arrow([3.4, -0.9, 0], [2.2, -0.3, 0], TW_US, 3, 0.14), arrow([0.4, -0.25, 0], [-1.6, -0.25, 0], TW_US, 3, 0.14),
                     arrow([-2.75, -0.62, 0], [-3.4, -1.12, 0], TW_US, 3, 0.14), arrow([-2.75, 0.62, 0], [-3.4, 1.12, 0], TW_US, 3, 0.14))
        self.play(LaggedStart(*[GrowArrow(a) for a in usl], lag_ratio=0.2), Indicate(u2[3], color=TW_US, scale_factor=1.3), run_time=0.9)
        self.end(pad=0.05)

        # c5a — the ten states
        self.beat("c5a")
        self.clear(h)
        h = self.show_heading("Tablo 18-1 — on durum, verici açık / kapalı", h)
        cards = VGroup(*[state_card(*s) for s in STATES]).arrange_in_grid(rows=2, cols=5, buff=(0.18, 0.3)).move_to([0, 0.45, 0])
        for c in cards:
            c[4].set_opacity(0)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.08), self.set_src("G.989.3 §18.2 · Tablo 18-1"), run_time=1.2)
        self.play(*[m.animate.set_opacity(0.45) for c in cards for m in c[2:4]], run_time=0.3)
        self.at(self.cue("açık mı kapalı mı", 2.9))
        self.play(*[c[4].animate.set_opacity(1) for c in cards], run_time=0.6)

        def hi(ix, col):
            return [cards[i][0].animate.set_stroke(col, 3.5) for i in ix] + [m.animate.set_opacity(1) for i in ix for m in cards[i][2:4]]
        self.at(self.cue("Başlangıç", 7.9))
        self.play(*hi([0], MUTED), run_time=0.35)
        self.at(self.cue("ön koruma", 8.7))
        self.play(*hi([1], MUTED), run_time=0.35)
        self.at(self.cue("verici kapalıdır", 12.0))
        self.play(*hi([2, 3, 7], MUTED), run_time=0.45)
        off = pill("Tx kapalı: 1 · 2 · 3 · 4 · 8", MUTED, 18)
        on = pill("Tx açık: 5 · 6 · 7", TXON, 18)
        fl = pill("arıza: 9 · 10", WARN, 18)
        sm = VGroup(off, on, fl).arrange(RIGHT, buff=0.4).move_to([0, -2.4, 0])
        self.play(FadeIn(off, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Ön çalışma", 15.7))
        self.play(*hi([4], TXON), run_time=0.35)
        self.at(self.cue("açıktır", 20.0))
        self.play(*hi([5, 6], TXON), FadeIn(on, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Son iki durum", 22.0))
        self.play(*hi([8, 9], WARN), FadeIn(fl, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # c6 — SLOS / QLOS on the 125 µs grid
        self.beat("c6")
        self.clear(h)
        h = self.show_heading("Sinyal kaybı — yukarı yönden (Tablo 18-3)", h)
        fw, x0 = 1.15, -5.75
        r1y, r2y = 0.75, -1.35
        f1 = frames_row(10, x0, r1y, fw, 0.5, MUTED, op=0.06)
        f2 = frames_row(10, x0, r2y, fw, 0.5, MUTED, op=0.06)
        bur = lambda k, y: Rectangle(width=0.38, height=0.3, stroke_width=0, fill_color=TW_US, fill_opacity=0.85).move_to([x0 + fw * (k + 0.3), y, 0])
        b1 = VGroup(*[bur(k, r1y) for k in range(5)])
        b2 = VGroup(*[bur(k, r2y) for k in range(5)])
        t1 = VGroup(T("Basit (SLOS)", 21, TXT, BOLD), tag("↓ iletim yokken", MUTED, 15)).arrange(RIGHT, buff=0.25).move_to([x0, r1y + 0.7, 0], aligned_edge=LEFT)
        t2 = T("Nitelikli (QLOS)", 21, TXT, BOLD).move_to([x0, r2y + 0.7, 0], aligned_edge=LEFT)
        sil1 = Rectangle(width=4 * fw, height=0.5, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.12).move_to([x0 + fw * 7, r1y, 0])
        bra1 = Brace(sil1, DOWN, color=WARN)
        brt1 = T("0,5 ms = 4 × 125 µs sessizlik", 18, WARN, BOLD).next_to(bra1, DOWN, buff=0.06)
        sil2 = Rectangle(width=4 * fw, height=0.5, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.12).move_to([x0 + fw * 7, r2y, 0])
        brt2 = T("4 ardışık çerçeve: ↑ iletim yok", 17, WARN, BOLD).next_to(sil2, UP, buff=0.1)
        ons = VGroup(*[VGroup(onu_icon("ONU", ONUC, 0.95, 0.42, 14), T("LOBi", 14, WARN, BOLD)) for _ in range(4)])
        for o in ons:
            o[1].next_to(o[0], RIGHT, buff=0.08)
        ons.arrange(RIGHT, buff=0.3).move_to([-0.6, -2.45, 0])
        allt = T("+ bütün ilgili ONU'lar için LOBi", 18, WARN, BOLD).next_to(ons, RIGHT, buff=0.3)
        fit(VGroup(ons, allt), 12.8)
        tl = T("125 µs", 14, MUTED).next_to(f1[0], UP, buff=0.05)
        self.play(FadeIn(f1), FadeIn(tl), FadeIn(b1), self.set_src("G.989.3 Tablo 18-3"), run_time=0.6)
        self.at(self.cue("Basit sinyal kaybı", 4.3))
        self.play(FadeIn(t1[0], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("aşağı yönde iletim olmayan", 5.9))
        self.play(FadeIn(t1[1]), run_time=0.4)
        self.at(self.cue("sıfır virgül beş", 9.1))
        self.play(FadeIn(sil1), FadeIn(bra1), run_time=0.5)
        self.at(self.cue("dört çerçevelik", 11.7))
        self.play(FadeIn(brt1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Nitelikli sinyal kaybı", 15.5))
        self.play(FadeIn(t2, shift=RIGHT * 0.1), FadeIn(f2), FadeIn(b2), run_time=0.6)
        self.play(FadeIn(sil2), FadeIn(brt2), run_time=0.5)
        self.at(self.cue("burst kaybı ilan", 22.0))
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in ons], lag_ratio=0.15), FadeIn(allt), run_time=0.9)
        self.end(pad=0.05)

        # c6a — timers: order, not values
        self.beat("c6a")
        self.clear(h)
        h = self.show_heading("Zamanlayıcılar: sayı yok, yalnızca sıralama", h)
        bx = -2.3

        def tbar(y, wdt, name, desc, c):
            r = Rectangle(width=wdt, height=0.48, stroke_width=0, fill_color=c, fill_opacity=0.75).move_to([bx + wdt / 2, y, 0])
            n = VGroup(T(name, 21, c, BOLD), T(desc, 15, MUTED)).arrange(DOWN, aligned_edge=RIGHT, buff=0.04).next_to([bx, y, 0], LEFT, buff=0.25)
            return VGroup(r, n)
        tp = tbar(1.55, 7.2, "Tpfail", "koruma tarafı arıza", STATE)
        th = tbar(0.75, 5.0, "Thold", "tutma", ACC)
        tw = tbar(-0.05, 3.0, "Twfail", "çalışma tarafı arıza", GOOD)
        rel = tag("göreli uzunluk — değer yok", MUTED, 15).move_to([4.6, -0.05, 0])
        ordr = T("Tpfail > Thold > Twfail", 26, GOLD, BOLD).move_to([0, -1.0, 0])
        warn_ = T("aksi halde tutma özelliği etkisiz kalır", 16, MUTED).next_to(ordr, DOWN, buff=0.1)
        tr_ = card("Tract ≈ 0,5 ms", "yukarı yön onayı için önerilen başlangıç değeri (§18.2.5)", None, ACC, w=6.3, h=1.05, tsize=21, bsize=16).move_to([-3.2, -2.6, 0])
        f50 = VGroup(T("50 ms anahtarlama hedefi", 21, MUTED, BOLD))
        f50.add(strike(f50[0]), T("metinde yok", 18, WARN, BOLD).next_to(f50[0], DOWN, buff=0.08))
        f50.move_to([3.6, -2.6, 0])
        self.play(self.set_src("G.989.3 Tablo 18-2 · §18.2"), run_time=0.3)
        self.at(self.cue("yalnızca sıralama", 3.4))
        self.play(FadeIn(rel), run_time=0.4)
        self.at(self.cue("koruma tarafındaki arıza", 5.4))
        self.play(GrowFromEdge(tp[0], LEFT), FadeIn(tp[1]), run_time=0.6)
        self.at(self.cue("tutma zamanlayıcısından", 8.7))
        self.play(GrowFromEdge(th[0], LEFT), FadeIn(th[1]), run_time=0.5)
        self.play(GrowFromEdge(tw[0], LEFT), FadeIn(tw[1]), run_time=0.5)
        self.at(self.cue("tutma zamanlayıcısı da", 15.8))
        self.play(FadeIn(ordr, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warn_), run_time=0.4)
        self.at(self.cue("Verilen tek değer", 21.0))
        self.play(FadeIn(tr_, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Elli milisaniye", 27.7))
        self.play(FadeIn(f50[0]), run_time=0.3)
        self.play(Create(f50[1]), FadeIn(f50[2]), run_time=0.5)
        self.end(pad=0.05)

        # c7 — ICTP
        self.beat("c7")
        self.clear(h)
        h = self.show_heading("ICTP — iki sonlandırıcı arasında", h)
        a = sbox("OLT CT 1", None, CT_A, 2.4, 0.9, 20).move_to([-4.4, 1.2, 0])
        b = sbox("OLT CT 2", None, CT_B, 2.4, 0.9, 20).move_to([4.4, 1.2, 0])
        link = DoubleArrow(a.get_right(), b.get_left(), buff=0.1, color=STATE, stroke_width=3, tip_length=0.18)
        lt = T("ICTP · kanal sonlandırıcıları arası protokol", 18, STATE, BOLD).next_to(link, UP, buff=0.12)
        ra = pill("birincil", MUTED, 17).next_to(a, DOWN, buff=0.15)
        rb = pill("ikincil", MUTED, 17).next_to(b, DOWN, buff=0.15)
        hs = pill("el sıkışma · prtHandshake()", STATE, 17).move_to([0, 0.4, 0])
        ra2 = pill("etkin", TXON, 17).move_to(ra)
        rb2 = pill("bekleme", MUTED, 17).move_to(rb)
        cR = card("geri dönüşlü", "varsayılan roller kalıcı", None, GOOD, w=5.6, h=1.0, tsize=20, bsize=18).move_to([-3.3, -1.25, 0])
        cN = card("geri dönüşsüz", "el sıkışmadan sonra bırakılır", None, GOLD, w=5.6, h=1.0, tsize=20, bsize=18).move_to([3.3, -1.25, 0])
        p1 = pill("ayrıntı: BBF TR-352 — G.989.3 kapsamı dışında", MUTED, 16)
        p2 = pill("durum makinesi ICTP olmadan da ilerler (§18.2)", ACC, 16)
        ps = VGroup(p1, p2).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        fit(ps, 13.0)
        self.play(FadeIn(a), FadeIn(b), self.set_src("G.989.3 §18.1–18.3 · Ek VI (bilgilendirici)"), run_time=0.5)
        self.at(self.cue("yani ICTP ile", 5.9))
        self.play(GrowFromCenter(link), FadeIn(lt), run_time=0.6)
        self.at(self.cue("birincil ve ikincildir", 7.8))
        self.play(FadeIn(ra, shift=UP * 0.1), FadeIn(rb, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("el sıkışmayla", 11.2))
        self.play(FadeIn(hs, scale=0.9), run_time=0.4)
        self.play(Transform(ra, ra2), Transform(rb, rb2), run_time=0.6)
        self.at(self.cue("Geri dönüşlü", 13.6))
        self.play(FadeIn(cR, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("geri dönüşsüz", 18.3))
        self.play(FadeIn(cN, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ayrı bir belgeye", 23.2))
        self.play(FadeIn(p1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ICTP olmadan da", 27.4))
        self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p2B")


class E10P2C(Act10):
    HDR, MANIFEST, PREV_BADGE = H10[2], M10("p2"), "tc"

    def construct(self):
        # c8 — wavelength channel protection, ONU side
        self.beat("c8")
        h = self.show_heading("İkinci katman: dalga boyu kanalı koruması (WLCP)")
        olt = sbox("OLT CT", None, OLTC, 1.8, 0.75, 19).move_to([-5.3, 1.55, 0])
        onu = onu_icon("ONU", ONUC, 1.5, 0.75, 19).move_to([5.4, 1.55, 0])
        fb = Line(olt.get_right(), onu.get_left(), color=FEED, stroke_width=3)
        msg = VGroup(RoundedRectangle(corner_radius=0.08, width=4.6, height=0.62, stroke_color=GOLD, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                     T("Protection_Control (PLOAM) · koruma kanalı", 16, GOLD, BOLD))
        msg[1].move_to(msg[0])
        fit(msg[1], 4.4)
        msg.move_to([-2.4, 2.1, 0])
        xs = [-5.0, -1.7, 1.7, 5.0]
        o5 = sbox("O5", "Çalışma", STATE, 2.3, 0.9, 20, 15).move_to([xs[0], -0.35, 0])
        o6 = sbox("O6", "Aralıklı LODS", STATE, 2.3, 0.9, 20, 15).move_to([xs[1], -0.35, 0])
        o8 = sbox("O8", "↓ Ayar", STATE, 2.3, 0.9, 20, 15).move_to([xs[2], -0.35, 0])
        pc = sbox("koruma kanalı", "önceden yapılandırılmış", GOOD, 2.3, 0.9, 18, 14).move_to([xs[3], -0.35, 0])
        a1 = VGroup(arrow(o5.get_right(), o6.get_left(), WARN, 2.5, 0.14), T("LODS", 15, WARN, BOLD).move_to([(xs[0] + xs[1]) / 2, 0.32, 0]))
        a2 = VGroup(arrow(o6.get_right(), o8.get_left(), STATE, 2.5, 0.14), T("TO3 dolunca", 15, GOLD, BOLD).move_to([0, 0.32, 0]))
        a3 = arrow(o8.get_right(), pc.get_left(), GOOD, 2.5, 0.14)
        clk = VGroup(Circle(radius=0.22, color=GOLD, stroke_width=2.5), Line(ORIGIN, UP * 0.15, color=GOLD, stroke_width=2.5), Line(ORIGIN, RIGHT * 0.11, color=GOLD, stroke_width=2.5))
        clk.move_to([0, -1.25, 0])
        wl = VGroup(T("WLCP açık → TO3", 17, GOLD, BOLD), T("WLCP kapalı → TO2", 17, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(clk, RIGHT, buff=0.25)
        combs = VGroup(*[pill(f"λ{i + 1}", CH[i], 17) for i in range(4)]).arrange(RIGHT, buff=0.35).move_to([0, -2.55, 0])
        mk = Triangle(color=ONUC, fill_color=ONUC, fill_opacity=1).scale(0.12).rotate(PI).next_to(combs[1], UP, buff=0.08)
        self.play(FadeIn(olt), FadeIn(onu), Create(fb), self.set_src("G.989.3 §11.3.3.15 · Tablo 12-1 (O6, O8)"), run_time=0.6)
        self.at(self.cue("bir PLOAM mesajıyla", 6.2))
        self.play(FadeIn(msg, shift=RIGHT * 0.2), run_time=0.4)
        self.play(msg.animate.move_to([2.4, 2.1, 0]), run_time=1.2)
        self.play(FadeIn(combs), FadeIn(mk), Indicate(combs[2], color=GOLD), run_time=0.7)
        self.at(self.cue("senkronunu kaybedip", 11.4))
        self.play(FadeIn(o5), GrowArrow(a1[0]), FadeIn(a1[1]), run_time=0.6)
        self.at(self.cue("O6'ya girdiğinde", 16.9))
        self.play(FadeIn(o6, scale=0.9), run_time=0.4)
        self.at(self.cue("TO3 zamanlayıcısını", 18.4))
        self.play(FadeIn(clk), Rotate(clk[1], -2 * PI, about_point=clk[0].get_center()), FadeIn(wl), run_time=1.0)
        self.at(self.cue("Süre dolunca", 22.2))
        self.play(GrowArrow(a2[0]), FadeIn(a2[1]), FadeIn(o8, scale=0.9), run_time=0.6)
        self.at(self.cue("koruma kanalına ayarlanır", 25.8))
        self.play(GrowArrow(a3), FadeIn(pc, scale=0.9), mk.animate.next_to(combs[2], UP, buff=0.08), run_time=0.8)
        self.end(pad=0.05)

        # c8a — the ONU optics do work here
        self.beat("c8a")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Burada ONU'nun optiği gerçekten çalışır", h)
        steps = VGroup(sbox("1 · yeni kanala ayar", "Tx + Rx", CH[2], 3.6, 0.95, 19, 15), sbox("2 · yeni kanalda senkron", "↓ PSync", STATE, 3.6, 0.95, 19, 15),
                       sbox("3 · kendini bildir", "↑ Tuning_Response", TW_US, 3.6, 0.95, 19, 15)).arrange(RIGHT, buff=0.55).move_to([0, 1.35, 0])
        sa = VGroup(*[arrow(steps[i].get_right(), steps[i + 1].get_left(), MUTED, 2.5, 0.14) for i in range(2)])
        po = sbox("koruma tarafı OLT CT", None, OLTC, 3.0, 0.8, 18).move_to([-4.3, -0.7, 0])
        slot = VGroup(Rectangle(width=3.2, height=0.6, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.15),
                      T("çekişmeli tahsis", 17, GOLD, BOLD))
        slot[1].move_to(slot[0])
        slot.move_to([0.6, -0.7, 0])
        sd = arrow(po.get_right(), slot.get_left(), GOLD, 2.5, 0.14)
        rng_ = tag("önceden mesafesi ölçülmüş", GOOD, 16).next_to(slot, DOWN, buff=0.12)
        ons = VGroup(*[onu_icon("ONU", ONUC, 0.95, 0.42, 14) for _ in range(3)]).arrange(DOWN, buff=0.15).move_to([5.3, -0.7, 0])
        ua = VGroup(*[arrow(o.get_left(), slot.get_right() + UP * (0.15 - 0.15 * k), TW_US, 2, 0.12) for k, o in enumerate(ons)])
        jt = T("Ek J.2.2 (koşullu)", 15, MUTED).next_to(po, DOWN, buff=0.12)
        to = pill("TO2 · TO3: standartta değer yok", WARN, 20).move_to([0, -2.7, 0])
        self.at(self.cue("yeni kanala ayar", 3.4))
        self.play(FadeIn(steps[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("yeni kanalda senkron", 4.8))
        self.play(GrowArrow(sa[0]), FadeIn(steps[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("kendini bildirme", 6.5))
        self.play(GrowArrow(sa[1]), FadeIn(steps[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Koruma tarafındaki OLT", 9.3))
        self.play(FadeIn(po), FadeIn(jt), self.set_src("G.989.3 Ek J.2.2 · Tablo 12-1"), run_time=0.5)
        self.at(self.cue("varlıklarını bildirebileceği", 12.5))
        self.play(GrowArrow(sd), FadeIn(slot), FadeIn(ons), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in ua], lag_ratio=0.2), run_time=0.7)
        self.at(self.cue("önceden mesafesi", 16.4))
        self.play(FadeIn(rng_, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("TO2 ve TO3", 21.2))
        self.play(FadeIn(to, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # c9 — terminology trap
        self.beat("c9")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Terim tuzağı: iki ayrı “B tipi”", h)
        cl = card("G.989.2 · A / B tipi BAĞLANTI", "A = yükselteçsiz OLT alıcısı\nB = yükselteçli OLT alıcısı", "Tablo 11-6 / 11-7, Not 3 / 4", TW_US, w=6.0, h=2.0, tsize=21, bsize=19).move_to([-3.4, 0.9, 0])
        cr = card("G.989.3 · B tipi KORUMA", "1:1 · iki OLT kanal sonlandırıcısı\nher kanal çifti için", "§18", ACC, w=6.0, h=2.0, tsize=21, bsize=19).move_to([3.4, 0.9, 0])
        ne = T("≠", 48, WARN, BOLD).move_to([0, 0.9, 0])
        fld = VGroup(RoundedRectangle(corner_radius=0.1, width=7.4, height=0.7, stroke_color=GOLD, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                     T("Channel_Profile · “Optical link type” (A / B)", 18, GOLD, BOLD))
        fld[1].move_to(fld[0])
        fld.move_to([-1.8, -1.45, 0])
        okk = T("→ bağlantı tipi ✓", 19, GOOD, BOLD).next_to(fld, RIGHT, buff=0.3).shift(UP * 0.2)
        nok = T("→ koruma ✗", 19, WARN, BOLD).next_to(fld, RIGHT, buff=0.3).shift(DOWN * 0.22)
        self.at(self.cue("A tipi ve B tipi bağlantı", 1.4))
        self.play(FadeIn(cl[0]), FadeIn(cl[1]), self.set_src("G.989.2 Tablo 11-6/11-7 · G.989.3 §18, §11 (Channel_Profile)"), run_time=0.5)
        self.at(self.cue("yükselteçsiz ve yükselteçli", 4.7))
        self.play(FadeIn(cl[2:], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("bambaşka bir şeydir", 8.8))
        self.play(FadeIn(cr, shift=LEFT * 0.1), FadeIn(ne, scale=0.8), run_time=0.6)
        self.at(self.cue("Kanal profilindeki", 13.1))
        self.play(FadeIn(fld, shift=UP * 0.1), FadeIn(okk), run_time=0.6)
        self.at(self.cue("korumayı değil", 17.4))
        self.play(FadeIn(nok), run_time=0.4)
        self.end(pad=0.05)

        self.note10("c10", [("1", "↓ geri getirme süresi < ONU'nun sabrı", "ONU yeniden ayara karar verirse B tipi değil, WLCP devreye girer.", "Bir:"),
                            ("2", "Bekleme tarafı gerçekten karanlık mı?", "Aynı kanalda iki verici: koruma kendisi arızaya dönüşür.", "İki:")])
        self.bridge_beat("c11", "Ağ ayakta.\nAma bir OLT'nin ya da ONU'nun standarda uyduğunu nasıl kanıtlarız?")
        self.save_timeline("ep10_p2C")
