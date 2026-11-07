"""S2·B2 — 'Bu bölümde' opening + 'Önceki bölümde' recap with the answers to the S2·B1 quiz."""
from ep12_common import *

AGENDA = ["PSBd ve senkron makinesi", "Koruma: FEC · karıştırıcı · HEC", "Aşağı yön çerçevesi ve BWmap",
          "Yukarı yön burst'ü", "Laboratuvarda: altın vektörler"]
PX, PY = 3.4, -0.45
CX = PX + 0.2


class Ep12Open(Act12):
    MANIFEST, FIRST = M12("open"), True

    def construct(self):
        # o1 — title, agenda, cover
        self.beat("o1")
        tag_ = T(f"SEZON 2 · BÖLÜM {EP12['n']} · {tr_upper(EP12['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([CX, PY, 0])
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        s2 = pill("SEZON 2", GOLD, 18).move_to([CX, PY + 2.4, 0])
        num = T(f"{EP12['n']:02d}", 110, ACC, BOLD)
        sub = fit(T(EP12["sub"], 22, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP12["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.25).move_to([CX, PY + 0.95, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(s2), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        rng = np.random.default_rng(12)
        bits = "".join("1" if v else "0" for v in rng.integers(0, 2, 40))
        bc = bitcells(bits, 5.6, 0.3, ACC).move_to([CX, PY - 1.3, 0])
        bl = T("ışığın taşıdığı bitler", 15, MUTED, BOLD).next_to(bc, UP, buff=0.1)
        fr = strip([(0.8, "PSBd", PHC, 0.6), (4.8, "çerçeve", FSC, 0.18)], CX - 2.8, PY - 2.25, 0.5, 15)
        tl = VGroup(tile("Fiziksel uyarlama", PHC, 2.7, 0.44, 16, 0.18), tile("Çerçeveleme", FSC, 2.7, 0.44, 16, 0.18)).arrange(RIGHT, buff=0.2).move_to([CX, PY - 2.25, 0])
        self.at(self.cue("ışığın taşıdığı bitleri", 2.6))
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(c) for c in bc], lag_ratio=0.02), run_time=1.0)
        self.at(self.cue("fiziksel uyarlamayı ve", 7.8))
        self.play(FadeIn(tl, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("bit bit açıyoruz", 10.9))
        self.play(FadeOut(tl), FadeIn(fr, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(s2, cover, bc, bl, fr)

        # o2 — PSBd and sync
        self.beat("o2")
        psb = fields([("PSync", 64, PSC), ("SFC", 64, SFCC), ("OC", 64, OCC)], 5.8, 0.6, 18, 14, unit=" bit").move_to([CX, PY + 1.6, 0])
        pl = T("PSBd · 24 bayt", 16, GOLD, BOLD).next_to(psb, UP, buff=0.12)
        sub2 = VGroup(T("sayaç · 51 bit", 15, SFCC, BOLD).move_to(psb[1][0].get_center() + DOWN * 0.75),
                      T("kimlik + güç", 15, OCC, BOLD).move_to(psb[2][0].get_center() + DOWN * 0.75))
        st = VGroup(*[tile(s, STATE, 1.25, 0.46, 15, 0.18) for s in ("Av", "Ön senk.", "Senkron", "Yen. senk.")]).arrange(RIGHT, buff=0.22).move_to([CX, PY - 1.4, 0])
        sa = VGroup(*[Arrow(st[i].get_right(), st[i + 1].get_left(), buff=0.02, color=MUTED, stroke_width=2, tip_length=0.1,
                            max_tip_length_to_length_ratio=0.5) for i in range(3)])
        stl = T("ONU kilitlenmesi", 15, STATE, BOLD).next_to(st, UP, buff=0.12)
        self.focus(0, VGroup(psb, pl, sub2, st, sa, stl))
        self.play(FadeIn(pl), run_time=0.3)
        self.at(self.cue("altmış dört bitlik senkron", 2.3))
        self.play(FadeIn(psb[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("süper çerçeve sayacı", 5.2))
        self.play(FadeIn(psb[1], shift=UP * 0.1), FadeIn(sub2[0]), run_time=0.4)
        self.at(self.cue("kimlik ve güç bilgisi", 9.0))
        self.play(FadeIn(psb[2], shift=UP * 0.1), FadeIn(sub2[1]), run_time=0.4)
        self.at(self.cue("nasıl kilitlendiği", 12.5))
        self.play(FadeIn(stl), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in st], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in sa], lag_ratio=0.2), run_time=1.0)
        self.end(pad=0.05)

        # o3 — protection layers
        self.beat("o3")
        sh = VGroup(*[sbox(a, b, c, 1.9, 1.0, 18, 14) for a, b, c in (("RS FEC", "248 B sözcük", PARC), ("Karıştırıcı", "x⁵⁸ + x³⁹ + 1", PHC), ("HEC", "13 bit", HECC))]).arrange(RIGHT, buff=0.15)
        sh.move_to([CX, PY + 1.3, 0])
        q = T("hangisi neyi korur — neyi korumaz?", 17, ACC, BOLD).move_to([CX, PY + 0.15, 0])
        pr = VGroup(T("PSBd:", 17, GOLD, BOLD), tag("FEC yok", WARN, 16), tag("karıştırılmaz", WARN, 16)).arrange(RIGHT, buff=0.18).move_to([CX, PY - 1.2, 0])
        self.focus(1, VGroup(sh, q, pr))
        self.at(self.cue("Reed Solomon", 2.0))
        self.play(FadeIn(sh[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("karıştırıcı ve", 3.8))
        self.play(FadeIn(sh[1], shift=UP * 0.1), run_time=0.35)
        self.at(self.cue("başlık hata denetimi", 5.0))
        self.play(FadeIn(sh[2], shift=UP * 0.1), run_time=0.35)
        self.at(self.cue("Hangisi neyi korur", 6.9))
        self.play(FadeIn(q), run_time=0.4)
        self.at(self.cue("ve neyi korumaz", 8.5))
        self.play(FadeIn(pr, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # o4 — downstream frame inside, time quantum
        self.beat("o4")
        x0 = CX - 2.9
        fs = strip([(0.45, "HL", HLC, 0.3), (1.2, "BWmap", BWC, 0.3), (1.05, "PLOAM", PLDC, 0.25), (2.7, "yük", PAYC, 0.15), (0.4, "BIP", BIPC, 0.3)], x0, PY + 1.45, 0.55, 15)
        fl = T("↓ FS çerçevesi", 15, MUTED, BOLD).next_to(fs, UP, buff=0.1)
        tq = VGroup(T("1 zaman kuantumu = 12,86 ns", 18, ACC, BOLD),
                    VGroup(tag("2,5G: 4 B", R25, 16), tag("10G: 16 B", R10, 16)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.18).move_to([CX, PY - 0.95, 0])
        self.focus(2, VGroup(fs, fl, tq))
        self.play(FadeIn(fl), FadeIn(fs[0]), run_time=0.4)
        self.at(self.cue("bant genişliği haritası", 3.0))
        self.play(FadeIn(fs[1], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("PLOAM bölmesi ve yük", 5.0))
        self.play(FadeIn(fs[2], shift=RIGHT * 0.1), FadeIn(fs[3], shift=RIGHT * 0.1), FadeIn(fs[4]), run_time=0.6)
        self.at(self.cue("iki hızı tek bir zaman", 6.8))
        self.play(FadeIn(tq, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # o5 — upstream burst
        self.beat("o5")
        x0 = CX - 2.6
        bu = strip([(0.8, "önsöz", PHC, 0.3), (0.5, "sın.", PHC, 0.65), (0.8, "başlık", HLC, 0.3), (0.75, "DBRu", BWC, 0.3),
                    (1.75, "yük", PAYC, 0.15), (0.6, "BIP", BIPC, 0.3)], x0, PY + 1.35, 0.55, 15)
        bl = T("↑ burst", 15, MUTED, BOLD).next_to(bu, UP, buff=0.1)
        pf = VGroup(*[tag(f"profil {i}", PHC, 15) for i in range(4)]).arrange(RIGHT, buff=0.15).move_to([CX, PY + 0.25, 0])
        cw = strip([(2.1, "216 B", PAYC, 0.15), (0.3, "", PARC, 0.45), (1.0, "kısa", PAYC, 0.15), (0.3, "", PARC, 0.45)], CX - 1.85, PY - 1.05, 0.5, 15)
        cwl = T("FEC: son kod sözcüğü kısalır", 15, PARC, BOLD).next_to(cw, DOWN, buff=0.12)
        self.focus(3, VGroup(bu, bl, pf, cw, cwl))
        self.play(FadeIn(bl), run_time=0.3)
        self.at(self.cue("önsöz ve sınırlayıcı", 2.1))
        self.play(FadeIn(bu[0], shift=RIGHT * 0.1), FadeIn(bu[1], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("burst profilleri", 3.9))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pf], lag_ratio=0.15), run_time=0.6)
        self.at(self.cue("ONU başlığı", 5.3))
        self.play(FadeIn(bu[2], shift=RIGHT * 0.1), run_time=0.3)
        self.at(self.cue("durum raporu ve", 6.3))
        self.play(FadeIn(bu[3:], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("burst sonunda nasıl kısaldığı", 8.4))
        self.play(FadeIn(cw, shift=UP * 0.1), FadeIn(cwl), run_time=0.6)
        self.end(pad=0.05)

        # o6 — lab with golden vectors
        self.beat("o6")
        pa = pa_icon(2.2, 1.45).move_to([CX - 1.4, PY + 1.1, 0])
        em = emu_icon(2.2, 1.45).move_to([CX + 1.4, PY + 1.1, 0])
        gv = VGroup(T("Ek IV · altın vektörler", 17, GOLD, BOLD),
                    VGroup(*[tag(f"IV.{i}", GOLD, 15) for i in range(1, 6)]).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.15).move_to([CX, PY - 1.3, 0])
        self.focus(4, VGroup(pa, em, gv))
        self.play(FadeIn(pa, shift=UP * 0.1), FadeIn(em, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("altın vektörleriyle", 1.8))
        self.play(FadeIn(gv, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep12_open")

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


DWL = [("1", "187,8", "0000"), ("2", "187,7", "0001"), ("3", "187,6", "0010"), ("4", "187,5", "0011"),
       ("5", "187,4", "0100"), ("6", "187,3", "0101"), ("7", "187,2", "0110"), ("8", "187,1", "0111")]
CHC = CH + ["#94A3B8"] * 4


class Ep12Recap(Act12):
    HDR, MANIFEST, FIRST = f"SEZON 2 · BÖLÜM {K12} · ÖNCEKİ BÖLÜMDE", M12("recap"), True

    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.2)

    def construct(self):
        # a1 — Alloc-ID 1022, GrantSize 0, PLOAMu
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Sezon 2 · Bölüm 1 · Işığın Dili")
        self.at(self.cue("Birinci soru", 1.9))
        self.to_header(tc)
        self.set_badge("ozet")
        q1 = self.qhead(1, "Alloc-ID 1022, GrantSize 0, PLOAMu = 1 olan bir tahsis nedir?", CH[0])
        al = fields([("Alloc-ID", 14, ACC), ("bayrak", 2, GOLD), ("StartTime", 16, MUTED), ("GrantSize", 16, ACC), ("", 3, MUTED), ("HEC", 13, MUTED)],
                    11.6, 0.55, 17, 14, show_w=False).move_to([0, 0.95, 0])
        v1 = VGroup(T("Alloc-ID =", 17, TXT, BOLD), HX("1022", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.12).move_to(al[0][0])
        v2 = VGroup(T("GrantSize =", 17, TXT, BOLD), HX("0", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.12).move_to(al[3][0])
        v3 = T("PLOAMu = 1", 15, GOLD, BOLD).next_to(al[1][0], DOWN, buff=0.12)
        al_l = T("BWmap tahsis yapısı", 15, MUTED, BOLD).next_to(al, UP, buff=0.1).align_to(al, LEFT)
        ans = pill("bant içi seri numarası (SN) tahsisi · yalnızca 10G ↑ ONU'lar", GOLD, 19).move_to([0, -0.3, 0])
        o10 = onu_box("ONU · 10G ↑", R10, 2.2, 0.62, 17).move_to([-4.6, -1.55, 0])
        o25 = onu_box("ONU · 2,5G ↑", R25, 2.2, 0.62, 17).move_to([-4.6, -2.55, 0])
        ok10 = T("cevap verir ✓", 17, GOOD, BOLD).next_to(o10, RIGHT, buff=0.25)
        no25 = T("cevap vermemeli ✗", 17, WARN, BOLD).next_to(o25, RIGHT, buff=0.25)
        hd = fields([("ONU-ID", 10, ACC), ("Ind", 9, MUTED), ("HEC", 13, MUTED)], 4.4, 0.55, 16, 14, show_w=False)
        pm = seg(0, 1.9, 0, PLC, "PLOAMu", 0.55, 0.2, 16)
        hdr_g = VGroup(hd, pm)
        pm.next_to(hd, RIGHT, buff=0)
        hdr_g.move_to([3.15, -1.55, 0])
        hv = HX("1023", 18, GOLD, BOLD).move_to(hd[0][0])
        hl = T("↑ FS başlığı · atanmamış ONU-ID 0x3FF", 15, MUTED, BOLD).next_to(hdr_g, DOWN, buff=0.12).align_to(hdr_g, LEFT)
        snm = T("Serial_Number_ONU", 15, PLC, BOLD).next_to(pm, UP, buff=0.1)
        self.play(FadeIn(q1, shift=RIGHT * 0.2), self.set_src("G.989.3 Tablo 6-5 · §8.1.1.2 · §8.1.2.1.1 · §12.1.5"), run_time=0.6)
        self.play(FadeIn(al_l), FadeIn(al), run_time=0.5)
        self.at(self.cue("tahsis kimliği bin yirmi iki", 3.0))
        self.play(FadeOut(al[0][1]), FadeIn(v1, scale=0.8), run_time=0.4)
        self.at(self.cue("boyutu sıfır olan", 5.5))
        self.play(FadeOut(al[3][1]), FadeIn(v2, scale=0.8), FadeIn(v3), run_time=0.5)
        self.at(self.cue("yalnızca on gigabit", 10.2))
        self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("bant içi bir seri numarası", 14.1))
        self.play(FadeIn(o10), FadeIn(ok10), run_time=0.5)
        self.at(self.cue("İki buçuk gigabitlik ONU'lar", 17.3))
        self.play(FadeIn(o25), FadeIn(no25), run_time=0.5)
        self.at(self.cue("henüz kimliği yoktur", 21.4))
        self.play(FadeIn(hd), run_time=0.4)
        self.at(self.cue("bin yirmi üçü kullanır", 28.1))
        self.play(FadeOut(hd[0][1]), FadeIn(hv, scale=0.8), FadeIn(hl), run_time=0.5)
        self.at(self.cue("seri numarası mesajını", 30.0))
        self.play(FadeIn(pm, shift=LEFT * 0.1), FadeIn(snm), run_time=0.5)
        self.end(pad=0.1)

        # a2 — PON-ID 0x12345673
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "PSBd'deki PON-ID 0x12345673 ise hangi aşağı yön kanalıdır?", CH[1])
        pf = fields([("yönetim etiketi · 28 bit", 28, ACC), ("DWLCH", 4, GOLD)], 8.4, 0.62, 18, 14, show_w=False).move_to([-1.9, 0.85, 0])
        hv = VGroup(HX("0x1234567", 22, ACC, BOLD), HX("3", 22, GOLD, BOLD))
        hv[0].next_to(pf[0][0], UP, buff=0.14)
        hv[1].next_to(pf[1][0], UP, buff=0.14)
        bin_ = HX("0011", 20, GOLD, BOLD).move_to(pf[1][0])
        lab_t = T("OLT'nin dokunmadan taşıdığı etiket", 16, ACC, BOLD).move_to(pf[0][0])
        y0 = -1.45
        cells = VGroup()
        for i, (n, f, b) in enumerate(DWL):
            r = RoundedRectangle(corner_radius=0.08, width=1.38, height=0.95, stroke_color=CHC[i], stroke_width=2, fill_color=CHC[i], fill_opacity=0.12)
            g = VGroup(T(f"kanal {n}", 15, CHC[i], BOLD), T(f"{f} THz", 15, TXT, BOLD), HX(b, 15, MUTED)).arrange(DOWN, buff=0.04).move_to(r)
            cells.add(VGroup(r, g))
        cells.arrange(RIGHT, buff=0.1).move_to([0, y0, 0])
        hl = glow(cells[3], CH[3])
        nm = pill("≈ 1598,9 nm", CH[3], 18).next_to(cells, DOWN, buff=0.25).set_x(cells[3].get_x())
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.3 §6.1.5.3–4 · Tablo 6-3 · Şekil 10-3"), run_time=0.6)
        self.at(self.cue("on altılık tabanda", 1.0))
        self.play(FadeIn(pf), FadeIn(hv), run_time=0.6)
        self.at(self.cue("En anlamsız dört bit", 7.5))
        self.play(Indicate(pf[1], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("sıfır sıfır bir bir", 9.8))
        self.play(FadeOut(pf[1][1]), FadeIn(bin_, scale=0.8), run_time=0.4)
        self.at(self.cue("aşağı yön kanal kimliğidir", 11.5))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cells], lag_ratio=0.08), run_time=0.9)
        self.at(self.cue("dördüncü kanal", 13.8))
        self.play(Create(hl), *[cells[i].animate.set_opacity(0.35) for i in range(8) if i != 3], run_time=0.6)
        self.at(self.cue("bin beş yüz doksan sekiz", 18.2))
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Kalan yirmi sekiz bit", 23.0))
        self.play(Indicate(pf[0], color=ACC, scale_factor=1.04), run_time=0.6)
        self.at(self.cue("dokunmadan taşıdığı", 24.8))
        self.play(FadeOut(pf[0][1]), FadeIn(lab_t), run_time=0.5)
        self.end(pad=0.1)

        # a3 — ONU-ID 19: defaults; what survives handover and O1
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "ONU-ID 19: hangi kimlikler kanal devrinde, hangileri O1'e dönüşte kalır?", CH[3])
        idt = tile("ONU-ID 19", ACC, 2.2, 0.55, 19, 0.25).move_to([-4.6, 0.9, 0])
        d1 = tile("varsayılan Alloc-ID 19", ACC, 3.2, 0.5, 17, 0.12).move_to([-0.6, 1.25, 0])
        d2 = tile("OMCC XGEM Port-ID 19", OMC, 3.2, 0.5, 17, 0.12).move_to([-0.6, 0.55, 0])
        ar = VGroup(arrow(idt.get_right(), d1.get_left(), MUTED, 2.2, 0.12), arrow(idt.get_right(), d2.get_left(), MUTED, 2.2, 0.12))
        K, F = "kalır ✓", "unutulur ✗"
        rows = [["ONU-ID 19", K, F], ["Alloc-ID'ler (varsayılan + açık)", K, F], ["varsayılan Port-ID 19 (OMCC)", K, F],
                ["OMCC ile atanmış portlar", K, K], ["bölümleme indeksi (CPI)", K, K], ["burst profilleri", F, F]]
        tb = table(["kimlik", "kanal devri", "O1'e dönüş"], rows, [5.2, 2.6, 2.6], size=17, hsize=16, row_h=0.42).move_to([0, -1.45, 0])
        for r in tb[1:]:
            for c in r[2:]:
                c.set_color(GOOD if "✓" in c.text else WARN)
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.3 §6.1.5.6–9 · Tablo 12-4 / 12-5 · §11.3.3.1"), run_time=0.6)
        self.at(self.cue("ONU kimliği on dokuz", 1.0))
        self.play(FadeIn(idt), run_time=0.4)
        self.play(GrowArrow(ar[0]), FadeIn(d1, shift=RIGHT * 0.1), GrowArrow(ar[1]), FadeIn(d2, shift=RIGHT * 0.1), run_time=0.8)
        self.at(self.cue("yalnızca burst profilleri", 8.8))
        self.play(FadeIn(tb[0]), FadeIn(tb[6][:2]), run_time=0.5)
        self.play(FadeIn(tb[6][2]), run_time=0.3)
        self.at(self.cue("tahsis kimlikleri ve portlar kalır", 14.3))
        self.play(*[FadeIn(tb[i][:3]) for i in (1, 2, 3, 4, 5)], run_time=0.6)
        self.at(self.cue("İlk duruma dönüşte", 17.3))
        self.play(FadeIn(tb[1][3]), FadeIn(tb[6][3]), run_time=0.4)
        self.at(self.cue("varsayılan port unutulur", 20.2))
        self.play(FadeIn(tb[2][3]), FadeIn(tb[3][3]), run_time=0.4)
        self.at(self.cue("bölümleme indeksi korunur", 24.6))
        self.play(FadeIn(tb[4][3]), FadeIn(tb[5][3]), run_time=0.4)
        self.at(self.cue("Şimdi bu bölüme", 29.1))
        self.play(Indicate(VGroup(tb[4][3], tb[5][3]), color=GOOD, scale_factor=1.05), run_time=0.5)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep12_recap")
