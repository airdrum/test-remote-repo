"""B04 · Perde 3 (spektrum: SMSR, MSE, OOB/OOC, WNE) and Perde 4 (göz maskesi ve titreşim)."""
import scipy.signal as sig

from ep03_common import *
from ep04_common import *

DS_NM = [thz_to_nm(f) for f in (187.8, 187.7, 187.6, 187.5)]


class E4P3A(Act4):
    HDR, MANIFEST, FIRST = H4[3], M4("p3"), True

    def construct(self):
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Spektrum")
        self.at(self.cue("Standart kaynak", 2))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Kaynak tipi ve SMSR")
        x0, y0, sy, fl = -6.0, -2.4, 0.07, -58.0
        ax = mini_axes(x0, y0, 6.6, 4.3, "optik frekans", "güç (dB)", xbuff=0.12)
        o = np.array([x0 + 3.0, y0, 0])
        spec = spec_db(o, 1.0, sy, [(0, 0), (-1.2, -37), (1.2, -33), (-2.4, -46), (2.4, -44)], (-2.95, 3.5), floor=fl, w=0.012, n=700)
        ytop, yside = y0 + (0 - fl) * sy, y0 + (-33 - fl) * sy
        axx = o[0] + 2.55
        sm = VGroup(DashedLine([o[0] + 0.1, ytop, 0], [axx + 0.1, ytop, 0], color=GOLD, stroke_width=1.5),
                    DashedLine([o[0] + 1.25, yside, 0], [axx + 0.1, yside, 0], color=GOLD, stroke_width=1.5),
                    DoubleArrow([axx, yside, 0], [axx, ytop, 0], buff=0, color=GOLD, stroke_width=3, tip_length=0.14))
        smt = T("SMSR", 22, GOLD, BOLD).next_to([axx, (ytop + yside) / 2, 0], RIGHT, buff=0.15)
        info = VGroup(T("kaynak tipi zorunlu değil", 20, MUTED), T("uygun verici: yalnızca", 20, TXT), T("tek boylamsal modlu (SLM) lazer", 20, TW_DS, BOLD),
                      T("amaç: mod bölüşme gürültüsü", 20, TXT), T("en küçük SMSR = 30 dB", 30, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 0.0, 0])
        self.play(Create(ax), FadeIn(info[0]), self.set_src("G.989.2 §11.1.5.1 · §11.1.5.2 · §9.3.8"), run_time=0.7)
        self.at(self.cue("uygun vericilerin", 4))
        self.play(Create(spec), FadeIn(info[1:3]), run_time=1.2)
        self.at(self.cue("Mod bölüşme", 9))
        self.play(FadeIn(sm), FadeIn(smt), FadeIn(info[3]), run_time=0.7)
        self.at(self.cue("otuz desibel", 14))
        self.play(FadeIn(info[4], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d1b")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Mod bölüşme gürültüsü (MPN)", h)
        bx0, by0 = -6.0, -0.6

        def modes(hs):
            return VGroup(*[Rectangle(width=0.32, height=v, stroke_width=0, fill_color=CH[i % 4], fill_opacity=0.9).move_to([bx0 + 0.5 + 0.55 * i, by0 + v / 2, 0])
                            for i, v in enumerate(hs)])
        S = [[0.5, 1.0, 1.7, 1.0, 0.5], [1.2, 0.5, 1.0, 1.5, 0.5], [0.5, 1.6, 0.9, 0.6, 1.1], [0.9, 0.7, 1.6, 0.6, 0.9]]
        mb = modes(S[0])
        base = Line([bx0, by0, 0], [bx0 + 3.3, by0, 0], color=MUTED, stroke_width=2)
        mt = VGroup(T("çok modlu lazer", 20, TXT, BOLD), T("toplam güç sabit ·", 17, MUTED), T("modlar arasında el değiştirir", 17, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(base, DOWN, buff=0.2).align_to(base, LEFT)
        fib = Arrow([-1.6, 0.95, 0], [3.0, 0.95, 0], buff=0, color=FEED, stroke_width=4, max_tip_length_to_length_ratio=0.05)
        ft = T("dispersiyonlu fiber: modlar farklı hızda", 17, FEED).next_to(fib, UP, buff=0.12)
        g = lambda c, s, a, col: VMobject(color=col, stroke_width=3).set_points_smoothly([[c + x, -0.6 + a * np.exp(-(x / s) ** 2), 0] for x in np.linspace(-0.6, 0.6, 30)])
        p_in = VGroup(*[g(-1.2, 0.18, 1.0 - 0.15 * i, CH[i]) for i in range(3)])
        p_out = VGroup(*[g(4.4 + 0.42 * (i - 1), 0.2, 0.9 - 0.15 * i, CH[i]) for i in range(3)])
        rx = box(1.0, 0.6, "Rx", "#94A3B8", 16).move_to([6.1, -0.35, 0])
        nt = T("alıcıda: güç dalgalanması → gürültü", 18, WARN, BOLD).move_to([3.4, -1.3, 0])
        res = pill("yan modlar −30 dB → etki önemsiz", GOOD, 22).move_to(DOWN * 2.45)
        self.at(self.cue("Çok modlu", 2))
        self.play(Create(base), FadeIn(mb), FadeIn(mt), run_time=0.7)
        for k in (1, 2, 3):
            self.play(Transform(mb, modes(S[k])), run_time=0.6)
        self.at(self.cue("Dispersiyonlu", 7))
        self.play(GrowArrow(fib), FadeIn(ft), FadeIn(p_in), run_time=0.8)
        self.play(TransformFromCopy(p_in, p_out), FadeIn(rx), run_time=1.0)
        self.at(self.cue("bu el değiştirme", 11))
        self.play(FadeIn(nt), run_time=0.5)
        self.at(self.cue("Yan modları otuz", 15))
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d1a")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("SMSR nerede ölçülür?", h)
        y = 0.9
        las = box(1.6, 0.8, "lazer", TW_DS, 20).move_to([-5.4, y, 0])
        cp = DashedLine([-3.8, y - 0.8, 0], [-3.8, y + 0.8, 0], color=GOLD, stroke_width=2.5)
        wm = box(1.2, 1.1, "WM", "#3B4A75", 18).move_to([-1.0, y, 0])
        cg = DashedLine([0.9, y - 0.8, 0], [0.9, y + 0.8, 0], color=ACC, stroke_width=2.5)
        odn = box(1.3, 0.7, "ODN", FEED, 16).move_to([4.6, y, 0])
        ln = VGroup(Line(las.get_right(), wm.get_left(), color=FEED, stroke_width=3), Line(wm.get_right(), odn.get_left(), color=FEED, stroke_width=3))
        lb = VGroup(T("S/R-CP", 16, GOLD, BOLD).next_to(cp, UP, buff=0.06), T("S/R-CG", 16, ACC, BOLD).next_to(cg, UP, buff=0.06))
        c1 = card("SMSR ≥ 30 dB", "lazer çıkışında, süzmeden önce\n→ lazer özelliği", None, GOLD, w=5.6, h=1.7, tsize=24, bsize=19).move_to([-3.4, -1.25, 0])
        c2 = card("OOB / OOC sınırları", "arayüzde (WM süzmesi dahil)\n→ arayüz özelliği", None, ACC, w=5.6, h=1.7, tsize=24, bsize=19).move_to([3.0, -1.25, 0])
        self.play(FadeIn(las), FadeIn(wm), FadeIn(odn), Create(ln), self.set_src("G.989.2 §9.3.8 · Tablo 11-4, 11-5"), run_time=0.8)
        self.at(self.cue("lazerin çıkışında", 2))
        self.play(Indicate(las, color=GOLD), run_time=0.8)
        self.at(self.cue("Tablo satırı", 5))
        self.play(Create(cp), FadeIn(lb[0]), run_time=0.5)
        self.at(self.cue("Yani SMSR", 9))
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("arayüzdeki bant dışı", 11))
        self.play(Create(cg), FadeIn(lb[1]), FadeIn(c2, shift=UP * 0.15), run_time=0.7)
        self.end(pad=0.05)

        self.beat("d2")
        self.clear(h)
        h = self.show_heading("En büyük spektral sapma (MSE)", h)
        k, yb = 0.115, -1.6
        base = Line([-6.3, yb, 0], [6.3, yb, 0], color=MUTED, stroke_width=2)
        win = Rectangle(width=40 * k, height=2.3, stroke_width=0, fill_color=TW_DS, fill_opacity=0.12).move_to([0, yb + 1.15, 0])
        wl = VGroup(DashedLine([-20 * k, yb, 0], [-20 * k, yb + 2.3, 0], color=TW_DS, stroke_width=2), DashedLine([20 * k, yb, 0], [20 * k, yb + 2.3, 0], color=TW_DS, stroke_width=2))
        f0 = VGroup(Line([0, yb - 0.08, 0], [0, yb + 0.08, 0], color=TXT, stroke_width=2), T("f₀ (Tablo 11-2)", 16, TXT).next_to([0, yb, 0], DOWN, buff=0.12))
        tk = VGroup(*[T(s, 15, TW_DS, BOLD).next_to([x, yb, 0], DOWN, buff=0.12) for s, x in (("−20 GHz", -20 * k), ("+20 GHz", 20 * k))])
        las = Line([0, yb, 0], [0, yb + 2.0, 0], color=GOLD, stroke_width=5)
        mt = T("± 20 GHz · tek yönlü sapma", 24, TW_DS, BOLD).move_to([0, yb + 2.65, 0])
        ps = VGroup(pill("sabit ve ayarlanabilir vericiler", ACC, 18), pill("en kötü koşul · yaşlanma dahil", GOLD, 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-4.5, 0.4, 0])
        no = VGroup(T("OLT için ayrı kayma /", 18, WARN, BOLD), T("kararlılık parametresi yok", 18, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, 0.4, 0])
        self.play(Create(base), FadeIn(f0), Create(las), self.set_src("G.989.2 §11.1.5.2.4 · Tablo 11-4, 11-5"), run_time=0.7)
        self.at(self.cue("aşağı yönde artı eksi", 4))
        self.play(FadeIn(win), Create(wl), FadeIn(tk), FadeIn(mt), run_time=0.7)
        self.play(las.animate.shift(RIGHT * 14 * k), run_time=0.6)
        self.play(las.animate.shift(LEFT * 30 * k), run_time=0.8)
        self.play(las.animate.shift(RIGHT * 19 * k), run_time=0.6)
        self.at(self.cue("Hem sabit", 9))
        self.play(FadeIn(ps[0], shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("ve en kötü", 12))
        self.play(FadeIn(ps[1], shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("OLT için ayrı", 16))
        self.play(FadeIn(no, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("bütün sınır", 21))
        self.play(Indicate(mt, color=TW_DS, scale_factor=1.08), run_time=0.8)
        self.end(pad=0.05)

        self.beat("d2a")
        self.clear(h)
        self.set_badge("tc")
        h = self.show_heading("Channel_Profile · oktet 11", h)
        cells = VGroup(*[VGroup(Square(0.75, stroke_color=OC_C, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), T("s", 24, OC_C, BOLD)) for _ in range(8)])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0.06).move_to([-2.4, 1.2, 0])
        ct = VGroup(T("↓ frekans kayması", 22, TXT, BOLD), T("gerçek − nominal (biliniyorsa)", 18, MUTED), T("işaretli · 0,1 GHz birimi", 20, OC_C, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(cells, RIGHT, buff=0.45)
        tb = table(["Değer", "Anlamı"], [["0000 0000", "kayma yok"], ["1000 0000", "kayma bilinmiyor"]], [3.0, 4.0], size=22, hsize=17, row_h=0.58).move_to([-2.9, -1.0, 0])
        hint = VGroup(Arrow([1.0, -1.0, 0], [2.4, -1.0, 0], buff=0, color=GOOD, stroke_width=3), card("ONU", "ayarlanabilir alıcı\niçin ipucu", None, GOOD, w=3.4, h=1.5, tsize=22, bsize=19).move_to([4.3, -1.0, 0]))
        self.at(self.cue("kanal profilindeki", 2))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.06), FadeIn(ct[0]), self.set_src("G.989.3 Tablo 11-18 · oktet 11"), run_time=0.9)
        self.at(self.cue("nominal değerden", 5))
        self.play(FadeIn(ct[1:]), run_time=0.5)
        self.play(FadeIn(tb), run_time=0.5)
        self.at(self.cue("ONU'nun ayarlanabilir", 11))
        self.play(GrowArrow(hint[0]), FadeIn(hint[1], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d2b")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("± 20 GHz lazer diliyle", h)
        r1 = VGroup(T("Δλ = λ² · Δf / c", 24, MUTED), T("± 20 GHz @ 1600 nm ≈ ± 0,17 nm", 30, TW_DS, BOLD)).arrange(RIGHT, buff=0.6).move_to(UP * 1.55)
        r2 = VGroup(T("DFB: ≈ 0,1 nm / K", 28, TXT, BOLD), T("→  ≈ ± 2 K", 34, GOLD, BOLD)).arrange(RIGHT, buff=0.6).move_to(UP * 0.45)
        chip = Rectangle(width=1.6, height=0.35, stroke_color=TW_DS, stroke_width=2, fill_color=TW_DS, fill_opacity=0.5).move_to([-2.0, -1.05, 0])
        tec = VGroup(Rectangle(width=2.6, height=0.55, stroke_color=GOLD, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([-2.0, -1.5, 0]),
                     *[Rectangle(width=0.16, height=0.42, stroke_width=0, fill_color=GOLD if i % 2 else WARN, fill_opacity=0.7).move_to([-3.1 + 0.25 * i, -1.5, 0]) for i in range(10)])
        th = Dot([-0.95, -1.05, 0], radius=0.08, color=WARN)
        loop = VGroup(box(1.9, 0.6, "sıcaklık kontrol", GOLD, 15).move_to([2.2, -1.3, 0]))
        lw = VGroup(Line(th.get_center(), [1.25, -1.05, 0], color=MUTED, stroke_width=2), Line([1.25, -1.55, 0], [-0.7, -1.55, 0], color=MUTED, stroke_width=2))
        lt = VGroup(T("lazer yongası", 15, TW_DS).next_to(chip, UP, buff=0.08), T("TEC", 15, GOLD, BOLD).next_to(tec[0], DOWN, buff=0.08), T("termistör", 14, WARN).move_to([-0.6, -0.75, 0]))
        tecg = VGroup(tec, chip, th, lt, loop, lw)
        tecg.scale(1.25).move_to([0, -1.15, 0])
        cap = T("OLT lazerleri pratikte termoelektrik soğutucuyla sıcaklık kontrollü", 21, GOOD, BOLD).move_to(DOWN * 2.6)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Tipik bir DFB", 6))
        self.play(FadeIn(r2[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yani bu sınır", 12))
        self.play(FadeIn(r2[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Bu yüzden OLT", 19))
        self.play(FadeIn(tec), FadeIn(chip), FadeIn(th), FadeIn(lt), run_time=0.7)
        self.play(FadeIn(loop), Create(lw), FadeIn(cap), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p3A")


class E4P3B(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[3], M4("p3"), "fiz"

    def construct(self):
        self.beat("d3")
        self.set_badge("std")
        h = self.show_heading("Komşuları korumak: iki güç yoğunluğu sınırı")
        axg, X = nm_axis(1595, 1627, x0=-5.0, x1=6.1, y=0.25, step=1, label_every=5, size=14)
        chans = VGroup(*[Line([X(v), 0.25, 0], [X(v), 1.6, 0], color=TW_DS, stroke_width=4) for v in DS_NM])
        me = chans[1]
        ptp = band(X, 1603, 1625, 0.7, 0.9, PTP, "PtP WDM kanalları", op=0.45, lsize=17, lcolor=TXT)
        tl = T("TWDM ↓", 16, TW_DS, BOLD).next_to(chans, LEFT, buff=0.25)
        ooc = VGroup(*[CurvedArrow([X(DS_NM[1]), 1.65, 0], [X(DS_NM[j]), 1.65, 0], angle=-2.0 if j > 1 else 2.0, color=ACC, stroke_width=2.5, tip_length=0.1) for j in (0, 2, 3)])
        oob = CurvedArrow([X(DS_NM[1]) + 0.05, 1.8, 0], [X(1612), 1.2, 0], angle=-0.7, color=PTP, stroke_width=2.5, tip_length=0.14)
        oobt = T("bant dışı (OOB)", 17, PTP, BOLD).move_to([X(1608), 2.2, 0])
        ooct = T("kanal dışı (OOC)", 17, ACC, BOLD).move_to([chans.get_x(), 2.2, 0])
        tb = table(["kanal başına, dBm / 15 GHz", "4 kanal", "8 kanal"], [["kanal dışı (OOC) → diğer TWDM kanalları", "−34,5", "−42,4"], ["bant dışı (OOB) → PtP WDM kanalları", "−44,9", "−52,1"]],
                   [6.6, 2.3, 2.3], size=22, hsize=17, row_h=0.6).move_to(DOWN * 1.65)
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(chans), FadeIn(tl), FadeIn(ptp), self.set_src("G.989.2 Tablo 11-4, 11-5"), run_time=0.8)
        self.at(self.cue("ikisi de on beş", 3))
        self.play(FadeIn(tb[0]), me.animate.set_stroke(GOLD, 6), run_time=0.5)
        self.at(self.cue("Kanal dışı sınır", 6))
        self.play(LaggedStart(*[Create(a) for a in ooc], lag_ratio=0.2), FadeIn(ooct), run_time=0.8)
        self.at(self.cue("dört kanallı sistemde", 9))
        self.play(FadeIn(tb[1], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Bant dışı sınır ise", 17))
        self.play(Create(oob), FadeIn(oobt), run_time=0.7)
        self.at(self.cue("eksi kırk dört", 22))
        self.play(FadeIn(tb[2], shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d3a")
        self.clear(h)
        h = self.show_heading("Notlar: varsayımlar", h)
        c1 = card("Kanal dışı (Not 5)", "kurban: diğer TWDM kanalı — FEC ile\nWM süzmesi ile kontrol\n0,1 dB ceza bütçesi", None, ACC, w=5.8, h=2.4, tsize=24, bsize=20).move_to([-3.1, 0.35, 0])
        c2 = card("Bant dışı (Not 4)", "kurban: PtP WDM — FEC olmadan\nuygun süzme ile kontrol\n0,1 dB ceza bütçesi", None, PTP, w=5.8, h=2.4, tsize=24, bsize=20).move_to([3.1, 0.35, 0])
        res = pill("FEC'siz kurban → bant dışı sınır daha sıkı", WARN, 22).move_to(DOWN * 1.9)
        self.at(self.cue("Kanal dışı sınır", 2))
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Bant dışı sınır da", 10))
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("bu yüzden daha sıkıdır", 20))
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d3b")
        self.clear(h)
        h = self.show_heading("Dört kanaldan sekize", h)
        tb = table(["dBm / 15 GHz", "4 kanal", "8 kanal", "sıkılaşma"], [["bant dışı (OOB)", "−44,9", "−52,1", "7,2 dB"], ["kanal dışı (OOC)", "−34,5", "−42,4", "7,9 dB"]],
                   [3.6, 2.2, 2.2, 2.4], size=23, hsize=17, row_h=0.6).move_to(UP * 1.25)

        def grp(n, cx):
            lines = VGroup(*[Line([cx + 0.42 * (i - (n - 1) / 2), -1.2, 0], [cx + 0.42 * (i - (n - 1) / 2), -0.2, 0], color=GOLD if i == 1 else WARN, stroke_width=4) for i in range(n)])
            return VGroup(lines, T(f"{n} kanal → {n - 1} girişimci", 20, TXT, BOLD).next_to(lines, DOWN, buff=0.18))
        g4, g8 = grp(4, -3.2), grp(8, 3.0)
        vt = T("kurban", 14, GOLD).next_to(g4[0][1], UP, buff=0.06)
        note = VGroup(T("§6.3: PSD değerleri 4 kanal · 20 km için optimize", 21, GOLD, BOLD), T("8 kanal / 40 km: ileride çalışılacak", 21, MUTED)).arrange(DOWN, buff=0.1).move_to(DOWN * 2.6)
        self.play(FadeIn(tb[0]), FadeIn(tb[1:]), self.set_src("G.989.2 Tablo 11-4, 11-5 · §6.3"), run_time=0.6)
        self.at(self.cue("bant dışında yedi", 3))
        self.play(Indicate(tb[1][4], color=GOLD), Indicate(tb[2][4], color=GOLD), run_time=0.9)
        self.at(self.cue("Girişimci sayısı", 9))
        self.play(FadeIn(g4), FadeIn(vt), run_time=0.5)
        self.at(self.cue("sekiz kanalda yedi", 12))
        self.play(FadeIn(g8), run_time=0.5)
        self.at(self.cue("Standart ayrıca", 14))
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d4")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Sınırları bastırma oranına çevirelim", h)
        eqs = VGroup(T("P_maks (10G E2) = +11 dBm", 24, TXT, BOLD), T("kanal dışı sınır (4 kanal) = −34,5 dBm / 15 GHz", 24, ACC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-2.3, 1.75, 0])
        ek = pill("Ek D yöntemi: P_maks − PSD sınırı", MUTED, 18).move_to([4.6, 1.75, 0])
        bx, k = -2.6, 0.1
        rows = [("kanal dışı · 4 kanal", 45.5, ACC, 0.45), ("bant dışı · 4 kanal", 55.9, PTP, -0.55), ("bant dışı · 8 kanal", 63.1, PTP, -1.55)]
        bars = VGroup()
        for name, v, c, y in rows:
            r = Rectangle(width=v * k, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.75).move_to([bx + v * k / 2, y, 0])
            bars.add(VGroup(T(name, 19, TXT, BOLD).next_to([bx, y, 0], LEFT, buff=0.2), r, T(tr(v, "{:.1f}") + " dB", 20, c, BOLD).next_to(r, RIGHT, buff=0.15)))
        sm = Rectangle(width=30 * k, height=0.55, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.55).move_to([bx + 15 * k, 0.45, 0])
        smt = T("SMSR 30 dB", 17, BG, BOLD).move_to(sm)
        wmt = T("WM süzmesi", 15, BG, BOLD).move_to([bx + 37.75 * k, 0.45, 0])
        sml = DashedLine([bx + 30 * k, 0.85, 0], [bx + 30 * k, -2.0, 0], color=GOLD, stroke_width=2)
        msg = T("PtP WDM FEC'siz → korumak daha pahalı", 22, WARN, BOLD).move_to(DOWN * 2.6)
        self.at(self.cue("On gigabit E2", 1))
        self.play(FadeIn(eqs[0]), self.set_src("G.989.2 Tablo 11-5 · Ek D.4"), run_time=0.5)
        self.at(self.cue("Kanal dışı sınır eksi", 4))
        self.play(FadeIn(eqs[1]), run_time=0.5)
        self.at(self.cue("aradaki fark kırk", 8))
        self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]), run_time=0.8)
        self.at(self.cue("otuz desibellik SMSR", 12))
        self.play(FadeIn(sm), FadeIn(smt), run_time=0.5)
        self.at(self.cue("aradaki fark çoklayıcının", 15))
        self.play(FadeIn(wmt), run_time=0.5)
        self.at(self.cue("Bu çıkarma", 19))
        self.play(FadeIn(ek, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d4b")
        self.at(self.cue("Aynı artı on bir", 2))
        self.play(FadeIn(sml), FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]), run_time=0.8)
        self.at(self.cue("sekiz kanallı sistemde altmış", 7))
        self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]), run_time=0.8)
        self.at(self.cue("PtP WDM kanalları", 11))
        self.play(FadeIn(msg, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p3B")


class E4P3C(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[3], M4("p3"), "fiz"

    def construct(self):
        self.beat("d4a")
        self.set_badge("std")
        h = self.show_heading("İstem dışı güç yoğunluğu (WNE)")
        tb = table(["", "2,5G ↓", "10G ↓"], [["en büyük ↓ WNE-PSD (dBm / 15 GHz)", "−63,5", "−63,7"]], [6.4, 2.2, 2.2], size=23, hsize=18, row_h=0.62).move_to(UP * 1.6)
        yb, x0 = -2.0, -5.8
        base = Line([x0, yb, 0], [6.0, yb, 0], color=MUTED, stroke_width=2)
        slots = [("ONU-B", -5.6, -2.6), ("ONU-A", -2.4, 0.6), ("ONU-C", 0.8, 3.8)]
        sl = VGroup()
        for name, a, b in slots:
            sl.add(VGroup(DashedLine([a, yb, 0], [a, yb + 1.5, 0], color=LINE, stroke_width=1.5), T(name, 16, TW_US if name == "ONU-A" else MUTED, BOLD).move_to([(a + b) / 2, yb + 1.7, 0])))
        trace = VMobject(color=TW_US, stroke_width=3).set_points_as_corners([[x0, yb + 0.12, 0], [-2.4, yb + 0.12, 0], [-2.3, yb + 1.3, 0], [0.5, yb + 1.3, 0], [0.6, yb + 0.12, 0], [6.0, yb + 0.12, 0]])
        wl = DashedLine([x0, yb + 0.2, 0], [6.0, yb + 0.2, 0], color=GOLD, stroke_width=2)
        wt = T("≤ ↑ WNE-PSD", 16, GOLD, BOLD).move_to([-4.1, yb + 0.45, 0])
        ut = T("↑ tanımı: ONU'ya ait olmayan burst'ler sırasında izin verilen güç", 19, TW_US, BOLD).move_to([0, 0.3, 0])
        ds = pill("↓ satırının tanımı: G.989'a bırakılmış", MUTED, 19).move_to(DOWN * 2.75)
        self.play(FadeIn(tb[0]), self.set_src("G.989.2 Tablo 11-4, 11-5 · §11.1.5.2.9"), run_time=0.4)
        self.at(self.cue("iki buçuk gigabitte", 4))
        self.play(FadeIn(tb[1], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Yukarı yönde bu kavram", 9))
        self.play(Create(base), FadeIn(sl), run_time=0.6)
        self.play(Create(trace), run_time=0.9)
        self.at(self.cue("ONU'ya ait olmayan", 13))
        self.play(Create(wl), FadeIn(wt), FadeIn(ut), run_time=0.7)
        self.at(self.cue("Aşağı yön satırının", 18))
        self.play(FadeIn(ds, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d5")
        self.clear(h)
        h = self.show_heading("Kanal dışı maske: iki düzey", h)
        yb = -0.9
        base = Line([-6.3, yb, 0], [0.2, yb, 0], color=MUTED, stroke_width=2)
        own = Line([-5.6, yb, 0], [-5.6, yb + 2.6, 0], color=TW_DS, stroke_width=4)
        ownt = T("verici", 15, TW_DS, BOLD).next_to(own, UP, buff=0.06)
        o1, o2 = yb + 0.95, yb + 0.35
        cx = [-3.5, -1.1]
        pts = [[-4.9, o1, 0]]
        for c in cx:
            pts += [[c - 0.45, o1, 0], [c - 0.45, o2, 0], [c + 0.45, o2, 0], [c + 0.45, o1, 0]]
        pts.append([0.2, o1, 0])
        mask = VGroup(VMobject(color=GOLD, stroke_width=3).set_points_as_corners(pts),
                      *[Line([c - 0.45, o2, 0], [c + 0.45, o2, 0], color=WARN, stroke_width=5) for c in cx])
        vic = VGroup(*[DashedVMobject(Rectangle(width=0.9, height=1.7, color=MUTED, stroke_width=1.5), num_dashes=24).move_to([c, yb + 0.85, 0]) for c in cx])
        vt = T("diğer kanalların ± MSE aralıkları", 15, MUTED).move_to([-2.3, yb + 2.0, 0])
        l1 = T("OOC1 · aralıklar arası · uyumsuz", 16, GOLD, BOLD).move_to([-2.3, yb - 0.35, 0])
        l2 = T("OOC2 · aralık içi · uyumlu (daha sıkı)", 16, WARN, BOLD).move_to([-2.3, yb - 0.7, 0])
        tbn = VGroup(T("↓ tablosu: kanal sayısı başına tek OOC değeri", 19, TXT, BOLD), T("OOC1 / OOC2 ayrımı: ↑ tablolarında", 19, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-2.8, -2.6, 0])
        mx, mb = 3.6, -0.9
        mbase = Line([mx - 2.6, mb, 0], [mx + 2.6, mb, 0], color=MUTED, stroke_width=2)
        car = Arrow([mx, mb, 0], [mx, mb + 2.6, 0], buff=0, color=TW_DS, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        rect = Rectangle(width=2.4, height=0.9, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.3).move_to([mx, mb + 0.45, 0])
        ml = VGroup(T("½ güç: taşıyıcı", 16, TW_DS, BOLD).next_to(car, RIGHT, buff=0.1).shift(UP * 0.8),
                    T("½ güç: 15 GHz dikdörtgen", 16, GOLD, BOLD).next_to(rect, DOWN, buff=0.12), T("Ek VIII · NRZ modeli", 19, TXT, BOLD).move_to([mx, mb + 3.0, 0]))
        self.play(Create(base), Create(own), FadeIn(ownt), FadeIn(vic), FadeIn(vt), self.set_src("G.989.2 §9.3.9 · Ek VIII.5"), run_time=0.8)
        self.play(Create(mask), FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.at(self.cue("Aşağı yön tablosu", 7))
        self.play(FadeIn(tbn[0]), run_time=0.5)
        self.at(self.cue("birinci ve ikinci", 11))
        self.play(FadeIn(tbn[1]), run_time=0.5)
        self.at(self.cue("Ek sekizdeki", 15))
        self.play(Create(mbase), FadeIn(ml[2]), GrowArrow(car), FadeIn(ml[0]), run_time=0.7)
        self.at(self.cue("on beş gigahertzlik", 19))
        self.play(GrowFromEdge(rect, DOWN), FadeIn(ml[1]), run_time=0.6)
        self.end(pad=0.05)

        self.note2("d6", ("SMSR ≠ güç yoğunluğu", "SMSR lazer çıkışında, PSD arayüzde ölçülür: birbirinin yerine koymayın."),
                   ("Sekiz kanal planı = kendi doğrulamanız", "PSD sınırları dört kanal için optimize; marjı kendiniz doğrulayın."))
        self.bridge_beat("d7", "Spektrum temiz.\nPeki zaman ekseninde sinyal ne kadar temiz?")
        self.save_timeline("ep04_p3C")


# ================================ PERDE 4 ======================================
EO, EW, EH = np.array([-4.4, -1.6, 0]), 3.4, 2.5


def eye_axes(o=EO, W=EW, H=EH):
    labs = VGroup()
    for v, s in ((0, "0"), (0.5, "0,5"), (1, "1")):
        labs.add(T(s, 14, MUTED).next_to(o + np.array([-0.3 * W, v * H, 0]), LEFT, buff=0.08))
    for u, s in ((0, "0"), (1, "1 UI")):
        labs.add(T(s, 14, MUTED).next_to(o + np.array([u * W, -0.5 * H, 0]), DOWN, buff=0.08))
    return labs


class E4P4A(Act4):
    HDR, MANIFEST, FIRST = H4[4], M4("p4"), True

    def construct(self):
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Göz maskesi ve titreşim")
        self.at(self.cue("Göz diyagramı", 1.5))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Göz diyagramı")
        scr = eye_frame(EO, EW, EH)
        eye = eye_traces(EO, EW, EH, ov=0.14)
        ax = eye_axes()
        P = lambda u, v: EO + np.array([u * EW, v * EH, 0])
        op = VGroup(DoubleArrow(P(0.5, 0.12), P(0.5, 0.88), buff=0, color=GOOD, stroke_width=3, tip_length=0.14), T("açıklık", 18, GOOD, BOLD).next_to(P(0.5, 0.5), RIGHT, buff=0.12))
        ov = VGroup(Arrow(P(1.05, 1.42), P(0.27, 1.12), buff=0.05, color=WARN, stroke_width=2.5, max_tip_length_to_length_ratio=0.12), T("aşma", 18, WARN, BOLD).move_to(P(1.15, 1.42) + RIGHT * 0.15))
        un = VGroup(Arrow(P(1.05, -0.42), P(0.27, -0.12), buff=0.05, color=WARN, stroke_width=2.5, max_tip_length_to_length_ratio=0.12), T("alt aşma", 18, WARN, BOLD).move_to(P(1.15, -0.42) + RIGHT * 0.35))
        tb = VGroup(T("OLT göz maskesi", 26, TXT, BOLD), T("Tablo 11-8", 30, GOLD, BOLD), T("2,5G ve 10G: aynı değerler", 22, ACC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, 0.2, 0])
        self.play(FadeIn(scr), FadeIn(ax), LaggedStart(*[Create(e) for e in eye], lag_ratio=0.02), self.set_src("G.989.2 §11.1.5.3 · Tablo 11-8"), run_time=1.2)
        self.at(self.cue("yalnızca açıklığı", 3))
        self.play(GrowFromCenter(op[0]), FadeIn(op[1]), run_time=0.5)
        self.at(self.cue("aşma ve alt aşma", 5))
        self.play(FadeIn(ov), FadeIn(un), run_time=0.6)
        self.at(self.cue("OLT vericisinin göz", 8))
        self.play(FadeIn(tb[0:2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ve değerler her iki", 12))
        self.play(FadeIn(tb[2], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e1a")
        self.play(FadeOut(op), FadeOut(ov), FadeOut(un), FadeOut(tb), run_time=0.4)
        self.play(*[e.animate.set_stroke(opacity=0.3) for e in eye], run_time=0.3)
        msk = eye_mask(EO, EW, EH, 0.4, 0.6)
        wbr = BraceBetweenPoints(P(0.4, 0.25), P(0.6, 0.25), DOWN, color=GOLD, buff=0.05)
        wbt = T("0,2 UI", 15, GOLD, BOLD).next_to(wbr, DOWN, buff=0.04)
        tick = lambda v, s, c: VGroup(DashedLine(P(-0.3, v), P(1.3, v), color=c, stroke_width=1.2, dash_length=0.06), T(s, 14, c, BOLD).next_to(P(1.3, v), RIGHT, buff=0.08))
        t_in = VGroup(tick(0.25, "0,25", GOLD), tick(0.75, "0,75", GOLD))
        t_ou = VGroup(tick(1.25, "1,25", WARN), tick(-0.25, "−0,25", WARN))
        txt = VGroup(T("iç bölge (dikdörtgen)", 21, TXT, BOLD), T("x3 − x2 = 0,2 UI", 22, GOLD, BOLD), T("y1 = 0,25 · y2 = 0,75", 22, GOLD, BOLD),
                     T("yasak: 1 + y3 = 1,25 üstü", 20, WARN, BOLD), T("yasak: −y4 = −0,25 altı", 20, WARN, BOLD), T("aşma / alt aşma ≤ %25", 26, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, 0.0, 0])
        self.at(self.cue("dikdörtgen bir iç bölge", 1))
        self.play(FadeIn(msk), FadeIn(txt[0]), run_time=0.7)
        self.at(self.cue("x üç eksi", 6))
        self.play(FadeIn(wbr), FadeIn(wbt), FadeIn(txt[1]), run_time=0.6)
        self.at(self.cue("Düşey olarak", 11))
        self.play(FadeIn(t_in), FadeIn(txt[2]), run_time=0.6)
        self.at(self.cue("Üstte bir artı", 17))
        self.play(FadeIn(t_ou), FadeIn(txt[3:5]), run_time=0.6)
        self.at(self.cue("yani aşma", 23))
        self.play(FadeIn(txt[5], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e1b")
        self.play(FadeOut(txt), FadeOut(wbr), FadeOut(wbt), run_time=0.4)
        m2 = eye_mask(EO, EW, EH, 0.3, 0.5)
        m3 = eye_mask(EO, EW, EH, 0.47, 0.67)
        sy = T("x2, x3: 0 ve 1 UI'ya göre\nsimetrik olmak zorunda değil", 20, GOLD, BOLD, line_spacing=0.9).move_to([4.0, 1.6, 0])
        org = VGroup(card("OLT maskesi", "G.959.1 §7.2.2.14 · OTN", None, TW_DS, w=5.0, h=1.15, tsize=21, bsize=18),
                     card("ONU maskesi", "G.957 §6.2.5 · SDH", None, TW_US, w=5.0, h=1.15, tsize=21, bsize=18)).arrange(DOWN, buff=0.2).move_to([4.15, -0.65, 0])
        same = T("aynı sayılar, iki ayrı miras", 22, ACC, BOLD).move_to([4.15, -2.35, 0])
        self.play(FadeIn(sy), run_time=0.5)
        self.play(Transform(msk, m2), run_time=0.7)
        self.play(Transform(msk, m3), run_time=0.8)
        self.play(Transform(msk, eye_mask(EO, EW, EH, 0.4, 0.6)), run_time=0.6)
        self.at(self.cue("Bu değerler", 6))
        self.play(FadeIn(org[0], shift=UP * 0.1), self.set_src("G.989.2 Tablo 11-8 (Not 1, 2) · Tablo 11-9"), run_time=0.5)
        self.at(self.cue("ONU vericisinin", 10))
        self.play(FadeIn(org[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Aynı sayılar", 16))
        self.play(FadeIn(same), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e1c")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Aşma nereden gelir? Doğrudan modülasyon", h)
        x0, w = -6.0, 6.4
        t = np.linspace(0, 1, 160)
        st = 0.25

        def plot(y0, hh, title, f, col, sw=3):
            axl = Line([x0, y0, 0], [x0 + w, y0, 0], color=MUTED, stroke_width=1.5)
            tt = T(title, 16, MUTED).next_to([x0, y0 + hh, 0], UP, buff=0.04).align_to([x0, 0, 0], LEFT)
            cv = VMobject(color=col, stroke_width=sw).set_points_as_corners([[x0 + w * a, y0 + hh * f(a), 0] for a in t])
            return VGroup(axl, tt, cv)
        drive = lambda a: 0.1 + 0.8 * (a > st)
        ring = lambda a: 0.1 + 0.75 * (0 if a < st else 1 - np.exp(-(a - st) * 14) * np.cos((a - st) * 62))
        eml = lambda a: 0.1 + 0.75 * (0 if a < st else 1 - np.exp(-(a - st) * 40))
        chirp = lambda a: 0.15 + (0 if a < st else 0.25 + 0.6 * np.exp(-(a - st) * 16) * np.abs(np.cos((a - st) * 62)) ** 0.6)
        flat = lambda a: 0.15 + (0 if a < st else 0.03 * np.exp(-(a - st) * 30))
        p1 = plot(1.25, 0.8, "sürücü akımı", drive, MUTED)
        p2 = plot(-0.85, 1.35, "optik güç", ring, TW_DS)
        p3 = plot(-2.95, 1.0, "optik frekans (çırpıntı)", chirp, GOLD)
        e2 = VMobject(color=GOOD, stroke_width=2.5).set_points_as_corners([[x0 + w * a, -0.85 + 1.35 * eml(a), 0] for a in t])
        e3 = VMobject(color=GOOD, stroke_width=2.5).set_points_as_corners([[x0 + w * a, -2.95 + 1.0 * flat(a), 0] for a in t])
        r = VGroup(T("gevşeme salınımı", 22, TW_DS, BOLD), T("→ gözde aşma", 20, TXT), T("frekans çırpıntısı", 22, GOLD, BOLD), T("→ fiberde dispersiyon cezası", 20, TXT),
                   T("EML (harici modülatör)", 22, GOOD, BOLD), T("→ iki etki de çok daha küçük", 20, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.8, -0.3, 0])
        r[2:4].shift(DOWN * 0.22)
        r[4:].shift(DOWN * 0.44)
        r.move_to([3.8, -0.3, 0])
        self.at(self.cue("Doğrudan modüle", 3))
        self.play(Create(p1), run_time=0.7)
        self.at(self.cue("gevşeme salınımlarına", 6))
        self.play(Create(p2), run_time=0.9)
        self.play(Create(p3), run_time=0.9)
        self.at(self.cue("Salınım gözde", 11))
        self.play(FadeIn(r[0:2]), run_time=0.5)
        self.at(self.cue("çırpıntı ise", 14))
        self.play(FadeIn(r[2:4]), run_time=0.5)
        self.at(self.cue("Harici modülatörlü", 18))
        self.play(Create(e2), Create(e3), FadeIn(r[4:]), run_time=0.9)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p4A")


class E4P4B(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[4], M4("p4"), "fiz"

    def construct(self):
        self.beat("e2")
        self.set_badge("std")
        h = self.show_heading("Referans alıcı (Şekil 11-4)")
        blocks = VGroup(box(2.3, 0.9, "optik verici", TW_DS, 18), box(2.5, 0.9, "zayıflatıcı\n(gerekirse)", MUTED, 16),
                        box(3.2, 0.9, "O/E + 4. derece\nThomson filtresi", GOLD, 16), box(2.6, 0.9, "dalga biçimi\nmonitörü", GOOD, 16)).arrange(RIGHT, buff=0.55).move_to(UP * 1.35)
        arr = VGroup(*[Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.05, color=FEED, stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        f = T("3 dB kesim frekansı = 0,75 × nominal hız", 32, GOLD, BOLD).move_to(DOWN * 0.15)
        f10 = T("10G: 0,75 × 9,95328 ≈ 7,5 GHz", 26, TXT, BOLD).move_to(DOWN * 0.95)
        wn = pill("değer metinde değil, şekilde — cihazda doğru filtreyi seçin", WARN, 20).move_to(DOWN * 2.2)
        self.play(FadeIn(blocks[0]), self.set_src("G.989.2 Şekil 11-4"), run_time=0.5)
        self.at(self.cue("optik elektrik", 2))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(arr[i]), FadeIn(blocks[i + 1])) for i in range(3)], lag_ratio=0.4), run_time=1.3)
        self.at(self.cue("Filtrenin üç", 7))
        self.play(FadeIn(f, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("on gigabitte yaklaşık", 12))
        self.play(FadeIn(f10), run_time=0.5)
        self.at(self.cue("Bu değer standardın", 15))
        self.play(FadeIn(wn, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e2b")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Neden Thomson filtresi?", h)
        x0, y0, w, hh = -6.0, -1.9, 5.4, 2.6
        ax1 = mini_axes(x0, y0, w, hh * 1.25, "zaman", "adım yanıtı", xbuff=0.12)
        tt = np.linspace(0, 9, 180)
        bb, ab = sig.bessel(4, 1, analog=True, norm="mag")
        bu, au = sig.butter(4, 1, analog=True)
        _, yb_ = sig.step((bb, ab), T=tt)
        _, yu_ = sig.step((bu, au), T=tt)
        cb = VMobject(color=GOOD, stroke_width=3.5).set_points_smoothly([[x0 + w * a / 9, y0 + hh * v, 0] for a, v in zip(tt, yb_)])
        cu = VMobject(color=WARN, stroke_width=2.5).set_points_smoothly([[x0 + w * a / 9, y0 + hh * v, 0] for a, v in zip(tt, yu_)])
        one = DashedLine([x0, y0 + hh, 0], [x0 + w, y0 + hh, 0], color=MUTED, stroke_width=1.2)
        l1 = VGroup(T("Thomson: aşma yok", 18, GOOD, BOLD), T("keskin kesimli filtre: aşma", 18, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([x0 + 3.95, y0 + 0.75, 0])
        gd = T("en düzgün grup gecikmesi", 18, GOOD).move_to([x0 + 2.7, y0 + hh * 1.25 + 0.42, 0])
        x1, w1 = 0.9, 5.6
        ax2 = mini_axes(x1, y0, w1, hh * 1.25, "frekans / bit hızı", "genlik", xbuff=0.42)
        fx = np.linspace(0.005, 2.0, 160)
        sinc = np.sinc(fx) ** 2
        nr = Polygon(*[[x1 + w1 * a / 2, y0 + hh * v, 0] for a, v in zip(fx, sinc)], [x1 + w1, y0, 0], [x1, y0, 0], stroke_width=0, fill_color=TW_DS, fill_opacity=0.25)
        wc = 1 / 0.75
        _, hm = sig.freqs(bb, ab, worN=fx * wc)
        cm = VMobject(color=GOLD, stroke_width=3).set_points_smoothly([[x1 + w1 * a / 2, y0 + hh * abs(v), 0] for a, v in zip(fx, hm)])
        m3 = VGroup(DashedLine([x1 + w1 * 0.375, y0, 0], [x1 + w1 * 0.375, y0 + hh * 1.1, 0], color=GOLD, stroke_width=2), T("0,75", 15, GOLD, BOLD).next_to([x1 + w1 * 0.375, y0, 0], DOWN, buff=0.08))
        tks = VGroup(*[T(s, 14, MUTED).next_to([x1 + w1 * a / 2, y0, 0], DOWN, buff=0.08) for a, s in ((0.0, "0"), (1.0, "1"), (2.0, "2"))])
        lg = VGroup(T("NRZ spektrumu", 16, TW_DS, BOLD), T("Thomson, −3 dB @ 0,75", 16, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([x1 + 4.0, y0 + hh * 1.05, 0])
        msg = T("sinyalin çoğu geçer, gürültü sınırlanır", 18, TXT, BOLD).move_to([x1 + w1 / 2, y0 - 0.95, 0])
        self.at(self.cue("Çünkü grup", 1))
        self.play(Create(ax1), Create(one), FadeIn(gd), run_time=0.6)
        self.play(Create(cu), Create(cb), FadeIn(l1), run_time=1.2)
        self.at(self.cue("Böylece ekranda", 8))
        self.play(Indicate(l1[0], color=GOOD, scale_factor=1.08), run_time=0.8)
        self.at(self.cue("Bant genişliği ise", 13))
        self.play(Create(ax2), FadeIn(tks), FadeIn(nr), run_time=0.6)
        self.play(Create(cm), FadeIn(m3), FadeIn(lg), run_time=0.8)
        self.at(self.cue("hızın dörtte", 18))
        self.play(FadeIn(msg), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e2a")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Maske marjı", h)
        o, W, H = np.array([-4.6, -1.5, 0]), 3.2, 2.3
        scr = eye_frame(o, W, H)
        eye = eye_traces(o, W, H, ov=0.1, op=0.45)
        mk = eye_mask(o, W, H, 0.4, 0.6)
        big = eye_mask(o, W, H, 0.3, 0.7, y1=0.17, y2=0.83, y3=0.16, y4=0.16)
        txt = VGroup(T("standart: maske marjı ya da", 20, MUTED), T("isabet oranı tanımlamaz", 20, MUTED), T("pratikte: göz maskeden", 21, TXT, BOLD),
                     T("ne kadar uzak?", 21, TXT, BOLD), T("üretimde marj = yaşlanma", 21, GOOD, BOLD), T("ve sıcaklık için güvenlik payı", 21, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        txt[2].shift(DOWN * 0.15); txt[3].shift(DOWN * 0.15); txt[4].shift(DOWN * 0.3); txt[5].shift(DOWN * 0.3)
        txt.move_to([3.9, 0.0, 0])
        mg = T("marj", 20, GOLD, BOLD).move_to(o + np.array([0.5 * W, 1.62 * H, 0]))
        self.play(FadeIn(scr), FadeIn(eye), FadeIn(mk), FadeIn(txt[0:2]), self.set_src("G.989.2 §11.1.5.3"), run_time=0.8)
        self.at(self.cue("Ama pratikte", 4))
        self.play(FadeIn(txt[2:4]), run_time=0.5)
        self.play(Transform(mk, big), FadeIn(mg), run_time=1.2)
        self.at(self.cue("üretim testlerinde", 8))
        self.play(FadeIn(txt[4:]), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep04_p4B")


class E4P4C(Act4):
    HDR, MANIFEST, PREV_BADGE = H4[4], M4("p4"), "std"

    def construct(self):
        self.beat("e3")
        h = self.show_heading("Titreşim üretimi — Tablo 11-10")
        cond = pill("zamanlama girişine titreşim uygulanmadan · tepeden tepeye", ACC, 19).move_to(UP * 2.0)
        X = lambda f: -4.4 + (np.log10(f) - 3) * 1.95
        yb = -2.15
        axis = Line([X(1e3) - 0.1, yb, 0], [X(2e8), yb, 0], color=MUTED, stroke_width=2)
        tk = VGroup(*[VGroup(Line([X(f), yb - 0.06, 0], [X(f), yb + 0.06, 0], color=MUTED, stroke_width=1.5), T(s, 14, MUTED).next_to([X(f), yb, 0], DOWN, buff=0.1))
                      for f, s in ((1e3, "1 kHz"), (1e4, "10 kHz"), (1e5, "100 kHz"), (1e6, "1 MHz"), (1e7, "10 MHz"), (1e8, "100 MHz"))])
        axt = T("frekans (log)", 15, MUTED).move_to([X(3e5), yb - 0.75, 0])

        def bar(a, b, y, c, lab, ui):
            r = Rectangle(width=X(b) - X(a), height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([(X(a) + X(b)) / 2, y, 0])
            return VGroup(r, T(lab, 15, BG, BOLD).move_to(r), T(ui, 19, c, BOLD).next_to(r, RIGHT, buff=0.15))
        b10 = VGroup(bar(2e4, 8e7, 1.1, TW_DS, "20 kHz – 80 MHz", "≤ 0,30 UI"), bar(4e6, 8e7, 0.55, TW_DS, "4 – 80 MHz", "≤ 0,10 UI"))
        b25 = VGroup(bar(5e3, 2e7, -0.5, GOLD, "5 kHz – 20 MHz", "≤ 0,30 UI"), bar(1e6, 2e7, -1.05, GOLD, "1 – 20 MHz", "≤ 0,10 UI"))
        g10 = T("10G", 22, TW_DS, BOLD).move_to([-5.9, 0.83, 0])
        g25 = T("2,5G", 22, GOLD, BOLD).move_to([-5.9, -0.78, 0])
        self.play(FadeIn(cond, shift=DOWN * 0.1), self.set_src("G.989.2 §11.1.5.4.3 · Tablo 11-10"), run_time=0.6)
        self.play(Create(axis), FadeIn(tk), FadeIn(axt), run_time=0.6)
        self.at(self.cue("On gigabitte yirmi", 8))
        self.play(FadeIn(g10), GrowFromEdge(b10[0][0], LEFT), FadeIn(b10[0][1:]), run_time=0.7)
        self.at(self.cue("dört megahertz ile", 13))
        self.play(GrowFromEdge(b10[1][0], LEFT), FadeIn(b10[1][1:]), run_time=0.6)
        self.at(self.cue("İki buçuk gigabitte", 19))
        self.play(FadeIn(g25), GrowFromEdge(b25[0][0], LEFT), FadeIn(b25[0][1:]), run_time=0.7)
        self.at(self.cue("ve bir megahertz", 24))
        self.play(GrowFromEdge(b25[1][0], LEFT), FadeIn(b25[1][1:]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e3a")
        self.clear(h)
        h = self.show_heading("Kökenler ve birim aralık", h)
        ps = VGroup(pill("sınırlar ← G.783 (SDH ekipmanı)", GOLD, 20), pill("filtreler · ölçüm süresi ← G.825", MUTED, 20)).arrange(RIGHT, buff=0.4).move_to(UP * 1.75)
        o, U, H = np.array([-2.3, -1.85, 0]), 4.6, 1.6
        scr = eye_frame(o, U, H, -0.28, 1.28, 1.3, -0.3)
        tr_ = eye_traces(o, U, H, ov=0.05, u0=-0.28, u1=1.28, jit=0.05, sw=1.8, op=0.45, seed=11)
        jb = VGroup(*[Rectangle(width=0.3 * U, height=1.6 * H, stroke_width=0, fill_color=GOLD, fill_opacity=0.16).move_to(o + np.array([u * U, 0.5 * H, 0])) for u in (0, 1)])
        ui = VGroup(DoubleArrow(o + np.array([0, -0.45 * H, 0]), o + np.array([U, -0.45 * H, 0]), buff=0, color=TXT, stroke_width=2.5, tip_length=0.14),
                    T("1 UI @ 10G ≈ 100 ps", 21, TXT, BOLD).move_to(o + np.array([0.5 * U, -0.68 * H, 0])))
        jt = VGroup(DoubleArrow(o + np.array([0.85 * U, 1.42 * H, 0]), o + np.array([1.15 * U, 1.42 * H, 0]), buff=0, color=GOLD, stroke_width=2.5, tip_length=0.1),
                    T("0,3 UI ≈ 30 ps tepeden tepeye", 21, GOLD, BOLD).move_to(o + np.array([0.62 * U, 1.66 * H, 0])))
        self.play(FadeIn(ps[0], shift=UP * 0.1), self.set_src("G.989.2 Tablo 11-10 (Not 1–3)"), run_time=0.5)
        self.at(self.cue("filtreler ve ölçüm", 4))
        self.play(FadeIn(ps[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Birim aralık cinsinden", 7))
        self.play(FadeIn(scr), FadeIn(tr_), run_time=0.8)
        self.at(self.cue("on gigabitte bir birim", 9))
        self.play(FadeIn(ui), run_time=0.5)
        self.at(self.cue("sıfır virgül üç", 13))
        self.play(FadeIn(jb), FadeIn(jt), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e3b")
        self.clear(h)
        h = self.show_heading("Titreşim toleransı", h)
        c1 = card("ONU alıcısı", "titreşim toleransı\n→ Bölüm 5", None, TW_DS, w=5.4, h=1.7, tsize=26, bsize=20).move_to([-3.1, 1.0, 0])
        c2 = card("OLT", "tolerans yalnızca\nbilgilendirme amaçlı", None, MUTED, w=5.4, h=1.7, tsize=26, bsize=20).move_to([3.1, 1.0, 0])
        yb = -1.7
        base = Line([-6.0, yb, 0], [6.0, yb, 0], color=MUTED, stroke_width=1.5)
        bursts = VGroup(*[Rectangle(width=w_, height=0.5, stroke_width=0, fill_color=TW_US, fill_opacity=0.85).move_to([x, yb + 0.25, 0]) for x, w_ in ((-4.8, 1.4), (-2.3, 1.9), (0.4, 1.0), (2.3, 1.6), (4.8, 1.2))])
        bt = T("↑ burst'ler: sürekli sinyal yok → bu ölçüm doğrudan yapılamaz", 19, TW_US, BOLD).next_to(base, DOWN, buff=0.25)
        self.play(FadeIn(c1, shift=UP * 0.15), self.set_src("G.989.2 §11.1.5.4.2"), run_time=0.6)
        self.at(self.cue("OLT tarafında", 5))
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("çünkü yukarı yön", 9))
        self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bursts], lag_ratio=0.15), run_time=0.9)
        self.play(FadeIn(bt), run_time=0.5)
        self.end(pad=0.05)

        self.note2("e4", ("Referans filtreyi doğru seçin", "Yanlış filtre gözü olduğundan açık ya da kapalı gösterir."),
                   ("Titreşimi gerçek koşulda ölçün", "OLT'nin gerçek saat kaynağıyla ve en kötü trafik deseninde."))
        self.bridge_beat("e5", "Bu bitler hangi yapının içinde gidiyor?")
        self.save_timeline("ep04_p4C")
