"""S2·B7 · Perde 3 (ayar süresi ve kilitleme — G.989.3 Ek F, §17.4, Tablo 14-1/14-2; G.989.2 §9.3.7 Tablo 9-2, §11.1.5.2.4,
Ek VIII) and Perde 4 (bağlama ve karışık sınıflar — Ek H, Ek X, Tablo 11-18 oktet 32; G.989.2 Tablo 6-1, Tablo 11-2)."""
from ep17_common import *


def mini_seq(title, color, arrows, w=3.9, h=2.05):
    """Small card with three lifelines (H · K · ONU) and unlabelled coloured arrows: arrows = [(from, to, colour, dashed)] with
    lane indices 0 = hedef, 1 = kaynak, 2 = ONU, or (0, 1, colour, 'ictp')."""
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    t = T(title, 16, color, BOLD).move_to(r.get_top() + DOWN * 0.25)
    xs = [r.get_left()[0] + w * f for f in (0.22, 0.5, 0.78)]
    heads = VGroup(*[T(s, 14, c, BOLD).move_to([x, r.get_top()[1] - 0.55, 0]) for s, c, x in zip(("H", "K", "ONU"), (TGTC, SRCC, ONUC), xs)])
    y0, y1 = r.get_top()[1] - 0.75, r.get_bottom()[1] + 0.12
    lines = VGroup(*[DashedLine([x, y0, 0], [x, y1, 0], color=MUTED, stroke_width=1.4, dash_length=0.07) for x in xs])
    ar = VGroup()
    n = len(arrows)
    for k, (a, b, c, d) in enumerate(arrows):
        y = y0 - 0.18 - (y0 - y1 - 0.3) * k / max(n - 1, 1)
        if d == "ictp":
            ar.add(RoundedRectangle(corner_radius=0.04, width=abs(xs[b] - xs[a]), height=0.08, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([(xs[a] + xs[b]) / 2, y, 0]))
        elif d:
            ar.add(DashedLine([xs[a], y, 0], [xs[b], y, 0], color=c, stroke_width=2, dash_length=0.06).add_tip(tip_length=0.1, tip_width=0.1))
        else:
            ar.add(Arrow([xs[a], y, 0], [xs[b], y, 0], buff=0.02, color=c, stroke_width=2.4, tip_length=0.12, max_tip_length_to_length_ratio=0.3))
    return VGroup(r, t, heads, lines, ar)


# ================================ PERDE 3 ======================================
class E17P3A(Act17):
    HDR, MANIFEST, FIRST = H17[3], M17("p3"), True

    def construct(self):
        # d1 — Annex F (normative): one timing chart for the ONU (§12) and OLT CT (§17) machines; timers against deadlock; three sequences
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Ayar süresi ve kilitleme")
        self.at(self.cue("F eki normatiftir", 2.9))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Ek F — ayar dizileri")
        nrm = tag("normatif", GOLD, 16).next_to(h, RIGHT, buff=0.3)
        m1 = sbox("ONU makinesi", "§12 · Tablo 12-4", ONUC, 2.9, 0.85, 19, 15).move_to([-4.6, 1.7, 0])
        m2 = sbox("OLT CT makinesi", "§17 · Tablo 17-9", OLTC, 2.9, 0.85, 19, 15).move_to([-4.6, 0.55, 0])
        one = sbox("tek zaman çizelgesi", "Şekil F.1 … F.3", GOLD, 3.2, 0.85, 19, 15).move_to([0.2, 1.12, 0])
        mg = VGroup(arrow(m1.get_right(), one.get_left() + UP * 0.15, MUTED, 2.2, 0.12), arrow(m2.get_right(), one.get_left() + DOWN * 0.15, MUTED, 2.2, 0.12))
        tms = VGroup(*[tag(s, TMRC, 15) for s in ("TO4", "TO5", "Ttarget", "Tsource")]).arrange(RIGHT, buff=0.12)
        tml = VGroup(tms, T("→ çıkmaz yok", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.2).move_to([0.6, 0.15, 0])
        cards = VGroup(mini_seq("F.1.1 · normal devir", TGTC, [(1, 2, GOLD, 0), (2, 1, ACKC, 0), (2, 0, CMPC, 0), (0, 2, TGTC, 0), (0, 1, ICTC, "ictp")]),
                       mini_seq("F.1.2 · geri dönüş", RBC, [(1, 2, GOLD, 0), (2, 1, ACKC, 0), (2, 1, RBC, 0), (1, 2, SRCC, 0), (0, 1, ICTC, "ictp")]),
                       mini_seq("F.1.3 · olumsuz cevap", NACKC, [(1, 2, GOLD, 0), (2, 1, NACKC, 0), (0, 1, ICTC, "ictp")])).arrange(RIGHT, buff=0.3).move_to([0, -1.75, 0])
        self.play(self.set_src("G.989.3 Ek F · F.1.1 … F.1.3 · Şekil F.1 … F.3"), FadeIn(nrm, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ONU'nun ve OLT", 5.6))
        self.play(FadeIn(m1, shift=RIGHT * 0.05), FadeIn(m2, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("tek bir zaman çizelgesinde", 10.0))
        self.play(GrowArrow(mg[0]), GrowArrow(mg[1]), FadeIn(one, scale=0.9), run_time=0.6)
        self.at(self.cue("çıkmaza düşmemek", 13.6))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in tms], lag_ratio=0.15), run_time=0.6)
        self.play(FadeIn(tml[1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Üç dizi çizer", 19.6))
        self.at(self.cue("normal devir", 20.8))
        self.play(FadeIn(cards[0], shift=UP * 0.08), run_time=0.45)
        self.at(self.cue("geri dönüş ve", 21.9))
        self.play(FadeIn(cards[1], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("olumsuz cevap", 23.0))
        self.play(FadeIn(cards[2], shift=UP * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # d2 — F.2 definition: TC-layer tuning time = preparation + PMD tuning + re-sync; from Scheduled SFC to correct DS sync; no numbers
        self.beat("d2")
        h = self.reset("F.2 — TC katmanı ayar süresi", rt=0.5)
        x0, y = -5.4, 0.85
        parts = stack_bar([(3.0, "hazırlık", PREPC), (4.0, "PMD ayarı", PMDTC), (3.6, "yeniden senkron", RSYC)], x0, y, 0.7, 19, 1.0)
        sfc = tmark(x0, y - 0.55, y + 0.6, "planlı SFC", GOLD, 16)
        snc = tmark(x0 + 10.6, y - 0.55, y + 0.6, "↓ senkron doğru kuruldu", GOOD, 16)
        ds = [VGroup(T("planlı çerçeve → PMD ayarının", 15, TXT, BOLD), T("gerçek başlangıcı · parametre", 15, TXT, BOLD), T("kurma işleme süresi", 15, TXT, BOLD)),
              VGroup(T("G.989.2 §9.3.7'de", 15, TXT, BOLD), T("tanımlı PMD süresi", 15, TXT, BOLD)),
              VGroup(T("ayar bitti → ↓ çerçeveye", 15, TXT, BOLD), T("senkron · en uzun süre", 15, TXT, BOLD))]
        for d, p in zip(ds, parts):
            d.arrange(DOWN, buff=0.06).next_to(p, DOWN, buff=0.3)
        tot = brace_lbl(parts, "TC katmanı ayar süresi · planlı SFC'den senkrona en uzun süre", GOLD, UP, 17)
        tot.shift(UP * 0.55)
        nv = VGroup(*[tag("sayı yok", WARN, 15).next_to(d, DOWN, buff=0.25) for d in ds])
        nvl = VGroup(T("F eki:", 18, TXT, BOLD), T("üç parçanın hiçbirine sayı vermez", 18, WARN, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.85, 0])
        self.play(self.set_src("G.989.3 Ek F.2 · G.989.2 §9.3.7"), FadeIn(sfc), run_time=0.4)
        self.at(self.cue("Hazırlık:", 3.5))
        self.play(GrowFromEdge(parts[0], LEFT), run_time=0.5)
        self.at(self.cue("planlı çerçeveden PMD", 4.2))
        self.play(FadeIn(ds[0][:2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("parametreleri kurmak", 9.3))
        self.play(FadeIn(ds[0][2], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Ayar:", 13.4))
        self.play(GrowFromEdge(parts[1], LEFT), FadeIn(ds[1], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Yeniden senkron:", 16.4))
        self.play(GrowFromEdge(parts[2], LEFT), run_time=0.5)
        self.at(self.cue("ayar bittikten sonra", 17.7))
        self.play(FadeIn(ds[2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Toplam,", 24.2))
        self.play(FadeIn(snc), FadeIn(tot), run_time=0.6)
        self.at(self.cue("hiçbirine sayı vermez", 30.5))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.05) for n in nv], lag_ratio=0.15), FadeIn(nvl), run_time=0.6)
        self.end(pad=0.05)
        self.parts = parts

        # d3 — PMD bridge S1·B7: only the middle part has numbers — G.989.2 Table 9-2 classes; mechanism out of scope, but the optical
        #      tables must hold throughout tuning to avoid rogue behaviour (§9.3.7)
        self.beat("d3")
        h, chp = self.pmd_reset("PMD Köprüsü — ayar sınıfları", s1chip(7))
        ax, X = log_axis(1, 2e6, -5.3, 6.2, -1.15, [(1, "1 µs"), (10, "10 µs"), (100, "100 µs"), (1e3, "1 ms"), (1e4, "10 ms"), (1e5, "100 ms"), (1e6, "1 s")], 15)
        cls = [("Sınıf 1", 1, 10, "< 10 µs", CLC["1"], 1.15), ("Sınıf 2 · 2R1 · 2R2", 10, 25e3, "10 µs … 25 ms", CLC["2"], 0.45), ("Sınıf 3", 25e3, 1e6, "25 ms … 1 s", CLC["3"], -0.25)]
        bars = VGroup()
        for name, a, b, txt, c, yy in cls:
            r = Rectangle(width=X(b) - X(a), height=0.42, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.35).move_to([(X(a) + X(b)) / 2, yy, 0])
            nm = T(name, 16, c, BOLD).move_to([-6.45, yy, 0], aligned_edge=LEFT)
            v = T(txt, 16, TXT, BOLD)
            if v.width < r.width - 0.2:
                v.move_to(r)
            else:
                v.next_to(r, RIGHT, buff=0.12)
            bars.add(VGroup(r, nm, v))
        rs = T("2R1: ≤ 100 GHz uzağa · 2R2: ≤ 200 GHz uzağa", 14, CLC["2"], BOLD).next_to(bars[1][0], DOWN, buff=0.04).align_to(bars[1][0], RIGHT)
        mid = VGroup(T("sayısı olan tek parça:", 17, TXT, BOLD), tag("PMD ayarı", PMDTC, 16), T("G.989.2 Tablo 9-2", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, 1.9, 0])
        q = self.quote("G.989.2 §9.3.7", "\"… must be met throughout the tuning process to avoid any rogue behaviour\"",
                       "Mekanizma kapsam dışı · ama optik tabloların bütün değerleri ayar boyunca sağlanmalı", 12.0)
        q.move_to([0, -2.7, 0])
        self.play(self.set_src("S1·B7 · G.989.2 §9.3.7 · Tablo 9-2"), run_time=0.3)
        self.at(self.cue("Sayısı olan tek parça", 1.0))
        self.play(FadeIn(mid, shift=DOWN * 0.05), run_time=0.5)
        self.at(self.cue("yedinci bölümündeki sınıflar", 4.5))
        self.play(Create(ax), run_time=0.6)
        for k, (key, d) in enumerate((("birinci sınıf on", 7.7), ("ikinci sınıf on", 11.0), ("üçüncü sınıf yirmi", 15.5))):
            self.at(self.cue(key, d))
            self.play(GrowFromEdge(bars[k][0], LEFT), FadeIn(bars[k][1:]), *([FadeIn(rs)] if k == 1 else []), run_time=0.6)
        self.at(self.cue("mekanizmayı kapsam dışı", 19.6))
        self.play(FadeIn(q[0]), run_time=0.4)
        self.at(self.cue("optik tabloların", 24.6))
        self.play(FadeIn(q[1], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("ayar süreci boyunca", 29.9))
        self.play(FadeIn(q[2], shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # d4 + d5 — our arithmetic with its assumptions: prep 0; re-sync 125–250 µs (2nd verified PSBd → Sync); grant every frame;
        #           OLT 6 frames → worst ONU outage ≈ 1.3 ms / 26 ms / 1 s; TC layer sets the time for a fast laser (≥ 12.5×);
        #           buffer for 1 Gbit/s ≈ 0.16 / 3.3 / 125 MB
        self.beat("d4")
        h = self.reset("Bizim hesabımız — bir devrin kesintisi", "std", 0.5)
        hs = interp("hesap · varsayımlarla", GOLD, 15).next_to(h, RIGHT, buff=0.3)
        asm = VGroup(VGroup(tag("hazırlık = 0", PREPC, 16)),
                     VGroup(tag("yeniden senkron", RSYC, 16), T("125–250 µs", 17, RSYC, BOLD)).arrange(RIGHT, buff=0.15),
                     VGroup(tag("hedef her çerçevede tahsis", TGTC, 16)),
                     VGroup(tag("OLT cevabı 6 çerçeve", OLTC, 16))).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-6.4, 1.05, 0], aligned_edge=LEFT)
        ss = VGroup(*[tile(s, STATE, w, 0.45, 15, 0.2) for s, w in (("Av", 0.8), ("Ön senkron", 1.6), ("Senkron", 1.3))]).arrange(RIGHT, buff=1.05).move_to([3.4, 1.55, 0])
        sa = VGroup(*[arrow(ss[k].get_right(), ss[k + 1].get_left(), GOOD, 2, 0.1) for k in range(2)])
        sl = VGroup(*[T(s, 14, GOOD, BOLD).next_to(sa[k], UP, buff=0.05) for k, s in enumerate(("1. PSBd ✓", "2. PSBd ✓"))])
        ssl = VGroup(T("S2·B2 makinesi:", 15, MUTED, BOLD), T("1–2 çerçeve = 125–250 µs", 16, RSYC, BOLD)).arrange(RIGHT, buff=0.15).next_to(ss, DOWN, buff=0.15)
        ax, X = log_axis(100, 3e6, -3.2, 5.0, -2.75, [(100, "100 µs"), (1e3, "1 ms"), (1e4, "10 ms"), (1e5, "100 ms"), (1e6, "1 s")], 15)
        res = [("Sınıf 1", 1.26e3, "≈ 1,3 ms", "0,16 MB", CLC["1"], -0.75), ("Sınıf 2", 26.3e3, "≈ 26 ms", "3,3 MB", CLC["2"], -1.4), ("Sınıf 3", 1.001e6, "≈ 1 s", "125 MB", CLC["3"], -2.05)]
        rb = VGroup()
        for name, v, s, buf, c, yy in res:
            r = Rectangle(width=X(v) - X(100), height=0.42, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.4).move_to([(X(100) + X(v)) / 2, yy, 0])
            nm = T(name, 16, c, BOLD).move_to([-6.4, yy, 0], aligned_edge=LEFT)
            lab = T(s, 17, c, BOLD).next_to(r, RIGHT, buff=0.12)
            bb = T(buf, 17, TXT, BOLD).move_to([6.35, yy, 0], aligned_edge=RIGHT)
            rb.add(VGroup(r, nm, lab, bb))
        rbl = T("en kötü ONU kesintisi", 15, MUTED, BOLD).move_to([-6.4, -0.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(hs, shift=LEFT * 0.05), self.set_src("G.989.3 Ek F.2 · §10 (S2·B2 senkron makinesi) · G.989.2 Tablo 9-2 · hesap"), run_time=0.4)
        self.at(self.cue("Hazırlık sıfır olsun", 2.7))
        self.play(FadeIn(asm[0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Yeniden senkron ikinci", 4.5))
        self.play(FadeIn(asm[1][0], shift=RIGHT * 0.05), FadeIn(ss[0]), run_time=0.4)
        self.at(self.cue("ilk doğrulanan PSBd", 8.6))
        self.play(GrowArrow(sa[0]), FadeIn(sl[0]), FadeIn(ss[1]), run_time=0.5)
        self.at(self.cue("ikincisi senkrona", 11.3))
        self.play(GrowArrow(sa[1]), FadeIn(sl[1]), FadeIn(ss[2]), run_time=0.5)
        self.at(self.cue("yüz yirmi beş ile", 13.5))
        self.play(FadeIn(ssl), FadeIn(asm[1][1]), run_time=0.5)
        self.at(self.cue("Hedef her çerçevede", 17.5))
        self.play(FadeIn(asm[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("OLT cevabını altı", 20.4))
        self.play(FadeIn(asm[3], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("en kötü kesintisi", 24.5))
        self.play(Create(ax), FadeIn(rbl), run_time=0.5)
        for k, (key, d) in enumerate((("bir virgül üç", 26.0), ("ikinci sınıfta yirmi altı", 30.0), ("üçüncü sınıfta bir saniyedir", 33.1))):
            self.at(self.cue(key, d))
            self.play(GrowFromEdge(rb[k][0], LEFT), FadeIn(rb[k][1:3]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("d5")
        cmp_ = VGroup(T("Sınıf 1:", 17, CLC["1"], BOLD), T("PMD < 10 µs", 17, PMDTC, BOLD), T("·", 17, MUTED), T("yeniden senkron ≥ 125 µs", 17, RSYC, BOLD),
                      T("→ en az 12,5 ×", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([3.0, 0.3, 0])
        fit(cmp_, 7.0)
        concl = VGroup(T("hızlı lazerde devrin süresini", 18, TXT, BOLD), tag("TC katmanı belirler", GOLD, 17)).arrange(RIGHT, buff=0.15)
        concl.move_to(cmp_).shift(UP * 0.0)
        bh = VGroup(T("tampon @ 1 Gbit/s", 15, MUTED, BOLD), interp("hesap", GOLD, 14)).arrange(RIGHT, buff=0.12).move_to([5.5, -0.3, 0])
        self.at(self.cue("hızlı bir lazerde", 0.5))
        self.play(FadeOut(VGroup(ss, sa, sl, ssl)), FadeIn(concl.move_to([3.0, 1.55, 0]), shift=DOWN * 0.05), run_time=0.6)
        self.at(self.cue("Birinci sınıfta yeniden", 5.0))
        self.play(FadeIn(cmp_[:4], shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("on iki buçuk katıdır", 8.5))
        self.play(FadeIn(cmp_[4], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("bir gigabitlik servis", 12.1))
        self.play(FadeIn(bh), run_time=0.4)
        for k, (key, d) in enumerate((("sıfır virgül on altı", 15.0), ("üç virgül üç", 18.9), ("yüz yirmi beş megabayttır", 21.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rb[k][3], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p3A")


class E17P3B(Act17):
    HDR, MANIFEST, FIRST = H17[3], M17("p3"), True
    PREV_BADGE = "std"

    def construct(self):
        # d6 — the profile trap: SFC match discards burst profiles; no profile → no answer; first Complete_u waits for the target's broadcast
        #      Burst_Profile, full set every 1–5 s → even a Class 1 ONU needs 1–5 s (our inference)
        self.beat("d6")
        h = self.show_heading("Asıl tuzak: profiller")
        ax, X = lin_axis(0, 6, -5.6, 6.0, -1.9, [0, 1, 2, 3, 4, 5, 6], size=15, fmt=lambda v: f"{v:g} s")
        sfc = tmark(X(0), -1.9, 0.9, "planlı SFC", GOLD, 15)
        dsc = VGroup(tag("Discard I", WARN, 15), T("burst profilleri atılır", 15, WARN, BOLD)).arrange(RIGHT, buff=0.1).move_to([X(0) + 0.15, 0.45, 0], aligned_edge=LEFT)
        rdy = VGroup(laser(True, CLC["1"], 0.26), T("Sınıf 1 · µs'de hazır", 15, CLC["1"], BOLD)).arrange(RIGHT, buff=0.12).move_to([X(0) + 0.15, -0.15, 0], aligned_edge=LEFT)
        gr = VGroup(*[VGroup(Line([X(t), -1.75, 0], [X(t), -1.35, 0], color=TGTC, stroke_width=2.4), xmark(Square(0.14).move_to([X(t), -1.15, 0]), WARN, 2.2, 0))
                      for t in np.arange(0.3, 2.85, 0.35)])
        grl = T("hedefin tahsisleri · profil bilinmiyor → cevap yok", 15, TGTC, BOLD).move_to([X(1.45), -2.75, 0])
        win = Rectangle(width=X(5) - X(1), height=2.9, stroke_width=0, fill_color=GOLD, fill_opacity=0.07).move_to([(X(1) + X(5)) / 2, -0.45, 0])
        wl = T("tam küme her 1–5 s · TminProfile", 15, GOLD, BOLD).next_to(win, UP, buff=0.06).shift(RIGHT * 0.6)
        bp = VGroup(mbox("Burst_Profile · hedef", GOLD, None, 0.4, 15, 0.35)).move_to([X(3.0) + 0.9, 0.45, 0])
        bpa = arrow([X(3.0), 0.2, 0], [X(3.0), -1.35, 0], GOLD, 2.2, 0.12)
        cu = VGroup(Line([X(3.1), -1.75, 0], [X(3.1), -1.35, 0], color=CMPC, stroke_width=3), T("Complete_u ✓", 15, CMPC, BOLD).move_to([X(3.1) + 0.75, -1.15, 0]))
        inf = VGroup(interp("çıkarım", GOLD, 14), T("Sınıf 1 ONU bile: devir 1–5 s", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([2.6, 1.85, 0])
        self.play(self.set_src("G.989.3 Tablo 12-4 (Discard I) · Tablo 12-3 · §11.3.3.1 · §17.1 · çıkarım"), Create(ax), run_time=0.5)
        self.at(self.cue("Sayaç eşleşince ONU", 2.5))
        self.play(FadeIn(sfc), FadeIn(dsc, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("profilini bilmediği", 7.1))
        self.play(FadeIn(rdy, shift=RIGHT * 0.05), LaggedStart(*[FadeIn(g) for g in gr], lag_ratio=0.12), FadeIn(grl), run_time=1.2)
        self.at(self.cue("Hedefin profili önceden", 11.0))
        self.play(FadeIn(win), run_time=0.4)
        self.at(self.cue("hedefin yayın burst profilini", 15.5))
        self.play(FadeIn(bp, shift=DOWN * 0.05), GrowArrow(bpa), run_time=0.5)
        self.play(FadeIn(cu), run_time=0.4)
        self.at(self.cue("tam küme bir ile beş", 18.9))
        self.play(FadeIn(wl), run_time=0.4)
        self.at(self.cue("birinci sınıf bir ONU bile", 25.5))
        self.play(FadeIn(inf, shift=DOWN * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # d7 — the door: O8 text mentions advance burst profile distribution 'if the system supports it', no method; our reading:
        #      cross-channel Burst_Profile (C = 1) carries the target's profile on the source channel; size TO4/TO5/Ttarget/Tsource to this wait
        self.beat("d7")
        h = self.reset("Kapı: profilleri önceden dağıtmak", rt=0.5)
        o8 = VGroup(T("Tablo 12-1 · O8:", 17, GOLD, BOLD), T("\"… as long as the system supports the advance burst profile distribution\"", 16, MUTED, slant=ITALIC)).arrange(RIGHT, buff=0.2)
        fit(o8, 12.6).move_to([0, 1.85, 0])
        nm_ = VGroup(T("yöntem:", 17, TXT, BOLD), T("tanımlanmamış", 17, WARN, BOLD)).arrange(RIGHT, buff=0.15).next_to(o8, DOWN, buff=0.15).align_to(o8, LEFT)
        srcc = ct_box("Kaynak CT · λ1", SRCC, 2.2, 0.55, 16).move_to([-4.8, 0.0, 0])
        onu = onu_box("ONU", ONUC, 1.2, 0.6, 17).move_to([-0.6, 0.0, 0])
        lk = Line(srcc.get_right(), onu.get_left(), color=SRCC, stroke_width=2.4)
        cb = mbox("Burst_Profile · C = 1", GOLD, None, 0.42, 15, 0.35).next_to(lk, UP, buff=0.12)
        cbl = VGroup(T("oktet 6: C = 1", 14, GOLD, BOLD), T("oktet 34–37: hedef ↓ PON-ID", 14, GOLD, BOLD)).arrange(DOWN, buff=0.04).next_to(lk, DOWN, buff=0.12)
        st = VGroup(T("\"sanki orada gönderilmiş gibi\"", 16, TXT, BOLD), VGroup(T("hedefin profili", 16, TGTC, BOLD), ok_x(True, 16)).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        st.next_to(onu, RIGHT, buff=0.3)
        tgt = ct_box("Hedef CT · λ3", TGTC, 2.2, 0.55, 16).move_to([5.2, -1.25, 0])
        hop_ = CurvedArrow(onu.get_bottom() + DOWN * 0.05, tgt.get_left() + LEFT * 0.05, angle=0.5, color=GOLD, stroke_width=2.2, tip_length=0.12)
        fast = T("ilk tahsise hemen cevap", 16, CMPC, BOLD).next_to(hop_, DOWN, buff=0.05).shift(LEFT * 0.4)
        yr = interp("bizim yorumumuz", GOLD, 15).move_to([-4.8, 0.85, 0])
        dim = VGroup(VGroup(*[tag(s, TMRC, 15) for s in ("TO4", "TO5", "Ttarget", "Tsource")]).arrange(RIGHT, buff=0.12),
                     T("→ lazerin hızına göre değil,", 17, MUTED, BOLD), T("bu beklemeye göre boyutlandır", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.18)
        fit(dim, 12.6).move_to([0, -2.85, 0])
        self.play(self.set_src("G.989.3 Tablo 12-1 (O8) · Burst_Profile (Tablo 11-4) oktet 6, 34–37 · yorum"), run_time=0.3)
        self.at(self.cue("O8'in tanımı", 2.2))
        self.play(FadeIn(o8, shift=DOWN * 0.05), run_time=0.6)
        self.at(self.cue("ama yöntemi tanımlamaz", 9.6))
        self.play(FadeIn(nm_, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Bizim yorumumuz", 11.5))
        self.play(FadeIn(yr), FadeIn(srcc), FadeIn(onu), Create(lk), run_time=0.5)
        self.at(self.cue("kanal ötesi burst", 13.3))
        self.play(FadeIn(cb, shift=RIGHT * 0.1), FadeIn(cbl), run_time=0.5)
        self.at(self.cue("hedefin profilini kaynak", 16.3))
        self.play(FadeIn(st[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("sanki orada", 19.1))
        self.play(FadeIn(st[0], shift=LEFT * 0.05), FadeIn(tgt), Create(hop_), FadeIn(fast), run_time=0.7)
        self.at(self.cue("Ve TO4", 22.1))
        self.play(FadeIn(dim[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("lazerin hızına göre", 23.6))
        self.play(FadeIn(dim[1]), run_time=0.3)
        self.at(self.cue("bu beklemeye göre", 27.5))
        self.play(FadeIn(dim[2], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # d8 — §17.4 locking: closed loop for fine-tuning ONUs; small Tx adjustments, received quality monitored; Adjust_Tx_Wavelength:
        #      direction bit + size in 0.1 GHz; our reading: the OLT-interactive one of G.989.2's two control types
        self.beat("d8")
        h = self.reset("§17.4 — kanal kilitleme", rt=0.5)
        olt = sbox("OLT CT", "alıcı · kalite ölçümü", OLTC, 2.4, 0.85, 19, 14).move_to([-4.4, 0.6, 0])
        onu = VGroup(onu_box("ONU", ONUC, 1.4, 0.7, 18), laser(True, TGTC, 0.3)).arrange(RIGHT, buff=0.12).move_to([1.2, 0.6, 0])
        dn = msg3(olt.get_right()[0] + 0.05, onu.get_left()[0] - 0.05, 1.0, "küçük verici ayarı isteği", GOLD, size=15)
        up = msg3(onu.get_left()[0] - 0.05, olt.get_right()[0] + 0.05, 0.2, "alınan sinyal → kalite izlenir", TGTC, size=15, above=False)
        loop = Arc(radius=0.32, start_angle=PI * 0.3, angle=TAU * 0.8, color=GOLD, stroke_width=3).add_tip(tip_length=0.13, tip_width=0.13).move_to([-2.2, -0.7, 0])
        ll = T("kapalı döngü · dithering", 15, GOLD, BOLD).next_to(loop, RIGHT, buff=0.2)
        aw = VGroup(T("Adjust_Tx_Wavelength · 0x14", 17, GOLD, BOLD),
                    VGroup(bitbox([("D", GOLD)], 0.42, 0.42, 16), T("yön biti · 0 düşük / 1 yüksek frekans", 15, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                    VGroup(Rectangle(width=1.4, height=0.42, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.18), T("boyut · 0,1 GHz birim", 15, TXT, BOLD)).arrange(RIGHT, buff=0.15))
        aw.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-3.3, -2.05, 0])
        two = VGroup(T("G.989.2 §9.3.7 · iki denetim türü", 16, MUTED, BOLD),
                     VGroup(tag("OLT–ONU etkileşimli", GOOD, 15), ok_x(True, 16)).arrange(RIGHT, buff=0.1),
                     tag("ONU tam denetimde", MUTED, 15)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, -2.05, 0])
        yr = interp("yorum", GOLD, 14).next_to(two[1], RIGHT, buff=0.15)
        self.play(self.set_src("G.989.3 §17.4 · §17.2.2 · Tablo 11-15 · G.989.2 §9.3.7"), run_time=0.3)
        self.at(self.cue("İnce ayarı destekleyen", 1.3))
        self.play(FadeIn(olt), FadeIn(onu), run_time=0.5)
        self.at(self.cue("kapalı bir döngü", 4.5))
        self.play(Create(loop), FadeIn(ll), run_time=0.6)
        self.at(self.cue("küçük verici ayarları", 7.0))
        self.play(*grow_msg(dn), run_time=0.5)
        self.at(self.cue("alınan sinyalin kalitesini", 9.3))
        self.play(*grow_msg(up), run_time=0.5)
        self.at(self.cue("Aracı dalga boyu ayarı", 12.1))
        self.play(FadeIn(aw[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("bir yön biti", 14.8))
        self.play(FadeIn(aw[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("gigahertzlik birimle bir boyut", 16.8))
        self.play(FadeIn(aw[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Bizim yorumumuzla bu", 20.2))
        self.play(FadeIn(two[0]), FadeIn(two[2]), run_time=0.4)
        self.at(self.cue("OLT ile etkileşimli", 24.5))
        self.play(FadeIn(two[1], shift=RIGHT * 0.05), FadeIn(yr), run_time=0.5)
        self.end(pad=0.05)

        # d9 — capabilities (SN_ONU / Tuning_Response): granularity (1 GHz), one-step time (frames, ≥ 90 %, transients included), 0 = none;
        #      rule: statistics from frame F + N × T + 6; 6 frames = 750 µs = normative PLOAM processing time (S1·B10's six frames)
        self.beat("d9")
        h = self.reset("ONU'nun iki yeteneği ve istatistik kuralı", rt=0.5)
        cap = VGroup(VGroup(tag("ayar granülerliği", ACC, 16), T("1 GHz birim · SN oktet 35 · TR oktet 31", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.15),
                     VGroup(tag("tek adım ayar süresi T", GOLD, 16), T("çerçeve · adımın ≥ %90'ı · geçişler dahil · SN 36 · TR 32", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.15),
                     VGroup(HX("0x00", 16, WARN, BOLD), T("→ ince ayar yok", 16, WARN, BOLD)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        cap.move_to([-6.4, 1.45, 0], aligned_edge=LEFT)
        x0, x1, y = -5.6, 4.6, -1.15
        ax, Xf = frame_axis(20, x0, x1, y, labels=False)
        F, NT = 2, 9
        Xs = lambda f: Xf(f)
        resp = VMobject(stroke_color=GOLD, stroke_width=3).set_points_smoothly(
            [[Xs(F + u * NT * 1.15), y + 0.15 + 0.95 * (1 - np.exp(-4.0 * u)) if u > 0 else y + 0.15, 0] for u in np.linspace(0, 1, 30)])
        p90 = DashedLine([Xs(F), y + 0.15 + 0.95 * 0.9, 0], [Xs(F + NT + 2), y + 0.15 + 0.95 * 0.9, 0], color=MUTED, stroke_width=1.4)
        p90l = T("%90", 14, MUTED, BOLD).next_to(p90, LEFT, buff=0.08)
        mF = tmark(Xs(F), y - 0.1, y + 1.35, "F · istek", GOLD, 15)
        bNT = brace_lbl(Line([Xs(F), y, 0], [Xs(F + NT), y, 0]), "N × T", GOLD, DOWN, 16)
        b6 = brace_lbl(Line([Xs(F + NT), y, 0], [Xs(F + NT + 6), y, 0]), "+ 6", ACC, DOWN, 16)
        st = Rectangle(width=Xs(20) - Xs(F + NT + 6), height=0.5, stroke_color=GOOD, stroke_width=1.6, fill_color=GOOD, fill_opacity=0.2).move_to([(Xs(F + NT + 6) + Xs(20)) / 2, y + 0.3, 0])
        stl = T("istatistik", 15, GOOD, BOLD).move_to(st)
        rule = VGroup(T("istatistik başlangıcı =", 20, TXT, BOLD), T("F + N × T + 6", 24, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.6, 0])
        six = VGroup(T("6 çerçeve = 750 µs", 17, ACC, BOLD), T("· PLOAM normatif işleme süresi", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12).move_to([2.2, 0.5, 0])
        ch = s1chip(10, 15).next_to(six, DOWN, buff=0.12).align_to(six, RIGHT)
        self.play(self.set_src("G.989.3 §17.4 · §11.2.6.5 · §11.2.6.6 · §11.1.2"), run_time=0.3)
        self.at(self.cue("bir gigahertzlik birimle ayar", 2.1))
        self.play(FadeIn(cap[0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("tek adım ayar süresi", 6.5))
        self.play(FadeIn(cap[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("en az yüzde doksanına", 9.8))
        self.play(Create(ax), FadeIn(mF), Create(resp), Create(p90), FadeIn(p90l), run_time=1.0)
        self.at(self.cue("Sıfır,", 14.9))
        self.play(FadeIn(cap[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("F çerçevesinde N adım", 18.0))
        self.play(FadeIn(bNT), run_time=0.4)
        self.at(self.cue("F artı N çarpı", 21.0))
        self.play(FadeIn(b6), FadeIn(st), FadeIn(stl), run_time=0.6)
        self.play(FadeIn(rule, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("yedi yüz elli", 28.2))
        self.play(FadeIn(six[0]), run_time=0.4)
        self.at(self.cue("normatif işleme süresidir", 31.0))
        self.play(FadeIn(six[1]), run_time=0.4)
        self.at(self.cue("birinci sezonun onuncu", 34.3))
        self.play(FadeIn(ch, shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # d10 — our arithmetic: T = 8 → N = 1: 1.75 ms, N = 4: 4.75 ms; field max 255 frames = 31.9 ms > Class 2 full-band 25 ms;
        #       window length, metric, dither amplitude, loop period: not in the standard
        self.beat("d10")
        h = self.reset("Bizim hesabımız — kilitlemenin zamanı", rt=0.5)
        hs = interp("hesap", GOLD, 15).next_to(h, RIGHT, buff=0.3)
        tb = mtable(["T (çerçeve)", "N (adım)", "istatistik", "gecikme"], [["8", "1", "F + 14", "1,75 ms"], ["8", "4", "F + 38", "4,75 ms"]],
                    [2.4, 2.0, 2.4, 2.2], size=19, hsize=16, row_h=0.52, mono=(2,)).move_to([-1.6, 1.25, 0])
        for r in tb[1:]:
            r[4].set_color(GOLD)
        x0 = -4.6
        bar1 = hbar(x0, -0.85, 31.9 * 0.3, GOLD, 0.45, 0.5)
        bar1.add(T("255 çerçeve = 31,9 ms · alanın en büyüğü", 16, BG, BOLD).move_to(bar1[0]))
        bar2 = hbar(x0, -1.45, 25 * 0.3, CLC["2"], 0.45, 0.25)
        bar2.add(T("Sınıf 2 · bütün bant · 25 ms", 16, TXT, BOLD).move_to(bar2[0]))
        l1 = T("tek adım", 15, GOLD, BOLD).next_to(bar1[0], LEFT, buff=0.15)
        l2 = T("PMD ayarı", 15, CLC["2"], BOLD).next_to(bar2[0], LEFT, buff=0.15)
        no = VGroup(T("standartta yok:", 17, WARN, BOLD), *[tag(s, WARN, 15) for s in ("pencere boyu", "kalite ölçütü", "titreşim genliği", "döngü periyodu")],
                    T("→ OLT'ye kalmış", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.13)
        fit(no, 12.8).move_to([0, -2.6, 0])
        self.play(FadeIn(hs), self.set_src("G.989.3 §17.4 · SN_ONU oktet 36 · G.989.2 Tablo 9-2 · hesap"), FadeIn(tb[0]), run_time=0.4)
        self.at(self.cue("tek adımda istatistik", 3.0))
        self.play(FadeIn(tb[1], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("dört adımda", 7.3))
        self.play(FadeIn(tb[2], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("Alanın en büyük", 12.1))
        self.play(FadeIn(l1), GrowFromEdge(bar1[0], LEFT), run_time=0.6)
        self.at(self.cue("otuz bir virgül dokuz", 16.1))
        self.play(FadeIn(bar1[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ikinci sınıfın bütün bant", 19.2))
        self.play(FadeIn(l2), GrowFromEdge(bar2[0], LEFT), FadeIn(bar2[1]), run_time=0.6)
        self.at(self.cue("Pencere boyu", 23.6))
        self.play(FadeIn(no[0]), FadeIn(no[1]), run_time=0.4)
        for k, (key, d) in enumerate((("kalite ölçütü", 24.6), ("titreşim genliği", 25.8), ("döngü periyodu", 27.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(no[k + 2], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("hepsi OLT'ye", 30.3))
        self.play(FadeIn(no[5], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p3B")


class E17P3C(Act17):
    HDR, MANIFEST, FIRST = H17[3], M17("p3"), True
    PREV_BADGE = "std"

    def construct(self):
        # d11 — PMD bridge S1·B7: MSE applies to a tunable Tx only in the stationary state; under fine OLT control it covers short-term drift and
        #       control errors; App VIII: max tuning error ≈ MSE − data rate → 10G, 50 GHz: 2.5 GHz (our arithmetic)
        self.beat("d11")
        h, chp = self.pmd_head("PMD Köprüsü — sapma bütçesi", s1chip(7))
        st = VGroup(T("MSE:", 18, GOLD, BOLD), tag("yalnızca durağan kanal durumunda", GOLD, 16)).arrange(RIGHT, buff=0.15).move_to([-6.4, 1.85, 0], aligned_edge=LEFT)
        cov = VGroup(T("OLT ince denetiminde kapsar:", 16, TXT, BOLD), *[tag(s, ACC, 15) for s in ("spektral genişlik", "granülerlik", "kısa süreli kayma", "denetim hataları")]).arrange(RIGHT, buff=0.12)
        fit(cov, 12.6).move_to([0, 1.15, 0])
        sc = 0.36
        x0 = -4.5
        mse = hbar(x0, 0.15, 12.5 * sc, GOLD, 0.5, 0.25)
        msl = T("MSE · 12,5 GHz (50 GHz aralık)", 16, GOLD, BOLD).next_to(mse, UP, buff=0.08).align_to(mse, LEFT)
        dr = hbar(x0, -0.55, 10 * sc, "#94A3B8", 0.5, 0.35)
        drl = T("veri hızı ≈ 10 GHz", 15, TXT, BOLD).move_to(dr[0])
        mte = hbar(x0 + 10 * sc, -0.55, 2.5 * sc, WARN, 0.5, 0.6)
        mtl = VGroup(T("en büyük ayar hatası", 16, WARN, BOLD), T("= 2,5 GHz", 20, WARN, BOLD)).arrange(RIGHT, buff=0.15).next_to(dr, DOWN, buff=0.2).align_to(dr, LEFT)
        frm = VGroup(T("Ek VIII:", 16, GOLD, BOLD), T("en büyük ayar hatası ≈ MSE − veri hızı", 16, TXT, BOLD), interp("hesap", GOLD, 14)).arrange(RIGHT, buff=0.15).move_to([-1.0, -2.1, 0])
        tb = mtable(["kanal aralığı", "MSE", "2,5G", "10G"], [["50 GHz", "± 12,5", "10,0", "2,5"], ["100 GHz", "± 20", "17,5", "10,0"], ["200 GHz", "± 25", "22,5", "15,0"]],
                    [2.0, 1.4, 1.2, 1.2], size=16, hsize=14, row_h=0.36).move_to([3.9, -0.45, 0])
        tb[1][4].set_color(WARN)
        tbl = T("en büyük ayar hatası · GHz", 14, MUTED, BOLD).next_to(tb, UP, buff=0.08)
        self.play(self.set_src("S1·B7 · G.989.2 §11.1.5.2.4 · Tablo 11-6/11-7 · Ek VIII.1 · hesap"), run_time=0.3)
        self.at(self.cue("en büyük spektral sapma", 2.5))
        self.play(FadeIn(st[0]), run_time=0.3)
        self.at(self.cue("yalnızca durağan kanal", 7.5))
        self.play(FadeIn(st[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ince denetiminde", 12.5))
        self.play(FadeIn(cov[0]), LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cov[1:]], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("Sekizinci ek", 18.2))
        self.play(FadeIn(frm[:2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("on gigabitte", 25.5))
        self.play(GrowFromEdge(mse[0], LEFT), FadeIn(msl), GrowFromEdge(dr[0], LEFT), FadeIn(drl), FadeIn(frm[2]), run_time=0.6)
        self.at(self.cue("elli gigahertz aralıkta", 27.8))
        self.play(FadeIn(tbl), FadeIn(tb), run_time=0.5)
        self.at(self.cue("iki buçuk gigahertz", 30.0))
        self.play(GrowFromEdge(mte[0], LEFT), FadeIn(mtl, shift=LEFT * 0.05), Indicate(tb[1][4], color=WARN, scale_factor=1.3), run_time=0.6)
        self.end(pad=0.05)

        # d12 — App VIII OLT WM rules = optical half of locking: monotonic on both sides, ripple < power-measurement resolution → always toward
        #       the minimum-loss point; our arithmetic: a step near the centre ≈ 0.195 dB @ 5 GHz < ± 0.5 dB repeatability; averaging helps
        self.beat("d12")
        h = self.reset("Kilitlemenin optik yarısı — Ek VIII.1", "std", 0.5)
        ax, X = lin_axis(-12, 12, -6.2, 0.6, -2.3, [-10, -5, 0, 5, 10], size=14, fmt=lambda v: f"{v:+g}".replace("+0", "0").replace("-", "−"))
        axl = T("GHz · filtre merkezine göre", 14, MUTED, BOLD).next_to(ax, DOWN, buff=0.35)
        Y = lambda db: 1.4 + db * 1.25
        yax, _ = v_axis(-2.5, 0, Y(-2.5), Y(0), -6.2, [-2, -1, 0], size=14, fmt=lambda v: tr(v))
        yl = T("dB", 14, MUTED, BOLD).next_to(yax, UP, buff=0.08)
        cur = gauss_curve(X, Y, -12, 12, 0.5, 8.0, ACC, 70)
        ref = T("referans: Gauss · 8 GHz'de 0,5 dB", 15, ACC, BOLD).move_to([-2.8, 1.75, 0])
        dot = glow_dot(GOLD, 0.06, 4).move_to([X(-9), Y(-0.5 * (9 / 8) ** 2), 0])
        r1 = VGroup(T("1 · iki yanında tekdüze azalan", 17, TXT, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        r2 = VGroup(T("2 · dalgalanma < güç ölçüm çözünürlüğü", 17, TXT, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        r3 = T("→ kilitleme vericiyi hep en düşük kayıp noktasına iter", 17, GOLD, BOLD)
        rules = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.0, 1.0, 0])
        fit(rules, 6.0)
        rules.move_to([3.85, 1.0, 0])
        stp = VGroup(DashedLine([X(0), Y(0), 0], [X(0), Y(-2.5), 0], color=MUTED, stroke_width=1.2), DashedLine([X(5), Y(-0.195), 0], [X(5), Y(-2.5), 0], color=GOLD, stroke_width=1.4))
        sv = VGroup(T("5 GHz'de", 16, TXT, BOLD), T("0,195 dB", 20, GOLD, BOLD), T("<", 20, TXT, BOLD), T("± 0,5 dB tekrarlanabilirlik", 16, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        sv.move_to([3.85, -0.75, 0])
        fit(sv, 6.0)
        sh = interp("hesap", GOLD, 14).next_to(sv, UP, buff=0.12).align_to(sv, LEFT)
        avg = VGroup(T("Ek VIII:", 16, GOLD, BOLD), T("ortalama alma hatayı azaltabilir", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([3.85, -1.75, 0])
        self.play(self.set_src("G.989.2 Ek VIII.1 · Ek VIII.3 · Tablo II.1 · hesap"), run_time=0.3)
        self.at(self.cue("OLT çoğullayıcı kuralları", 1.0))
        self.play(Create(ax), FadeIn(axl), FadeIn(yax), FadeIn(yl), Create(cur), FadeIn(ref), run_time=1.0)
        self.at(self.cue("tekdüze azalmalı", 5.4))
        self.play(FadeIn(r1, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("dalgalanması güç ölçüm", 8.4))
        self.play(FadeIn(r2, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("böylece kilitleme", 13.3))
        self.play(FadeIn(r3, shift=LEFT * 0.05), FadeIn(dot), run_time=0.4)
        for f in (-6, -3, -1, 0):
            self.play(dot.animate.move_to([X(f), Y(-0.5 * (f / 8) ** 2), 0]), run_time=0.35)
        self.at(self.cue("merkeze yakın bir adım", 18.4))
        self.play(FadeIn(stp), FadeIn(sh), FadeIn(sv[:2]), run_time=0.6)
        self.at(self.cue("yarım desibellik", 21.8))
        self.play(FadeIn(sv[2:], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ortalamanın hatayı", 28.1))
        self.play(FadeIn(avg, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # d13 — supervision (Tables 14-1/14-2): Adjust_Tx_Wavelength count (M, drift estimation basis), amplitude estimator (M); DOTXi defect;
        #       thresholds must consider closed-loop control; no default threshold
        self.beat("d13")
        h = self.reset("Denetim — sayaçlar ve kusur", rt=0.5)
        c1 = VGroup(tag("M", GOOD, 15), T("Adjust_Tx_Wavelength mesaj sayısı", 18, TXT, BOLD), T("→ kayma tahmininin temeli", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.15)
        c2 = VGroup(tag("M", GOOD, 15), T("ayar genliği tahmincisi", 18, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        cs = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-6.3, 1.5, 0], aligned_edge=LEFT)
        dfx = RoundedRectangle(corner_radius=0.14, width=12.4, height=2.6, stroke_color=WARN, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([0, -1.25, 0])
        dt = VGroup(HX("DOTXi", 22, WARN, BOLD), T("verici dalga boyu kayması uyarısı", 19, WARN, BOLD)).arrange(RIGHT, buff=0.2).move_to(dfx.get_corner(UL) + [0.3, -0.38, 0], aligned_edge=LEFT)
        cond = VGroup(T("birim zamandaki istek sayısı", 17, TXT, BOLD), T("ve / veya", 15, MUTED, BOLD), T("istenen genlik", 17, TXT, BOLD), T("> yapılandırılan eşik", 17, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        cond.next_to(dt, DOWN, buff=0.25).align_to(dt, LEFT)
        thr = VGroup(T("eşikler:", 17, TXT, BOLD), T("ONU kapalı döngüde mi? → hesaba kat", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15).next_to(cond, DOWN, buff=0.22).align_to(dt, LEFT)
        dflt = VGroup(T("varsayılan eşik:", 17, TXT, BOLD), T("yok", 18, WARN, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.15).next_to(thr, DOWN, buff=0.22).align_to(dt, LEFT)
        self.play(self.set_src("G.989.3 Tablo 14-1 · Tablo 14-2 · §17.4"), run_time=0.3)
        self.at(self.cue("Dalga boyu ayarı mesajlarının", 0.7))
        self.play(FadeIn(c1[:2], shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("kayma tahmininin temelidir", 5.5))
        self.play(FadeIn(c1[2], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("genlik tahmincisi", 8.3))
        self.play(FadeIn(c2, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("Bir de kusur vardır", 11.0))
        self.play(FadeIn(dfx), run_time=0.3)
        self.at(self.cue("verici dalga boyu kayması", 12.7))
        self.play(FadeIn(dt, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("Birim zamandaki istek", 15.5))
        self.play(FadeIn(cond[:3], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("eşikleri aşınca", 20.0))
        self.play(FadeIn(cond[3], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("kapalı döngüde olup", 23.4))
        self.play(FadeIn(thr, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("Varsayılan eşik yoktur", 28.2))
        self.play(FadeIn(dflt, shift=RIGHT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # d14 — engineer note; d15 — bridge
        self.note11("d14", [("1", "Devir süresini üç parçasıyla ölçün",
                             "Sınıf 1 lazer, burst profilleri önceden dağıtılmıyorsa devri hızlandırmaz", "devir süresini üç"),
                            ("2", "TO4'ü Ek F'nin çizimine göre değil, §12 tablosuna göre kodlayın",
                             "ek onu Complete_u'da, Tablo 12-4 O8.2'deki uygunluk kararında durdurur", "TO4'ü F ekinin")])
        self.bridge_beat("d15", "ONU bir kanalda kilitli.\nPeki birden çok kanalı birlikte kullanmak isterse?")
        self.save_timeline("ep17_p3C")


# ================================ PERDE 4 ======================================
def chain(names, w=0.62, h=0.34, size=14, buff=0.08):
    cols = {"O1": O1C, "O2-3": SNC, "O4": RGC, "O5": OPC}
    return VGroup(*[tile(n, cols[n], w, h, size, 0.22) for n in names]).arrange(RIGHT, buff=buff)


class E17P4A(Act17):
    HDR, MANIFEST, FIRST = H17[4], M17("p4"), True

    def construct(self):
        # e1 — Annex H (normative, short): a bonded ONU supports several PON interfaces, each an ANI ME in the single OMCI MIB;
        #      one activation state machine per interface
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Bağlama ve karışık sınıflar")
        self.at(self.cue("H eki normatiftir", 1.6))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Ek H — kanal bağlama")
        nrm = VGroup(tag("normatif", GOLD, 16), tag("kısa", MUTED, 16)).arrange(RIGHT, buff=0.12).next_to(h, RIGHT, buff=0.3)
        body = RoundedRectangle(corner_radius=0.2, width=7.0, height=4.4, stroke_color=ONUC, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-2.6, -0.75, 0])
        bl = T("bağlı ONU", 20, ONUC, BOLD).move_to(body.get_corner(UL) + [0.3, -0.32, 0], aligned_edge=LEFT)
        mib = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.25, stroke_color=GOLD, stroke_width=2, fill_color="#0C1324", fill_opacity=1).move_to([-2.6, 0.35, 0])
        mibl = T("OMCI MIB · tek kopya", 16, GOLD, BOLD).move_to(mib.get_corner(UL) + [0.25, -0.25, 0], aligned_edge=LEFT)
        anis = VGroup(*[tag(f"ANI ME #{k}", GOLD, 15) for k in (1, 2)]).arrange(RIGHT, buff=0.5).move_to(mib).shift(DOWN * 0.18)
        ifs = VGroup()
        for k, (x, c) in enumerate(((-4.2, CH[0]), (-1.0, CH[1]))):
            box_ = RoundedRectangle(corner_radius=0.1, width=2.9, height=1.5, stroke_color=c, stroke_width=2, fill_color="#0C1324", fill_opacity=1).move_to([x, -1.65, 0])
            t = T(f"PON arayüzü {k + 1}", 16, c, BOLD).move_to(box_.get_top() + DOWN * 0.25)
            ch_ = chain(["O1", "O2-3", "O4", "O5"], 0.6, 0.34, 14, 0.06).move_to(box_).shift(DOWN * 0.18)
            ifs.add(VGroup(box_, t, ch_))
        cts = VGroup(ct_box("CT · λ1", CH[0], 1.5, 0.5, 16).move_to([3.9, 0.3, 0]), ct_box("CT · λ2", CH[1], 1.5, 0.5, 16).move_to([3.9, -1.65, 0]))
        lk = VGroup(Line(ifs[0][0].get_bottom() + DOWN * 0.0, ifs[0][0].get_bottom() + DOWN * 0.45, color=CH[0], stroke_width=2.2),
                    Line(ifs[1][0].get_right(), cts[1].get_left(), color=CH[1], stroke_width=2.2))
        lk0 = VGroup(Line(ifs[0][0].get_bottom() + DOWN * 0.45, [2.6, ifs[0][0].get_bottom()[1] - 0.45, 0], color=CH[0], stroke_width=2.2),
                     Line([2.6, ifs[0][0].get_bottom()[1] - 0.45, 0], [2.6, 0.3, 0], color=CH[0], stroke_width=2.2),
                     Line([2.6, 0.3, 0], cts[0].get_left(), color=CH[0], stroke_width=2.2))
        sm_ = T("her arayüz: ayrı aktivasyon makinesi", 16, TXT, BOLD).next_to(body, DOWN, buff=0.12).align_to(body, LEFT)
        self.play(self.set_src("G.989.3 Ek H.1"), FadeIn(nrm, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Kanal bağlamalı servis", 4.0))
        self.play(FadeIn(body), FadeIn(bl), run_time=0.5)
        self.at(self.cue("birden çok PON arayüzünü", 8.8))
        self.play(FadeIn(ifs[0][:2]), FadeIn(ifs[1][:2]), FadeIn(cts), Create(lk), Create(lk0), run_time=0.8)
        self.at(self.cue("tek OMCI bilgi tabanında", 12.5))
        self.play(FadeIn(mib), FadeIn(mibl), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.05) for a in anis], lag_ratio=0.3), run_time=0.6)
        self.at(self.cue("ayrı bir aktivasyon durum", 18.5))
        self.play(FadeIn(ifs[0][2], shift=RIGHT * 0.05), FadeIn(ifs[1][2], shift=RIGHT * 0.05), FadeIn(sm_), run_time=0.6)
        self.end(pad=0.05)

        # e2 — order: the pilot interface completes activation (→ O5) first; pilot uses ONU-ID 1023 in Serial_Number_ONU and is the source of
        #      the ONU-ID and the partition; later interfaces: same SN, pilot's ONU-ID, another TWDM channel in the partition, may be concurrent
        self.beat("e2")
        h = self.reset("Ek H.1 — önce öncü arayüz", rt=0.5)
        x0 = -4.2
        L = [("PON 1 · öncü · λ1", CH[0], 1.25, x0), ("PON 2 · λ2", CH[1], 0.05, 0.0), ("PON 3 · λ3", CH[2], -1.15, 0.55)]
        lanes = VGroup()
        for name, c, y, xs in L:
            segs = strip([(1.0, "O1", O1C, 0.3), (1.5, "O2-3", SNC, 0.3), (1.1, "O4", RGC, 0.3), (6.5 - (xs + 3.6), "O5", OPC, 0.15)], xs, y, 0.5, 15)
            lb = T(name, 16, c, BOLD).move_to([-6.45, y, 0], aligned_edge=LEFT)
            lanes.add(VGroup(lb, segs))
        gate = DashedLine([0.0, 1.75, 0], [0.0, -1.65, 0], color=GOLD, stroke_width=2)
        gl = T("öncü O5'te → sonra diğerleri", 15, GOLD, BOLD).next_to(gate.get_top(), RIGHT, buff=0.12)
        sn1 = mbox("SN · ONU-ID 0x03FF = 1023", SNC, None, 0.36, 14, 0.3).next_to(lanes[0][1][1], UP, buff=0.1)
        sn2 = mbox("aynı SN · öncünün ONU-ID'si", SNC, None, 0.36, 14, 0.3).next_to(lanes[1][1][1], DOWN, buff=0.1)
        src_ = VGroup(T("öncü:", 17, CH[0], BOLD), T("ONU-ID'nin ve kanal bölümlemesinin kaynağı", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([-1.5, -2.25, 0])
        prt = VGroup(tag("bölüm içinde başka bir TWDM kanalı", GOOD, 15), tag("eşzamanlı olabilir", GOOD, 15)).arrange(RIGHT, buff=0.2).move_to([0.0, -2.95, 0])
        self.play(self.set_src("G.989.3 Ek H.1 · Tablo 11-25 (oktet 1–2)"), run_time=0.3)
        self.at(self.cue("İlk arayüzün aktivasyonu", 1.2))
        self.play(FadeIn(lanes[0][0]), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.05) for s in lanes[0][1]], lag_ratio=0.2), run_time=0.9)
        self.play(Create(gate), FadeIn(gl), run_time=0.5)
        self.at(self.cue("bu ilk arayüz öncüdür", 8.2))
        self.play(Indicate(lanes[0][0], color=CH[0], scale_factor=1.1), run_time=0.5)
        self.at(self.cue("atanmamış ONU kimliğini", 10.5))
        self.play(FadeIn(sn1, shift=DOWN * 0.05), run_time=0.45)
        self.at(self.cue("ve ONU kimliğinin ve bölümlemenin", 16.4))
        self.play(FadeIn(src_, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Sonraki her arayüz", 20.2))
        self.play(FadeIn(lanes[1][0]), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.05) for s in lanes[1][1]], lag_ratio=0.2), run_time=0.8)
        self.play(FadeIn(sn2, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("bölüm içindeki başka", 26.9))
        self.play(FadeIn(prt[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("eşzamanlı da olabilir", 30.3))
        self.play(FadeIn(lanes[2][0]), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.05) for s in lanes[2][1]], lag_ratio=0.15), FadeIn(prt[1], shift=UP * 0.05), run_time=0.7)
        self.end(pad=0.05)

        # e3 — undefined behaviour in four cases; one OMCC per interface; an OMCI command on any → the same MIB; answer on the same interface
        self.beat("e3")
        h = self.reset("Tanımsız davranış ve OMCC", rt=0.5)
        ub = VGroup(*[VGroup(ok_x(False, 18), T(s, 17, TXT, BOLD)).arrange(RIGHT, buff=0.15) for s in
                      ("başka bir kanal bölümü", "zaten etkin arayüzün olduğu kanal", "farklı bir seri numarası", "OLT farklı bir ONU-ID atarsa")])
        ub.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-6.3, 0.35, 0], aligned_edge=LEFT)
        ubl = T("tanımsız davranış:", 18, WARN, BOLD).next_to(ub, UP, buff=0.3).align_to(ub, LEFT)
        mib = sbox("OMCI MIB", "tek kopya", GOLD, 2.4, 0.85, 19, 15).move_to([3.6, 1.5, 0])
        pi = VGroup(*[sbox(f"PON {k}", f"OMCC {k}", c, 1.9, 0.75, 17, 14).move_to([x, -0.9, 0]) for k, c, x in ((1, CH[0], 2.0), (2, CH[1], 5.2))])
        om = VGroup(*[DashedLine(p[0].get_top(), mib[0].get_bottom(), color=p[0].get_stroke_color(), stroke_width=2) for p in pi])
        cmd = arrow(pi[1][0].get_bottom() + DOWN * 0.75, pi[1][0].get_bottom(), GOLD, 2.4, 0.12)
        cml = T("OMCI komutu", 15, GOLD, BOLD).next_to(cmd, RIGHT, buff=0.1)
        ap = arrow(pi[1][0].get_top() + LEFT * 0.2, mib[0].get_bottom() + RIGHT * 0.4, GOLD, 3, 0.14)
        rep_ = arrow(pi[1][0].get_bottom() + LEFT * 0.4, pi[1][0].get_bottom() + LEFT * 0.4 + DOWN * 0.75, GOOD, 2.4, 0.12)
        rpl = T("cevap · aynı arayüzden", 15, GOOD, BOLD).next_to(rep_, LEFT, buff=0.1)
        self.at(self.cue("Tanımsız davranış", 0.0))
        self.play(FadeIn(ubl), self.set_src("G.989.3 Ek H.1 · G.988"), run_time=0.3)
        for k, (key, d) in enumerate((("başka bir bölüm", 3.1), ("zaten etkin bir", 4.4), ("farklı bir seri numarası", 8.2), ("farklı bir ONU kimliği", 10.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(ub[k], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("Her arayüz için bir OMCC", 14.1))
        self.play(FadeIn(mib), FadeIn(pi), Create(om[0]), Create(om[1]), run_time=0.6)
        self.at(self.cue("hangisinden gelirse", 16.8))
        self.play(GrowArrow(cmd), FadeIn(cml), run_time=0.4)
        self.play(GrowArrow(ap), Indicate(mib, color=GOLD, scale_factor=1.06), run_time=0.6)
        self.at(self.cue("cevap komutun geldiği", 23.0))
        self.play(GrowArrow(rep_), FadeIn(rpl), run_time=0.5)
        self.end(pad=0.05)

        # e4 — our inference: the same ONU-ID in several channels at once → uniqueness is per channel; ICTP consistency check must allow it;
        #      not in the standard: traffic distribution, handover of a bonded interface, any G.989.2 line on multi-transceiver ONUs
        self.beat("e4")
        h = self.reset("Bizim çıkarımımız — kimlik kanal düzeyinde", rt=0.5)
        cols = VGroup()
        for k, (lam, c) in enumerate((("λ1", CH[0]), ("λ2", CH[1]))):
            hd = tile(f"kanal {lam}", c, 2.3, 0.45, 16, 0.25)
            ids = VGroup(HX("ONU-ID a", 17, MUTED, BOLD), HX("ONU-ID k", 18, GOLD, BOLD), HX("ONU-ID b", 17, MUTED, BOLD)) if k == 0 else \
                VGroup(HX("ONU-ID c", 17, MUTED, BOLD), HX("ONU-ID k", 18, GOLD, BOLD), HX("ONU-ID d", 17, MUTED, BOLD))
            ids.arrange(DOWN, buff=0.18)
            cols.add(VGroup(hd, ids).arrange(DOWN, buff=0.25))
        cols.arrange(RIGHT, buff=1.0).move_to([-3.6, 0.45, 0])
        same = Line(cols[0][1][1].get_right() + RIGHT * 0.1, cols[1][1][1].get_left() + LEFT * 0.1, color=GOLD, stroke_width=2.4)
        sl = T("aynı bağlı ONU", 15, GOLD, BOLD).next_to(same, UP, buff=0.05)
        cr = VGroup(interp("çıkarım", GOLD, 14), T("benzersizlik: kanal düzeyinde", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([3.0, 1.35, 0])
        ict = VGroup(T("ICTP · SN ve ONU-ID tutarlılık denetimi", 16, ICTC, BOLD), T("→ buna izin vermeli", 16, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([3.0, 0.45, 0])
        no = VGroup(T("standartta yok:", 17, WARN, BOLD), tag("trafiğin kanallara dağıtımı", WARN, 15), tag("bağlı bir arayüzün devri", WARN, 15),
                    tag("G.989.2: çok alıcı-vericili ONU · tek satır yok", WARN, 15)).arrange(RIGHT, buff=0.15)
        fit(no, 12.8).move_to([0, -2.45, 0])
        self.play(self.set_src("G.989.3 Ek H.1 · Ek VI (UC5) · çıkarım"), run_time=0.3)
        self.at(self.cue("aynı ONU kimliği aynı anda", 1.5))
        self.play(FadeIn(cols), run_time=0.6)
        self.play(Create(same), FadeIn(sl), run_time=0.5)
        self.at(self.cue("benzersizliği kanal düzeyindedir", 7.0))
        self.play(FadeIn(cr, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("ICTP'nin kimlik tutarlılığı", 10.6))
        self.play(FadeIn(ict, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("Standartta olmayanlar", 15.7))
        self.play(FadeIn(no[0]), run_time=0.3)
        for k, (key, d) in enumerate((("trafiğin kanallara", 17.5), ("bağlı bir arayüzün devri", 19.9), ("çok alıcı vericili", 22.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(no[k + 1], shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p4A")


class E17P4B(Act17):
    HDR, MANIFEST, FIRST = H17[4], M17("p4"), True
    PREV_BADGE = "std"

    def construct(self):
        # e5 — Appendix X (informative): pay-as-you-grow — N1 CTs first, higher classes later; the ODN reused; ONU optics identical N1 … E1
        #      → the mix is only on the OLT side; no special TC feature
        self.beat("e5")
        h = self.show_heading("Ek X — karışık sınıflar")
        inf_ = tag("bilgilendirici", MUTED, 16).next_to(h, RIGHT, buff=0.3)
        t1 = VGroup(T("önce", 16, MUTED, BOLD), VGroup(*[ct_box("N1", CH[k], 0.8, 0.42, 15) for k in range(2)]).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.12).move_to([-5.2, 0.9, 0])
        t2 = VGroup(T("sonra", 16, MUTED, BOLD), VGroup(*[ct_box(n, CH[k + 2], 0.8, 0.42, 15) for k, n in enumerate(("N2", "E1"))]).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.12).move_to([-3.2, 0.9, 0])
        ga = arrow(t1.get_right() + RIGHT * 0.05, t2.get_left() + LEFT * 0.05, GOLD, 2.2, 0.12)
        gal = T("kademeli büyüme", 15, GOLD, BOLD).move_to([-4.2, 1.95, 0])
        odn = VGroup(splitter(0.3), T("ODN", 16, FEED, BOLD)).arrange(RIGHT, buff=0.15).move_to([-0.3, 0.9, 0])
        odl = T("çoğu zaman yeniden kullanılmak zorunda", 15, FEED, BOLD).next_to(odn, DOWN, buff=0.2)
        cls = VGroup(*[tile(n, c, 0.9, 0.45, 17, 0.2) for n, c in (("N1", GOOD), ("N2", ACC), ("E1", GOLD))]).arrange(RIGHT, buff=0.15).move_to([3.8, 1.2, 0])
        cb = brace_lbl(cls, "ONU tarafı optik: aynı", ONUC, DOWN, 17)
        mix = VGroup(T("karışım yalnızca", 18, TXT, BOLD), tag("OLT tarafında", OLTC, 17)).arrange(RIGHT, buff=0.15).move_to([0, -1.55, 0])
        tc_ = VGroup(T("özel TC özelliği", 18, TXT, BOLD), T("gerekmez", 18, GOOD, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.15).next_to(mix, DOWN, buff=0.3)
        self.play(self.set_src("G.989.3 Ek X.1 · Ek X.2.1 · G.989.2 Tablo 6-1"), FadeIn(inf_, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Senaryo kademeli büyümedir", 3.7))
        self.play(FadeIn(gal), run_time=0.3)
        self.at(self.cue("önce N1 optikli", 6.0))
        self.play(FadeIn(t1, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("sonra daha yüksek", 8.7))
        self.play(GrowArrow(ga), FadeIn(t2, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("ODN çoğu zaman", 11.5))
        self.play(FadeIn(odn), FadeIn(odl), run_time=0.5)
        self.at(self.cue("ONU tarafı optik", 17.7))
        self.play(FadeIn(cls), run_time=0.4)
        self.at(self.cue("N1'den E1'e kadar", 19.1))
        self.play(FadeIn(cb), run_time=0.4)
        self.at(self.cue("karışım yalnızca OLT", 21.6))
        self.play(FadeIn(mix, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("özel bir TC özelliği", 24.9))
        self.play(FadeIn(tc_, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # e6 — PMD bridge S1·B2: N1 14–29, N2 16–31 dB; N2's extra 2 dB may buy one more split stage if N1 has margin; our check: ideal 1×2 = 3.01 dB
        self.beat("e6")
        h, chp = self.pmd_reset("PMD Köprüsü — iki desibel", s1chip(2))
        ax, X = lin_axis(10, 36, -5.2, 5.6, -1.6, [10, 14, 16, 20, 25, 29, 31, 35], size=15, fmt=lambda v: f"{v:g}")
        axl = T("optik yol kaybı · dB", 15, MUTED, BOLD).next_to(ax, DOWN, buff=0.3)
        bars = VGroup()
        for name, a, b, c, y in (("N1", 14, 29, GOOD, 1.05), ("N2", 16, 31, ACC, 0.3)):
            r = Rectangle(width=X(b) - X(a), height=0.45, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.3).move_to([(X(a) + X(b)) / 2, y, 0])
            lab = T(f"{name} · {a}–{b} dB", 16, TXT, BOLD).move_to(r)
            nm = T(name, 17, c, BOLD).next_to(r, LEFT, buff=0.2)
            bars.add(VGroup(r, lab, nm))
        p2 = brace_lbl(Line([X(29), 0.0, 0], [X(31), 0.0, 0]), "+2 dB", GOLD, DOWN, 16)
        sp = Rectangle(width=X(32.01) - X(29), height=0.4, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.3).move_to([(X(29) + X(32.01)) / 2, -0.95, 0])
        spl = VGroup(T("ideal 1×2:", 15, WARN, BOLD), T("10·log10(2) = 3,01 dB", 16, WARN, BOLD)).arrange(RIGHT, buff=0.12).next_to(sp, LEFT, buff=0.2)
        ek = VGroup(T("Ek X:", 17, GOLD, BOLD), T("N1 kurulumunda uygun pay varsa → bir ayırma kademesi daha", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, 1.9, 0])
        con = VGroup(interp("bizim kontrolümüz", GOLD, 14), T("2 dB tek başına yetmez → koşul bu yüzden", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -2.65, 0])
        self.play(self.set_src("S1·B2 · G.989.2 Tablo 6-1 · G.989.3 Ek X.2.1 · hesap"), Create(ax), FadeIn(axl), run_time=0.5)
        self.at(self.cue("N1 on dört", 4.7))
        self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), run_time=0.5)
        self.at(self.cue("N2 on altı", 7.0))
        self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), run_time=0.5)
        self.at(self.cue("fazladan iki desibeli", 9.7))
        self.play(FadeIn(p2), run_time=0.4)
        self.at(self.cue("N1 kurulumunda uygun pay", 12.9))
        self.play(FadeIn(ek, shift=DOWN * 0.05), run_time=0.5)
        self.at(self.cue("ideal bir bire iki", 20.2))
        self.play(GrowFromEdge(sp, LEFT), FadeIn(spl), run_time=0.6)
        self.at(self.cue("İki desibel tek başına", 25.9))
        self.play(FadeIn(con, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # e7 — Figure X.2: two legacy systems merged; two N1 CTs on λ1, each feeding its own ODN; three N2 CTs through 1×2 splitters into both;
        #      each ONU still sees four CTs; modelling it as two systems = excessive and useless complexity
        self.beat("e7")
        h = self.reset("Ek X.2.2 — iki eski sistem birleşir", "std", 0.5)
        cy = [1.7, 0.85, 0.0, -0.85, -1.7]
        spec = [("CT1 · N1", CH[0]), ("CT2 · N2", CH[1]), ("CT3 · N2", CH[2]), ("CT4 · N2", CH[3]), ("CT5 · N1", CH[0])]
        cts = VGroup(*[ct_box(n, c, 1.6, 0.48, 15).move_to([-5.6, y, 0]) for (n, c), y in zip(spec, cy)])
        wma = sbox("WM 4×1", "A", MUTED, 1.2, 1.5, 16, 14).move_to([-0.8, 0.95, 0])
        wmb = sbox("WM 4×1", "B", MUTED, 1.2, 1.5, 16, 14).move_to([-0.8, -0.95, 0])
        sps = VGroup(*[splitter(0.22).move_to([-3.3, y, 0]) for y in cy[1:4]])
        ln = VGroup(Line(cts[0].get_right(), wma[0].get_left() + UP * 0.6, color=CH[0], stroke_width=2.2),
                    Line(cts[4].get_right(), wmb[0].get_left() + DOWN * 0.6, color=CH[0], stroke_width=2.2))
        sl = VGroup()
        for k, (s_, c) in enumerate(zip(sps, CH[1:4])):
            sl.add(VGroup(Line(cts[k + 1].get_right(), s_.get_left(), color=c, stroke_width=2.2),
                          Line(s_.get_right(), wma[0].get_left() + UP * (0.25 - 0.25 * k), color=c, stroke_width=1.8),
                          Line(s_.get_right(), wmb[0].get_left() + UP * (0.25 - 0.25 * k), color=c, stroke_width=1.8)))
        spl = T("1×2", 14, FEED, BOLD).next_to(sps, DOWN, buff=0.08)
        odn = VGroup(*[VGroup(Line(w[0].get_right(), w[0].get_right() + RIGHT * 0.8, color=FEED, stroke_width=2.2), splitter(0.28).move_to(w[0].get_right() + RIGHT * 1.05),
                              T(f"ODN-64 {s}", 15, FEED, BOLD).move_to(w[0].get_right() + RIGHT * 1.05 + DOWN * 0.42)) for w, s in ((wma, "A"), (wmb, "B"))])
        onus = VGroup(*[onu_box("ONU", ONUC, 0.9, 0.45, 15).move_to(o[1].get_center() + RIGHT * 1.2) for o in odn])
        see = VGroup(*[T("4 CT görür", 15, ONUC, BOLD).next_to(o, RIGHT, buff=0.15) for o in onus])
        lam1 = tag("ikisi de λ1", CH[0], 15).next_to(cts[0], UP, buff=0.12).shift(RIGHT * 1.2)
        cx = VGroup(T("\"iki sistem gibi modellemek:", 17, TXT, BOLD), T("aşırı ve yararsız karmaşıklık\"", 17, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.2, -2.55, 0])
        self.play(self.set_src("G.989.3 Ek X.2.2 · Şekil X.2 · Ek X.2.3"), run_time=0.3)
        self.at(self.cue("iki eski sistem", 1.0))
        self.play(FadeIn(cts), FadeIn(wma), FadeIn(wmb), run_time=0.6)
        self.at(self.cue("İki N1 sonlandırıcısı", 4.0))
        self.play(Indicate(VGroup(cts[0], cts[4]), color=CH[0], scale_factor=1.05), FadeIn(lam1), run_time=0.6)
        self.at(self.cue("kendi ODN'ini besler", 9.0))
        self.play(Create(ln), FadeIn(odn), run_time=0.7)
        self.at(self.cue("Üç N2 sonlandırıcısı", 11.3))
        self.play(FadeIn(sps), FadeIn(spl), *[Create(s) for s in sl], run_time=1.0)
        self.at(self.cue("ayar yaparken yine dört", 18.0))
        self.play(FadeIn(onus), FadeIn(see), run_time=0.5)
        self.at(self.cue("iki sistem gibi", 22.5))
        self.play(FadeIn(cx, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # e8 — cloned CTs: share NG2SYS ID, channel IDs, PON-ID, PON-TAG …; disjoint ONU sets; three ways to tell the subtrees apart
        self.beat("e8")
        h = self.reset("Çözüm: klonlanmış sonlandırıcılar", rt=0.5)
        c1 = sbox("CT1", "λ1 · ODN A", CH[0], 1.8, 0.75, 18, 14).move_to([-5.2, 1.0, 0])
        c5 = sbox("CT5", "λ1 · ODN B", CH[0], 1.8, 0.75, 18, 14).move_to([-5.2, -0.6, 0])
        sh = VGroup(*[tag(s, GOLD, 15) for s in ("NG2SYS ID", "↓ / ↑ kanal kimlikleri", "PON-ID", "PON-TAG", "…")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-2.4, 0.2, 0])
        br = VGroup(Line(c1[0].get_right(), sh.get_left() + UP * 0.4, color=GOLD, stroke_width=1.6), Line(c5[0].get_right(), sh.get_left() + DOWN * 0.4, color=GOLD, stroke_width=1.6))
        shl = T("paylaşılan parametreler", 15, GOLD, BOLD).next_to(sh, UP, buff=0.12)
        dj = VGroup(T("ONU kümeleri:", 16, TXT, BOLD), T("ayrık", 17, GOOD, BOLD), T("· tasarım gereği", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.12).move_to([-4.0, -1.7, 0])
        ways = VGroup(T("alt ağacı ayırmanın 3 yolu", 17, TXT, BOLD),
                      VGroup(T("1", 17, GOLD, BOLD), T("yalnızca klonlu kanallarda aktivasyon", 16, TXT, BOLD), tag("ONU-ID ayırır", GOOD, 14)).arrange(RIGHT, buff=0.15),
                      VGroup(T("2", 17, GOLD, BOLD), T("klonlu çifte kalibrasyon isteği", 16, TXT, BOLD), tag("ONU-ID ayırır", GOOD, 14)).arrange(RIGHT, buff=0.15),
                      VGroup(T("3", 17, GOLD, BOLD), T("sonradan devir", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        ways.move_to([3.6, 0.0, 0])
        for w in ways[1:3]:
            w[2].set_opacity(0)
        self.at(self.cue("Çözüm klonlanmış", 0.5))
        self.play(FadeIn(c1), FadeIn(c5), self.set_src("G.989.3 Ek X.2.3 · Şekil X.3"), run_time=0.5)
        for k, (key, d) in enumerate((("sistem kimliği", 3.0), ("kanal kimlikleri", 4.3), ("PON kimliği ve PON etiketi", 5.7))):
            self.at(self.cue(key, d))
            if k == 0:
                self.play(FadeIn(shl), Create(br), FadeIn(sh[0], shift=RIGHT * 0.05), run_time=0.45)
            elif k == 1:
                self.play(FadeIn(sh[1], shift=RIGHT * 0.05), run_time=0.3)
            else:
                self.play(FadeIn(sh[2:], shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("ayrık ONU kümelerine", 13.5))
        self.play(FadeIn(dj, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("Alt ağacı ayırmak", 16.7))
        self.play(FadeIn(ways[0]), run_time=0.35)
        for k, (key, d) in enumerate((("yalnızca klonlu kanallarda", 20.0), ("klonlu çifte kalibrasyon", 23.2), ("ya da sonradan devir", 25.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(ways[k + 1][:2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("ilk ikisinde ONU kimliği", 27.1))
        self.play(ways[1][2].animate.set_opacity(1), ways[2][2].animate.set_opacity(1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p4B")


class E17P4C(Act17):
    HDR, MANIFEST, FIRST = H17[4], M17("p4"), True
    PREV_BADGE = "std"

    def construct(self):
        # e9 — Channel_Profile octet 32 'cloned configuration': upper nibble = cloned system, lower nibble = operator-assigned subtree ID
        #      (only in the channel's own profile); present since 2021; field limit: 1 GHz units cannot write ± 12.5 GHz
        self.beat("e9")
        h = self.show_heading("Kanal profili oktet 32 — klonlu yapılandırma")
        bb = bitbox([(c, GOLD) for c in "AAAA"] + [(c, ACC) for c in "BBBB"], 0.55, 0.6, 20).move_to([-2.4, 1.3, 0])
        bl = T("Channel_Profile · oktet 32", 16, MUTED, BOLD).next_to(bb, UP, buff=0.12)
        a_ = VGroup(T("A · üst 4 bit", 17, GOLD, BOLD), VGroup(HX("0000", 16, TXT, BOLD), T("normal", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12),
                    VGroup(HX("0001", 16, GOLD, BOLD), T("klonlu sistem", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        a_.next_to(bb[:4], DOWN, buff=0.3).align_to(bb, LEFT).shift(LEFT * 1.2)
        b_ = VGroup(T("B · alt 4 bit", 17, ACC, BOLD), T("operatörün verdiği alt ağaç no.", 16, TXT, BOLD), T("yalnız \"bu kanal\" profilinde · aksi 0", 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        b_.next_to(bb[4:], DOWN, buff=0.3).align_to(bb[4:], LEFT).shift(RIGHT * 0.3)
        since = tag("2021'den beri", GOOD, 16).next_to(bb, RIGHT, buff=0.4)
        lim = RoundedRectangle(corner_radius=0.14, width=12.4, height=1.25, stroke_color=WARN, stroke_width=1.8, fill_color=PANEL, fill_opacity=1).move_to([0, -2.35, 0])
        lt = VGroup(T("alan sınırı:", 17, WARN, BOLD), T("System_Profile · 1 GHz birim", 17, TXT, BOLD), T("·", 17, MUTED), T("50 GHz aralıkta MSE ± 12,5 GHz", 17, TXT, BOLD),
                    T("→", 18, MUTED), HX("12? 13?", 18, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        fit(lt, 12.0).move_to(lim)
        self.play(self.set_src("G.989.3 Tablo 11-18 (oktet 32) · Ek X · Tablo 11-17 · G.989.2 Tablo 11-6"), run_time=0.3)
        self.at(self.cue("otuz ikinci baytı", 1.0))
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(b) for b in bb], lag_ratio=0.06), run_time=0.7)
        self.at(self.cue("üst dört bit", 3.8))
        self.play(FadeIn(a_, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("alt dört bit", 6.2))
        self.play(FadeIn(b_[:2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("ikincisi yalnızca", 10.5))
        self.play(FadeIn(b_[2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("iki bin yirmi birden", 14.1))
        self.play(FadeIn(since, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Bir alan sınırı", 17.3))
        self.play(FadeIn(lim), FadeIn(lt[0]), run_time=0.4)
        self.at(self.cue("bir gigahertzlik birimleri", 19.1))
        self.play(FadeIn(lt[1]), run_time=0.4)
        self.at(self.cue("on iki buçuk gigahertzlik", 24.0))
        self.play(FadeIn(lt[2:4]), run_time=0.4)
        self.at(self.cue("tam yazamaz", 27.5))
        self.play(FadeIn(lt[4:], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # e10 — PMD bridge S1·B3: DS channels 100 GHz apart → a 100 GHz-restricted Class 2 (2R1) receiver reaches only the neighbour;
        #       at 200 GHz US spacing a 2R1 transmitter cannot reach even the neighbour; choose restricted classes with the channel plan
        self.beat("e10")
        h, chp = self.pmd_reset("PMD Köprüsü — kısıtlı sınıf ve plan", s1chip(3))

        def grid(y, sp, n, color, lab):
            xs = [-3.2 + k * sp for k in range(n)]
            ln = Line([-5.0, y, 0], [6.4, y, 0], color=MUTED, stroke_width=1.5)
            tk = VGroup(*[Line([x, y - 0.2, 0], [x, y + 0.45, 0], color=color, stroke_width=3) for x in xs])
            t = T(lab, 16, color, BOLD).move_to([-6.4, y + 0.1, 0], aligned_edge=LEFT)
            return VGroup(ln, tk, t), xs
        U = 1.35   # units per 100 GHz
        g1, x1 = grid(0.85, U, 6, CH[1], "↓ · 100 GHz aralık")
        g2, x2 = grid(-1.25, 2 * U, 4, CH[0], "↑ · 200 GHz aralık")
        sp1 = brace_lbl(Line([x1[0], 0.85, 0], [x1[1], 0.85, 0]), "100 GHz", MUTED, DOWN, 14)
        sp2 = brace_lbl(Line([x2[0], -1.25, 0], [x2[1], -1.25, 0]), "200 GHz", MUTED, DOWN, 14)
        r1 = Rectangle(width=2 * U, height=0.35, stroke_color=CLC["2"], stroke_width=2, fill_color=CLC["2"], fill_opacity=0.25).move_to([x1[1], 1.55, 0])
        r1l = T("2R1 alıcı · ≤ 100 GHz", 15, CLC["2"], BOLD).next_to(r1, UP, buff=0.06)
        ok1 = T("yalnız komşu kanal ✓", 16, GOOD, BOLD).next_to(r1, RIGHT, buff=0.3)
        r2 = Rectangle(width=2 * U, height=0.35, stroke_color=CLC["2"], stroke_width=2, fill_color=CLC["2"], fill_opacity=0.25).move_to([x2[1], -0.55, 0])
        r2l = T("2R1 verici · ≤ 100 GHz", 15, CLC["2"], BOLD).next_to(r2, UP, buff=0.06)
        no2 = T("komşuya bile ulaşamaz ✗", 16, WARN, BOLD).next_to(r2, RIGHT, buff=0.3)
        con = VGroup(interp("çıkarım", GOLD, 14), T("kısıtlı sınıf, kanal planıyla birlikte seçilmeli", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -2.85, 0])
        self.play(self.set_src("S1·B3 · G.989.2 Tablo 9-2 · Tablo 11-2 · çıkarım"), run_time=0.3)
        self.at(self.cue("Aşağı yön kanalları yüz", 7.2))
        self.play(FadeIn(g1), FadeIn(sp1), run_time=0.6)
        self.at(self.cue("yüz gigahertzle kısıtlı", 12.5))
        self.play(FadeIn(r1), FadeIn(r1l), run_time=0.5)
        self.at(self.cue("yalnızca komşu kanala", 17.0))
        self.play(FadeIn(ok1, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Yukarı yönde iki yüz", 19.3))
        self.play(FadeIn(g2), FadeIn(sp2), run_time=0.6)
        self.at(self.cue("aynı sınıftaki bir verici", 23.4))
        self.play(FadeIn(r2), FadeIn(r2l), FadeIn(no2, shift=LEFT * 0.05), run_time=0.6)
        self.at(self.cue("Kısıtlı sınıf,", 27.8))
        self.play(FadeIn(con, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # e11 — engineer note; e12 — bridge
        self.note11("e11", [("1", "Bağlı ONU'ları SN ve kanal çiftiyle izleyin, ONU-ID ile değil",
                             "aynı kimlik birden çok kanalda yasal olarak görünür", "bağlı ONU'ları envanterde"),
                            ("2", "Klonlu CT'lerde alt ağacı yalnızca ONU-ID ve oktet 32 ayırır",
                             "kimlik planını ayrık tutun · ayırma kademesi eklemeden önce N1 payını ölçün", "klonlu sonlandırıcılarda")])
        self.bridge_beat("e12", "Kurallar belli.\nŞimdi laboratuvarda bir devri ölçelim.")
        self.save_timeline("ep17_p4C")
