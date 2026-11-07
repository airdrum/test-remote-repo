"""S2·B2 · Perde 1 (PSBd + senkron — G.989.3 §10.1.1) and Perde 2 (FEC, karıştırıcı, HEC — §10.1.3, §10.1.4, Ek A/B)."""
from ep12_common import *

OC64 = [("OC gövdesi", 51, OCC), ("HEC", 13, HECC)]
OCB = [("PIT", 8, OCC), ("PON-ID", 32, ACC), ("R", 1, MUTED), ("C", 1, MUTED), ("TOL", 9, GOLD)]
PIT = [("RE", 1, OCC), ("ODN sınıfı", 3, OCC), ("FEC", 1, OCC), ("P", 1, OCC), ("Bağlantı tipi", 2, OCC)]
DWL = [("1", "187,8", "0000"), ("2", "187,7", "0001"), ("3", "187,6", "0010"), ("4", "187,5", "0011"),
       ("5", "187,4", "0100"), ("6", "187,3", "0101"), ("7", "187,2", "0110"), ("8", "187,1", "0111")]
CHC = CH + ["#94A3B8"] * 4


def oc_rows():
    oc = fields(OC64, 12.4, 0.55, 18, 14, unit=" bit").move_to([0, 2.05, 0])
    body = fields(OCB, 12.4, 0.55, 17, 14).move_to([0, 0.85, 0])
    zl = zoom_lines(oc[0][0], body, OCC)
    return oc, body, zl


