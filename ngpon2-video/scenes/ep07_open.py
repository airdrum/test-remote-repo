"""B07 — 'Bu bölümde' opening + 'Önceki bölümde' recap (answers to the B06 quiz)."""
from ep07_common import *

AGENDA = ["Ayar: sınıflar, sapma, granülerlik", "Ayar sırasında spektrum: OOC + gevşeme",
          "Kalibrasyon: iç ayar ↔ dalga boyu", "Kanal yönetimi: devir, O8/O9, kilit",
          "Laboratuvar: ayar süresi, cırlama, sızıntı"]
PX, PY = 3.4, -0.45


class Ep07Open(Narrated):
    MANIFEST = M7("open")

    def q(self, sub, default):
        b = self.bmap[self.timeline[-1]["id"]]
        for c in b["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        return default

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP7['n']} · {tr_upper(EP7['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP7['n']:02d}", 120, ACC, BOLD)
        sub = T(EP7["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP7["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            fit(m, 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.at(self.q("rengini değiştirebilmesi", 11))
        grid = chan_cells(4, PX + 0.2, PY - 2.3, tgt=1)
        arr = arrow(grid[1].get_top() + UP * 0.1, grid[3].get_top() + UP * 0.1, TUNE, 3)
        self.play(FadeIn(grid), run_time=0.6)
        self.play(grid[1][0].animate.set_fill(MUTED, 0.25).set_stroke(MUTED), grid[1][1].animate.set_opacity(0.4),
                  grid[3][0].animate.set_fill(CH[3], 0.85).set_stroke(CH[3]), grid[3][1].animate.set_color(BG).set_opacity(1),
                  GrowArrow(arr), run_time=0.7)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(cover, grid, arr)

        # o2 — tuning classes
        self.beat("o2")
        cls = VGroup(pill("Sınıf 1 · < 10 µs", GOOD, 19), pill("Sınıf 2 · 10 µs – 25 ms", GOLD, 19),
                     pill("Sınıf 3 · 25 ms – 1 s", WARN, 19)).arrange(DOWN, buff=0.4).move_to([PX + 0.2, PY + 0.3, 0])
        cap = T("Tablo 9-2 · mekanizma dayatılmaz", 19, TUNE, BOLD).move_to([PX + 0.2, PY + 2.2, 0])
        self.focus(0, VGroup(cls, cap))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.4)
        self.at(self.q("üç sınıfa böler", 9))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cls], lag_ratio=0.25), run_time=1.0)
        self.end(pad=0.05)

        # o3 — spectrum during tuning
        self.beat("o3")
        axg, X = lin_axis(-250, 250, PX - 2.8, PX + 3.2, PY - 1.4, [-200, -100, 0, 100, 200], size=12, fmt=lambda v: tr(v), unit="GHz")
        lobes = VGroup(*[lobe(X, 100 * k, PY - 1.4, 1.2, 14, CH[(k + 2) % 4], op=0.3) for k in (-2, -1, 0, 1, 2)])
        sweep = arrow([X(-180), PY + 0.2, 0], [X(180), PY + 0.2, 0], TUNE, 3)
        swt = T("lazer süpürülürken", 15, TUNE, BOLD).next_to(sweep, UP, buff=0.08)
        cap = T("ayar anında: gevşetilmiş maske", 19, LEAK, BOLD).move_to([PX + 0.2, PY + 1.9, 0])
        self.focus(1, VGroup(axg, lobes, sweep, swt, cap))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(lobes), run_time=0.7)
        self.at(self.q("komşu kanallara ne yayar", 2))
        self.play(GrowArrow(sweep), FadeIn(swt), run_time=0.6)
        self.at(self.q("gevşetildiği", 7))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o4 — calibration
        self.beat("o4")
        o = np.array([PX - 2.3, PY - 1.6, 0])
        ax = VGroup(Line(o, o + [5.0, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 3.0, 0], color=MUTED, stroke_width=2))
        axl = VGroup(T("iç ayar", 14, MUTED).next_to(ax[0], RIGHT, buff=0.1), T("dalga boyu", 14, MUTED).next_to(ax[1], UP, buff=0.05))
        ln = Line(o + [0.3, 0.4, 0], o + [4.6, 2.7, 0], color=LOCK, stroke_width=3)
        dot = glow_dot(GOLD, 0.06, 3).move_to(o + [2.6, 1.65, 0])
        dl = T("kalibrasyon kaydı", 15, GOLD, BOLD).next_to(dot, UP, buff=0.15)
        cap = T("↓ otonom · ↑ OLT geri beslemesi", 18, ACC, BOLD).move_to([PX + 0.2, PY + 2.0, 0])
        self.focus(2, VGroup(ax, axl, ln, dot, dl, cap))
        self.play(Create(ax), FadeIn(axl), run_time=0.5)
        self.at(self.q("iç ayar değerinin", 1.5))
        self.play(Create(ln), FadeIn(dot), FadeIn(dl), run_time=0.7)
        self.at(self.q("OLT geri beslemesiyle", 11))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o5 — channel handover state machine
        self.beat("o5")
        st = VGroup(*[sbox(s, None, c, 1.5, 0.8, 22) for s, c in [("O5", GOOD), ("O8", GOLD), ("O9", TUNE)]]).arrange(RIGHT, buff=1.1).move_to([PX + 0.2, PY + 0.4, 0])
        ars = VGroup(arrow(st[0].get_right(), st[1].get_left(), MUTED), arrow(st[1].get_right(), st[2].get_left(), MUTED))
        sl = VGroup(T("hizmet", 13, GOOD).next_to(st[0], DOWN, buff=0.12), T("ayar-çıkış", 13, GOLD).next_to(st[1], DOWN, buff=0.12), T("ayar-giriş", 13, TUNE).next_to(st[2], DOWN, buff=0.12))
        cap = T("planlı devir + yeni kanala kilit", 19, ACC, BOLD).move_to([PX + 0.2, PY + 2.0, 0])
        self.focus(3, VGroup(st, ars, sl, cap))
        self.at(self.q("planlı devir", 3))
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in st], lag_ratio=0.25), FadeIn(sl), run_time=0.9)
        self.play(GrowArrow(ars[0]), GrowArrow(ars[1]), run_time=0.5)
        self.at(self.q("O-sekiz ve O-dokuz", 10))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        wm = instr("OSC", 2.1, 1.5, "1536,2 nm", "dalga boyu ölçer", TUNE).move_to([PX - 1.3, PY + 0.7, 0])
        osa = instrument("OSA", 2.1, 1.5).move_to([PX + 1.9, PY + 0.7, 0])
        cap = T("ayar süresi · cırlama · kanal dışı güç", 18, GOOD, BOLD).move_to([PX + 0.2, PY - 1.4, 0])
        self.focus(4, VGroup(wm, osa, cap))
        self.play(FadeIn(wm, shift=UP * 0.15), FadeIn(osa, shift=UP * 0.15), run_time=0.8)
        self.at(self.q("kanal dışı gücü", 5))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep07_open")

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


