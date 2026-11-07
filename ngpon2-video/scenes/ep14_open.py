"""S2·B4 — 'Bu bölümde' opening + 'Önceki bölümde' recap with the answers to the S2·B3 quiz."""
from ep14_common import *

AGENDA = ["Kim, ne kadar: Alloc-ID ve tanımlayıcı", "DBA: rapor, izleme, referans model", "Gecikme: kuantum, yoklama, döngü",
          "Çekişme: Ek J, Ek K, sanal yığın", "Laboratuvarda: gecikme ve verim"]
PX, PY = 3.4, -0.45
CX = PX + 0.2
OWN = [ACC, GOLD, PINK]


class Ep14Open(Act14):
    MANIFEST, FIRST = M14("open"), True

    def construct(self):
        # o1 — title, agenda, cover; one upstream time axis shared by many ONUs
        self.beat("o1")
        tag_ = T(f"SEZON 2 · BÖLÜM {EP14['n']} · {tr_upper(EP14['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([CX, PY, 0])
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.0)
        s2 = pill("SEZON 2", GOLD, 18).move_to([CX, PY + 2.4, 0])
        num = T(f"{EP14['n']:02d}", 110, ACC, BOLD)
        sub = fit(T(EP14["sub"], 22, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP14["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.25).move_to([CX, PY + 1.05, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(s2), run_time=0.5)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.3)
        y = PY - 2.25
        ax = Line([CX - 2.95, y, 0], [CX + 2.95, y, 0], color=MUTED, stroke_width=2)
        axl = T("↑ tek zaman ekseni · bir TWDM kanalı", 15, MUTED, BOLD).next_to(ax, DOWN, buff=0.14)
        onus = VGroup(*[onu_box(f"ONU {i + 1}", ONUC, 1.05, 0.46, 15).move_to([CX - 2.35 + 1.25 * i, PY - 1.2, 0]) for i in range(3)])
        dba = sbox("OLT · DBA", None, OLTC, 1.45, 0.5, 16).move_to([CX + 2.15, PY - 1.2, 0])
        bx = [(-2.85, 0.7, 0), (-2.05, 0.45, 1), (-1.5, 0.9, 2), (-0.5, 0.55, 0), (0.15, 0.5, 2), (0.75, 1.0, 1), (1.85, 0.6, 0), (2.5, 0.35, 1)]
        bursts = VGroup(*[Rectangle(width=w, height=0.36, stroke_color=MUTED, stroke_width=1.6, fill_color=MUTED, fill_opacity=0.3)
                          .move_to([CX + x + w / 2, y + 0.2, 0]) for x, w, _ in bx])
        ar = VGroup(*[arrow(onus[o].get_bottom(), [bursts[k].get_x(), y + 0.4, 0], OWN[o], 1.6, 0.08) for k, (_, _, o) in enumerate(bx) if k in (0, 1, 2)])
        bm = arrow(dba.get_bottom(), [CX + 2.15, y + 0.42, 0], BWC, 2, 0.1)
        bml = T("BWmap", 14, BWC, BOLD).next_to(bm, RIGHT, buff=0.06)
        self.at(self.cue("Bir TWDM kanalının yukarı", 2.5))
        self.play(Create(ax), FadeIn(axl), run_time=0.6)
        self.at(self.cue("birçok ONU'nun ortak", 5.1))
        self.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.08) for o in onus], lag_ratio=0.2), LaggedStart(*[FadeIn(b) for b in bursts], lag_ratio=0.08), run_time=1.0)
        self.at(self.cue("o eksenin kime", 9.9))
        self.play(*[bursts[k].animate.set_fill(OWN[o], opacity=0.45).set_stroke(OWN[o]) for k, (_, _, o) in enumerate(bx)],
                  *[o[0].animate.set_stroke(OWN[i]) for i, o in enumerate(onus)], LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("kaynak tahsisi ve dinamik", 15.6))
        self.play(FadeIn(dba, shift=LEFT * 0.08), GrowArrow(bm), FadeIn(bml), run_time=0.6)
        self.at(self.cue("kısaca DBA", 19.8))
        self.play(Indicate(dba, color=ACC, scale_factor=1.1), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(s2, cover, ax, axl, onus, dba, bursts, ar, bm, bml)

        # o2 — who and how much: Alloc-ID / T-CONT tree, the descriptor bar, three timing parameters without values
        self.beat("o2")
        onu = onu_box("ONU", ONUC, 1.2, 0.5, 16).move_to([CX - 2.3, PY + 1.9, 0])
        al = VGroup(*[tile(s, ACC, 1.75, 0.42, 15, 0.15) for s in ("Alloc-ID 5", "Alloc-ID 1100", "Alloc-ID 1101")]).arrange(DOWN, buff=0.15)
        al.move_to([CX + 0.15, PY + 1.65, 0])
        tc = VGroup(tag("OMCC", OMC, 14), tag("T-CONT", SAC, 14), tag("T-CONT", SAC, 14))
        for t, a in zip(tc, al):
            t.next_to(a, RIGHT, buff=0.2)
        lk = VGroup(*[Line(onu.get_right(), a.get_left(), color=MUTED, stroke_width=1.6) for a in al])
        x0 = CX - 2.8
        bar = strip([(1.0, "sabit", FXC, 0.45), (1.4, "güvenceli", ASC, 0.4), (1.5, "güvencesiz", NAC, 0.35), (1.2, "en iyi çaba", BEC, 0.3)], x0, PY - 0.2, 0.5, 14)
        rm = DashedLine([x0 + 5.1, PY + 0.15, 0], [x0 + 5.1, PY - 0.55, 0], color=RMC, stroke_width=2.5)
        rml = T("en büyük", 14, RMC, BOLD).next_to(rm, UP, buff=0.04)
        bl = T("trafik tanımlayıcısı = akışın sözleşmesi", 15, MUTED, BOLD).next_to(bar, DOWN, buff=0.12).align_to(bar, LEFT)
        tp = VGroup(*[VGroup(tag(n, c, 16), T("= ?", 18, WARN, BOLD)).arrange(RIGHT, buff=0.12) for n, c in (("TJT", TJC), ("TBDT", TBC), ("TPST", TPC))]).arrange(RIGHT, buff=0.35)
        tp.move_to([CX, PY - 1.85, 0])
        tpl = T("zamanlama parametreleri · değer yok", 15, MUTED, BOLD).next_to(tp, DOWN, buff=0.12)
        self.focus(0, VGroup(onu, al, tc, lk, bar, rm, rml, bl, tp, tpl))
        self.play(FadeIn(onu), run_time=0.3)
        self.at(self.cue("tahsis kimlikleri", 1.7))
        self.play(LaggedStart(*[Create(l) for l in lk], lag_ratio=0.15), LaggedStart(*[FadeIn(a, shift=RIGHT * 0.08) for a in al], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("T-CONT'lar", 3.2))
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.06) for t in tc], lag_ratio=0.15), run_time=0.6)
        self.at(self.cue("trafik tanımlayıcısı", 6.0))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in bar], lag_ratio=0.15), Create(rm), FadeIn(rml), FadeIn(bl), run_time=1.0)
        self.at(self.cue("hiç değer vermediği", 8.7))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.08) for t in tp], lag_ratio=0.2), FadeIn(tpl), run_time=0.8)
        self.end(pad=0.05)

        # o3 — DBA methods, the four-level strict order, recommended targets
        self.beat("o3")
        ms = VGroup(*[tile(s, c, 1.95, 0.48, 15, 0.15) for s, c in (("durum raporlama", SRC), ("trafik izleme", TMC), ("iş birlikli", COC))]).arrange(RIGHT, buff=0.12)
        ms.move_to([CX, PY + 2.0, 0])
        steps = VGroup()
        for i, (s, c) in enumerate((("1 · sabit", FXC), ("2 · güvenceli", ASC), ("3 · güvencesiz", NAC), ("4 · en iyi çaba", BEC))):
            steps.add(tile(s, c, 2.3, 0.42, 15, 0.3).move_to([CX - 1.95 + i * 1.3, PY + 0.85 - i * 0.5, 0]))
        sl = T("katı öncelik sırası", 15, MUTED, BOLD).move_to([CX + 1.6, PY + 0.95, 0])
        tg = VGroup(*[pill(s, GOOD, 16) for s in ("durağan: %10", "geri gelme: 2 ms", "yakınsama: 6 ms")]).arrange(RIGHT, buff=0.12)
        fit(tg, 6.1).move_to([CX, PY - 1.95, 0])
        tgl = T("önerilen başarım hedefleri", 15, MUTED, BOLD).next_to(tg, UP, buff=0.12)
        self.focus(1, VGroup(ms, steps, sl, tg, tgl))
        self.at(self.cue("durum raporlama", 0.8))
        self.play(FadeIn(ms[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("trafik izleme ve", 2.2))
        self.play(FadeIn(ms[1], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue("iş birlikli yöntem", 3.6))
        self.play(FadeIn(ms[2], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue("referans modeli", 5.3))
        self.play(FadeIn(sl), FadeIn(steps[0], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("dört katlı", 7.8))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in steps[1:]], lag_ratio=0.25), run_time=0.8)
        self.at(self.cue("başarım hedefleri", 10.8))
        self.play(FadeIn(tgl), LaggedStart(*[FadeIn(t, shift=UP * 0.08) for t in tg], lag_ratio=0.2), run_time=0.8)
        self.end(pad=0.05)

        # o4 — delay and time: the quantum, polling cost, request-grant loop, mobile fronthaul
        self.beat("o4")
        q = VGroup(*[Rectangle(width=0.26, height=0.36, stroke_color=TIMC, stroke_width=1.4, fill_color=TIMC, fill_opacity=0.12 + 0.05 * (i % 2)) for i in range(16)]).arrange(RIGHT, buff=0)
        q.move_to([CX - 0.9, PY + 2.0, 0])
        ql = T("12,86 ns", 16, TIMC, BOLD).next_to(q, RIGHT, buff=0.2)
        pb = VGroup(hbar(CX - 2.9, PY + 0.95, 2.9, OVC, 0.4, 0.5), hbar(CX - 2.9, PY + 0.95, 5.8, OVC, 0.4, 0.0))
        pbl = T("yoklama burst'leri · ek yük", 15, MUTED, BOLD).next_to(pb, DOWN, buff=0.08).align_to(pb, LEFT)
        olt = ct_box("OLT", OLTC, 1.1, 0.46, 15).move_to([CX - 2.2, PY - 0.75, 0])
        o1 = ct_box("ONU", ONUC, 1.1, 0.46, 15).move_to([CX + 2.2, PY - 0.75, 0])
        lp = VGroup(CurvedArrow(o1.get_left() + UP * 0.1, olt.get_right() + UP * 0.1, angle=0.5, color=BWC, stroke_width=2.2, tip_length=0.12),
                    CurvedArrow(olt.get_right() + DOWN * 0.1, o1.get_left() + DOWN * 0.1, angle=0.5, color=GOLD, stroke_width=2.2, tip_length=0.12))
        lpl = VGroup(T("rapor", 14, BWC, BOLD).move_to([CX, PY - 0.2, 0]), T("tahsis", 14, GOLD, BOLD).move_to([CX, PY - 1.3, 0]))
        mf = VGroup(tag("CU", COC, 15), T("→", 18, MUTED, BOLD), tag("OLT", OLTC, 15), T("→", 18, MUTED, BOLD), tag("RU", COC, 15),
                    T("mobil ön taşıma", 15, COC, BOLD)).arrange(RIGHT, buff=0.15).move_to([CX, PY - 2.35, 0])
        self.focus(2, VGroup(q, ql, pb, pbl, olt, o1, lp, lpl, mf))
        self.at(self.cue("tahsisin ölçü birimi", 2.2))
        self.play(LaggedStart(*[FadeIn(c) for c in q], lag_ratio=0.04), FadeIn(ql), run_time=0.8)
        self.at(self.cue("yoklamanın bedeli", 4.0))
        self.play(FadeIn(pb[1]), GrowFromEdge(pb[0], LEFT), FadeIn(pbl), run_time=0.7)
        self.at(self.cue("istek ve tahsis döngüsü", 5.5))
        self.play(FadeIn(olt), FadeIn(o1), Create(lp[0]), FadeIn(lpl[0]), run_time=0.6)
        self.play(Create(lp[1]), FadeIn(lpl[1]), run_time=0.5)
        self.at(self.cue("mobil ön taşıma", 9.0))
        self.play(FadeIn(mf, shift=UP * 0.08), run_time=0.6)
        self.end(pad=0.05)

        # o5 — contention: one allocation shared by several ONUs, virtual stack, the 50 ms
        self.beat("o5")
        ca = tile("çekişmeli tahsis", GOLD, 2.3, 0.5, 16, 0.2).move_to([CX + 1.2, PY + 1.9, 0])
        cs = VGroup(*[onu_box(f"ONU {i + 1}", ONUC, 1.05, 0.42, 14).move_to([CX - 2.1, PY + 2.45 - 0.55 * i, 0]) for i in range(3)])
        ca_a = VGroup(*[arrow(o.get_right(), ca.get_left(), GOLD, 1.8, 0.09) for o in cs])
        stk = VGroup(*[Rectangle(width=1.5, height=0.42, stroke_color=STATE, stroke_width=2, fill_color=PANEL, fill_opacity=1) for _ in range(3)]).arrange(DOWN, buff=0)
        stk.move_to([CX - 1.2, PY - 1.0, 0])
        sl = VGroup(*[T(f"L = {i + 1}", 14, STATE, BOLD).next_to(stk[i], LEFT, buff=0.12) for i in range(3)])
        dots = VGroup(Dot(color=ACC, radius=0.09).move_to(stk[0]).shift(LEFT * 0.3), Dot(color=PINK, radius=0.09).move_to(stk[1]), Dot(color=GOLD, radius=0.09).move_to(stk[2]).shift(RIGHT * 0.3))
        stl = T("sanal yığın", 15, STATE, BOLD).next_to(stk, DOWN, buff=0.12)
        f50 = VGroup(pill("50 ms", WARN, 22), T("?", 30, WARN, BOLD)).arrange(RIGHT, buff=0.15).move_to([CX + 1.7, PY - 1.0, 0])
        self.focus(3, VGroup(ca, cs, ca_a, stk, sl, dots, stl, f50))
        self.at(self.cue("aynı tahsisi paylaştığı", 1.2))
        self.play(LaggedStart(*[FadeIn(o) for o in cs], lag_ratio=0.15), FadeIn(ca), LaggedStart(*[GrowArrow(a) for a in ca_a], lag_ratio=0.15), run_time=0.9)
        self.at(self.cue("sanal yığın", 6.6))
        self.play(FadeIn(stk), FadeIn(sl), FadeIn(stl), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("elli milisaniye", 9.2))
        self.play(FadeIn(f50, scale=0.9), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab: traffic generator, analyzer, OLT emulator; four measurements
        self.beat("o6")
        tg = tg_icon(1.85, 1.3, "Trafik üreteci").move_to([CX - 2.1, PY + 1.35, 0])
        pa = pa_icon(1.85, 1.3, "Analizör").move_to([CX, PY + 1.35, 0])
        em = emu_icon(1.85, 1.3, "OLT emülatörü").move_to([CX + 2.1, PY + 1.35, 0])
        ts = VGroup(*[tag(s, GOOD, 16) for s in ("gecikme", "verim", "aşırı yük", "yoklamanın bedeli")]).arrange(RIGHT, buff=0.15)
        fit(ts, 6.1).move_to([CX, PY - 1.25, 0])
        ref = VGroup(T("ölçüt:", 15, MUTED, BOLD), tag("referans model · §7.3", GOLD, 15)).arrange(RIGHT, buff=0.15).move_to([CX, PY - 0.3, 0])
        self.focus(4, VGroup(tg, pa, em, ts, ref))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("bir protokol analizörü", 2.8))
        self.play(FadeIn(pa, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("OLT emülatörüyle", 5.0))
        self.play(FadeIn(em, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("referans modele karşı", 8.0))
        self.play(FadeIn(ref, shift=UP * 0.08), run_time=0.4)
        for k, (key, d) in enumerate((("gecikme,", 11.4), ("verim,", 12.0), ("aşırı yük", 12.5), ("ve yoklamanın bedeli", 13.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(ts[k], shift=UP * 0.08), run_time=0.3)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep14_open")

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


class Ep14Recap(Act14):
    HDR, MANIFEST, FIRST = f"SEZON 2 · BÖLÜM {K14} · ÖNCEKİ BÖLÜMDE", M14("recap"), True

    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.2)

    def construct(self):
        # a1 — 1518 B Ethernet frame in one DS XGEM frame: PLI 1518, P 1520, 2 × 0x55, 1528 B, LF 1; preamble/SFD dropped, FCS kept
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Sezon 2 · Bölüm 3 · XGEM")
        self.at(self.cue("Birinci soru", 1.9))
        self.to_header(tc)
        self.set_badge("ozet")
        q1 = self.qhead(1, "1518 B'lık Ethernet çerçevesi tek XGEM çerçevesinde ↓: PLI, dolgu, toplam boy? Önsöze ne olur?", CH[0])
        y1 = 0.6
        x0 = -6.2
        eth = strip([(1.15, "önsöz 7 B", MUTED, 0.2), (0.6, "SFD", MUTED, 0.3), (8.2, "DA … yük … FCS · 1518 B", R10, 0.18)], x0, y1, 0.55, 16)
        fcs = Rectangle(width=0.7, height=0.55, stroke_color=GOOD, stroke_width=2.5).move_to([eth[2].get_right()[0] - 0.35, y1, 0])
        fl = T("Ethernet çerçevesi", 15, MUTED, BOLD).next_to(eth, UP, buff=0.08).align_to(eth, LEFT)
        y2 = -1.0
        xh = x0 + 1.75
        xg = strip([(1.25, "başlık 8 B", SAC, 0.55), (7.85, "yük · 1518 B", SAC, 0.14), (0.45, "", PADC, 0.55)], xh, y2, 0.6, 16)
        pad = VGroup(HX("55", 14, BG, BOLD), HX("55", 14, BG, BOLD)).arrange(DOWN, buff=0.02).move_to(xg[2])
        ar = arrow([eth[2].get_x(), y1 - 0.32, 0], [xg[1].get_x(), y2 + 0.36, 0], MUTED, 2.2, 0.12)
        pli = VGroup(T("PLI =", 18, PLIC, BOLD), HX("1518", 20, PLIC, BOLD)).arrange(RIGHT, buff=0.12).move_to([-2.2, -0.2, 0])
        bP = brace_lbl(VGroup(xg[1], xg[2]), "P = 4·⌈1518/4⌉ = 1520 B · 2 dolgu baytı 0x55", SAC, DOWN, 16)
        bT = BraceBetweenPoints([xg.get_left()[0], y2 - 0.95, 0], [xg.get_right()[0], y2 - 0.95, 0], DOWN, color=GOLD)
        bTl = VGroup(T("toplam 1528 B", 19, GOLD, BOLD), tag("LF = 1", LFC, 16)).arrange(RIGHT, buff=0.3).next_to(bT, DOWN, buff=0.06)
        drop = VGroup(xmark(VGroup(eth[0], eth[1]), WARN, 4), T("kapsüllemeden önce atılır", 15, WARN, BOLD).next_to(VGroup(eth[0], eth[1]), DOWN, buff=0.1))
        keep = T("FCS taşınır ✓", 15, GOOD, BOLD).next_to(fcs, UP, buff=0.08)
        self.play(FadeIn(q1, shift=RIGHT * 0.2), self.set_src("G.989.3 §9.1.2 · (9-1) · §9.4.1 · Şekil 9-5"), run_time=0.6)
        self.play(FadeIn(fl), FadeIn(eth, shift=RIGHT * 0.1), run_time=0.6)
        self.at(self.cue("Gösterge bin beş yüz", 10.7))
        self.play(GrowArrow(ar), FadeIn(xg[0]), FadeIn(xg[1]), FadeIn(pli, shift=LEFT * 0.08), run_time=0.8)
        self.at(self.cue("Yük dördün katına", 13.5))
        self.play(FadeIn(xg[2]), run_time=0.4)
        self.at(self.cue("beş beş yazılmış", 17.9))
        self.play(FadeIn(pad), FadeIn(bP), run_time=0.6)
        self.at(self.cue("Başlıkla toplam", 22.7))
        self.play(GrowFromCenter(bT), FadeIn(bTl[0]), run_time=0.6)
        self.at(self.cue("son parça biti bir", 26.4))
        self.play(FadeIn(bTl[1], shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("Önsöz ve sınırlayıcı", 28.0))
        self.play(Create(drop[0]), FadeIn(drop[1]), run_time=0.6)
        self.at(self.cue("denetim dizisi taşınır", 32.0))
        self.play(Create(fcs), FadeIn(keep, shift=DOWN * 0.06), run_time=0.5)
        self.end(pad=0.1)

        # a2 — 2.5G ONU, GrantSize 4 with DBRu: DBRu (380 units incl. the queued frame) + one 12 B idle XGEM frame
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "Kuyruğunda 1518 B olan 2,5G ONU, DBRu istenen 4 sözcüklük tahsiste ne gönderir?", CH[1])
        cw = 1.25
        ws = VGroup(*[Rectangle(width=cw, height=0.7, stroke_color=MUTED, stroke_width=2) for _ in range(4)]).arrange(RIGHT, buff=0).move_to([-3.4, 0.55, 0])
        g16 = brace_lbl(ws, "GrantSize 4 × 4 B = 16 B", MUTED, DOWN, 16)
        dbr = VGroup(Rectangle(width=cw, height=0.7, stroke_width=0, fill_color=BWC, fill_opacity=0.45).move_to(ws[0]), T("DBRu", 17, BG, BOLD).move_to(ws[0]))
        idl = VGroup(Rectangle(width=2 * cw, height=0.7, stroke_width=0, fill_color=IDC, fill_opacity=0.55).move_to(ws[1:3]), T("boş başlık 8 B", 16, TXT, BOLD).move_to(ws[1:3]),
                     Rectangle(width=cw, height=0.7, stroke_width=0, fill_color=IDC, fill_opacity=0.18).move_to(ws[3]), T("4 B", 16, TXT, BOLD).move_to(ws[3]))
        r12 = brace_lbl(ws[1:], "kalan 12 B < 16 B", GOLD, UP, 16)
        qf = VGroup(tile("1518 B", R10, 1.6, 0.5, 16, 0.2), T("kuyrukta", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.2).move_to([-3.4, -1.9, 0])
        nofr = VGroup(xmark(qf[0], WARN, 3), T("bölme yasak", 16, WARN, BOLD).next_to(qf, RIGHT, buff=0.25))
        p = apanel(5.2, 2.9, "Analizör · çözülen alanlar", ACC).move_to([3.5, 0.2, 0])
        rows = VGroup(kv("BufOcc", "380 birim", kw=1.9), kv("Port-ID", "65535 = 0xFFFF", kw=1.9), kv("PLI", "4", kw=1.9),
                      kv("KI", "0", kw=1.9), kv("LF", "1", kw=1.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows.move_to(p[0]).shift(DOWN * 0.2)
        rows[0][1].set_color(BWC)
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.3 §8.1.1.2.4 · §8.1.2.2.1 · §9.1.4 · §9.3"), run_time=0.6)
        self.at(self.cue("rapor isteyen dört sözcüklük", 7.9))
        self.play(Create(ws), FadeIn(g16), FadeIn(qf), run_time=0.8)
        self.at(self.cue("Önce DBRu", 13.0))
        self.play(FadeIn(dbr), FadeIn(p), run_time=0.5)
        self.at(self.cue("üç yüz seksen birimi", 14.5))
        self.play(FadeIn(rows[0], shift=RIGHT * 0.06), Indicate(qf[0], color=BWC), run_time=0.6)
        self.at(self.cue("Kalan on iki bayt", 18.1))
        self.play(FadeIn(r12), run_time=0.5)
        self.at(self.cue("bölme yasaktır", 21.0))
        self.play(Create(nofr[0]), FadeIn(nofr[1]), run_time=0.5)
        self.at(self.cue("tek bir boş çerçeveyle", 22.3))
        self.play(FadeIn(idl), run_time=0.6)
        for k, (key, d) in enumerate((("port kimliği altmış", 27.1), ("gösterge dört", 30.9), ("anahtar indeksi sıfır", 32.1), ("son parça biti bir", 33.9))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.06), run_time=0.35)
        self.end(pad=0.1)

        # a3 — idle PLI = 4 → next header 12 B ahead; (9-1) does not apply; short idle upstream only; DS BIP pitfall
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "PLI = 4 olan boş çerçeveden sonraki başlık kaç bayt ileride? Dört sıfır baytı neden yalnızca ONU gönderir?", CH[3])
        y = 0.55
        x0 = -6.0
        u = 0.28
        st = strip([IH_(8 * u, "boş başlık · 8 B"), IP_(4 * u, "4 B"), H_(8 * u, "sonraki başlık"), P_(1.2, "")], x0, y, 0.6, 16)
        hp = hop(st[0].get_left()[0] + 0.05, st[2].get_left()[0], y + 0.32, GOLD, 2.5, -0.8)
        hpl = T("12 B", 20, GOLD, BOLD).next_to(hp, UP, buff=0.04)
        nf = VGroup(T("boş çerçeve: PLI = gerçek yük boyu", 17, TXT, BOLD), VGroup(T("(9-1) yuvarlaması", 16, MUTED, BOLD), T("uygulanmaz", 16, WARN, BOLD)).arrange(RIGHT, buff=0.15))
        nf.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.9, y + 0.05, 0])
        si = VGroup(HX("00 00 00 00", 22, TXT, BOLD), tag("kısa boş · yalnızca ↑", PADC, 16)).arrange(RIGHT, buff=0.3).move_to([-3.2, -1.0, 0])
        ds = strip([FS_(0.6, "HL"), FS_(0.9, "BWmap", BWC), FS_(0.9, "PLOAM", PLDC, 0.25), (2.6, "FS yükü", PAYC, 0.12), FS_(0.7, "BIP", BIPC, 0.4)], -6.0, -2.35, 0.55, 15)
        dl = T("↓ FS çerçevesi", 15, MUTED, BOLD).next_to(ds, UP, buff=0.08).align_to(ds, LEFT)
        bipg = glow(ds[4], WARN, 0.05)
        xp = VGroup(tag("XG-PON ONU", ONUC, 16), VGroup(T("BIP'i kısa boş çerçeve sanar", 17, TXT, BOLD),
                                                         T("→ OLT ↓ yönde kısa boştan kaçınır", 17, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(RIGHT, buff=0.25)
        fit(xp, 6.2).next_to(ds, RIGHT, buff=0.35)
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.3 §9.1.3 · §9.1.4"), run_time=0.6)
        self.at(self.cue("on iki bayt ileridedir", 2.0))
        self.play(FadeIn(st[:2], shift=RIGHT * 0.08), run_time=0.5)
        self.play(FadeIn(st[2:], shift=RIGHT * 0.08), Create(hp), FadeIn(hpl), run_time=0.7)
        self.at(self.cue("gerçek yük boyudur", 7.5))
        self.play(FadeIn(nf[0], shift=LEFT * 0.08), run_time=0.5)
        self.at(self.cue("yuvarlama formülüne uymaz", 10.5))
        self.play(FadeIn(nf[1], shift=LEFT * 0.08), run_time=0.5)
        self.at(self.cue("Dört sıfır bayt", 13.7))
        self.play(FadeIn(si[0], shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("yalnızca yukarı yönde vardır", 16.7))
        self.play(FadeIn(si[1], shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("OLT ondan kaçınır", 19.4))
        self.play(FadeIn(dl), FadeIn(ds), run_time=0.5)
        self.at(self.cue("BIP kuyruğunu", 23.0))
        self.play(Create(bipg), FadeIn(xp, shift=LEFT * 0.08), run_time=0.6)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep14_recap")
