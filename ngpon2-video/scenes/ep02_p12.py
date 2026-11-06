"""B02 · Perde 1 (ODN'in anatomisi) and Perde 2 (yol kaybı sınıfları)."""
from kit import *

H1, H2 = "BÖLÜM 2 · PERDE 1 — ODN'in anatomisi", "BÖLÜM 2 · PERDE 2 — Yol kaybı sınıfları"
M1, M2 = "build/ep02/p1/audio_proc/manifest.json", "build/ep02/p2/audio_proc/manifest.json"
CLS = [("N1", 14, CH[0]), ("N2", 16, CH[1]), ("E1", 18, CH[2]), ("E2", 20, CH[3])]


def three_segments(y=-0.3):
    cts = VGroup(*[box(1.2, 0.42, f"CT{i + 1}", CH[i], 15).move_to([-5.9, y + 1.0 - i * 0.66, 0]) for i in range(4)])
    wm = box(0.6, 2.8, "WM", "#3B4A75", 16).move_to([-3.6, y, 0])
    att = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=GOLD, stroke_width=3.5) for c in cts])
    sp = splitter(0.38).move_to([1.6, y, 0])
    feed = Line(wm.get_right(), sp.get_left(), color=ACC, stroke_width=6)
    onus = VGroup(*[box(1.3, 0.5, "ONU", "#94A3B8", 15).move_to([5.4, y + 1.35 - i * 0.9, 0]) for i in range(4)])
    dist = VGroup(*[Line(sp.get_right(), o.get_left(), color=PINK, stroke_width=3) for o in onus])
    co = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=4.0, height=3.6, color=MUTED).move_to([-4.6, y, 0]), num_dashes=60)
    co_t = T("merkez ofis", 15, MUTED).next_to(co, UP, buff=0.05)
    return dict(cts=cts, wm=wm, att=att, sp=sp, feed=feed, onus=onus, dist=dist, co=co, co_t=co_t,
                all=VGroup(co, co_t, cts, wm, att, feed, sp, dist, onus))