class Ep07Recap(Act7):
    HDR, MANIFEST, FIRST = "BÖLÜM 7 · ÖNCEKİ BÖLÜMDE", M7("recap"), True

    def construct(self):
        qa = [("Soru 1", "Ayar sırasında ONU'nun kanal dışı\ngüç maskesi neden gevşetilir?", CH[0], "a1", 2,
               [("lazer bir renkten diğerine süpürülür → arada kalan kanalları geçer", "arada kalan kanalların"),
                ("D eki: yasaklamak yerine sınırlı gevşeme", "D ekinde sınırlı"),
                ("ayar kısa + OLT koordineli → rahatsızlık sınırlı", "OLT tarafından koordine")]),
              ("Soru 2", "Ayar süresi neden tek değer değil,\nbir aralıkla tanımlanır?", CH[1], "a2", 1,
               [("süre mekanizmaya bağlı: ısıl yavaş, diğerleri hızlı", "mekanizmaya bağlıdır"),
                ("Tablo 9-2: C1 < 10 µs · C2 10 µs–25 ms · C3 25 ms–1 s", "Birinci sınıf on mikrosaniyenin"),
                ("aralık = aynı sınıfta farklı gerçeklemelere yer", "aynı sınıf içinde farklı")]),
              ("Soru 3", "Fiziksel ayar süresi ile TC ayar\nsüresi neden farklıdır?", CH[3], "a3", 1,
               [("fiziksel: yalnızca lazer / filtre oturması", "lazerin ya da filtrenin"),
                ("TC = hazırlık + fiziksel ayar + yeniden senkron", "üç parçanın toplamıdır"),
                ("ONU yeni kanalda senkron + atama alınca biter", "çerçeve senkronunu kurup")])]
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 6 · Patlama")
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
        self.save_timeline("ep07_recap")
