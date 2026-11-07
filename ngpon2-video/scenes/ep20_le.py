"""S2·B10 · Laboratuvarda (anahtarlama, ICTP'siz sistem, dışlamalar ve ihlaller, ONU tarafı koruma, başıboş ONU'lar, yabancı ışık ve boş pencere,
acil durdurma, keşif durdurma ve inatçı ONU, bir paketin hayatı) and Kapanış — season and series finale (summary, quiz with answers, series wrap,
'LAMBDA — Dizinin sonu', credits)."""
from ep20_common import *


class LabAct(Act20):
    def next_test(self, n, title, h, rt=0.4):
        keep = {self.hdr, self.badge, h}
        out = [m for m in self.mobjects if m not in keep]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=rt)
        if self.src is not None and self.src in out:
            self.src = None
        return step_head(self, n, title, h)


def exp(s, ok=True, size=16, color=None):
    """Expected outcome line: ✓ / ✗ + text."""
    return VGroup(ok_x(ok, size + 2), T(s, size, color or TXT, BOLD)).arrange(RIGHT, buff=0.12)


def wire(a, b, color=FEED, sw=2.2, dashed=False):
    return (DashedLine(a, b, color=color, stroke_width=sw, dash_length=0.08) if dashed else Line(a, b, color=color, stroke_width=sw))


def stim(s, color=GOLD, w=5.2, size=16):
    """Stimulus tile (what we do) for a test row."""
    r = RoundedRectangle(corner_radius=0.08, width=w, height=0.5, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=0.12)
    t = tf(s, size, TXT, BOLD, w=w - 0.25).move_to(r)
    return VGroup(r, t)


def trow(y, s, outs, color=GOLD, w=5.0, x0=-6.35):
    """Test row: stimulus tile at the left, arrow, expected outcomes stacked at the right."""
    st = stim(s, color, w).move_to([x0 + w / 2, y, 0])
    oc = VGroup(*outs).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    fit(oc, 12.7 - w - 1.0).move_to([x0 + w + 0.85, y, 0], aligned_edge=LEFT)
    a = arrow(st[0].get_right(), [x0 + w + 0.7, y, 0], MUTED, 2.2, 0.12)
    return VGroup(st, a, oc)


def trace(scr, pts, color, sw=2.6):
    """Scope trace from fractional points [(fx, fy)] inside the scope screen."""
    s = scr[0]
    x0, x1, y0, y1 = s.get_left()[0], s.get_right()[0], s.get_bottom()[1], s.get_top()[1]
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners([[x0 + (x1 - x0) * a, y0 + (y1 - y0) * b, 0] for a, b in pts])


