"""B01 · Perde 5 — Hat hızları ve G.989.2'yi okumak."""
from kit import *

HDR5 = "BÖLÜM 1 · PERDE 5 — Hızlar ve G.989.2'yi okumak"
MAN5 = "build/v4/ep01_p5/audio_proc/manifest.json"


class P5A(Act):
    HDR, MANIFEST, FIRST = HDR5, MAN5, True

    def construct(self):
        self.beat("t1")
        tc = self.title_card("PERDE 5", "Hızlar ve G.989.2'yi okumak")
        self.at(self.cues[2] - 0.2)
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("İki nominal hat hızı")
        r1 = T("9,95328 Gbit/s", 50, WHITE, BOLD).move_to(UP * 0.8 + LEFT * 3.5)
        r2 = T("2,48832 Gbit/s", 50, GOLD, BOLD).move_to(UP * 0.8 + RIGHT * 3.5)
        self.at(self.cues[3] - 0.2)
        self.play(Write(r1), run_time=1.0)
        self.play(Write(r2), run_time=1.0)
        self.end(pad=0.05)

        self.beat("t2")
        f1 = T("= 64 × 155,52 Mbit/s  →  STM-64", 22, WHITE).next_to(r1, DOWN, buff=0.35)
        f2 = T("= 16 × 155,52 Mbit/s  →  STM-16", 22, GOLD).next_to(r2, DOWN, buff=0.35)
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.7)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.7)
        sdh = pill("SDH mirası", MUTED, 20).move_to(DOWN * 1.1)
        self.at(self.cues[3])
        self.play(FadeIn(sdh), run_time=0.5)
        k8 = T("hat hızı = 8 kHz'in katı   ⇒   1 / 8 kHz = 125 µs çerçeve", 28, ACC, BOLD).move_to(DOWN * 2.2)
        self.at(self.cues[5])
        self.play(Write(k8), self.set_src("G.989.2 §11.1.1"), run_time=1.2)
        self.end(pad=0.05)

        # t3 — Table 11-1
        self.beat("t3")
        self.clear(h)
        h = self.show_heading("Tablo 11-1: kanal başına hız seçenekleri", h)
        tb = table(["Seçenek", "Aşağı / yukarı (Gbit/s)", "Parametre tabloları"],
                   [["Temel hız", "9,95328 / 2,48832", "11-5 / 11-6"], ["Seçenek 1", "9,95328 / 9,95328", "11-5 / 11-7"], ["Seçenek 2", "2,48832 / 2,48832", "11-4 / 11-6"]],
                   [2.6, 4.6, 3.6], size=24, hsize=19, row_h=0.72).move_to(UP * 0.2)
        self.play(FadeIn(tb[0]), run_time=0.5)
        for i, t0 in enumerate([self.cues[2], self.cues[5], self.cues[7]]):
            self.at(t0 - 0.1)
            self.play(FadeIn(tb[i + 1], shift=UP * 0.1), run_time=0.6)
        any_ = pill("kanal grubundaki her TWDM kanalı herhangi bir seçeneği kullanabilir", ACC, 19).next_to(tb, DOWN, buff=0.5)
        self.at(self.cues[9])
        self.play(FadeIn(any_, shift=UP * 0.1), self.set_src("G.989.2 §11.1.1, Tablo 11-1"), run_time=0.7)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p5A")