class E2P1A(Act):
    HDR, MANIFEST, FIRST = H1, M1, True

    def construct(self):
        self.beat("b1")
        tc = self.title_card("PERDE 1", "ODN'in anatomisi")
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 2.0)
        self.to_header(tc)
        h = self.show_heading("Ağacın parçaları")
        d = three_segments()
        self.play(FadeIn(d["all"]), run_time=1.0)
        self.end(pad=0.05)

        self.beat("b2")
        self.set_badge("tc")
        lab = VGroup(T("kanal bağlantı fiberi", 17, GOLD, BOLD).next_to(d["att"], DOWN, buff=1.35).shift(RIGHT * 0.3),
                     T("besleme fiberi · herkes paylaşır", 17, ACC, BOLD).next_to(d["feed"], UP, buff=0.12),
                     T("dağıtım fiberi", 17, PINK, BOLD).next_to(d["dist"], DOWN, buff=0.45))
        self.play(self.set_src("G.989.3 Ek VII — TWDM PON fiber mesafesi"), run_time=0.3)
        for k, (seg, t0) in enumerate([(d["att"], self.cues[2]), (d["feed"], self.cues[3]), (d["dist"], self.cues[5] if len(self.cues) > 5 else self.cues[-1])]):
            self.at(t0 - 0.2)
            self.play(Indicate(seg, color=WHITE, scale_factor=1.0), FadeIn(lab[k], shift=UP * 0.1), run_time=0.8)
        self.end(pad=0.05)

        self.beat("b2a")
        self.play(VGroup(d["all"], lab).animate.scale(0.62).to_edge(UP, buff=1.25), run_time=0.7)
        bx = -5.6
        def stacked(y, parts, title):
            g, x = VGroup(), bx
            for w, c, t in parts:
                r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x + w / 2, y, 0])
                g.add(VGroup(r, T(t, 15, BG, BOLD).move_to(r)))
                x += w
            return VGroup(T(title, 20, TXT, BOLD).next_to([bx, y, 0], LEFT, buff=0.25), g)
        dist_bar = stacked(-1.6, [(0.4, GOLD, ""), (8.0, ACC, "besleme"), (1.4, PINK, "dağıtım")], "mesafe")
        loss_bar = stacked(-2.6, [(0.3, GOLD, ""), (1.6, ACC, "fiber"), (6.4, CH[0], "ayırıcı"), (1.5, PINK, "")], "kayıp")
        for b in (dist_bar, loss_bar):
            b[0].shift(RIGHT * 1.3)
            b[1].shift(RIGHT * 1.3)
        tip = T("(tipik oranlar)", 15, MUTED).next_to(loss_bar, DOWN, buff=0.15).align_to(loss_bar[1], RIGHT)
        self.play(FadeIn(dist_bar[0]), LaggedStart(*[GrowFromEdge(p, LEFT) for p in dist_bar[1]], lag_ratio=0.2), run_time=1.0)
        self.at(self.cues[-2] if len(self.cues) > 2 else 6.0)
        self.play(FadeIn(loss_bar[0]), LaggedStart(*[GrowFromEdge(p, LEFT) for p in loss_bar[1]], lag_ratio=0.2), FadeIn(tip), run_time=1.0)
        self.end(pad=0.05)

        self.beat("b3")
        self.play(*[FadeOut(m) for m in (dist_bar, loss_bar, tip)], VGroup(d["all"], lab).animate.scale(1 / 0.62).move_to(DOWN * 0.3), run_time=0.7)
        coil = VGroup(*[Circle(radius=0.12 + 0.05 * k, color=GOLD, stroke_width=2) for k in range(3)]).move_to(d["att"][2].get_center())
        long_t = T("uzun kanal bağlantı fiberi (CT'ye göre farklı)", 17, GOLD, BOLD).move_to(lab[0]).align_to(lab[0], LEFT)
        self.at(self.cues[1] - 0.2)
        self.play(FadeIn(coil), FadeTransform(lab[0], long_t), run_time=0.7)
        onu = d["onus"][1]
        self.at(self.cues[2] - 0.2)
        self.play(onu[0].animate.set_stroke(CH[0]), run_time=0.4)
        self.play(onu[0].animate.set_stroke(CH[2]), Indicate(coil, color=WHITE), run_time=0.9)
        dl = pill("ONU kanal değiştirince OLT'ye olan mesafe de değişir → Perde 5", GOLD, 18).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.drop_badge()

        # b4 — Table 11-3, simple ODN
        self.beat("b4")
        self.set_badge("std")
        h = self.show_heading("Basit ODN — G.989.2 Tablo 11-3")
        rows = [["Fiber tipi", "G.652 ya da uyumlu"], ["Zayıflama aralığı", "Tablo 6-1 (N1 … E2)"], ["Maks. fiber mesafesi", "DD20: 20 km · DD40: 40 km"],
                ["Min. fiber mesafesi", "0 km"], ["Maks. diferansiyel yol kaybı", "15 dB"], ["Çift yönlü iletim", "tek fiber, WDM"], ["Bakım dalga boyu", "ITU-T L.313'e bakınız"]]
        tb = table(["Parametre", "Değer"], rows, [5.4, 5.6], size=21, hsize=18, row_h=0.56).move_to(DOWN * 0.45)
        self.play(FadeIn(tb[0]), self.set_src("G.989.2 §11.1.4.1, Tablo 11-3"), run_time=0.5)
        n = len(self.cues)
        for i in range(7):
            self.at(self.cues[min(n - 1, 1 + i)] - 0.1 if n > 1 else 0.5 + i)
            self.play(FadeIn(tb[i + 1], shift=UP * 0.08), run_time=0.4)
        self.end(pad=0.05)

        self.beat("b5")
        self.play(tb.animate.scale(0.7).to_edge(UP, buff=1.4), run_time=0.6)
        sc = 0.18
        x0 = -5.6
        ax = NumberLine(x_range=[0, 60, 10], length=60 * sc, include_numbers=False, color=MUTED).move_to([x0 + 30 * sc, -2.4, 0])
        nums = VGroup(*[T(f"{v}", 16, MUTED).next_to(ax.n2p(v), DOWN, buff=0.08) for v in range(0, 61, 10)], T("km", 16, MUTED).next_to(ax, RIGHT, buff=0.15))
        dd20 = Rectangle(width=20 * sc, height=0.35, stroke_width=0, fill_color=ACC, fill_opacity=0.8).move_to([x0 + 10 * sc, -1.85, 0])
        dd40 = Rectangle(width=40 * sc, height=0.35, stroke_width=0, fill_color=CH[1], fill_opacity=0.6).move_to([x0 + 20 * sc, -1.4, 0])
        re = DashedVMobject(Rectangle(width=20 * sc, height=0.35, color=WARN), num_dashes=30).move_to([x0 + 50 * sc, -1.4, 0])
        labs = VGroup(T("DD20", 16, BG, BOLD).move_to(dd20), T("DD40", 16, BG, BOLD).move_to(dd40), T("60 km: menzil genişletici gerekebilir (Not 2)", 16, WARN, BOLD).next_to(re, UP, buff=0.1))
        self.play(Create(ax), FadeIn(nums), GrowFromEdge(dd20, LEFT), GrowFromEdge(dd40, LEFT), FadeIn(labs[:2]), run_time=1.0)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(Create(re), FadeIn(labs[2]), run_time=0.8)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p1A")


