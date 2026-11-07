"""S2·B2 · Laboratuvarda (Ek IV altın vektörleri, HEC, karıştırıcı, çerçeve çözücü, senkron, sayaçlar, BWmap, burst) and Kapanış."""
from ep12_common import *

IV = [["IV.1", "10G · RS(248, 216) · tam", "01 … D8 (216 B)", "6d 8d 89 21 … 18 1a"],
      ["IV.2", "10G · ↑ kısa sözcük", "01 … CC (204 B)", "a5 2c aa 6d … 8d 7d"],
      ["IV.3", "2,5G · RS(248, 232) · tam", "01 … E8 (232 B)", "41 42 da e0 … ee bf"],
      ["IV.4", "2,5G · ↓ 157. kısa sözcük", "01 … 98 (152 B)", "c5 28 62 d3 … 84 4e"],
      ["IV.5", "2,5G · ↑ kısa sözcük", "01 … CC (204 B)", "1e e8 d8 c6 … 13 93"]]
A51 = ["0000000000001FC00000003F", "8007F0007F0000000102001F", "C00204007F0003F8"]


def doc_icon(w=2.2, h=1.6, title="Ek IV", lines=("altın vektörler", "IV.1 … IV.12")):
    r = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - 0.3, 0], [w / 2 - 0.3, h / 2, 0], [-w / 2, h / 2, 0],
                stroke_color=GOLD, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    g = VGroup(T(title, 20, GOLD, BOLD), *[T(s, 15, TXT, BOLD) for s in lines]).arrange(DOWN, buff=0.08).move_to(r)
    return VGroup(r, g)