class P5B(Act):
    HDR, MANIFEST, PREV_BADGE = HDR5, MAN5, "std"

    def construct(self):
        self.beat("t4")
        self.set_badge("tc")
        h = self.show_heading("Çift hızlı yukarı yön kanalı")
        frame = Rectangle(width=12.0, height=1.0, stroke_color=MUTED, stroke_width=2).move_to(UP * 0.3)
        fl = T("bir yukarı yön PHY çerçevesi (125 µs)", 18, MUTED).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
        bursts, x = VGroup(), frame.get_left()[0] + 0.2
        for k, (w, fast) in enumerate([(1.4, True), (2.6, False), (1.1, True), (2.2, False), (1.6, True)]):
            c = WHITE if fast else GOLD
            bursts.add(Rectangle(width=w, height=0.7, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x + w / 2, frame.get_y(), 0]))
            x += w + 0.35
        lg = VGroup(VGroup(Square(0.25, fill_color=WHITE, fill_opacity=0.85, stroke_width=0), T("10 Gbit/s ONU", 18, WHITE)).arrange(RIGHT, buff=0.15),
                    VGroup(Square(0.25, fill_color=GOLD, fill_opacity=0.85, stroke_width=0), T("2,5 Gbit/s ONU", 18, GOLD)).arrange(RIGHT, buff=0.15)
                    ).arrange(RIGHT, buff=0.6).next_to(frame, DOWN, buff=0.3)
        self.at(self.cues[1] - 0.2)
        self.play(Create(frame), FadeIn(fl), run_time=0.6)
        self.at(self.cues[2])
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bursts], lag_ratio=0.25), FadeIn(lg), run_time=1.6)
        src = pill("G.989.3 Tablo 6-1, 4. satır: 9,95328 ↓ / 9,95328 + 2,48832 ↑", GOLD, 18).to_edge(DOWN, buff=0.7)
        self.at(self.cues[3])
        self.play(FadeIn(src, shift=UP * 0.1), self.set_src("G.989.3 §6.1.1"), run_time=0.6)
        self.end(pad=0.05)

        # t5 — rate follows channel
        self.beat("t5")
        self.clear(h)
        h = self.show_heading("NG-PON2'de hız, kanalın özelliğidir", h)
        tb = table(["ONU kombinasyonu", "↓ Gbit/s", "↑ Gbit/s"], [["1", "2,48832", "2,48832"], ["2", "9,95328", "2,48832"], ["3", "9,95328", "9,95328"]],
                   [2.8, 2.0, 2.0], size=22, hsize=17, row_h=0.6).move_to([-3.1, 0.2, 0])
        self.play(FadeIn(tb), self.set_src("G.989.3 Tablo 6-2"), run_time=0.8)
        ch2 = box(2.6, 0.7, "λ2 · 2,5/2,5", GOLD, 18).move_to([3.6, 1.0, 0])
        ch3 = box(2.6, 0.7, "λ3 · 10/10", WHITE, 18).move_to([3.6, -0.6, 0])
        onu = box(1.4, 0.6, "ONU", CH[1], 18).move_to([3.6, 0.2, 0]).shift(LEFT * 3.0 + RIGHT * 3.0)
        onu.next_to(ch2, LEFT, buff=0.4)
        self.at(self.cues[1])
        self.play(FadeIn(ch2), FadeIn(ch3), FadeIn(onu), run_time=0.6)
        self.play(onu.animate.next_to(ch3, LEFT, buff=0.4), run_time=1.2)
        rule = pill("ONU hangi kanala ayarlanırsa, o kanalın hızını konuşur", ACC, 20).to_edge(DOWN, buff=0.75)
        self.at(self.cues[2])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # t6 — scrambled NRZ
        self.beat("t6")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Hat kodu: karıştırılmış NRZ", h)
        rng = np.random.default_rng(12)
        bits = rng.integers(0, 2, 20)
        w = VMobject(color=CH[1], stroke_width=4).set_points_as_corners(nrz(bits, -6.2, 0.5, -1.0, 0.8, rise=0.05))
        bl = VGroup(*[T(str(b), 20, MUTED).move_to([-6.2 + 0.5 * i + 0.25, 1.25, 0]) for i, b in enumerate(bits)])
        hi = T("yüksek ışık\n= 1", 20, CH[1], BOLD).move_to([5.6, 0.8, 0])
        lo = T("düşük ışık\n= 0", 20, MUTED, BOLD).move_to([5.6, -1.0, 0])
        self.at(self.cues[1] - 0.3)
        self.play(Create(w), FadeIn(bl), run_time=1.6)
        self.at(self.cues[2])
        self.play(FadeIn(hi), run_time=0.4)
        self.at(self.cues[3])
        self.play(FadeIn(lo), run_time=0.4)
        n = pill("göz diyagramı ve sönüm oranı ölçümlerinin temeli → Bölüm 4", ACC, 19).to_edge(DOWN, buff=0.75)
        self.at(self.cues[4])
        self.play(FadeIn(n, shift=UP * 0.1), self.set_src("G.989.2 §11.1.2"), run_time=0.6)
        self.end(pad=0.05)

        # t7 + t7a — clock accuracy
        self.beat("t7")
        self.clear(h)
        h = self.show_heading("Saat doğruluğu", h)
        ax = Line([-5.2, -2.2, 0], [-5.2, 1.9, 0], color=MUTED, stroke_width=2)
        steps = [("Stratum-1", "1 × 10⁻¹¹ · normalde izlenebilir referans", 1.6, ACC),
                 ("Stratum-3", "zamanlamaya duyarlı uygulamalar", 0.0, GOLD),
                 ("Stratum-4", "3,2 × 10⁻⁵ ≈ ±32 ppm · serbest çalışmada en az", -1.6, WARN)]
        lv = VGroup()
        for name, desc, y, c in steps:
            d = Dot([-5.2, y, 0], color=c, radius=0.1)
            lv.add(VGroup(d, T(name, 24, c, BOLD).next_to(d, RIGHT, buff=0.3), T(desc, 18, TXT).next_to(d, RIGHT, buff=2.4)))
        up = T("daha doğru ↑", 16, MUTED).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), FadeIn(up), run_time=0.5)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(lv[0], shift=RIGHT * 0.2), self.set_src("G.989.2 §11.1.1.1–11.1.1.2"), run_time=0.7)
        self.at(self.cues[4] - 0.2)
        self.play(FadeIn(lv[2], shift=RIGHT * 0.2), run_time=0.7)
        onu = pill("ONU ↑ frekans doğruluğu = aldığı ↓ sinyalinki", CH[1], 19).to_edge(DOWN, buff=0.7)
        self.at(self.cues[6])
        self.play(FadeIn(onu, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("t7a")
        self.play(FadeIn(lv[1], shift=RIGHT * 0.2), run_time=0.7)
        self.at(self.cues[1])
        self.play(Indicate(lv[1], color=GOLD, scale_factor=1.05), run_time=0.9)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p5B")


DOC = [("§6", "Mimari · yol kaybı ve fiber mesafe sınıfları", ACC, "n"), ("§9", "Ortak gereksinimler: dalga boyu planı, PMD tanımları,\nayar özellikleri, kanal dışı PSD maskesi", ACC, "n"),
       ("§10", "Girişim/sinyal (X/S) toleransı", ACC, "n"), ("§11", "TWDM PMD tabloları (11-4 … 11-7) · yukarı yön ek yükü", ACC, "n"),
       ("Ek A", "Ayarlanabilir PtP WDM PMD", GOLD, "n"), ("Ek B", "AMCC", GOLD, "n"), ("Ek C", "Düşük kayıplı PtP WDM PMD", GOLD, "n"), ("Ek D", "ONU güç dengeleme", GOLD, "n"),
       ("Ek I", "Eski sistemlerle dalga boyu değerlendirmesi", MUTED, "i"), ("Ek II", "Optik katman izleme ölçümleri", MUTED, "i"), ("Ek III", "PHY ek yük zamanı", MUTED, "i"),
       ("Ek IV", "Jitter bütçesi", MUTED, "i"), ("Ek V", "OLT burst edinim süresi ve göz açıklığı ölçümü", MUTED, "i"), ("Ek VI", "Raman etkileşimleri", MUTED, "i"),
       ("Ek VII", "Döngüsel AWG ızgara örnekleri", MUTED, "i"), ("Ek VIII", "WM, kanal arası girişim, ayar süresi", MUTED, "i"), ("Ek IX", "Raman için alternatif hat kodu", MUTED, "i"),
       ("Ek X", "Yukarı yön PMD örnekleri", MUTED, "i"), ("Ek XI", "S/R-CP parametreleri", MUTED, "i")]


def doc_map():
    rows = VGroup()
    for k, desc, c, kind in DOC:
        tag = RoundedRectangle(corner_radius=0.08, width=1.05, height=0.36, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.18 if kind == "n" else 0.05)
        if kind == "i":
            tag = DashedVMobject(tag, num_dashes=24)
        t = T(k, 15, TXT, BOLD).move_to(tag)
        d = T(desc, 15, TXT if kind == "n" else MUTED, line_spacing=0.85)
        rows.add(VGroup(VGroup(tag, t), d))
    for r in rows:
        r[1].next_to(r[0], RIGHT, buff=0.18)
    left = VGroup(*rows[:8]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    right = VGroup(*rows[8:]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to(DOWN * 0.45)
    return rows, left, right


class P5C(Act):
    HDR, MANIFEST, PREV_BADGE = HDR5, MAN5, "std"

    def construct(self):
        self.beat("t8")
        h = self.show_heading("G.989.2'nin haritası")
        rows, left, right = doc_map()
        self.at(self.cues[1] - 0.2)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.15), run_time=0.6)
        self.at(self.cues[3])
        self.play(FadeIn(rows[1], shift=RIGHT * 0.15), run_time=0.6)
        self.end(pad=0.05)
        self.beat("t9")
        self.play(FadeIn(rows[2], shift=RIGHT * 0.15), run_time=0.6)
        self.at(self.cues[1])
        self.play(FadeIn(rows[3], shift=RIGHT * 0.15), run_time=0.5)
        self.play(Indicate(rows[3][1], color=ACC, scale_factor=1.06), run_time=0.6)
        self.end(pad=0.05)
        self.beat("t10")
        nl = T("normatif (bağlayıcı)", 16, GOLD, BOLD).next_to(rows[4][0], LEFT, buff=0.2).shift(LEFT * 0.0)
        self.at(self.cues[1] - 0.2)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[4:8]], lag_ratio=0.3), run_time=2.0)
        il = T("bilgilendirici", 16, MUTED, BOLD).next_to(right, UP, buff=0.12).align_to(right, LEFT)
        nl2 = T("normatif", 16, GOLD, BOLD).next_to(left, UP, buff=0.12).align_to(left, LEFT)
        self.play(FadeIn(nl2), run_time=0.3)
        self.at(self.cues[7])
        self.play(FadeIn(il), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[8:]], lag_ratio=0.1), run_time=2.2)
        q = T("“This appendix does not form an integral part of this Recommendation.”", 16, MUTED, slant=ITALIC).to_edge(DOWN, buff=0.45).shift(RIGHT * 1.5)
        self.at(self.cues[10])
        self.play(FadeIn(q), run_time=0.6)
        self.end(pad=0.05)
        self.beat("t11")
        self.play(FadeOut(q), run_time=0.3)
        for i, idx in enumerate([13, 14, 15, 12]):
            self.at([self.cues[1], self.cues[2], self.cues[3], self.cues[3] + 1.6][i])
            self.play(rows[idx][0][0].animate.set_fill(GOOD, opacity=0.35).set_stroke(GOOD), rows[idx][1].animate.set_color(GOOD), run_time=0.5)
        tip = pill("test mühendisi için en değerli sayfaların bir kısmı burada", GOOD, 18).to_edge(DOWN, buff=0.45)
        self.at(self.cues[4])
        self.play(FadeIn(tip, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p5C")


ROWS_T = [("Çalışma bandı", "1596 – 1603 nm", "", "", ""), ("Kanal aralığı", "100 GHz", "", "", ""), ("Maks. spektral sapma", "±20 GHz", "", "", ""),
          ("Min. sönüm oranı", "8,2 dB", "", "", ""), ("Min. SMSR (S/R-CP)", "30 dB", "", "", ""),
          ("Ort. başlatma gücü min", "+3,0", "+5,0", "+7,0", "+9,0"), ("Ort. başlatma gücü maks", "+7,0", "+9,0", "+11,0", "+11,0"),
          ("Dispersiyon aralığı", "0–420 ps/nm (DD20) · 0–840 (DD40)", "", "", "")]
ROWS_R = [("BER referansı", "10⁻³", "", "", ""), ("Maks. OPP", "2,0 dB", "", "", ""),
          ("Hassasiyet (dBm)", "−28,0", "−28,0", "−28,0", "−28,0"), ("Aşırı yük (dBm)", "−7,0", "−7,0", "−7,0", "−9,0")]


def t115():
    W = [3.9, 1.6, 1.6, 1.6, 1.6]
    TW = sum(W)

    def row(cells, widths, fill, color=TXT, weight=MEDIUM, size=16, h=0.42):
        bg = Rectangle(width=TW, height=h, stroke_width=0, fill_color=fill, fill_opacity=1)
        g = VGroup(bg)
        x = -TW / 2
        for c, w in zip(cells, widths):
            t = T(c, size, color, weight)
            if t.width > w - 0.15:
                t.scale_to_fit_width(w - 0.15)
            t.move_to([x + 0.12, 0, 0], aligned_edge=LEFT)
            g.add(t)
            x += w
        return g

    def tb(rows, title, color):
        hdr = row([title, "N1", "N2", "E1", "E2"], W, "#16213A", MUTED, BOLD)
        hdr[1].set_color(color)
        body = []
        for i, (k, a, b, c, d) in enumerate(rows):
            fill = PANEL if i % 2 == 0 else "#0E1628"
            body.append(row([k, a], [W[0], TW - W[0]], fill) if not b else row([k, a, b, c, d], W, fill))
        return VGroup(hdr, *body).arrange(DOWN, buff=0)
    tx = tb(ROWS_T, "OLT vericisi (S/R-CG)", GOLD)
    rx = tb(ROWS_R, "ONU alıcısı (R/S)", CH[1])
    return VGroup(tx, rx).arrange(DOWN, buff=0.18)


class P5D(Act):
    HDR, MANIFEST, PREV_BADGE = HDR5, MAN5, "std"

    def construct(self):
        self.beat("t11a")
        h = self.show_heading("Bir tabloyu okumak: Tablo 11-5 (9,95328 Gbit/s ↓)")
        tab = t115().scale(0.8).move_to([-2.75, -0.75, 0])
        tx, rx = tab
        self.play(FadeIn(tx[0]), FadeIn(rx[0]), self.set_src("G.989.2 Tablo 11-5 (seçili satırlar)"), run_time=0.8)
        self.at(self.cues[2])
        self.play(Indicate(tx[0], color=GOLD, scale_factor=1.03), run_time=0.6)
        self.at(self.cues[3])
        self.play(Indicate(rx[0], color=CH[1], scale_factor=1.03), run_time=0.6)
        self.end(pad=0.05)

        self.beat("t11b")
        for i, t0 in enumerate([self.cues[1], self.cues[2], self.cues[3], self.cues[4], self.cues[5]]):
            self.at(t0 - 0.1)
            self.play(FadeIn(tx[1 + i], shift=UP * 0.08), run_time=0.45)
        smsr = tx[5]
        box_ = SurroundingRectangle(smsr, color=WARN, buff=0.03)
        nt = T("SMSR: CG değil, CP noktasında!", 18, WARN, BOLD).next_to(tab, RIGHT, buff=0.3).align_to(smsr, UP)
        self.at(self.cues[6])
        self.play(Create(box_), FadeIn(nt), run_time=0.7)
        self.end(pad=0.05)

        self.beat("t11c")
        self.play(FadeOut(box_), FadeOut(nt), run_time=0.3)
        self.play(FadeIn(tx[6], shift=UP * 0.08), run_time=0.5)
        self.at(self.cues[2])
        self.play(FadeIn(tx[7], shift=UP * 0.08), run_time=0.5)
        self.at(self.cues[5])
        self.play(FadeIn(rx[3], shift=UP * 0.08), run_time=0.5)
        self.at(self.cues[7])
        self.play(FadeIn(rx[1], shift=UP * 0.08), run_time=0.5)
        self.at(self.cues[8])
        self.play(FadeIn(rx[2], shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # t11d — closing the budget
        self.beat("t11d")
        opl = table(["Tablo 6-1 (yol kaybı)", "N1", "N2", "E1", "E2"], [["min / maks (dB)", "14 / 29", "16 / 31", "18 / 33", "20 / 35"]],
                    [3.9, 1.6, 1.6, 1.6, 1.6], size=16, hsize=16, row_h=0.42).scale(0.8).next_to(tab, UP, buff=0.12).align_to(tab, LEFT)
        self.play(FadeIn(opl, shift=DOWN * 0.1), run_time=0.6)
        calc = VGroup(T("+3,0", 26, GOLD, BOLD), T("− 29", 26, CH[1], BOLD), T("− 2,0", 26, MUTED, BOLD), T("= −28,0 dBm", 26, GOOD, BOLD)
                      ).arrange(RIGHT, buff=0.22).move_to([4.25, 0.9, 0])
        cl = VGroup(T("Pmin", 16, GOLD), T("OPLmaks", 16, CH[1]), T("OPP", 16, MUTED), T("= hassasiyet", 16, GOOD))
        for c, l in zip(calc, cl):
            l.next_to(c, UP, buff=0.08)
        hl = [SurroundingRectangle(tx[6][2], color=GOLD, buff=0.02), SurroundingRectangle(opl[1][2], color=CH[1], buff=0.02),
              SurroundingRectangle(rx[2][2], color=MUTED, buff=0.02), SurroundingRectangle(rx[3][2], color=GOOD, buff=0.02)]
        for i, t0 in enumerate([self.cues[2], self.cues[4], self.cues[6], self.cues[7]]):
            self.at(t0 - 0.1)
            self.play(FadeIn(calc[i], shift=LEFT * 0.1), FadeIn(cl[i]), Create(hl[i]), run_time=0.5)
        others = VGroup(*[T(s, 20, GOOD, BOLD) for s in ("N2: +5 − 31 − 2 = −28 ✓", "E1: +7 − 33 − 2 = −28 ✓", "E2: +9 − 35 − 2 = −28 ✓")]
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(calc, DOWN, buff=0.5)
        self.at(self.cues[9])
        self.play(LaggedStart(*[FadeIn(o, shift=LEFT * 0.15) for o in others], lag_ratio=0.3), run_time=1.4)
        clos = pill("kendi içinde kapanan bir güç bütçesi", GOOD, 17).next_to(others, DOWN, buff=0.35)
        self.at(self.cues[11])
        self.play(FadeIn(clos, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # t11e — overload check
        self.beat("t11e")
        self.play(FadeOut(VGroup(calc, cl, others, clos, *hl)), run_time=0.4)
        calc2 = VGroup(T("+7,0", 26, GOLD, BOLD), T("− 14", 26, CH[1], BOLD), T("= −7,0 dBm", 26, GOOD, BOLD)).arrange(RIGHT, buff=0.22).move_to([4.25, 0.9, 0])
        cl2 = VGroup(T("Pmaks", 16, GOLD), T("OPLmin", 16, CH[1]), T("= aşırı yük", 16, GOOD))
        for c, l in zip(calc2, cl2):
            l.next_to(c, UP, buff=0.08)
        hl2 = [SurroundingRectangle(tx[7][2], color=GOLD, buff=0.02), SurroundingRectangle(opl[1][2], color=CH[1], buff=0.02), SurroundingRectangle(rx[4][2], color=GOOD, buff=0.02)]
        self.play(FadeIn(rx[4], shift=UP * 0.08), run_time=0.5)
        self.at(self.cues[2] - 0.2)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c), FadeIn(l), Create(b)) for c, l, b in zip(calc2, cl2, hl2)], lag_ratio=0.4), run_time=1.6)
        e2 = T("E2: +11 − 20 = −9 ✓  (tablo: −9,0)", 20, GOOD, BOLD).next_to(calc2, DOWN, buff=0.5)
        hl3 = SurroundingRectangle(rx[4][5], color=GOOD, buff=0.02)
        self.at(self.cues[5])
        self.play(FadeIn(e2, shift=LEFT * 0.15), Create(hl3), run_time=0.8)
        tip = pill("satırları birbirine karşı doğrulayın", ACC, 19).next_to(e2, DOWN, buff=0.4)
        self.at(self.cues[7])
        self.play(FadeIn(tip), run_time=0.5)
        self.end(pad=0.05)

        # t11f — dispersion consistency
        self.beat("t11f")
        self.play(FadeOut(VGroup(calc2, cl2, e2, tip, hl3, *hl2)), run_time=0.4)
        hd = SurroundingRectangle(tx[8], color=ACC, buff=0.02)
        dc = VGroup(T("420 ps/nm ÷ 20 km", 28, ACC, BOLD), T("= 21 ps/nm/km", 30, ACC, BOLD), T("L bandında G.652 fiber ≈ 20–21", 18, MUTED),
                    T("Perde 2'deki D(λ) eğrisi, tabloda sayı olarak", 18, TXT)).arrange(DOWN, buff=0.18).move_to([4.2, 0.4, 0])
        self.at(self.cues[1])
        self.play(FadeIn(tx[8], shift=UP * 0.08), run_time=0.4)
        self.play(Create(hd), run_time=0.5)
        self.at(self.cues[3])
        self.play(FadeIn(dc[0]), FadeIn(dc[1]), run_time=0.8)
        self.at(self.cues[5])
        self.play(FadeIn(dc[2]), run_time=0.5)
        self.at(self.cues[6])
        self.play(FadeIn(dc[3]), run_time=0.5)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p5D")


class P5E(Act):
    HDR, MANIFEST, PREV_BADGE = HDR5, MAN5, "std"

    def construct(self):
        self.beat("t12")
        h = self.show_heading("Gözden kaçmaması gereken not (§6.3)")
        q = self.quote("G.989.2 §6.3", "“The following power spectral density (PSD) values in the PMD tables in clause 11 have been optimized\nfor TWDM 4-channel and 20 km. Investigations for TWDM 8 channel and/or DD40 (40 km) are for further study.”",
                       "§11'deki PSD değerleri 4 kanal ve 20 km için optimize · 8 kanal / 40 km: ileride çalışılacak", width=12.4).move_to(UP * 0.4)
        self.at(self.cues[1] - 0.2)
        self.play(FadeIn(q, shift=UP * 0.15), self.set_src("G.989.2 §6.3"), run_time=1.0)
        self.at(self.cues[3])
        self.play(Indicate(q[2], color=GOLD, scale_factor=1.03), run_time=0.8)
        self.end(pad=0.05)

        self.beat("t13")
        w = card("8 kanal ya da 40 km mı tasarlıyorsunuz?", "Tablodaki bazı değerler doğrudan geçerli olmayabilir.\nDipnotlar ve bu tür cümleler, tablolar kadar önemlidir.",
                 None, WARN, w=10.0, h=2.0, tsize=24).move_to(DOWN * 2.0)
        self.play(FadeIn(w, shift=UP * 0.2), run_time=0.8)
        self.end(pad=0.05)

        # t14 — versions
        self.beat("t14")
        self.clear(h)
        h = self.show_heading("Sürümler", h)
        ev = [("2014", "1. baskı"), ("2016", "Amd.1"), ("2017", "Amd.2"), ("2019", "2. baskı"), ("2019", "Cor.1"), ("2020", "Amd.1")]
        line = Line([-6.0, 0.6, 0], [6.0, 0.6, 0], color=MUTED, stroke_width=2)
        pts = VGroup()
        for i, (y, n) in enumerate(ev):
            x = -5.5 + i * 2.2
            c = ACC if i >= 3 else LEGACY
            pts.add(VGroup(Dot([x, 0.6, 0], color=c, radius=0.11), T(y, 18, c, BOLD).move_to([x, 1.05, 0]), T(n, 18, TXT if i >= 3 else MUTED).move_to([x, 0.15, 0])))
        self.play(Create(line), LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pts], lag_ratio=0.12), run_time=1.4)
        base = DashedVMobject(SurroundingRectangle(pts[3:], buff=0.2, corner_radius=0.12, color=ACC), num_dashes=60)
        bt = T("bu seri: 2. baskı + Cor.1 + Amd.1", 18, ACC, BOLD).next_to(base, UP, buff=0.08)
        self.at(self.cues[1])
        self.play(Create(base), FadeIn(bt), run_time=0.8)
        notes = VGroup(T("2. baskı: değişiklikler birleştirildi · bazı OOB/OOC girişim parametreleri gevşetildi", 18, TXT),
                       T("Cor.1: Tablo 10-1 — ONU alıcısı X/S parametreleri yenilendi", 18, TXT),
                       T("Amd.1: Ek D — güç dengeleme PSD değerleri güncellendi", 18, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(DOWN * 1.6)
        for i, t0 in enumerate([self.cues[3], self.cues[5], self.cues[6]]):
            self.at(t0 - 0.1)
            self.play(FadeIn(notes[i], shift=RIGHT * 0.15), run_time=0.6)
        self.play(self.set_src("G.989.2 (2019)/Amd.1 (10/2020) — Özet ve tarihçe"), run_time=0.3)
        self.at(self.cues[7])
        self.play(Indicate(base, color=ACC), run_time=0.8)
        self.end(pad=0.2)
        self.clear()
        self.drop_badge()
        self.save_timeline("ep01_p5E")