class E2P1B(Act):
    HDR, MANIFEST, PREV_BADGE = H1, M1, "std"

    def construct(self):
        self.beat("b6")
        self.set_badge("fiz")
        h = self.show_heading("Ayırıcı yapıları")
        def tree(x, y, stages, label):
            g = VGroup()
            src = Line([x - 1.8, y, 0], [x - 1.2, y, 0], color=WHITE, stroke_width=4)
            g.add(src)
            nodes = [np.array([x - 1.2, y, 0])]
            for s, (fan, w) in enumerate(stages):
                new = []
                for nd in nodes:
                    sp = splitter(0.15).move_to(nd + RIGHT * 0.15)
                    g.add(sp)
                    outs = [sp.get_right() + RIGHT * w + UP * (dy) for dy in np.linspace(0.6 / (s + 1), -0.6 / (s + 1), min(fan, 4))]
                    for o in outs:
                        g.add(Line(sp.get_right(), o, color=FEED, stroke_width=1.5))
                    new += outs[:1] if s < len(stages) - 1 else []
                nodes = new
            g.add(T(label, 18, TXT, BOLD).next_to(g, DOWN, buff=0.25))
            return g
        central = tree(-3.4, 0.4, [(64, 2.4)], "merkezi: 1 × 1:64")
        casc = tree(2.2, 0.4, [(4, 1.0), (16, 1.6)], "kademeli: 1:4 + 1:16")
        VGroup(central, casc).scale(1.25).move_to(UP * 0.55)
        m1 = T("…64 kol", 15, MUTED).next_to(central, RIGHT, buff=0.1)
        self.play(FadeIn(central), FadeIn(m1), run_time=0.9)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(casc), run_time=0.9)
        eq = VGroup(T("10·log₁₀64 = 18 dB", 22, ACC, BOLD), T("6 dB + 12 dB = 18 dB", 22, ACC, BOLD)).arrange(RIGHT, buff=2.4).move_to(DOWN * 1.9)
        extra = T("+ her kademe: fazlalık kaybı, ek, konnektör", 18, WARN, BOLD).next_to(eq[1], DOWN, buff=0.2)
        self.at(self.cues[4] - 0.2 if len(self.cues) > 4 else 6)
        self.play(FadeIn(eq), run_time=0.7)
        self.at(self.cues[-1] - 0.2)
        self.play(FadeIn(extra), run_time=0.5)
        self.end(pad=0.05)

        self.beat("b6a")
        self.clear(h)
        ax = Axes(x_range=[1250, 1650, 50], y_range=[17, 23, 1], x_length=8.0, y_length=3.6,
                  axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-1.9, -0.6, 0])
        xl = VGroup(*[T(str(v), 15, MUTED).next_to(ax.c2p(v, 17), DOWN, buff=0.1) for v in (1300, 1400, 1500, 1600)], T("nm", 15, MUTED).next_to(ax.c2p(1650, 17), DOWN, buff=0.1))
        yl = VGroup(*[T(str(v), 15, MUTED).next_to(ax.c2p(1250, v), LEFT, buff=0.1) for v in (18, 20, 22)], T("ekleme kaybı (dB)", 15, MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
        plc = ax.plot(lambda l: 20.3 + 0.15 * np.sin((l - 1250) / 90), x_range=[1260, 1640], color=ACC, stroke_width=4)
        fbt = ax.plot(lambda l: 19.6 + 1.6 * np.sin((l - 1250) / 120) ** 2 + 0.4 * (l - 1450) / 200, x_range=[1260, 1640], color=WARN, stroke_width=4)
        lg = VGroup(T("PLC — dalga boyunda düz", 18, ACC, BOLD), T("FBT — dalga boyuna duyarlı", 18, WARN, BOLD), T("(temsili eğriler)", 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, RIGHT, buff=0.3)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.7)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(Create(plc), FadeIn(lg[0]), FadeIn(lg[2]), run_time=1.0)
        self.at(self.cues[-1] - 0.3)
        self.play(Create(fbt), FadeIn(lg[1]), run_time=1.0)
        self.end(pad=0.05)

        self.beat("b6b")
        self.clear(h)
        sc = 0.42
        x0 = -5.0
        ax2 = NumberLine(x_range=[0, 24, 2], length=24 * sc, include_numbers=False, color=MUTED).move_to([x0 + 12 * sc, -1.6, 0])
        nums = VGroup(*[T(str(v), 15, MUTED).next_to(ax2.n2p(v), DOWN, buff=0.08) for v in range(0, 25, 4)], T("dB", 15, MUTED).next_to(ax2, RIGHT, buff=0.15))
        ideal = Rectangle(width=18.06 * sc, height=0.6, stroke_width=0, fill_color=ACC, fill_opacity=0.85).move_to([x0 + 9.03 * sc, -0.6, 0])
        it = T("ideal 10·log₁₀64 = 18,06 dB", 19, BG, BOLD).move_to(ideal)
        ex = Rectangle(width=2.7 * sc, height=0.6, stroke_width=0, fill_color=WARN, fill_opacity=0.85).next_to(ideal, RIGHT, buff=0)
        et = T("fazlalık + düzgünsüzlük", 17, WARN, BOLD).next_to(ex, UP, buff=0.12)
        ds = T("veri sayfası en kötü durum: tipik 20 … 21 dB (1:64 PLC)", 20, TXT, BOLD).move_to(UP * 0.9)
        self.play(Create(ax2), FadeIn(nums), GrowFromEdge(ideal, LEFT), FadeIn(it), run_time=0.9)
        self.play(GrowFromEdge(ex, LEFT), FadeIn(et), FadeIn(ds), run_time=0.8)
        self.end(pad=0.05)

        # b7 — 4x2 WM hybrid
        self.beat("b7")
        self.clear(h)
        h = self.show_heading("Hibrit yapı: 4×2 WM (G.989.3 Ek X)", h)
        cts = VGroup(*[box(1.0, 0.42, f"CT{i + 1}", CH[i], 14).move_to([-5.6, 0.9 - i * 0.6, 0]) for i in range(4)])
        wm = RoundedRectangle(corner_radius=0.1, width=2.0, height=2.4, stroke_color=GOLD, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([-2.9, 0.0, 0])
        wmt = VGroup(T("4×2 WM", 20, GOLD, BOLD), T("4×1 WM + 1:2", 15, MUTED)).arrange(DOWN, buff=0.08).move_to(wm)
        ins = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=CH[i], stroke_width=2.5) for i, c in enumerate(cts)])
        outs, sps = VGroup(), VGroup()
        for k, y in enumerate((0.8, -0.8)):
            s = splitter(0.3).move_to([1.3, y, 0])
            outs.add(Line([wm.get_right()[0], y * 0.5, 0], s.get_left(), color=FEED, stroke_width=3.5))
            sps.add(VGroup(s, T("1:32", 14, MUTED).next_to(s, DOWN, buff=0.1)))
        onu = VGroup(*[VGroup(*[Line(sps[k][0].get_right(), sps[k][0].get_right() + RIGHT * 1.6 + UP * dy, color="#94A3B8", stroke_width=1.5) for dy in (0.35, 0.12, -0.12, -0.35)]) for k in range(2)])
        self.play(FadeIn(cts), Create(ins), FadeIn(wm), FadeIn(wmt), run_time=1.0)
        self.at(self.cues[3] - 0.2 if len(self.cues) > 3 else 4)
        self.play(Create(outs), FadeIn(sps), Create(onu), self.set_src("G.989.3 Ek X, Şekil X.1"), run_time=1.0)
        self.end(pad=0.05)

        # b7a — wavelength-routed ODN with AWG
        self.beat("b7a")
        self.clear(h)
        h = self.show_heading("Dalga boyu yönlendirmeli ODN", h)
        feed = Line([-5.6, -0.2, 0], [-1.3, -0.2, 0], color=FEED, stroke_width=5)
        awg = RoundedRectangle(corner_radius=0.1, width=1.4, height=2.6, stroke_color=ACC, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([-0.6, -0.2, 0])
        at = T("AWG", 20, ACC, BOLD).move_to(awg)
        outs = VGroup(*[VGroup(Line([awg.get_right()[0], -0.2 + 0.9 - i * 0.6, 0], [3.4, 1.2 - i * 0.95, 0], color=CH[i], stroke_width=3),
                               box(1.4, 0.48, f"ONU · λ{i + 1}", CH[i], 14).move_to([4.2, 1.2 - i * 0.95, 0])) for i in range(4)])
        notes = VGroup(pill("kayıp: güç ayırıcıdan çok düşük", GOOD, 18), pill("her ONU belirli bir kanala bağlı", WARN, 18)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.8)
        self.play(Create(feed), FadeIn(awg), FadeIn(at), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.2) for o in outs], lag_ratio=0.2), run_time=1.2)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(FadeIn(notes[0]), run_time=0.5)
        self.at(self.cues[3] - 0.2 if len(self.cues) > 3 else 7)
        self.play(FadeIn(notes[1]), run_time=0.5)
        nx = T("döngüsel AWG ızgaraları: G.989.2 Ek VII → Bölüm 3", 18, ACC, BOLD).next_to(notes, UP, buff=0.25)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(nx), self.set_src("G.989.2 Ek VII"), run_time=0.5)
        self.end(pad=0.05)

        self.engineer_note("b8", [("1", "Bütçe: en kötü kol", "Ayırıcı düzgünsüzlüğü ONU'lar arasında kayıp farkı yaratır.\nBütçeyi en kötü kola göre yapın.", 1),
                                  ("2", "Diferansiyel kayıp: ayrıca", "En iyi ve en kötü yolun farkını ayrı kontrol edin\n(≤ 15 dB, Tablo 11-3).", 2)])
        self.beat("b9")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bu parçaların toplam kaybı\nstandartta nasıl sınıflara ayrılıyor?")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep02_p1B")