class E20LabA(LabAct):
    HDR, MANIFEST, FIRST = H20["L"], M20("lab"), True

    def construct(self):
        # g1 — bench: two OLT CTs (or a dual-CT emulator), two WMs, a two-input splitter and ONUs; optical switches on attachment fibres and feeders;
        #      photodiode + scope on the DS outputs; protocol analyzer, ONU emulator, traffic generator; record every timer that has no value
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Koruma, başıboşluk ve acil durdurma")
        self.at(self.cue("Düzenek", 1.2))
        h = self.heading("Düzenek")
        self.to_header_badge(tc, "lab", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        y1, y2 = 1.45, -0.45
        c1 = ctu("OLT CT 1", CT1C, True, 1.5, 0.5, 16).move_to([-5.85, y1, 0])
        c2 = ctu("OLT CT 2", CT2C, False, 1.5, 0.5, 16).move_to([-5.85, y2, 0])
        emu = tag("ya da çift CT'li\nemülatör", MUTED, 14).move_to([-5.85, (y1 + y2) / 2, 0])
        pd = VGroup(*[VGroup(Circle(radius=0.13, stroke_color=GOLD, stroke_width=2, fill_color=PANEL, fill_opacity=1), T("PD", 14, GOLD, BOLD)) for _ in range(2)])
        for p_, y in zip(pd, (y1, y2)):
            p_[1].move_to(p_[0])
            p_.move_to([-4.7, y, 0])
        sw1 = VGroup(*[oswitch_icon(0.42, FEED, "").move_to([-4.0, y, 0]) for y in (y1, y2)])
        wm = VGroup(*[sbox("WM", None, FEED, 0.6, 0.9, 16).move_to([-3.05, y, 0]) for y in (y1, y2)])
        sw2 = VGroup(*[oswitch_icon(0.42, FEED, "").move_to([-2.05, y, 0]) for y in (y1, y2)])
        swl = T("optik anahtarlar", 14, FEED, BOLD).move_to([-3.05, (y1 + y2) / 2, 0])
        sp = splitter(0.27).move_to([-0.75, (y1 + y2) / 2, 0])
        spl = T("2:N ayırıcı", 14, MUTED, BOLD).move_to([-0.68, 1.05, 0])
        fib = VGroup()
        for y, c, p_, a, w_, b in zip((y1, y2), (c1, c2), pd, sw1, wm, sw2):
            fib.add(wire(c[0].get_right(), p_[0].get_left()), wire(p_[0].get_right(), [a[0].get_x(), y, 0]), wire([a[1].get_x(), y, 0], w_[0].get_left()),
                    wire(w_[0].get_right(), [b[0].get_x(), y, 0]))
        fd = VGroup(VMobject(stroke_color=FEED, stroke_width=2.2).set_points_as_corners([[sw2[0][1].get_x(), y1, 0], [-1.6, y1, 0], sp.get_left() + UP * 0.08]),
                    VMobject(stroke_color=FEED, stroke_width=2.2).set_points_as_corners([[sw2[1][1].get_x(), y2, 0], [-1.6, y2, 0], sp.get_left() + DOWN * 0.08]))
        o1 = onu_box("ONU", ONUC, 1.0, 0.44, 15).move_to([1.0, 1.45, 0])
        o2 = onu_box("ONU", ONUC, 1.0, 0.44, 15).move_to([1.0, 0.75, 0])
        oe = emu_icon(1.3, 0.85, "ONU emülatörü").move_to([1.15, -0.45, 0])
        ds = VGroup(wire(sp.get_right(), o1[0].get_left()), wire(sp.get_right(), o2[0].get_left()), wire(sp.get_right(), oe[0].get_left()))
        sc = VGroup(scope(1.6, 0.9, ORIGIN), T("osiloskop", 14, MUTED, BOLD)).move_to([-4.7, -1.9, 0])
        sc[1].next_to(sc[0], DOWN, buff=0.06)
        tp = VGroup(wire(pd[0][0].get_bottom(), [-4.55, -1.45, 0], GOLD, 1.6, True), wire(pd[1][0].get_bottom(), [-4.85, -1.45, 0], GOLD, 1.6, True))
        pa = pa_icon(1.3, 0.85, "analizör").move_to([-0.75, -1.85, 0])
        pt = wire(sp.get_bottom(), pa[0].get_top(), MUTED, 1.6, True)
        tg = tg_icon(1.3, 0.85, "trafik üreteci").move_to([3.4, 1.1, 0])
        tw = wire(o1[0].get_right(), tg[0].get_left(), GOOD, 1.8, True)
        rec = VGroup(T("değeri olmayan her zamanlayıcıyı kaydedin:", 15, TXT, BOLD),
                     *[tag(s, TMRC, 14) for s in ("Tsstart", "Tpfail", "Thold", "Twfail", "Tictp", "TO2…TO5", "TPST", "Tseek")]).arrange(RIGHT, buff=0.1)
        fit(rec, 12.7).move_to([0, -3.02, 0])
        self.at(self.cue("iki OLT kanal sonlandırıcısı", 1.9))
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(emu), self.set_src("G.989.3 §18 · §19 · Tablo 11-9 · Ek XI · tezgâh: yorum"), run_time=0.5)
        self.at(self.cue("iki WM", 7.6))
        self.play(FadeIn(wm), *[Create(f) for f in fib], FadeIn(pd), run_time=0.5)
        self.at(self.cue("iki girişli bir ayırıcı", 8.2))
        self.play(Create(fd), FadeIn(sp), FadeIn(spl), *[Create(d) for d in ds], FadeIn(o1), FadeIn(o2), run_time=0.6)
        self.at(self.cue("optik anahtarlar", 11.1))
        self.play(FadeIn(sw1), FadeIn(sw2), FadeIn(swl), run_time=0.45)
        self.at(self.cue("fotodiyot ve osiloskop", 15.9))
        self.play(Indicate(pd, color=GOLD), Create(tp[0]), Create(tp[1]), FadeIn(sc), run_time=0.6)
        self.at(self.cue("bir protokol analizörü", 19.8))
        self.play(Create(pt), FadeIn(pa), run_time=0.4)
        self.at(self.cue("bir ONU emülatörü", 21.7))
        self.play(FadeIn(oe), run_time=0.35)
        self.play(Create(tw), FadeIn(tg), run_time=0.35)
        self.at(self.cue("Değeri olmayan her zamanlayıcıyı", 25.1))
        self.play(FadeIn(rec[0]), LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in rec[1:]], lag_ratio=0.08), run_time=0.7)
        self.end(pad=0.05)

        # g2 — TEST 1: switchover — cut the attachment fibre, the feeder and the CT power in turn; log LOS declaration, Tx-on, ONU sync, first BWmap-consistent
        #      burst; the only pass criterion from the text: the two DS outputs never overlap; then set Tpfail = Thold on purpose → the scope must show overlap
        self.beat("g2")
        h = self.next_test(1, "Anahtarlama", h)
        cuts = VGroup(*[VGroup(cutmark(ORIGIN, CUTC, 0.11), T(s, 16, TXT, BOLD)).arrange(RIGHT, buff=0.15) for s in ("1 · bağlantı fiberi", "2 · besleyici", "3 · CT gücü")])
        cuts.arrange(RIGHT, buff=0.6).move_to([-1.5, 1.85, 0])
        rl = VGroup(T("kaydet:", 16, MUTED, BOLD), *[tag(s, ACC, 15) for s in ("LOS ilanı", "Tx açılması", "ONU senkronu", "ilk BWmap-tutarlı burst")])
        rl.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-6.3, -0.25, 0], aligned_edge=LEFT)
        sc = scope(5.6, 2.6, [2.6, -0.15, 0])
        lb = VGroup(T("PD · CT 1", 14, CT1C, BOLD).move_to([-0.6, 0.4, 0]), T("PD · CT 2", 14, CT2C, BOLD).move_to([-0.6, -0.75, 0]))
        t1 = trace(sc, [(0.0, 0.8), (0.42, 0.8), (0.44, 0.58), (1.0, 0.58)], CT1C)
        t2 = trace(sc, [(0.0, 0.18), (0.56, 0.18), (0.58, 0.4), (1.0, 0.4)], CT2C)
        gap = VGroup(DashedLine([sc[0].get_left()[0] + 5.6 * 0.44, sc[0].get_bottom()[1], 0], [sc[0].get_left()[0] + 5.6 * 0.44, sc[0].get_top()[1], 0], color=GOOD, stroke_width=1.4),
                     DashedLine([sc[0].get_left()[0] + 5.6 * 0.57, sc[0].get_bottom()[1], 0], [sc[0].get_left()[0] + 5.6 * 0.57, sc[0].get_top()[1], 0], color=GOOD, stroke_width=1.4))
        crit = VGroup(T("tek geçme ölçütü:", 16, GOOD, BOLD), T("iki ↓ çıkış hiçbir an çakışmamalı", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([0.6, -2.0, 0])
        t2b = trace(sc, [(0.0, 0.18), (0.33, 0.18), (0.35, 0.4), (1.0, 0.4)], WARN)
        ovl = Rectangle(width=5.6 * 0.09, height=2.6, stroke_width=0, fill_color=WARN, fill_opacity=0.18).move_to([sc[0].get_left()[0] + 5.6 * 0.39, -0.15, 0])
        bad = VGroup(tag("Tpfail = Thold (bilerek)", WARN, 15), T("→ osiloskop çakışmayı göstermeli", 16, WARN, BOLD)).arrange(RIGHT, buff=0.15).move_to([0.6, -2.65, 0])
        self.play(self.set_src("G.989.3 §18.1 · §18.2.5 · Tablo 18-3 / 18-4"), run_time=0.3)
        for k, (key, d) in enumerate((("Bağlantı fiberini", 1.8), ("besleyiciyi ve", 3.3), ("sonlandırıcının gücünü", 4.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(cuts[k], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("kaybın ilanını", 7.7))
        self.play(FadeIn(rl[0]), FadeIn(rl[1]), FadeIn(sc), FadeIn(lb), run_time=0.4)
        for k, (key, d) in enumerate((("verici açmayı", 8.9), ("ONU senkronunu", 10.1), ("haritayla tutarlı ilk", 11.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rl[k + 2], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("tek geçme ölçütü", 14.9))
        self.play(Create(t1), Create(t2), run_time=0.8)
        self.at(self.cue("hiçbir an çakışmamalı", 17.6))
        self.play(FadeIn(gap), FadeIn(crit, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("koruma arızasını bilerek", 21.3))
        self.play(FadeIn(bad[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("osiloskop çakışmayı", 25.5))
        self.play(Create(t2b), FadeIn(ovl), FadeIn(bad[1], shift=LEFT * 0.05), run_time=0.6)
        self.end(pad=0.05)

        # g3 — TEST 2: ICTP-less system — cut ICTP, Tictp = 0: switching must wait for Tpfail; attenuate only the standby side's US input: with ICTP → COMM-FAIL
        #      in the dark, without → we expect an overlap; 40 km spool with Tract = 0.5 ms → both our inferences
        self.beat("g3")
        h = self.next_test(2, "ICTP'siz sistem", h)
        r1 = trow(1.55, "ICTP bağlantısını kes · Tictp = 0", [exp("anahtarlama Tpfail dolana kadar beklemeli", True, 16)], ICTPC)
        r2 = trow(0.45, "yalnızca bekleme tarafının ↑ girişini zayıflat (VOA)", [exp("ICTP varken: karanlıkta (9) iletişim arızası", True, 16),
                                                                                   VGroup(T("ICTP yokken:", 16, WARN, BOLD), T("çakışma bekleriz", 16, WARN, BOLD), ytag("bizim çıkarımımız")).arrange(RIGHT, buff=0.12)], GOLD)
        r3 = trow(-0.95, "40 km makara (DD40) · Tract = 0,5 ms", [VGroup(T("ilk burst ≈ 561 µs > 0,5 ms → sahte COMM-FAIL?", 16, TXT, BOLD), ytag("bizim çıkarımımız")).arrange(RIGHT, buff=0.12)], GOLD)
        sp_ = spool("40 km", FEED, 0.38).move_to([-5.6, -2.3, 0])
        both = VGroup(T("iki çıkarımı da sınayın:", 17, GOLD, BOLD), tag("Tract ↔ mesafe (b11)", GOLD, 15), tag("ICTP'siz çakışma (b12)", GOLD, 15)).arrange(RIGHT, buff=0.15).move_to([0.6, -2.3, 0])
        self.play(self.set_src("G.989.3 §18.3 · Şekil 18-3 · §18.2.5 · çıkarımlar: Perde 1"), run_time=0.3)
        self.at(self.cue("ICTP'yi kesip", 2.4))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("anahtarlama koruma arızasını", 5.8))
        self.play(GrowArrow(r1[1]), FadeIn(r1[2], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("yalnızca bekleme tarafının", 9.3))
        self.play(FadeIn(r2[0], shift=RIGHT * 0.05), GrowArrow(r2[1]), run_time=0.4)
        self.at(self.cue("ICTP varken karanlıkta", 14.7))
        self.play(FadeIn(r2[2][0], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("yokken bir çakışma", 18.9))
        self.play(FadeIn(r2[2][1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Kırk kilometrelik makarayla", 21.2))
        self.play(FadeIn(r3[0], shift=RIGHT * 0.05), GrowArrow(r3[1]), FadeIn(r3[2], shift=LEFT * 0.05), FadeIn(sp_), run_time=0.5)
        self.at(self.cue("iki çıkarımımızı da", 27.6))
        self.play(FadeIn(both, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g4 — TEST 3: exclusions and violations — all ONUs send dying gasp: the Active CT must not declare QLOS and must send periodic Standby-LOS() to its peer;
        #      inject a Standby message into the Working CT: report, Tx off, back to Initialization (Note 2); reboot a CT while its peer works: it must stay dark
        self.beat("g4")
        h = self.next_test(3, "Dışlamalar ve ihlaller", h)
        r1 = trow(1.5, "bütün ONU'lara son nefes (DG) gönderttir", [exp("etkin taraf QLOS ilan etmemeli", True, 16),
                                                                    exp("eşine periyodik ICTP: Standby-LOS()", True, 16, ICTPC)], GOLD)
        r2 = trow(-0.1, "çalışan CT'ye ICTP: Standby-*() enjekte et", [exp("raporla · vericiyi kapat", True, 16), exp("(1) başlatmaya dön · Tablo 18-4 Not 2", True, 16)], ICTPC)
        r3 = trow(-1.7, "eşi çalışırken bir CT'yi yeniden başlat", [exp("karanlık kalmalı: sessiz başlangıç (1) → (2) → (3)", True, 16)], STBC)
        self.play(self.set_src("G.989.3 Tablo 18-3 (QLOS dışlamaları) · Tablo 18-4 Not 2 · §19.3.2"), run_time=0.3)
        self.at(self.cue("son nefes gönderttirin", 3.0))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.05), GrowArrow(r1[1]), run_time=0.4)
        self.at(self.cue("nitelikli kayıp ilan etmemeli", 6.2))
        self.play(FadeIn(r1[2][0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("periyodik bekleme ve kayıp", 9.7))
        self.play(FadeIn(r1[2][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Çalışan tarafa bekleme", 14.3))
        self.play(FadeIn(r2[0], shift=RIGHT * 0.05), GrowArrow(r2[1]), run_time=0.4)
        self.at(self.cue("raporlamalı,", 17.9))
        self.play(FadeIn(r2[2][0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("başlatmaya dönmelidir", 20.5))
        self.play(FadeIn(r2[2][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("yeniden başlatın", 22.4))
        self.play(FadeIn(r3[0], shift=RIGHT * 0.05), GrowArrow(r3[1]), run_time=0.4)
        self.at(self.cue("karanlık kalmalıdır", 26.7))
        self.play(FadeIn(r3[2], shift=LEFT * 0.05), run_time=0.3)
        self.end(pad=0.05)
        self.save_timeline("ep20_labA")


class E20LabB(LabAct):
    HDR, MANIFEST, PREV_BADGE = H20["L"], M20("lab"), "lab"

    def construct(self):
        # g5 — TEST 4: ONU-side protection: configure the protection channel (Protection_Control), kill the working channel: O6 → O8, sync on the protection
        #      channel, Tuning_Response on the contention grant; measure the time to the first directed grant as TPST; two ONUs at once → collision → directed grants to all
        self.beat("g5")
        h = step_head(self, 4, "ONU tarafı koruma")
        self.play(self.set_src("G.989.3 §11.3.3.15 · Tablo 12-1 / 12-4 · Ek J.2.2 · §7.1.1 (TPST)"), run_time=0.3)
        r1 = trow(1.6, "Protection_Control (0x19) · bayrak 0x00", [exp("ONU saklar · Acknowledgement ↑", True, 16)], GOOD)
        ch = VGroup(*[sbox(s, None, SM_COL[k], 0.95, 0.46, 16) for s, k in (("O5", "O5.1"), ("O6", "O6"), ("O8", "O8.1"), ("O9", "O9"))]).arrange(RIGHT, buff=0.35)
        ca = VGroup(*[arrow(ch[i][0].get_right(), ch[i + 1][0].get_left(), MUTED, 2, 0.1) for i in range(3)])
        chg = VGroup(ch, ca)
        r2 = trow(0.55, "çalışan kanalı söndür", [VGroup(chg, T("koruma kanalında senkron", 15, OPC, BOLD)).arrange(RIGHT, buff=0.2)], WARN, 3.6)
        r3 = trow(-0.5, "çekişmeli tahsis (işlev 0x02)", [exp("Tuning_Response (Complete_u) ↑", True, 16)], GOLD)
        yl = -1.55
        lne = Line([-1.0, yl, 0], [5.6, yl, 0], color=MUTED, stroke_width=2)
        m0 = tmark(-0.6, yl - 0.2, yl + 0.25, "↓ senkron", OPC, 14)
        m1 = tmark(4.2, yl - 0.2, yl + 0.25, "ilk yönlü tahsis", ACC, 14)
        br = brace_lbl(Line([-0.6, yl - 0.25, 0], [4.2, yl - 0.25, 0]), "ölç → TPST", GOLD, DOWN, 16)
        tl = stim("süreyi ölç", TMRC, 2.6).move_to([-4.95, yl, 0])
        r5 = trow(-2.75, "iki ONU'yu birlikte geçir → çarpışma", [exp("OLT herkese yönlü tahsisi hemen geri vermeli", True, 16)], WARN)
        self.at(self.cue("Koruma kanalını mesajla", 2.7))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.05), GrowArrow(r1[1]), FadeIn(r1[2], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("çalışan kanalı söndürün", 5.2))
        self.play(FadeIn(r2[0], shift=RIGHT * 0.05), GrowArrow(r2[1]), run_time=0.4)
        self.at(self.cue("ONU O6'dan O8'e", 7.7))
        self.play(FadeIn(r2[2][0][0], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("koruma kanalında senkron", 9.8))
        self.play(FadeIn(r2[2][0][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("çekişmeli tahsise ayar", 12.5))
        self.play(FadeIn(r3[0], shift=RIGHT * 0.05), GrowArrow(r3[1]), FadeIn(r3[2], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("İlk yönlü tahsise kadarki", 16.2))
        self.play(FadeIn(tl, shift=RIGHT * 0.05), Create(lne), FadeIn(m0), FadeIn(m1), run_time=0.5)
        self.play(FadeIn(br, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("İki ONU'yu birlikte", 21.5))
        self.play(FadeIn(r5[0], shift=RIGHT * 0.05), GrowArrow(r5[1]), run_time=0.4)
        self.at(self.cue("çarpışmada OLT herkese", 23.9))
        self.play(FadeIn(r5[2], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g6 — TEST 5: rogue ONUs from the emulator: outside its StartTime → LOBi at the victims, TIWi after three corrections; on the neighbouring US channel →
        #      LOBi at the host, interference at the neighbour, ICTP alerts; then the extreme case: disable the channel at once, re-enable ONUs one by one
        self.beat("g6")
        h = self.next_test(5, "Başıboş ONU'lar", h)
        r1 = trow(1.45, "emülatör: StartTime dışında gönder (a)", [exp("kurbanlarda LOBi", True, 16), exp("3 düzeltmeden sonra TIWi uyarısı", True, 16)], GOLD)
        r2 = trow(-0.2, "emülatör: komşu ↑ kanalda gönder (b)", [exp("ev sahibi CT: LOBi · komşu CT: girişim", True, 16),
                                                                   VGroup(ok_x(True, 18), T("ICTP:", 16, ICTPC, BOLD), HX("onuAlert()", 15, ICTPC, BOLD), HX("rogueAlert()", 15, ICTPC, BOLD)).arrange(RIGHT, buff=0.12)], WARN)
        r3 = trow(-1.85, "uç durum: kanalı topluca kapat", [VGroup(HX("0x0F", 16, WARN, BOLD), T("→ hepsi O7 ·", 16, TXT, BOLD), HX("0x00 + SN", 16, GOOD, BOLD), T("→ tek tek aç", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.12)], WARN)
        self.play(self.set_src("G.989.3 §19.1 · Tablo 14-2 (LOBi, TIWi) · Tablo VI.3 · §12.1.5 · Tablo 11-9"), run_time=0.3)
        self.at(self.cue("başlangıç zamanının dışında", 2.5))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.05), GrowArrow(r1[1]), run_time=0.4)
        self.at(self.cue("kurbanlarda burst kaybı", 6.5))
        self.play(FadeIn(r1[2][0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("üç düzeltmeden sonra", 8.6))
        self.play(FadeIn(r1[2][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Komşu yukarı yön kanalında", 12.4))
        self.play(FadeIn(r2[0], shift=RIGHT * 0.05), GrowArrow(r2[1]), run_time=0.4)
        self.at(self.cue("ev sahibinde burst kaybı", 15.4))
        self.play(FadeIn(r2[2][0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("ICTP uyarıları", 18.9))
        self.play(FadeIn(r2[2][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Sonra uç durumu", 20.2))
        self.play(FadeIn(r3[0], shift=RIGHT * 0.05), GrowArrow(r3[1]), run_time=0.4)
        self.at(self.cue("kanalı topluca kapatın", 22.4))
        self.play(FadeIn(r3[2][:2], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("ONU'ları tek tek açın", 24.4))
        self.play(FadeIn(r3[2][2:], shift=LEFT * 0.05), run_time=0.3)
        self.end(pad=0.05)

        # g7 — TEST 6: alien light and the idle window: a continuous-mode 10G module on a spare splitter port must be rejected in a quiet window (invalid PSBu);
        #      then withhold all grants, open an idle window and read the OLT received power; S1·B10's resolution was 0.1 dB
        self.beat("g7")
        h = self.next_test(6, "Yabancı ışık ve boş pencere", h)
        olt = ctu("OLT CT", OLTC, True, 1.5, 0.5, 16).move_to([-5.6, 1.1, 0])
        sp = splitter(0.3).move_to([-3.2, 1.1, 0])
        f = wire(olt[0].get_right(), sp.get_left())
        on = VGroup(*[onu_box("ONU", ONUC, 0.95, 0.42, 15).move_to([-1.2, y, 0]) for y in (1.75, 1.1)])
        port = Circle(radius=0.09, stroke_color=MUTED, stroke_width=2, fill_color=BG, fill_opacity=1).move_to([-1.65, 0.45, 0])
        ds = VGroup(*[wire(sp.get_right(), o[0].get_left()) for o in on], wire(sp.get_right(), port.get_left()))
        sfp = VGroup(RoundedRectangle(corner_radius=0.06, width=2.75, height=0.5, stroke_color=PTPC, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                     T("10G modül · sürekli kip", 15, PTPC, BOLD)).move_to([0.45, 0.45, 0])
        fit(sfp[1], 2.55).move_to(sfp[0])
        sw = wire(port.get_right(), sfp[0].get_left(), PTPC, 2.2)
        q1 = VGroup(tag("sessiz pencere", QWC, 15), T("→ PSBu geçersiz →", 16, TXT, BOLD), T("reddet", 17, GOOD, BOLD), tag("§19.4 · shall", GOLD, 14)).arrange(RIGHT, buff=0.15)
        q1.move_to([-6.3, -0.55, 0], aligned_edge=LEFT)
        q2 = VGroup(tag("boş pencere", QWC, 15), T("bütün tahsisleri geri tut → OLT'nin alınan gücünü oku", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        q2.move_to([-6.3, -1.4, 0], aligned_edge=LEFT)
        pm = inst("PM", "OLT alınan güç", 1.6, 1.1, "dBm", c1=GOLD).move_to([4.6, 0.9, 0])
        rs = VGroup(chipz_s1(10), T("çözünürlük 0,1 dB", 17, S1C, BOLD)).arrange(RIGHT, buff=0.15).move_to([-6.3, -2.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(olt), Create(f), FadeIn(sp), *[Create(d) for d in ds], FadeIn(on), FadeIn(port), self.set_src("G.989.3 §19.4 · §19.5 · S1·B10 (G.989.2 Ek II)"), run_time=0.6)
        self.at(self.cue("Boş bir ayırıcı portuna", 3.4))
        self.play(Create(sw), FadeIn(sfp, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("sessiz pencerede sonlandırıcı", 9.9))
        self.play(FadeIn(q1[:2], shift=RIGHT * 0.05), run_time=0.35)
        self.play(FadeIn(q1[2:], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("bütün tahsisleri geri tutup", 15.8))
        self.play(FadeIn(q2, shift=RIGHT * 0.05), FadeIn(pm, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("birinci sezonun onuncu", 23.0))
        self.play(FadeIn(rs, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep20_labB")


def chipz_s1(n):
    return tag(f"S1·B{n}", S1C, 15)


class E20LabC(LabAct):
    HDR, MANIFEST, PREV_BADGE = H20["L"], M20("lab"), "lab"

    def construct(self):
        # g8 — TEST 7: emergency stop: disable one ONU with a non-zero Reason Code (it must log it); OSA: laser below −62.6 dBm (/15 GHz); power cycle → stays in O7
        #      (a dark channel → may look at the protection channel first); Enable only on a channel it does not listen to → stays off; on all channels → O1, SN
        #      carries code 5 (Activation Debug 0101)
        self.beat("g8")
        h = step_head(self, 7, "Acil durdurma")
        self.play(self.set_src("G.989.3 Tablo 11-9 (Amd.2) · Tablo 12-1 / 12-4 · Ek XI · Tablo 11-25 (Activation Debug) · G.989.2 §11.1.5.2.9"), run_time=0.3)
        r1 = trow(1.65, "Disable (0xFF + SN) · neden kodu ≠ 0", [exp("ONU kodu kaydeder", True, 16)], WARN)
        osa = inst("OSA", "OSA", 1.4, 0.95, "λ", c1=GOLD).move_to([-5.5, 0.35, 0])
        r2 = VGroup(T("lazer", 16, TXT, BOLD), T("< −62,6 dBm / 15 GHz", 18, GOLD, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.15).move_to([-4.4, 0.45, 0], aligned_edge=LEFT)
        r3 = trow(-0.75, "güç döngüsü", [exp("O7'de kalır", True, 16), exp("kanalı karanlıksa: önce koruma kanalını arayabilir (O7.2)", True, 16, MUTED)], WARN, 3.0)
        r4 = trow(-1.95, "Enable yalnızca dinlemediği kanalda", [exp("kapalı kalır", False, 16)], GOOD, 4.6)
        r4b = VGroup(T("bütün kanallarda →", 16, GOOD, BOLD), sbox("O1", None, O1C, 0.8, 0.42, 16), T("· Serial_Number_ONU: Activation Debug", 15, TXT, BOLD),
                     HX("0101", 18, GOOD, BOLD), T("= 5", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.12)
        fit(r4b, 12.6).move_to([-6.35, -2.75, 0], aligned_edge=LEFT)
        self.at(self.cue("neden koduyla kapatın", 2.3))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.05), GrowArrow(r1[1]), run_time=0.4)
        self.at(self.cue("kodu kaydetmeli", 6.8))
        self.play(FadeIn(r1[2], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("OSA ile lazerin", 8.1))
        self.play(FadeIn(osa, shift=UP * 0.05), FadeIn(r2[0]), run_time=0.4)
        self.at(self.cue("altmış iki virgül altı", 10.9))
        self.play(FadeIn(r2[1:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Gücü kesip açın", 15.4))
        self.play(FadeIn(r3[0], shift=RIGHT * 0.05), GrowArrow(r3[1]), run_time=0.35)
        self.at(self.cue("O7'de kalmalı", 16.7))
        self.play(FadeIn(r3[2][0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("kanalı karanlıksa", 17.9))
        self.play(FadeIn(r3[2][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("dinlemediği kanalda", 22.1))
        self.play(FadeIn(r4[0], shift=RIGHT * 0.05), GrowArrow(r4[1]), run_time=0.35)
        self.at(self.cue("kapalı kalmalı", 25.9))
        self.play(FadeIn(r4[2], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Bütün kanallarda gönderin", 27.2))
        self.play(FadeIn(r4b[0], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("O1'e dönmeli", 29.4))
        self.play(FadeIn(r4b[1]), run_time=0.25)
        self.at(self.cue("beş kodunu taşımalı", 30.5))
        self.play(FadeIn(r4b[2:], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g9 — TEST 8: discovery stop and the stubborn ONU: 0x3F during SN acquisition → ONUs in O2-3 drop to O7 and stay there after a power cycle; keep granting an
        #      emulator that ignores the disable → DFi must be declared
        self.beat("g9")
        h = self.next_test(8, "Keşif durdurma ve inatçı ONU", h)
        r1 = trow(1.3, "SN alımı sırasında 0x3F (Disable_Discovery)", [VGroup(sbox("O2-3", None, SNC, 1.0, 0.42, 16), T("→", 17, MUTED, BOLD), sbox("O7", None, ESC, 0.8, 0.42, 16)).arrange(RIGHT, buff=0.15),
                                                                     exp("güç döngüsünden sonra da O7", True, 16)], WARN)
        r2 = trow(-0.8, "kapatmayı yok sayan emülatöre tahsis vermeyi sürdür", [VGroup(ok_x(True, 18), T("DFi ilan edilmeli", 17, DEFC, BOLD)).arrange(RIGHT, buff=0.12),
                                                                                 T("(tahsis kesilirse başarısızlık görünmez)", 15, MUTED, BOLD)], WARN, 6.0)
        self.play(self.set_src("G.989.3 Tablo 11-9 (0x3F) · Tablo 12-4 · Tablo 14-2 (DFi)"), run_time=0.3)
        self.at(self.cue("üç ef seçeneğini", 3.7))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.05), GrowArrow(r1[1]), run_time=0.4)
        self.at(self.cue("O2-3'teki ONU'lar O7'ye", 8.4))
        self.play(FadeIn(r1[2][0], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("güç döngüsünden sonra", 11.1))
        self.play(FadeIn(r1[2][1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Kapatmayı yok sayan", 14.8))
        self.play(FadeIn(r2[0], shift=RIGHT * 0.05), GrowArrow(r2[1]), run_time=0.4)
        self.at(self.cue("devre dışı bırakma başarısızlığı", 19.7))
        self.play(FadeIn(r2[2], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g10 — TEST 9: the life of a packet: one 1518-byte frame; the analyzer must show downstream the header and the two pad bytes, upstream the report's 380,
        #       the 96-block grant, the 1800-byte burst and the 4-byte short idle
        self.beat("g10")
        h = self.next_test(9, "Bir paketin hayatı", h)
        tg = tg_icon(1.6, 1.1, "1 × 1518 B").move_to([-5.5, 0.4, 0])
        p = apanel(9.4, 4.3, "Analizör · bir paketin hayatı", GOOD).move_to([1.45, 0.05, 0])
        top = panel_top(p, 0.15)
        dl = T("↓ aşağı yön", 16, CH[1], BOLD).move_to([-3.05, top - 0.15, 0], aligned_edge=LEFT)
        d1 = kv("XGEM başlığı", "0x17B90400000020A7", 16, 17, kw=2.2).move_to([-2.85, top - 0.6, 0], aligned_edge=LEFT)
        d2 = kv("dolgu", "55 55  (2 B)", 16, 17, kw=2.2).move_to([-2.85, top - 1.05, 0], aligned_edge=LEFT)
        ul = T("↑ yukarı yön", 16, ONUC, BOLD).move_to([-3.05, top - 1.6, 0], aligned_edge=LEFT)
        u1 = kv("DBRu", "00 01 7C 66  (BufOcc 380)", 16, 17, kw=2.2).move_to([-2.85, top - 2.05, 0], aligned_edge=LEFT)
        u2 = kv("GrantSize", "96 blok", 16, 17, kw=2.2).move_to([-2.85, top - 2.5, 0], aligned_edge=LEFT)
        u3 = kv("FEC'li burst", "1800 B", 16, 17, kw=2.2).move_to([-2.85, top - 2.95, 0], aligned_edge=LEFT)
        u4 = kv("kısa boş", "4 B (tahsisin sonunda)", 16, 17, kw=2.2).move_to([-2.85, top - 3.4, 0], aligned_edge=LEFT)
        bz = ytag("bizim hesabımız — altın vektör değil").next_to(p, DOWN, buff=0.12).align_to(p, RIGHT)
        self.play(self.set_src("Perde 4 değerleri · bizim hesabımız (S2·B10)"), run_time=0.3)
        self.at(self.cue("Tek bir bin beş yüz", 2.9))
        self.play(FadeIn(tg, shift=RIGHT * 0.05), FadeIn(p), run_time=0.5)
        self.at(self.cue("aşağı yönde başlığı", 7.4))
        self.play(FadeIn(dl), FadeIn(d1, shift=RIGHT * 0.05), FadeIn(bz), run_time=0.4)
        self.play(FadeIn(d2, shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("raporun üç yüz seksenini", 11.6))
        self.play(FadeIn(ul), FadeIn(u1, shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("doksan altı blokluk", 14.7))
        self.play(FadeIn(u2, shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("bin sekiz yüz baytlık", 17.1))
        self.play(FadeIn(u3, shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("dört baytlık kısa boş", 19.9))
        self.play(FadeIn(u4, shift=RIGHT * 0.05), run_time=0.3)
        self.end(pad=0.05)

        # g11 — lab note
        self.note11("g11", [("1", "Koruma sürelerini tek bir zaman tabanında toplayın",
                             "Analizörün zaman damgası ile fotodiyotun kenarı aynı eksende durmalıdır.", "koruma sürelerini"),
                            ("2", "Sezonun defteri artık bir kabul test planıdır",
                             "Her satırda: madde numarası · ölçülen değer ·\nstandardın vermediği her değer için sizin seçiminiz.", "İki:")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep20_labC")


POINTS = [("G.989.3: G.987.3 üstüne üç alt katmanlı bir dil · 9 kimlik · 125 µs", "S2·B1–B2"),
          ("Veri XGEM ile taşınır, DBA ile paylaşılır, PLOAM ve OMCC ile yönetilir", "S2·B3–B5"),
          ("ONU'nun hayatı bir durum makinesi: aktivasyon, mesafe, devir, acil durdurma", "S2·B6–B7 · B10"),
          ("Güven ve sağlık da protokol: AES anahtarları, dikkatli uyku, 111 sayaç, 10 kusur", "S2·B8–B9"),
          ("Koruma ve başıboşluk: B tipinde 10 durum, 6 zamanlayıcı — tek değer", "S2·B10")]
QA = [("B tipi makinenin üç\nsinyal olayı nedir?",
       [("SLOS:", "yayın yapmayan durumlarda\n0,5 ms (4 çerçeve) sessizlik"), ("QLOS:", "yayın yapan durumlarda 4 çerçeve\nsessizlik + bütün ONU'larda LOBi"),
        ("LOS temizlendi:", "haritayla tutarlı bir burst")], CH[0]),
      ("Tpfail neden Thold ve\nTwfail'den büyüktür?",
       [("Çünkü:", "koruyan taraf, çalışan taraf\nsusmadan konuşmasın"), ("Sıra:", "Tpfail > Thold > Twfail\n(§18.2.5)")], CH[1]),
      ("Acil durdurmadaki ONU\nkaranlıkta yeniden başlarsa?",
       [("O7.2:", "kanal tarar — önce olası\nkanallar, Tseek ≈ 1 dk'ya kadar"), ("Çıkış:", "yalnızca bütün kanallarda\ngönderilen açmayla → O1")], CH[3])]


class E20End(Act20):
    HDR, MANIFEST, FIRST = H20["E"], M20("end"), True

    def construct(self):
        # h1/h2 — season summary (five points), the closing rule: where the standard is silent, the engineer picks and writes a value
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Sezonun özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header_badge(tc, "ozet", 0.5)
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT), 9.6)
            ch = tag(c, GOLD, 16)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.95, -1.65, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.75, y, 0])
        last = VGroup(T("Standardın sustuğu her yer", 22, TXT, BOLD), T("→ mühendisin bir değer seçip yazacağı yer", 22, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.75, 0])
        fit(last, 12.6)
        for k, (key, d) in enumerate((("G.989.3,", 1.5), ("İki:", 13.1), ("Üç:", 19.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((3, 4), (("Dört:", 0.0), ("Beş:", 8.1))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("Standardın sustuğu her yer", 19.4))
        self.play(FadeIn(last[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("mühendisin bir değer", 21.7))
        self.play(FadeIn(last[1], shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.15)

        # h3 — quiz with the answers right after each question
        self.beat("h3")
        self.clear()
        ttl = VGroup(T("Kendini test et", 36, TXT, BOLD), T("cevaplar hemen ardından", 20, MUTED, BOLD)).arrange(RIGHT, buff=0.4).move_to([0, 2.45, 0])
        cards = VGroup()
        for i, (q, ans, c) in enumerate(QA):
            r = RoundedRectangle(corner_radius=0.16, width=4.15, height=4.95, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            hd = T(f"Soru {i + 1}", 22, c, BOLD)
            qt = T(q, 18, TXT, BOLD, line_spacing=0.85)
            dv = Line(LEFT * 1.8, RIGHT * 1.8, color=LINE, stroke_width=1.5)
            al = T("Cevap", 16, GOOD, BOLD)
            parts = VGroup(*[VGroup(T(a, 15, GOOD, BOLD), T(b, 15, TXT, BOLD, line_spacing=0.85)).arrange(DOWN, aligned_edge=LEFT, buff=0.05) for a, b in ans])
            parts.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            body = VGroup(hd, qt, dv, al, parts).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            fit(body, 3.75)
            body.move_to(r).align_to(r, UP).shift(DOWN * 0.22)
            dv.set_x(r.get_x())
            cards.add(VGroup(r, hd, qt, dv, al, parts))
        cards.arrange(RIGHT, buff=0.25).move_to([0, -0.5, 0])
        self.play(FadeIn(ttl[0]), run_time=0.5)
        self.at(self.cue("cevaplar hemen ardından", 1.4))
        self.play(FadeIn(ttl[1], shift=LEFT * 0.1), run_time=0.4)
        plan = [(0, "Birinci soru", 3.4, [("basit kayıp,", 8.4), ("nitelikli kayıp,", 13.8), ("temizlenme,", 21.7)]),
                (1, "İkinci soru", 25.0, [("koruyan,", 31.8), ("çalışan susmadan", 32.5)]),
                (2, "Üçüncü soru", 35.3, [("O7.2'de kanal tarar", 41.1), ("yalnızca bütün kanallarda", 42.8)])]
        for k, key, d, ans in plan:
            self.at(self.cue(key, d))
            self.play(FadeIn(cards[k][:4], shift=UP * 0.15), run_time=0.6)
            for j, (ak, ad) in enumerate(ans):
                self.at(self.cue(ak, ad))
                self.play(*([FadeIn(cards[k][4])] if j == 0 else []), FadeIn(cards[k][5][j], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.1)

        # h4 — two seasons, two halves: season 1 physics (G.989.2), season 2 language (G.989.3); related work named in the sources; no successor named
        self.beat("h4")
        self.clear()
        self.drop_badge()

        def chips(eps, color, label):
            g = VGroup()
            for e in eps:
                r = RoundedRectangle(corner_radius=0.1, width=2.45, height=0.68, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
                t = VGroup(T(f"B{e['n']}", 14, color, BOLD), tf(e["title"], 15, TXT, BOLD, w=2.3)).arrange(DOWN, buff=0.03)
                fit(t, 2.3).move_to(r)
                g.add(VGroup(r, t))
            VGroup(VGroup(*g[:5]).arrange(RIGHT, buff=0.1), VGroup(*g[5:]).arrange(RIGHT, buff=0.1)).arrange(DOWN, buff=0.1)
            return g
        s1 = chips(SERIES["episodes"], S1C, "S1").move_to([0, 1.2, 0])
        s2 = chips(SERIES["season2"]["episodes"], ACC, "S2").move_to([0, -0.88, 0])
        l1 = VGroup(T("Sezon 1 · fizik", 20, S1C, BOLD), T("G.989.2 · dalga boyları · güç bütçeleri · burst'ler", 17, TXT, BOLD)).arrange(RIGHT, buff=0.3)
        l1.next_to(s1, UP, buff=0.12).align_to(s1, LEFT)
        l2 = VGroup(T("Sezon 2 · dil", 20, ACC, BOLD), T("G.989.3 · bitlerin hangi sırayla ve neden taşındığı", 17, TXT, BOLD)).arrange(RIGHT, buff=0.3)
        l2.next_to(s2, UP, buff=0.12).align_to(s2, LEFT)
        nb = VGroup(T("komşu işler:", 16, MUTED, BOLD), *[tag(s, GOLD, 15) for s in ("G.9802 ailesi", "G.988 · OMCI", "G.987.3 · temel", "G.984 ailesi",
                                                                                     "G-Sup.45", "G-Sup.49", "G-Sup.81", "G-Sup.84")]).arrange(RIGHT, buff=0.1)
        fit(nb, 12.7).move_to([0, -2.2, 0])
        nx = VGroup(T("sonraki nesil: adı geçmez ·", 17, TXT, BOLD), T("özet yalnızca “100 Gbit/s ve ötesi” der", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -2.95, 0])
        self.at(self.cue("Birinci sezon fizikti", 2.5))
        self.play(FadeIn(l1[0], shift=RIGHT * 0.1), LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in s1], lag_ratio=0.06), run_time=1.0)
        self.at(self.cue("dalga boyları,", 5.1))
        self.play(FadeIn(l1[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("İkinci sezon dildi", 8.3))
        self.play(FadeIn(l2[0], shift=RIGHT * 0.1), LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in s2], lag_ratio=0.06), run_time=1.0)
        self.at(self.cue("bitlerin hangi sırayla", 10.6))
        self.play(FadeIn(l2[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Kaynaklar komşu işleri", 14.2))
        self.play(FadeIn(nb[0]), run_time=0.3)
        for idx, key, d in (((1,), "G.9802 ailesi", 17.4), ((2,), "OMCI'ın G.988'i", 20.7), ((3,), "temelimiz G.987.3", 22.1), ((4,), "G.984 ailesi", 23.6),
                            ((5,), "G serisinin kırk beş", 26.5), ((6,), "kırk dokuz,", 28.5), ((7, 8), "seksen bir ve", 29.5)):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(nb[i], shift=UP * 0.05) for i in idx], run_time=0.3)
        self.at(self.cue("Bir sonraki nesli", 32.6))
        self.play(FadeIn(nx[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("yüz gigabit ve ötesinden", 35.4))
        self.play(FadeIn(nx[1], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.1)

        # h5 — LAMBDA — end of the series, then the season-2 credits
        self.beat("h5")
        fin = VGroup(T("LAMBDA", 72, ACC, BOLD), T("Dizinin sonu", 40, TXT, BOLD)).arrange(DOWN, buff=0.25).move_to([0, 1.65, 0])
        lam = VGroup(*[Line([-1.6 + 0.32 * i, 0.15, 0], [-1.6 + 0.32 * i, 0.6, 0], color=CH[i % 4], stroke_width=5) for i in range(11)])
        jr = VGroup(T("20 bölüm: bir ışık darbesinden bir PLOAM mesajına,", 21, TXT, BOLD), T("bir fiber kesiğinden bir paketin hayatına", 21, TXT, BOLD)).arrange(DOWN, buff=0.12).move_to([0, -0.75, 0])
        vb = VGroup(tag("söylediğini oku", ACC, 18), tag("söylemediğini gör", GOLD, 18), tag("ikisini laboratuvarda sına", GOOD, 18)).arrange(RIGHT, buff=0.3).move_to([0, -1.85, 0])
        th = T("İzlediğiniz için teşekkürler · görüşmek üzere", 24, MUTED).move_to([0, -2.85, 0])
        self.play(*[FadeOut(m) for m in self.mobjects], FadeIn(fin[0], scale=0.9), run_time=0.8)
        self.play(FadeIn(fin[1], shift=UP * 0.15), LaggedStart(*[Create(l) for l in lam], lag_ratio=0.08), run_time=0.9)
        self.at(self.cue("Yirmi bölüm boyunca", 1.9))
        self.play(FadeIn(jr[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("bir fiber kesiğinden", 6.9))
        self.play(FadeIn(jr[1], shift=UP * 0.1), run_time=0.5)
        for k, (key, d) in enumerate((("standardın söylediğini okumayı", 11.5), ("söylemediğini görmeyi", 14.1), ("ve ikisini laboratuvarda", 16.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(vb[k], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("İzlediğiniz için", 18.8))
        self.play(FadeIn(th, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.6)
        self.play(FadeOut(VGroup(fin, lam, jr, vb, th)), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP20['n']} · {EP20['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep20_end")
