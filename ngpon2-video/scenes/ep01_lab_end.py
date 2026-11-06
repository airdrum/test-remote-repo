"""B01 · Laboratuvarda (test tezgâhı) + Kapanış + künye."""
from kit import *

HDRL = "BÖLÜM 1 · LABORATUVARDA — Test tezgâhı"
HDRE = "BÖLÜM 1 · KAPANIŞ"
MANL = "build/v4/ep01_lab/audio_proc/manifest.json"
MANE = "build/v4/ep01_end/audio_proc/manifest.json"


def extra_tile(kind, w=2.15, h=1.55):
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color="#475569", stroke_width=2, fill_color="#0D1426", fill_opacity=1)
    c = body.get_center()
    if kind == "spool":
        g = VGroup(*[Circle(radius=r, color=CH[1], stroke_width=2).move_to(c + UP * 0.1) for r in (0.18, 0.3, 0.42)]); name = "Fiber makarası"
    elif kind == "tls":
        g = VGroup(*[FunctionGraph(lambda x, cc=cc: c[1] - 0.35 + 0.6 * np.exp(-((x - cc) / 0.05) ** 2), x_range=[cc - 0.2, cc + 0.2], color=CH[i], stroke_width=2)
                     for i, cc in enumerate([c[0] - 0.5, c[0] - 0.15, c[0] + 0.2, c[0] + 0.55])]); name = "Girişim kaynakları"
    else:
        g = VGroup(Rectangle(width=0.18, height=0.7, color=WARN, stroke_width=2).move_to(c + UP * 0.1),
                   Circle(radius=0.15, color=WARN, fill_color=WARN, fill_opacity=0.8).move_to(c + DOWN * 0.3)); name = "Sıcaklık kabini"
    return VGroup(body, VGroup(), g, VGroup(), T(name, 16, TXT, SEMIBOLD).next_to(body, DOWN, buff=0.1))


