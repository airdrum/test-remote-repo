"""S2·B8 · Laboratuvarda (altın vektörler, sayaç bloğu, anahtar değişimi zamanlaması, başarısız yenileme, anahtar denetimi, MIC hatası
enjeksiyonu, varsayılan anahtarlı acil durdurma, kayıt zinciri, Şekil 15-8 izi, azaltılmış güç ve zayıf sayaç) and Kapanış."""
from ep18_common import *


class LabAct(Act18):
    def next_test(self, n, title, h, rt=0.4):
        keep = {self.hdr, self.badge, h}
        out = [m for m in self.mobjects if m not in keep]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=rt)
        if self.src is not None and self.src in out:
            self.src = None
        return step_head(self, n, title, h)


def ivrow(tag_, what, val, ok=True, color=TXT):
    return VGroup(T(tag_, 16, GOLD, BOLD), T(what, 16, TXT, BOLD), HX(val, 16, color, BOLD), ok_x(ok, 17))


def place_rows(rows, top, xs, dy=0.42):
    for k, r in enumerate(rows):
        y = top - k * dy
        for c, x in zip(r, xs):
            c.move_to([x, y, 0], aligned_edge=LEFT)


class E18LabA(LabAct):
    HDR, MANIFEST, FIRST = H18["L"], M18("lab"), True

    def construct(self):
        # g1 — bench: OLT and ONU emulator, analyzer with decryption + MIC engines, traffic generator, a second ONU emulator on a spare splitter
        #      port (our attacker); isolated test network only
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Anahtarlar, kodlar ve sayaç blokları")
        self.at(self.cue("Düzenek", 1.0))
        h = self.heading("Düzenek")
        self.to_header_badge(tc, "lab", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        olt = emu_icon(1.9, 1.3, "OLT emülatörü").move_to([-5.2, 0.95, 0])
        sp = splitter(0.34).move_to([-2.0, 0.95, 0])
        fd = Line(olt[0].get_right(), sp.get_left(), color=FEED, stroke_width=2.5)
        onu = emu_icon(1.9, 1.3, "ONU emülatörü").move_to([1.5, 1.55, 0])
        atk = emu_icon(1.9, 1.3, "2. ONU emülatörü").move_to([1.5, -0.9, 0])
        atk[0].set_stroke(ATKC)
        d1 = Line(sp.get_right(), onu[0].get_left(), color=FEED, stroke_width=2)
        d2 = Line(sp.get_right(), atk[0].get_left(), color=ATKC, stroke_width=2)
        spr = T("boş port", 15, ATKC, BOLD).next_to(d2.point_from_proportion(0.55), LEFT, buff=0.15)
        atl = tag("saldırganımız", ATKC, 16).next_to(atk, RIGHT, buff=0.3)
        pa = pa_icon(1.9, 1.3, "Analizör").move_to([-3.25, -1.35, 0])
        pl = VGroup(T("şifre çözme motoru", 15, ACC, BOLD), T("bütünlük (MIC) motoru", 15, MICC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(pa, LEFT, buff=0.2)
        tp = DashedLine([-3.25, 0.95, 0], pa[0].get_top(), color=MUTED, stroke_width=1.6)
        tg = tg_icon(1.9, 1.3, "Trafik üreteci").move_to([5.3, 1.55, 0])
        tl = DashedLine(tg[0].get_left(), onu[0].get_right(), color=GOOD, stroke_width=1.6)
        iso = VGroup(lock(WARN, 0.26), T("yalnızca yalıtılmış bir test ağında", 18, WARN, BOLD)).arrange(RIGHT, buff=0.15).move_to([3.4, -2.75, 0])
        self.at(self.cue("bir OLT ve ONU emülatörü", 1.7))
        self.play(FadeIn(olt, shift=UP * 0.1), Create(fd), FadeIn(sp), Create(d1), FadeIn(onu, shift=UP * 0.1),
                  self.set_src("G.989.3 §15 · Ek IV.6–IV.12 · tezgâh ve yöntemler: yorum"), run_time=0.7)
        self.at(self.cue("şifre çözme ve bütünlük", 3.8))
        self.play(Create(tp), FadeIn(pa, shift=UP * 0.1), FadeIn(pl, shift=RIGHT * 0.05), run_time=0.6)
        self.at(self.cue("bir trafik üreteci", 9.0))
        self.play(FadeIn(tg, shift=UP * 0.1), Create(tl), run_time=0.5)
        self.at(self.cue("ayırıcının boş bir portunda", 10.6))
        self.play(Create(d2), FadeIn(spr), FadeIn(atk, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("saldırganımız", 15.3))
        self.play(FadeIn(atl, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("yalnızca yalıtılmış", 16.5))
        self.play(FadeIn(iso, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # g2 — TEST 1: golden vectors IV.6–IV.12 byte for byte before every capture; IV.9 with direction byte 0x02 must change the MIC
        self.beat("g2")
        h = self.next_test(1, "Altın vektörler — her yakalamadan önce", h)
        p = apanel(12.6, 4.55, "Analizör · motor doğrulaması · Ek IV", GOOD).move_to([0, -0.6, 0])
        top = panel_top(p, 0.25)
        data = [("IV.6", "↓ AES-128 CTR", "ffd1ae0c4b46c9c1 … 6ecd5beb"), ("IV.7", "↑ AES-128 CTR", "0d5a4657fd686fa4 … c3a7e4d8"),
                ("IV.8", "anahtar türetme", "SK 795fcf6c… · KEK 6f9c99b8…"), ("IV.9", "↓ PLOAM MIC", "46398756280814e6"),
                ("IV.10", "↑ PLOAM MIC", "feaf8d09208f0d9b"), ("IV.11", "anahtar raporu", "ECB 4018340d… · ad 3cc507bb…"), ("IV.12", "↓ OMCI MIC", "78dca53d")]
        rows = [ivrow(a, b, c) for a, b, c in data]
        place_rows(rows, top - 0.12, (-5.9, -4.6, -1.3, 5.5), 0.42)
        for r in rows:
            r[3].set_opacity(0)
        cd = VGroup(T("IV.9 · Cdir = 0x02 →", 16, WARN, BOLD), HX("229a69aa5b6e5054", 16, WARN, BOLD), T("≠ 46398756280814e6", 16, MUTED, BOLD), T("→ yön hatası hemen görünür", 16, WARN, BOLD))
        cd.arrange(RIGHT, buff=0.18)
        fit(cd, 12.0).move_to([0, top - 0.12 - 7 * 0.42 - 0.12, 0])
        self.play(FadeIn(p), self.set_src("G.989.3 Ek IV.6 … IV.12 · (15-7) · S2·B5"), run_time=0.4)
        for idx, key, d in (((0, 1), "Dördüncü ekin altıncı", 3.7), ((2,), "sekizincisi anahtar türetme", 8.2), ((3, 4), "dokuzuncu ve onuncusu", 10.6),
                            ((5,), "on birincisi anahtar raporu", 13.4), ((6,), "on ikincisi OMCI kodu", 15.7)):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(rows[i][:3], shift=RIGHT * 0.05) for i in idx], run_time=0.35)
        self.at(self.cue("hepsi bayt bayt", 18.3))
        self.play(*[r[3].animate.set_opacity(1) for r in rows], run_time=0.5)
        self.at(self.cue("Dokuzuncu örneği yön baytı", 20.6))
        self.play(FadeIn(cd[0]), Indicate(rows[3][2], color=WARN, scale_factor=1.05), run_time=0.5)
        self.at(self.cue("kod değişmeli", 24.6))
        self.play(FadeIn(cd[1:3], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("yön hatası hemen", 25.8))
        self.play(FadeIn(cd[3], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g3 — TEST 2: counter block at SFC = 1: capture the first encrypted DS and US frames, IFC from the header position, build the ICB
        #      (upper half equal, lower half copy DS / complement US); decrypted payload = what the traffic generator sent
        self.beat("g3")
        h = self.next_test(2, "Sayaç bloğu — SFC = 1", h)
        em = VGroup(emu_icon(1.6, 1.1, "emülatör"), VGroup(T("SFC(49..0)", 17, SFCC8, BOLD), T("= 1", 20, GOLD, BOLD)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.3)
        em.move_to([-3.8, 1.55, 0])
        cap = VGroup(T("yakala:", 16, MUTED, BOLD), tag("ilk şifreli ↓ çerçeve", ACC, 16), tag("ilk şifreli ↑ burst", GOLD, 16)).arrange(RIGHT, buff=0.15).move_to([3.0, 1.75, 0])
        ifc = VGroup(T("IFC = k", 17, IFCC8, BOLD), T("← başlığın ilk 4 baytının bloğu", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).next_to(cap, DOWN, buff=0.2).align_to(cap, LEFT)
        spd = [("SFC = 1", 50, SFCC8), ("k", 14, IFCC8), ("SFC = 1", 50, SFCC8), ("k", 14, IFCC8)]
        spu = [("SFC = 1", 50, SFCC8), ("k", 14, IFCC8), ("¬ 1", 50, NOTC), ("¬ k", 14, NOTC)]
        dsr = fields(spd, 11.4, 0.55, 17, 14, show_w=False).move_to([0.55, 0.05, 0])
        usr = fields(spu, 11.4, 0.55, 17, 14, show_w=False).move_to([0.55, -0.75, 0])
        rl = VGroup(T("↓", 24, TXT, BOLD).next_to(dsr, LEFT, buff=0.25), T("↑", 24, TXT, BOLD).next_to(usr, LEFT, buff=0.25))
        up = brace_lbl(VGroup(usr[0][0], usr[1][0]), "üst yarı · iki yönde aynı", SFCC8, DOWN, 15)
        lo1 = T("↓ alt yarı: kopya", 15, SFCC8, BOLD).next_to(dsr[2], UP, buff=0.08)
        lo2 = brace_lbl(VGroup(usr[2][0], usr[3][0]), "↑ alt yarı: tümleyen", NOTC, DOWN, 15)
        res = VGroup(T("çözülen yük", 18, TXT, BOLD), T("=", 20, GOOD, BOLD), T("trafik üretecinin gönderdiği", 18, TXT, BOLD), ok_x(True, 20)).arrange(RIGHT, buff=0.2).move_to([0, -2.75, 0])
        self.at(self.cue("Emülatörde süper çerçeve", 1.8))
        self.play(FadeIn(em, shift=UP * 0.05), self.set_src("G.989.3 §15.4.3 · Şekil 15-1 · 15-2 · §10.1.1.1.2"), run_time=0.5)
        self.at(self.cue("İlk şifreli aşağı", 5.6))
        self.play(FadeIn(cap, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("blok numarasını başlığın", 10.4))
        self.play(FadeIn(ifc, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("ilk sayaç bloğunu kurun", 14.3))
        self.play(FadeIn(rl[0]), FadeIn(dsr[:2]), FadeIn(rl[1]), FadeIn(usr[:2]), run_time=0.5)
        self.at(self.cue("üst yarı iki yönde", 16.6))
        self.play(FadeIn(up), run_time=0.4)
        self.at(self.cue("alt yarı aşağıda kopya", 18.7))
        self.play(TransformFromCopy(dsr[:2], dsr[2:]), FadeIn(lo1), run_time=0.6)
        self.at(self.cue("yukarıda tümleyen", 20.6))
        self.play(FadeIn(usr[2:], shift=UP * 0.05), FadeIn(lo2), run_time=0.5)
        self.at(self.cue("Çözülen yük", 22.1))
        self.play(FadeIn(res[0]), run_time=0.3)
        self.at(self.cue("trafik üretecinin", 23.1))
        self.play(FadeIn(res[1:], shift=LEFT * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # g4 — TEST 3: timestamp Generate → NewKey → Confirm → ExistingKey; each reply within 750 µs + grant wait; first new-KI DS and US XGEM
        #      frames: DS first, switch on an XGEM frame boundary
        self.beat("g4")
        h = self.next_test(3, "Değişimin zamanlaması", h)
        xs = (-4.9, -1.9, 1.1, 4.1)
        ms = [("Key_Control · Generate", "↓", PLC), ("Key_Report · NewKey", "↑", ONUC), ("Key_Control · Confirm", "↓", PLC), ("Key_Report · ExistingKey", "↑", ONUC)]
        st = VGroup()
        for x, (s, d, c) in zip(xs, ms):
            st.add(VGroup(T(d, 20, c, BOLD), mbox(s, c, 2.55, 0.42, 15, 0.22)).arrange(RIGHT, buff=0.08).move_to([x, 1.55, 0]))
        tl = Line([-6.4, 0.95, 0], [6.4, 0.95, 0], color=MUTED, stroke_width=2)
        tk = VGroup(*[Line([x, 0.85, 0], [x, 1.05, 0], color=MUTED, stroke_width=2) for x in xs])
        rp = VGroup(*[brace_lbl(Line([xs[a], 0.9, 0], [xs[b], 0.9, 0]), "≤ 750 µs + tahsis beklemesi", GOLD, DOWN, 15, 0.02) for a, b in ((0, 1), (2, 3))])
        y1, y2 = -0.85, -1.75
        fw = 0.82

        def frames(y, nsw, xsw):
            g = VGroup()
            x = -5.3
            k = 0
            while x + fw <= 6.5:
                new = x >= xsw - 0.01
                c = GOOD if new else "#60A5FA"
                r = Rectangle(width=fw - 0.06, height=0.42, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.35 if new else 0.15).move_to([x + fw / 2, y, 0])
                g.add(VGroup(r, HX("10" if new else "01", 14, TXT, BOLD).move_to(r)))
                x += fw
                k += 1
            return g
        dsf = frames(y1, 0, -0.38)
        usf = frames(y2, 0, 2.08)
        lb = VGroup(T("↓ XGEM KI", 15, TXT, BOLD).next_to(dsf, LEFT, buff=0.15), T("↑ XGEM KI", 15, TXT, BOLD).next_to(usf, LEFT, buff=0.15))
        sw1 = DashedLine([-0.38, y1 + 0.35, 0], [-0.38, y1 - 0.35, 0], color=GOOD, stroke_width=2.4)
        sw2 = DashedLine([2.08, y2 + 0.35, 0], [2.08, y2 - 0.35, 0], color=GOOD, stroke_width=2.4)
        tg = VGroup(tag("1 · ↓ önce", ACC, 16), tag("2 · ↑ sonra", "#60A5FA", 16), tag("geçiş: XGEM çerçevesi sınırında", GOOD, 16)).arrange(RIGHT, buff=0.3).move_to([0, -2.8, 0])
        self.at(self.cue("Dört mesajı damgalayın", 2.7))
        self.play(Create(tl), FadeIn(tk), self.set_src("G.989.3 §15.5.3 · Şekil 15-3 · §11.1.2 · §15.5.3.1"), run_time=0.5)
        for k, (key, d) in enumerate((("üret isteği", 4.6), ("yeni anahtar raporu", 5.6), ("onay isteği", 7.3), ("mevcut anahtar raporu", 8.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(st[k], shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("yedi yüz elli mikrosaniyelik", 11.0))
        self.play(FadeIn(rp), run_time=0.5)
        self.at(self.cue("Yeni indeksli ilk aşağı", 18.1))
        self.play(FadeIn(lb), LaggedStart(*[FadeIn(f) for f in dsf], lag_ratio=0.05), LaggedStart(*[FadeIn(f) for f in usf], lag_ratio=0.05), run_time=1.0)
        self.at(self.cue("aşağı yön önce geçmelidir", 23.4))
        self.play(Create(sw1), Create(sw2), FadeIn(tg[:2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("geçiş bir XGEM çerçevesi", 25.6))
        self.play(FadeIn(tg[2], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep18_labA")


class E18LabB(LabAct):
    HDR, MANIFEST, PREV_BADGE = H18["L"], M18("lab"), "lab"

    def construct(self):
        # g5 — TEST 4: failed rekey: suppress Key_Report(NewKey) → OLT repeats every 10 ms (TK2), gives up at 100 ms (TK1);
        #      suppress Key_Control(Confirm) → ONU repeats every 20 ms (TK5), drops to no key at 100 ms (TK4); then KI = 00 → clear payload
        self.beat("g5")
        h = step_head(self, 4, "Başarısız yenileme")
        ax1, X = lin_axis(0, 110, -4.4, 6.2, 0.75, [0, 20, 40, 60, 80, 100], size=14)
        ax2, _ = lin_axis(0, 110, -4.4, 6.2, -1.15, [0, 20, 40, 60, 80, 100], size=14)
        u1 = T("ms", 14, MUTED).next_to(ax1, RIGHT, buff=0.1).shift(DOWN * 0.15)
        u2 = T("ms", 14, MUTED).next_to(ax2, RIGHT, buff=0.1).shift(DOWN * 0.15)
        la = VGroup(T("Key_Report(NewKey)", 16, ONUC, BOLD), T("bastırıldı", 16, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.8, 1.15, 0])
        lb = VGroup(T("Key_Control(Confirm)", 16, PLC, BOLD), T("bastırıldı", 16, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.8, -0.75, 0])
        ta = VGroup(*[Rectangle(width=0.14, height=0.42, stroke_width=0, fill_color=PLC, fill_opacity=0.85).move_to([X(t), 1.0, 0]) for t in range(0, 100, 10)])
        tb = VGroup(*[Rectangle(width=0.14, height=0.42, stroke_width=0, fill_color=ONUC, fill_opacity=0.85).move_to([X(t), -0.9, 0]) for t in range(0, 100, 20)])
        tal = T("OLT: Key_Control yinelenir · TK2 = 10 ms", 15, PLC, BOLD).next_to(ta, UP, buff=0.12).align_to(ta, LEFT)
        tbl = T("ONU: Key_Report(NewKey) yinelenir · TK5 = 20 ms", 15, ONUC, BOLD).next_to(tb, UP, buff=0.12).align_to(tb, LEFT)
        ea = VGroup(DashedLine([X(100), 0.6, 0], [X(100), 1.45, 0], color=WARN, stroke_width=2.4), tag("TK1 · 100 ms → KL0", WARN, 15))
        ea[1].next_to(ea[0], UP, buff=0.05)
        eb = VGroup(DashedLine([X(100), -1.3, 0], [X(100), -0.45, 0], color=WARN, stroke_width=2.4), tag("TK4 · 100 ms → KN0", WARN, 15))
        eb[1].next_to(eb[0], UP, buff=0.05)
        xg = strip([(1.0, "KI = 00", KIC, 0.45), (3.2, "yük · şifresiz", CLRC, 0.25)], -2.2, -2.55, 0.5, 15)
        xl = T("ardından trafik:", 17, TXT, BOLD).next_to(xg, LEFT, buff=0.25)
        ol = VGroup(lock(CLRC, 0.24, opened=True), T("yük artık şifresiz", 17, WARN, BOLD)).arrange(RIGHT, buff=0.12).next_to(xg, RIGHT, buff=0.25)
        self.at(self.cue("Yeni anahtar raporunu bastırın", 2.6))
        self.play(FadeIn(la), Create(ax1), FadeIn(u1), self.set_src("G.989.3 §15.5.3.2 · §15.5.3.3 · Şekil 15-4 · 15-5 · §15.5.1"), run_time=0.5)
        self.at(self.cue("OLT isteği on milisaniyede", 5.2))
        self.play(FadeIn(tal), LaggedStart(*[GrowFromEdge(t, DOWN) for t in ta], lag_ratio=0.12), run_time=1.0)
        self.at(self.cue("yüz milisaniyede vazgeçmelidir", 8.7))
        self.play(Create(ea[0]), FadeIn(ea[1], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("Onay isteğini bastırın", 11.4))
        self.play(FadeIn(lb), Create(ax2), FadeIn(u2), run_time=0.5)
        self.at(self.cue("ONU raporu yirmi", 13.3))
        self.play(FadeIn(tbl), LaggedStart(*[GrowFromEdge(t, DOWN) for t in tb], lag_ratio=0.15), run_time=0.9)
        self.at(self.cue("anahtarsız duruma", 17.1))
        self.play(Create(eb[0]), FadeIn(eb[1], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("Ardından trafiğe bakın", 21.0))
        self.play(FadeIn(xl), FadeIn(xg), run_time=0.45)
        self.at(self.cue("indeks sıfırsa", 22.9))
        self.play(FadeIn(ol, shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g6 — TEST 5: key check: Confirm for the active index, compare the returned Key_Name with our own AES-CMAC(KEK, key | π digits);
        #      a wrong key loaded in the emulator → name mismatch → the OLT stops using that index
        self.beat("g6")
        h = self.next_test(5, "Anahtar denetimi", h)
        xo, xn = -5.2, -1.4
        ll = VGroup(lifeline("OLT", xo, 1.7, -1.5, OLTC, 1.2, 0.46, 15), lifeline("ONU", xn, 1.7, -1.5, ONUC, 1.2, 0.46, 15))
        m1 = msg3(xo, xn, 0.85, "Key_Control · Confirm · etkin indeks", PLC, size=15)
        m2 = msg3(xn, xo, -0.15, "Key_Report · ExistingKey · Key_Name", ONUC, size=15)
        xr = -0.4
        nm = VGroup(T("gelen ad", 16, ONUC, BOLD), HX("3cc507bb1731c569ed7b79f8bdc376be", 16, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([xr, 1.4, 0], aligned_edge=LEFT)
        ca = VGroup(T("bizim hesabımız · KEK ile", 16, KEKC, BOLD), HX("AES-CMAC(KEK, anahtar ‖ “3141592653589793”)", 15, KEKC, BOLD),
                    VGroup(HX("3cc507bb1731c569ed7b79f8bdc376be", 16, TXT, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        ca.move_to([xr, 0.0, 0], aligned_edge=LEFT)
        iv = T("Ek IV.11 değerleri", 14, MUTED, BOLD).next_to(ca, DOWN, buff=0.08).align_to(ca, LEFT)
        wr = VGroup(T("emülatöre yanlış anahtar →", 17, TXT, BOLD), T("ad tutmaz", 17, WARN, BOLD), ok_x(False, 18), T("→ OLT o indeksi kullanmayı bırakır", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        fit(wr, 12.6).move_to([0, -2.4, 0])
        self.at(self.cue("Etkin indeks için onay", 2.3))
        self.play(FadeIn(ll), *grow_msg(m1), self.set_src("G.989.3 §15.5.3.1 · Tablo 11-27 · Ek IV.11"), run_time=0.6)
        self.play(*grow_msg(m2), run_time=0.5)
        self.at(self.cue("gelen adı kendi hesabınızla", 5.0))
        self.play(FadeIn(nm, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("anahtar şifreleme anahtarıyla", 8.7))
        self.play(FadeIn(ca[0], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("pi basamaklarının", 11.3))
        self.play(FadeIn(ca[1:], shift=LEFT * 0.05), FadeIn(iv), run_time=0.5)
        self.at(self.cue("yanlış bir anahtar yükleyin", 14.6))
        self.play(FadeIn(wr[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ad tutmamalı", 18.4))
        self.play(FadeIn(wr[1:3], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("OLT o indeksi kullanmayı", 19.5))
        self.play(FadeIn(wr[3], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g7 — TEST 6: MIC error injection: one corrupted byte in a directed DS PLOAM → no ack, ONU MIC error counter +1; ≥ 3 consecutive bad US PLOAMs
        #      → LOPCi; bad US OMCI MICs → LOOCi; wrong direction byte and wrong key as separate cases
        self.beat("g7")
        h = self.next_test(6, "Bütünlük hatası enjeksiyonu", h)
        p = apanel(12.6, 3.9, "Emülatör · enjeksiyon → beklenen", MICC).move_to([0, -0.35, 0])
        top = panel_top(p, 0.25)
        data = [("↓ yönlendirilmiş PLOAM · 1 bayt bozuk", "onay yok", "ONU · PLOAM MIC hataları +1"),
                ("↑ PLOAM · art arda ≥ 3 bozuk", "LOPCi", "PLOAM kanalı kaybı"),
                ("↑ OMCI MIC bozuk", "LOOCi", "OMCC kanalı kaybı"),
                ("yanlış yön baytı (Cdir)", "MIC ✗", "ayrı vaka olarak dene"),
                ("yanlış anahtar (varsayılan ↔ ONU'ya özgü)", "MIC ✗", "ayrı vaka olarak dene")]
        rows = []
        for k, (a, b, c) in enumerate(data):
            r = VGroup(T(a, 17, TXT, BOLD), T("→", 17, MUTED, BOLD), T(b, 17, WARN, BOLD), T(c, 16, MUTED, BOLD))
            rows.append(r)
        place_rows(rows, top - 0.25, (-6.0, -0.9, -0.4, 1.9), 0.6)
        self.play(FadeIn(p), self.set_src("G.989.3 §11.2.5 · §11.1.3 · §15.8.4 · Tablo 14-1 · Tablo 14-2"), run_time=0.4)
        self.at(self.cue("Yönlendirilmiş bir aşağı yön", 3.3))
        self.play(FadeIn(rows[0][0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("onay gelmemeli", 8.6))
        self.play(FadeIn(rows[0][1:3]), run_time=0.3)
        self.at(self.cue("bütünlük hatası sayacı", 9.8))
        self.play(FadeIn(rows[0][3], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Art arda en az üç", 13.4))
        self.play(FadeIn(rows[1][0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("PLOAM kanalı kaybı.", 17.6))
        self.play(FadeIn(rows[1][1:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Yukarı yön OMCI kodlarını", 19.2))
        self.play(FadeIn(rows[2][0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("OMCC kanalı kaybı", 21.9))
        self.play(FadeIn(rows[2][1:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Yanlış yön baytını", 23.4))
        self.play(FadeIn(rows[3], shift=RIGHT * 0.05), FadeIn(rows[4], shift=RIGHT * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g8 — TEST 7: default-key limit: the attacker emulator builds a broadcast Disable_Serial_Number with the default MIC; our expectation: the ONU
        #      obeys (MIC verifies); re-enable it; integrity proven, origin not
        self.beat("g8")
        h = self.next_test(7, "Varsayılan anahtarın sınırı", h)
        at = emu_icon(1.7, 1.15, "saldırgan emülatör").move_to([-5.3, 0.95, 0])
        at[0].set_stroke(ATKC)
        msg_ = VGroup(mtile(0x06, "Disable_Serial_Number · yayın 0x03FF", "dis", 5.0, 0.44, 16),
                      VGroup(T("MIC:", 15, MUTED, BOLD), HX("33adf1f7c67f2f7b", 15, DKC, BOLD), keychip(True, 14, "(0x55) × 16")).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        msg_.move_to([-0.9, 1.05, 0])
        ex = T("örnek MIC: S2·B5'teki hesabımız", 14, MUTED, BOLD).next_to(msg_, DOWN, buff=0.06).align_to(msg_, LEFT)
        a1 = arrow(at[0].get_right(), msg_.get_left() + LEFT * 0.05, ATKC, 2.4, 0.12)
        onu = onu_box("ONU", ONUC, 1.2, 0.55, 17).move_to([4.6, 1.05, 0])
        a2 = arrow(msg_.get_right() + RIGHT * 0.05, onu.get_left(), ATKC, 2.4, 0.12)
        yt = ytag("bizim beklentimiz").move_to([-4.9, -0.75, 0])
        ok = VGroup(T("ONU:", 17, ONUC, BOLD), T("MIC ✓", 17, GOOD, BOLD), T("→ itaat eder", 17, WARN, BOLD), sbox("O7", "acil durdurma", ESC, 1.9, 0.7, 19, 14), laser(False, GOLD, 0.3)).arrange(RIGHT, buff=0.2)
        ok.next_to(yt, RIGHT, buff=0.3)
        en = VGroup(T("sonra:", 16, MUTED, BOLD), tag("OLT · Enable SN → ONU geri döner", GOOD, 16)).arrange(RIGHT, buff=0.15).move_to([0, -1.85, 0])
        cn = VGroup(T("kod", 19, TXT, BOLD), T("bütünlüğü kanıtlar", 19, GOOD, BOLD), T("·", 19, MUTED, BOLD), T("kaynağı kanıtlamaz", 19, WARN, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -2.8, 0])
        self.at(self.cue("Saldırgan emülatörden", 3.3))
        self.play(FadeIn(at, shift=UP * 0.05), FadeIn(onu), self.set_src("G.989.3 Tablo 11-9 · §15.8.1 · Tablo 12-1 (O7) · S2·B5 · yorum"), run_time=0.5)
        self.at(self.cue("varsayılan kodlu bir yayın", 5.1))
        self.play(GrowArrow(a1), FadeIn(msg_), FadeIn(ex), run_time=0.6)
        self.play(GrowArrow(a2), run_time=0.4)
        self.at(self.cue("Bizim beklentimiz", 10.7))
        self.play(FadeIn(yt), run_time=0.3)
        self.at(self.cue("ONU itaat eder", 12.2))
        self.play(FadeIn(ok[:3], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("çünkü kod tutar", 13.5))
        self.play(FadeIn(ok[3:], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("yeniden etkinleştirin", 14.8))
        self.play(FadeIn(en, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("kodun bütünlüğü kanıtladığını", 18.5))
        self.play(FadeIn(cn[:2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("kaynağı kanıtlamadığını", 21.0))
        self.play(FadeIn(cn[2:], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep18_labB")


class E18LabC(LabAct):
    HDR, MANIFEST, PREV_BADGE = H18["L"], M18("lab"), "lab"

    def construct(self):
        # g9 — TEST 8: registration chain: set a Registration_ID; capture SN_ONU, Burst_Profile, Registration; compute PLOAM_IK and verify the directed
        #      Ranging_Time MIC; KEK → decrypt Key_Report, then payloads; repeat with the default Registration_ID
        self.beat("g9")
        h = step_head(self, 8, "Kayıt zinciri")
        b1 = flow_box("Registration_ID gir", "ONU'ya", CNC, 2.6, 0.75, 17)
        b2 = VGroup(T("yakala:", 15, MUTED, BOLD), mbox("↑ Serial_Number_ONU", ONUC, 2.6, 0.38, 15), mbox("↓ Burst_Profile", GOLD, 2.6, 0.38, 15),
                    mbox("↑ Registration", CNC, 2.6, 0.38, 15)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        b3 = VGroup(knode("MSK", None, 1.1, 0.42, 15), knode("SK", None, 1.0, 0.42, 15), knode("PLOAM_IK", None, 1.6, 0.42, 15)).arrange(RIGHT, buff=0.25)
        b3a = VGroup(*[arrow(b3[k].get_right(), b3[k + 1].get_left(), MUTED, 1.8, 0.08) for k in range(2)])
        b4 = VGroup(mbox("↓ Ranging_Time · yönlendirilmiş", SKC, 3.4, 0.42, 15), VGroup(T("MIC", 15, TXT, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.15)
        b1.move_to([-5.2, 1.25, 0])
        b2.move_to([-1.7, 1.25, 0])
        b3g = VGroup(b3, b3a).move_to([2.9, 1.65, 0])
        b4.next_to(b3g, DOWN, buff=0.3)
        a12 = arrow(b1.get_right(), b2.get_left() + LEFT * 0.05, MUTED, 2, 0.1)
        a23 = arrow(b2.get_right() + RIGHT * 0.05, b3g.get_left() + LEFT * 0.05, MUTED, 2, 0.1)
        a34 = arrow(b3[2].get_bottom(), b4[0].get_top() + RIGHT * 0.4, PIKC, 2, 0.1)
        y2 = -1.05
        c1 = VGroup(knode("KEK", None, 1.3, 0.48, 16), T("SK'den", 15, KEKC, BOLD)).arrange(LEFT, buff=0.15)
        c1.shift(np.array([-4.6, y2, 0]) - c1[0].get_center())
        c2 = mbox("Key_Report çöz (AES-ECB⁻¹)", PLC, 3.4, 0.46, 16).move_to([-1.3, y2, 0])
        c3 = knode("veri anahtarı", DEKC, 2.3, 0.48, 16).move_to([1.95, y2, 0])
        c4 = VGroup(mbox("XGEM yüklerini çöz", GOOD, 2.5, 0.46, 16), ok_x(True, 18)).arrange(RIGHT, buff=0.1).move_to([5.0, y2, 0])
        ca = VGroup(arrow(c1[0].get_right(), c2.get_left(), MUTED, 2, 0.1), arrow(c2.get_right(), c3.get_left(), MUTED, 2, 0.1), arrow(c3.get_right(), c4.get_left(), MUTED, 2, 0.1))
        rp = VGroup(T("tekrarla:", 17, TXT, BOLD), tag("Registration_ID = 36 × 0x00", DKC, 16), T("→ kök anahtar herkesçe bilinir", 17, DKC, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.55, 0])
        self.at(self.cue("ONU'ya bir kayıt kimliği girin", 2.2))
        self.play(FadeIn(b1, shift=RIGHT * 0.05), self.set_src("G.989.3 §15.3 · Tablo 11-25 · 11-5 · 11-26 · 11-27 · çıkarım"), run_time=0.5)
        self.at(self.cue("seri numarası mesajını", 4.8))
        self.play(GrowArrow(a12), FadeIn(b2[:2], shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("burst profilini ve kayıt", 6.8))
        self.play(FadeIn(b2[2:], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("PLOAM bütünlük anahtarını", 10.5))
        self.play(GrowArrow(a23), FadeIn(b3[0]), GrowArrow(b3a[0]), FadeIn(b3[1]), GrowArrow(b3a[1]), FadeIn(b3[2]), run_time=0.8)
        self.play(GrowArrow(a34), FadeIn(b4, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Anahtar şifreleme anahtarıyla", 18.8))
        self.play(FadeIn(c1), GrowArrow(ca[0]), FadeIn(c2), run_time=0.7)
        self.at(self.cue("sonra yükleri çözün", 23.1))
        self.play(GrowArrow(ca[1]), FadeIn(c3), GrowArrow(ca[2]), FadeIn(c4), run_time=0.7)
        self.at(self.cue("Testi varsayılan", 24.8))
        self.play(FadeIn(rp, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # g10 — TEST 9: mutual authentication: verify the 13 steps in order: result AVC with the new OMCI_IK, Request_Registration / Registration with the
        #       default key, the next directed PLOAM with the new PLOAM_IK; with 802.1X: ≤ 200 ms from success to the first new-key message
        self.beat("g10")
        h = self.next_test(9, "Karşılıklı doğrulama — Şekil 15-8", h)
        cells = VGroup(*[tile(str(k + 1), PLC if k >= 11 else OMC, 0.72, 0.5, 17, 0.2) for k in range(13)])
        nxt = tile("sonraki ↓ PLOAM", SKC, 2.2, 0.5, 16, 0.2)
        row = VGroup(*cells, nxt).arrange(RIGHT, buff=0.08).move_to([0, 1.55, 0])
        fit(row, 12.8)
        chk9 = VGroup(arrow(cells[8].get_bottom() + DOWN * 0.05, cells[8].get_bottom() + DOWN * 0.45, OMC, 2, 0.09), keychip(False, 15, "AVC · yeni OMCI_IK ✓"))
        chk9[1].next_to(chk9[0], DOWN, buff=0.06).align_to(chk9[0], LEFT).shift(LEFT * 0.4)
        c1213 = VGroup(arrow(VGroup(cells[11], cells[12]).get_bottom() + DOWN * 0.05, VGroup(cells[11], cells[12]).get_bottom() + DOWN * 0.95, PLC, 2, 0.09),
                       keychip(True, 15, "varsayılan anahtar ✓"))
        c1213[1].next_to(c1213[0], DOWN, buff=0.06)
        cn = VGroup(arrow(nxt.get_bottom() + DOWN * 0.05, nxt.get_bottom() + DOWN * 0.45, SKC, 2, 0.09), keychip(False, 15, "yeni PLOAM_IK ✓"))
        cn[1].next_to(cn[0], DOWN, buff=0.06).align_to(nxt, RIGHT)
        c1213[1].shift(LEFT * 0.35)
        ax, X = lin_axis(0, 250, -3.6, 6.0, -1.85, [0, 50, 100, 150, 200, 250], size=14)
        axu = T("ms", 14, MUTED).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.15)
        s0 = tmark(X(0), -1.85, -1.05, "doğrulama başarısı", GOOD, 15, dashed=False)
        win = Rectangle(width=X(200) - X(0), height=0.36, stroke_color=GOLD, stroke_width=1.6, fill_color=GOLD, fill_opacity=0.15).move_to([(X(0) + X(200)) / 2, -1.55, 0])
        f1 = tmark(X(150), -1.85, -1.05, "yeni anahtarlı ilk mesaj", GOOD, 15)
        lim = VGroup(DashedLine([X(200), -2.05, 0], [X(200), -1.1, 0], color=WARN, stroke_width=2.2), T("≤ 200 ms", 16, WARN, BOLD))
        lim[1].next_to(lim[0], RIGHT, buff=0.1).shift(UP * 0.25)
        dl = T("802.1X kullanılıyorsa", 17, TXT, BOLD).move_to([-5.4, -1.55, 0])
        self.at(self.cue("on üç adımını", 2.8))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cells], lag_ratio=0.06), self.set_src("G.989.3 §15.8.2 · Şekil 15-8 · §15.8.3"), run_time=1.0)
        self.at(self.cue("sonucu bildiren mesaj yeni", 6.7))
        self.play(GrowArrow(chk9[0]), FadeIn(chk9[1], shift=UP * 0.05), Indicate(cells[8], color=OMC, scale_factor=1.15), run_time=0.6)
        self.at(self.cue("kayıt isteği ve kayıt varsayılan", 10.4))
        self.play(GrowArrow(c1213[0]), FadeIn(c1213[1], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("sonraki yönlendirilmiş PLOAM", 14.0))
        self.play(FadeIn(nxt, shift=LEFT * 0.05), GrowArrow(cn[0]), FadeIn(cn[1], shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("Sekiz yüz iki nokta bir X kullanılıyorsa", 18.6))
        self.play(FadeIn(dl), Create(ax), FadeIn(axu), FadeIn(s0), run_time=0.6)
        self.at(self.cue("başarıdan yeni anahtarlı", 22.0))
        self.play(GrowFromEdge(win, LEFT), Create(lim[0]), FadeIn(lim[1]), run_time=0.6)
        self.play(FadeIn(f1), run_time=0.4)
        self.end(pad=0.05)

        # g11 — TEST 10: reduced strength: Leff = 64 → first 8 bytes of the decrypted new key 0x55, EMS reports Leff; weak counter: on an emulator that can
        #       preset the SFC, send bidirectional encrypted traffic at the middle and at zero, look for equal keystream blocks (our method)
        self.beat("g11")
        h = self.next_test(10, "Azaltılmış güç ve zayıf sayaç", h)
        lf = VGroup(T("Leff = 64", 20, GOLD, BOLD), T("yapılandır", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.15).move_to([-4.3, 1.75, 0])
        cells = VGroup()
        for i in range(16):
            fx = i < 8
            c = GOLD if fx else GOOD
            r = Rectangle(width=0.36, height=0.42, stroke_color=c, stroke_width=1.4, fill_color=c, fill_opacity=0.5 if fx else 0.12)
            cells.add(VGroup(r, HX("55" if fx else "··", 14, BG if fx else GOOD, BOLD).move_to(r)))
        cells.arrange(RIGHT, buff=0.03).move_to([-3.3, 0.85, 0])
        cl = T("çözülen yeni anahtar:", 15, MUTED, BOLD).next_to(cells, UP, buff=0.1).align_to(cells, LEFT)
        c8 = VGroup(T("ilk 8 bayt 0x55", 16, GOLD, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.1).next_to(cells, DOWN, buff=0.2).align_to(cells, LEFT)
        ems = VGroup(T("yönetim sistemi Leff'i bildirir", 16, TXT, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.1).next_to(c8, DOWN, buff=0.18).align_to(c8, LEFT)
        dv = Line([0.1, 2.0, 0], [0.1, -2.1, 0], color=LINE, stroke_width=1.5)
        em = VGroup(emu_icon(1.5, 1.05, "SFC ön ayarlı emülatör"), VGroup(tag("SFC = 2⁴⁹", WARN, 16), tag("SFC(49..0) = 0", WARN, 16)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.35)
        em.move_to([3.6, 1.25, 0])
        bd = VGroup(T("↕ şifreli trafik", 16, TXT, BOLD), T("→ ↓ ve ↑ anahtar akışı blokları eşit mi?", 16, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(em, DOWN, buff=0.3)
        ks = VGroup(*[Rectangle(width=0.32, height=0.3, stroke_color=c, stroke_width=1.4, fill_color=c, fill_opacity=0.4) for c in ("#60A5FA", "#60A5FA", WARN, "#60A5FA")]).arrange(RIGHT, buff=0.04)
        ku = VGroup(*[Rectangle(width=0.32, height=0.3, stroke_color=c, stroke_width=1.4, fill_color=c, fill_opacity=0.4) for c in (GOLD, WARN, GOLD, GOLD)]).arrange(RIGHT, buff=0.04)
        kv_ = VGroup(VGroup(T("↓", 15, TXT, BOLD), ks).arrange(RIGHT, buff=0.1), VGroup(T("↑", 15, TXT, BOLD), ku).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        kv_.next_to(bd, DOWN, buff=0.2).align_to(bd, LEFT)
        yt = ytag("bu yöntem bizim").next_to(kv_, RIGHT, buff=0.4)
        self.at(self.cue("Etkin uzunluğu altmış dört", 3.3))
        self.play(FadeIn(lf, shift=RIGHT * 0.05), self.set_src("G.989.3 §15.9.2 · §15.4.3 NOT · yöntem: bizim"), run_time=0.45)
        self.at(self.cue("ilk sekiz baytı beş beş", 6.1))
        self.play(FadeIn(cl), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.05), run_time=0.8)
        self.play(FadeIn(c8, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("yönetim sistemi uzunluğu", 10.6))
        self.play(FadeIn(ems, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Sayacı ön ayarlayabilen", 14.1))
        self.play(Create(dv), FadeIn(em[0], shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("aralığın ortasında ve alanın", 17.4))
        self.play(FadeIn(em[1], shift=LEFT * 0.05), run_time=0.4)
        self.play(FadeIn(bd, shift=UP * 0.05), FadeIn(kv_), run_time=0.5)
        self.at(self.cue("bu yöntem bizimdir", 26.6))
        self.play(FadeIn(yt, shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g12 — lab note
        self.note11("g12", [("1", "Aktivasyon kayıtlarını sır gibi saklayın",
                             "Aktivasyonu kaydeden bir analizör kayıt tabanlı anahtarları türetebilir.", "aktivasyonu kaydeden"),
                            ("2", "Anahtar indeksi · SFC · bütünlük sayaçları: aynı satırda",
                             "Bir şifre sorununu çoğu zaman üçü birlikte açıklar.", "anahtar indeksini")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep18_labC")


POINTS = [("Dört tehdit · kayıt tabanlı doğrulama zorunlu ama tek yönlü,\nbaşarısızlığı O5'i engellemez · Ek C / D'nin gövdesi G.987.3'te", "§15.1 · §15.2"),
          ("Tek kök, tek ilkel: MSK → SK → OMCI_IK · PLOAM_IK · KEK\nAES-CMAC ile · zincirin her girdisi hattan açık geçer", "§15.3"),
          ("Tek alıcılı anahtarı ONU üretir · iki makine, beş zamanlayıcı\n↓ önce geçer · başarısız yenileme → şifresiz trafik", "§15.5"),
          ("↑ sayaç bloğunun alt yarısı tümleyen · zayıf çerçeveler:\naralığın ortası ve (bizim hesabımız) SFC(49..0) = 0", "§15.4.3"),
          ("Varsayılan anahtarlı kod kaynağı kanıtlamaz · kullanıcı\nverisinde MIC yok · yük dışındaki her şey açık", "§15.8 · §15.4")]


class E18End(Act18):
    HDR, MANIFEST, FIRST = H18["E"], M18("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.0))
        self.to_header_badge(tc, "ozet", 0.5)
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.4)
            ch = tag(c, GOLD, 16)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.75, -2.4, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.7, y, 0])
        for k, (key, d) in enumerate((("standart dört tehdit", 1.3), ("bütün anahtarlar AES-CMAC", 15.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((2, 3, 4), (("tek alıcılı anahtarı ONU", 0.1), ("yukarı yön sayaç bloğunun", 11.4), ("varsayılan anahtarlı kodlar", 21.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.7, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Tek alıcılı anahtar iki yönü\nşifreler: aynı çerçevedeki ↓ ve ↑\nyükün aynı anahtar akışını\nkullanmasını ne engeller,\nnot hangi istisnayı anar?", CH[0]),
            ("Kayıt kimliği varsayılan\nkalmış bir ONU'nun veri\nanahtarına hangi mesajlardan\nulaşılır?", CH[1]),
            ("Onay beklemedeki OLT'ye\nmevcut anahtar raporu\ngelmezse ne olur, ne zaman,\nve Amd.1 burada neyi\ndüzeltti?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.1), ("İkinci soru", 16.0), ("Üçüncü soru", 25.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 37.1))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: Enerji ve Sağlık (power management states, performance counters, OLT and ONU defects; the channel-loss defects named here)
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e9 = SERIES["season2"]["episodes"][8]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e9['n']} · {e9['title']}", 50, TXT, BOLD), T(e9["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        fit(nxt[1], 12.6)
        tg_ = VGroup(*[tag(s, GOOD, 16) for s in ("güç yönetimi durumları", "başarım sayaçları", "OLT ve ONU kusurları")]).arrange(RIGHT, buff=0.2).move_to([0, -0.85, 0])
        df = VGroup(tag("LOPCi · PLOAM kanalı kaybı", WARN, 16), tag("LOOCi · OMCC kanalı kaybı", WARN, 16)).arrange(RIGHT, buff=0.3)
        q = T("→ orada açılacak", 18, GOLD, BOLD)
        dg = VGroup(df, q).arrange(RIGHT, buff=0.4).move_to([0, -2.0, 0])
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("Güç yönetimi durumları", 2.8))
        self.play(FadeIn(nxt[2]), FadeIn(tg_[0], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("başarım sayaçları", 4.7))
        self.play(FadeIn(tg_[1], shift=UP * 0.06), run_time=0.35)
        self.at(self.cue("OLT ve ONU kusurları", 6.2))
        self.play(FadeIn(tg_[2], shift=UP * 0.06), run_time=0.35)
        self.at(self.cue("kanal kaybı kusurlarını", 8.0))
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.05) for d in df], lag_ratio=0.2), FadeIn(q, shift=LEFT * 0.05), run_time=0.7)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(tg_, dg)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP18['n']} · {EP18['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep18_end")
