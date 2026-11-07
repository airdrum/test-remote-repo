"""S2·B1 · Laboratuvarda (test tezgâhı 2.0: protokol analizörü + OLT emülatörü) and Kapanış."""
from ep11_common import *

OC64 = [("PIT", 8, MUTED), ("PON-ID", 32, ACC), ("R", 1, MUTED), ("C", 1, MUTED), ("TOL", 9, MUTED), ("HEC", 13, MUTED)]


def step_head(self_, n, s, old=None):
    t = VGroup(pill(f"ADIM {n}", GOOD, 18), T(s, 32, TXT, BOLD)).arrange(RIGHT, buff=0.3)
    t.next_to(self_.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
    fit(t, 12.0)
    self_.play(FadeTransform(old, t) if old is not None else FadeIn(t, shift=RIGHT * 0.2), run_time=0.5)
    return t


def ok_line(s, ok=True, size=18):
    return VGroup(T("✓" if ok else "✗", size + 2, GOOD if ok else WARN, BOLD), T(s, size, TXT)).arrange(RIGHT, buff=0.2)


class E11LabA(Act11):
    HDR, MANIFEST, FIRST = H11["L"], M11("lab"), True

    def construct(self):
        # g1 — bench 2.0
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Test tezgâhı 2.0")
        self.at(self.cue("Birinci sezonun tezgâhında", 1.2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Sezon 1 tezgâhı + iki yeni cihaz")
        s1 = VGroup(instr("PM", 1.9, 1.35, "P · dBm", None, ACC), instrument("OSA", 1.9, 1.35), instr("BERT", 1.9, 1.35, "BER", None, GOOD),
                    instr("VOA", 1.9, 1.35, "dB", None, GOLD)).arrange(RIGHT, buff=0.35).move_to([-0.95, 1.2, 0])
        s1l = T("Sezon 1", 18, MUTED, BOLD).next_to(s1, LEFT, buff=0.3)
        dut = onu_box("ONU (DUT)", ONUC, 1.7, 0.7, 17).move_to([5.3, 1.35, 0])
        pa = pa_icon(2.7, 1.8).move_to([-2.7, -1.35, 0])
        em = emu_icon(2.7, 1.8).move_to([1.6, -1.35, 0])
        pat = T("↓ ve ↑ yönü izler", 16, ACC, BOLD).next_to(pa, RIGHT, buff=0.2).shift(UP * 0.35)
        emt = T("mesajları istediğimiz\ngibi üretir", 16, GOLD, BOLD, line_spacing=0.85).next_to(em, RIGHT, buff=0.2).shift(UP * 0.3)
        fit(emt, 2.0)
        s2l = T("yeni", 18, GOLD, BOLD).next_to(VGroup(pa, em), LEFT, buff=0.3)
        goal = pill("bu bölüm: kimlikleri okumak", ACC, 18).move_to([4.6, -2.75, 0])
        self.play(FadeIn(s1l), FadeIn(dut), self.set_src("tezgâh seçimi: yorum · ölçümler G.989.3 §6"), run_time=0.4)
        for k, (key, d) in enumerate((("bir güç ölçer", 2.0), ("bir OSA", 4.6), ("hata oranı test cihazı", 5.3), ("ayarlı zayıflatıcı", 7.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(s1[k], shift=UP * 0.1), run_time=0.35)
        self.at(self.cue("iki cihaz ekliyoruz", 10.2))
        self.play(s1.animate.set_opacity(0.45), FadeIn(s2l), run_time=0.5)
        self.at(self.cue("bir protokol analizörü", 12.8))
        self.play(FadeIn(pa, shift=UP * 0.15), FadeIn(pat), run_time=0.6)
        self.at(self.cue("bir OLT emülatörü", 17.1))
        self.play(FadeIn(em, shift=UP * 0.15), FadeIn(emt), run_time=0.6)
        self.at(self.cue("kimlikleri okuyacağız", 21.7))
        self.play(FadeIn(goal, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g2 — find PSync, unmask OC, check HEC, split fields
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "PSBd'yi bul, OC'yi çöz")
        p = apanel(6.6, 2.6, "Analizör · ↓ bit akışı", ACC)
        p.move_to([-3.0, 0.75, 0])
        def hrow(off):
            a = HX(off, 16, MUTED)
            b = HX("C5 E5 18 40 FD 59 BB 49", 16, GOLD, BOLD)
            c = HX("·· ··", 16, MUTED)
            b.move_to(a.get_left() + RIGHT * 1.75, aligned_edge=LEFT)
            c.next_to(b, RIGHT, buff=0.2)
            return VGroup(a, b, c)
        rows = VGroup(hrow("bayt 0"), HX("…", 16, MUTED), hrow("bayt 155520"))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for r in (rows[0], rows[2]):
            r[1].set_x(rows[0][1].get_x())
            r[2].next_to(r[1], RIGHT, buff=0.2)
        fit(rows, 6.2).move_to(p[0]).shift(DOWN * 0.2)
        per = VGroup(tag("10G: her 155 520 B", R10, 17), tag("2,5G: her 38 880 B", R25, 17)).arrange(RIGHT, buff=0.25).next_to(p, DOWN, buff=0.18)
        steps = VGroup(T("① PSync deseni: C5E51840 FD59BB49", 17, TXT, BOLD), T("② OC ⊕ 0x0F0F0F0F 0F0F0F0F", 17, TXT, BOLD),
                       T("③ HEC kontrolü (13 bit)", 17, TXT, BOLD), T("④ alanlara ayır", 17, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(steps, 5.6).move_to([3.55, 0.75, 0])
        ocf = fields(OC64, 12.4, 0.55, 17, 14).move_to([0, -2.35, 0])
        ocl = T("OC yapısı · 64 bit", 15, MUTED, BOLD).next_to(ocf, UP, buff=0.12).align_to(ocf, LEFT)
        self.play(self.set_src("G.989.3 §10.1.1.2 – .3 · §10.1.1.1.3 · Ek A (HEC)"), run_time=0.3)
        self.at(self.cue("senkron bloğunu bulmak", 0.8))
        self.play(FadeIn(p), FadeIn(rows[0]), FadeIn(steps[0], shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("on gigabitte her yüz elli beş bin", 5.4))
        self.play(FadeIn(rows[1:]), FadeIn(per[0], shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("iki buçuk gigabitte her otuz sekiz bin", 10.0))
        self.play(FadeIn(per[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("sabit desenle geri açın", 18.1))
        self.play(FadeIn(steps[1], shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("hata denetimini kontrol edin", 22.8))
        self.play(FadeIn(steps[2], shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("alanlarına ayırın", 25.2))
        self.play(FadeIn(steps[3], shift=LEFT * 0.1), FadeIn(ocl), LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in ocf], lag_ratio=0.1), run_time=0.8)
        self.end(pad=0.05)

        # g3 — PON-ID vs optics
        self.beat("g3")
        self.clear(h)
        h = step_head(self, 2, "PON-ID ↔ optik", h)
        pf = fields([("yönetim etiketi", 28, ACC), ("DWLCH ID", 4, GOLD)], 6.0, 0.6, 17, 14).move_to([-3.3, 1.35, 0])
        val = HX("PON-ID = 0x1234 5673", 24, TXT, BOLD).next_to(pf, UP, buff=0.25).align_to(pf, LEFT)
        v1 = HX("0x1234567", 18, ACC, BOLD).move_to(pf[0][0])
        v2 = HX("0011", 18, GOLD, BOLD).move_to(pf[1][0])
        res = VGroup(T("en anlamsız 4 bit → DWLCH ID = 0011 → kanal 4", 18, GOLD, BOLD)).next_to(pf, DOWN, buff=0.45).align_to(pf, LEFT)
        fit(res, 6.2)
        axg, X = lin_axis(187.05, 187.85, 0.6, 6.3, -0.35, [187.1, 187.3, 187.5, 187.7], size=14, unit="THz")
        pk = lobe(X, 187.5, -0.35, 1.5, 0.018, CH[3], op=0.4)
        pkl = T("OSA / dalga boyu ölçer", 16, MUTED, BOLD).move_to([3.45, 1.85, 0])
        pkv = T("ölçülen: 187,5 THz", 18, CH[3], BOLD).next_to([X(187.5), 1.25, 0], RIGHT, buff=0.15)
        tb = table(["Kanal", "THz", "nm", "DWLCH ID"], [["4", "187,5", "1598,89", "0011"]], [1.4, 1.6, 1.8, 2.0], size=19, hsize=16, row_h=0.5)
        tb.move_to([-1.6, -2.3, 0])
        tbl = T("Tablo 6-3", 15, MUTED, BOLD).next_to(tb, LEFT, buff=0.2)
        okm = T("✓ eşleşiyor", 22, GOOD, BOLD).next_to(tb, RIGHT, buff=0.4)
        self.play(self.set_src("G.989.3 §6.1.5.3 – .4 · Tablo 6-3 · Ek VIII (örnek çözüm)"), run_time=0.3)
        self.at(self.cue("en anlamsız dört biti", 4.2))
        self.play(*[FadeIn(c) for c in pf], run_time=0.5)
        self.at(self.cue("aşağı yön kanal kimliğidir", 7.3))
        self.play(Indicate(pf[1], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("dalga boyu ölçerle", 9.6))
        self.play(FadeIn(axg), FadeIn(pkl), run_time=0.5)
        self.play(FadeIn(pk), run_time=0.5)
        self.at(self.cue("frekans tablosuyla", 14.2))
        self.play(FadeIn(tbl), FadeIn(tb[0]), run_time=0.4)
        self.at(self.cue("on altılık tabanda", 17.2))
        self.play(FadeIn(val, shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeTransform(pf[0][1], v1), run_time=0.4)
        self.at(self.cue("sıfır sıfır bir bir", 23.6))
        self.play(FadeTransform(pf[1][1], v2), FadeIn(res), run_time=0.5)
        self.at(self.cue("dördüncü kanaldır", 26.4))
        self.play(FadeIn(tb[1], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("yüz seksen yedi virgül beş", 28.4))
        self.play(FadeIn(pkv), FadeIn(okm, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g4 — system identity and profile-set consistency
        self.beat("g4")
        self.clear(h)
        h = step_head(self, 3, "Sistem kimliği ve profil kümesi", h)
        p = apanel(6.4, 2.3, "Yakalama · System_Profile", GOLD)
        p.move_to([-3.1, 1.0, 0])
        l1 = kv("tür / ONU-ID", "0x17 / 0x03FF", 15, 17, kw=2.0)
        l2 = kv("oktet 5–7", "0000 SSSS SSSS SSSS SSSS SSSS", 15, 15, kw=2.0)
        pl = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit(pl, 6.0).move_to(p[0]).shift(UP * 0.02)
        s20 = brace_lbl(l2[1], "NG2SYS ID · 20 bit (üst 4 bit = 0)", ACC, DOWN, 15)
        cts = VGroup(*[VGroup(ct_box(f"CT {i + 1}", CH[i], 1.1, 0.45, 15), HX("S", 17, ACC, BOLD), T("✓", 18, GOOD, BOLD)).arrange(RIGHT, buff=0.15) for i in range(4)])
        cts.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, 1.0, 0])
        ctl = T("her CT'de aynı", 16, GOOD, BOLD).next_to(cts, UP, buff=0.1)
        x0, x1, yw = -5.6, 5.6, -1.75
        win = Rectangle(width=x1 - x0, height=1.15, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.05).move_to([0, yw, 0])
        wl = T("profil penceresi (TminProfile: 1 … 5 s)", 15, GOLD, BOLD).next_to(win, UP, buff=0.06).align_to(win, LEFT)
        sp = tile("System_Profile", GOLD, 1.9, 0.45, 14, 0.3).move_to([x0 + 1.2, yw + 0.17, 0])
        cps = VGroup(*[tile(f"Channel_Profile {i + 1}", CH[i], 2.0, 0.45, 14, 0.25) for i in range(4)]).arrange(RIGHT, buff=0.12).next_to(sp, RIGHT, buff=0.2)
        pids = VGroup(*[HX("PON-ID", 14, CH[i], BOLD).next_to(cps[i], DOWN, buff=0.08) for i in range(4)])
        cnt = T("sayı = System_Profile'daki kanal sayısı (oktet 10) ✓", 17, GOOD, BOLD).move_to([0.6, -2.85, 0])
        ex = tag("örnek: 4 kanal", MUTED, 14).next_to(wl, RIGHT, buff=0.25)
        self.play(self.set_src("G.989.3 §6.1.5.2 · Tablo 11-17 / 11-18 · §17.1"), run_time=0.3)
        self.at(self.cue("Sistem profili mesajını yakalayın", 2.3))
        self.play(FadeIn(p), FadeIn(l1), run_time=0.5)
        self.at(self.cue("yirmi bitlik sistem kimliğini", 5.1))
        self.play(FadeIn(l2), FadeIn(s20), run_time=0.5)
        self.at(self.cue("bütün kanal sonlandırıcılarında aynı", 8.2))
        self.play(FadeIn(ctl), LaggedStart(*[FadeIn(c, shift=LEFT * 0.1) for c in cts], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("Bir profil penceresi boyunca", 13.3))
        self.play(FadeIn(win), FadeIn(wl), FadeIn(sp), FadeIn(ex), run_time=0.5)
        self.at(self.cue("kanal profili mesajlarının sayısını", 15.8))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in cps], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("kanal sayısına eşit olmalı", 19.6))
        self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("her biri bir PON kimliği", 24.2))
        self.play(LaggedStart(*[FadeIn(pi_) for pi_ in pids], lag_ratio=0.15), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep11_labA")


class E11LabB(Act11):
    HDR, MANIFEST, PREV_BADGE = H11["L"], M11("lab"), "lab"

    def construct(self):
        # g5 — ONU-ID rules in PLOAM
        self.beat("g5")
        h = step_head(self, 4, "ONU-ID kuralları (PLOAM)")
        tb = table(["ONU-ID", "↓ PLOAMd", "↑ PLOAMu"], [["0x3FF · 1023", "yayın ✓", "atanmamış ONU ✓"], ["0x3FD · 0x3FE", "✗ görünmemeli", "✗ görünmemeli"]],
                   [3.2, 3.2, 3.6], size=19, hsize=16, row_h=0.56).move_to([0, 1.2, 0])
        for c in (2, 3):
            tb[1][c].set_color(GOOD)
            tb[2][c].set_color(WARN)
        hd = fields([("ONU-ID", 10, ACC), ("Ind", 9, MUTED), ("HEC", 13, MUTED)], 8.0, 0.55, 17, 14).move_to([-1.0, -1.25, 0])
        hdl = T("↑ FS burst başlığı (SN cevabı)", 16, MUTED, BOLD).next_to(hd, UP, buff=0.12).align_to(hd, LEFT)
        hv = HX("0x3FF", 18, GOLD, BOLD).move_to(hd[0][0])
        hok = T("✓ atanmamış değer", 18, GOOD, BOLD).next_to(hd, RIGHT, buff=0.35)
        six = T("PLOAM oktet 1–2: 6 üst bit = 0", 15, MUTED).move_to([0, -2.55, 0])
        self.play(FadeIn(tb[0]), self.set_src("G.989.3 Tablo 6-4 · §11.2.1 · §8.1.2.1.1"), run_time=0.5)
        self.at(self.cue("yalnızca aşağı yönde yayın", 3.0))
        self.play(FadeIn(tb[1][0]), FadeIn(tb[1][1]), FadeIn(tb[1][2]), run_time=0.5)
        self.at(self.cue("yukarı yönde atanmamış", 7.9))
        self.play(FadeIn(tb[1][3]), run_time=0.4)
        self.at(self.cue("hiç görünmemelidir", 12.1))
        self.play(FadeIn(tb[2], shift=UP * 0.05), FadeIn(six), run_time=0.5)
        self.at(self.cue("Seri numarası cevaplarında", 16.3))
        self.play(FadeIn(hd), FadeIn(hdl), run_time=0.5)
        self.at(self.cue("bin yirmi üç olmalıdır", 20.0))
        self.play(FadeTransform(hd[0][1], hv), FadeIn(hok, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # g6 — the default triple
        self.beat("g6")
        self.clear(h)
        h = step_head(self, 5, "Varsayılan üçlü", h)
        xe, xo, y0, y1 = -5.0, -0.6, 1.6, -2.4
        le = lifeline("Emülatör", xe, y0, y1, GOLD, 1.9)
        lo = lifeline("ONU", xo, y0, y1, ONUC, 1.9)
        m1 = msg(xe, xo, 0.75, "Assign_ONU-ID · 19", GOLD, 17)
        m2 = msg(xe, xo, -1.45, "Deactivate_ONU-ID", WARN, 17)
        p = apanel(5.5, 3.4, "Analizör", ACC)
        p.move_to([3.65, -0.1, 0])
        c1 = ok_line("ranging tahsisi: Alloc-ID 19", True, 17)
        c2 = ok_line("OMCI çerçeveleri: Port-ID 19", True, 17)
        c3 = ok_line("19 · 19 · 19 kullanımı durur", True, 17)
        cs = VGroup(c1, c2, c3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(cs, 5.1).move_to(p[0]).shift(DOWN * 0.2)
        self.play(FadeIn(le), FadeIn(lo), FadeIn(p), self.set_src("G.989.3 §6.1.5.6 – .8 · §12.1.5"), run_time=0.5)
        self.at(self.cue("kimlik atayın", 2.4))
        self.play(GrowArrow(m1[0]), run_time=0.4)
        self.at(self.cue("diyelim on dokuz", 5.5))
        self.play(FadeIn(m1[1]), run_time=0.3)
        self.at(self.cue("Mesafe ölçüm tahsisinin", 6.9))
        self.play(FadeIn(c1, shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("OMCI çerçevelerinin portu", 11.0))
        self.play(FadeIn(c2, shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.cue("kimliği iptal edin", 15.0))
        self.play(GrowArrow(m2[0]), FadeIn(m2[1]), run_time=0.5)
        self.at(self.cue("kullanmayı bırakmalıdır", 17.1))
        self.play(FadeIn(c3, shift=RIGHT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # g7 — the rate gate
        self.beat("g7")
        self.clear(h)
        h = step_head(self, 6, "Hız kapısı", h)
        hx = [(-4.4, "Emülatör: SN tahsisi"), (0.4, "10G ↑ ONU"), (3.9, "2,5G ↑ ONU")]
        hdr = VGroup(*[T(s, 17, MUTED, BOLD).move_to([x, 1.75, 0]) for x, s in hx])
        cases = [("yalnız 1022", R10, True, False, "tek hızlı · 10G kanal"), ("yalnız 1023", R25, False, True, "tek hızlı · 2,5G kanal"), ("1021", GOLD, True, True, "çift hızlı kanal")]
        rows = VGroup()
        for i, (g, c, a, b, note) in enumerate(cases):
            y = 0.95 - i * 1.25
            gt = VGroup(tile(g, c, 2.0, 0.55, 18, 0.25), T(note, 14, c, BOLD)).arrange(DOWN, buff=0.06).move_to([-4.4, y, 0])
            ra = VGroup(onu_box("10G", R10, 1.0, 0.5, 15), T("cevap ✓" if a else "sessiz", 16, GOOD if a else MUTED, BOLD)).arrange(RIGHT, buff=0.2).move_to([0.4, y, 0])
            rb = VGroup(onu_box("2,5G", R25, 1.0, 0.5, 15), T("cevap ✓" if b else "sessiz", 16, GOOD if b else MUTED, BOLD)).arrange(RIGHT, buff=0.2).move_to([3.9, y, 0])
            ar = Arrow([-3.2, y, 0], [-0.7, y, 0], buff=0, color=c, stroke_width=2.5, tip_length=0.13)
            rows.add(VGroup(gt, ar, ra, rb))
        amcc = T("not: AMCC SN tahsisi = Alloc-ID 1021, StartTime = GrantSize = 0xFFFF (§12.1.5)", 15, MUTED).move_to([0, -2.75, 0])
        self.play(FadeIn(hdr), self.set_src("G.989.3 Tablo 6-5 · Not 1 · §12.1.5"), run_time=0.4)
        for i, (k1, d1, k2, d2) in enumerate((("yalnızca bin yirmi iki", 2.0, "sessiz kalmalıdır", 9.5), ("Yalnızca bin yirmi üç", 13.0, "on gigabitlik ONU sessiz", 15.4),
                                              ("Çift hızlı bir kanalda", 18.4, "ikisinin de cevap", 21.5))):
            self.at(self.cue(k1, d1))
            self.play(FadeIn(rows[i][0], shift=RIGHT * 0.1), GrowArrow(rows[i][1]), run_time=0.5)
            self.at(self.cue(k2, d2))
            self.play(FadeIn(rows[i][2]), FadeIn(rows[i][3]), run_time=0.5)
        self.play(FadeIn(amcc), run_time=0.4)
        self.end(pad=0.05)

        # g8 — golden vector (Appendix IV.9)
        self.beat("g8")
        self.clear(h)
        h = step_head(self, 7, "Altın vektör (Ek IV.9)", h)
        spec = [("", 2, PLC), ("", 1, PLC), ("", 1, PLC), ("İçerik · Alloc-ID 0x0445 · tip 0x01", 36, PLC), ("MIC", 8, GOLD)]
        pf = fields(spec, 12.4, 0.6, 16, 14).move_to([0, 1.45, 0])
        lead = VGroup()
        for i, (s, lx) in enumerate((("ONU-ID 0x0013", -5.4), ("Assign_Alloc-ID", -3.4), ("SeqNo 0x03", -1.55))):
            t = HX(s, 15, PLC, BOLD) if i != 1 else T(s, 15, PLC, BOLD)
            t.move_to([lx, 2.2, 0])
            lead.add(VGroup(t, Line(t.get_bottom() + DOWN * 0.04, pf[i][0].get_top(), color=PLC, stroke_width=1.5)))
        p = apanel(7.6, 2.75, "Analizör · PLOAM çözücü", ACC)
        p.move_to([-2.4, -1.1, 0])
        dl = VGroup(kv("ONU-ID", "0x0013 (19)", 15, 16, kw=1.7), kv("Alloc-ID", "0x0445 (1093)", 15, 16, kw=1.7),
                    kv("MIC (verilen)", "46 39 87 56 28 08 14 e6", 15, 16, kw=1.7), kv("PLOAM_IK", "e256ce76785c78717c7b3044ab28e2cd", 15, 14, kw=1.7))
        dl.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(dl, 7.2).move_to(p[0]).shift(DOWN * 0.2)
        alg = T("AES-CMAC-64(PLOAM_IK, 0x01 | mesaj)", 15, MUTED).next_to(p, DOWN, buff=0.1).align_to(p, LEFT)
        okc = card("MIC kontrolü", "hesaplanan = verilen ✓\nçözücü ve bütünlük doğrulandı", None, GOOD, w=4.4, h=1.45, tsize=20, bsize=16).move_to([4.2, -0.6, 0])
        nx = VGroup(T("ayrıntı:", 15, MUTED), s2chip(5)).arrange(RIGHT, buff=0.15).move_to([4.2, -2.2, 0])
        self.play(self.set_src("G.989.3 Ek IV.9 (bilgilendirici) · §11.3.3.7 · §15.6"), run_time=0.3)
        self.at(self.cue("tahsis kimliği atama mesajı", 2.2))
        self.play(*[FadeIn(c[0]) for c in pf], *[FadeIn(c[2]) for c in pf], FadeIn(lead[1]), FadeIn(lead[2]), FadeIn(pf[3][1]), run_time=0.6)
        self.at(self.cue("ONU kimliği on dokuz", 6.6))
        self.play(FadeIn(lead[0]), FadeIn(p), FadeIn(dl[0]), run_time=0.5)
        self.at(self.cue("tahsis kimliği bin doksan üç", 8.4))
        self.play(FadeIn(dl[1]), Indicate(pf[3][1], color=PLC, scale_factor=1.05), run_time=0.5)
        self.at(self.cue("bütünlük kodu da verilmiştir", 10.8))
        self.play(FadeIn(pf[4][1]), pf[4][0].animate.set_fill(opacity=0.5), FadeIn(dl[2]), FadeIn(dl[3]), FadeIn(alg), run_time=0.6)
        self.at(self.cue("bütünlük kontrolünü bu vektörle", 16.0))
        self.play(FadeIn(okc, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("beşinci bölümde", 21.2))
        self.play(FadeIn(nx, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep11_labB")


class E11LabC(Act11):
    HDR, MANIFEST, PREV_BADGE = H11["L"], M11("lab"), "lab"

    def construct(self):
        # g9 — idle XGEM
        self.beat("g9")
        h = step_head(self, 8, "Boş XGEM")
        x0, y = -5.6, 1.25
        frs = VGroup()
        x = x0
        for i in range(8):
            frs.add(VGroup(seg(x, 0.32, y, MUTED, "H", h=0.55, op=0.5, size=13), seg(x + 0.32, 1.0, y, MUTED, "boş", h=0.55, op=0.12, size=14)))
            x += 1.4
        fl = T("↓ FS yükü · trafik yok", 16, MUTED, BOLD).next_to(frs, UP, buff=0.12).align_to(frs, LEFT)
        zh = fields([("PLI", 14, MUTED), ("Anahtar", 2, MUTED), ("Port-ID", 16, GOLD), ("Seçenekler", 18, MUTED), ("LF", 1, MUTED), ("HEC", 13, MUTED)], 10.0, 0.55, 16, 14).move_to([-0.8, -0.65, 0])
        zv = HX("0xFFFF · 65535", 16, GOLD, BOLD).move_to(zh[2][0])
        zl = VGroup(DashedLine(frs[0][0].get_corner(DL), zh.get_corner(UL) + UP * 0.3, color=MUTED, stroke_width=1.2),
                    DashedLine(frs[0][0].get_corner(DR), zh.get_corner(UR) + UP * 0.3, color=MUTED, stroke_width=1.2))
        rx = sbox("alıcı", "boş yükü atar", ONUC, 2.0, 0.85, 18, 15).move_to([5.3, -0.65, 0])
        new = VGroup()
        x = x0
        for i in range(8):
            c = [ACC, GOLD, PINK, ACC, GOLD, ACC, PINK, GOLD][i]
            if i in (2, 6):
                new.add(frs[i].copy())
            else:
                new.add(VGroup(seg(x, 0.32, y, c, "H", h=0.55, op=0.55, size=13), seg(x + 0.32, 1.0, y, c, "veri", h=0.55, op=0.2, size=14)))
            x += 1.4
        rule = T("boş çerçeve: gönderilecek SDU yokken (§9.1.4)", 16, MUTED).move_to([0, -2.3, 0])
        self.play(self.set_src("G.989.3 §9.1.4 · Tablo 6-6"), run_time=0.3)
        self.at(self.cue("Yüksüz bir aşağı yönde", 2.0))
        self.play(FadeIn(fl), LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in frs], lag_ratio=0.1), run_time=0.9)
        self.at(self.cue("altmış beş bin beş yüz otuz beş", 6.0))
        self.play(Create(zl), FadeIn(zh), run_time=0.6)
        self.play(FadeTransform(zh[2][1], zv), run_time=0.4)
        self.at(self.cue("alıcı bunları atar", 11.9))
        self.play(FadeIn(rx, shift=LEFT * 0.1), FadeIn(rule), run_time=0.5)
        self.at(self.cue("Trafiği açınca", 13.8))
        self.play(FadeOut(zl), *[Transform(a, b) for a, b in zip(frs, new)], run_time=1.0)
        self.end(pad=0.05)

        # g10 — channel partition index test
        self.beat("g10")
        self.clear(h)
        h = step_head(self, 9, "Bölümleme indeksi", h)
        onu = RoundedRectangle(corner_radius=0.14, width=3.0, height=1.5, stroke_color=ONUC, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-4.7, 0.85, 0])
        ot = T("ONU", 17, ONUC, BOLD).move_to(onu.get_corner(UL) + [0.4, -0.25, 0])
        cv = HX("CPI = 5", 24, GOLD, BOLD).move_to(onu).shift(DOWN * 0.1)
        set_ = msg(-0.4, onu.get_right()[0], 1.3, "OMCI: CPI = 5", GOLD, 17)
        chs = VGroup(*[tile(f"λ{i + 1}", CH[i], 0.8, 0.5, 16, 0.3) for i in range(4)]).arrange(RIGHT, buff=0.1)
        chf = SurroundingRectangle(chs, color=ACC, buff=0.12, corner_radius=0.08)
        chg = VGroup(chs, chf, T("sunulan: yalnız bölüm ≠ 5", 15, ACC, BOLD).next_to(chf, UP, buff=0.06)).move_to([3.4, 0.85, 0])
        ax0, ax1, ay = -5.6, 4.8, -1.15
        tax = Arrow([ax0, ay, 0], [ax1 + 0.6, ay, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.14)
        t0 = VGroup(Line([ax0 + 0.2, ay - 0.15, 0], [ax0 + 0.2, ay + 0.15, 0], color=MUTED, stroke_width=3), T("eşleşme yok → TCPI başlar", 15, GOLD, BOLD).next_to([ax0 + 0.2, ay, 0], UP, buff=0.22).shift(RIGHT * 1.0))
        t1 = VGroup(Line([ax1, ay - 0.15, 0], [ax1, ay + 0.15, 0], color=WARN, stroke_width=4), T("CPI → 0", 16, WARN, BOLD).next_to([ax1, ay, 0], UP, buff=0.22))
        br = BraceBetweenPoints([ax0 + 0.2, ay - 0.2, 0], [ax1, ay - 0.2, 0], DOWN, color=GOLD)
        brt = T("ölç: önerilen TCPI = 5 dk", 18, GOLD, BOLD).next_to(br, DOWN, buff=0.06)
        pc = VGroup(T("güç kes / aç", 16, MUTED, BOLD), T("→ CPI korunur ✓", 17, GOOD, BOLD)).arrange(RIGHT, buff=0.2).move_to([3.4, -2.75, 0])
        self.play(FadeIn(onu), FadeIn(ot), self.set_src("G.989.3 §6.1.5.9"), run_time=0.4)
        self.at(self.cue("indeksini beşe ayarlayın", 2.8))
        self.play(GrowArrow(set_[0]), FadeIn(set_[1]), FadeIn(cv), run_time=0.6)
        self.at(self.cue("başka bir bölümün kanallarını", 6.7))
        self.play(FadeIn(chg, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("geçen süreyi ölçün", 10.7))
        self.play(GrowArrow(tax), FadeIn(t0), run_time=0.6)
        self.play(FadeIn(t1), FadeIn(br), run_time=0.5)
        self.at(self.cue("önerilen değer beş dakikadır", 15.7))
        self.play(FadeIn(brt), Transform(cv, HX("CPI = 0", 24, WARN, BOLD).move_to(cv)), run_time=0.5)
        self.at(self.cue("gücü kesip açın", 18.2))
        self.play(FadeIn(pc[0]), run_time=0.3)
        self.at(self.cue("indeks korunmalıdır", 20.0))
        self.play(FadeIn(pc[1], shift=RIGHT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        self.note11("g11", [("1", "2021'e göre yazılmış çözücüler geçerli", "§6 o günden beri değişmedi — Amd.1 ve Amd.2 yalnızca şekil numaralarını kaydırdı.", "Bir:"),
                            ("2", "Tek defter: protokol + optik", "PON-ID ile frekans aynı satırda — ör. 0x12345673 ↔ 187,5 THz.", "İki:")], badge="lab")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.hdr and m is not self.badge], run_time=0.5)
        self.save_timeline("ep11_labC")


POINTS = [("G.989.3: G.987.3'ün üstüne kurulu, üç alt katmanlı TC katmanı\nservis uyarlama · çerçeveleme · fiziksel uyarlama", "3 alt katman"),
          ("Dört hız kombinasyonu; dördüncüsü çift hızlı ↑ kanal\nyalnızca TC katmanında tanımlı", "10 / 10 + 2,5"),
          ("Yönetim: gömülü alanlar · PLOAM · OMCC\nkanal sonlandırıcıları arasında: ICTP", "3 kanal + ICTP"),
          ("Dokuz kimlik; ONU-ID = varsayılan Alloc-ID = OMCC Port-ID\nkanal devrinde korunur", "19 = 19 = 19"),
          ("Hız farkına rağmen iki hız, aynı zaman kuantumunu paylaşır", "12,86 ns")]


class E11End(Act11):
    HDR, MANIFEST, FIRST = H11["E"], M11("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header(tc)
        self.set_badge("ozet")
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.6)
            ch = tag(c, GOLD, 17)
            rows.add(VGroup(n, t, ch))
        rows_y = np.linspace(1.75, -2.35, 5)
        for r, y in zip(rows, rows_y):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.6, y, 0])
        for k, (key, d) in enumerate((("G.987.3'ün üstüne kurulmuş", 2.2), ("dört hız kombinasyonundan", 11.9), ("yönetim üç kanaldan geçer", 21.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((3, 4), (("dokuz kimlik vardır", 0.4), ("hız farkına rağmen", 10.7))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Alloc-ID 1022, boyutu 0,\nPLOAM isteyen tahsis: nedir?\nKim cevap verebilir,\nhangi ONU-ID ile?", CH[0]),
            ("PSBd'de PON-ID\n0x12345673 ise\nhangi ↓ kanal?", CH[1]),
            ("ONU-ID 19 olan ONU'nun\nhangi kimlikleri kanal\ndevrinde, hangileri O1'e\ndönüşte korunur?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 13.5), ("Üçüncü soru", 23.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 35.2))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e2 = SERIES["season2"]["episodes"][1]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e2['n']} · {e2['title']}", 50, TXT, BOLD), T(e2["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.1)
        fit(nxt[1], 12.6)
        y = -1.6
        psb = seg(-5.6, 1.0, y, GOLD, "PSBd", h=0.6, op=0.55, size=16, lcolor=BG)
        bw = seg(-4.6, 1.5, y, GOLD, "BWmap", h=0.6, op=0.3, size=16)
        pl = seg(-3.1, 1.2, y, PLC, "PLOAM", h=0.6, op=0.2, size=16)
        py = seg(-1.9, 3.0, y, TW_DS, "XGEM …", h=0.6, op=0.12, size=16)
        dsl = T("↓ çerçeve · 125 µs", 15, TW_DS, BOLD).next_to(VGroup(psb, py), DOWN, buff=0.1)
        ub = VGroup(seg(2.0, 0.8, y, GOLD, "PSBu", h=0.6, op=0.55, size=14, lcolor=BG), seg(2.8, 2.8, y, TW_US, "burst", h=0.6, op=0.2, size=16))
        usl = T("↑ burst", 15, TW_US, BOLD).next_to(ub, DOWN, buff=0.1)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        self.at(self.cue("Senkron bloğundan", 2.2))
        self.play(FadeIn(psb, shift=RIGHT * 0.1), run_time=0.4)
        self.play(FadeIn(bw, shift=RIGHT * 0.1), FadeIn(pl, shift=RIGHT * 0.1), FadeIn(py, shift=RIGHT * 0.1), FadeIn(dsl), run_time=0.6)
        self.at(self.cue("yukarı yön burst'ünü", 7.5))
        self.play(FadeIn(ub, shift=LEFT * 0.1), FadeIn(usl), run_time=0.6)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(psb, bw, pl, py, dsl, ub, usl)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP11['n']} · {EP11['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep11_end")