class LabA(Act):
    HDR, MANIFEST, FIRST = HDRL, MANL, True

    def construct(self):
        self.beat("u1")
        tc = self.title_card("LABORATUVARDA", "Test tezgâhı")
        self.at(self.cues[1] - 0.2)
        self.to_header(tc)
        self.set_badge("lab")
        tiles = VGroup(*[instrument(k) for k in ("OSA", "DCA", "BERT", "PM", "VOA", "OSC")])
        tiles.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.55)).move_to([-2.4, -0.5, 0])
        self.at(self.cues[2])
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2, scale=0.95) for t in tiles], lag_ratio=0.12), run_time=1.6)
        dims = VGroup(*[Rectangle(width=t.width + 0.1, height=t.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=0).move_to(t) for t in tiles])
        self.add(dims)
        self.end(pad=0.05)

        def focus(i, title, lines, eps, beat):
            self.beat(beat)
            info = card(title, "\n".join(lines), None, GOOD, w=4.6, h=2.6, tsize=24, bsize=18).move_to([4.5, 0.4, 0])
            chips = VGroup(*[pill(f"B{e}", ACC, 18) for e in eps]).arrange(RIGHT, buff=0.15).next_to(info, DOWN, buff=0.25)
            anims = [dims[j].animate.set_fill(opacity=0.0 if j == i else 0.72) for j in range(len(tiles))]
            if hasattr(self, "_info"):
                anims += [FadeOut(self._info)]
            self.play(*anims, FadeIn(info, shift=LEFT * 0.2), run_time=0.7)
            self.at(self.cues[-1] if len(self.cues) else 0)
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in chips], lag_ratio=0.2), run_time=0.6)
            self._info = VGroup(info, chips)
            self.end(pad=0.05)

        focus(0, "OSA", ["kanal haritası", "SMSR · spektral sapma", "RBW → 50/100 GHz'de doğruluk"], [3, 4, 7], "u2")
        focus(1, "DCA + referans alıcı", ["göz maskesi", "sönüm oranı", "sürekli ↓ ve burst ↑"], [4, 6], "u3")
        self.beat("u3a")
        self.play(FadeOut(self._info), *[d_.animate.set_fill(opacity=0.72) for d_ in dims], run_time=0.5)
        del self._info
        n1 = card("Göz maskesi: geometri + düzenek", "Maske parametreleri: Tablo 11-8\nTest düzeneği: Şekil 11-4", "G.989.2 §11.1.5.3", ACC, w=5.6, h=2.0, tsize=22).move_to([3.9, 1.0, 0])
        n2 = card("Kalibrasyon dalga boyu", "Ölçer 1550 nm'ye ayarlıysa L bandında\nonda birler mertebesinde dB hata", None, WARN, w=5.6, h=1.9, tsize=22).next_to(n1, DOWN, buff=0.3)
        self.play(FadeIn(n1, shift=LEFT * 0.2), run_time=0.7)
        self.at(self.cues[3] if len(self.cues) > 3 else 0)
        self.play(FadeIn(n2, shift=LEFT * 0.2), run_time=0.7)
        self.end(pad=0.05)
        self.play(FadeOut(n1), FadeOut(n2), run_time=0.4)
        focus(2, "BERT", ["sürekli ve burst mod", "hassasiyet · aşırı yük", "yol cezası"], [5, 8], "u4")
        self.beat("u5")
        self.play(FadeOut(self._info), *[dims[j].animate.set_fill(opacity=0.0 if j in (3, 4, 5) else 0.72) for j in range(len(tiles))], run_time=0.6)
        info = VGroup(card("VOA", "yol kaybını yeniden yaratır", None, GOOD, w=4.6, h=1.1, tsize=22, bsize=17),
                      card("Burst güç ölçer", "ortalama tuzağına düşmemek için", None, GOOD, w=4.6, h=1.1, tsize=22, bsize=17),
                      card("Osiloskop + hızlı PD", "burst zamanlaması · ayar süresi", None, GOOD, w=4.6, h=1.1, tsize=22, bsize=17)).arrange(DOWN, buff=0.2).move_to([4.5, -0.3, 0])
        for k, t0 in enumerate([0.2, self.cues[3], self.cues[5]]):
            self.at(t0)
            self.play(FadeIn(info[k], shift=LEFT * 0.2), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_labA")


class LabB(Act):
    HDR, MANIFEST, PREV_BADGE = HDRL, MANL, "lab"

    def construct(self):
        self.beat("u6")
        h = self.show_heading("Ve ayrıca")
        ex = VGroup(*[extra_tile(k) for k in ("spool", "tls", "temp")]).arrange(RIGHT, buff=0.7).move_to(UP * 0.5)
        for k, t0 in enumerate([self.cues[1], self.cues[2], self.cues[3]]):
            self.at(t0 - 0.1)
            self.play(FadeIn(ex[k], shift=UP * 0.2), run_time=0.6)
        q = self.quote("G.989.2 §11.1", "“All parameter values specified are met under the worst-case operating conditions such as temperature\nand humidity, and include ageing effects…”",
                       "Bütün değerler en kötü koşullarda — sıcaklık, nem — ve yaşlanma dahil sağlanmalı", width=12.0).to_edge(DOWN, buff=0.95)
        self.at(self.cues[4])
        self.play(FadeIn(q, shift=UP * 0.15), self.set_src("G.989.2 §11.1"), run_time=0.8)
        self.end(pad=0.05)

        # u6a — reference downstream test setup
        self.beat("u6a")
        self.clear(h)
        h = self.show_heading("Tipik aşağı yön test düzeneği", h)
        y = 0.3
        olt = box(1.8, 0.8, "OLT Tx (DUT)", GOLD, 16).move_to([-5.6, y, 0])
        voa = box(1.1, 0.7, "VOA", MUTED, 16).move_to([-3.4, y, 0])
        spool = VGroup(*[Circle(radius=r, color=CH[1], stroke_width=2) for r in (0.16, 0.28, 0.4)]).move_to([-1.6, y, 0])
        sp_t = T("20/40 km", 14, CH[1]).next_to(spool, DOWN, buff=0.08)
        cpl = box(1.0, 0.7, "kuplör", MUTED, 15).move_to([0.4, y, 0])
        onu = box(1.9, 0.8, "ONU Rx", CH[1], 16).move_to([3.0, y, 0])
        bert = box(1.3, 0.7, "BERT", GOOD, 16).move_to([5.4, y, 0])
        osa = box(1.0, 0.6, "OSA", GOOD, 15).move_to([-0.3, y - 1.7, 0])
        pm = box(1.2, 0.6, "güç ölç.", GOOD, 15).move_to([1.2, y - 1.7, 0])
        chain = [olt, voa, spool, cpl, onu, bert]
        lines = VGroup(*[Line(a.get_right(), b.get_left(), color=FEED, stroke_width=3) for a, b in zip(chain[:-1], chain[1:])])
        taps = VGroup(Line(cpl.get_bottom(), osa.get_top(), color=FEED, stroke_width=2), Line(cpl.get_bottom(), pm.get_top(), color=FEED, stroke_width=2))
        odn = DashedVMobject(SurroundingRectangle(VGroup(voa, spool, sp_t), buff=0.2, corner_radius=0.12, color=ACC), num_dashes=50)
        odn_t = T("referans ODN", 15, ACC, BOLD).next_to(odn, UP, buff=0.06)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(olt), run_time=0.4)
        self.at(self.cues[3])
        self.play(FadeIn(voa), FadeIn(spool), FadeIn(sp_t), Create(lines[:2]), Create(odn), FadeIn(odn_t), run_time=1.0)
        self.at(self.cues[4])
        self.play(FadeIn(cpl), Create(lines[2]), run_time=0.5)
        self.play(FadeIn(osa), FadeIn(pm), Create(taps), run_time=0.7)
        self.at(self.cues[6])
        self.play(FadeIn(onu), FadeIn(bert), Create(lines[3:]), run_time=0.8)
        nx = pill("→ Bölüm 2: referans ODN'i adım adım kuracağız", ACC, 18).to_edge(DOWN, buff=0.7)
        self.at(self.cues[7])
        self.play(FadeIn(nx), self.set_src("şematik · mühendislik pratiği"), run_time=0.6)
        self.end(pad=0.05)

        # u7 — engineer's note: three columns
        self.beat("u7")
        self.clear()
        self.set_badge("not")
        tb = table(["Ölçüm", "Referans noktası", "BER referansı", "Sıcaklık"],
                   [["OLT Tx başlatma gücü", "S/R-CG", "—", "min / oda / maks"], ["ONU Rx hassasiyeti", "R/S", "10⁻³ (10G)", "min / oda / maks"],
                    ["…", "…", "…", "…"]], [3.6, 2.8, 2.6, 3.0], size=20, hsize=18, row_h=0.6).move_to(DOWN * 0.3)
        ttl = T("Her ölçümün yanına üç sütun", 30, PINK, BOLD).next_to(tb, UP, buff=0.5)
        self.play(FadeIn(ttl), run_time=0.5)
        self.at(self.cues[2])
        self.play(FadeIn(tb[0]), run_time=0.5)
        for k, t0 in enumerate([self.cues[3], self.cues[4], self.cues[4] + 1.5]):
            self.at(t0)
            self.play(FadeIn(tb[k + 1], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.2)
        self.clear()
        self.drop_badge()
        self.save_timeline("ep01_labB")


class EndA(Act):
    HDR, MANIFEST, FIRST = HDRE, MANE, True

    def construct(self):
        self.beat("v1")
        tc = self.title_card("KAPANIŞ", "Bölüm 1'in özeti")
        self.at(self.cues[1] - 0.3)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["PON pasif bir ağaçtır: ↓ herkese yayın, ↑ sıraya girmek zorunda",
               "NG-PON2 hızı değil renk sayısını artırdı: TWDM 4–8 kanal + PtP WDM",
               "G.989.2 ışığı, G.989.3 bitleri tanımlar: 125 µs çerçeveler / zamanlanmış burst'ler",
               "PMD tabloları S/R-CG'ye göre yazılmıştır (S/R-CP: alternatif, Ek XI)",
               "Hassasiyet, FEC öncesi BER referansına göre: 10G → 10⁻³, 2,5G → 10⁻⁴"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 22, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        for k, t0 in enumerate([self.cues[1], self.cues[5]]):
            self.at(t0)
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.05)
        self.beat("v2")
        for k, t0 in zip([2, 3, 4], [self.cues[0], self.cues[5], self.cues[7]]):
            self.at(t0)
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.15)

        self.beat("v3")
        self.clear()
        self.set_badge("ozet")
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("PMD tabloları hangi referans\nnoktasına göre yazılmıştır?\nNeden alternatif bir nokta var?", CH[0]),
            ("10G NG-PON2 alıcısının\nhassasiyeti hangi BER'de\nölçülür?", CH[1]),
            ("64 ONU'lu ağda kapalı\nvericilerin sızıntısı tabanı\nkaç dB yükseltir?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 2'nin başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, t0 in enumerate([self.cues[1], self.cues[4] - 0.4, self.cues[6] - 0.4]):
            self.at(t0)
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cues[8])
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # v3a — season map
        self.beat("v3a")
        self.clear()
        ttl = T("Sezon 1 haritası", 36, TXT, BOLD).move_to(UP * 2.55)
        eps = SERIES["episodes"]
        cards = VGroup()
        for e in eps:
            r = RoundedRectangle(corner_radius=0.14, width=2.45, height=1.55, stroke_color=ACC if e["n"] == 1 else LINE, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=1)
            t = VGroup(T(f"B{e['n']}", 18, ACC, BOLD), T(e["title"], 17, TXT, BOLD)).arrange(DOWN, buff=0.08).move_to(r)
            if t.width > 2.25:
                t.scale_to_fit_width(2.25)
            cards.add(VGroup(r, t))
        cards.arrange_in_grid(rows=2, cols=5, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        tick = T("✓", 30, GOOD, BOLD).next_to(cards[0][0].get_corner(UR), DL, buff=0.08)
        self.play(FadeIn(ttl), FadeIn(cards[0]), FadeIn(tick), run_time=0.6)
        times = [self.cues[0] + 2.0, self.cues[0] + 3.4, self.cues[0] + 4.8, self.cues[0] + 6.2, self.cues[1] if len(self.cues) > 1 else 9,
                 None, None, None, None]
        n = len(self.cues)
        tl = [self.cues[min(i, n - 1)] for i in range(n)]
        step = max(0.6, (self.bdur - 3.0) / 9)
        for k in range(1, 10):
            self.at(1.2 + step * (k - 1))
            self.play(FadeIn(cards[k], scale=0.9), run_time=0.45)
        self.end(pad=0.1)

        # v4 — next episode teaser + credits
        self.beat("v4")
        self.clear()
        self.drop_badge()
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T("Bölüm 2 · Işığın Yolu", 54, TXT, BOLD),
                     T("ODN · optik yol kaybı sınıfları · fiber mesafe · referans ODN", 22, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 0.9)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        sc = 0.3
        bar = VGroup(*[Rectangle(width=15 * sc, height=0.22, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([-1.9 + (lo - 14) * sc + 15 * sc / 2, -1.4 - 0.3 * i, 0])
                       for i, (lo, c) in enumerate([(14, CH[0]), (16, CH[1]), (18, CH[2]), (20, CH[3])])])
        bl = T("14 … 35 dB", 22, ACC, BOLD).next_to(bar, RIGHT, buff=0.3)
        self.at(self.cues[3])
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.2), FadeIn(bl), run_time=1.2)
        self.end(pad=0.6)
        self.play(FadeOut(VGroup(nxt, bar, bl)), FadeOut(self.hdr), run_time=0.7)
        # credits (silent)
        cr = VGroup(T("LAMBDA · Bölüm 1 · Işığa Dönüş", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Google Gemini TTS — ses: Sadaltager", 22, ACC, BOLD),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep01_end")
