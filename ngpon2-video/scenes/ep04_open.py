"""B04 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to the B03 quiz."""
from ep03_common import *
from ep04_common import *

AGENDA = ["Hız, saat ve hat kodu", "Güç ve sönüm oranı", "Spektrum: SMSR, sapma, OOB / OOC",
          "Göz maskesi, titreşim · 125 µs çerçeve", "Laboratuvar: DCA ve OSA"]
PX, PY = 3.4, -0.45
CX = PX + 0.2  # teaser panel centre x


class Ep04Open(Narrated):
    MANIFEST = M4("open")

    def cue(self, sub, default=0.0):
        for c in self.bmap[self.timeline[-1]["id"]]["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        print(f"CUE MISS {self.timeline[-1]['id']}: {sub!r}", file=sys.stderr)
        return default

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP4['n']} · {EP4['title'].upper()}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([CX, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP4['n']:02d}", 120, ACC, BOLD)
        sub = T(EP4["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP4["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            if m.width > 6.0:
                m.scale_to_fit_width(6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([CX, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, cover

        # o2 — rates, clock, line code
        self.beat("o2")
        rates = VGroup(T("9,95328 Gbit/s", 30, TW_DS, BOLD), T("2,48832 Gbit/s", 30, TW_DS, BOLD)).arrange(DOWN, buff=0.22).move_to([CX, PY + 1.85, 0])
        clk = VGroup(pill("Stratum-1", GOLD, 19), pill("Stratum-4", MUTED, 19)).arrange(RIGHT, buff=0.35).move_to([CX, PY + 0.45, 0])
        bits = "1011001110100101"
        tb = 0.34
        wave = nrz_wave(bits, CX - len(bits) * tb / 2, tb, PY - 1.85, PY - 0.95)
        wl = T("karıştırılmış NRZ", 18, MUTED).next_to(wave, DOWN, buff=0.18)
        self.focus(0, VGroup(rates, clk, wave, wl))
        self.at(self.cue("dokuz virgül", 1.5))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rates], lag_ratio=0.4), run_time=0.9)
        self.at(self.cue("Stratum", 5))
        self.play(FadeIn(clk, shift=UP * 0.1), run_time=0.5)
        self.play(Create(wave), FadeIn(wl), run_time=0.9)
        self.end(pad=0.05)

        # o3 — launch power windows + ER
        self.beat("o3")
        Y = lambda d: PY - 1.6 + (d - 2) * 0.21
        bars, labs = VGroup(), VGroup()
        for i, (cl, lo, hi) in enumerate([("N1", 3, 7), ("N2", 5, 9), ("E1", 7, 11), ("E2", 9, 11)]):
            x = CX - 1.95 + i * 1.3
            r = Rectangle(width=0.62, height=Y(hi) - Y(lo), stroke_width=0, fill_color=TW_DS if cl != "E2" else WARN, fill_opacity=0.8).move_to([x, (Y(hi) + Y(lo)) / 2, 0])
            bars.add(r)
            labs.add(T(cl, 18, TXT, BOLD).move_to([x, PY - 2.05, 0]))
        cap = T("başlatma gücü penceresi · 10G ↓", 18, MUTED).move_to([CX, PY + 0.75, 0])
        er = pill("sönüm oranı ≥ 8,2 dB", GOLD, 20).move_to([CX, PY + 2.0, 0])
        trade = T("ER ↓  ⇄  güç ↑", 20, GOLD, BOLD).next_to(er, DOWN, buff=0.2)
        self.focus(1, VGroup(bars, labs, cap, er, trade))
        self.at(self.cue("sınıf başına", 1.5))
        self.play(FadeIn(labs), FadeIn(cap), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=1.0)
        self.at(self.cue("sönüm oranının", 4))
        self.play(FadeIn(er, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.cue("güçle takası", 6))
        self.play(FadeIn(trade), run_time=0.5)
        self.end(pad=0.05)

        # o4 — spectrum: SMSR, MSE, OOB/OOC
        self.beat("o4")
        o = np.array([CX, PY - 1.4, 0])
        o = o + LEFT * 0.35
        spec = spec_db(o, 1.0, 0.046, [(0, 0), (-1.3, -38), (1.3, -34)], (-2.5, 2.5), floor=-58, w=0.04)
        base = Line(o + [-2.6, 0, 0], o + [2.6, 0, 0], color=MUTED, stroke_width=2)
        ytop, yside = o[1] + 58 * 0.046, o[1] + (58 - 34) * 0.046
        ax_ = o[0] + 1.85
        sm = VGroup(DashedLine([o[0] + 1.3, yside, 0], [ax_ + 0.1, yside, 0], color=GOLD, stroke_width=1.5),
                    DashedLine([o[0] + 0.1, ytop, 0], [ax_ + 0.1, ytop, 0], color=GOLD, stroke_width=1.5),
                    DoubleArrow([ax_, yside, 0], [ax_, ytop, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12),
                    T("SMSR\n≥ 30 dB", 17, GOLD, BOLD, line_spacing=0.85).next_to([ax_, (yside + ytop) / 2, 0], RIGHT, buff=0.12))
        mse = VGroup(DoubleArrow([o[0] - 0.55, ytop + 0.3, 0], [o[0] + 0.55, ytop + 0.3, 0], buff=0, color=TW_DS, stroke_width=2.5, tip_length=0.1),
                     T("± 20 GHz", 16, TW_DS, BOLD).move_to([o[0], ytop + 0.58, 0]))
        nb = VGroup(pill("OOC → diğer TWDM", ACC, 16), pill("OOB → PtP WDM", PTP, 16)).arrange(RIGHT, buff=0.25).move_to([CX, PY - 2.2, 0])
        self.focus(2, VGroup(spec, base, sm, mse, nb))
        self.play(Create(base), Create(spec), run_time=1.0)
        self.at(self.cue("yan mod", 1.5))
        self.play(FadeIn(sm), run_time=0.6)
        self.at(self.cue("spektral sapma", 3))
        self.play(FadeIn(mse), run_time=0.5)
        self.at(self.cue("komşuları", 5))
        self.play(FadeIn(nb, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # o5 — eye mask + 125 µs frame
        self.beat("o5")
        eo = np.array([CX - 1.6, PY + 0.35, 0])
        W, H = 2.0, 1.15
        scr = eye_frame(eo, W, H, -0.3, 1.9, 1.5, -0.5)
        eye = eye_traces(eo, W, H, u0=-0.3, u1=1.9, sw=1.6, op=0.45)
        msk = eye_mask(eo, W, H, 0.4, 0.6, u0=-0.3, u1=1.9)
        fx = CX - 2.9
        fb = seg_bar([("PSBd", 0.9, GOLD, 0.85), ("FEC + karıştırıcı · yük", 4.9, TW_DS, 0.25)], PY - 1.75, fx, h=0.55, size=16)
        fl = VGroup(DoubleArrow([fx, PY - 2.3, 0], [fx + 5.8, PY - 2.3, 0], buff=0, color=MUTED, stroke_width=2, tip_length=0.1),
                    T("125 µs", 16, MUTED, BOLD).move_to([CX, PY - 2.55, 0]))
        self.focus(3, VGroup(scr, eye, msk, fb, fl))
        self.play(FadeIn(scr), LaggedStart(*[Create(e) for e in eye], lag_ratio=0.02), run_time=1.0)
        self.play(FadeIn(msk), run_time=0.5)
        self.at(self.cue("TC köprüsünde", 3))
        self.play(FadeIn(fb[1]), FadeIn(fl), run_time=0.6)
        self.at(self.cue("PSBd", 5))
        self.play(GrowFromEdge(fb[0], LEFT), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        dca = instrument("DCA", 2.5, 1.8).move_to([CX - 1.45, PY + 0.4, 0])
        osa = instrument("OSA", 2.5, 1.8).move_to([CX + 1.45, PY + 0.4, 0])
        cap = T("göz · sönüm oranı · spektrum", 20, GOOD, BOLD).move_to([CX, PY - 1.6, 0])
        self.focus(4, VGroup(dca, osa, cap))
        self.play(FadeIn(dca, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("OSA ile", 2.5))
        self.play(FadeIn(osa, shift=UP * 0.15), FadeIn(cap), run_time=0.6)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep04_open")

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


class Ep04Recap(Act4):
    HDR, MANIFEST, FIRST = "BÖLÜM 4 · ÖNCEKİ BÖLÜMDE", M4("recap"), True

    def construct(self):
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 3 · Renk Haritası")
        self.at(1.2)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["Dalga boyu planı: TWDM ↓ 1596–1603 nm · ↑ geniş / azaltılmış / dar", "Eski sistemlerle birlikte: G-PON · XG-PON1 · RF video · OTDR",
               "Izgaralar: ↓ 100 GHz sabit · ↑ CS 50…200 GHz · MSE", "Raman: modülasyon karışması ve güç tüketimi",
               "Kanal profilleri: System_Profile · Channel_Profile"]
        items = VGroup(*[VGroup(T("✓", 26, GOOD, BOLD), T(s, 23, TXT)).arrange(RIGHT, buff=0.3) for s in pts]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.25)
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.35), run_time=3.0)
        self.end(pad=0.05)
        qa = [("Soru 1", "4 kanal · döngüsel değil · 100 GHz ↑ ızgara:\nen küçük ayar penceresi?", "W = (N − 1) · CS + 2 · MSE\n= 3 · 100 + 2 · 20 = 340 GHz", CH[0], "a2", "Formül"),
              ("Soru 2", "↑ kanal 195,1 THz:\nChannel_Profile'da hangi sayıyla yazılır?", "0,1 GHz birimi: 195 100 GHz\n→ 1 951 000", CH[1], "a3", "Frekans sıfır virgül"),
              ("Soru 3", "Raman modülasyon karışması:\naynı yönde mi, karşı yönde mi?", "Yalnızca AYNI yönde yayılanlar arasında\nKarşı yön: güç tüketimi var, modülasyon karışması yok", CH[3], "a4", "Raman kaynaklı")]
        prev = None
        for title, q, a, c, bid, key in qa:
            self.beat(bid)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            else:
                self.clear(rt=0.4)
            qt = VGroup(T(title, 26, c, BOLD), T(q, 28, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.15).to_edge(LEFT, buff=1.0)
            ans = RoundedRectangle(corner_radius=0.18, width=11.5, height=2.2, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.55)
            at = VGroup(T("Cevap", 20, GOOD, BOLD), T(a, 24, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ans).align_to(ans, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(max(1.5, self.cue(key, 3)))
            self.play(FadeIn(ans), FadeIn(at, shift=UP * 0.1), run_time=0.7)
            prev = VGroup(qt, ans, at)
            self.end(pad=0.1)
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep04_recap")