# ================================ PERDE 1 ======================================
class E12P1A(Act12):
    HDR, MANIFEST, FIRST = H12[1], M12("p1"), True

    def construct(self):
        # b1 — continuous downstream, 125 µs frames, 24-byte PSBd
        self.beat("b1")
        tc = self.title_card("PERDE 1", "Senkron bloğu")
        self.at(self.cue("Çalışan bir OLT", 2.8))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Aşağı yön: kesintisiz 125 µs çerçeveler")
        y = 1.25
        olt = ct_box("OLT CT", OLTC, 1.35, 0.62, 18).move_to([-5.95, y, 0])
        x0, x1 = -4.75, 6.35
        fw = (x1 - x0) / 3
        frames = VGroup()
        for i in range(3):
            frames.add(VGroup(seg(x0 + i * fw, 0.42, y, PHC, None, 0.62, 0.8), seg(x0 + i * fw + 0.42, fw - 0.42, y, TW_DS, "çerçeve yükü", 0.62, 0.12, 16)))
        ticks = VGroup(*[VGroup(Line([x0 + i * fw, y - 0.42, 0], [x0 + i * fw, y - 0.55, 0], color=MUTED, stroke_width=2),
                                T(s, 15, MUTED, BOLD).move_to([x0 + i * fw, y - 0.75, 0])) for i, s in enumerate(("0", "125 µs", "250 µs", "375 µs"))])
        ticks[0][1].shift(RIGHT * 0.08)
        ticks[3][1].shift(LEFT * 0.25)
        feed = Arrow(olt.get_right(), [x0, y, 0], buff=0.05, color=TW_DS, stroke_width=3, tip_length=0.14, max_tip_length_to_length_ratio=0.4)
        cont = T("sürekli ↓", 16, TW_DS, BOLD).next_to(olt, DOWN, buff=0.15)
        r10 = VGroup(tag("10G · 9,95328 Gbit/s", R10, 18), T("→  155 520 bayt / çerçeve", 22, TXT, BOLD)).arrange(RIGHT, buff=0.3)
        r25 = VGroup(tag("2,5G · 2,48832 Gbit/s", R25, 18), T("→  38 880 bayt / çerçeve", 22, TXT, BOLD)).arrange(RIGHT, buff=0.3)
        rr = VGroup(r10, r25).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.05, -0.55, 0])
        for r in rr:
            r[1].set_x(rr.get_left()[0] + 3.3 + r[1].width / 2)
        zoom = VGroup(*[seg(0, 1.9, 0, c, s, 0.7, 0.3, 18) for s, c in (("8 B", PSC), ("8 B", SFCC), ("8 B", OCC))])
        zoom.arrange(RIGHT, buff=0).move_to([-3.45, -2.3, 0])
        zl = zoom_lines(frames[0][0], zoom, PHC)
        zt = VGroup(T("PSBd · 24 bayt", 22, GOLD, BOLD), T("aşağı yön fiziksel senkron bloğu", 17, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        zt.next_to(zoom, RIGHT, buff=0.35)
        self.play(FadeIn(olt), FadeIn(cont), self.set_src("G.989.3 §10.1.1 · Şekil 10-1"), run_time=0.5)
        self.play(GrowArrow(feed), run_time=0.4)
        self.at(self.cue("yüz yirmi beş mikrosaniyelik", 8.3))
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in frames], lag_ratio=0.25), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.2), run_time=1.2)
        self.at(self.cue("on gigabitte yüz elli beş", 12.8))
        self.play(FadeIn(r10, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("iki buçuk gigabitte otuz sekiz", 16.9))
        self.play(FadeIn(r25, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yirmi dört baytlık bir blokla", 21.7))
        self.play(*[Indicate(f[0], color=GOLD, scale_factor=1.25) for f in frames], run_time=0.8)
        self.at(self.cue("aşağı yön fiziksel senkron bloğu", 25.8))
        self.play(Create(zl), FadeIn(zoom, shift=DOWN * 0.1), FadeIn(zt[1]), run_time=0.7)
        self.at(self.cue("kısaca PSBd", 28.6))
        self.play(FadeIn(zt[0], shift=RIGHT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # b1a — PMD bridge: 8 kHz
        self.beat("b1a")
        self.clear()
        self.set_badge("pmd")
        h = self.show_heading("PMD Köprüsü — 8 kHz'in katı")
        ch = self.chip_at(s1chip(4), h)
        rng = np.random.default_rng(4)
        bits = "".join("1" if v else "0" for v in rng.integers(0, 2, 70))
        wx0, wx1, wy = -6.2, -0.5, 0.55
        tb = (wx1 - wx0) / len(bits)
        wave = VMobject(stroke_color=TW_DS, stroke_width=2.2).set_points_as_corners(nrz(bits, wx0, tb, wy - 0.45, wy + 0.45, 0.02))
        marks = VGroup(*[Rectangle(width=0.32, height=1.1, stroke_width=0, fill_color=GOLD, fill_opacity=0.35).move_to([wx0 + 0.16 + k * 2.85, wy, 0]) for k in range(2)])
        ml = VGroup(*[T("PSBd", 15, GOLD, BOLD).next_to(m, UP, buff=0.08) for m in marks])
        per = DoubleArrow([marks[0].get_x(), wy - 0.85, 0], [marks[1].get_x(), wy - 0.85, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12)
        perl = T("125 µs", 17, GOLD, BOLD).next_to(per, DOWN, buff=0.08)
        wl = T("Sezon 1: dışarıdan, optik sinyal", 17, MUTED, BOLD).next_to(VGroup(wave, ml), UP, buff=0.15).align_to(wave, LEFT)
        eq = VGroup(VGroup(T("9,95328 Gbit/s", 22, R10, BOLD), T("= 1 244 160 × 8 kHz", 22, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                    VGroup(T("2,48832 Gbit/s", 22, R25, BOLD), T("= 311 040 × 8 kHz", 22, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                    T("1 / 8 kHz = 125 µs", 26, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.5, 0.6, 0])
        nb = T("(bit / çerçeve)", 15, MUTED).next_to(eq[0], DOWN, buff=0.04).align_to(eq[0][1], LEFT)
        inside = VGroup(*[seg(0, 2.2, 0, c, s, 0.6, 0.3, 17) for s, c in (("PSync", PSC), ("SFC", SFCC), ("OC", OCC))]).arrange(RIGHT, buff=0).move_to([1.8, -2.35, 0])
        il = T("bu bölüm: bloğun içi →", 20, ACC, BOLD).next_to(inside, LEFT, buff=0.35)
        self.play(FadeIn(ch, shift=LEFT * 0.1), self.set_src("G.989.2 §11.1.1 · Tablo 11-1 · S1·B4"), run_time=0.5)
        self.at(self.cue("PSBd'yi dışarıdan", 1.0))
        self.play(FadeIn(wl), Create(wave), run_time=1.0)
        self.at(self.cue("optik bir sinyal olarak", 5.5))
        self.play(FadeIn(marks), FadeIn(ml), GrowFromCenter(per), FadeIn(perl), run_time=0.7)
        self.at(self.cue("sekiz kilohertzin katıdır", 8.1))
        self.play(FadeIn(eq[0], shift=LEFT * 0.1), FadeIn(nb), run_time=0.5)
        self.play(FadeIn(eq[1], shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("sekiz kilohertzin periyodudur", 14.5))
        self.play(FadeIn(eq[2], shift=UP * 0.1), Indicate(perl, color=GOLD), run_time=0.7)
        self.at(self.cue("bloğun içine giriyoruz", 17.1))
        self.play(FadeIn(il, shift=RIGHT * 0.1), LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in inside], lag_ratio=0.2), run_time=0.8)
        self.end(pad=0.05)

        # b2 — three 8-byte parts; PSync
        self.beat("b2")
        self.clear()
        self.set_badge("std")
        h = self.show_heading("PSBd = 3 × 8 bayt")
        psb = fields([("PSync", 64, PSC), ("SFC yapısı", 64, SFCC), ("OC yapısı", 64, OCC)], 12.4, 0.62, 20, 15, unit=" bit").move_to([0, 2.0, 0])
        hx = VGroup(*[HX(PSYNC[i:i + 2], 30, PSC, BOLD) for i in range(0, 16, 2)]).arrange(RIGHT, buff=0.32).move_to([0, 0.6, 0])
        hxl = T("PSync = 0x", 22, MUTED, BOLD).next_to(hx, LEFT, buff=0.15)
        bc = bitcells(PSYNC_BITS, 11.52, 0.34, PSC).move_to([0, -0.35, 0])
        cnt = VGroup(T("32 × 1", 20, PSC, BOLD), T("·", 20, MUTED), T("32 × 0", 20, MUTED, BOLD)).arrange(RIGHT, buff=0.2).next_to(bc, DOWN, buff=0.25).align_to(bc, LEFT)
        runs = VGroup(SurroundingRectangle(bc[26:32], color=GOLD, buff=0.04, stroke_width=3), SurroundingRectangle(bc[32:38], color=GOLD, buff=0.04, stroke_width=3))
        rl = T("en uzun özdeş dizi: 6 bit", 20, GOLD, BOLD).next_to(runs, DOWN, buff=0.2).set_x(runs.get_x())
        pr = VGroup(tag("karıştırılmaz", WARN, 19), tag("FEC ile korunmaz", WARN, 19)).arrange(RIGHT, buff=0.3).move_to([-3.2, -2.45, 0])
        fin = pill("ONU'nun aradığı tek sabit işaret", PSC, 20).move_to([3.3, -2.45, 0])
        self.play(self.set_src("G.989.3 §10.1.1.1 · Şekil 10-2 · sayımlar hesaplanmıştır"), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in psb], lag_ratio=0.25), run_time=1.0)
        self.at(self.cue("Birincisi senkron deseni", 3.1))
        self.play(Indicate(psb[0], color=PSC, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("altmış dört bitlik bir sözcük", 6.3))
        self.play(FadeIn(hxl), LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in hx], lag_ratio=0.08), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c in bc], lag_ratio=0.01), run_time=0.8)
        self.at(self.cue("Otuz iki biri ve otuz iki", 8.8))
        self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("en uzun özdeş bit dizisi", 12.2))
        self.play(Create(runs), FadeIn(rl), run_time=0.7)
        self.at(self.cue("Desen ne karıştırılır", 15.6))
        self.play(FadeIn(pr[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("ne de FEC ile korunur", 17.5))
        self.play(FadeIn(pr[1], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("tek sabit işarettir", 20.5))
        self.play(FadeIn(fin, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # b3 — SFC structure
        self.beat("b3")
        self.clear(h)
        h = self.show_heading("SFC yapısı — süper çerçeve sayacı", h)
        sf = fields([("süper çerçeve sayacı (SFC)", 51, SFCC), ("HEC", 13, HECC)], 12.4, 0.62, 20, 15, unit=" bit").move_to([0, 2.0, 0])
        vals = ["0x0 0012 3456 789A", "0x0 0012 3456 789B", "0x0 0012 3456 789C"]
        fr = VGroup()
        for i, v in enumerate(vals):
            p = seg(0, 0.42, 0, PHC, None, 0.55, 0.8)
            q = seg(0.42, 3.4, 0, TW_DS, None, 0.55, 0.1)
            lab = HX(v, 16, SFCC, BOLD).next_to(p, UP, buff=0.1).align_to(p, LEFT)
            fr.add(VGroup(p, q, lab))
        fr.arrange(RIGHT, buff=0.12).move_to([0, 0.5, 0])
        inc = VGroup(*[T("+1", 18, GOOD, BOLD).move_to([(fr[i][0].get_x() + fr[i + 1][0].get_x()) / 2, -0.15, 0]) for i in range(2)])
        wr = VGroup(HX("0x7 FFFF FFFF FFFF", 22, GOLD, BOLD), T("→", 26, MUTED, BOLD), HX("0x0 0000 0000 0000", 22, GOOD, BOLD)).arrange(RIGHT, buff=0.3).move_to([0, -0.95, 0])
        wl = T("hepsi 1 → sonraki çerçevede 0", 17, MUTED, BOLD).next_to(wr, DOWN, buff=0.12)
        calc = T("2⁵¹ × 125 µs ≈ 8 919 yıl", 34, TXT, BOLD).move_to([-2.3, -2.5, 0])
        nv = pill("pratikte hiç taşmaz", GOOD, 20).next_to(calc, RIGHT, buff=0.5)
        self.play(self.set_src("G.989.3 §10.1.1.1.2 · Şekil 10-2 · süre hesaplanmıştır"), run_time=0.3)
        self.play(FadeIn(sf[0]), run_time=0.5)
        self.at(self.cue("elli bir bitlik bir sayaç", 3.1))
        self.play(Indicate(sf[0], color=SFCC, scale_factor=1.04), run_time=0.5)
        self.play(FadeIn(sf[1], shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("Sayaç her çerçevede bir artar", 9.2))
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in fr], lag_ratio=0.3), LaggedStart(*[FadeIn(i) for i in inc], lag_ratio=0.3), run_time=1.2)
        self.at(self.cue("hepsi bir olduktan sonraki", 11.7))
        self.play(FadeIn(wr[0]), run_time=0.4)
        self.play(FadeIn(wr[1:], shift=RIGHT * 0.1), FadeIn(wl), run_time=0.6)
        self.at(self.cue("yüz yirmi beş mikrosaniyelik adımlarla", 17.2))
        self.play(FadeIn(calc, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("sayaç pratikte hiç taşmaz", 23.6))
        self.play(FadeIn(nv, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p1A")


class E12P1B(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[1], M12("p1"), "std"

    def construct(self):
        # b4 — OC structure, PIT byte
        self.beat("b4")
        h = self.show_heading("OC yapısı — işletim denetimi")
        oc, body, zl = oc_rows()
        pit = fields(PIT, 7.2, 0.55, 16, 14).move_to([0, -0.45, 0])
        pz = zoom_lines(body[0][0], pit, OCC)
        rows = num_rows([("RE · 1 bit", OCC, "güç değeri:  0 = OLT CT  ·  1 = yeniden üreteç (RE)"),
                         ("ODN · 3 bit", OCC, "000 N1 · 001 N2 · 011 E1 · 100 E2 (diğerleri ayrılmış)"),
                         ("FEC · 1 bit", OCC, "aşağı yön FEC:  1 = açık  ·  0 = kapalı"),
                         ("P · 1 bit", OCC, "1 = G.989.3 TC  ·  0 = G.987.3 (XG-PON) TC"),
                         ("Tip · 2 bit", OCC, "bağlantı tipi:  10 = A  ·  01 = B  ·  11 = ikisi  ·  00 = belirtilmemiş")], size=17, gap=0.43)
        fit(rows, 12.4).move_to([0, -2.22, 0])
        self.play(self.set_src("G.989.3 §10.1.1.1.3 · Şekil 10-3 · Tablo 10-1"), run_time=0.3)
        self.play(FadeIn(oc[0]), run_time=0.5)
        self.at(self.cue("on üç bitlik hata denetimi", 3.6))
        self.play(FadeIn(oc[1], shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("OLT'nin her çerçevede bütün", 9.2))
        self.play(Create(zl), LaggedStart(*[FadeIn(c, shift=DOWN * 0.08) for c in body], lag_ratio=0.12), run_time=1.0)
        self.at(self.cue("PON kimlik türüdür", 13.8))
        self.play(Create(pz), FadeIn(pit), Indicate(body[0], color=OCC, scale_factor=1.06), run_time=0.8)
        for k, (key, d) in enumerate((("yeniden üreteçten", 16.5), ("üç bit ODN sınıfını", 21.3), ("aşağı yön FEC'inin", 23.0),
                                      ("G.989.3 mü yoksa XG-PON", 27.0), ("bağlantı tipini söyler", 32.1))):
            self.at(self.cue(key, d))
            cell = pit[[0, 1, 2, 3, 4][k]]
            self.play(FadeIn(rows[k], shift=RIGHT * 0.1), Indicate(cell[0], color=GOLD, scale_factor=1.15), run_time=0.5)
        self.end(pad=0.05)

        # b4a — PON-ID: admin label + DWLCH ID
        self.beat("b4a")
        h = self.heading12("PON-ID — 32 bit", h)
        self.play(FadeOut(pit), FadeOut(pz), FadeOut(rows), run_time=0.4)
        pid = fields([("yönetim etiketi", 28, ACC), ("DWLCH ID", 4, GOLD)], 9.6, 0.6, 18, 14).move_to([0, -0.45, 0])
        pzz = zoom_lines(body[1][0], pid, ACC)
        flow = VGroup(tile("operatör · EMS/OSS", MUTED, 2.6, 0.5, 16, 0.12), tile("OLT CT", OLTC, 1.4, 0.5, 16, 0.12),
                      tile("PSBd · her çerçevede", GOLD, 2.8, 0.5, 16, 0.12)).arrange(RIGHT, buff=0.55).move_to([-1.2, -1.55, 0])
        fa = VGroup(*[arrow(flow[i].get_right(), flow[i + 1].get_left(), MUTED, 2.2, 0.12) for i in range(2)])
        tr_ = T("dokunmadan taşır", 16, ACC, BOLD).next_to(flow, RIGHT, buff=0.3)
        cells = VGroup()
        for i, (n, f, b) in enumerate(DWL):
            r = RoundedRectangle(corner_radius=0.08, width=1.42, height=0.62, stroke_color=CHC[i], stroke_width=2, fill_color=CHC[i], fill_opacity=0.12)
            g = VGroup(HX(b, 15, CHC[i], BOLD), T(f"{f} THz", 15, TXT, BOLD)).arrange(DOWN, buff=0.03).move_to(r)
            cells.add(VGroup(r, g))
        cells.arrange(RIGHT, buff=0.1).move_to([0, -2.65, 0])
        cl = T("kanal 1 … 8", 15, MUTED, BOLD).next_to(cells, UP, buff=0.08).align_to(cells, LEFT)
        self.play(Indicate(body[1], color=ACC, scale_factor=1.04), self.set_src("G.989.3 §6.1.5.3–4 · Şekil 10-3 · Tablo 6-3"), run_time=0.6)
        self.play(Create(pzz), FadeIn(pid), run_time=0.6)
        self.at(self.cue("yirmi sekiz bitlik bir yönetim", 3.3))
        self.play(Indicate(pid[0], color=ACC, scale_factor=1.04), run_time=0.5)
        self.at(self.cue("operatörün verdiği", 6.6))
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in flow], lag_ratio=0.3), LaggedStart(*[GrowArrow(a) for a in fa], lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(tr_, shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("dört bitlik aşağı yön dalga boyu", 11.6))
        self.play(Indicate(pid[1], color=GOLD, scale_factor=1.15), run_time=0.6)
        self.at(self.cue("sıfırdan yediye", 15.8))
        self.play(FadeIn(cl), LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cells], lag_ratio=0.08), run_time=1.0)
        self.at(self.cue("sekiz kanal", 21.5))
        self.play(LaggedStart(*[Indicate(c[1][1], color=GOLD, scale_factor=1.1) for c in cells], lag_ratio=0.06), run_time=0.9)
        self.end(pad=0.05)

        # b4b — R, C, TOL
        self.beat("b4b")
        h = self.heading12("Son 11 bit — güç", h)
        self.play(FadeOut(pid), FadeOut(pzz), FadeOut(flow), FadeOut(fa), FadeOut(tr_), FadeOut(cells), FadeOut(cl), run_time=0.4)
        pw = fields([("R", 1, MUTED), ("C", 1, MUTED), ("TOL", 9, GOLD)], 5.5, 0.6, 18, 14).move_to([-3.55, -0.45, 0])
        pzw = zoom_lines(VGroup(body[2][0], body[4][0]), pw, GOLD)
        rn = VGroup(VGroup(tag("R", MUTED, 17), T("ayrılmış · 0", 18, TXT)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("C", MUTED, 17), T("TOL referans noktası:", 18, TXT)).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rn.move_to([2.6, -0.2, 0], aligned_edge=LEFT).set_x(0.4, direction=LEFT)
        cc = VGroup(tag("0 = S/R-CG", ACC, 17), tag("1 = S/R-CP", ACC, 17)).arrange(RIGHT, buff=0.2).next_to(rn[1], RIGHT, buff=0.25)
        ax_y = -2.45
        X = lambda v: -5.9 + v / 511 * 11.8
        axl = Line([X(0), ax_y, 0], [X(511), ax_y, 0], color=MUTED, stroke_width=2.5)
        pts = [(0, "0x000", "−30 dBm", GOLD), (300, "0x12C", "0 dBm", GOLD), (510, "0x1FE", "+21 dBm", GOLD)]
        mk = VGroup()
        for v, hx_, db, c in pts:
            mk.add(VGroup(Line([X(v), ax_y - 0.1, 0], [X(v), ax_y + 0.1, 0], color=c, stroke_width=3),
                          HX(hx_, 15, MUTED, BOLD).move_to([X(v), ax_y + 0.33, 0]), T(db, 17, c, BOLD).move_to([X(v), ax_y - 0.35, 0])))
        mk[0][1].shift(RIGHT * 0.25)
        mk[0][2].shift(RIGHT * 0.38)
        mk[2][1].shift(LEFT * 0.42)
        mk[2][2].shift(LEFT * 0.5)
        ns = VGroup(Dot([X(511), ax_y, 0], radius=0.07, color=WARN), T("0x1FF = desteklenmiyor", 16, WARN, BOLD).move_to([X(511) - 1.25, ax_y + 0.75, 0]))
        frm = T("P = −30 dBm + TOL × 0,1 dB", 22, GOLD, BOLD).move_to([-2.8, -1.45, 0])
        axn = T("TOL kodu (9 bit)", 15, MUTED, BOLD).next_to(axl, DOWN, buff=0.5).align_to(axl, LEFT)
        self.play(Indicate(VGroup(body[2], body[3], body[4]), color=GOLD, scale_factor=1.04), self.set_src("G.989.3 §10.1.1.1.3 · Şekil 10-3"), run_time=0.6)
        self.play(Create(pzw), FadeIn(pw), run_time=0.5)
        self.at(self.cue("Bir ayrılmış bit", 2.3))
        self.play(FadeIn(rn[0], shift=RIGHT * 0.1), Indicate(pw[0][0], color=GOLD), run_time=0.5)
        self.at(self.cue("hangi referans noktasında", 4.4))
        self.play(FadeIn(rn[1], shift=RIGHT * 0.1), Indicate(pw[1][0], color=GOLD), run_time=0.5)
        self.at(self.cue("S/R-CG mi", 8.1))
        self.play(FadeIn(cc, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("dokuz bitlik TOL alanı", 11.2))
        self.play(Indicate(pw[2], color=GOLD, scale_factor=1.06), Create(axl), FadeIn(axn), run_time=0.7)
        self.at(self.cue("eksi otuz dBm'den", 15.4))
        self.play(FadeIn(frm, shift=UP * 0.1), LaggedStart(*[FadeIn(m) for m in mk], lag_ratio=0.25), run_time=1.0)
        self.at(self.cue("En büyük kod", 21.5))
        self.play(FadeIn(ns, scale=0.9), run_time=0.5)
        self.end(pad=0.05)

        # b5 — PMD bridge: each field a season-1 table
        self.beat("b5")
        self.clear()
        self.set_badge("pmd")
        h = self.show_heading("PMD Köprüsü — her alan bir Sezon 1 tablosu")
        rows = [("ODN sınıfı · 3 bit", "yol kaybı sınıfları N1 · N2 · E1 · E2 (G.989.2 Tablo 6-1)", 2),
                ("DWLCH ID · 4 bit", "↓ frekans planı 187,8 – 187,1 THz (G.989.2 Tablo 11-2)", 3),
                ("Bağlantı tipi · 2 bit", "A: yükselteçsiz · B: yükselteçli OLT alıcısı (§11.1.4)", 8),
                ("TOL · 0,1 dB adım", "izleme çözünürlüğü 0,1 dB (G.989.2 Ek II)", 10)]
        g = VGroup()
        for i, (f, d, n) in enumerate(rows):
            y = 1.35 - i * 1.1
            a = tile(f, OCC, 3.1, 0.55, 17, 0.18).move_to([-5.0, y, 0])
            b = fit(T(d, 18, TXT), 5.4).move_to([-3.2, y, 0], aligned_edge=LEFT)
            c = s1chip(n, 16).move_to([5.0, y, 0])
            ar = arrow(a.get_right(), b.get_left() + LEFT * 0.08, MUTED, 2, 0.1)
            g.add(VGroup(a, ar, b, c))
        tl = T("Sezon 1'de birer tablo → G.989.3'te birkaç bit", 18, MUTED, BOLD).move_to([0, -3.0, 0])
        keys = (("ikinci bölümdeki yol kaybı", 5.3), ("üçüncü bölümdeki frekans", 9.8), ("sekizinci bölümdeki", 15.0), ("onuncu bölümdeki izleme", 20.3))
        self.play(self.set_src("G.989.3 Şekil 10-3 ↔ G.989.2 Tablo 6-1 · 11-2 · §11.1.4 · Ek II"), run_time=0.3)
        self.at(self.cue("birinci sezonda bir tabloydu", 1.0))
        self.play(FadeIn(tl), run_time=0.4)
        for k, (key, d) in enumerate(keys):
            self.at(self.cue(key, d))
            self.play(FadeIn(g[k][0], shift=RIGHT * 0.1), GrowArrow(g[k][1]), FadeIn(g[k][2]), FadeIn(g[k][3], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # b6 — 0x0F0F… XOR on SFC and OC
        self.beat("b6")
        self.clear()
        self.set_badge("std")
        h = self.show_heading("SFC ve OC: sabit desenle XOR")
        psb = fields([("PSync", 64, PSC), ("SFC yapısı", 64, SFCC), ("OC yapısı", 64, OCC)], 12.4, 0.6, 19, 15, show_w=False).move_to([0, 2.05, 0])
        xo = VGroup(*[HX("XOR 0x0F0F0F0F 0F0F0F0F", 15, GOLD, BOLD).next_to(psb[i][0], DOWN, buff=0.12) for i in (1, 2)])
        nox = T("XOR yok", 17, WARN, BOLD).next_to(psb[0][0], DOWN, buff=0.12)
        tx = VGroup(tile("SFC / OC + HEC hesapla", SFCC, 3.3, 0.55, 17, 0.15), tile("XOR 0x0F0F…", GOLD, 2.4, 0.55, 17, 0.2),
                    tile("hatta", MUTED, 1.3, 0.55, 17, 0.12)).arrange(RIGHT, buff=0.5).move_to([-1.6, 0.75, 0])
        txa = VGroup(*[arrow(tx[i].get_right(), tx[i + 1].get_left(), MUTED, 2.2, 0.12) for i in range(2)])
        txl = T("verici", 16, MUTED, BOLD).next_to(tx, LEFT, buff=0.25)
        rx = T("alıcı: önce XOR'u geri al, sonra HEC doğrula", 17, MUTED, BOLD).next_to(tx, DOWN, buff=0.15).align_to(tx, LEFT)
        z = "0" * 32
        pat = "00001111" * 4
        xr = "".join("1" if a != b else "0" for a, b in zip(z, pat))
        b0 = bitcells(z, 8.0, 0.32, SFCC).move_to([0.2, -0.75, 0])
        b1 = bitcells(pat, 8.0, 0.32, GOLD).move_to([0.2, -1.3, 0])
        b2 = bitcells(xr, 8.0, 0.32, SFCC).move_to([0.2, -1.95, 0])
        l0 = T("SFC (ilk 32 bit)", 16, SFCC, BOLD).next_to(b0, LEFT, buff=0.25)
        l1 = T("XOR 0x0F0F0F0F", 16, GOLD, BOLD).next_to(b1, LEFT, buff=0.25)
        l2 = T("hatta", 16, TXT, BOLD).next_to(b2, LEFT, buff=0.25)
        sep = Line(b1.get_corner(DL) + DOWN * 0.13, b1.get_corner(DR) + DOWN * 0.13, color=MUTED, stroke_width=1.5)
        run0 = T("32 bitlik 0 dizisi", 16, WARN, BOLD).next_to(b0, RIGHT, buff=0.15)
        run2 = T("en uzun dizi 4 bit", 16, GOOD, BOLD).next_to(b2, RIGHT, buff=0.15)
        gl = pill("neredeyse sıfır sayaca geçiş ekler", GOOD, 19).move_to([0, -2.85, 0])
        self.play(FadeIn(psb), self.set_src("G.989.3 §10.1.1.2 · bit örneği hesaplanmıştır"), run_time=0.5)
        self.at(self.cue("hata denetimi hesaplandıktan", 1.4))
        self.play(FadeIn(txl), FadeIn(tx[0], shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("sayaç ve OC yapıları", 4.4))
        self.play(GrowArrow(txa[0]), FadeIn(tx[1], shift=RIGHT * 0.1), GrowArrow(txa[1]), FadeIn(tx[2]), run_time=0.6)
        self.at(self.cue("sıfır ef sıfır ef", 7.6))
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.08) for x in xo], lag_ratio=0.3), FadeIn(rx), run_time=0.7)
        self.at(self.cue("Neredeyse tamamı sıfır", 12.2))
        self.play(FadeIn(l0), FadeIn(b0), FadeIn(run0), run_time=0.5)
        self.play(FadeIn(l1), FadeIn(b1), Create(sep), run_time=0.5)
        self.play(FadeIn(l2), FadeIn(b2), FadeIn(run2), FadeIn(gl, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Senkron deseni bu işleme girmez", 16.5))
        self.play(FadeIn(nox, shift=UP * 0.1), Indicate(psb[0], color=WARN, scale_factor=1.04), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p1B")


class E12P1C(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[1], M12("p1"), "std"

    def construct(self):
        # b7 — reference machine, four states
        self.beat("b7")
        h = self.show_heading("Senkron durum makinesi — Şekil 10-4")
        sm = SyncSM(y=0.75)
        ref = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=13.2, height=3.2, stroke_color=MUTED, stroke_width=1.5), num_dashes=90).move_to([0, 0.55, 0])
        refl = T("referans makine", 15, MUTED, BOLD).next_to(ref, UP, buff=0.06).align_to(ref, LEFT).shift(RIGHT * 0.2)
        t1 = tag("ayrıntılar ONU'ya ait · standart dışı", MUTED, 18)
        t2 = tag("başarım bu makineyle eşleşmeli", GOOD, 18)
        tt = VGroup(t1, t2).arrange(RIGHT, buff=0.4).move_to([0, -2.4, 0])
        self.play(self.set_src("G.989.3 §10.1.1.3 · Şekil 10-4"), run_time=0.3)
        self.at(self.cue("referans durum makinesi", 2.3))
        for b in sm.b:
            b.set_opacity(0.3)
        self.play(Create(ref), FadeIn(refl), *[FadeIn(b) for b in sm.b], run_time=0.7)
        self.at(self.cue("ayrıntıların ONU'ya ait", 5.9))
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("başarımın bu makineyle", 8.9))
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("dört durumu vardır", 13.7))
        self.play(Indicate(refl, color=ACC), run_time=0.4)
        for i, (key, d) in enumerate((("av", 16.1), ("ön senkron", 16.4), ("senkron ve yeniden", 17.3))):
            self.at(self.cue(key, d))
            if i < 2:
                self.play(sm.b[i].animate.set_opacity(1), run_time=0.3)
            else:
                self.play(sm.b[2].animate.set_opacity(1), sm.b[3].animate.set_opacity(1), run_time=0.35)
        self.end(pad=0.05)

        # b7a — Hunt: exact match in all alignments; Pre-Sync; Sync; tolerant checks
        self.beat("b7a")
        self.play(FadeOut(tt), FadeOut(ref), FadeOut(refl), run_time=0.4)
        cur = glow(sm.b[0], GOLD)
        rng = np.random.default_rng(7)
        bits = "".join("1" if v else "0" for v in rng.integers(0, 2, 60))
        st = bitcells(bits, 11.4, 0.3, MUTED).move_to([0, -1.55, 0])
        win = Rectangle(width=11.4 / 60 * 16, height=0.5, stroke_color=GOLD, stroke_width=3).move_to(st[0:16])
        wl = T("her bit ve bayt hizalamasında kaydır · 64 / 64 birebir", 17, GOLD, BOLD).next_to(st, DOWN, buff=0.2)
        v1 = VGroup(tag("av", WARN, 17), T("PSync: 64 / 64 birebir", 19, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        v2 = VGroup(tag("kilitli", GOOD, 17), T("PSync: 64 bitten ≥ 62 eşleşme", 19, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        v3 = VGroup(tag("kilitli", GOOD, 17), T("SFC: HEC geçerli ve = yerel kopya + 1", 19, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        vv = VGroup(v1, v2, v3).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -2.1, 0])
        self.at(self.cue("Av durumunda ONU", 0.0))
        self.play(Create(cur), run_time=0.4)
        self.at(self.cue("bütün bit ve bayt", 1.4))
        self.play(FadeIn(st), Create(win), FadeIn(wl), Create(sm.hh[0]), FadeIn(sm.hh[1]), run_time=0.7)
        self.play(win.animate.move_to(st[44:60]), run_time=2.4, rate_func=linear)
        self.at(self.cue("birebir eşleşme ister", 6.1))
        self.play(win.animate.set_fill(GOLD, 0.25), Indicate(wl, color=GOLD, scale_factor=1.03), run_time=0.6)
        self.at(self.cue("geçerli bir sayaç oluşturuyorsa", 9.5))
        self.play(GrowArrow(sm.hp[0]), FadeIn(sm.hp[1]), cur.animate.move_to(sm.b[1]), run_time=0.7)
        self.at(self.cue("hem desen hem sayaç", 15.3))
        self.play(GrowArrow(sm.ps[0]), FadeIn(sm.ps[1]), GrowArrow(sm.ph[0]), FadeIn(sm.ph[1]), run_time=0.7)
        self.at(self.cue("senkron olur", 19.0))
        self.play(cur.animate.move_to(sm.b[2]), run_time=0.5)
        self.at(self.cue("Doğrulama artık daha hoşgörülüdür", 21.0))
        self.play(FadeOut(st), FadeOut(win), FadeOut(wl), FadeIn(v1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("en az altmış ikisi", 23.8))
        self.play(FadeIn(v2, shift=UP * 0.1), Create(sm.ss[0]), FadeIn(sm.ss[1]), run_time=0.6)
        self.at(self.cue("yerel kopyanın bir fazlası", 29.3))
        self.play(FadeIn(v3, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # b7b — Sync → Re-Sync → Hunt, M = 3, 375 µs
        self.beat("b7b")
        self.play(FadeOut(vv), run_time=0.4)
        self.at(self.cue("tek bir hatalı çerçeve", 0.5))
        self.play(GrowArrow(sm.sr[0]), FadeIn(sm.sr[1]), cur.animate.move_to(sm.b[3]), run_time=0.7)
        self.at(self.cue("tek bir iyi çerçeve", 6.4))
        self.play(GrowArrow(sm.rs[0]), FadeIn(sm.rs[1]), cur.animate.move_to(sm.b[2]), run_time=0.7)
        self.at(self.cue("M eksi bir ardışık", 10.5))
        self.play(Create(sm.rh[0]), FadeIn(sm.rh[1]), run_time=0.8)
        fx0 = -4.4
        fr = VGroup()
        marks = ["✓", "✗", "✗", "✗"]
        sts = ["Senkron", "Yeniden s.", "Yeniden s.", "Av · LODS"]
        cols = [GOOD, WARN, WARN, WARN]
        for i in range(4):
            r = Rectangle(width=2.0, height=0.5, stroke_color=cols[i], stroke_width=2, fill_color=cols[i], fill_opacity=0.15).move_to([fx0 + i * 2.15, -2.45, 0])
            m = T(f"çerçeve {marks[i]}", 16, cols[i], BOLD).move_to(r)
            s = T(sts[i], 15, STATE if i < 3 else WARN, BOLD).next_to(r, DOWN, buff=0.1)
            fr.add(VGroup(r, m, s))
        br = BraceBetweenPoints(fr[1][0].get_corner(UL) + UP * 0.05, fr[3][0].get_corner(UR) + UP * 0.05, UP, color=WARN)
        brl = T("3 kötü çerçeve × 125 µs = 375 µs", 17, WARN, BOLD).next_to(br, UP, buff=0.05)
        mm = pill("önerilen M = 3", GOLD, 19).move_to([5.4, -2.45, 0])
        self.at(self.cue("Önerilen M değeri üçtür", 16.4))
        self.play(FadeIn(mm, shift=LEFT * 0.1), FadeIn(fr[0]), run_time=0.5)
        self.at(self.cue("toplam üç kötü çerçeve", 18.4))
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in fr[1:]], lag_ratio=0.3), run_time=1.0)
        self.play(cur.animate.move_to(sm.b[0]), run_time=0.5)
        self.at(self.cue("üç yüz yetmiş beş mikrosaniye", 23.1))
        self.play(FadeIn(br), FadeIn(brl), run_time=0.6)
        self.end(pad=0.05)

        # b7c — LODS only in Hunt / Pre-Sync
        self.beat("b7c")
        self.play(FadeOut(fr), FadeOut(br), FadeOut(brl), FadeOut(mm), FadeOut(cur), run_time=0.4)
        zl = SurroundingRectangle(VGroup(sm.b[0], sm.b[1]), color=WARN, buff=0.1, stroke_width=2.5, fill_color=WARN, fill_opacity=0.08)
        zr = SurroundingRectangle(VGroup(sm.b[2], sm.b[3]), color=GOOD, buff=0.1, stroke_width=2.5, fill_color=GOOD, fill_opacity=0.06)
        ll = T("LODS kusuru ilan edilir", 19, WARN, BOLD).move_to([zl.get_x(), -2.15, 0])
        lr = T("hâlâ senkron sayılır · LODS yok", 19, GOOD, BOLD).move_to([zr.get_x(), -2.15, 0])
        ch = s1chip(5, 16)
        ans = VGroup(ch, T("sorusunun tam cevabı", 17, MUTED, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.9, 0])
        self.play(self.set_src("G.989.3 §10.1.1.3 · Tablo 14-3 (LODS)"), run_time=0.3)
        self.at(self.cue("yalnızca av ya da ön senkron", 2.4))
        self.play(FadeIn(zl), FadeIn(ll, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Yeniden senkron hâlâ", 7.6))
        self.play(FadeIn(zr), FadeIn(lr, shift=UP * 0.1), Indicate(sm.b[3], color=GOOD, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("beşinci bölümünde sorduğumuz", 10.9))
        self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        # b8 — robustness up to 1e-3
        self.beat("b8")
        self.clear()
        self.set_badge("neden")
        h = self.show_heading("Tasarım hedefi: 10⁻³'e kadar dayanıklı")
        c1 = card("Yanlış kilitlenme", "rastgele bir bit akışına\nkilitlenmemeli", None, WARN, w=4.2, h=1.45, tsize=21, bsize=18).move_to([-4.3, 1.45, 0])
        c2 = card("Yanlış senkron kaybı", "BER ≤ 10⁻³ iken\nLODS ilan etmemeli", None, WARN, w=4.2, h=1.45, tsize=21, bsize=18).move_to([-4.3, -0.25, 0])
        lk = VGroup(T("10⁻³", 40, GOLD, BOLD), T("= G.989.2 · 10G ↓ referans BER", 18, TXT, BOLD), T("(Tablo 11-4 / 11-5)", 15, MUTED)).arrange(DOWN, buff=0.1).move_to([-4.3, -2.1, 0])
        p = apanel(7.0, 4.6, "Kaba hesap · bağımsız hatalar, BER = 10⁻³", GOLD).move_to([2.95, -0.15, 0])
        rows = VGroup(kv("P(≥ 3 hata / 64 bit)", "≈ 4,0 × 10⁻⁵", kw=3.6), kv("PSync + SFC / çerçeve", "≈ 8,0 × 10⁻⁵", kw=3.6),
                      kv("3 ardışık kötü çerçeve", "≈ 5 × 10⁻¹³", kw=3.6), kv("8000 çerçeve / s ile", "≈ 8 yılda bir", kw=3.6, vcolor=GOOD))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(p[0]).shift(DOWN * 0.15)
        fit(rows, 6.5)
        est = interp("tahmin · türetilmiş — standartta yok", GOLD, 15).next_to(p, DOWN, buff=0.12)
        self.play(self.set_src("G.989.3 §10.1.1.3 · G.989.2 Tablo 11-4/11-5 · hesap: türetilmiş"), run_time=0.3)
        self.at(self.cue("rastgele bir bit akışına", 0.6))
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Bu hata oranı", 14.1))
        self.play(FadeIn(lk[0], scale=0.9), run_time=0.4)
        self.at(self.cue("on gigabitlik aşağı yön referans", 15.2))
        self.play(FadeIn(lk[1:], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Kaba bir hesapla", 20.8))
        self.play(FadeIn(p), FadeIn(est), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[:3]], lag_ratio=0.3), run_time=1.2)
        self.at(self.cue("yılda bir kereden çok daha seyrektir", 24.5))
        self.play(FadeIn(rows[3], shift=RIGHT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # b9 — engineer note
        self.note11("b9", [("1", "PSBd'yi FEC değil, üç mekanizma korur",
                            "64 bitlik birebir PSync eşleşmesi · SFC ve OC üstünde HEC · 0x0F0F… deseni", "PSBd'yi koruyan şey"),
                           ("2", "Analizörde: önce deseni geri alın",
                            "OC XOR 0x0F0F0F0F 0F0F0F0F → sonra HEC; yoksa her HEC başarısız görünür.", "bir protokol analizöründe")])
        self.bridge_beat("b10", "Çerçeveyi bulduk.\nPeki içindeki bitleri ne koruyor?")
        self.save_timeline("ep12_p1C")


# ================================ PERDE 2 ======================================
def xor_sym(r=0.16, color=GOLD, sw=2.5):
    c = Circle(radius=r, color=color, stroke_width=sw)
    return VGroup(c, Line(c.get_left(), c.get_right(), color=color, stroke_width=sw), Line(c.get_top(), c.get_bottom(), color=color, stroke_width=sw))


def cw_row(x0, x1, y, n, color, par_frac, h=0.5, short=None):
    """n equal codeword blocks (data + parity sliver) between x0 and x1; short=(w_frac) appends a short block."""
    tot = n + (short or 0)
    w = (x1 - x0) / tot
    g = VGroup()
    x = x0
    for i in range(n):
        g.add(strip([(w * (1 - par_frac), "", color, 0.16 if i % 2 else 0.26), (w * par_frac, "", PARC, 0.55)], x, y, h))
        x += w
    if short:
        sw_ = w * short
        g.add(strip([(sw_ - w * par_frac, "", GOLD, 0.3), (w * par_frac, "", PARC, 0.55)], x, y, h))
    return g


class E12P2A(Act12):
    HDR, MANIFEST, FIRST = H12[2], M12("p2"), True

    def construct(self):
        # c1 — RS codes
        self.beat("c1")
        tc = self.title_card("PERDE 2", "Koruma katmanları")
        self.at(self.cue("Önce FEC", 2.4))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("FEC — Reed-Solomon, 248 baytlık kod sözcüğü")
        x0, W = -3.4, 9.6
        u = W / 248
        r10 = strip([(216 * u, "216 B veri", R10, 0.2), (32 * u, "32 B", PARC, 0.5)], x0, 1.15, 0.6, 17)
        r25 = strip([(232 * u, "232 B veri", R25, 0.2), (16 * u, "16", PARC, 0.5)], x0, -0.75, 0.6, 15)
        l10 = T("10G · RS(248, 216)", 21, R10, BOLD).move_to([-6.5, 1.15, 0], aligned_edge=LEFT)
        l25 = T("2,5G · RS(248, 232)", 21, R25, BOLD).move_to([-6.5, -0.75, 0], aligned_edge=LEFT)
        br = BraceBetweenPoints([x0, 1.5, 0], [x0 + W, 1.5, 0], UP, color=MUTED)
        brl = T("248 bayt", 18, MUTED, BOLD).next_to(br, UP, buff=0.05)
        t10 = VGroup(T("32 eşlik baytı", 18, PARC, BOLD), T("→ sözcük başına 16 bayt düzeltme", 18, TXT)).arrange(RIGHT, buff=0.2).next_to(r10, DOWN, buff=0.18).align_to(r10, RIGHT)
        t25 = VGroup(T("16 eşlik baytı", 18, PARC, BOLD), T("→ 8 bayt düzeltme", 18, TXT)).arrange(RIGHT, buff=0.2).next_to(r25, DOWN, buff=0.18).align_to(r25, RIGHT)
        z10 = seg(x0 - 7 * u * 2.2, 7 * u * 2.2, 1.15, MUTED, None, 0.6, 0.1, dashed=True)
        z25 = seg(x0 - 7 * u * 2.2, 7 * u * 2.2, -0.75, MUTED, None, 0.6, 0.1, dashed=True)
        zl = VGroup(T("RS(255, 223)", 16, MUTED, BOLD).next_to(z10, UP, buff=0.08), T("RS(255, 239)", 16, MUTED, BOLD).next_to(z25, UP, buff=0.08))
        zl[0].align_to(z10, LEFT)
        zl[1].align_to(z25, LEFT)
        note = VGroup(tag("+ 7 sıfır bayt", MUTED, 18), T("kodlayıcıda başa eklenir · gönderilmez · alıcıda geri eklenir", 18, TXT)).arrange(RIGHT, buff=0.25).move_to([0, -2.45, 0])
        self.play(self.set_src("G.989.3 §10.1.3 · Ek B (= G.987.3 Ek B)"), run_time=0.3)
        self.at(self.cue("Reed Solomon kodları", 3.1))
        self.play(FadeIn(l10), FadeIn(r10[0]), run_time=0.5)
        self.at(self.cue("kod sözcüğü iki yüz kırk sekiz", 6.4))
        self.play(FadeIn(r10[1]), FadeIn(br), FadeIn(brl), run_time=0.5)
        self.at(self.cue("otuz iki eşlik baytı", 14.2))
        self.play(Indicate(r10[1], color=PARC, scale_factor=1.1), FadeIn(t10[0]), run_time=0.5)
        self.at(self.cue("sözcük başına on altı bayt", 16.0))
        self.play(FadeIn(t10[1], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("İki buçuk gigabitte RS", 19.1))
        self.play(FadeIn(l25), FadeIn(r25), run_time=0.5)
        self.at(self.cue("on altı eşlik baytı", 24.1))
        self.play(Indicate(r25[1], color=PARC, scale_factor=1.2), FadeIn(t25[0]), run_time=0.5)
        self.at(self.cue("sekiz bayt düzeltme", 25.8))
        self.play(FadeIn(t25[1], shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("İkisi de iki yüz elli beş", 27.5))
        self.play(FadeIn(z10), FadeIn(z25), FadeIn(zl), run_time=0.6)
        self.at(self.cue("yedi sıfır baytla", 30.9))
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # c2 — cost and net rates
        self.beat("c2")
        self.clear(h)
        h = self.show_heading("Bedel: 10G'de iki kat", h)
        bx0, bw = -4.4, 9.0
        b10 = strip([(bw * (1 - 0.129), "", R10, 0.18), (bw * 0.129, "", PARC, 0.6)], bx0, 1.55, 0.55)
        b25 = strip([(bw * (1 - 0.065), "", R25, 0.18), (bw * 0.065, "", PARC, 0.6)], bx0, 0.75, 0.55)
        bl = VGroup(T("10G", 20, R10, BOLD).next_to(b10, LEFT, buff=0.25), T("2,5G", 20, R25, BOLD).next_to(b25, LEFT, buff=0.25))
        pl = VGroup(T("%12,9", 26, PARC, BOLD).next_to(b10, RIGHT, buff=0.25), T("%6,5", 26, PARC, BOLD).next_to(b25, RIGHT, buff=0.25))
        cap = T("eşlik payı (32 / 248 · 16 / 248)", 16, MUTED, BOLD).next_to(b25, DOWN, buff=0.12).align_to(b25, RIGHT)
        tb = mtable(["FS çerçevesi (net)", "FEC açık", "FEC kapalı"], [["10G", "8,667648 Gbit/s", "9,951744 Gbit/s"], ["2,5G", "2,326016 Gbit/s", "2,486784 Gbit/s"]],
                    [3.0, 3.4, 3.4], size=22, hsize=17, row_h=0.62).move_to([0, -1.45, 0])
        tb[1][1].set_color(R10)
        tb[2][1].set_color(R25)
        self.play(self.set_src("G.989.3 Tablo 8-1 · hızlar: bayt × 8 × 8000 / s (hesaplanmıştır)"), run_time=0.3)
        self.at(self.cue("on gigabitte eşlik payı", 1.8))
        self.play(FadeIn(bl[0]), FadeIn(b10), run_time=0.5)
        self.play(FadeIn(pl[0], shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("yüzde altı virgül beş", 5.9))
        self.play(FadeIn(bl[1]), FadeIn(b25), FadeIn(pl[1], shift=LEFT * 0.1), FadeIn(cap), run_time=0.6)
        self.at(self.cue("Net olarak", 9.4))
        self.play(FadeIn(tb[0]), FadeIn(tb[1][:2]), FadeIn(tb[2][:2]), run_time=0.5)
        self.at(self.cue("sekiz virgül altı altı yedi", 10.3))
        self.play(FadeIn(tb[1][2], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("iki virgül üç iki altı", 16.9))
        self.play(FadeIn(tb[2][2], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("FEC kapalıyken bu sayılar", 22.4))
        self.play(FadeIn(tb[1][3], shift=UP * 0.08), FadeIn(tb[2][3], shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # c3 — codewords in the frame; 2.5G short codeword with 80-byte zero pad
        self.beat("c3")
        self.clear(h)
        h = self.show_heading("Kod sözcükleri çerçevede", h)
        y1, y2 = 1.45, -0.05
        p1 = seg(-6.3, 0.62, y1, PHC, "PSBd", 0.55, 0.6, 14, BG)
        p2 = seg(-6.3, 0.62, y2, PHC, "PSBd", 0.55, 0.6, 14, BG)
        c10 = cw_row(-5.6, 6.3, y1, 16, R10, 0.129, 0.55)
        c25 = cw_row(-5.6, 6.3, y2, 14, R25, 0.065, 0.55, short=0.68)
        lab10 = T("10G: 627 × 248 B = 155 496 B · tam sayı", 18, R10, BOLD).next_to(c10, UP, buff=0.12).align_to(c10, LEFT)
        lab25 = T("2,5G: 156 × 248 B", 18, R25, BOLD).next_to(c25, UP, buff=0.12).align_to(c25, LEFT)
        sh = c25[-1]
        shl = T("+ 168 B kısa sözcük", 18, GOLD, BOLD).next_to(c25, UP, buff=0.12).align_to(c25, RIGHT)
        nf = T("FEC dışı", 15, WARN, BOLD).next_to(p1, DOWN, buff=0.1)
        zx0, zw = -4.6, 10.4
        u = zw / 248
        zz = strip([(80 * u, "80 × 0x00", MUTED, 0.12, True), (152 * u, "152 B veri", GOLD, 0.25), (16 * u, "16", PARC, 0.55)], zx0, -2.2, 0.6, 16)
        zlines = VGroup(DashedLine(sh.get_corner(DL), zz[1].get_corner(UL), color=GOLD, stroke_width=1.5), DashedLine(sh.get_corner(DR), zz[2].get_corner(UR), color=GOLD, stroke_width=1.5))
        b232 = BraceBetweenPoints(zz[0].get_corner(DL), zz[1].get_corner(DR), DOWN, color=MUTED)
        b232l = T("232 B → kodlanır", 16, MUTED, BOLD).next_to(b232, DOWN, buff=0.04)
        st = strike(zz[0], WARN, 3)
        nt = T("gönderilmez", 16, WARN, BOLD).next_to(zz[0], UP, buff=0.08)
        rx = T("ONU: 80 sıfırı geri ekler, sonra çözer", 17, GOOD, BOLD).next_to(b232l, RIGHT, buff=0.6)
        self.play(self.set_src("G.989.3 §10.1.3.1.1 · Ek IV.4"), run_time=0.3)
        self.at(self.cue("Kod sözcükleri PSBd'den sonra", 0.2))
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.4)
        self.at(self.cue("FEC'e dahil değildir", 4.5))
        self.play(FadeIn(nf, shift=UP * 0.08), Indicate(p1, color=WARN), run_time=0.6)
        self.at(self.cue("tam altı yüz yirmi yedi", 6.8))
        self.play(LaggedStart(*[FadeIn(c) for c in c10], lag_ratio=0.05), FadeIn(lab10), run_time=1.0)
        self.at(self.cue("yüz elli altı tam sözcük", 12.2))
        self.play(LaggedStart(*[FadeIn(c) for c in c25[:-1]], lag_ratio=0.05), FadeIn(lab25), run_time=1.0)
        self.at(self.cue("yüz altmış sekiz baytlık kısa", 16.0))
        self.play(FadeIn(sh), FadeIn(shl), run_time=0.5)
        self.at(self.cue("yüz elli iki baytlık verisi", 21.0))
        self.play(Create(zlines), FadeIn(zz[1:]), run_time=0.6)
        self.at(self.cue("başına seksen sıfır bayt", 24.5))
        self.play(FadeIn(zz[0], shift=RIGHT * 0.1), FadeIn(b232), FadeIn(b232l), run_time=0.6)
        self.at(self.cue("bu sıfırlar gönderilmez", 29.7))
        self.play(Create(st), FadeIn(nt), run_time=0.4)
        self.at(self.cue("alıcıda geri eklenir", 31.7))
        self.play(FadeIn(rx, shift=LEFT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # c4 — DS static vs US per-burst
        self.beat("c4")
        self.clear(h)
        h = self.show_heading("FEC: iki yön, iki kural", h)
        lt = tile("↓ aşağı yön · statik", R10, 5.8, 0.6, 20, 0.2).move_to([-3.35, 1.85, 0])
        rt = tile("↑ yukarı yön · burst başına", TW_US, 5.8, 0.6, 20, 0.2).move_to([3.35, 1.85, 0])
        pit = fields(PIT, 5.2, 0.5, 15, 14, show_w=False).move_to([-3.35, 0.85, 0])
        pfl = T("OC · PIT", 15, MUTED, BOLD).next_to(pit, LEFT, buff=0.15)
        fb = glow(pit[2][0], GOLD, 0.05)
        fbt = T("FEC = 1 → bütün ONU'lar için açık", 17, GOLD, BOLD).next_to(pit, DOWN, buff=0.2)
        wc = card("Canlı kanalda değiştirme", "“…can cause intermittent traffic loss …”\naralıklı trafik kaybına yol açabilir", "§10.1.3.1.2", WARN, w=5.9, h=1.55, tsize=20, bsize=17).move_to([-3.35, -1.35, 0])
        tx0 = 0.6
        tl = Line([tx0, 0.55, 0], [6.3, 0.55, 0], color=MUTED, stroke_width=2)
        bs = [(0.1, 1.6, "ONU A", "profil 0 · FEC açık", ACC), (1.85, 1.8, "ONU B", "profil 1 · FEC kapalı", MUTED), (3.8, 1.8, "ONU C", "profil 0 · FEC açık", ACC)]
        bur = VGroup()
        for a, w, n, p, c in bs:
            r = Rectangle(width=w, height=0.6, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.2).move_to([tx0 + a + w / 2, 0.9, 0])
            bur.add(VGroup(r, T(n, 16, TXT, BOLD).move_to(r), fit(T(p, 15, c, BOLD), w + 0.1).next_to(r, DOWN, buff=0.45)))
        tll = T("↑ çerçeve", 15, MUTED, BOLD).next_to(tl, DOWN, buff=0.06).align_to(tl, RIGHT)
        rr = VGroup(tag("her ONU için", TW_US, 18), tag("burst profiliyle (Burst_Profile · F biti)", TW_US, 18), tag("dinamik", TW_US, 18)).arrange(DOWN, buff=0.18).move_to([3.45, -1.45, 0])
        self.play(self.set_src("G.989.3 §10.1.3 · §10.1.3.1.2 · §10.1.3.2.4"), run_time=0.3)
        self.at(self.cue("Aşağı yönde FEC", 5.6))
        self.play(FadeIn(lt, shift=DOWN * 0.1), run_time=0.4)
        self.at(self.cue("statik olarak ya açık", 7.0))
        self.play(FadeIn(pit), FadeIn(pfl), run_time=0.5)
        self.at(self.cue("OC'deki bitle duyurulur", 11.5))
        self.play(Create(fb), FadeIn(fbt, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("canlı bir kanalda", 13.8))
        self.play(FadeIn(wc[0]), FadeIn(wc[1]), run_time=0.5)
        self.at(self.cue("aralıklı trafik kaybına", 19.1))
        self.play(FadeIn(wc[2:]), run_time=0.5)
        self.at(self.cue("Yukarı yönde ise FEC", 24.8))
        self.play(FadeIn(rt, shift=DOWN * 0.1), Create(tl), FadeIn(tll), run_time=0.5)
        self.at(self.cue("her ONU için", 26.6))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.08) for b in bur], lag_ratio=0.2), FadeIn(rr[0]), run_time=0.7)
        self.at(self.cue("burst profiliyle dinamik", 27.7))
        self.play(FadeIn(rr[1:], shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p2A")


class E12P2B(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[2], M12("p2"), "std"

    def construct(self):
        # c5 — BER estimate: FEC decoder vs BIP-32
        self.beat("c5")
        h = self.show_heading("Hata oranı tahmini: hangi sayaç?")
        fr = strip([(0.6, "PSBd", PHC, 0.6), (9.6, "FS çerçevesi (FEC kod sözcükleri)", FSC, 0.12), (1.0, "BIP", BIPC, 0.45)], -5.6, 1.6, 0.6, 16)
        bipl = T("FS kuyruğu · 4 bayt · BIP-32", 16, BIPC, BOLD).next_to(fr[2], DOWN, buff=0.1).align_to(fr[2], RIGHT)

        def path(lbl, c, mid, y):
            a = tag(lbl, c, 19).move_to([-5.3, y, 0])
            b = tile(mid, c, 4.6, 0.6, 18, 0.15).move_to([-1.0, y, 0])
            d = tile("BER tahmini", GOOD, 2.4, 0.6, 18, 0.15).move_to([3.4, y, 0])
            return VGroup(a, arrow(a.get_right(), b.get_left(), MUTED, 2.2, 0.12), b, arrow(b.get_right(), d.get_left(), MUTED, 2.2, 0.12), d)
        pa = path("FEC açık", ACC, "FEC çözücünün düzeltmeleri", 0.25)
        pb = path("FEC kapalı", BIPC, "BIP-32 hataları", -0.75)
        qt = self.quote("G.989.3 §8.1.2.3", "“… the BIP-based BER estimate is applicable only when the FEC is turned off.”",
                        "BIP tabanlı tahmin yalnızca FEC kapalıyken geçerlidir.", width=11.6)
        qt.to_edge(LEFT, buff=0.85).set_y(-2.3)
        self.play(FadeIn(fr), self.set_src("G.989.3 §8.1.1.5 · §8.1.2.3 · Tablo 14-1"), run_time=0.5)
        self.at(self.cue("FEC çözücünün düzeltmelerinden", 1.5))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in pa], lag_ratio=0.2), run_time=1.0)
        self.at(self.cue("Kapalıyken çerçevenin sonundaki", 5.7))
        self.play(Indicate(fr[2], color=GOLD, scale_factor=1.15), FadeIn(bipl), run_time=0.7)
        self.at(self.cue("BIP-32'den", 12.0))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in pb], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("Standart açıkça söyler", 12.9))
        self.play(FadeIn(qt[0]), FadeIn(qt[1]), run_time=0.5)
        self.at(self.cue("yalnızca FEC kapalıyken", 14.8))
        self.play(FadeIn(qt[2], shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # c6 — scrambler polynomial, DS frame-synchronous, preload
        self.beat("c6")
        self.clear(h)
        h = self.show_heading("Karıştırıcı — x⁵⁸ + x³⁹ + 1", h)
        n, cw = 58, 0.17
        rx0 = -4.93
        reg = VGroup(*[Square(cw, stroke_color=PHC, stroke_width=1.2, fill_color=PANEL, fill_opacity=1).move_to([rx0 + cw * (i + 0.5), 1.75, 0]) for i in range(n)])
        rl = VGroup(T("1", 14, MUTED).next_to(reg[0], UP, buff=0.06), T("39", 14, GOLD, BOLD).next_to(reg[38], UP, buff=0.06), T("58", 14, GOLD, BOLD).next_to(reg[57], UP, buff=0.06))
        rgl = T("58 bitlik kaydırma yazmacı", 16, MUTED, BOLD).move_to([rx0, 1.38, 0], aligned_edge=LEFT)
        xs = xor_sym(0.15, GOLD).move_to([reg[57].get_x() + 0.55, 1.0, 0])
        t39 = VGroup(Line(reg[38].get_bottom(), [reg[38].get_x(), 1.0, 0], color=GOLD, stroke_width=2), Line([reg[38].get_x(), 1.0, 0], xs.get_left(), color=GOLD, stroke_width=2))
        t58 = VGroup(Line(reg[57].get_right(), [xs.get_x(), 1.75, 0], color=GOLD, stroke_width=2), Line([xs.get_x(), 1.75, 0], xs.get_top(), color=GOLD, stroke_width=2))
        fb = VMobject(stroke_color=GOLD, stroke_width=2).set_points_as_corners([xs.get_bottom(), [xs.get_x(), 0.72, 0], [rx0 - 0.2, 0.72, 0], [rx0 - 0.2, 1.75, 0], reg[0].get_left()])
        ks = Arrow(xs.get_right(), [6.4, 1.0, 0], buff=0.02, color=GOLD, stroke_width=2.5, tip_length=0.12, max_tip_length_to_length_ratio=0.3)
        ksl = T("anahtar akışı", 15, GOLD, BOLD).move_to([6.05, 1.32, 0])
        y = -0.55
        psb = seg(-6.0, 0.8, y, PHC, "PSBd", 0.6, 0.6, 15, BG)
        pay = seg(-5.2, 11.4, y, FSC, None, 0.6, 0.1)
        scr = scramble(pay[0], 120, 3, PHC)
        rs = VGroup(Line([-5.2, y - 0.45, 0], [-5.2, y + 0.45, 0], color=GOOD, stroke_width=4), T("yeniden yükle", 15, GOOD, BOLD).move_to([-4.2, y + 0.55, 0]))
        run_ = Arrow([-5.1, y - 0.55, 0], [6.2, y - 0.55, 0], buff=0, color=MUTED, stroke_width=2, tip_length=0.12, max_tip_length_to_length_ratio=0.05)
        runl = T("çerçevenin son bitine kadar", 15, MUTED, BOLD).next_to(run_, DOWN, buff=0.05)
        pre = fields([("P1 … P51 = bu çerçevenin SFC'si", 51, SFCC), ("1111111", 7, GOLD)], 11.0, 0.6, 18, 14, unit=" bit").move_to([0.25, -2.35, 0])
        prl = T("ön yükleme", 16, MUTED, BOLD).next_to(pre, LEFT, buff=0.2)
        self.play(self.set_src("G.989.3 §10.1.4.1 · Şekil 10-15"), run_time=0.3)
        self.at(self.cue("Polinom x üzeri", 1.5))
        self.play(LaggedStart(*[FadeIn(c) for c in reg], lag_ratio=0.01), FadeIn(rl), FadeIn(rgl), run_time=0.9)
        self.play(Create(t39), Create(t58), FadeIn(xs), Create(fb), GrowArrow(ks), FadeIn(ksl), run_time=1.0)
        self.at(self.cue("çerçeveye senkrondur", 8.0))
        self.play(FadeIn(psb), FadeIn(pay), run_time=0.5)
        self.at(self.cue("PSBd'den sonraki ilk bitte", 10.5))
        self.play(FadeIn(rs, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.cue("çerçevenin sonuna kadar", 14.2))
        self.play(GrowArrow(run_), FadeIn(runl), LaggedStart(*[Create(l) for l in scr], lag_ratio=0.01), run_time=1.2)
        self.at(self.cue("elli bir biti", 17.1))
        self.play(FadeIn(pre[0]), FadeIn(prl), run_time=0.5)
        self.at(self.cue("kalan yedi bit birdir", 24.6))
        self.play(FadeIn(pre[1], shift=LEFT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # c6a — US burst-synchronous; order framing → FEC → scrambling
        self.beat("c6a")
        self.clear(h)
        h = self.show_heading("Yukarı yön: burst'e senkron", h)
        ds = VGroup(seg(-6.0, 0.8, 1.75, PHC, "PSBd", 0.5, 0.6, 15, BG), seg(-5.2, 1.6, 1.75, BWC, "BWmap", 0.5, 0.3, 15), seg(-3.6, 3.0, 1.75, FSC, "↓ çerçeve k", 0.5, 0.1, 15))
        dsv = HX("SFC = k", 16, SFCC, BOLD).next_to(ds[0], UP, buff=0.08)
        y = 0.3
        bu = VGroup(seg(-1.0, 1.1, y, PHC, "önsöz", 0.6, 0.3, 15), seg(0.1, 0.9, y, PHC, "sın.", 0.6, 0.65, 15, BG), seg(1.0, 5.2, y, TW_US, None, 0.6, 0.1))
        bscr = scramble(bu[2][0], 60, 5, PHC)
        bul = T("↑ PHY burst", 15, MUTED, BOLD).next_to(bu, UP, buff=0.08).align_to(bu, LEFT)
        grant = CurvedArrow(ds[1].get_bottom() + DOWN * 0.05, bu[0].get_left() + LEFT * 0.05, angle=0.6, color=BWC, stroke_width=2.2, tip_length=0.12)
        gl = T("tahsis", 15, BWC, BOLD).next_to(grant, LEFT, buff=0.05).shift(DOWN * 0.15)
        rs = VGroup(Line([1.0, y - 0.45, 0], [1.0, y + 0.45, 0], color=GOOD, stroke_width=4), T("başla", 15, GOOD, BOLD).next_to([1.0, y + 0.45, 0], UP, buff=0.06))
        pv = VGroup(T("ön yükleme:", 16, MUTED, BOLD), HX("SFC = k", 17, SFCC, BOLD), T("(tahsisi gönderen ↓ çerçevenin)", 15, MUTED)).arrange(RIGHT, buff=0.15).move_to([2.35, -0.5, 0])
        steps = [("FS çerçeve / burst", FSC), ("FEC", PARC), ("karıştır", PHC), ("+ PSBd / PSBu", PHC), ("hat", MUTED)]
        pp = VGroup(*[tile(s, c, 2.1 if i < 4 else 0.9, 0.6, 17, 0.18 if i != 3 else 0.5, TXT if i != 3 else BG) for i, (s, c) in enumerate(steps)]).arrange(RIGHT, buff=0.42).move_to([0, -1.75, 0])
        pa = VGroup(*[arrow(pp[i].get_right(), pp[i + 1].get_left(), MUTED, 2.2, 0.12) for i in range(4)])
        nn = T("senkron blokları hiçbir zaman karıştırılmaz", 18, WARN, BOLD).next_to(pp[3], DOWN, buff=0.25)
        self.play(self.set_src("G.989.3 §10.1.4.2 · §10.1.2.2 · §10.1.3.2"), run_time=0.3)
        self.play(FadeIn(ds), FadeIn(dsv), run_time=0.5)
        self.at(self.cue("burst'e senkrondur", 1.5))
        self.play(Create(grant), FadeIn(gl), FadeIn(bu), FadeIn(bul), run_time=0.8)
        self.at(self.cue("sonraki ilk bitte başlar", 4.5))
        self.play(FadeIn(rs, shift=DOWN * 0.1), LaggedStart(*[Create(l) for l in bscr], lag_ratio=0.01), run_time=0.9)
        self.at(self.cue("o burst'ü tahsis eden", 9.3))
        self.play(FadeIn(pv, shift=UP * 0.1), Indicate(dsv, color=SFCC), run_time=0.7)
        self.at(self.cue("Sıra her iki yönde", 13.9))
        self.play(FadeIn(pp[0], shift=RIGHT * 0.1), run_time=0.4)
        for k, (key, d) in enumerate((("sonra FEC", 17.6), ("en son karıştırma", 18.5))):
            self.at(self.cue(key, d))
            self.play(GrowArrow(pa[k]), FadeIn(pp[k + 1], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("Senkron blokları hiçbir", 20.0))
        self.play(GrowArrow(pa[2]), FadeIn(pp[3], shift=RIGHT * 0.1), GrowArrow(pa[3]), FadeIn(pp[4]), FadeIn(nn, shift=UP * 0.08), run_time=0.7)
        self.end(pad=0.05)

        # c7 — PMD bridge: scrambled NRZ and 72-bit CID
        self.beat("c7")
        self.clear()
        self.set_badge("pmd")
        h = self.show_heading("PMD Köprüsü — 72 bitlik CID")
        chips = VGroup(s1chip(4, 16), s1chip(5, 16)).arrange(RIGHT, buff=0.15)
        self.chip_at(chips, h)
        rng = np.random.default_rng(9)
        raw = "1101" + "0" * 46 + "1011"
        scb = "".join("1" if v else "0" for v in rng.integers(0, 2, len(raw)))
        wx0, wx1 = -4.3, 3.2
        tb = (wx1 - wx0) / len(raw)
        w1 = VMobject(stroke_color=WARN, stroke_width=2.4).set_points_as_corners(nrz(raw, wx0, tb, 0.85, 1.65, 0.02))
        w2 = VMobject(stroke_color=GOOD, stroke_width=2.4).set_points_as_corners(nrz(scb, wx0, tb, -0.75, 0.05, 0.02))
        run_ = BraceBetweenPoints([wx0 + 4 * tb, 0.75, 0], [wx0 + 50 * tb, 0.75, 0], DOWN, color=WARN)
        runl = T("uzun özdeş dizi", 16, WARN, BOLD).next_to(run_, DOWN, buff=0.04)
        l1 = T("karıştırılmamış", 17, WARN, BOLD).move_to([-6.45, 1.25, 0], aligned_edge=LEFT)
        l2 = T("karıştırılmış NRZ", 17, GOOD, BOLD).move_to([-6.45, -0.35, 0], aligned_edge=LEFT)
        g2 = VGroup(T("G.989.2 §11.1.2", 15, MUTED, BOLD), T("↓ ve ↑ hat kodu:\nkarıştırılmış NRZ", 17, TXT, BOLD, line_spacing=0.85)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.1, 1.25, 0])
        g3 = VGroup(T("G.989.2 Tablo 11-4 … 11-7", 15, MUTED, BOLD), T("CID bağışıklığı: 72 bit", 17, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.1, -0.35, 0])
        for g in (g2, g3):
            g.align_to(g2, LEFT)
        a = tile("optik tablo · G.989.2 · 72 bit CID", PMDC, 5.2, 0.62, 18, 0.15).move_to([-3.2, -2.3, 0])
        b = tile("TC katmanı · G.989.3 · x⁵⁸ + x³⁹ + 1", PHC, 5.2, 0.62, 18, 0.15).move_to([3.2, -2.3, 0])
        ab = DoubleArrow(a.get_right(), b.get_left(), buff=0.08, color=ACC, stroke_width=3, tip_length=0.14)
        abl = T("birbirine dayanır", 16, ACC, BOLD).next_to(ab, UP, buff=0.08)
        self.play(FadeIn(chips, shift=LEFT * 0.1), self.set_src("G.989.2 §11.1.2 · Tablo 11-4…11-7 · G.989.3 §6.1.3.3"), run_time=0.5)
        self.at(self.cue("karıştırılmış NRZ olarak", 1.0))
        self.play(FadeIn(l2), Create(w2), FadeIn(g2, shift=LEFT * 0.1), run_time=0.9)
        self.at(self.cue("yetmiş iki bitlik ardışık", 6.9))
        self.play(FadeIn(g3, shift=LEFT * 0.1), run_time=0.5)
        self.play(FadeIn(l1), Create(w1), FadeIn(run_), FadeIn(runl), run_time=0.9)
        self.at(self.cue("iletimi rastgeleleştirir", 13.3))
        self.play(Indicate(w2, color=GOOD, scale_factor=1.02), w1.animate.set_stroke(opacity=0.45), run_time=0.7)
        self.at(self.cue("Optik tablo ile TC", 19.7))
        self.play(FadeIn(a, shift=RIGHT * 0.1), FadeIn(b, shift=LEFT * 0.1), GrowFromCenter(ab), FadeIn(abl), run_time=0.7)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p2B")


A4 = [["hata yok", "hatasız · OK", "eşlik biti hatası · OK"],
      ["tek hata", "tek BCH + eşlik hatası · düzeltilir", "tek BCH hatası · düzeltilir"],
      ["çift hata", "çift BCH hatası · düzeltilir", "üçlü hata · DÜZELTİLEMEZ"],
      ["düzeltilemez", "çoklu hata · düzeltilemez", "çoklu hata · düzeltilemez"]]


class E12P2C(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[2], M12("p2"), "std"

    def construct(self):
        # c8 — two HEC sizes
        self.beat("c8")
        h = self.show_heading("HEC — iki boy")
        f64 = fields([("korunan alan", 51, ACC), ("BCH", 12, HECC), ("P", 1, GOLD)], 12.0, 0.6, 19, 14, unit=" bit").move_to([0.3, 1.75, 0])
        l64 = T("64 bit", 22, ACC, BOLD).next_to(f64, LEFT, buff=0.2)
        u64 = VGroup(*[tag(s, ACC, 17) for s in ("SFC", "OC", "BWmap tahsis yapısı", "XGEM başlığı")]).arrange(RIGHT, buff=0.2).move_to([0.3, 0.65, 0])
        z32 = seg(-5.7, 6.0, -0.65, MUTED, "32 sıfır bit · gönderilmez", 0.6, 0.08, 16, MUTED, dashed=True)
        f32 = fields([("19 bit", 19, R25), ("BCH", 12, HECC), ("P", 1, GOLD)], 6.0, 0.6, 18, 14, show_w=False).move_to([3.3, -0.65, 0])
        l32 = T("32 bit", 22, R25, BOLD).next_to(z32, LEFT, buff=0.2)
        u32 = VGroup(*[tag(s, R25, 17) for s in ("HLend (↓ FS başlığı)", "↑ FS başlığı")]).arrange(RIGHT, buff=0.2).move_to([3.3, -1.55, 0])
        bch = VGroup(T("BCH(63, 12, 2)", 20, HECC, BOLD), T("g(x) = x¹² + x¹⁰ + x⁸ + x⁵ + x⁴ + x³ + 1", 20, TXT), T("+ 1 çift eşlik biti", 20, GOLD, BOLD)).arrange(RIGHT, buff=0.35).move_to([0, -2.6, 0])
        fit(bch, 12.6)
        self.play(self.set_src("G.989.3 Ek A.1 · Şekil A.1"), run_time=0.3)
        self.at(self.cue("İki boyu vardır", 3.0))
        self.play(FadeIn(l64), FadeIn(f64), run_time=0.5)
        self.at(self.cue("elli bir bitlik bir alanı", 5.5))
        self.play(Indicate(f64[0], color=ACC, scale_factor=1.03), run_time=0.5)
        self.at(self.cue("sayaç", 9.2))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.08) for t in u64], lag_ratio=0.25), run_time=0.9)
        self.at(self.cue("Otuz iki bitlik biçim", 14.9))
        self.play(FadeIn(l32), FadeIn(f32), run_time=0.5)
        self.at(self.cue("on dokuz bitlik bir alanı", 16.5))
        self.play(FadeIn(z32), run_time=0.5)
        self.at(self.cue("çerçeve başlığı ve ONU'nun", 19.4))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.08) for t in u32], lag_ratio=0.3), run_time=0.7)
        self.at(self.cue("on iki bitlik bir BCH", 23.3))
        self.play(FadeIn(bch, shift=UP * 0.08), Indicate(VGroup(f64[1], f64[2], f32[1], f32[2]), color=GOLD, scale_factor=1.05), run_time=0.8)
        self.end(pad=0.05)

        # c9 — Table A.4
        self.beat("c9")
        self.clear(h)
        h = self.show_heading("Tablo A.4 — HEC çözüm sonucu", h)
        top = VGroup(tag("BCH: 2 hatayı düzeltir", GOOD, 19), tag("3 hatayı algılar", GOLD, 19)).arrange(RIGHT, buff=0.3).move_to([0, 1.95, 0])
        tb = table(["BCH sonucu", "eşlik geçer", "eşlik başarısız"], A4, [2.8, 4.7, 4.7], size=19, hsize=17, row_h=0.62).move_to([0, -0.55, 0])
        for r in tb[1:]:
            for c in r[2:]:
                c.set_color(WARN if "düzeltilemez" in c.text.lower() or "DÜZELTİLEMEZ" in c.text else GOOD)
        hl = SurroundingRectangle(tb[3][3], color=WARN, buff=0.06, stroke_width=3.5)
        self.play(self.set_src("G.989.3 Ek A.1 · Tablo A.4"), run_time=0.3)
        self.play(FadeIn(top[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("üç hatayı algılar", 2.4))
        self.play(FadeIn(top[1], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("Eşlik biti kodla birlikte", 4.0))
        self.play(FadeIn(tb[0]), run_time=0.4)
        self.at(self.cue("hata yok", 6.7))
        self.play(FadeIn(tb[1]), run_time=0.4)
        self.at(self.cue("tek hata", 7.5))
        self.play(FadeIn(tb[2][:2]), FadeIn(tb[2][3]), run_time=0.4)
        self.at(self.cue("çift hata düzeltilebilir", 8.3))
        self.play(FadeIn(tb[3][:3]), run_time=0.4)
        self.at(self.cue("tek bir BCH hatası ile eşlik", 10.4))
        self.play(FadeIn(tb[2][2], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("Ama çift BCH hatası", 15.7))
        self.play(FadeIn(tb[3][3], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("üçlü bir hatadır", 20.3))
        self.play(Create(hl), run_time=0.5)
        self.at(self.cue("dört durumu bir tabloda", 23.4))
        self.play(FadeIn(tb[4]), run_time=0.4)
        self.end(pad=0.05)

        # c10 — history: ASCII credits in Annex A, Annex B one sentence
        self.beat("c10")
        self.clear(h)
        h = self.show_heading("Tarih notu — XG-PON mirası", h)
        p = apanel(6.4, 2.6, "Tablo A.2 · 64 bitlik test sözcükleri → ASCII", ACC).move_to([-3.25, 0.9, 0])
        lines = VGroup(HX("XG-PON was produced", 20, TXT, BOLD), HX("thanks to …", 20, TXT, BOLD), T("(XG-PON editörlerinin adları)", 15, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lines.move_to(p[0]).shift(DOWN * 0.2)
        cb = card("Ek B — tek cümle", "“This is the same as Annex B\nof [ITU-T G.987.3].”", "FEC polinomları: G.987.3'te", PARC, w=5.9, h=2.0, tsize=21, bsize=19).move_to([3.3, 0.9, 0])
        names = [("G.987.3 · XG-PON", MUTED), ("G.989.3 · 2015", ACC), ("2021 · Ed. 2.0", ACC), ("Amd.1 · 2023", GOLD), ("Amd.2 · 2025", GOLD)]
        ch = VGroup(*[tile(s, c, 2.15, 0.55, 16, 0.15) for s, c in names]).arrange(RIGHT, buff=0.33).move_to([0, -1.35, 0])
        ca = VGroup(*[arrow(ch[i].get_right(), ch[i + 1].get_left(), MUTED, 2, 0.1) for i in range(4)])
        same = VGroup(*[T("değişiklik yok", 15, GOOD, BOLD).next_to(ch[i], DOWN, buff=0.12) for i in (3, 4)])
        cap = T("§8 · §10 · Ek A · Ek B · Ek III · Ek IV: 2021'den beri aynı", 17, GOOD, BOLD).move_to([0, -2.6, 0])
        self.play(self.set_src("G.989.3 Ek A (Tablo A.2 / A.3) · Ek B · Amd.1 / Amd.2"), run_time=0.3)
        self.at(self.cue("A ekindeki HEC test vektörleri", 1.8))
        self.play(FadeIn(p), run_time=0.5)
        self.at(self.cue("ASCII olarak okunduğunda", 4.4))
        self.play(FadeIn(lines[0], shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("editörlere teşekkür eden", 6.5))
        self.play(FadeIn(lines[1:], shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("B eki ise tek cümledir", 11.3))
        self.play(FadeIn(cb[0]), FadeIn(cb[1]), run_time=0.5)
        self.at(self.cue("G.987.3'ün B ekiyle aynıdır", 13.2))
        self.play(FadeIn(cb[2:]), run_time=0.5)
        self.at(self.cue("XG-PON'dan miras kalmıştır", 15.6))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in ch[:3]], lag_ratio=0.25), LaggedStart(*[GrowArrow(a) for a in ca[:2]], lag_ratio=0.25), run_time=0.9)
        self.at(self.cue("iki bin yirmi üç ve iki bin yirmi beş", 20.4))
        self.play(GrowArrow(ca[2]), FadeIn(ch[3]), GrowArrow(ca[3]), FadeIn(ch[4]), FadeIn(same), run_time=0.7)
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # c11 — engineer note
        self.note11("c11", [("1", "10G'de FEC açmak: kapasitenin 1/8'inden fazlası",
                             "%12,9 > %12,5 — ama G.989.2'nin 10⁻³ referans BER'i FEC varsayar.", "on gigabitte FEC'i açmak"),
                            ("2", "XG-PON kodunu yeniden kullanırken dikkat",
                             "Bu katman G.987.3 ile birebir aynı; başka yerlerde küçük farklar var.", "altyapı kodunuzu")])
        self.bridge_beat("c12", "Bitler korunuyor.\nPeki aşağı yön çerçevesinin içinde ne taşınıyor?")
        self.save_timeline("ep12_p2C")
