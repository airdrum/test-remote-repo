"""B05 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to the B04 quiz."""
from ep05_common import *

AGENDA = ["Bütçe: hassasiyet, aşırı yük, OPP", "X/S toleransı: kalabalıkta duymak",
          "Zaman: saat, CID, titreşim, ayar", "Senkron, FEC ve ilk adımlar", "Laboratuvar: BER eğrisi, OPP, X/S"]
PX, PY = 3.4, -0.45


class Ep05Open(Narrated):
    MANIFEST = M5("open")

    def q(self, sub, default):
        b = self.bmap[self.timeline[-1]["id"]]
        for c in b["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        return default

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP5['n']} · {tr_upper(EP5['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP5['n']:02d}", 120, ACC, BOLD)
        sub = T(EP5["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP5["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            fit(m, 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.at(self.q("sekiz renk", 6))
        ear = VGroup(*[Line([PX - 1.97 + i * 0.6, PY - 2.55, 0], [PX - 1.97 + i * 0.6, PY - 2.0, 0], color=TW_DS, stroke_width=4) for i in range(8)])
        pick = SurroundingRectangle(ear[3], color=GOOD, buff=0.1, stroke_width=3)
        self.play(LaggedStart(*[Create(l) for l in ear], lag_ratio=0.08), run_time=0.8)
        self.play(ear[3].animate.set_color(GOOD).set_stroke(width=7), Create(pick), run_time=0.5)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(cover, ear, pick)

        # o2 — receiver side of the budget
        self.beat("o2")
        axg, X = lin_axis(-34, -4, PX - 2.6, PX + 3.0, PY - 1.1, [-30, -20, -10], size=13, unit="alınan güç (dBm)")
        w25 = Rectangle(width=X(-10) - X(-30), height=0.42, stroke_width=0, fill_color=TW_DS, fill_opacity=0.75).move_to([(X(-10) + X(-30)) / 2, PY + 0.55, 0])
        w10 = Rectangle(width=X(-7) - X(-28), height=0.42, stroke_width=0, fill_color=GOOD, fill_opacity=0.75).move_to([(X(-7) + X(-28)) / 2, PY - 0.2, 0])
        l25 = T("2,5G  −30 … −10 dBm", 15, BG, BOLD).move_to(w25)
        l10 = T("10G  −28 … −7 dBm", 15, BG, BOLD).move_to(w10)
        sens = T("hassasiyet", 16, GOLD, BOLD).next_to(w25, UP, buff=0.12).align_to(w25, LEFT)
        ovl = T("aşırı yük", 16, GOLD, BOLD).next_to(w25, UP, buff=0.12).align_to(w10, RIGHT)
        cap = T("her sınıfta aynı pencere", 22, GOOD, BOLD).move_to([PX + 0.2, PY + 1.75, 0])
        pl = VGroup(pill("OPP", ACC, 16), pill("BER referansı", ACC, 16)).arrange(RIGHT, buff=0.3).move_to([PX + 0.2, PY - 2.35, 0])
        self.focus(0, VGroup(axg, w25, w10, l25, l10, sens, ovl, cap, pl))
        self.play(Create(axg[0]), FadeIn(axg[1:]), run_time=0.6)
        self.at(self.q("hassasiyet", 1.8))
        self.play(GrowFromEdge(w25, LEFT), FadeIn(l25), FadeIn(sens), run_time=0.6)
        self.at(self.q("aşırı yük", 2.7))
        self.play(GrowFromEdge(w10, LEFT), FadeIn(l10), FadeIn(ovl), run_time=0.6)
        self.at(self.q("yol cezası", 3.5))
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("Ve neden", 6))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o3 — X/S
        self.beat("o3")
        axg, X = lin_axis(-260, 260, PX - 2.8, PX + 3.2, PY - 1.0, [-200, -100, 0, 100, 200], size=13, unit="C'ye göre (GHz)")
        tgt = lobe(X, 0, PY - 1.0, 1.3, 9, SIG, op=0.35)
        nb = VGroup(*[lobe(X, s * (80 + 100 * k), PY - 1.0, 2.05, 9, XC, op=0.25) for s in (-1, 1) for k in (0, 1)])
        st = T("S", 20, SIG, BOLD).next_to(tgt, UP, buff=0.08)
        xt = T("X = S + 4 dB", 16, XC, BOLD).move_to([X(130), PY + 1.35, 0])
        old = T("Y = S + 6 dB", 20, MUTED, BOLD)
        new = T("S + 7 dB", 20, GOOD, BOLD)
        fix = VGroup(old, Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=MUTED, stroke_width=2.5), new, pill("Cor.1", GOLD, 15)).arrange(RIGHT, buff=0.2).move_to([PX + 0.2, PY + 1.95, 0])
        strike = Line(old.get_left(), old.get_right(), color=WARN, stroke_width=3)
        self.focus(1, VGroup(axg, tgt, nb, st, xt, fix, strike))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(tgt), FadeIn(st), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in nb], lag_ratio=0.15), FadeIn(xt), run_time=0.9)
        self.at(self.q("birinci düzeltmenin", 4.4))
        self.play(FadeIn(old), run_time=0.4)
        self.play(Create(strike), FadeIn(fix[1:], shift=LEFT * 0.1), run_time=0.7)
        self.end(pad=0.05)

        # o4 — time
        self.beat("o4")
        bits = [1, 0, 1, 1, 0, 1] + [0] * 14 + [1, 0, 1]
        tb = 5.6 / len(bits)
        x0 = PX - 2.6
        sig = VMobject(stroke_color=TW_DS, stroke_width=3).set_points_as_corners(nrz(bits, x0, tb, PY + 0.75, PY + 1.45))
        run = Rectangle(width=14 * tb, height=0.95, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.12).move_to([x0 + (6 + 7) * tb, PY + 1.1, 0])
        rt = T("ardışık özdeş rakamlar: 72 bit", 16, GOLD, BOLD).next_to(run, DOWN, buff=0.1)
        lax, LX = log_axis(1e4, 1e8, PX - 2.4, PX + 2.8, PY - 2.2, [(1e5, "100 kHz"), (1e6, "1 MHz"), (1e7, "10 MHz")], size=12)
        yA, yB = PY - 0.75, PY - 1.85
        mask = VMobject(stroke_color=ACC, stroke_width=3).set_points_as_corners([[LX(1e4), yA, 0], [LX(4e5), yA, 0], [LX(4e6), yB, 0], [LX(1e8), yB, 0]])
        ml = VGroup(T("0,75 UIpp", 13, ACC, BOLD).next_to([LX(1e4), yA, 0], UP, buff=0.06, aligned_edge=LEFT),
                    T("0,075 UIpp", 13, ACC, BOLD).next_to([LX(1e8), yB, 0], UP, buff=0.06, aligned_edge=RIGHT))
        tun = pill("ayar adımı ≤ 5 GHz", PINK, 15).move_to([PX + 1.85, PY - 0.75, 0])
        self.focus(2, VGroup(sig, run, rt, lax, mask, ml, tun))
        self.play(Create(sig), run_time=0.8)
        self.at(self.q("ardışık özdeş", 2.0))
        self.play(FadeIn(run), FadeIn(rt), run_time=0.5)
        self.at(self.q("titreşim toleransı", 3.8))
        self.play(Create(lax[0]), FadeIn(lax[1:]), Create(mask), FadeIn(ml), run_time=0.8)
        self.play(FadeIn(tun), run_time=0.4)
        self.end(pad=0.05)

        # o5 — TC bridge
        self.beat("o5")
        names = [("Av", -1.5, 0.95), ("Ön senkron", 1.5, 0.95), ("Senkron", 1.5, -0.35), ("Yeniden\nsenkron", -1.5, -0.35)]
        bx = VGroup(*[sbox(n, None, STATE, 2.1, 0.8, 18).move_to([PX + 0.2 + x, PY + y, 0]) for n, x, y in names])
        ar = VGroup(arrow(bx[0].get_right(), bx[1].get_left(), STATE), arrow(bx[1].get_bottom(), bx[2].get_top(), STATE),
                    arrow(bx[2].get_left() + UP * 0.12, bx[3].get_right() + UP * 0.12, STATE), arrow(bx[3].get_right() + DOWN * 0.12, bx[2].get_left() + DOWN * 0.12, STATE),
                    arrow(bx[3].get_top(), bx[0].get_bottom(), WARN))
        lods = T("LODS", 15, WARN, BOLD).next_to(ar[4], LEFT, buff=0.1)
        fl = VGroup(pill("FEC", GOLD, 16), pill("O1.1 → O1.2 → O2-3", ACC, 16)).arrange(RIGHT, buff=0.3).move_to([PX + 0.2, PY - 1.75, 0])
        self.focus(3, VGroup(bx, ar, lods, fl))
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in bx], lag_ratio=0.2), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in ar[:4]], lag_ratio=0.15), run_time=0.7)
        self.at(self.q("senkron kaybı", 2.0))
        self.play(GrowArrow(ar[4]), FadeIn(lods), run_time=0.5)
        self.at(self.q("çerçevenin içindeki", 3.0))
        self.play(FadeIn(fl[0], shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(fl[1], shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        voa = instrument("VOA", 1.9, 1.4).move_to([PX - 1.3, PY + 0.75, 0])
        bert = instr("BERT", 1.9, 1.4, "BER 1,0E-3", "FEC öncesi", GOOD).move_to([PX + 1.7, PY + 0.75, 0])
        o = np.array([PX - 2.2, PY - 2.3, 0])
        axl = VGroup(Line(o, o + [4.6, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 1.6, 0], color=MUTED, stroke_width=2))
        pts = [o + [0.4 + 0.9 * k, 1.35 - 0.28 * k, 0] for k in range(5)]
        dots = VGroup(*[Dot(p, radius=0.06, color=GOLD) for p in pts])
        ln = Line(pts[0] + (pts[0] - pts[-1]) * 0.08, pts[-1] + (pts[-1] - pts[0]) * 0.08, color=GOLD, stroke_width=2.5)
        cap = T("BER eğrisi · OPP · X/S", 20, GOOD, BOLD).move_to([PX + 0.2, PY + 2.1, 0])
        self.focus(4, VGroup(voa, bert, axl, dots, ln, cap))
        self.play(FadeIn(voa, shift=UP * 0.15), FadeIn(bert, shift=UP * 0.15), run_time=0.7)
        self.play(Create(axl), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), run_time=0.8)
        self.at(self.q("yol cezasını", 2.4))
        self.play(Create(ln), FadeIn(cap), run_time=0.6)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep05_open")

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


class Ep05Recap(Act5):
    HDR, MANIFEST, FIRST = "BÖLÜM 5 · ÖNCEKİ BÖLÜMDE", M5("recap"), True

    def construct(self):
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 4 · Kaynak")
        self.at(1.2)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["OLT: PON'un saati — Stratum-1'e izlenebilir", "Güç penceresi 4 dB · sönüm oranı ≥ 8,2 dB",
               "SMSR · bant dışı / kanal dışı PSD · göz maskesi", "125 µs çerçeve: PSBd · FEC · karıştırma · TOL"]
        items = check_list(pts, 23, buff=0.4).move_to(DOWN * 0.2)
        keys = ["saat", "güç penceresi", "spektral sınırlar", "göz maskesi"]
        for k, key in enumerate(keys):
            self.at(self.q(key, 2 + 1.5 * k))
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.5)
        self.end(pad=0.05)
        self.clear()
        qa = [("Soru 1", "10G OLT · N1 · en küçük başlatma gücü:\nTOL alanında hangi sayı?", CH[0], "a2", 2,
               [("P_min = +3 dBm  ·  TOL: −30 dBm'den 0,1 dB adımlarla", "N1 sınıfında"), ("+3 − (−30) = 33 dB  →  330 adım", "otuz üç"),
                ("TOL = 330", "Cevap")]),
              ("Soru 2", "10G E2: en büyük güç ile 4 kanallı\nkanal dışı sınır arasındaki fark?", CH[1], "a3", 1,
               [("P_maks = +11 dBm  ·  kanal dışı sınır −34,5 dBm / 15 GHz", "en büyük güç"), ("fark = 45,5 dB", "Fark kırk"),
                ("SMSR 30 dB'nin üstü → çoklayıcının süzmesi", "Otuz desibellik")]),
              ("Soru 3", "2,5G aşağı yön çerçevesinde\nson kod sözcüğü neden kısa?", CH[3], "a4", 2,
               [("yük 38 856 B — 248'in tam katı değil", "iki buçuk gigabitlik"), ("156 × 248 B  +  168 B = 152 veri + 16 eşlik", "Yüz elli altı"),
                ("son veri bloğu: kodlamadan önce + 80 sanal sıfır bayt — gönderilmez", "Son veri bloğu")])]
        prev = None
        for title, qs, c, bid, hl, ans_lines in qa:
            self.beat(bid)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            qt = VGroup(T(title, 26, c, BOLD), T(qs, 28, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.25).to_edge(LEFT, buff=1.0)
            box_ = RoundedRectangle(corner_radius=0.18, width=11.6, height=2.5, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.45)
            lines = VGroup(*[T(s, 23, GOOD if k == hl else TXT, BOLD if k == hl else NORMAL) for k, (s, _) in enumerate(ans_lines)])
            at = VGroup(T("Cevap", 20, GOOD, BOLD), *lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            fit(at, 11.0)
            at.move_to(box_).align_to(box_, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(self.q(ans_lines[0][1], 1.0))
            self.play(FadeIn(box_), FadeIn(at[0]), FadeIn(lines[0], shift=UP * 0.1), run_time=0.6)
            for k in (1, 2):
                self.at(self.q(ans_lines[k][1], 4 + 4 * k))
                self.play(FadeIn(lines[k], shift=UP * 0.1), run_time=0.5)
            prev = VGroup(qt, box_, at)
            self.end(pad=0.1)
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep05_recap")
