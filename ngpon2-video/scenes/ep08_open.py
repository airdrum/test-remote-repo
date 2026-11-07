"""B08 — 'Bu bölümde' opening + 'Önceki bölümde' recap (answers to the B07 quiz)."""
from ep08_common import *

AGENDA = ["OLT burst alıcısı: kilit + dinamik aralık", "Önsöz ekonomisi: gard / önsöz / sınırlayıcı",
          "Güç dengeleme: aralığı daraltmak", "İlk adımlar: sessiz pencere, mesafe ölçümü",
          "Laboratuvar: edinim, göz, dinamik aralık"]
PX, PY = 3.4, -0.45


class Ep08Open(Narrated):
    MANIFEST = M8("open")

    def q(self, sub, default):
        b = self.bmap[self.timeline[-1]["id"]]
        for c in b["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        return default

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP8['n']} · {tr_upper(EP8['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP8['n']:02d}", 120, ACC, BOLD)
        sub = T(EP8["sub"], 22, TXT, SEMIBOLD)
        refs = T(EP8["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            fit(m, 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.at(self.q("tek tek dinleyen", 13))
        olt = sbox("OLT", "alıcı", RX, 1.6, 0.85, 22, 15).move_to([PX + 2.4, PY - 1.0, 0])
        train, edges, xe = burst_train(PX - 2.6, PY - 1.4, [0.95, 0.35, 0.7, 0.45], BURST, bw=0.6, gap=0.3)
        feed = VGroup(*[arrow([e[1], PY - 1.4 + 0.1, 0], olt.get_left(), MUTED, 1.5, 0.08) for e in edges[::2]])
        self.play(FadeIn(olt), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in train], lag_ratio=0.15), run_time=1.0)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(cover, olt, train)

        # o2 — OLT burst receiver, dynamic range
        self.beat("o2")
        train, edges, xe = burst_train(PX - 2.8, PY - 1.3, [0.95, 0.3, 0.7, 0.45, 0.85], BURST, bw=0.6, gap=0.35)
        axl = Line([PX - 2.8, PY - 1.3, 0], [xe + 0.1, PY - 1.3, 0], color=MUTED, stroke_width=2)
        dr = DoubleArrow([PX + 2.6, PY - 1.3, 0], [PX + 2.6, PY - 0.35, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12)
        drt = VGroup(T("≈ 21 dB", 17, GOLD, BOLD), T("dinamik aralık", 13, GOLD)).arrange(DOWN, buff=0.05).next_to(dr, RIGHT, buff=0.12)
        cap = T("her burst'te güce + faza sıfırdan kilit", 18, RX, BOLD).move_to([PX + 0.2, PY + 1.7, 0])
        self.focus(0, VGroup(axl, train, dr, drt, cap))
        self.play(Create(axl), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in train], lag_ratio=0.12), run_time=1.0)
        self.at(self.q("sıfırdan kilitlenmek", 2))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.q("dinamik aralığı kaldırmak", 8))
        self.play(GrowFromCenter(dr), FadeIn(drt), run_time=0.6)
        self.end(pad=0.05)

        # o3 — preamble economy
        self.beat("o3")
        bw = {"g0": 0.4, "on": 0.3, "pre": 1.3, "dlm": 0.5, "pay": 2.2, "off": 0.3, "g1": 0.4}
        env, edges, xe = burst_env(PX - 2.8, PY - 1.4, PY + 0.3, BURST, widths=bw)
        axl = Line([PX - 2.8, PY - 1.4, 0], [xe + 0.1, PY - 1.4, 0], color=MUTED, stroke_width=2)
        labs = VGroup(seg_label(edges, "g0", "gard", MUTED, PY + 0.3, 13),
                      seg_label(edges, "pre", "önsöz", ACC, PY + 0.3, 14),
                      seg_label(edges, "dlm", "sınır.", GOLD, PY + 0.3, 12))
        cap = T("Tplo = gard + önsöz + sınırlayıcı", 18, BURST, BOLD).move_to([PX + 0.2, PY + 1.7, 0])
        self.focus(1, VGroup(axl, env, labs, cap))
        self.play(Create(axl), FadeIn(env, shift=UP * 0.1), run_time=0.8)
        self.at(self.q("gard,", 2))
        self.play(FadeIn(labs), run_time=0.5)
        self.at(self.q("kaç bit olması", 6))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o4 — power leveling
        self.beat("o4")
        axg, X = lin_axis(-28, -2, PX - 2.8, PX + 3.0, PY - 1.3, [-26, -16, -7], size=13, fmt=lambda v: tr(v), unit="OLT'de alınan güç (dBm)")
        wide = DoubleArrow([X(-26), PY + 0.2, 0], [X(-7), PY + 0.2, 0], buff=0, color=WARN, stroke_width=2.5, tip_length=0.12)
        widet = T("geniş aralık", 14, WARN, BOLD).next_to(wide, UP, buff=0.06)
        narrow = DoubleArrow([X(-26), PY - 0.5, 0], [X(-15), PY - 0.5, 0], buff=0, color=GOOD, stroke_width=2.5, tip_length=0.12)
        narrowt = T("dengelenmiş: daralmış", 14, GOOD, BOLD).next_to(narrow, DOWN, buff=0.06)
        red = VGroup(arrow([X(-7), PY + 0.55, 0], [X(-15), PY + 0.55, 0], GOOD, 3), T("yakın ONU −12 dB", 15, GOOD, BOLD).move_to([X(-11), PY + 0.95, 0]))
        cap = T("vericinin nezaketi → alıcının işi kolay", 18, RX, BOLD).move_to([PX + 0.2, PY + 1.9, 0])
        self.focus(2, VGroup(axg, wide, widet, narrow, narrowt, red, cap))
        self.play(Create(axg[0]), FadeIn(axg[1:]), GrowFromCenter(wide), FadeIn(widet), run_time=0.7)
        self.at(self.q("gücünü kısarak", 2))
        self.play(GrowArrow(red[0]), FadeIn(red[1]), run_time=0.5)
        self.at(self.q("daraltması", 6))
        self.play(GrowFromCenter(narrow), FadeIn(narrowt), FadeIn(cap, shift=DOWN * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # o5 — activation: quiet window
        self.beat("o5")
        yb = PY - 0.6
        tl = Line([PX - 2.8, yb, 0], [PX + 3.0, yb, 0], color=MUTED, stroke_width=2)
        busy1 = Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=BURST, fill_opacity=0.5).move_to([PX - 1.9, yb + 0.27, 0])
        busy2 = Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=BURST, fill_opacity=0.5).move_to([PX + 2.0, yb + 0.27, 0])
        qw = Rectangle(width=1.8, height=0.7, stroke_color=GOOD, stroke_width=2.5, fill_color=GOOD, fill_opacity=0.12).move_to([PX + 0.1, yb + 0.35, 0])
        qwt = T("sessiz pencere", 15, GOOD, BOLD).next_to(qw, UP, buff=0.1)
        new = T("yeni ONU: seri no + mesafe ölçümü", 16, GOLD, BOLD).next_to(qw, DOWN, buff=0.5).set_x(PX + 0.2)
        cap = T("yanlış anda konuşan = kekeme ONU savunması", 17, WARN, BOLD).move_to([PX + 0.2, PY + 1.9, 0])
        self.focus(3, VGroup(tl, busy1, busy2, qw, qwt, new, cap))
        self.play(Create(tl), FadeIn(busy1), FadeIn(busy2), run_time=0.5)
        self.at(self.q("sessiz pencere,", 1))
        self.play(FadeIn(qw), FadeIn(qwt), run_time=0.5)
        self.at(self.q("mesafe ölçümü", 4))
        self.play(FadeIn(new, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("kekeme ONU savunması", 10))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        dca = instrument("DCA", 2.1, 1.5).move_to([PX - 1.3, PY + 0.7, 0])
        em = VGroup(sbox("ONU #1", "aşırı yük", NEAR, 1.9, 0.7, 16, 12), sbox("ONU #2", "hassasiyet", FAR, 1.9, 0.7, 16, 12)).arrange(DOWN, buff=0.25).move_to([PX + 1.9, PY + 0.7, 0])
        cap = T("edinim süresi · göz · dinamik aralık · burst BER", 17, GOOD, BOLD).move_to([PX + 0.2, PY - 1.4, 0])
        self.focus(4, VGroup(dca, em, cap))
        self.play(FadeIn(dca, shift=UP * 0.15), FadeIn(em, shift=UP * 0.15), run_time=0.8)
        self.at(self.q("hata oranını", 6))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep08_open")

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


class Ep08Recap(Act8):
    HDR, MANIFEST, FIRST = "BÖLÜM 8 · ÖNCEKİ BÖLÜMDE", M8("recap"), True

    def construct(self):
        qa = [("Soru 1", "OLT burst alıcısı her yeni burst'e\nne kadar hızlı kilitlenmeli?", CH[0], "a1", 2,
               [("kilit önsöz boyunca: önce güç, sonra saat fazı", "önsözü boyunca"),
                ("bütçe: G.989.2 Ek III — önsöz zamanı", "üçüncü ekinde"),
                ("ölçüm: Ek V (G.987.2'ye atıfla)", "beşinci ekte")]),
              ("Soru 2", "Burst modu göz açıklığı neden\nsürekli moddan farklı ölçülür?", CH[1], "a2", 1,
               [("her burst farklı ONU gücü/fazı → yeniden kilit", "yeniden kilitlenir"),
                ("göz ancak kilit sonrası + gövdede anlamlı", "burst'ün gövdesi boyunca"),
                ("ölçüm önsözden sonra gövdeye kapılanır", "gövdeye kapılanır")]),
              ("Soru 3", "Güç dengeleme neden gereklidir?", CH[3], "a3", 1,
               [("en yakın/uzak ONU arası ~15 dB diferansiyel yol kaybı", "on beş desibele varan"),
                ("burst'ler aşırı yük–hassasiyet arası farklı güçte gelir", "aşırı yük ile hassasiyet"),
                ("yakın ONU'yu ≤ 12 dB kısıp aralığı daralt", "on iki desibele kadar")])]
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 7 · Renk Değiştiren Lazer")
        self.at(self.cue("Geçen bölümün", 1.6))
        self.to_header(tc)
        self.set_badge("ozet")
        prev = None
        first = True
        for title, qs, c, bid, hl, ans_lines in qa:
            if not first:
                self.beat(bid)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            qt = VGroup(T(title, 26, c, BOLD), T(qs, 28, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.25).to_edge(LEFT, buff=1.0)
            box_ = RoundedRectangle(corner_radius=0.18, width=11.8, height=2.5, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.45)
            lines = VGroup(*[T(s, 22, GOOD if k == hl else TXT, BOLD if k == hl else NORMAL) for k, (s, _) in enumerate(ans_lines)])
            at = VGroup(T("Cevap", 20, GOOD, BOLD), *lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            fit(at, 11.2)
            at.move_to(box_).align_to(box_, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(self.q(ans_lines[0][1], 2.0))
            self.play(FadeIn(box_), FadeIn(at[0]), FadeIn(lines[0], shift=UP * 0.1), run_time=0.6)
            for k in (1, 2):
                self.at(self.q(ans_lines[k][1], 7 + 7 * k))
                self.play(FadeIn(lines[k], shift=UP * 0.1), run_time=0.5)
            prev = VGroup(qt, box_, at)
            self.end(pad=0.1)
            first = False
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep08_recap")
