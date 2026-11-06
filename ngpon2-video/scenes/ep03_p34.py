"""B03 · Perde 3 (ızgaralar) and Perde 4 (Raman)."""
from ep03_common import *

DS_THZ = [187.8, 187.7, 187.6, 187.5, 187.4, 187.3, 187.2, 187.1]


def tr(x, fmt):
    return fmt.format(x).replace(".", ",")


def mini_axes(x0, y0, w, h, xl, yl, color=MUTED):
    o = np.array([x0, y0, 0])
    return VGroup(Line(o, o + [w, 0, 0], color=color, stroke_width=2), Line(o, o + [0, h, 0], color=color, stroke_width=2),
                  T(xl, 15, color).next_to(o + [w / 2, 0, 0], DOWN, buff=0.42), T(yl, 15, color).next_to(o + [0, h, 0], UP, buff=0.08))


class E3P3A(Act3):
    HDR, MANIFEST, FIRST = H3[3], M3("p3"), True

    def construct(self):
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Izgaralar")
        self.at(self.cue("Aşağı yön ızgarası", 2))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Aşağı yön ızgarası — Tablo 11-2")
        rows = [[str(i + 1), tr(f, "{:.1f}"), tr(thz_to_nm(f), "{:.2f}"), f"{i:04b}"] for i, f in enumerate(DS_THZ)]
        tb = table(["Kanal", "f (THz) · normatif", "λ (nm) · bilgi", "DWLCH ID"], rows, [1.3, 2.9, 2.6, 1.9], size=19, hsize=16, row_h=0.44).move_to([-2.2, -0.35, 0])
        for r in tb[1:]:
            r[4].set_opacity(0)
        tb[0][4].set_opacity(0)
        self.play(FadeIn(tb[0]), self.set_src("G.989.2 Tablo 11-2 · G.989.3 Tablo 6-3"), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[1:]], lag_ratio=0.12), run_time=1.6)
        self.end(pad=0.05)

        self.beat("d1a")
        b1 = BraceBetweenPoints(tb[1].get_corner(UR) + RIGHT * 0.1, tb[4].get_corner(DR) + RIGHT * 0.1, RIGHT, color=GOOD)
        b2 = BraceBetweenPoints(tb[5].get_corner(UR) + RIGHT * 0.1, tb[8].get_corner(DR) + RIGHT * 0.1, RIGHT, color=MUTED)
        t1 = T("TWDM · 4 kanal", 18, GOOD, BOLD).next_to(b1, RIGHT, buff=0.15)
        t2 = VGroup(T("isteğe bağlı", 18, MUTED, BOLD), T("PtP WDM / diğer", 16, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(b2, RIGHT, buff=0.15)
        mse = pill("↓ MSE ± 20 GHz", GOLD, 20).move_to([4.6, 1.9, 0])
        self.play(FadeIn(b1), FadeIn(t1), run_time=0.5)
        self.at(self.cue("Beşten sekize", 2))
        self.play(FadeIn(b2), FadeIn(t2), *[VGroup(*r[:4]).animate.set_opacity(0.55) for r in tb[5:]], run_time=0.6)
        self.at(self.cue("en büyük spektral", 5))
        self.play(FadeIn(mse, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d2")
        self.set_badge("tc")
        self.play(*[FadeOut(m) for m in (b1, b2, t1, t2, mse)], *[VGroup(*r[:4]).animate.set_opacity(1) for r in tb[5:]], run_time=0.4)
        self.play(tb[0][4].animate.set_opacity(1), *[r[4].animate.set_opacity(1) for r in tb[1:]], run_time=0.7)
        W = 3.8
        pid = VGroup(Rectangle(width=W * 28 / 32, height=0.55, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                     Rectangle(width=W * 4 / 32, height=0.55, stroke_color=ACC, stroke_width=2, fill_color=ACC, fill_opacity=0.35)).arrange(RIGHT, buff=0).move_to([4.75, 0.9, 0])
        pl = VGroup(T("PON-ID · 32 bit", 19, TXT, BOLD).next_to(pid, UP, buff=0.12),
                    T("28 bit yönetim etiketi", 15, MUTED).move_to(pid[0]), T("DWLCH", 12, ACC, BOLD).next_to(pid[1], DOWN, buff=0.08))
        oc = T("PSBd · OC → her ↓ çerçevede", 17, GOLD, BOLD).next_to(pid, DOWN, buff=0.55)
        self.at(self.cue("Otuz iki bitlik", 3))
        self.play(FadeIn(pid), FadeIn(pl), run_time=0.7)
        self.at(self.cue("PON kimliği her", 5))
        self.play(FadeIn(oc), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d2a")
        self.set_badge("std")
        n2 = VGroup(T("Tablo 11-4, Not 2", 18, GOLD, BOLD), T("birleşik mux/demux için\n100 GHz'ten küçük sapmalar", 16, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        o11 = VGroup(T("Channel_Profile · oktet 11", 18, "#A78BFA", BOLD), T("↓ frekans kayması · işaretli\n0,1 GHz birimi", 16, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        VGroup(n2, o11).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.75, -1.3, 0])
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Kanal profili de", 2))
        self.play(FadeIn(o11, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p3A")


class E3P3B(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[3], M3("p3"), "std"

    def construct(self):
        self.beat("d3")
        h = self.show_heading("Yukarı yön: kanal aralığı ve sapma (Tablo 11-6/11-7)")
        x0, y0, sx, sy = -5.4, -2.0, 0.026, 0.12
        ax = mini_axes(x0, y0, 230 * sx, 30 * sy, "kanal aralığı (GHz)", "MSE (± GHz)")
        tk = VGroup(*[T(str(v), 14, MUTED).next_to([x0 + v * sx, y0, 0], DOWN, buff=0.08) for v in (50, 100, 150, 200)],
                    *[T(str(v), 14, MUTED).next_to([x0, y0 + v * sy, 0], LEFT, buff=0.08) for v in (10, 20, 30)])
        pts = [(50, 12.5), (100, 20), (200, 25)]
        dots = VGroup(*[Dot([x0 + a * sx, y0 + b * sy, 0], radius=0.07, color=GOLD) for a, b in pts])
        lbl = VGroup(*[T(f"±{tr(b, '{:g}')}", 16, GOLD, BOLD).next_to(d, UP, buff=0.1) for d, (a, b) in zip(dots, pts)])
        seg = VMobject(color=GOLD, stroke_width=2.5).set_points_as_corners([d.get_center() for d in dots])
        info = VGroup(T("CS: 50 … 200 GHz", 22, TW_US, BOLD), T("sabit frekans yok —", 19, TXT), T("ızgarayı sistem seçer", 19, TXT), T("ara değerler: üç noktadan (Not 1)", 17, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, 0.2, 0])
        self.play(FadeIn(info[0:3]), self.set_src("G.989.2 Tablo 11-6, 11-7"), run_time=0.6)
        self.at(self.cue("en büyük spektral", 2))
        self.play(Create(ax), FadeIn(tk), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), FadeIn(lbl), run_time=1.0)
        self.at(self.cue("Aradaki değerler", 5))
        self.play(Create(seg), FadeIn(info[3]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d3a")
        self.clear(h)
        c1 = card("Sapma: bir ayar döngüsü boyunca", "ayarlanma + kilitlenme süresi dahil", None, GOLD, w=6.0, h=1.5, tsize=22, bsize=19)
        c2 = card("Tx gücünün λ bağımlılığı", "2,5G ↑: ± 0,05 dB/GHz\n10G ↑: ± 0,02 dB/GHz", "Not 13: OLT geri bildirimiyle ayarlanan ONU'lar", TW_US, w=6.0, h=2.2, tsize=22, bsize=19)
        VGroup(c1, c2).arrange(DOWN, buff=0.35).move_to(DOWN * 0.3)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Ayrıca verici", 2))
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d4")
        self.clear(h)
        h = self.show_heading("Ayar penceresi — döngüsel olmayan ızgara", h)
        k, xs, y = 0.0125, -4.6, -0.3
        chans = VGroup()
        for i in range(4):
            x = xs + (40 + i * 100) * k
            chans.add(VGroup(Line([x, y - 0.7, 0], [x, y + 0.7, 0], color=CH[i], stroke_width=4),
                             DoubleArrow([x - 20 * k, y + 0.9, 0], [x + 20 * k, y + 0.9, 0], buff=0, color=GOLD, stroke_width=2, tip_length=0.08)))
        base = Line([xs - 0.3, y - 0.7, 0], [xs + 420 * k, y - 0.7, 0], color=MUTED, stroke_width=2)
        br = BraceBetweenPoints([xs + 20 * k, y - 0.85, 0], [xs + 360 * k, y - 0.85, 0], DOWN, color=ACC)
        f = VGroup(T("W = (N − 1) · CS + 2 · MSE", 28, ACC, BOLD), T("= 3 · 100 + 2 · 20 = 340 GHz", 26, TXT, BOLD)).arrange(DOWN, buff=0.15).next_to(br, DOWN, buff=0.25)
        self.play(Create(base), LaggedStart(*[FadeIn(c[0]) for c in chans], lag_ratio=0.2), run_time=0.9)
        self.play(*[GrowFromCenter(c[1]) for c in chans], run_time=0.5)
        self.at(self.cue("Döngüsel ızgara kullanılmıyorsa", 3))
        self.play(FadeIn(br), FadeIn(f[0]), run_time=0.6)
        self.at(self.cue("Dört kanal", 5))
        self.play(FadeIn(f[1]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d4a")
        self.play(FadeOut(br), FadeOut(f), run_time=0.4)
        h2 = self.heading("Ayar penceresi — döngüsel ızgara")
        self.play(FadeTransform(h, h2), run_time=0.4)
        h = h2
        rep = VGroup()
        for i in range(4):
            x = xs + (40 + (i + 4) * 100) * k
            rep.add(Line([x, y - 0.7, 0], [x, y + 0.7, 0], color=CH[i], stroke_width=4).set_opacity(0.4))
        base2 = Line([xs + 420 * k, y - 0.7, 0], [xs + 820 * k, y - 0.7, 0], color=MUTED, stroke_width=2)
        fsr = BraceBetweenPoints([xs + 40 * k, y + 1.1, 0], [xs + 440 * k, y + 1.1, 0], UP, color=MUTED)
        fsrt = T("tekrar aralığı (FSR)", 16, MUTED).next_to(fsr, UP, buff=0.05)
        br2 = BraceBetweenPoints([xs + 40 * k, y - 0.85, 0], [xs + 540 * k, y - 0.85, 0], DOWN, color=GOOD)
        f2 = VGroup(T("W = (N + 1) · CS", 28, GOOD, BOLD), T("= 5 · 100 = 500 GHz", 26, TXT, BOLD)).arrange(DOWN, buff=0.15).next_to(br2, DOWN, buff=0.25)
        self.play(Create(base2), FadeIn(rep), run_time=0.6)
        self.play(FadeIn(br2), FadeIn(f2), run_time=0.6)
        self.at(self.cue("Döngüsel çoklayıcıda", 3))
        self.play(FadeIn(fsr), FadeIn(fsrt), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d4b")
        self.clear(h)
        h = self.show_heading("En küçük ayar penceresi (Tablo 11-6, Not 2)", h)
        tb = table(["CS", "N", "döngüsel değil", "döngüsel"], [["100 GHz", "4", "340 GHz", "500 GHz"], ["100 GHz", "8", "740 GHz", "900 GHz"],
                                                               ["50 GHz", "4", "175 GHz", "250 GHz"], ["50 GHz", "8", "375 GHz", "450 GHz"]],
                   [2.4, 1.2, 3.0, 3.0], size=24, hsize=19, row_h=0.62).move_to(DOWN * 0.2)
        self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[1:3]], lag_ratio=0.3), run_time=0.9)
        self.at(self.cue("Elli gigahertz", 2))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[3:]], lag_ratio=0.3), run_time=0.8)
        self.end(pad=0.05)

        self.beat("d4c")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Lazer diliyle", h)
        r1 = VGroup(T("500 GHz", 30, GOOD, BOLD), T("≈ 3,9 nm @ 1536 nm", 24, TXT), T("DFB ≈ 0,1 nm/K → ≈ 40 K", 24, GOLD, BOLD)).arrange(RIGHT, buff=0.5)
        r2 = VGroup(T("900 GHz", 30, WARN, BOLD), T("≈ 7,1 nm", 24, TXT), T("ısıl ayar zorlanır →\nçok bölümlü / harici kavite", 22, WARN, BOLD, line_spacing=0.9)).arrange(RIGHT, buff=0.5)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(DOWN * 0.2)
        b7 = T("→ ayarlanabilir lazer: Bölüm 7", 19, ACC, BOLD).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(r1[0]), FadeIn(r1[1]), run_time=0.5)
        self.at(self.cue("Tipik bir DFB", 2))
        self.play(FadeIn(r1[2]), run_time=0.5)
        self.at(self.cue("Dokuz yüz", 5))
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(b7), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p3B")


class E3P3C(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[3], M3("p3"), "fiz"

    def construct(self):
        self.beat("d5")
        self.set_badge("std")
        h = self.show_heading("Ek VII → Ek VIII.4")
        q = self.quote("G.989.2 (2019) · Appendix VII — Cyclic AWG channel grid design examples", "“This appendix has been deprecated.”",
                       "Döngüsel AWG örnekleri kaldırıldı — fikir Ek VIII'deki ızgara örneklerinde", width=12.0).move_to(UP * 1.2)
        rows = [["1", "195,591", "1532,756"], ["2", "195,486", "1533,573"], ["3", "195,382", "1534,391"], ["…", "…", "…"], ["8", "194,861", "1538,495"]]
        tb = table(["Kanal", "f (THz)", "λ (nm)"], rows, [1.4, 2.4, 2.4], size=19, hsize=16, row_h=0.42).move_to([-3.0, -1.5, 0])
        cs = VGroup(T("ızgara dışı örnek (Tablo VIII.6)", 18, MUTED), T("CS = 104,2 GHz", 34, GOLD, BOLD)).arrange(DOWN, buff=0.15).move_to([3.3, -1.4, 0])
        self.play(FadeIn(q, shift=UP * 0.1), self.set_src("G.989.2 Ek VII, Ek VIII.4"), run_time=0.8)
        self.at(self.cue("Izgara dışı", 3))
        self.play(FadeIn(tb), FadeIn(cs[0]), run_time=0.6)
        self.play(Write(cs[1]), run_time=0.7)
        self.end(pad=0.05)

        self.beat("d5a")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Neden 104,2 GHz? AWG'de Δf ∝ f", h)
        awg = box(1.6, 2.8, "AWG", "#3B4A75", 20).move_to([-3.6, 0.2, 0])
        inp = Line([-6.2, 0.2, 0], awg.get_left(), color=FEED, stroke_width=4)
        ports = VGroup()
        for i in range(4):
            yy = 1.2 - i * 0.68
            ports.add(VGroup(Line([awg.get_right()[0], yy, 0], [-0.9, yy, 0], color=CH[i], stroke_width=3),
                             T(f"port {i + 1}: ↓ {tr(187.8 - 0.1 * i, '{:.1f}')} · ↑ {tr(195.591 - 0.1042 * i, '{:.3f}')} THz", 15, CH[i], BOLD).next_to([-0.9, yy, 0], RIGHT, buff=0.15)))
        eq = VGroup(T("Δλ / λ ≈ sabit  →  Δf ∝ f", 26, GOLD, BOLD), T("Δf↑ ≈ 100 GHz × 195,59 / 187,8 ≈ 104,15 GHz", 24, TXT, BOLD),
                    T("tek çift yönlü AWG: ↓ ve ↑ aynı portta", 20, GOOD, BOLD)).arrange(DOWN, buff=0.2).move_to(DOWN * 2.1)
        self.play(Create(inp), FadeIn(awg), LaggedStart(*[Create(p[0]) for p in ports], lag_ratio=0.15), run_time=0.9)
        self.play(FadeIn(eq[0]), run_time=0.5)
        self.at(self.cue("Aynı AWG", 3))
        self.play(LaggedStart(*[FadeIn(p[1]) for p in ports], lag_ratio=0.15), FadeIn(eq[1]), run_time=1.0)
        self.at(self.cue("Böylece", 4))
        self.play(FadeIn(eq[2]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d6")
        self.clear(h)
        h = self.show_heading("En büyük ayar hatası (MTE) — Ek VIII.1", h)
        f = T("MTE = MSE − (−15 dB tek yanlı spektral genişlik) ≈ MSE − veri hızı", 24, ACC, BOLD).move_to(UP * 1.6)
        k = 0.22
        def row(y, rate, mte, color):
            mse = Rectangle(width=20 * k, height=0.5, stroke_color=GOLD, stroke_width=2, fill_opacity=0).move_to([-3.0 + 10 * k, y, 0])
            m = Rectangle(width=mte * k, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.8).align_to(mse, LEFT).move_to([-3.0 + mte * k / 2, y, 0])
            w = Rectangle(width=(20 - mte) * k, height=0.5, stroke_width=0, fill_color=WARN, fill_opacity=0.5).next_to(m, RIGHT, buff=0)
            return VGroup(T(rate, 20, TXT, BOLD).next_to(mse, LEFT, buff=0.3), mse, m, w, T(f"MTE ≈ {tr(mte, '{:g}')} GHz", 20, color, BOLD).next_to(mse, RIGHT, buff=0.3))
        r1 = row(0.2, "2,5G · CS 100", 17.5, GOOD)
        r2 = row(-0.8, "10G · CS 100", 10, GOLD)
        leg = VGroup(T("■ MSE = 20 GHz", 16, GOLD), T("■ spektral yarı genişlik", 16, WARN)).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.9)
        self.play(FadeIn(f), self.set_src("G.989.2 Ek VIII.1"), run_time=0.7)
        self.at(self.cue("Yüz gigahertz aralıkta", 4))
        self.play(FadeIn(r1), FadeIn(leg), run_time=0.6)
        self.play(FadeIn(r2), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d6a")
        self.clear(h)
        h = self.show_heading("OLT alıcı filtresi: üç şart", h)
        o = np.array([-5.6, -2.1, 0])
        curve = VMobject(color=ACC, stroke_width=3.5).set_points_smoothly([o + [x, 3.0 * np.exp(-((x - 2.6) / 1.15) ** 4), 0] for x in np.linspace(0, 5.2, 60)])
        axl = Line(o, o + [5.4, 0, 0], color=MUTED, stroke_width=2)
        mt = VGroup(DashedLine(o + [2.6 - 0.9, 0, 0], o + [2.6 - 0.9, 3.1, 0], color=GOLD, stroke_width=2), DashedLine(o + [2.6 + 0.9, 0, 0], o + [2.6 + 0.9, 3.1, 0], color=GOLD, stroke_width=2),
                    T("± MTE", 16, GOLD, BOLD).move_to(o + [2.6, 3.35, 0]))
        dot = Dot(o + [2.6 + 1.3, 3.0 * np.exp(-((1.3) / 1.15) ** 4), 0], color=TW_US, radius=0.1)
        conds = VGroup(T("1  (1+X) dB bant genişliği < 2·MTE", 21, TXT), T("2  merkezden iki yana tekdüze azalma", 21, TXT), T("3  dalgalanma < OLT güç ölçüm çözünürlüğü", 21, TXT),
                       T("→ ONU λ, OLT Rx gücüne bakarak\n    her zaman merkeze kayar", 21, GOOD, BOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.0, -0.2, 0])
        self.play(Create(axl), Create(curve), FadeIn(mt), run_time=0.9)
        for i, key in enumerate(["Bir artı X", "Filtre eğrisi", "kalan dalgalanma"]):
            self.at(self.cue(key, 2 + 2 * i))
            self.play(FadeIn(conds[i], shift=LEFT * 0.1), run_time=0.45)
        self.at(self.cue("Amaç basit", 8))
        self.play(FadeIn(dot), FadeIn(conds[3]), run_time=0.5)
        self.play(MoveAlongPath(dot, VMobject().set_points_smoothly([o + [x, 3.0 * np.exp(-((x - 2.6) / 1.15) ** 4), 0] for x in np.linspace(3.9, 2.6, 20)])), run_time=1.6)
        self.end(pad=0.05)

        self.beat("d6b")
        self.clear(h)
        h = self.show_heading("Kanal dışı emisyon: iki düzey (Ek VIII.5)", h)
        vic = Rectangle(width=3.0, height=2.2, stroke_color=TW_US, stroke_width=2.5, fill_color=TW_US, fill_opacity=0.12).move_to([0, -0.3, 0])
        vt = T("kurban kanal bant genişliği", 17, TW_US, BOLD).next_to(vic, DOWN, buff=0.12)
        sig = Line([0, -1.4, 0], [0, 0.6, 0], color=TW_US, stroke_width=4)
        i1 = VGroup(Line([-3.4, -1.4, 0], [-3.4, -0.6, 0], color=WARN, stroke_width=4), T("OOC1 · dışarıda\nuyumsuz karışma", 17, WARN, BOLD, line_spacing=0.9).move_to([-3.4, 0.25, 0]))
        i2 = VGroup(Line([0.8, -1.4, 0], [0.8, -0.85, 0], color=GOLD, stroke_width=4), T("OOC2 · içeride\nuyumlu karışma — daha sıkı", 17, GOLD, BOLD, line_spacing=0.9).move_to([3.8, 0.25, 0]))
        ar = Arrow([2.6, 0.0, 0], [0.9, -0.8, 0], buff=0.05, color=GOLD, stroke_width=2.5)
        self.play(FadeIn(vic), Create(sig), FadeIn(vt), self.set_src("G.989.2 Ek VIII.5"), run_time=0.7)
        self.at(self.cue("Birinci düzey", 1))
        self.play(FadeIn(i1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("İkinci düzey", 3))
        self.play(FadeIn(i2, shift=UP * 0.1), GrowArrow(ar), run_time=0.6)
        self.end(pad=0.05)

        self.beat("d6c")
        self.clear(h)
        h = self.show_heading("2,5G ↑ kanal dışı PSD sınırları (Tablo 11-6)", h)
        tb = table(["Düzey", "CS", "Sınır (dBm / 15 GHz)"], [["OOC1", "50 GHz", "−36,7"], ["OOC1", "100 GHz", "−40,5"], ["OOC1", "200 GHz", "−44,4"], ["OOC2", "8 kanal", "−48,8"]],
                   [2.2, 2.4, 3.8], size=24, hsize=19, row_h=0.62).move_to(DOWN * 0.1)
        b7 = T("→ ayrıntılar: Bölüm 7 (ayarlanabilir lazer)", 19, ACC, BOLD).next_to(tb, DOWN, buff=0.4)
        self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[1:4]], lag_ratio=0.25), self.set_src("G.989.2 Tablo 11-6"), run_time=1.0)
        self.at(self.cue("İkinci düzey sınır", 3))
        self.play(FadeIn(tb[4], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Bu ayrıntıları", 4))
        self.play(FadeIn(b7), run_time=0.4)
        self.end(pad=0.05)

        self.engineer_note("d7", [("1", "Yukarı yön ızgarası bir sistem kararı", "Standart değil; operatör ve OLT üreticisi belirler.", 1),
                                  ("2", "Birlikte değerlendirin", "Ayar penceresi · sapma sınırı · çoklayıcı teknolojisi.", 2)])
        self.beat("d8")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Yan yana yürüyen ışıklar birbirini rahat bırakır mı?\nCevap: hayır. Raman.")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep03_p3C")


def raman_gain(x):
    """Representative silica Raman gain vs frequency offset (THz), peak ≈ 13.2 THz, normalised."""
    if x <= 13.2:
        return 0.97 * (x / 13.2) ** 1.15 + 0.03 * np.sin(np.pi * x / 13.2)
    return 0.72 * np.exp(-((x - 13.2) / 2.6) ** 2) + 0.28 * np.exp(-((x - 13.2) / 14.0) ** 2) * max(0.0, 1 - (x - 13.2) / 36.8)


class E3P4A(Act3):
    HDR, MANIFEST, FIRST = H3[4], M3("p4"), True

    def construct(self):
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Raman")
        self.at(self.cue("Uyarılmış", 2))
        self.to_header(tc)
        self.set_badge("fiz")
        h = self.show_heading("Uyarılmış Raman saçılması (SRS)")
        x0, y0, sx, sy = -5.6, -2.1, 0.2, 3.0
        ax = mini_axes(x0, y0, 52 * sx, 1.1 * sy, "frekans farkı (THz)", "Raman kazancı (bağıl)")
        tk = VGroup(*[T(str(v), 14, MUTED).next_to([x0 + v * sx, y0, 0], DOWN, buff=0.08) for v in (0, 10, 20, 30, 40, 50)])
        g = VMobject(color=WARN, stroke_width=3.5).set_points_smoothly([[x0 + x * sx, y0 + raman_gain(x) * sy, 0] for x in np.linspace(0, 50, 120)])
        tag = T("temsili · G.652 (Şekil VI.1)", 15, MUTED).move_to([x0 + 38 * sx, y0 + 2.6, 0])
        rng = VGroup(DoubleArrow([x0 + 1 * sx, y0 + 3.45, 0], [x0 + 40 * sx, y0 + 3.45, 0], buff=0, color=GOLD, stroke_width=2, tip_length=0.1),
                     T("etki: ≈ 1 … 40 THz", 17, GOLD, BOLD).move_to([x0 + 20.5 * sx, y0 + 3.7, 0]))
        self.play(Create(ax), FadeIn(tk), FadeIn(tag), self.set_src("G.989.2 Ek VI"), run_time=0.7)
        self.at(self.cue("Silika fiberde", 2))
        self.play(Create(g), run_time=1.4)
        self.at(self.cue("etkiler bir terahertz", 3))
        self.play(FadeIn(rng), run_time=0.5)
        self.end(pad=0.05)
        self.g, self.gax = VGroup(ax, tk, g, tag, rng), (x0, y0, sx, sy)

        self.beat("e1a")
        self.play(FadeOut(self.g), run_time=0.4)
        c1 = card("Modülasyon karışması", "bir sinyalin modülasyonu\ndiğerinin üzerine biner\nyalnızca AYNI yönde", None, WARN, w=5.4, h=2.3, tsize=24, bsize=19).move_to([-3.0, 0.0, 0])
        c2 = card("Güç tüketimi", "kısa λ pompa gibi davranır,\nuzun λ'yı güçlendirir\nAYNI ve KARŞI yönde", None, GOLD, w=5.4, h=2.3, tsize=24, bsize=19).move_to([3.0, 0.0, 0])
        a1 = VGroup(Arrow([-4.6, -1.6, 0], [-3.4, -1.6, 0], buff=0, color=WARN), Arrow([-2.6, -1.6, 0], [-1.4, -1.6, 0], buff=0, color=WARN))
        a2 = VGroup(Arrow([1.4, -1.6, 0], [2.6, -1.6, 0], buff=0, color=GOLD), Arrow([4.6, -1.6, 0], [3.4, -1.6, 0], buff=0, color=GOLD))
        self.at(self.cue("Birincisi", 1))
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(a1), run_time=0.6)
        self.at(self.cue("İkincisi", 4))
        self.play(FadeIn(c2, shift=UP * 0.15), FadeIn(a2), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e1b")
        self.play(*[FadeOut(m) for m in (c1, c2, a1, a2)], FadeIn(VGroup(*self.g[:4])), run_time=0.5)
        x0, y0, sx, sy = self.gax
        pk = VGroup(DashedLine([x0 + 13.2 * sx, y0, 0], [x0 + 13.2 * sx, y0 + 3.05, 0], color=WARN, stroke_width=2),
                    T("tepe ≈ 13 THz ≈ 100 nm @ 1550 nm", 18, WARN, BOLD).move_to([x0 + 24 * sx, y0 + 3.15, 0]))
        reg = Rectangle(width=5 * sx, height=3.2, stroke_width=0, fill_color=ACC, fill_opacity=0.18).move_to([x0 + 7.5 * sx, y0 + 1.6, 0])
        rt = T("NG-PON2\n5–10 THz", 15, ACC, BOLD, line_spacing=0.85).move_to([x0 + 7.5 * sx, y0 + 0.55, 0])
        self.play(Create(pk[0]), FadeIn(pk[1]), run_time=0.6)
        self.at(self.cue("NG-PON2'nin kendi", 2))
        self.play(FadeIn(reg), FadeIn(rt), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e2")
        self.clear(h)
        h = self.show_heading("Kurban: RF video", h)
        axg, X = nm_axis(1540, 1610, y=-1.8, step=5, label_every=10)
        v = band(X, 1550, 1560, -1.25, 0.8, VIDEO, "RF video", lsize=16)
        d = band(X, 1596, 1603, -1.25, 0.8, TW_DS, "TWDM ↓", lsize=15)
        arr = VGroup(Arrow([X(1550), 0.0, 0], [X(1562), 0.0, 0], buff=0, color=VIDEO), Arrow([X(1596), 0.0, 0], [X(1608), 0.0, 0], buff=0, color=TW_DS),
                     T("aynı yön →", 18, TXT, BOLD).move_to([X(1579), 0.0, 0]))
        df = VGroup(DoubleArrow([X(1555), -0.55, 0], [X(1599.5), -0.55, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12), T("≈ 5–6 THz", 18, GOLD, BOLD).move_to([X(1577), -0.3, 0]))
        noise = T("TWDM modülasyonu → video taşıyıcısında gürültü", 21, WARN, BOLD).move_to(UP * 1.3)
        self.play(Create(axg[0]), FadeIn(axg[1:]), GrowFromEdge(v, DOWN), GrowFromEdge(d, DOWN), run_time=0.8)
        self.at(self.cue("aynı yönde", 2))
        self.play(FadeIn(arr), run_time=0.5)
        self.at(self.cue("Aralarındaki fark", 3))
        self.play(FadeIn(df), run_time=0.5)
        self.at(self.cue("TWDM sinyallerinin", 5))
        self.play(FadeIn(noise, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e2a")
        self.clear(h)
        h = self.show_heading("Etki RF spektrumunun alt ucunda", h)
        x0, y0 = -5.6, -2.0
        k = 10.4 / 860
        ax = mini_axes(x0, y0, 10.6, 3.2, "RF frekansı (MHz)", "")
        tk = VGroup(*[T(str(v), 14, MUTED).next_to([x0 + v * k, y0, 0], DOWN, buff=0.08) for v in (50, 300, 550, 860)])
        chans = VGroup(*[Rectangle(width=0.06, height=2.4, stroke_width=0, fill_color=VIDEO, fill_opacity=0.5).move_to([x0 + f * k, y0 + 1.2, 0]) for f in range(55, 860, 24)])
        xt = VMobject(color=WARN, stroke_width=3.5).set_points_smoothly([[x0 + f * k, y0 + 0.15 + 2.2 / (1 + (f / 140) ** 1.6), 0] for f in np.linspace(50, 860, 60)])
        xtl = T("Raman karışma gürültüsü (temsili)", 17, WARN, BOLD).move_to([x0 + 560 * k, y0 + 2.9, 0])
        hl = Rectangle(width=250 * k, height=3.0, stroke_width=0, fill_color=WARN, fill_opacity=0.12).move_to([x0 + 175 * k, y0 + 1.5, 0])
        hlt = T("≤ 300 MHz (10–20 km)", 17, WARN, BOLD).next_to(hl, UP, buff=0.05)
        wo = T("farklı grup hızları (walk-off) → yüksek frekanslar ortalanır", 18, MUTED).move_to(UP * 1.75)
        self.play(Create(ax), FadeIn(tk), FadeIn(chans), run_time=0.8)
        self.play(Create(xt), FadeIn(xtl), run_time=0.8)
        self.at(self.cue("Çünkü farklı", 1))
        self.play(FadeIn(wo), run_time=0.5)
        self.at(self.cue("Standarda göre", 4))
        self.play(FadeIn(hl), FadeIn(hlt), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p4A")


class E3P4B(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[4], M3("p4"), "fiz"

    def construct(self):
        self.beat("e3")
        h = self.show_heading("Yukarı yön kanalları: güç tüketimi")
        olt = box(1.3, 1.6, "OLT", "#94A3B8", 20).move_to([-5.6, 0.0, 0])
        fib = Line([-4.95, 0.0, 0], [5.8, 0.0, 0], color=FEED, stroke_width=4)
        ds = VGroup(*[Arrow([-4.6 + 2.2 * i, 0.45, 0], [-3.2 + 2.2 * i, 0.45, 0], buff=0, color=TW_DS, stroke_width=7 - 1.2 * i, max_tip_length_to_length_ratio=0.2) for i in range(5)])
        us = VGroup(*[Arrow([-3.2 + 2.2 * i, -0.45, 0], [-4.6 + 2.2 * i, -0.45, 0], buff=0, color=TW_US, stroke_width=2.0, max_tip_length_to_length_ratio=0.2) for i in range(5)])
        lds = T("↓ L bandı · güçlü", 18, TW_DS, BOLD).next_to(ds, UP, buff=0.15)
        lus = T("↑ C bandı · zayıf (ODN'den geçti)", 18, TW_US, BOLD).next_to(us, DOWN, buff=0.15)
        en = VGroup(*[CurvedArrow([-3.9 + 2.2 * i, -0.3, 0], [-3.9 + 2.2 * i, 0.3, 0], angle=-1.2, color=GOLD, stroke_width=2.5) for i in range(3)])
        ent = T("enerji: kısa λ (↑) → uzun λ (↓)", 20, GOLD, BOLD).move_to(DOWN * 2.0)
        self.play(FadeIn(olt), Create(fib), run_time=0.6)
        self.at(self.cue("TWDM yukarı yön kanalları", 1))
        self.play(LaggedStart(*[GrowArrow(a) for a in ds], lag_ratio=0.1), FadeIn(lds), run_time=0.8)
        self.at(self.cue("OLT'nin yakınında", 2))
        self.play(LaggedStart(*[GrowArrow(a) for a in us], lag_ratio=0.1), FadeIn(lus), run_time=0.8)
        self.at(self.cue("Yukarı yön sinyali", 4))
        self.play(LaggedStart(*[Create(e) for e in en], lag_ratio=0.2), FadeIn(ent), run_time=0.9)
        self.end(pad=0.05)

        self.beat("e3a")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Raman, yukarı yön yol cezasının içinde", h)
        n10 = self.quote("G.989.2 Tablo 11-6, Not 10", "“…assume no S/R-CG located splitters and low optical fibre loss, resulting in the worst case Raman effect.”",
                         "Ceza: sınıfa özgü verici gücü · mesafe · dalga boyu sayısı", width=12.0).move_to(UP * 1.1)
        opp = table(["maks. OPP (dB) · 2,5G ↑", "N1", "N2", "E1", "E2"], [["DD20 · 4 kanal", "1,0", "1,0", "1,5", "1,5"], ["DD40 · 8 kanal", "1,7", "2,1", "2,8", "2,8"]],
                    [4.0, 1.5, 1.5, 1.5, 1.5], size=21, hsize=17, row_h=0.55).move_to(DOWN * 1.6)
        hl = SurroundingRectangle(opp[2][5], color=WARN, buff=0.04)
        self.play(FadeIn(n10, shift=UP * 0.1), self.set_src("G.989.2 Tablo 11-6"), run_time=0.8)
        self.at(self.cue("En kötü durum", 3))
        self.play(FadeIn(opp), run_time=0.6)
        self.at(self.cue("Sekiz kanal", 5))
        self.play(Create(hl), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e3b")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Birlikte çalışma tabloyu karmaşıklaştırır", h)
        axg, X = nm_axis(1470, 1610, y=-1.9, step=10, label_every=20)
        us = band(X, 1524, 1544, -1.35, 0.7, TW_US, "TWDM ↑", lsize=15)
        gp = band(X, 1480, 1500, -1.35, 0.7, LEGACY, "G-PON ↓", lsize=14, lcolor=TXT)
        vd = band(X, 1550, 1560, -1.35, 0.7, VIDEO, "video", lsize=14)
        xg = band(X, 1575, 1580, -1.35, 0.7, LEGACY, None)
        xgt = T("XG ↓", 14, MUTED, BOLD).next_to(xg, UP, buff=0.08)
        a1 = CurvedArrow([X(1490), -0.85, 0], [X(1530), -0.85, 0], angle=-1.0, color=GOOD, stroke_width=3)
        t1 = T("pompalar: ↑ kazanır", 17, GOOD, BOLD).next_to(a1, UP, buff=0.08)
        a2 = CurvedArrow([X(1538), -0.85, 0], [X(1577), -0.85, 0], angle=-1.0, color=WARN, stroke_width=3)
        t2 = T("↑ güç kaybeder", 17, WARN, BOLD).next_to(a2, UP, buff=0.08)
        net = T("net etki: ağda hangi sistemler var?", 22, GOLD, BOLD).move_to(UP * 1.6)
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(us), run_time=0.6)
        self.at(self.cue("G-PON aşağı", 1))
        self.play(FadeIn(gp), Create(a1), FadeIn(t1), run_time=0.8)
        self.at(self.cue("XG-PON1 aşağı", 3))
        self.play(FadeIn(vd), FadeIn(xg), FadeIn(xgt), Create(a2), FadeIn(t2), run_time=0.8)
        self.at(self.cue("Net etki", 5))
        self.play(FadeIn(net), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e4")
        self.clear(h)
        h = self.show_heading("Azaltma yöntemleri — Ek VI", h)
        names = [("HighPassRF", "alçak RF frekanslarını\nbastır (< 200 MHz @10G)", WARN), ("DoP0", "sıfır birleşik\npolarizasyon derecesi", GOLD),
                 ("DedicatedTx", "özel bastırma\nvericisi", ACC), ("PSD-S", "DSP ile spektrum\nşekillendirme", TW_US)]
        cards = VGroup(*[card(n, b, None, c, w=3.05, h=1.9, tsize=21, bsize=16) for n, b, c in names]).arrange(RIGHT, buff=0.22).move_to(UP * 0.7)
        res = T("HighPassRF → Raman karışmasında ≤ 12 dB azalma", 22, WARN, BOLD).move_to(DOWN * 1.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.15), self.set_src("G.989.2 Ek VI"), run_time=1.0)
        self.play(*[c.animate.set_opacity(0.3) for c in cards[1:]], run_time=0.4)
        self.at(self.cue("Bu, Raman", 4))
        self.play(FadeIn(res), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e4a")
        self.play(cards[0].animate.set_opacity(0.3), cards[1].animate.set_opacity(1), FadeOut(res), run_time=0.4)
        pol = VGroup(*[Arrow(ORIGIN, (UP if i % 4 in (1, 2) else RIGHT) * 0.55, buff=0, color=CH[i % 4], stroke_width=4).move_to([-5.0 + i * 0.7, -1.4, 0]) for i in range(6)])
        pt = T("kanal 1: 0° · 2–3: 90° · 4–5: 0° …", 16, MUTED).next_to(pol, DOWN, buff=0.2)
        r = VGroup(T("paralel (DoP = 1) yerine DoP = 0 → −6 dB karışma", 19, GOLD, BOLD), T("2 : 1 elektriksel/optik dB → +3 dB optik güç", 19, TXT),
                   T("PM fiber · polarizasyon kontrollü WM", 17, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -1.6, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in pol], lag_ratio=0.1), FadeIn(pt), run_time=0.9)
        self.at(self.cue("Hepsinin paralel", 2))
        self.play(FadeIn(r[0]), run_time=0.5)
        self.at(self.cue("Elektriksel", 3))
        self.play(FadeIn(r[1]), run_time=0.5)
        self.at(self.cue("Bunun için", 5))
        self.play(FadeIn(r[2]), run_time=0.4)
        self.end(pad=0.05)

        self.beat("e4b")
        self.play(*[FadeOut(m) for m in (pol, pt, r)], cards[1].animate.set_opacity(0.3), cards[2].animate.set_opacity(1), run_time=0.4)
        d1 = T("DedicatedTx: yıkıcı girişimle iptal → CCR +12 … 14 dB", 21, ACC, BOLD).move_to(DOWN * 1.2)
        d2 = T("PSD-S: veri spektrumu video bölgesinden uzaklaştırılır", 21, TW_US, BOLD).move_to(DOWN * 1.9)
        self.play(FadeIn(d1), run_time=0.5)
        self.at(self.cue("Dördüncüsü", 3))
        self.play(cards[3].animate.set_opacity(1), FadeIn(d2), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p4B")


def miller_psd(fT):
    w = 2 * np.pi * fT
    num = 23 - 2 * np.cos(w / 2) - 22 * np.cos(w) - 12 * np.cos(1.5 * w) + 5 * np.cos(2 * w) + 12 * np.cos(2.5 * w) + 2 * np.cos(3 * w) - 8 * np.cos(3.5 * w) + 2 * np.cos(4 * w)
    return 2 / (w ** 2 * (17 + 8 * np.cos(4 * w))) * num


class E3P4C(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[4], M3("p4"), "fiz"

    def construct(self):
        self.beat("e5")
        self.set_badge("std")
        h = self.show_heading("Ek IX — Raman için hat kodları")
        x0, y0, sx, sy = -5.6, -2.1, 3.0, 2.6
        ax = mini_axes(x0, y0, 2.05 * sx, 1.15 * sy, "f · T (bit hızına göre)", "PSD (tepeye göre)")
        tk = VGroup(*[T(tr(v, "{:g}"), 14, MUTED).next_to([x0 + v * sx, y0, 0], DOWN, buff=0.08) for v in (0, 0.5, 1, 1.5, 2)])
        fs = np.linspace(0.005, 2.0, 160)
        nrz = np.sinc(fs) ** 2
        mil = np.array([miller_psd(f) for f in fs]); mil = mil / mil.max()
        cn = VMobject(color=MUTED, stroke_width=3).set_points_smoothly([[x0 + f * sx, y0 + v * sy, 0] for f, v in zip(fs, nrz)])
        cm = VMobject(color=GOLD, stroke_width=3.5).set_points_smoothly([[x0 + f * sx, y0 + v * sy, 0] for f, v in zip(fs, mil)])
        lg = VGroup(T("NRZ", 18, MUTED, BOLD), T("Miller", 18, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([x0 + 1.75 * sx, y0 + 2.6, 0])
        lf = VGroup(T("Miller: alçak frekansta az enerji", 16, GOLD, BOLD).move_to([x0 + 1.25 * sx, y0 + 1.35, 0]))
        lf.add(Arrow(lf[0].get_bottom() + LEFT * 0.9, [x0 + 0.12 * sx, y0 + 0.3, 0], buff=0.05, color=GOLD, stroke_width=2.5, max_tip_length_to_length_ratio=0.12))
        b8 = card("8B10B", "DC dengeli kod\nMAC alt katmanı · aç / kapa", None, ACC, w=4.6, h=1.7, tsize=24, bsize=18).move_to([3.9, 0.9, 0])
        self.play(Create(ax), FadeIn(tk), self.set_src("G.989.2 Ek IX"), run_time=0.6)
        self.at(self.cue("8B10B kodu", 1))
        self.play(FadeIn(b8, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Miller kodu", 3))
        self.play(Create(cn), Create(cm), FadeIn(lg), run_time=1.2)
        self.play(FadeIn(lf), run_time=0.4)
        self.end(pad=0.05)

        self.beat("e5b")
        r1 = VGroup(Rectangle(width=4.0, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=0.85), T("10 Gbit/s veri", 17, BG, BOLD))
        r1[1].move_to(r1[0])
        r2 = VGroup(Rectangle(width=5.0, height=0.5, stroke_width=0, fill_color=WARN, fill_opacity=0.85), T("12,5 Gbit/s hat (× 10/8)", 17, BG, BOLD))
        r2[1].move_to(r2[0])
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, -1.2, 0])
        ov = T("ek yük %25 · hassasiyete etkisi var", 18, WARN, BOLD).next_to(VGroup(r1, r2), DOWN, buff=0.18)
        self.play(GrowFromEdge(r1, LEFT), run_time=0.5)
        self.play(GrowFromEdge(r2, LEFT), run_time=0.6)
        self.at(self.cue("on gigabit uyumlu", 2))
        self.play(FadeIn(ov), run_time=0.5)
        self.end(pad=0.05)

        self.beat("e5a")
        self.clear(h)
        h = self.show_heading("Miller: yan fayda ve bedel", h)
        c1 = card("Yan fayda", "dar spektrum → daha az dispersiyon cezası\n10G ↓ (L bandı) / ↑ (C bandı): EML yerine DML", None, GOOD, w=11.0, h=1.8, tsize=24, bsize=20).move_to(UP * 0.6)
        c2 = card("Bedel", "180° faz belirsizliği → bitler ters çözülür\nkod ihlalleri ile yakalanır", None, WARN, w=11.0, h=1.8, tsize=24, bsize=20).move_to(DOWN * 1.5)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Bedeli ise", 3))
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.05)

        self.beat("e6")
        self.clear(h)
        self.set_badge("tc")
        h = self.show_heading("TC köprüsü: Channel_Profile oktet 12", h)
        bits = ["0", "0", "S", "E", "L", "L", "L", "L"]
        cols = [MUTED, MUTED, TW_DS, GOLD, ACC, ACC, ACC, ACC]
        cells = VGroup(*[VGroup(Square(0.9, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), T(b, 30, c, BOLD)) for b, c in zip(bits, cols)])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0.08).move_to(UP * 0.8)
        leg = VGroup(T("S: hat hızı — 0 = 9,95328 · 1 = 2,48832 Gbit/s", 20, TW_DS), T("E: aşağı yön FEC açık / kapalı", 20, GOLD),
                     T("LLLL: hat kodu — 0000 = NRZ · diğerleri: ileride çalışılacak", 20, ACC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.08), self.set_src("G.989.3 Tablo 11-18"), run_time=0.9)
        self.play(FadeIn(leg[0:2]), run_time=0.5)
        self.at(self.cue("Bugün yalnızca", 2))
        self.play(FadeIn(leg[2]), Indicate(cells[4:], color=WHITE), run_time=0.8)
        self.end(pad=0.05)

        self.engineer_note("e7", [("1", "Devreye almadan önce ölçün", "Video alıcısında taşıyıcı gürültü oranını kaydedin.", 1),
                                  ("2", "Kanalları tek tek açın", "Alçak frekanslı TV kanallarındaki değişimi izleyin.", 2)])
        self.beat("e8")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bütün bu harita ONU'ya nasıl anlatılır?\nKanal profilleri.")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep03_p4C")