class E12LabA(Act12):
    HDR, MANIFEST, FIRST = H12["L"], M12("lab"), True

    def construct(self):
        # g1 — bench: analyzer, OLT emulator, Appendix IV golden vectors
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Altın vektörler")
        self.at(self.cue("Bu bölümün düzeneği", 1.2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Düzenek")
        pa = pa_icon(2.5, 1.7).move_to([-4.6, 1.15, 0])
        em = emu_icon(2.5, 1.7).move_to([-1.3, 1.15, 0])
        dut = onu_box("ONU (DUT)", ONUC, 1.9, 0.75, 18).move_to([1.8, 1.25, 0])
        dc = doc_icon().move_to([5.0, 1.15, 0])
        y = -1.75
        fl = VGroup(tile("bilinen giriş", MUTED, 2.3, 0.62, 18, 0.12), tile("uygulama (DUT)", ONUC, 2.5, 0.62, 18, 0.15),
                    tile("çıkış", MUTED, 1.5, 0.62, 18, 0.12), tile("vektördeki çıkış", GOLD, 2.6, 0.62, 18, 0.15)).arrange(RIGHT, buff=0.55).move_to([-0.3, y, 0])
        fa = VGroup(arrow(fl[0].get_right(), fl[1].get_left(), MUTED, 2.2, 0.12), arrow(fl[1].get_right(), fl[2].get_left(), MUTED, 2.2, 0.12))
        eq = T("=?", 24, GOLD, BOLD).move_to((fl[2].get_right() + fl[3].get_left()) / 2)
        ok = T("bit bit aynı ✓", 19, GOOD, BOLD).next_to(fl, DOWN, buff=0.25)
        dl = T("altın vektör:", 18, GOLD, BOLD).next_to(fl, UP, buff=0.22).align_to(fl, LEFT)
        self.play(self.set_src("G.989.3 Ek IV · tezgâh seçimi: yorum"), run_time=0.3)
        self.at(self.cue("bir protokol analizörü", 2.6))
        self.play(FadeIn(pa, shift=UP * 0.1), FadeIn(dut), run_time=0.6)
        self.at(self.cue("bir OLT emülatörü", 4.8))
        self.play(FadeIn(em, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("dördüncü ekindeki altın", 7.0))
        self.play(FadeIn(dc, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("Altın vektörler", 10.2))
        self.play(FadeIn(dl), FadeIn(fl[0]), GrowArrow(fa[0]), FadeIn(fl[1]), GrowArrow(fa[1]), FadeIn(fl[2]), run_time=0.9)
        self.at(self.cue("hazır giriş ve çıkış", 15.5))
        self.play(FadeIn(eq), FadeIn(fl[3], shift=LEFT * 0.1), FadeIn(ok, shift=UP * 0.08), run_time=0.6)
        self.end(pad=0.05)

        # g2 — FEC encoder against IV.1 – IV.5
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "FEC kodlayıcı — Ek IV.1 – IV.5")
        tb = mtable(["vektör", "kod sözcüğü", "yük", "eşlik (ilk 4 … son 2 bayt)"], IV, [1.2, 4.2, 3.0, 4.2], size=18, hsize=15, row_h=0.5, mono=(2, 3)).move_to([0, 0.7, 0])
        for r in tb[1:]:
            r[2].set_color(R10 if r[2].text.startswith("10G") else R25)
            r[4].set_color(PARC)
        y = -2.15
        fl = VGroup(tile("yük", MUTED, 1.3, 0.6, 18, 0.12), tile("kodlayıcı (DUT)", ONUC, 2.6, 0.6, 18, 0.15), tile("eşlik", PARC, 1.4, 0.6, 18, 0.2),
                    tile("Ek IV'teki eşlik", GOLD, 2.6, 0.6, 18, 0.15)).arrange(RIGHT, buff=0.55).move_to([-0.9, y, 0])
        fa = VGroup(arrow(fl[0].get_right(), fl[1].get_left(), MUTED, 2.2, 0.12), arrow(fl[1].get_right(), fl[2].get_left(), MUTED, 2.2, 0.12))
        eq = T("=?", 22, GOLD, BOLD).move_to((fl[2].get_right() + fl[3].get_left()) / 2)
        ok = T("bayt bayt aynı ✓", 19, GOOD, BOLD).next_to(fl, RIGHT, buff=0.3)
        self.play(self.set_src("G.989.3 Ek IV.1 – IV.5"), run_time=0.3)
        self.at(self.cue("Ekteki beş vektör", 2.1))
        self.play(FadeIn(tb[0]), run_time=0.4)
        for k, (key, d, rows) in enumerate((("on gigabitlik tam ve kısa", 3.6, (1, 2)), ("iki buçuk gigabitlik tam", 7.0, (3,)),
                                            ("yüz elli yedinci kısa", 10.5, (4,)), ("yukarı yönün kısa sözcüğünü", 13.5, (5,)))):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(tb[i], shift=UP * 0.06) for i in rows], run_time=0.45)
        self.at(self.cue("Yükü kodlayıcıya verin", 16.6))
        self.play(FadeIn(fl[0]), GrowArrow(fa[0]), FadeIn(fl[1]), GrowArrow(fa[1]), FadeIn(fl[2]), run_time=0.8)
        self.at(self.cue("bayt bayt aynı olmalıdır", 18.5))
        self.play(FadeIn(eq), FadeIn(fl[3], shift=LEFT * 0.1), FadeIn(ok, shift=LEFT * 0.08), run_time=0.6)
        self.end(pad=0.05)

        # g3 — the polynomials are not in G.989.3; reproduced from the vectors
        self.beat("g3")
        self.clear(h)
        h = step_head(self, 1, "FEC — polinomlar nerede?", h)
        cb = card("G.989.3 Ek B (tamamı)", "“This is the same as Annex B\nof [ITU-T G.987.3].”", "→ alan ve üreteç polinomu bu metinde yok", PARC, w=5.4, h=2.1, tsize=20, bsize=18).move_to([-3.6, 0.85, 0])
        p = apanel(6.6, 3.0, "Yeniden üretilen RS parametreleri", GOLD).move_to([3.25, 0.85, 0])
        rows = VGroup(kv("cisim", "GF(2⁸)", kw=2.0), kv("ilkel polinom", "x⁸+x⁴+x³+x²+1 (0x11D)", kw=2.0), kv("α", "0x02", kw=2.0),
                      kv("üreteç", "∏(x − αⁱ), i = 0 … 2t−1", kw=2.0), kv("kök sayısı", "10G: 32 · 2,5G: 16", kw=2.0)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(rows, 6.2).move_to(p[0]).shift(DOWN * 0.2)
        est = interp("türetilmiş — vektörlerden; standartta yazılı değil", GOLD, 16).next_to(p, DOWN, buff=0.12)
        chk = VGroup(*[VGroup(tag(f"IV.{i}", GOLD, 17), T("✓", 22, GOOD, BOLD)).arrange(RIGHT, buff=0.1) for i in range(1, 6)]).arrange(RIGHT, buff=0.35)
        tot = T("5 / 5 tutuyor", 22, GOOD, BOLD)
        cr = VGroup(chk, tot).arrange(RIGHT, buff=0.5).move_to([0, -2.45, 0])
        self.play(self.set_src("G.989.3 Ek B · Ek IV.1 – IV.5 · parametreler türetilmiştir"), run_time=0.3)
        self.at(self.cue("polinomlarını yazmaz", 0.8))
        self.play(FadeIn(cb[0]), FadeIn(cb[1]), run_time=0.5)
        self.at(self.cue("G.987.3'e atıf yapar", 3.9))
        self.play(FadeIn(cb[2:]), run_time=0.5)
        self.at(self.cue("Ama beş vektör", 5.7))
        self.play(FadeIn(p), run_time=0.4)
        self.at(self.cue("Galois cisminde", 8.5))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.08) for r in rows], lag_ratio=0.2), run_time=1.2)
        self.at(self.cue("Biz bunu yaptık", 16.6))
        self.play(FadeIn(est, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("beş vektörün beşi de tutuyor", 18.0))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in chk], lag_ratio=0.12), FadeIn(tot), run_time=0.8)
        self.end(pad=0.05)

        # g4 — decoder: inject symbol errors
        self.beat("g4")
        self.clear(h)
        h = step_head(self, 1, "FEC çözücü — sembol hatası ekle", h)
        cols, rows_ = 31, 8
        cs = 0.2
        grid = VGroup(*[Square(cs, stroke_color=PAYC if i < 216 else PARC, stroke_width=1, fill_color=PAYC if i < 216 else PARC, fill_opacity=0.18)
                        for i in range(248)])
        grid.arrange_in_grid(rows=rows_, cols=cols, buff=0.025).move_to([-2.8, 0.55, 0])
        gl = T("1 kod sözcüğü = 248 sembol (bayt)", 16, MUTED, BOLD).next_to(grid, UP, buff=0.12).align_to(grid, LEFT)
        rng = np.random.default_rng(12)
        idx = rng.choice(248, 17, replace=False)
        errs16 = VGroup(*[grid[i].copy().set_fill(WARN, 0.85).set_stroke(WARN) for i in idx[:16]])
        err17 = grid[idx[16]].copy().set_fill(WARN, 0.85).set_stroke(WARN)
        p = apanel(5.4, 2.6, "Çözücü sonucu", ACC).move_to([3.6, 0.55, 0])
        r1 = VGroup(tag("10G · t = 16", R10, 17), T("≤ 16 hata → düzeltilir ✓", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        r2 = VGroup(tag("2,5G · t = 8", R25, 17), T("≤ 8 hata → düzeltilir ✓", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        r3 = VGroup(tag("t + 1", WARN, 17), T("17 / 9 hata → düzeltilemez", 18, WARN, BOLD)).arrange(RIGHT, buff=0.2)
        rr = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        fit(rr, 5.0).move_to(p[0]).shift(DOWN * 0.2)
        ctr = VGroup(T("Düzeltilemeyen FEC kod sözcükleri", 18, TXT, BOLD), HX("+1", 24, WARN, BOLD)).arrange(RIGHT, buff=0.3)
        ctrb = SurroundingRectangle(ctr, color=WARN, buff=0.15, corner_radius=0.1)
        cg = VGroup(ctrb, ctr).move_to([0, -2.3, 0])
        ctl = T("Tablo 14-1 PM sayacı", 15, MUTED).next_to(cg, RIGHT, buff=0.2)
        self.play(self.set_src("G.989.3 §10.1.3 · Tablo 14-1 · t = (n − k) / 2"), FadeIn(grid), FadeIn(gl), run_time=0.6)
        self.at(self.cue("rastgele sembol hataları", 1.1))
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in errs16[:6]], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("On gigabitte on altıya", 5.4))
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in errs16[6:]], lag_ratio=0.08), FadeIn(p), FadeIn(r1, shift=RIGHT * 0.08), run_time=0.9)
        self.at(self.cue("iki buçuk gigabitte sekize", 7.3))
        self.play(FadeIn(r2, shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("Bir fazlası", 11.8))
        self.play(FadeIn(err17, scale=0.4), FadeIn(r3, shift=RIGHT * 0.08), grid.animate.set_stroke(WARN, opacity=0.6), run_time=0.6)
        self.at(self.cue("düzeltilemeyen kod sözcüğü sayacını", 12.8))
        self.play(FadeIn(cg, shift=UP * 0.08), FadeIn(ctl), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_labA")


class E12LabB(Act12):
    HDR, MANIFEST, PREV_BADGE = H12["L"], M12("lab"), "lab"

    def construct(self):
        # g5 — HEC unit test
        self.beat("g5")
        h = step_head(self, 2, "HEC — Ek A test sözcükleri")
        a2 = tile("Tablo A.2 · 33 × 64 bit", ACC, 3.6, 0.6, 18, 0.15)
        a3 = tile("Tablo A.3 · 24 × 32 bit", R25, 3.6, 0.6, 18, 0.15)
        aa = VGroup(a2, a3).arrange(DOWN, buff=0.2).move_to([-4.4, 1.35, 0])
        a57 = T("57 sözcük → hatasız ✓", 20, GOOD, BOLD).next_to(aa, DOWN, buff=0.25)
        rng = np.random.default_rng(5)
        w = "".join("1" if v else "0" for v in rng.integers(0, 2, 64))
        bc = bitcells(w, 7.0, 0.32, ACC).move_to([2.9, 1.65, 0])
        bl = T("64 bitlik sözcük (51 + 12 + P)", 15, MUTED, BOLD).next_to(bc, UP, buff=0.1).align_to(bc, LEFT)
        fl = [5, 22, 40]
        flips = VGroup(*[SurroundingRectangle(bc[i], color=WARN, buff=0.03, stroke_width=3) for i in fl])
        pf = SurroundingRectangle(bc[63], color=GOLD, buff=0.03, stroke_width=3)
        res = table(["çevrilen", "Tablo A.4 durumu", "sonuç"], [["1 bit", "tek BCH (+ eşlik) hatası", "düzeltilir ✓"], ["2 bit", "çift BCH hatası", "düzeltilir ✓"],
                                                               ["yalnız eşlik biti", "eşlik biti hatası", "OK ✓"], ["3 bit · eşlik ✗", "üçlü hata", "DÜZELTİLEMEZ ✗"]],
                    [3.0, 4.2, 3.2], size=18, hsize=15, row_h=0.5).move_to([1.35, -1.25, 0])
        for i, r in enumerate(res[1:]):
            r[3].set_color(WARN if i == 3 else GOOD)
        hl = SurroundingRectangle(res[4], color=WARN, buff=0.04, stroke_width=3)
        self.play(self.set_src("G.989.3 Ek A.1 · Tablo A.2 / A.3 / A.4"), run_time=0.3)
        self.at(self.cue("elli yedi test sözcüğü", 1.4))
        self.play(FadeIn(aa, shift=RIGHT * 0.08), run_time=0.5)
        self.play(FadeIn(a57, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("Sonra bir", 6.0))
        self.play(FadeIn(bl), FadeIn(bc), Create(flips[0]), run_time=0.5)
        self.at(self.cue("iki ve üç bit çevirin", 6.9))
        self.play(Create(flips[1]), run_time=0.3)
        self.play(Create(flips[2]), run_time=0.3)
        self.at(self.cue("eşlik bitini de", 8.7))
        self.play(Create(pf), run_time=0.4)
        self.at(self.cue("dört durumun tablosuyla", 11.0))
        self.play(FadeIn(res[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.06) for r in res[1:4]], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("Üç bit hata ile eşlik", 14.2))
        self.play(FadeIn(res[4], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("düzeltilemez olarak", 17.3))
        self.play(Create(hl), run_time=0.4)
        self.end(pad=0.05)

        # g6 — scrambler from SFC = 0, Table A.5
        self.beat("g6")
        self.clear(h)
        h = step_head(self, 3, "Karıştırıcı — Ek A.2", h)
        e = apanel(4.6, 1.6, "OLT emülatörü", GOLD).move_to([-4.3, 1.45, 0])
        ev = kv("SFC", "0x0 0000 0000 0000", ksize=17, vsize=17, kw=0.8).move_to(e[0]).shift(DOWN * 0.18)
        fit(ev, 4.2)
        p = apanel(7.4, 2.25, "ilk 256 karıştırıcı biti · PSBd'den sonra", ACC).move_to([2.5, 1.2, 0])
        hx = VGroup(*[HX(s, 20, TXT, BOLD) for s in A51]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fit(hx, 7.0).move_to(p[0]).shift(DOWN * 0.2)
        first = format(int(A51[0][:16], 16), "064b")
        bc = bitcells(first, 9.6, 0.3, GOLD).move_to([0.4, -0.75, 0])
        b51 = brace_lbl(bc[:51], "51 bit = SFC (hepsi 0)", SFCC, DOWN, 16)
        b7 = brace_lbl(bc[51:58], "7 × 1", GOLD, DOWN, 16)
        bcl = T("ilk 64 bit", 15, MUTED, BOLD).next_to(bc, LEFT, buff=0.2)
        ok = pill("Tablo A.5 ile aynı ✓", GOOD, 19).move_to([4.6, -2.45, 0])
        nt = VGroup(T("SFC'yi küçük değerle başlatmak: §15.4.3 NOT →", 17, TXT, BOLD), s2chip(8, 16)).arrange(RIGHT, buff=0.2).move_to([-2.2, -2.45, 0])
        fit(nt, 7.8)
        self.play(self.set_src("G.989.3 Ek A.2 · Tablo A.5 · §10.1.4.1 · §15.4.3"), run_time=0.3)
        self.at(self.cue("süper çerçeve sayacını sıfıra", 2.0))
        self.play(FadeIn(e), FadeIn(ev), run_time=0.5)
        self.at(self.cue("ilk iki yüz elli altı", 6.3))
        self.play(FadeIn(p), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.08) for x in hx], lag_ratio=0.25), run_time=0.9)
        self.play(FadeIn(bcl), FadeIn(bc), FadeIn(b51), FadeIn(b7), run_time=0.7)
        self.at(self.cue("A ekindeki tabloyla aynı", 11.0))
        self.play(FadeIn(ok, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("Sayacı küçük bir değerle", 13.9))
        self.play(FadeIn(nt[0]), run_time=0.5)
        self.at(self.cue("şifreleme bölümünde", 16.8))
        self.play(FadeIn(nt[1], shift=LEFT * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # g7 — downstream frame decoder
        self.beat("g7")
        self.clear(h)
        h = step_head(self, 4, "Çerçeve çözücü", h)
        pl = apanel(5.6, 3.2, "Analizör · ↓ çözücü", ACC).move_to([-3.6, 0.65, 0])
        steps = VGroup(ok_line("PSync kilidi", True, 18), ok_line("SFC: n → n + 1 → n + 2", True, 18), ok_line("SFC / OC: XOR 0x0F0F… geri alındı", True, 18))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(pl[0]).shift(DOWN * 0.2)
        fit(steps, 5.2)
        pr = apanel(6.6, 3.2, "OC · çözülen alanlar (örnek değerler)", GOLD).move_to([3.2, 0.65, 0])
        kvs = VGroup(kv("PON-ID", "0x1234 5673", kw=1.9), kv("DWLCH ID", "0011 → kanal 4", kw=1.9), kv("ODN sınıfı", "001 → N2", kw=1.9),
                     kv("↓ FEC", "1 → açık", kw=1.9), kv("TOL", "0x14A → +3,0 dBm", kw=1.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        fit(kvs, 6.1).move_to(pr[0]).shift(DOWN * 0.2)
        hlx = VGroup(tag("HLend", HLC, 18), HX("N = 64 · P = 2", 19, TXT, BOLD), T("→", 22, MUTED, BOLD), T("8N + 48P + 8 = 616 B ≤ 135 432 B", 20, GOOD, BOLD), T("✓", 22, GOOD, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -1.9, 0])
        fit(hlx, 12.6)
        hln = T("FS çerçeve boyu (Tablo 8-1, 10G FEC açık)", 15, MUTED).next_to(hlx, DOWN, buff=0.1).align_to(hlx[3], LEFT)
        self.play(self.set_src("G.989.3 §10.1.1 · Şekil 10-3 · §8.1.1.1 · Tablo 8-1"), run_time=0.3)
        self.at(self.cue("Senkron desenine kilitlenin", 2.5))
        self.play(FadeIn(pl), FadeIn(steps[0], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("sayacın her çerçevede", 4.8))
        self.play(FadeIn(steps[1], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("sıfır ef desenini geri alın", 8.8))
        self.play(FadeIn(steps[2], shift=RIGHT * 0.08), FadeIn(pr), run_time=0.5)
        for k, (key, d) in enumerate((("PON kimliği", 12.5), ("kanal kimliği", 13.5), ("ODN sınıfı", 14.7), ("FEC biti", 15.6), ("TOL", 16.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(kvs[k], shift=RIGHT * 0.08), run_time=0.3)
        self.at(self.cue("HLend'den N ve P", 16.9))
        self.play(FadeIn(hlx[:2], shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("sekiz N artı kırk sekiz P", 19.5))
        self.play(FadeIn(hlx[2:], shift=RIGHT * 0.08), FadeIn(hln), run_time=0.6)
        self.end(pad=0.05)

        # g8 — sync machine stress with an error injector
        self.beat("g8")
        self.clear(h)
        h = step_head(self, 5, "Senkron makinesi — hata enjeksiyonu", h)
        inj = tile("hata enjektörü → PSync", WARN, 3.6, 0.6, 18, 0.15).move_to([-4.4, 1.75, 0])
        errs = [0, 2, 3, 3, 3]
        st = ["Senkron", "Senkron", "Yeniden s.", "Yeniden s.", "Av · LODS"]
        sc = [GOOD, GOOD, GOLD, GOLD, WARN]
        frs = VGroup()
        for i, (e_, s_, c) in enumerate(zip(errs, st, sc)):
            r = Rectangle(width=2.2, height=0.62, stroke_color=WARN if e_ >= 3 else (GOLD if e_ else MUTED), stroke_width=2,
                          fill_color=WARN if e_ >= 3 else PANEL, fill_opacity=0.15 if e_ >= 3 else 1)
            lab = T(f"PSync: {e_} bit ✗" if e_ else "PSync: hatasız", 16, TXT, BOLD).move_to(r)
            ss = tile(s_, c, 2.0, 0.5, 16, 0.18).next_to(r, DOWN, buff=0.35)
            frs.add(VGroup(r, lab, ss))
        frs.arrange(RIGHT, buff=0.18).move_to([0, 0.35, 0])
        ok2 = T("≥ 62/64 → değişmez", 15, GOOD, BOLD).next_to(frs[1][0], UP, buff=0.12)
        o5 = sbox("O5", "çalışma", GOOD, 2.4, 0.85, 20, 15).move_to([-1.8, -2.05, 0])
        o6 = sbox("O6", "aralıklı LODS", WARN, 2.6, 0.85, 20, 15).move_to([2.0, -2.05, 0])
        oa = arrow(o5.get_right(), o6.get_left(), WARN, 3, 0.15)
        lods = VGroup(lamp(True, 0.12), T("LODS ilan edildi", 17, WARN, BOLD)).arrange(RIGHT, buff=0.15).next_to(frs[4], UP, buff=0.12)
        self.play(self.set_src("G.989.3 §10.1.1.3 · Tablo 14-3 · ONU durumları O5 / O6 (§12)"), FadeIn(inj), run_time=0.5)
        self.at(self.cue("iki bit hata ekleyin", 2.5))
        self.play(FadeIn(frs[0][:2]), FadeIn(frs[0][2]), FadeIn(frs[1][:2], shift=RIGHT * 0.08), run_time=0.6)
        self.at(self.cue("durum değişmemelidir", 7.6))
        self.play(FadeIn(frs[1][2], shift=DOWN * 0.08), FadeIn(ok2), run_time=0.5)
        self.at(self.cue("Üç bit ekleyin", 9.3))
        self.play(FadeIn(frs[2][:2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("yeniden senkrona geçmelidir", 10.6))
        self.play(FadeIn(frs[2][2], shift=DOWN * 0.08), run_time=0.4)
        self.at(self.cue("Sonraki iki çerçeveyi", 13.5))
        self.play(FadeIn(frs[3], shift=RIGHT * 0.08), run_time=0.4)
        self.play(FadeIn(frs[4][:2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("senkron kaybı ilan etmeli", 16.1))
        self.play(FadeIn(frs[4][2], shift=DOWN * 0.08), FadeIn(lods), run_time=0.5)
        self.play(FadeIn(o5), GrowArrow(oa), FadeIn(o6), run_time=0.7)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_labB")


class E12LabC(Act12):
    HDR, MANIFEST, PREV_BADGE = H12["L"], M12("lab"), "lab"

    def construct(self):
        # g9 — BER counters with FEC on/off
        self.beat("g9")
        h = step_head(self, 6, "Hata oranı sayaçları")
        em = emu_icon(1.9, 1.3).move_to([-5.6, 1.35, 0])
        voa = instr("VOA", 2.15, 1.3, "dB", None, GOLD).move_to([-3.05, 1.35, 0])
        onu = onu_box("ONU", ONUC, 1.3, 0.6, 18).move_to([-0.9, 1.45, 0])
        ln = VGroup(Line(em[0].get_right(), voa[0].get_left(), color=FEED, stroke_width=3), Line(voa[0].get_right(), onu.get_left(), color=FEED, stroke_width=3))
        ref = T("referans BER: 10⁻³ (10G) · 10⁻⁴ (2,5G)", 15, GOLD, BOLD).next_to(VGroup(voa, onu), DOWN, buff=0.12).align_to(voa, LEFT)
        p = apanel(5.5, 2.5, "ONU PM sayaçları (Tablo 14-1)", ACC).move_to([3.75, 1.05, 0])
        rows = VGroup(kv("Toplam FEC kod sözcüğü", "5 016 000 / s", kw=3.0, vcolor=GOLD), kv("Düzeltilen FEC baytı", "…", kw=3.0),
                      kv("BIP-32 hata sayısı", "…", kw=3.0)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fit(rows, 5.1).move_to(p[0]).shift(DOWN * 0.2)
        c1 = card("FEC açık", "ham BER ≈ düzeltilen bitler / alınan bitler", None, ACC, w=6.2, h=1.05, tsize=19, bsize=17).move_to([-3.25, -1.05, 0])
        c2 = card("FEC kapalı", "BER ≈ BIP-32 hataları / (32 × korunan sözcük)", None, BIPC, w=6.2, h=1.05, tsize=19, bsize=17).move_to([3.25, -1.05, 0])
        wn = pill("canlı kanalda ↓ FEC'i asla açıp kapamayın", WARN, 19).move_to([0, -2.45, 0])
        self.play(self.set_src("G.989.3 Tablo 14-1 · §10.1.3.1.2 · G.989.2 Tablo 11-4/11-5 · yöntem: yorum"), run_time=0.3)
        self.at(self.cue("ayarlı bir zayıflatıcı", 3.5))
        self.play(FadeIn(em), FadeIn(voa), FadeIn(onu), Create(ln), run_time=0.7)
        self.at(self.cue("referans hata oranına kadar", 7.0))
        self.play(FadeIn(ref, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("FEC açıkken ham hata", 10.2))
        self.play(FadeIn(c1, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("kapalıyken BIP-32", 14.3))
        self.play(FadeIn(c2, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("beş milyon on altı bin", 17.9))
        self.play(FadeIn(p), FadeIn(rows), run_time=0.6)
        self.play(Indicate(rows[0][1], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("canlı bir kanalda", 23.7))
        self.play(FadeIn(wn, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # g10 — malformed BWmaps, observe the ONU optical output
        self.beat("g10")
        self.clear(h)
        h = step_head(self, 7, "Hatalı haritalar", h)
        e = apanel(6.2, 3.9, "OLT emülatörü · kural dışı BWmap", GOLD).move_to([-3.4, 0.3, 0])
        cases = [("StartTime > 9719", "burst yok", WARN), ("seride > 16 yapı", "kısa kesilir", GOLD),
                 ("bozuk HEC (düzeltilemez)", "kalanı bastırılır", GOLD), ("bilinmeyen Alloc-ID", "kalanı bastırılır", GOLD)]
        cl = VGroup()
        for s_, r_, c in cases:
            cl.add(VGroup(T("• " + s_, 18, TXT, BOLD), T("→ " + r_, 17, c, BOLD)))
        for r in cl:
            r[1].next_to(r[0], RIGHT, buff=0.2)
        cl.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        for r in cl:
            r[1].set_x(cl.get_left()[0] + 3.6 + r[1].width / 2)
        fit(cl, 5.8).move_to(e[0]).shift(DOWN * 0.2)
        sc = scope(5.2, 2.6, [3.6, 0.55, 0])
        scl = T("hızlı fotodiyot + osiloskop", 16, MUTED, BOLD).next_to(sc, UP, buff=0.1)
        x0, x1, yb = sc[0].get_left()[0], sc[0].get_right()[0], sc[0].get_bottom()[1] + 0.35
        trig = VGroup(DashedLine([x0 + 0.5, yb - 0.2, 0], [x0 + 0.5, yb + 2.0, 0], color=ACC, stroke_width=2), T("çerçeve tetiği", 14, ACC, BOLD).move_to([x0 + 1.25, yb + 2.05, 0]))
        bx0, bx1 = x0 + 1.4, x1 - 0.5
        exp = DashedVMobject(Polygon([bx0, yb, 0], [bx0 + 0.1, yb + 1.3, 0], [bx1 - 0.1, yb + 1.3, 0], [bx1, yb, 0], stroke_color=MUTED, stroke_width=2), num_dashes=40)
        cut = Polygon([bx0, yb, 0], [bx0 + 0.1, yb + 1.3, 0], [bx0 + 1.3, yb + 1.3, 0], [bx0 + 1.4, yb, 0], stroke_color=TW_US, stroke_width=2.5, fill_color=TW_US, fill_opacity=0.35)
        flat = Line([x0 + 0.1, yb, 0], [x1 - 0.1, yb, 0], color=TW_US, stroke_width=2.5)
        res = VGroup(T("burst ya hiç gelmemeli", 17, WARN, BOLD), T("ya da kısa kesilmeli", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.4).next_to(sc, DOWN, buff=0.2)
        self.play(self.set_src("G.989.3 §8.1.1.3 · gözlem yöntemi: yorum"), run_time=0.3)
        self.at(self.cue("kuralları ihlal eden", 2.5))
        self.play(FadeIn(e), run_time=0.5)
        for k, (key, d) in enumerate((("sınır dışı başlangıç", 6.8), ("seride on altıdan fazla", 9.2), ("bozuk bir HEC", 11.7), ("bilinmeyen bir tahsis", 12.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(cl[k][0], shift=RIGHT * 0.08), run_time=0.35)
        self.at(self.cue("hızlı bir fotodiyot", 15.4))
        self.play(FadeIn(sc), FadeIn(scl), Create(flat), Create(exp), run_time=0.7)
        self.at(self.cue("çerçeve tetiğine kilitli", 20.3))
        self.play(Create(trig[0]), FadeIn(trig[1]), run_time=0.5)
        self.at(self.cue("burst ya hiç gelmemeli", 23.6))
        self.play(FadeIn(res[0]), FadeIn(cl[0][1]), Indicate(flat, color=WARN), run_time=0.6)
        self.at(self.cue("ya da kısa kesilmelidir", 25.6))
        self.play(FadeIn(res[1]), FadeIn(cut), *[FadeIn(cl[k][1]) for k in (1, 2, 3)], run_time=0.6)
        self.end(pad=0.05)

        # g11 — burst anatomy at the OLT
        self.beat("g11")
        self.clear(h)
        h = step_head(self, 8, "Burst anatomisi — OLT tarafında", h)
        yb, yt = -0.15, 1.35
        px0 = -6.0
        prev = VMobject(stroke_color=TW_US, stroke_width=2.5).set_points_as_corners([[px0, yt, 0], [-4.6, yt, 0], [-4.35, yb, 0], [-3.5, yb, 0]])
        on_ = VMobject(stroke_color=TW_US, stroke_width=2.5).set_points_as_corners([[-3.5, yb, 0], [-2.9, yt, 0]])
        pre = VMobject(stroke_color=PHC, stroke_width=1.8).set_points_as_corners([[-2.9 + i * 0.09, yt if i % 2 == 0 else yt - 0.5, 0] for i in range(26)])
        dlm = Rectangle(width=0.8, height=0.5, stroke_color=PHC, stroke_width=2, fill_color=PHC, fill_opacity=0.55).move_to([-0.2, yt - 0.25, 0])
        pay = VMobject(stroke_color=TW_US, stroke_width=2.5).set_points_as_corners([[0.2, yt, 0], [4.9, yt, 0], [5.35, yb, 0], [6.2, yb, 0]])
        base = DashedLine([px0, yb - 0.02, 0], [6.3, yb - 0.02, 0], color=MUTED, stroke_width=1.5)

        def mbr(xa, xb, y, s, c):
            b = BraceBetweenPoints([xa, y, 0], [xb, y, 0], UP, color=c)
            return VGroup(b, T(s, 15, c, BOLD).next_to(b, UP, buff=0.04))
        mg = mbr(-4.6, -2.9, yt + 0.12, "koruma", MUTED)
        mp = mbr(-2.9, -0.6, yt + 0.12, "önsöz", PHC)
        md = mbr(-0.6, 0.2, yt + 0.12, "sın.", PHC)
        ton = VGroup(Line([-3.5, yb - 0.25, 0], [-2.9, yb - 0.25, 0], color=WARN, stroke_width=3), T("Ton", 15, WARN, BOLD).move_to([-3.2, yb - 0.5, 0]))
        tof = VGroup(Line([4.9, yb - 0.25, 0], [5.35, yb - 0.25, 0], color=WARN, stroke_width=3), T("Toff", 15, WARN, BOLD).move_to([5.12, yb - 0.5, 0]))
        rl = VGroup(VGroup(tag("önsöz", PHC, 16), T("uzunluk + desen ↔ profil (oktet 16 – 25)", 17, TXT)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("sınırlayıcı", PHC, 16), T("↔ oktet 7 – 15 · FEC açık / kapalı çifti (Tablo III.1)", 17, TXT)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("Ton / Toff", WARN, 16), T("≤ 320 / 1280 bit (2,5G / 10G) · G.989.2 Tablo 11-6 / 11-7", 17, TXT)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("koruma", MUTED, 16), T("gerçek boşluk ↔ BWmap'teki aralık", 17, TXT)).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(rl, 12.4).move_to([0, -2.05, 0])
        prof = tag("etkin burst profili", GOLD, 16).move_to([3.0, yt + 0.5, 0])
        self.play(self.set_src("G.989.3 §10.1.2 · Tablo 11-4 · Ek III · G.989.2 Tablo 11-6 / 11-7 · yöntem: yorum"), FadeIn(base), Create(prev), run_time=0.6)
        self.at(self.cue("burst analizörüyle önsözün", 2.6))
        self.play(Create(on_), Create(pre), FadeIn(mp), FadeIn(rl[0], shift=RIGHT * 0.08), run_time=0.8)
        self.at(self.cue("sınırlayıcıyı ve FEC açık", 8.3))
        self.play(FadeIn(dlm), FadeIn(md), Create(pay), FadeIn(rl[1], shift=RIGHT * 0.08), run_time=0.8)
        self.at(self.cue("etkin profille karşılaştırın", 13.0))
        self.play(FadeIn(prof, shift=DOWN * 0.08), run_time=0.4)
        self.at(self.cue("Verici açma ve kapama geçişlerini", 15.4))
        self.play(FadeIn(ton), FadeIn(tof), FadeIn(rl[2], shift=RIGHT * 0.08), run_time=0.6)
        self.at(self.cue("gerçek koruma süresini", 20.3))
        self.play(FadeIn(mg), FadeIn(rl[3], shift=RIGHT * 0.08), run_time=0.6)
        self.end(pad=0.05)

        # g12 — lab note
        self.note11("g12", [("1", "Altın vektörler bir kalibrasyon kaynağıdır",
                             "Her yeni firmware sürümünde yeniden çalıştırın.", "altın vektörler bir kalibrasyon"),
                            ("2", "Ek IV'ün kalan vektörleri: IV.6 – IV.12",
                             "Şifreleme ve PLOAM bütünlüğü için — S2·B5 ve S2·B8'de kullanacağız.", "kalan vektörleri şifreleme")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep12_labC")


POINTS = [("Her ↓ çerçeve 24 baytlık PSBd ile başlar:\n64 bit PSync · 51 bit SFC · OC (kimlik + güç)", "§10.1.1"),
          ("ONU 4 durumlu makineyle kilitlenir; önerilen M = 3;\nLODS yalnızca Av ve Ön senkronda", "§10.1.1.3"),
          ("FEC: ↓ statik, ↑ burst profiline bağlı; 10G'de bedeli ≈ %13", "§10.1.3"),
          ("BWmap: 12,86 ns'lik ortak zaman kuantumu → iki hız aynı ızgarada", "§8.1.1.2"),
          ("Koruma süresi: G.989.3'ün 64 bitine değil,\nG.989.2'nin verici geçiş sürelerine bakın", "§10.1.2.3")]


class E12End(Act12):
    HDR, MANIFEST, FIRST = H12["E"], M12("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir", 1.2))
        self.to_header(tc)
        self.set_badge("ozet")
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.6)
            ch = tag(c, GOLD, 17)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.75, -2.35, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.7, y, 0])
        for k, (key, d) in enumerate((("her aşağı yön çerçevesi", 1.5), ("ONU dört durumlu", 15.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((2, 3, 4), (("FEC aşağı yönde statik", 0.2), ("bant genişliği haritası", 8.5), ("koruma süresi için", 19.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("2,5G ↓ çerçeve kaç\nkod sözcüğüne bölünür?\nSonuncusuna ne olur?", CH[0]),
            ("Senkrondaki ONU, PSync'te\n3 bit hatalı çerçeve alırsa\nhangi duruma geçer?\nLODS ne zaman ilan edilir?", CH[1]),
            ("Kimliği olmayan 10G ONU,\nFEC açıkken SN tahsisine\nkaç baytlık burst ile\ncevap verir?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 9.5), ("Üçüncü soru", 21.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 33.1))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: XGEM
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e3 = SERIES["season2"]["episodes"][2]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e3['n']} · {e3['title']}", 50, TXT, BOLD), T(e3["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.1)
        fit(nxt[1], 12.6)
        y = -1.6
        hd = seg(-5.6, 1.6, y, FSC, "FS başlığı", h=0.6, op=0.3, size=16)
        xg = xgem_run(-4.0, y, [(2.2, "SDU"), (1.4, "parça 1"), (1.8, "parça 2")], h=0.6, hw=0.4, size=15)
        bp = seg(xg.get_right()[0], 0.9, y, BIPC, "BIP", h=0.6, op=0.3, size=16)
        pl = T("FS yükü: XGEM çerçeveleri", 15, SAC, BOLD).next_to(xg, DOWN, buff=0.1)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("Kullanıcı verisinin", 1.9))
        self.play(FadeIn(nxt[2]), FadeIn(hd, shift=RIGHT * 0.1), run_time=0.5)
        self.play(FadeIn(xg[0], shift=RIGHT * 0.1), FadeIn(pl), run_time=0.6)
        self.at(self.cue("parçalandığı", 6.5))
        self.play(FadeIn(xg[1:], shift=RIGHT * 0.1), FadeIn(bp, shift=RIGHT * 0.1), run_time=0.6)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(hd, xg, bp, pl)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP12['n']} · {EP12['title']}", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Coqui XTTS-v2 — ses: Ana Florence (yerel GPU)", 22, ACC, BOLD),
                    T("(Coqui Public Model License — ticari olmayan kullanım)", 18, ACC),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.3 (2021)/Amd.1 (2023)/Amd.2 (2025) · ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020)", 18, MUTED)).arrange(DOWN, buff=0.3)
        fit(cr, 13.2)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep12_end")