def class_axis(y=-2.4, sc=0.33, x0=-5.8):
    ax = NumberLine(x_range=[0, 36, 5], length=36 * sc, include_numbers=False, color=MUTED).move_to([x0 + 18 * sc, y, 0])
    nums = VGroup(*[T(str(v), 16, MUTED).next_to(ax.n2p(v), DOWN, buff=0.08) for v in range(0, 36, 5)], T("dB", 16, MUTED).next_to(ax, RIGHT, buff=0.15))
    bars = VGroup()
    for i, (nm, lo, c) in enumerate(CLS):
        r = Rectangle(width=15 * sc, height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([ax.n2p(lo + 7.5)[0], y + 0.55 + 0.5 * i, 0])
        bars.add(VGroup(r, T(f"{nm}  {lo}–{lo + 15} dB", 17, BG, BOLD).move_to(r)))
    return ax, nums, bars


class E2P2A(Act):
    HDR, MANIFEST, FIRST = H2, M2, True

    def construct(self):
        self.beat("c1")
        tc = self.title_card("PERDE 2", "Yol kaybı sınıfları")
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 2)
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Dört sınıf — G.989.2 Tablo 6-1")
        ax, nums, bars = class_axis()
        ref = pill("kayıp: S/R-CG ↔ R/S arasında", ACC, 18).move_to([3.6, 1.9, 0])
        self.play(Create(ax), FadeIn(nums), FadeIn(ref), self.set_src("G.989.2 §6.2, Tablo 6-1"), run_time=0.8)
        self.end(pad=0.05)

        self.beat("c2")
        for i in range(4):
            self.at(self.cues[i] - 0.1 if i < len(self.cues) else 1 + i)
            self.play(GrowFromEdge(bars[i], LEFT), run_time=0.5)
        sh = T("her sınıf +2 dB kaydırılmış · genişlik 15 dB", 20, GOLD, BOLD).next_to(bars, UP, buff=0.3)
        self.at(self.cues[-1] - 0.2)
        self.play(FadeIn(sh), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c2a")
        self.play(*[FadeOut(m) for m in (sh, ref)], VGroup(ax, nums, bars).animate.scale(0.6).to_corner(DR, buff=0.4), run_time=0.6)
        olt = box(1.2, 0.8, "OLT", "#3B4A75", 18).move_to([-5.6, 0.8, 0])
        near = box(1.5, 0.5, "ONU yakın", CH[1], 15).move_to([-2.4, 1.6, 0])
        far = box(1.5, 0.5, "ONU uzak", CH[3], 15).move_to([2.6, 0.0, 0])
        ln = Line(olt.get_right(), near.get_left(), color=CH[1], stroke_width=3)
        lf = Line(olt.get_right(), far.get_left(), color=CH[3], stroke_width=3)
        tn = T("en az kayıp", 16, CH[1]).next_to(ln, UP, buff=0.05)
        tf = T("en çok kayıp", 16, CH[3]).next_to(lf.get_center(), DOWN, buff=0.15)
        dr = pill("fark → alıcı dinamik aralığı + burst başına ayar", GOLD, 18).move_to([-1.6, -1.3, 0])
        self.play(FadeIn(olt), FadeIn(near), Create(ln), FadeIn(tn), run_time=0.7)
        self.play(FadeIn(far), Create(lf), FadeIn(tf), run_time=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(dr), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c2b")
        self.play(*[FadeOut(m) for m in (olt, near, far, ln, lf, tn, tf, dr)], run_time=0.4)
        cmp_ = table(["Sistem", "Sınıflar"], [["XG-PON (G.987.2)", "N1 · N2 · E1 · E2"], ["NG-PON2 (G.989.2)", "N1 · N2 · E1 · E2"]], [4.6, 4.6], size=22, hsize=18, row_h=0.62).move_to([-1.6, 0.6, 0])
        why = pill("aynı ODN, aynı kayıp varsayımları → birlikte çalışma", GOOD, 19).next_to(cmp_, DOWN, buff=0.4)
        self.play(FadeIn(cmp_), run_time=0.7)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(why), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c3")
        self.play(FadeOut(cmp_), FadeOut(why), run_time=0.4)
        q = self.quote("G.989.2 §6.2 · §9.3.5.1", "“It takes into account a 15 dB differential optical path loss.”\n“The attenuation range is the difference between the maximum and minimum optical path loss in each class.”",
                       "Her sınıf 15 dB diferansiyel kaybı hesaba katar · zayıflama aralığı = maks − min", width=12.0).move_to(UP * 0.6)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.9)
        self.end(pad=0.05)

        self.beat("c4")
        self.play(FadeOut(q), run_time=0.4)
        warn = card("Neden bir alt sınır?", "Az kayıp = alıcı aşırı yükü, BER bozulması, hatta hasar.\nKazanç elemanı, WDM kuplörü ya da düşük oranlı ayırıcı içeren\nağlar alt sınırın altına düşebilir → zayıflatıcı ile en küçük kaybı garanti et.",
                    "G.989.2 §6.2", WARN, w=11.0, h=2.6, tsize=26).move_to(UP * 0.5)
        self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.8)
        self.end(pad=0.05)

        self.beat("c4a")
        self.play(FadeOut(warn), run_time=0.4)
        olt = box(1.2, 0.7, "OLT", "#3B4A75", 16).move_to([-5.4, 0.6, 0])
        sp = splitter(0.28).move_to([-1.4, 0.6, 0])
        l1 = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=3)
        outs = VGroup(*[Line(sp.get_right(), sp.get_right() + RIGHT * 1.6 + UP * (0.6 - 0.17 * k), color="#94A3B8", stroke_width=1.5) for k in range(8)])
        lab = T("bina içi: 1:8 + birkaç yüz metre ≈ 11–12 dB", 19, WARN, BOLD).move_to([-1.5, -0.6, 0])
        lim = T("< 14 dB (N1 alt sınırı)", 19, WARN, BOLD).next_to(lab, DOWN, buff=0.15)
        att = VGroup(Rectangle(width=0.8, height=0.42, stroke_color=GOOD, stroke_width=2.5, fill_color=BG, fill_opacity=1), T("ATT", 14, GOOD, BOLD)).move_to(l1)
        att[1].move_to(att[0])
        ok = T("çözüm: sabit zayıflatıcı", 19, GOOD, BOLD).next_to(lim, DOWN, buff=0.25)
        self.play(FadeIn(olt), Create(l1), FadeIn(sp), Create(outs), run_time=0.8)
        self.play(FadeIn(lab), FadeIn(lim), run_time=0.6)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(att, scale=1.3), FadeIn(ok), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep02_p2A")


