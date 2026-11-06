"""B03 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to the B02 quiz."""
from ep03_common import *

AGENDA = ["Spektrum haritası: Tablo 9-1", "Komşular: G-PON, XG-PON1, video, OTDR", "Izgaralar: aralık, sapma, ayar penceresi",
          "Raman ve kanal profilleri", "Laboratuvar: OSA ve yalıtım"]
PX, PY = 3.4, -0.45


class Ep03Open(Narrated):
    MANIFEST = M3("open")

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP3['n']} · {EP3['title'].upper()}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP3['n']:02d}", 120, ACC, BOLD)
        sub = T(EP3["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP3["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            if m.width > 6.0:
                m.scale_to_fit_width(6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, cover

        # o2 — spectrum bands
        self.beat("o2")
        axg, X = nm_axis(1520, 1630, PX - 2.8, PX + 3.0, PY - 1.0, step=10, label_every=50, size=13)
        b = VGroup(band(X, 1524, 1544, PY - 0.55, 0.45, TW_US, "TWDM ↑", lsize=13),
                   band(X, 1596, 1603, PY + 0.05, 0.45, TW_DS, None).add(T("TWDM ↓", 13, TW_DS, BOLD).move_to([X(1599.5), PY + 0.5, 0])),
                   band(X, 1603, 1625, PY - 0.55, 0.45, PTP, "PtP", lsize=13))
        tb = T("Tablo 9-1", 26, GOLD, BOLD).move_to([PX + 0.2, PY + 1.6, 0])
        self.focus(0, VGroup(axg, b, tb))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(tb), run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in b], lag_ratio=0.3), run_time=1.2)
        self.end(pad=0.05)

        # o3 — neighbours
        self.beat("o3")
        axg, X = nm_axis(1250, 1680, PX - 2.8, PX + 3.0, PY - 1.0, step=50, label_every=100, size=13)
        leg = VGroup(*[band(X, a, c, PY - 0.55, 0.45, col, None) for a, c, col in [(1260, 1280, LEGACY), (1290, 1330, LEGACY), (1480, 1500, LEGACY), (1550, 1560, VIDEO), (1575, 1580, LEGACY)]],
                     outline_band(X, 1625, 1675, PY - 0.55, 0.45, MUTED))
        names = VGroup(T("XG-PON1 ↑", 12, MUTED).move_to([X(1270), PY + 0.05, 0]), T("G-PON ↑", 12, MUTED).move_to([X(1310), PY + 0.35, 0]),
                       T("G-PON ↓", 12, MUTED).move_to([X(1490), PY + 0.05, 0]), T("video", 12, VIDEO).move_to([X(1555), PY + 0.35, 0]),
                       T("XG ↓", 12, MUTED).move_to([X(1578), PY + 0.05, 0]), T("OTDR", 12, MUTED).move_to([X(1650), PY + 0.05, 0]))
        ng = VGroup(band(X, 1524, 1544, PY - 0.55, 0.45, TW_US, None, op=0.9), band(X, 1596, 1603, PY - 0.55, 0.45, TW_DS, None), band(X, 1603, 1625, PY - 0.55, 0.45, PTP, None))
        cap = T("NG-PON2 boşluklara yerleşir", 20, GOOD, BOLD).move_to([PX + 0.2, PY + 1.4, 0])
        self.focus(1, VGroup(axg, leg, names, ng, cap))
        self.play(Create(axg[0]), FadeIn(axg[1:]), LaggedStart(*[FadeIn(x) for x in leg], lag_ratio=0.15), FadeIn(names), run_time=1.3)
        self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in ng], lag_ratio=0.25), FadeIn(cap), run_time=1.0)
        self.end(pad=0.05)

        # o4 — grids
        self.beat("o4")
        y = PY + 0.2
        base = Line([PX - 2.8, y - 0.6, 0], [PX + 3.0, y - 0.6, 0], color=MUTED, stroke_width=2)
        chans = VGroup()
        for i in range(4):
            x = PX - 2.0 + i * 1.35
            chans.add(VGroup(Line([x, y - 0.6, 0], [x, y + 0.6, 0], color=CH[i], stroke_width=4),
                             DoubleArrow([x - 0.3, y + 0.8, 0], [x + 0.3, y + 0.8, 0], buff=0, color=GOLD, stroke_width=2, tip_length=0.1)))
        cs = BraceBetweenPoints([PX - 2.0, y - 0.75, 0], [PX - 0.65, y - 0.75, 0], DOWN, color=ACC)
        cst = T("kanal aralığı 50…200 GHz", 16, ACC, BOLD).next_to(cs, DOWN, buff=0.08)
        mse = T("± MSE", 16, GOLD, BOLD).next_to(chans[3][1], UP, buff=0.08)
        w = T("ayar penceresi ≥ (N−1)·CS + 2·MSE", 20, TXT, BOLD).move_to([PX + 0.2, PY - 2.1, 0])
        self.focus(2, VGroup(base, chans, cs, cst, mse, w))
        self.play(Create(base), LaggedStart(*[FadeIn(c[0]) for c in chans], lag_ratio=0.2), run_time=0.9)
        self.play(FadeIn(cs), FadeIn(cst), run_time=0.5)
        self.play(*[GrowFromCenter(c[1]) for c in chans], FadeIn(mse), run_time=0.6)
        self.play(FadeIn(w, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o5 — Raman + channel profiles
        self.beat("o5")
        y = PY + 0.9
        v = band(lambda n: PX - 2.4 + (n - 1540) * 0.07, 1550, 1560, y, 0.45, VIDEO, "video", lsize=13)
        d = band(lambda n: PX - 2.4 + (n - 1540) * 0.07, 1596, 1603, y, 0.45, TW_DS, "TWDM ↓", lsize=12)
        ar = CurvedArrow(d[0].get_top() + UP * 0.05, v[0].get_top() + UP * 0.05, angle=0.9, color=WARN, stroke_width=3)
        rt = T("Raman karışması", 18, WARN, BOLD).next_to(ar, UP, buff=0.05)
        cp = pill("Channel_Profile · System_Profile", "#A78BFA", 18).move_to([PX + 0.2, PY - 1.3, 0])
        cpt = T("haritayı ONU'ya anlatır (G.989.3 §17.1)", 16, MUTED).next_to(cp, DOWN, buff=0.15)
        self.focus(3, VGroup(v, d, ar, rt, cp, cpt))
        self.play(FadeIn(v), FadeIn(d), run_time=0.6)
        self.play(Create(ar), FadeIn(rt), run_time=0.8)
        self.at(self.cues[-2] - 0.2 if len(self.cues) > 2 else 5)
        self.play(FadeIn(cp, shift=UP * 0.1), FadeIn(cpt), run_time=0.6)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        osa = instrument("OSA", 2.6, 1.9).move_to([PX - 1.2, PY + 0.4, 0])
        iso = VGroup(box(1.4, 0.7, "WM", "#3B4A75", 16), T("yalıtım\n> 50 dB?", 16, GOOD, BOLD)).arrange(DOWN, buff=0.15).move_to([PX + 1.8, PY + 0.4, 0])
        cap = T("kanal haritası · yalıtım · Raman", 20, GOOD, BOLD).move_to([PX + 0.2, PY - 1.5, 0])
        self.focus(4, VGroup(osa, iso, cap))
        self.play(FadeIn(osa, shift=UP * 0.15), FadeIn(iso, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(cap), run_time=0.5)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep03_open")

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


class Ep03Recap(Act):
    HDR, MANIFEST, FIRST = "BÖLÜM 3 · ÖNCEKİ BÖLÜMDE", M3("recap"), True

    def construct(self):
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 2 · Işığın Yolu")
        self.at(1.2)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["ODN: kanal bağlantı · besleme · dağıtım fiberi", "Dört sınıf N1 … E2 · bütçe: P_min − S ≥ OPL_maks + OPP",
               "Dispersiyon aralığı · ORL ≥ 32 dB · ayrık yansıma < −35 dB", "Mesafenin zaman yüzü: sessiz pencere, ranging, EqD"]
        items = VGroup(*[VGroup(T("✓", 26, GOOD, BOLD), T(s, 23, TXT)).arrange(RIGHT, buff=0.3) for s in pts]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.35), run_time=2.6)
        self.end(pad=0.05)
        self.clear()
        qa = [("Soru 1", "20 km fiber + 1:128 ayırıcı: hangi sınıf?", "1:128 ≈ 23,5 + fiber 5 + ekler 1,5 ≈ 30 dB\nN1 (≤ 29 dB) ✗   ·   N2 (≤ 31 dB) ✓ — pay ≈ 1 dB", CH[0], "a2"),
              ("Soru 2", "Yükselteçli OLT alıcısı ONU'nun P_min'ini kaç dB düşürür?", "2,5G ↑: +4 → 0 dBm  =  4 dB\n10G ↑: +4 → +2 dBm  =  2 dB  (N1 … E1)", CH[1], "a3"),
              ("Soru 3", "40 km diferansiyel mesafe: SN toplama sessiz penceresi?", "≈ 400 µs (RTD değişimi) + 2 µs + 48 µs\n= 450 µs   (G.989.3 §13.1.2)", CH[3], "a4")]
        prev = None
        for title, q, a, c, bid in qa:
            self.beat(bid)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            qt = VGroup(T(title, 26, c, BOLD), T(q, 28, TXT, SEMIBOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.2).to_edge(LEFT, buff=1.0)
            ans = RoundedRectangle(corner_radius=0.18, width=11.5, height=2.3, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.3)
            at = VGroup(T("Cevap", 20, GOOD, BOLD), T(a, 24, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ans).align_to(ans, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(max(1.0, self.cues[1] - 0.2) if len(self.cues) > 1 else 1.0)
            self.play(FadeIn(ans), FadeIn(at, shift=UP * 0.1), run_time=0.7)
            prev = VGroup(qt, ans, at)
            self.end(pad=0.1)
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep03_recap")
