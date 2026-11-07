"""B06 — 'Bu bölümde' opening + 'Önceki bölümde' recap (answers to the B05 quiz)."""
from ep06_common import *

AGENDA = ["Burst modu: açılma, kapanma, önsöz", "Karanlıkta güç: WNE-PSD ve maskeler",
          "Burst'ün şekli: göz, titreşim, SMSR", "TC köprüsü: PSBu, profil, FEC, harita",
          "Laboratuvar: kapılı göz, zamanlama, karanlık"]
PX, PY = 3.4, -0.45


class Ep06Open(Narrated):
    MANIFEST = M6("open")

    def q(self, sub, default):
        b = self.bmap[self.timeline[-1]["id"]]
        for c in b["cues"]:
            if sub in c["text"]:
                return max(0.0, c["t"] - 0.2)
        return default

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP6['n']} · {tr_upper(EP6['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP6['n']:02d}", 120, ACC, BOLD)
        sub = T(EP6["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP6["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            fit(m, 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX + 0.2, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.at(self.q("yanıp sönen", 12))
        # a row of ONUs; only one is transmitting (its burst "lit")
        onus = VGroup(*[Line([PX - 2.1 + i * 0.6, PY - 2.55, 0], [PX - 2.1 + i * 0.6, PY - 2.05, 0], color=MUTED, stroke_width=4) for i in range(8)])
        lit = SurroundingRectangle(onus[4], color=BURST, buff=0.1, stroke_width=3)
        self.play(LaggedStart(*[Create(l) for l in onus], lag_ratio=0.08), run_time=0.8)
        self.play(onus[4].animate.set_color(BURST).set_stroke(width=7), Create(lit), run_time=0.5)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(cover, onus, lit)

        # o2 — burst mode basics
        self.beat("o2")
        bw = {"g0": 0.4, "on": 0.45, "pre": 1.1, "dlm": 0.4, "pay": 2.1, "off": 0.45, "g1": 0.4}
        env, edges, xe = burst_env(PX - 2.8, PY - 1.6, PY + 0.4, BURST, widths=bw)
        axl = Line([PX - 2.8, PY - 1.6, 0], [xe + 0.1, PY - 1.6, 0], color=MUTED, stroke_width=2)
        labs = VGroup(seg_label(edges, "on", "açılma", GOOD, PY + 0.4, 13),
                      seg_label(edges, "pre", "önsöz", ACC, PY + 0.4, 14),
                      seg_label(edges, "dlm", "sınır.", GOLD, PY + 0.4, 12),
                      seg_label(edges, "off", "kapanma", WARN, PY + 0.4, 13))
        cap = T("sadece sıramızda: aç · gönder · kapat", 19, BURST, BOLD).move_to([PX + 0.2, PY + 1.6, 0])
        self.focus(0, VGroup(axl, env, labs, cap))
        self.play(Create(axl), FadeIn(env, shift=UP * 0.1), run_time=0.8)
        self.at(self.q("açılma ve kapanma", 6))
        self.play(FadeIn(labs), run_time=0.6)
        self.at(self.q("önsöz ile sınırlayıcı", 9.5))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o3 — dark power
        self.beat("o3")
        axg, X = lin_axis(-70, -30, PX - 2.8, PX + 3.0, PY - 1.1, [-62.6, -50, -40, -30], size=13, unit="güç yoğunluğu (dBm / 15 GHz)")
        floor = DashedLine([X(-62.6), PY - 1.1, 0], [X(-62.6), PY + 1.1, 0], color=LEAK, stroke_width=3)
        flab = T("WNE-PSD −62,6", 16, LEAK, BOLD).next_to(floor, UP, buff=0.1)
        leaks = VGroup(*[glow_dot(LEAK, 0.05, 3).move_to([PX - 2.2 + i * 0.5, PY + 0.4 + 0.12 * (i % 3), 0]) for i in range(8)])
        cap = T("kapalı verici bile sızdırır", 20, LEAK, BOLD).move_to([PX + 0.2, PY + 1.75, 0])
        self.focus(1, VGroup(axg, floor, flab, leaks, cap))
        self.play(Create(axg[0]), FadeIn(axg[1:]), run_time=0.6)
        self.at(self.q("sızdırdığı güç", 2))
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in leaks], lag_ratio=0.1), run_time=0.8)
        self.at(self.q("Etkin değilken", 5))
        self.play(Create(floor), FadeIn(flab), run_time=0.6)
        self.at(self.q("izin verilen bölge", 10))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o4 — burst shape
        self.beat("o4")
        e = eye(PX - 0.3, PY + 0.1, 3.0, 1.9, BURST, 0.12)
        mask = eye_mask(PX - 0.3, PY + 0.1, 3.0, 1.9, GOLD)
        cap = T("ilk bitinden temiz: göz · titreşim · SMSR", 18, GOLD, BOLD).move_to([PX + 0.2, PY + 1.75, 0])
        self.focus(2, VGroup(e, mask, cap))
        self.play(LaggedStart(*[Create(c) for c in e], lag_ratio=0.04), run_time=1.0)
        self.at(self.q("göz maskesi", 3))
        self.play(FadeIn(mask), run_time=0.6)
        self.at(self.q("yan mod", 6.5))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o5 — TC bridge
        self.beat("o5")
        psb = sbox("PSBu", "önsöz + sınırlayıcı", STATE, 3.0, 0.95, 22, 16).move_to([PX - 1.1, PY + 0.75, 0])
        prof = sbox("burst profili", "OLT seçer", ACC, 2.8, 0.95, 20, 16).move_to([PX + 2.0, PY + 0.75, 0])
        fec = pill("yukarı yön FEC: RS(248,216)", GOLD, 16).move_to([PX - 0.4, PY - 0.5, 0])
        bmap = pill("bant genişliği haritası = zamanlama", BURST, 16).move_to([PX + 0.1, PY - 1.4, 0])
        self.focus(3, VGroup(psb, prof, fec, bmap))
        self.play(FadeIn(psb, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("burst profili", 5))
        self.play(FadeIn(prof, shift=UP * 0.1), GrowArrow(arrow(psb.get_right(), prof.get_left(), MUTED)), run_time=0.5)
        self.at(self.q("hata düzeltmesi", 9))
        self.play(FadeIn(fec, shift=UP * 0.1), run_time=0.4)
        self.at(self.q("bant genişliği haritası", 11.5))
        self.play(FadeIn(bmap, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        dca = instrument("DCA", 2.2, 1.6).move_to([PX - 1.2, PY + 0.7, 0])
        pm = instr("PM", 2.2, 1.6, "−62,6 dBm", "karanlık · 15 GHz", LEAK).move_to([PX + 1.8, PY + 0.7, 0])
        cap = T("kapılı göz · zamanlama · karanlık güç", 19, GOOD, BOLD).move_to([PX + 0.2, PY - 1.4, 0])
        self.focus(4, VGroup(dca, pm, cap))
        self.play(FadeIn(dca, shift=UP * 0.15), FadeIn(pm, shift=UP * 0.15), run_time=0.8)
        self.at(self.q("karanlıktaki güç", 5))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep06_open")

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


class Ep06Recap(Act6):
    HDR, MANIFEST, FIRST = "BÖLÜM 6 · ÖNCEKİ BÖLÜMDE", M6("recap"), True

    def construct(self):
        qa = [("Soru 1", "10G ↓ · E2 sınıfında aşırı yük\nneden −9 dBm?", CH[0], "a1", 2,
               [("E2'de OLT P_maks = +11 dBm (E1 ile aynı tavan)", "en büyük başlatma"),
                ("en küçük yol kaybı 20 dB", "Yirmi desibellik"),
                ("+11 − 20 = −9 dBm  →  bir güç tavanının izi", "eksi dokuz")]),
              ("Soru 2", "2,5G ONU için S, X ve Z\ndüzeyleri nedir?", CH[1], "a2", 1,
               [("S = hassasiyet + OPP = −30 + 1 = −29 dBm", "yol cezası bir"),
                ("X = S + 4 = −25 dBm  (her TWDM girişimcisi)", "Her TWDM"),
                ("Z = S + 7 = −22 dBm  (noktadan noktaya ↓)", "noktadan noktaya")]),
              ("Soru 3", "Senkron ONU kaç kötü çerçeveden\nsonra senkron kaybı ilan eder?", CH[3], "a3", 2,
               [("önerilen M = 3", "Önerilen M"),
                ("3 ardışık çerçevede PSync / SFC doğrulaması başarısız", "üç ardışık"),
                ("→ SD_LOS ilan → arama (serial hunt) durumu", "arama durumuna")])]
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 5 · Alıcı")
        self.at(self.cue("geçen bölümün", 1.6))
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
            box_ = RoundedRectangle(corner_radius=0.18, width=11.6, height=2.5, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.45)
            lines = VGroup(*[T(s, 23, GOOD if k == hl else TXT, BOLD if k == hl else NORMAL) for k, (s, _) in enumerate(ans_lines)])
            at = VGroup(T("Cevap", 20, GOOD, BOLD), *lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            fit(at, 11.0)
            at.move_to(box_).align_to(box_, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(self.q(ans_lines[0][1], 2.0))
            self.play(FadeIn(box_), FadeIn(at[0]), FadeIn(lines[0], shift=UP * 0.1), run_time=0.6)
            for k in (1, 2):
                self.at(self.q(ans_lines[k][1], 6 + 6 * k))
                self.play(FadeIn(lines[k], shift=UP * 0.1), run_time=0.5)
            prev = VGroup(qt, box_, at)
            self.end(pad=0.1)
            first = False
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep06_recap")