class E2P2B(Act):
    HDR, MANIFEST, PREV_BADGE = H2, M2, "std"

    def construct(self):
        self.beat("c5")
        self.set_badge("fiz")
        h = self.show_heading("Örnek bütçe")
        ax, nums, bars = class_axis(y=-2.6)
        bars.set_opacity(0.35)
        sc = 0.33
        x0 = -5.8
        y = 0.55
        parts = [(20.5, CH[0], "1:64 ≈ 20,5"), (5.0, ACC, "20 km ≈ 5"), (1.5, PINK, "1,5")]
        segs, x = VGroup(), x0
        for w, c, t in parts:
            r = Rectangle(width=w * sc, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x + w * sc / 2, y, 0])
            segs.add(VGroup(r, T(t, 15, BG, BOLD).move_to(r)))
            x += w * sc
        self.play(Create(ax), FadeIn(nums), FadeIn(bars), run_time=0.7)
        for i, t0 in enumerate([self.cues[1], self.cues[2], self.cues[4] if len(self.cues) > 4 else self.cues[-2]]):
            self.at(t0 - 0.2)
            self.play(GrowFromEdge(segs[i], LEFT), run_time=0.6)
        tot = T("≈ 27 dB → N1 ✓", 24, GOOD, BOLD).next_to(segs, UP, buff=0.25).align_to(segs, RIGHT)
        mark = DashedLine(ax.n2p(27) + UP * 3.5, ax.n2p(27), color=GOOD, stroke_width=2)
        tip = T("(fiber: tipik ~0,25 dB/km)", 15, MUTED).next_to(segs, DOWN, buff=0.15).align_to(segs, LEFT)
        self.at(self.cues[-1] - 0.3)
        self.play(FadeIn(tot), Create(mark), bars[0].animate.set_opacity(1), FadeIn(tip), run_time=0.8)
        self.end(pad=0.05)

        self.beat("c6")
        add40 = Rectangle(width=5 * sc, height=0.6, stroke_width=0, fill_color=CH[1], fill_opacity=0.9).next_to(segs, RIGHT, buff=0)
        a40 = T("+5 (40 km)", 14, BG, BOLD).move_to(add40)
        tot2 = T("≈ 32 dB → E1", 24, CH[2], BOLD).move_to(tot)
        mark2 = DashedLine(ax.n2p(32) + UP * 3.5, ax.n2p(32), color=CH[2], stroke_width=2)
        self.play(GrowFromEdge(add40, LEFT), FadeIn(a40), FadeTransform(tot, tot2), Transform(mark, mark2), bars[0].animate.set_opacity(0.35), bars[2].animate.set_opacity(1), run_time=1.0)
        add128 = Rectangle(width=3 * sc, height=0.6, stroke_width=0, fill_color=CH[0], fill_opacity=0.6).next_to(add40, RIGHT, buff=0)
        a128 = T("+3", 14, BG, BOLD).move_to(add128)
        tot3 = T("≈ 35 dB → E2 sınırında", 24, CH[3], BOLD).move_to(tot2).shift(RIGHT * 0.5)
        mark3 = DashedLine(ax.n2p(35) + UP * 3.5, ax.n2p(35), color=CH[3], stroke_width=2)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 6)
        self.play(GrowFromEdge(add128, LEFT), FadeIn(a128), FadeTransform(tot2, tot3), Transform(mark, mark3), bars[2].animate.set_opacity(0.35), bars[3].animate.set_opacity(1), run_time=1.0)
        self.end(pad=0.05)

        self.clear()
        self.save_timeline("ep02_p2B")


class E2P2C(Act):
    HDR, MANIFEST, PREV_BADGE = H2, M2, "fiz"

    def construct(self):
        h = None
        self.beat("c6a")
        self.clear(h)
        h = self.show_heading("Sınıf seçimi = mimari karar", h)
        left = card("Daha yüksek sınıf", "daha uzun mesafe\nveya daha yüksek bölünme", None, GOOD, w=5.2, h=2.0, tsize=24)
        right = card("Bedeli", "daha güçlü verici · daha hassas alıcı\ngenellikle daha pahalı optik", None, WARN, w=5.2, h=2.0, tsize=24)
        VGroup(left, right).arrange(RIGHT, buff=0.5).move_to(UP * 0.6)
        tx = table(["10G ↓ OLT vericisi", "N1", "E2"], [["min. başlatma gücü", "+3,0 dBm", "+9,0 dBm"]], [4.6, 2.0, 2.0], size=22, hsize=18, row_h=0.6).move_to(DOWN * 1.8)
        self.play(FadeIn(left, shift=UP * 0.2), run_time=0.6)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 4)
        self.play(FadeIn(right, shift=UP * 0.2), run_time=0.6)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 7)
        self.play(FadeIn(tx), self.set_src("G.989.2 Tablo 11-5"), run_time=0.6)
        self.end(pad=0.05)

        self.beat("c7")
        self.clear(h)
        self.set_badge("tc")
        h = self.show_heading("Sahada sınıflar: kademeli büyüme (G.989.3 Ek X)", h)
        ph = VGroup(card("1. aşama", "CT1, CT2 → N1 optikler\n(ilk yaygın optikler)", None, CH[0], w=5.0, h=1.8, tsize=24),
                    card("2. aşama", "CT3, CT4 → N2 optikler\n(+2 dB bütçe)", None, CH[1], w=5.0, h=1.8, tsize=24)).arrange(RIGHT, buff=0.6).move_to(UP * 0.7)
        arr = Arrow(ph[0].get_right(), ph[1].get_left(), buff=0.1, color=MUTED, stroke_width=3)
        same = pill("aynı ODN, iki sınıf birlikte", GOOD, 20).move_to(DOWN * 1.2)
        self.at(self.cues[1] - 0.2 if len(self.cues) > 1 else 2)
        self.play(FadeIn(ph[0], shift=UP * 0.2), self.set_src("G.989.3 Ek X"), run_time=0.6)
        self.at(self.cues[2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(GrowArrow(arr), FadeIn(ph[1], shift=UP * 0.2), run_time=0.8)
        self.at(self.cues[-1] - 0.2)
        self.play(FadeIn(same), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c8")
        q = self.quote("G.989.3 Ek X", "“As outlined in ITU-T G.989.2, the ONU side optics is identical for N1 through to E1 ODN optical path loss classes.”",
                       "ONU optikleri N1 … E1 için aynı → sınıf farkı OLT optikleriyle karşılanır", width=12.0).move_to(DOWN * 2.0)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.end(pad=0.05)

        self.engineer_note("c9", [("1", "Sınıfı ölçümle belirleyin", "Ölçülen en kötü ve en iyi yola bakın; ortalama kayıp yanıltır.", 1),
                                  ("2", "Marj bırakın", "Yaşlanma, onarım ekleri ve sıcaklık için bütçede pay ayırın.", 2)])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep02_p2C")
