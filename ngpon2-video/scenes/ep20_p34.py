"""S2·B10 · Perde 3 (başıboş ONU ve acil durdurma — G.989.3 §19.1–§19.5, §12.1.5, §11.3.3.5 Tablo 11-9 (Amd.2 neden kodu), Tablo 12-1 O7,
Ek XI (Amd.1); PMD: S1·B7, S1·B6) and Perde 4 (bir paketin hayatı — one 1518-byte Ethernet frame down and up through both seasons;
header / HEC / CRC values: bizim hesabımız, altın vektör değil)."""
from ep20_common import *


def lanes4(cx, cy, w=4.0, dy=0.5, x_lab=0.28):
    """Four upstream channel lanes (λ1…λ4, top → bottom) inside a panel centred at (cx, cy). Returns (VGroup, Y(k), x0, x1)."""
    x0, x1 = cx - w / 2 + 0.6, cx + w / 2 - 0.15
    Y = lambda k: cy + 0.75 - dy * k
    g = VGroup()
    for k in range(4):
        g.add(VGroup(Line([x0, Y(k), 0], [x1, Y(k), 0], color=CH[k], stroke_width=1.6, stroke_opacity=0.6),
                     T(f"λ{k + 1}", 14, CH[k], BOLD).move_to([cx - w / 2 + x_lab, Y(k), 0])))
    return g, Y, x0, x1


def blk(x0, x1, y, color, h=0.3, op=0.45, dashed=False):
    if dashed:
        return DashedVMobject(Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=1.8), num_dashes=16).move_to([(x0 + x1) / 2, y, 0])
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


# ================================ PERDE 3 ======================================
class E20P3A(Act20):
    HDR, MANIFEST, FIRST = H20[3], M20("p3"), True

    def construct(self):
        # d1 — §19 scope: rogue models tied to the multi-wavelength structure + coexistence with G-PON / XG-PON ONUs; no OLT–ONU interoperation specified;
        #      techniques → G-Sup.49 (not in our sources)
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Başıboş ONU ve acil durdurma")
        h = self.heading("§19 — kapsam")
        self.at(self.cue("On dokuzuncu madde", 1.8))
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        fr = frame_box("§19 · başıboş davranış ve hafifletilmesi", GOLD, 7.6, 2.5, 18).move_to([-2.45, 0.85, 0])
        ls = VGroup(chk("çok dalga boylu yapıya bağlı başıboşluk modelleri", True, 17),
                    chk("G-PON (G.984) · XG-PON (G.987) ONU'larıyla birlikte yaşama", True, 17),
                    chk("OLT ↔ ONU birlikte çalışma: tanımlanmaz", False, 17)).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        fit(ls, 7.0).move_to(fr[0]).shift(DOWN * 0.18)
        gs = doc_card("G-Sup.49 (2020)", ["başıboş ONU", "teknikleri"], WARN, 2.9, 1.4, 19, 16).move_to([4.6, 0.85, 0])
        ga = arrow(fr.get_right() + RIGHT * 0.1, gs.get_left() + LEFT * 0.1, WARN, 2.4, 0.13)
        gn = tag("kaynaklarımızda yok", WARN, 15).next_to(gs, DOWN, buff=0.15)
        q = self.quote("G.989.3 §19", "“This clause does not specify any interoperation between an OLT and an ONU.”",
                       "Bu madde OLT ile ONU arasında hiçbir birlikte çalışmayı tanımlamaz.", 12.0).move_to([0, -2.05, 0])
        self.play(FadeIn(fr), self.set_src("G.989.3 §19 giriş · Kaynakça [b-ITU-T G-sup.49]"), run_time=0.4)
        self.at(self.cue("çok dalga boylu yapıya", 3.3))
        self.play(FadeIn(ls[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("G-PON ile XG-PON", 6.5))
        self.play(FadeIn(ls[1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("ama OLT ile ONU arasında", 12.6))
        self.play(FadeIn(ls[2], shift=RIGHT * 0.05), FadeIn(q, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Teknikler için", 17.8))
        self.play(GrowArrow(ga), FadeIn(gs, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("o belge kaynaklarımızda", 22.6))
        self.play(FadeIn(gn, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # d2 — three models (§19.1) in time and wavelength: a) wrong time slot in its own channel → LOBi there; b) Tx hops to a wrong upstream channel → own CT
        #      LOBi, affected CTs interference; c) Tx tuned to a non-target channel → source and target miss it, an affected CT sees interference; PtP: b and c
        self.beat("d2")
        h = self.reset("Üç model — zaman ve dalga boyu", "std", 0.5, extra=[self.src_in("G.989.3 §19.1 · §19.2")])
        pans = VGroup()
        info = []
        for i, (ttl, c) in enumerate((("a · yanlış zaman dilimi", GOLD), ("b · yanlış ↑ kanal (atlama)", WARN), ("c · hedef olmayan kanal", PINK))):
            cx = -4.45 + 4.45 * i
            fr = RoundedRectangle(corner_radius=0.12, width=4.2, height=2.75, stroke_color=c, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([cx, 0.45, 0])
            tt = T(ttl, 16, c, BOLD).next_to(fr, UP, buff=0.08)
            ln, Y, x0, x1 = lanes4(cx, 0.3, 4.2, 0.52)
            tl = T("zaman →", 14, MUTED, BOLD).move_to([x1 - 0.45, Y(3) - 0.4, 0])
            pans.add(VGroup(fr, tt, ln, tl))
            info.append((Y, x0, x1, cx))
        # a
        Y, x0, x1, cx = info[0]
        a_ok = blk(x0 + 0.5, x0 + 1.7, Y(0), GOOD)
        a_bad = blk(x0 + 1.3, x0 + 2.5, Y(0), GOLD, op=0.6)
        a_x = T("✗", 18, WARN, BOLD).move_to([x0 + 1.5, Y(0) + 0.38, 0])
        a_l = VGroup(T("OLT (λ1):", 15, TXT, BOLD), T("LOBi", 16, DEFC, BOLD)).arrange(RIGHT, buff=0.1).move_to([cx, -1.35, 0])
        # b
        Y, x0, x1, cx = info[1]
        b_slot = blk(x0 + 0.8, x0 + 2.0, Y(0), WARN, dashed=True)
        b_hop = arrow([x0 + 1.4, Y(0) - 0.16, 0], [x0 + 1.4, Y(1) + 0.17, 0], WARN, 2.2, 0.1)
        b_ok = blk(x0 + 0.5, x0 + 1.6, Y(1), GOOD)
        b_bad = blk(x0 + 0.9, x0 + 2.1, Y(1), WARN, op=0.6)
        b_l = VGroup(VGroup(T("kendi CT (λ1):", 15, TXT, BOLD), T("LOBi", 16, DEFC, BOLD)).arrange(RIGHT, buff=0.1),
                     VGroup(T("etkilenen (λ2):", 15, TXT, BOLD), T("girişim", 16, WARN, BOLD)).arrange(RIGHT, buff=0.1)).arrange(DOWN, buff=0.06).move_to([cx, -1.5, 0])
        # c
        Y, x0, x1, cx = info[2]
        c_src = blk(x0 + 0.4, x0 + 1.4, Y(0), PINK, dashed=True)
        c_tgt = blk(x0 + 1.8, x0 + 2.8, Y(2), PINK, dashed=True)
        c_tl = T("hedef", 14, PINK, BOLD).next_to(c_tgt, UP, buff=0.04)
        c_ok = blk(x0 + 1.5, x0 + 2.6, Y(3), GOOD)
        c_bad = blk(x0 + 1.9, x0 + 3.0, Y(3), PINK, op=0.6)
        c_l = VGroup(VGroup(T("kaynak + hedef:", 15, TXT, BOLD), T("bulamaz", 16, PINK, BOLD)).arrange(RIGHT, buff=0.1),
                     VGroup(T("etkilenen (λ4):", 15, TXT, BOLD), T("girişim", 16, WARN, BOLD)).arrange(RIGHT, buff=0.1)).arrange(DOWN, buff=0.06).move_to([cx, -1.5, 0])
        ptp = VGroup(tag("PtP WDM · §19.2", PTPC, 16), T("yalnızca b ve c (zaman dilimi yok)", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.6, 0])
        self.play(FadeIn(pans[0]), run_time=0.4)
        self.at(self.cue("A modelinde", 1.3))
        self.play(FadeIn(a_ok), run_time=0.3)
        self.play(FadeIn(a_bad, shift=RIGHT * 0.2), FadeIn(a_x), run_time=0.45)
        self.at(self.cue("OLT o kanalda burst", 6.7))
        self.play(FadeIn(a_l, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("B modelinde", 9.4))
        self.play(FadeIn(pans[1]), FadeIn(b_ok), run_time=0.4)
        self.play(FadeIn(b_slot), GrowArrow(b_hop), FadeIn(b_bad, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.cue("kendi sonlandırıcısı burst", 15.0))
        self.play(FadeIn(b_l[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("etkilenenler girişim", 17.8))
        self.play(FadeIn(b_l[1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("C modelinde", 20.0))
        self.play(FadeIn(pans[2]), FadeIn(c_ok), FadeIn(c_src), FadeIn(c_tgt), FadeIn(c_tl), run_time=0.45)
        self.play(FadeIn(c_bad, shift=DOWN * 0.15), run_time=0.4)
        self.at(self.cue("kaynak da hedef de", 24.7))
        self.play(FadeIn(c_l[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("etkilenen bir sonlandırıcı", 27.3))
        self.play(FadeIn(c_l[1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("PtP WDM'de yalnızca", 30.8))
        self.play(FadeIn(ptp, shift=UP * 0.05), pans[0].animate.set_opacity(0.45), run_time=0.45)
        self.end(pad=0.05)

        # d3 — PMD bridge: b and c are wavelength-domain rogues (S1·B7): the optical tables must hold throughout tuning; US MSE ±20 GHz at 100 GHz spacing;
        #      a is S1·B6: Tx on/off within 128.6 ns, dark ≤ −62.6 dBm / 15 GHz
        self.beat("d3")
        h, chp = self.pmd_reset2("PMD Köprüsü — dalga boyu ve zaman", [s1chip(7, 16), s1chip(6, 16)])
        self.play(self.set_src("S1·B7 · S1·B6 · G.989.2 §9.3.7 · Tablo 11-7 · §11.1.5.2.9"), run_time=0.3)
        # left: wavelength domain
        fx0, fx1, fy = -6.2, -0.7, -0.55
        fax = Line([fx0, fy, 0], [fx1, fy, 0], color=MUTED, stroke_width=2)
        F = lambda g: -3.45 + g * 0.022      # GHz offset from the middle channel → x
        cs = [-100, 0, 100]
        ticks = VGroup(*[VGroup(Line([F(g), fy - 0.07, 0], [F(g), fy + 0.07, 0], color=MUTED, stroke_width=1.5),
                                T(f"{g:+d} GHz" if g else "0", 14, MUTED, BOLD).next_to([F(g), fy, 0], DOWN, buff=0.08)) for g in cs])
        lobes = VGroup(*[lobe(lambda v: F(v), g, fy, 1.3, 7, CH[i + 1], 0.25, 2.2) for i, g in enumerate(cs)])
        mse = Rectangle(width=F(20) - F(-20), height=1.55, stroke_width=0, fill_color=GOLD, fill_opacity=0.14).move_to([F(0), fy + 0.78, 0])
        msel = VGroup(Line([F(-20), fy + 1.62, 0], [F(20), fy + 1.62, 0], color=GOLD, stroke_width=2), T("± 20 GHz", 16, GOLD, BOLD).move_to([F(0), fy + 1.85, 0]))
        sp = brace_lbl(Line([F(0), fy - 0.5, 0], [F(100), fy - 0.5, 0]), "100 GHz aralık", MUTED, DOWN, 15)
        drift = arrow([F(26), fy + 1.1, 0], [F(74), fy + 1.1, 0], WARN, 2.6, 0.13)
        dl = VGroup(T("b / c:", 15, WARN, BOLD), T("komşu kanala", 15, WARN, BOLD)).arrange(DOWN, buff=0.03).move_to([F(50), fy + 0.6, 0])
        rq = VGroup(T("G.989.2 §9.3.7:", 15, S1C, BOLD), T("optik tablolar ayar boyunca sağlanmalı", 15, TXT, BOLD)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        rq.move_to([-6.2, -2.45, 0], aligned_edge=LEFT)
        # right: time domain (burst envelope)
        tx0, tx1 = 0.6, 6.4
        lo, hi = -1.35, 0.85
        env = VMobject(stroke_color=CH[1], stroke_width=3).set_points_as_corners([[tx0, lo, 0], [2.0, lo, 0], [2.6, hi, 0], [4.6, hi, 0], [5.2, lo, 0], [tx1, lo, 0]])
        dark = VGroup(DashedLine([tx0, lo - 0.05, 0], [tx1, lo - 0.05, 0], color=WARN, stroke_width=1.8, dash_length=0.08))
        dkl = T("karanlık: ≤ −62,6 dBm / 15 GHz", 16, WARN, BOLD).move_to([(tx0 + tx1) / 2, lo - 0.38, 0])
        on = brace_lbl(Line([2.0, hi + 0.15, 0], [2.6, hi + 0.15, 0]), "≤ 128,6 ns", GOLD, UP, 16)
        off = brace_lbl(Line([4.6, hi + 0.15, 0], [5.2, hi + 0.15, 0]), "≤ 128,6 ns", GOLD, UP, 16)
        bl = T("burst", 15, CH[1], BOLD).move_to([3.6, hi - 0.3, 0])
        ab = T("a: zaman alanında başıboşluk", 15, GOLD, BOLD).move_to([(tx0 + tx1) / 2, -2.45, 0])
        self.at(self.cue("yedinci bölümündeki dalga boyu", 1.6))
        self.play(Create(fax), FadeIn(ticks), LaggedStart(*[Create(l) for l in lobes], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("G.989.2 optik tabloların", 7.4))
        self.play(FadeIn(rq, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("tam da bunu önlemek", 10.6))
        self.play(GrowArrow(drift), FadeIn(dl), run_time=0.45)
        self.at(self.cue("yüz gigahertzlik aralıkta", 14.4))
        self.play(FadeIn(sp), FadeIn(mse), Create(msel[0]), FadeIn(msel[1]), run_time=0.5)
        self.at(self.cue("A ise birinci sezonun", 20.6))
        self.play(FadeIn(dark), FadeIn(ab), run_time=0.4)
        self.at(self.cue("verici en çok yüz yirmi", 24.0))
        self.play(Create(env), FadeIn(bl), run_time=0.8)
        self.play(FadeIn(on), FadeIn(off), run_time=0.4)
        self.at(self.cue("karanlıkken on beş", 29.8))
        self.play(FadeIn(dkl, shift=UP * 0.05), Indicate(dark, color=WARN), run_time=0.5)
        self.end(pad=0.05)

        # d4 — coexistence (§19.3): ONUs of an uncontrolled system that can transmit without a grant cause rogue events without being faulty; recommended:
        #      silent start on a new channel and at every re-initialization (= the Initialization state of Perde 1); isolating foreign devices may be impossible;
        #      nothing normative toward legacy ONUs — one recommendation, no procedure, parameter or message
        self.beat("d4")
        h = self.reset("Birlikte yaşama — §19.3", "std", 0.5, extra=[self.src_in("G.989.3 §19.3.1 · §19.3.2 · §19.3.3")])
        oc = ctu("NG-PON2 OLT CT", OLTC, False, 2.3, 0.5, 16).move_to([-5.15, 1.55, 0])
        lg = VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.08, width=2.3, height=0.62, stroke_color=LEGACY, stroke_width=2), num_dashes=30),
                    T("G-PON / XG-PON OLT", 15, MUTED, BOLD)).move_to([-5.15, 0.35, 0])
        lg[1].move_to(lg[0])
        lgl = T("bizim denetimimiz dışında", 14, MUTED, BOLD).next_to(lg, DOWN, buff=0.06)
        sp = splitter(0.26).move_to([-2.75, 0.95, 0])
        f1 = Line(oc.get_right(), sp.get_left() + UP * 0.06, color=FEED, stroke_width=2.5)
        f2 = DashedLine(lg.get_right(), sp.get_left() + DOWN * 0.06, color=LEGACY, stroke_width=2.2, dash_length=0.08)
        on1 = onu_box("ONU", ONUC, 0.95, 0.42, 15).move_to([-1.0, 1.65, 0])
        on2 = onu_box("ONU", ONUC, 0.95, 0.42, 15).move_to([-1.0, 0.95, 0])
        fo = sbox("G.984 · G.987 ONU", None, WARN, 2.1, 0.46, 15).move_to([-0.45, 0.2, 0])
        ds = VGroup(*[Line(sp.get_right(), m[0].get_left(), color=FEED, stroke_width=2) for m in (on1, on2, fo)])
        rb = arrow([fo[0].get_left()[0] - 0.05, 0.05, 0], [-2.55, 0.62, 0], WARN, 3, 0.14)
        rbl = T("izinsiz ↑", 15, WARN, BOLD).next_to(rb, DOWN, buff=0.02).shift(LEFT * 0.25)
        nf = VGroup(T("arızalı değil —", 16, TXT, BOLD), T("ama başıboşluk", 16, WARN, BOLD)).arrange(RIGHT, buff=0.1).move_to([-3.4, -0.75, 0])
        px = 3.75
        rh = VGroup(tag("önerilen · §19.3.2", GOLD, 15), T("sessiz başlangıç: yeni kanal + her yeniden başlatma", 16, TXT, BOLD)).arrange(DOWN, buff=0.08)
        fit(rh, 5.6).move_to([px, 1.75, 0])
        ib = VGroup(tbbox(1, 2.6, 0.78), VGroup(T("Tsstart ▶", 15, TMRC, BOLD), T("↑ duyulursa → koruma dalı", 14, STBC, BOLD)).arrange(DOWN, buff=0.04, aligned_edge=LEFT)).arrange(RIGHT, buff=0.2)
        fit(ib, 5.6).move_to([px, 0.65, 0])
        ibl = tag("Perde 1 · başlatma durumu", STBC, 14).next_to(ib, DOWN, buff=0.1)
        iso = VGroup(tag("§19.3.3", MUTED, 14), T("yabancıları yalıtmak zor ya da imkânsız", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(iso, 5.8).move_to([px, -0.65, 0])
        big = VGroup(T("Eski ONU'lara karşı normatif:", 19, TXT, BOLD), T("hiçbir şey", 21, WARN, BOLD)).arrange(RIGHT, buff=0.18).move_to([0, -1.7, 0])
        nn = VGroup(tag("tek kural: öneri", GOLD, 16), tag("prosedür ✗", WARN, 16), tag("parametre ✗", WARN, 16), tag("mesaj ✗", WARN, 16)).arrange(RIGHT, buff=0.18).move_to([0, -2.5, 0])
        self.play(FadeIn(oc), Create(f1), FadeIn(sp), Create(ds[:2]), FadeIn(on1), FadeIn(on2), run_time=0.6)
        self.at(self.cue("Kontrol edilmeyen bir sistemin", 1.3))
        self.play(FadeIn(lg), FadeIn(lgl), Create(f2), Create(ds[2]), FadeIn(fo), run_time=0.6)
        self.play(GrowArrow(rb), FadeIn(rbl), run_time=0.4)
        self.at(self.cue("arızalı olmasalar da", 6.8))
        self.play(FadeIn(nf, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Önerilen,", 10.5))
        self.play(FadeIn(rh[0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("her yeniden başlatmada sessiz", 11.2))
        self.play(FadeIn(rh[1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("birinci perdenin başlatma", 17.6))
        self.play(FadeIn(ib, shift=UP * 0.05), FadeIn(ibl), run_time=0.45)
        self.at(self.cue("Yabancıları yalıtmak", 21.2))
        self.play(FadeIn(iso, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Eski ONU'lara karşı normatif", 25.4))
        self.play(FadeIn(big, shift=UP * 0.05), run_time=0.45)
        for k, (key, d) in enumerate((("tek kural bir öneridir", 29.3), ("prosedür,", 31.2), ("parametre ya da", 32.0), ("ya da mesaj", 32.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(nn[k], shift=UP * 0.05), run_time=0.25)
        self.end(pad=0.1)
        self.save_timeline("ep20_p3A")


class E20P3B(Act20):
    HDR, MANIFEST, PREV_BADGE = H20[3], M20("p3"), "std"

    def construct(self):
        # d5 — §19.4, the only "shall": a non-AMCC signal in a quiet window is valid only with a valid PSBu; otherwise the CT may adjust its CDR to isolate it
        #      or report unexpected light; that event has no name, counter or threshold
        self.beat("d5")
        h = self.reset("Tek “shall” — §19.4 yabancı ışık", "std", 0.5, extra=[self.src_in("G.989.3 §19.4 (tam metin) · PSBu: S2·B2 · S1·B8")])
        q = self.quote("G.989.3 §19.4", "“… shall consider that signal valid only if the received PSBu structure is valid.”",
                       "Sessiz pencerede AMCC olmayan sinyal → ancak PSBu geçerliyse geçerli sayılır.", 12.0).move_to([0, 1.6, 0])
        y = -0.35
        qw = sbox("sessiz pencere", "kimse gönderemez", QWC, 2.3, 0.78, 17, 14).move_to([-5.2, y, 0])
        sg = sbox("AMCC olmayan", "sinyal", WARN, 2.1, 0.78, 17, 14).move_to([-2.45, y, 0])
        dm = VGroup(Square(1.0, stroke_color=GOLD, stroke_width=2.4, fill_color=PANEL, fill_opacity=1).rotate(PI / 4), T("PSBu\ngeçerli?", 15, GOLD, BOLD))
        dm[1].move_to(dm[0])
        dm.move_to([0.3, y, 0])
        a1 = arrow(qw[0].get_right(), sg[0].get_left(), MUTED, 2.2, 0.12)
        a2 = arrow(sg[0].get_right(), dm[0].get_left(), MUTED, 2.2, 0.12)
        yes = VGroup(arrow(dm[0].get_top(), [0.3, y + 1.1, 0], GOOD, 2.2, 0.12))
        yes.add(VGroup(T("evet →", 15, GOOD, BOLD), T("geçerli say", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.1).next_to(yes[0], RIGHT, buff=0.1).shift(UP * 0.18))
        nob = VGroup(sbox("CDR'yi ayarla", "sinyali yalıt · may", MUTED, 2.6, 0.72, 16, 14), sbox("beklenmeyen ışık", "raporla · may", MUTED, 2.6, 0.72, 16, 14)).arrange(DOWN, buff=0.18)
        nob.move_to([4.6, y - 0.35, 0])
        na = VGroup(arrow(dm[0].get_right(), nob[0][0].get_left(), WARN, 2.2, 0.12), arrow(dm[0].get_right(), nob[1][0].get_left(), WARN, 2.2, 0.12),
                    T("hayır", 15, WARN, BOLD).move_to([1.85, y + 0.3, 0]))
        nv = VGroup(T("bu olayın:", 17, MUTED, BOLD), tag("adı ✗", WARN, 16), tag("sayacı ✗", WARN, 16), tag("eşiği ✗", WARN, 16)).arrange(RIGHT, buff=0.18).move_to([0, -2.55, 0])
        self.at(self.cue("tek zorunlu cümlesi", 0.0))
        self.play(FadeIn(q[0]), run_time=0.4)
        self.at(self.cue("sessiz pencerede AMCC", 4.5))
        self.play(FadeIn(q[1:], shift=UP * 0.05), FadeIn(qw), GrowArrow(a1), FadeIn(sg), run_time=0.6)
        self.at(self.cue("ancak PSBu yapısı", 9.4))
        self.play(GrowArrow(a2), FadeIn(dm), run_time=0.4)
        self.play(GrowArrow(yes[0]), FadeIn(yes[1]), run_time=0.4)
        self.at(self.cue("Değilse saat ve veri", 13.8))
        self.play(GrowArrow(na[0]), FadeIn(na[2]), FadeIn(nob[0], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("beklenmeyen ışık rapor", 20.9))
        self.play(GrowArrow(na[1]), FadeIn(nob[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Bu olayın adı", 24.0))
        self.play(FadeIn(nv[:2], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("sayacı ve eşiği", 25.2))
        self.play(FadeIn(nv[2:], shift=UP * 0.05), run_time=0.3)
        self.end(pad=0.05)

        # d6 — §19.5 idle window: withhold every allocation (SN and ranging included) to catch mis-connected PtP modems that do not do silent start and
        #      usually transmit unconditionally; any power received = mis-connected transmitter; no duration, period, threshold or alarm name;
        #      our reading: the OLT keeps transmitting downstream, so a modem that waits for light is caught too
        self.beat("d6")
        h = self.reset("Boş pencere — §19.5", "std", 0.5, extra=[self.src_in("G.989.3 §19.5 · yorum: bizim")])
        x0, fw, n = -4.4, 1.05, 10
        X = lambda f: x0 + fw * f
        yd, yg, yp = 1.3, 0.45, -0.45
        labs = VGroup(side_lbl("↓ yayın", yd, GOLD, size=16), side_lbl("tahsisler", yg, ACC, size=16), side_lbl("↑ alınan güç", yp, OLTC, size=16))
        grants = VGroup()
        for f in list(range(0, 3)) + list(range(7, 10)):
            for j, (w_, c) in enumerate(((0.28, ACC), (0.2, SNC), (0.3, ACC))):
                grants.add(Rectangle(width=w_, height=0.34, stroke_width=0, fill_color=c, fill_opacity=0.65).move_to([X(f) + 0.18 + 0.33 * j, yg, 0]))
        win = Rectangle(width=X(7) - X(3), height=2.35, stroke_color=QWC, stroke_width=2, fill_color=QWC, fill_opacity=0.1).move_to([(X(3) + X(7)) / 2, (yd + yp) / 2 - 0.05, 0])
        wl = T("boş pencere: hiçbir tahsis yok", 16, QWC, BOLD).next_to(win, UP, buff=0.06)
        wl2 = T("seri numarası ve mesafe ölçümü dahil", 14, QWC, BOLD).move_to([(X(3) + X(7)) / 2, yg, 0])
        ax, _ = frame_axis(n, X(0), X(n), -1.05, True, 14, MUTED)
        ds = Rectangle(width=X(n) - X(0), height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([(X(0) + X(n)) / 2, yd, 0])
        md = VGroup(RoundedRectangle(corner_radius=0.08, width=1.9, height=0.62, stroke_color=PTPC, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                    T("PtP modem", 16, PTPC, BOLD)).move_to([-5.3, -1.9, 0])
        md[1].move_to(md[0])
        mdl = VGroup(T("yanlış bağlanmış", 15, TXT, BOLD), T("sessiz başlangıç yok", 15, MUTED, BOLD), T("genellikle koşulsuz gönderir", 15, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        mdl.next_to(md, RIGHT, buff=0.2)
        pw = Rectangle(width=X(6.6) - X(3.4), height=0.34, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.5).move_to([(X(3.4) + X(6.6)) / 2, yp, 0])
        pwl = T("her güç = yanlış bağlanmış verici", 15, WARN, BOLD).move_to([(X(3) + X(7)) / 2, 0.0, 0])
        nv = VGroup(*[tag(s, WARN, 15) for s in ("süre ✗", "sıklık ✗", "eşik ✗", "alarm adı ✗")]).arrange(RIGHT, buff=0.12).move_to([3.3, -1.95, 0])
        ip = VGroup(ytag("bizim yorumumuz"), T("OLT ↓ yayını sürer → ışık bekleyen modem de yakalanır", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(ip, 12.6).move_to([0, -2.85, 0])
        self.play(FadeIn(labs), FadeIn(ax), run_time=0.4)
        self.at(self.cue("Sonlandırıcı bütün tahsisleri", 1.0))
        self.play(LaggedStart(*[FadeIn(g) for g in grants], lag_ratio=0.02), run_time=0.6)
        self.at(self.cue("seri numarası ve mesafe", 3.5))
        self.play(FadeIn(win), FadeIn(wl), FadeIn(wl2), run_time=0.45)
        self.at(self.cue("fibere yanlış bağlanmış", 9.6))
        self.play(FadeIn(md, shift=UP * 0.05), FadeIn(mdl[0]), run_time=0.4)
        self.at(self.cue("sessiz başlamayı bilmeyen", 11.6))
        self.play(FadeIn(mdl[1]), run_time=0.3)
        self.at(self.cue("genellikle koşulsuz", 17.2))
        self.play(FadeIn(mdl[2]), run_time=0.3)
        self.at(self.cue("Pencerede alınan her güç", 19.9))
        self.play(GrowFromEdge(pw, LEFT), FadeIn(pwl, shift=UP * 0.05), run_time=0.5)
        for k, (key, d) in enumerate((("Süre,", 25.0), ("sıklık,", 25.5), ("eşik ve alarm", 26.1), ("alarm adı yoktur", 26.9))):
            self.at(self.cue(key, d))
            self.play(FadeIn(nv[k], shift=UP * 0.05), run_time=0.2)
        self.at(self.cue("Bizim yorumumuz", 28.2))
        self.play(FadeIn(ip[0]), GrowFromEdge(ds, LEFT), run_time=0.5)
        self.at(self.cue("ışık bekleyen modem", 29.5))
        self.play(FadeIn(ip[1], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # d7 — §12 tools (EqD readjustment, ONU-ID deactivation, SN disabling); extreme case: disable all in the channel, re-enable conformant ONUs one by one;
        #      octet 5 of the broadcast Disable_Serial_Number: 0xFF / 0x00 one SN off / on, 0x0F / 0xF0 everyone off / on, 0x3F only ONUs in O2-3 off
        self.beat("d7")
        h = self.reset("Asıl araçlar — §12.1.5 · Disable_Serial_Number", "std", 0.5, extra=[self.src_in("G.989.3 §12.1.5 · Tablo 11-9 · Tablo 11-2 · Tablo 12-3")])
        tools = VGroup(mtile(0x04, "Ranging_Time · EqD yeniden ayarı", "kim", 4.05, 0.44, 15), mtile(0x05, "Deactivate_ONU-ID · kimlik iptali", "dis", 4.05, 0.44, 15),
                       mtile(0x06, "Disable_Serial_Number · SN kapat", "dis", 4.05, 0.44, 15)).arrange(RIGHT, buff=0.12).move_to([0, 1.85, 0])
        ext = VGroup(tag("uç durum", WARN, 15), T("kanaldaki herkesi kapat → uyumluları tek tek aç", 15, TXT, BOLD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        ext.move_to([-6.35, 1.0, 0], aligned_edge=LEFT)
        ob = VGroup(*[onu_box(f"ONU {k + 1}", ONUC, 1.05, 0.44, 15) for k in range(4)]).arrange(DOWN, buff=0.14).move_to([-5.0, -0.75, 0])
        onus = VGroup(*[VGroup(b, txlamp(True, 0.08).next_to(b, RIGHT, buff=0.18)) for b in ob])
        st1 = VGroup(HX("0x0F", 16, WARN, BOLD), T("hepsi kapalı", 15, WARN, BOLD)).arrange(RIGHT, buff=0.1).next_to(onus, RIGHT, buff=0.3).shift(UP * 0.35)
        st2 = VGroup(HX("0x00 + SN", 16, GOOD, BOLD), T("tek tek", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.1).next_to(onus, RIGHT, buff=0.3).shift(DOWN * 0.35)
        rows = [["0xFF", "bu seri numarası → kapalı (O7)"], ["0x00", "bu seri numarası → açık"], ["0x0F", "kanaldaki bütün ONU'lar → kapalı"],
                ["0xF0", "kanaldaki bütün ONU'lar → açık"], ["0x3F", "yalnızca O2-3'tekiler → kapalı (Disable_Discovery)"]]
        tb = mtable(["oktet 5", "seçenek"], rows, [1.35, 5.2], size=16, hsize=15, row_h=0.46, mono=(0,)).move_to([2.95, -0.45, 0])
        for r in tb[1:]:
            r[1].set_color(GOOD if r[1].text in ("0x00", "0xF0") else WARN)
        cap = T("yayın · ONU-ID 0x03FF · oktet 5 = seçenek", 15, MUTED, BOLD).next_to(tb, DOWN, buff=0.12)
        self.at(self.cue("gecikmeyi yeniden ayarlamak", 2.9))
        self.play(FadeIn(tools[0], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("ONU kimliğini iptal", 5.2))
        self.play(FadeIn(tools[1], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("seri numarasını devre dışı", 7.4))
        self.play(FadeIn(tools[2], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Uç durumda sonlandırıcı", 10.4))
        self.play(FadeIn(ext, shift=RIGHT * 0.05), FadeIn(onus), run_time=0.45)
        self.play(*[Transform(o[1], txlamp(False, 0.08).move_to(o[1])) for o in onus], FadeIn(st1, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("uyumluları tek tek", 14.6))
        self.play(FadeIn(st2, shift=LEFT * 0.05), run_time=0.3)
        for k in (0, 1, 3):
            self.play(Transform(onus[k][1], txlamp(True, 0.08).move_to(onus[k][1])), run_time=0.25)
        self.at(self.cue("beşinci baytı seçeneği", 17.6))
        self.play(FadeIn(tb[0]), FadeIn(cap), *[FadeIn(r[0]) for r in tb[1:]], run_time=0.4)
        for k, (key, d) in enumerate((("ef ef bir seri", 21.4), ("sıfır sıfır açar", 24.2), ("sıfır ef kanaldaki", 25.6), ("ef sıfır açar", 28.6), ("üç ef yalnızca", 29.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(tb[k + 1][1:], shift=RIGHT * 0.05), run_time=0.3)
        self.end(pad=0.05)
        self.save_timeline("ep20_p3B")


class E20P3C(Act20):
    HDR, MANIFEST, PREV_BADGE = H20[3], M20("p3"), "std"

    def construct(self):
        # d8 — Amd.2 Reason Code in octets 14–15 (0x0000 = not specified; suggested values in G-Sup.84; the ONU only logs it); a disabled ONU switches its laser
        #      off → O7: keeps DS sync and parses PLOAM, but neither forwards nor transmits; persists over power cycles; Enable must go out on every channel
        self.beat("d8")
        h = self.reset("Disable_Serial_Number (Amd.2) ve O7", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 11-9 (Amd.2) · Tablo 11-2 · Tablo 12-1 (O7) · 12-4")])
        mt = VGroup(mtile(0x06, "Disable_Serial_Number ↓", "dis", 4.0, 0.44, 16), tag("MIC: varsayılan PLOAM anahtarı", DKC, 15)).arrange(RIGHT, buff=0.3)
        mt.move_to([-6.4, 2.0, 0], aligned_edge=LEFT)
        spec = [("ONU-ID", 1.25, OIDC, "1–2"), ("0x06", 0.8, TYC, "3"), ("SeqNo", 0.95, SQC, "4"), ("seçenek", 1.15, WARN, "5"), ("Vendor_ID", 1.6, ONUC, "6–9"),
                ("VSSN", 1.6, ONUC, "10–13"), ("neden kodu", 1.7, AMDC, "14–15"), ("dolgu", 1.9, MUTED, "16–40"), ("MIC", 1.35, MICC, "41–48")]
        oc = octets(spec, 12.6, 0.56, 15, 14).move_to([0, 1.2, 0])
        amd = tag("Amd.2", AMDC, 14).next_to(oc[6], UP, buff=0.08)
        rc = VGroup(HX("0x0000", 16, AMDC, BOLD), T("= belirtilmemiş", 15, TXT, BOLD), T("· önerilen değerler:", 15, MUTED, BOLD), tag("G-Sup.84 · kaynaklarda yok", WARN, 14),
                    T("· ONU yalnızca kaydeder", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.12)
        fit(rc, 12.6).move_to([0, 0.3, 0])
        o7 = sbox("O7", "acil durdurma", ESC, 1.9, 0.78, 22, 15).move_to([-5.3, -1.05, 0])
        lz = laser(False, ESC, 0.36).next_to(o7, UP, buff=0.12)
        lzl = T("lazer kapalı", 14, ESC, BOLD).next_to(lz, RIGHT, buff=0.12)
        props = VGroup(chk("↓ senkron sürer", True, 16), chk("PLOAM okunur", True, 16), chk("veri iletmez", False, 16), chk("↑ göndermez", False, 16))
        VGroup(VGroup(*props[:2]).arrange(DOWN, aligned_edge=LEFT, buff=0.12), VGroup(*props[2:]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(RIGHT, buff=0.45)
        props.move_to([-1.55, -1.05, 0])
        pc = VGroup(Arc(radius=0.3, start_angle=PI / 2, angle=-1.6 * PI, color=WARN, stroke_width=3).add_tip(tip_length=0.12), T("güç kesintisini aşar", 16, WARN, BOLD))
        pc.arrange(RIGHT, buff=0.15).move_to([4.2, -0.9, 0])
        en = VGroup(T("açma (0x00 / 0xF0):", 16, GOOD, BOLD), *[VGroup(tile(f"λ{k + 1}", CH[k], 0.6, 0.38, 15, 0.25), T("✓", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.04) for k in range(4)],
                    T("bütün kanallarda", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0.8, -2.45, 0])
        self.play(FadeIn(mt, shift=RIGHT * 0.05), LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in oc], lag_ratio=0.06), run_time=0.8)
        self.play(FadeIn(amd), Indicate(oc[6], color=AMDC, scale_factor=1.05), run_time=0.5)
        self.at(self.cue("belirtilmemişse sıfır", 6.3))
        self.play(FadeIn(rc[:2], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("seksen dördüncü ekinde", 8.1))
        self.play(FadeIn(rc[2:4], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("ONU yalnızca kaydeder", 12.6))
        self.play(FadeIn(rc[4], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("lazerini söndürür", 14.4))
        self.play(FadeIn(lz), FadeIn(lzl), run_time=0.35)
        self.at(self.cue("acil durdurmaya geçer", 17.9))
        self.play(FadeIn(o7, scale=0.9), run_time=0.35)
        self.at(self.cue("senkronu ve PLOAM okumayı", 19.7))
        self.play(FadeIn(props[:2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("ne veri iletir ne gönderir", 22.6))
        self.play(FadeIn(props[2:], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("güç kesintisini aşar", 25.2))
        self.play(FadeIn(pc, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("bütün kanallarda gönderilmelidir", 27.8))
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.05) for e in en], lag_ratio=0.12), run_time=0.7)
        self.end(pad=0.05)

        # d9 — Appendix XI (Amd.1): two substates invisible to the OLT — O7.1 In-Sync, O7.2 Off-Sync; a rebooted ONU wakes in O7.2 and dwells Tseek per channel:
        #      likely channels first (protection, Tuning_Request target), then round-robin; Tseek may double each round up to ≈ 1 min; no initial value;
        #      our reading: an 8-channel round may approach 8 minutes
        self.beat("d9")
        h = self.reset("Ek XI — O7.1 ve O7.2", "std", 0.5, extra=[self.src_in("G.989.3 Amd.1 Ek XI · Şekil XI.1 · Tablo XI.1 · G.989.2 Tablo 11-2 (8 kanal)")])
        frm = DashedVMobject(RoundedRectangle(corner_radius=0.18, width=5.7, height=2.35, stroke_color=ESC, stroke_width=2), num_dashes=60).move_to([-3.4, 0.3, 0])
        frl = T("O7 · acil durdurma", 16, ESC, BOLD).move_to([-3.4, frm.get_top()[1] + 0.2, 0])
        s1 = sbox("O7.1", "senkronlu", ESC, 2.05, 0.78, 20, 15).move_to([-4.85, 0.3, 0])
        s2 = sbox("O7.2", "senkronsuz", ESC, 2.05, 0.78, 20, 15).move_to([-1.95, 0.3, 0])
        e12 = VGroup(arrow(s1[0].get_right() + UP * 0.17, s2[0].get_left() + UP * 0.17, WARN, 2.2, 0.12), T("LODS", 14, WARN, BOLD).move_to([-3.4, 0.68, 0]))
        e21 = VGroup(arrow(s2[0].get_left() + DOWN * 0.17, s1[0].get_right() + DOWN * 0.17, GOOD, 2.2, 0.12), T("DSYNC", 14, GOOD, BOLD).move_to([-3.4, -0.08, 0]))
        inv = tag("OLT'ye görünmez", MUTED, 14).move_to([-3.4, -0.55, 0])
        dis = VGroup(T("her durumdan · Disable SN", 14, ESC, BOLD), arrow([-4.85, 2.0, 0], [-4.85, 0.72, 0], ESC, 2.2, 0.12))
        dis[0].next_to(dis[1], UP, buff=0.04).shift(RIGHT * 0.3)
        rb = VGroup(T("yeniden başlatma", 14, TMRC, BOLD), arrow([-1.95, 2.0, 0], [-1.95, 0.72, 0], TMRC, 2.2, 0.12))
        rb[0].next_to(rb[1], UP, buff=0.04)
        en = VGroup(arrow(s1[0].get_bottom(), [-4.85, -1.55, 0], GOOD, 2.2, 0.12), T("Enable SN → O1", 14, GOOD, BOLD).move_to([-3.75, -1.3, 0]))
        x0 = 0.55
        pr = VGroup(tile("koruma", GOOD, 1.0, 0.4, 15, 0.3), tile("hedef", GOLD, 0.9, 0.4, 15, 0.3)).arrange(RIGHT, buff=0.08)
        rr = VGroup(*[tile(f"λ{k + 1}", MUTED, 0.5, 0.4, 14, 0.15) for k in range(8)]).arrange(RIGHT, buff=0.05)
        pr.move_to([x0, 2.0, 0], aligned_edge=LEFT)
        rr.move_to([x0 + 0.35, 1.38, 0], aligned_edge=LEFT)
        scan = VGroup(pr, T("↓", 16, MUTED, BOLD).move_to([x0 + 0.15, 1.38, 0]), rr)
        pl = T("önce olası kanallar", 14, GOOD, BOLD).next_to(pr, RIGHT, buff=0.2)
        rl = T("sonra sırayla hepsi (round-robin)", 14, MUTED, BOLD).next_to(rr, DOWN, buff=0.08).align_to(rr, LEFT)
        yb = -2.05
        bars = VGroup()
        hs = [0.15, 0.3, 0.6, 1.2, 1.9, 1.9]
        for k, hh in enumerate(hs):
            r = Rectangle(width=0.62, height=hh, stroke_color=TMRC, stroke_width=1.6, fill_color=TMRC, fill_opacity=0.4).move_to([x0 + 0.45 + 0.85 * k, yb + hh / 2, 0])
            bars.add(VGroup(r, T(["Tseek", "×2", "×4", "×8", "…", "…"][k], 14, TXT, BOLD).next_to(r, DOWN, buff=0.06)))
        cap = VGroup(DashedLine([x0 + 0.05, yb + 1.9, 0], [x0 + 5.15, yb + 1.9, 0], color=GOLD, stroke_width=2), T("≈ 1 dk", 16, GOLD, BOLD).move_to([x0 + 5.65, yb + 1.9, 0]))
        bl = T("tur başına Tseek", 14, TMRC, BOLD).move_to([x0 + 2.6, yb + 2.2, 0])
        nv = tag("başlangıç değeri yok", WARN, 14).move_to([x0 + 1.0, yb + 1.25, 0])
        ip = VGroup(ytag("bizim yorumumuz"), T("8 kanal × ≈ 1 dk ≈ 8 dk / tur", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([-3.4, -2.6, 0])
        self.at(self.cue("OLT'ye görünmeyen", 3.0))
        self.play(Create(frm), FadeIn(frl), FadeIn(inv), run_time=0.5)
        self.at(self.cue("O7.1 senkronlu", 6.5))
        self.play(FadeIn(s1), GrowArrow(dis[1]), FadeIn(dis[0]), run_time=0.4)
        self.at(self.cue("O7.2 senkronsuz", 7.8))
        self.play(FadeIn(s2), GrowArrow(e12[0]), FadeIn(e12[1]), GrowArrow(e21[0]), FadeIn(e21[1]), run_time=0.45)
        self.play(GrowArrow(en[0]), FadeIn(en[1]), run_time=0.35)
        self.at(self.cue("Yeniden başlayan ONU", 9.1))
        self.play(GrowArrow(rb[1]), FadeIn(rb[0]), Indicate(s2, color=TMRC, scale_factor=1.05), run_time=0.5)
        self.at(self.cue("her kanalda bir arama", 12.1))
        self.play(FadeIn(bars[0]), FadeIn(bl), run_time=0.35)
        self.at(self.cue("önce koruma kanalı", 15.2))
        self.play(FadeIn(pr, shift=RIGHT * 0.05), FadeIn(pl), run_time=0.35)
        self.at(self.cue("sonra sırayla hepsi", 18.5))
        self.play(LaggedStart(*[FadeIn(r) for r in rr], lag_ratio=0.08), FadeIn(scan[1]), FadeIn(rl), run_time=0.6)
        self.at(self.cue("her turda ikiye", 21.6))
        self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars[1:4]], lag_ratio=0.2), *[FadeIn(b[1]) for b in bars[1:4]], run_time=0.6)
        self.at(self.cue("yaklaşık bir dakikaya", 24.5))
        self.play(*[GrowFromEdge(b[0], DOWN) for b in bars[4:]], *[FadeIn(b[1]) for b in bars[4:]], Create(cap[0]), FadeIn(cap[1]), run_time=0.5)
        self.at(self.cue("başlangıç değeri yoktur", 27.4))
        self.play(FadeIn(nv, shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("sekiz kanallık bir tur", 29.4))
        self.play(FadeIn(ip, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        self.note11("d10", [("1", "Acil durdurma yapışkan, kanala yerel ve kimlik doğrulamasızdır",
                             "Güç kesintisini aşar · açma bütün kanallarda gönderilmeli ·\nmesaj herkesçe bilinen varsayılan anahtarla imzalanır →\nbizim yorumumuzla sahte bir 0x0F kanalı susturur.", "acil durdurma yapışkandır"),
                            ("2", "Devre dışı bırakma başarısızlığını (DFi) görmek için",
                             "O ONU'ya tahsis vermeyi sürdürün: yoksa kapatmayı yok sayan ONU görünmez kalır.", "İki:")])
        self.bridge_beat("d11", "Sistemi korumanın bütün yollarını gördük.\nŞimdi sezonun son hikâyesi: bir paketin hayatı.")
        self.save_timeline("ep20_p3C")


# ================================ PERDE 4 ======================================
LAY = [("Ethernet", "SNI · UNI", GOOD), ("XGEM", "kapsülleme · AES", SAC), ("FS çerçeve", "BWmap · burst", BWC),
       ("PHY", "FEC · karıştırma · PSB", PSC), ("PMD", "ışık", CH[1])]


class Stack:
    """Two layer stacks (OLT CT left, ONU right) joined by the ODN, a packet marker on the inner side of the active layer and a highlight frame.
    Keep `all`, `pkt`, `hl` on stage with reset_keep; move with `go(side, layer)`; `fib` is the fibre path (OLT PMD → ONU PMD)."""

    def __init__(self, xo=-5.6, xn=5.6, w=2.25, top=1.7, dy=0.84, h=0.62):
        self.xo, self.xn, self.top, self.dy, self.w = xo, xn, top, dy, w
        self.cols = {}
        g = VGroup()
        for side, x, name, c in (("o", xo, "OLT CT", OLTC), ("n", xn, "ONU", ONUC)):
            col = VGroup()
            for i, (a, b, cc) in enumerate(LAY):
                r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=cc, stroke_width=2, fill_color=cc, fill_opacity=0.1).move_to([x, top - i * dy, 0])
                t = VGroup(T(a, 16, TXT, BOLD), T(b, 14, cc, BOLD)).arrange(DOWN, buff=0.03)
                fit(t, w - 0.15).move_to(r)
                col.add(VGroup(r, t))
            self.cols[side] = col
            g.add(col, T(name, 17, c, BOLD).next_to(col, UP, buff=0.12))
        yb, yf = top - 4 * dy - h / 2, -3.0
        self.fib = VMobject(stroke_color=FEED, stroke_width=3).set_points_as_corners([[xo, yb, 0], [xo, yf, 0], [xn, yf, 0], [xn, yb, 0]])
        g.add(self.fib, T("ODN · N1 · 20 km", 14, MUTED, BOLD).move_to([2.9, yf - 0.2, 0]))
        self.all = g
        self.pkt = RoundedRectangle(corner_radius=0.06, width=0.34, height=0.26, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.9)
        self.hl = SurroundingRectangle(self.cols["o"][0][0], color=GOLD, buff=0.05, stroke_width=3.5, corner_radius=0.1)

    def pos(self, side, i):
        x = self.xo + self.w / 2 + 0.22 if side == "o" else self.xn - self.w / 2 - 0.22
        return np.array([x, self.top - i * self.dy, 0])

    def place(self, side, i):
        self.pkt.move_to(self.pos(side, i))
        self.hl.move_to(self.cols[side][i][0].get_center())
        return self

    def go(self, side, i):
        return [self.pkt.animate.move_to(self.pos(side, i)), self.hl.animate.move_to(self.cols[side][i][0].get_center())]

    def keep(self):
        return [self.all, self.pkt, self.hl]


def chipz(*names):
    """Small season tags 'S2·B3', 'S1·B4' … (S1 violet, S2 accent)."""
    return VGroup(*[tag(n, S1C if n.startswith("S1") else ACC, 15) for n in names]).arrange(RIGHT, buff=0.1)


def kvrow(k, v, y, x0=-3.9, xv=-1.35, ksize=16, vsize=18, vcolor=TXT, mono=False):
    a = T(k, ksize, MUTED, BOLD).move_to([x0, y, 0], aligned_edge=LEFT)
    b = (HX(v, vsize - 1, vcolor, BOLD) if mono else T(v, vsize, vcolor, BOLD)).move_to([xv, y, 0], aligned_edge=LEFT)
    return VGroup(a, b)


def vals(cells, vs, y, color=GOLD, size=15):
    """Value labels centred under field cells."""
    return VGroup(*[HX(v, size, color, BOLD).move_to([c[0].get_x(), y, 0]) for c, v in zip(cells, vs)])


class P4Act(Act20):
    def stage(self, side, i, extra=()):
        """Fresh scene: build the stack with the packet already at (side, i)."""
        self.stk = Stack().place(side, i)
        self.play(FadeIn(self.stk.all), FadeIn(self.stk.pkt), FadeIn(self.stk.hl), *extra, run_time=0.6)

    def step(self, title, chips, badge="std", src=None):
        """Heading + season chips at its right, keeping the stack."""
        ex = [self.src_in(src)] if src else []
        h = self.reset_keep(title, badge, self.stk.keep(), 0.5, w=6.6, extra=ex)
        ch = self.chips_at([chipz(*chips)], h)
        self.play(FadeIn(ch, shift=LEFT * 0.1), run_time=0.3)
        return h, ch


class E20P4A(P4Act):
    HDR, MANIFEST, FIRST = H20[4], M20("p4"), True

    def construct(self):
        # e1 — one 1518-byte Ethernet frame through every layer; our configuration: channel pair 1, 10G/10G, FEC on, N1, 20 km, ONU-ID 5, Alloc-ID = Port 1024;
        #      header and HEC values are ours, not golden vectors
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Bir paketin hayatı")
        h = self.heading("Yapılandırma — bizim seçimimiz")
        self.at(self.cue("Bin beş yüz on sekiz", 2.5))
        self.stk = Stack().place("o", 0)
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        self.play(FadeIn(self.stk.all), self.set_src("G.989.3 §8 · §9 · §13 · G.989.2 Tablo 11-1 · 11-5 · 11-7 · hesaplar: bizim (S2·B10 calc)"), run_time=0.7)
        eb = VGroup(Rectangle(width=6.2, height=0.48, stroke_color=GOOD, stroke_width=2, fill_color=GOOD, fill_opacity=0.25),
                    T("Ethernet çerçevesi · DA … FCS · 1518 B", 17, TXT, BOLD)).move_to([0, 1.95, 0])
        eb[1].move_to(eb[0])
        rows = VGroup(kvrow("kanal çifti", "TWDM 1 · ↓ 187,8 THz", 1.15), kvrow("hız", "9,95328 / 9,95328 Gbit/s", 0.6),
                      kvrow("FEC", "açık · ↓ ve ↑", 0.05), kvrow("ODN", "N1 · 14–29 dB · 20 km (DD20)", -0.5),
                      kvrow("ONU-ID", "5", -1.05), kvrow("Alloc-ID · Port-ID", "1024 (0x400)", -1.6))
        gv = VGroup(ytag("bizim hesabımız"), T("başlık · HEC · CRC değerleri — altın vektör değil", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        fit(gv, 7.9).move_to([0, -2.4, 0])
        self.play(FadeIn(eb, shift=DOWN * 0.05), FadeIn(self.stk.pkt, scale=1.5), FadeIn(self.stk.hl), run_time=0.5)
        self.at(self.cue("Yapılandırma bizim seçimimiz", 9.3))
        self.play(Indicate(h, color=GOLD, scale_factor=1.03), run_time=0.5)
        for k, (key, d) in enumerate((("birinci kanal çifti", 11.8), ("iki yönde on gigabit", 13.5), ("FEC açık", 15.3), ("N1 sınıfı", 16.0),
                                      ("ONU kimliği beş", 18.2), ("tahsis kimliği ve port", 19.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("Başlık ve hata denetimi", 22.8))
        self.play(FadeIn(gv[0]), run_time=0.3)
        self.at(self.cue("altın vektör değildirler", 27.1))
        self.play(FadeIn(gv[1], shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # e2 — downstream: preamble + SFD dropped, FCS kept (S2·B3); Port 1024 (S2·B1); payload rounded to a multiple of 4: 1520 B, 2 pad bytes; AES-CTR (S2·B8)
        #      covers the payload only — 95 counter blocks; the 8-byte header 0x17B9 0400 0000 20A7 (our HEC)
        self.beat("e2")
        h, ch = self.step("↓ Ethernet → XGEM", ["S2·B3", "S2·B1", "S2·B8"], src="G.989.3 §9.1.2–9.1.3 (9-1) · §9.4.1 · §15.4.3 · Ek A · başlık: bizim hesabımız")
        x0 = -3.9
        pre = VGroup(Rectangle(width=1.25, height=0.42, stroke_color=WARN, stroke_width=1.8, fill_color=WARN, fill_opacity=0.15).move_to([x0 + 0.625, 1.95, 0]),
                     T("önsöz+SFD", 14, WARN, BOLD).move_to([x0 + 0.625, 1.95, 0]))
        prx = strike(pre[0], WARN, 3)
        efr = VGroup(Rectangle(width=6.45, height=0.42, stroke_color=GOOD, stroke_width=1.8, fill_color=GOOD, fill_opacity=0.25).move_to([x0 + 1.25 + 3.225, 1.95, 0]),
                     T("DA … veri … FCS · 1518 B", 15, TXT, BOLD).move_to([x0 + 1.25 + 3.225, 1.95, 0]))
        fcs = T("FCS kalır", 14, GOOD, BOLD).next_to(efr[0], DOWN, buff=0.05).align_to(efr[0], RIGHT)
        port = VGroup(T("sınıflandır →", 15, MUTED, BOLD), tag("XGEM Port-ID 0x0400 = 1024", PIDC, 15)).arrange(RIGHT, buff=0.12).move_to([x0, 1.2, 0], aligned_edge=LEFT)
        yx = 0.4
        xh = Rectangle(width=0.8, height=0.46, stroke_color=SAC, stroke_width=2, fill_color=SAC, fill_opacity=0.55).move_to([x0 + 0.4, yx, 0])
        xhl = T("8 B", 14, BG, BOLD).move_to(xh)
        xp = Rectangle(width=5.6, height=0.46, stroke_color=SAC, stroke_width=2, fill_color=SAC, fill_opacity=0.15).move_to([x0 + 0.8 + 2.8, yx, 0])
        xpl = T("yük 1518 B", 15, TXT, BOLD).move_to(xp)
        xd = Rectangle(width=0.55, height=0.46, stroke_color=PADC, stroke_width=2, fill_color=PADC, fill_opacity=0.45).move_to([x0 + 6.4 + 0.275, yx, 0])
        xdl = T("+2", 14, TXT, BOLD).move_to(xd)
        tot = T("= 1528 B", 15, SAC, BOLD).next_to(xd, RIGHT, buff=0.1)
        p4 = VGroup(T("P = 4·⌈1518/4⌉ = 1520 B", 15, PADC, BOLD), T("· 2 dolgu baytı 0x55", 15, PADC, BOLD)).arrange(RIGHT, buff=0.1).next_to(xp, UP, buff=0.06).align_to(xp, RIGHT)
        aes = brace_lbl(VGroup(xp, xd), "AES-CTR: yalnızca yük · 1520 / 16 = 95 sayaç bloğu", PINK, DOWN, 15)
        hcl = VGroup(lock(MUTED, 0.2, opened=True), T("başlık açık", 14, MUTED, BOLD)).arrange(RIGHT, buff=0.06).next_to(xh, DOWN, buff=0.12)
        yh = -1.3
        fx = fields(XH, 7.8, 0.46, 15, 14, show_w=False, lpos=UP).move_to([0, yh, 0])
        fv = vals(fx, ["1518", "01", "0x0400", "0", "1", "0x0A7"], yh - 0.42)
        hx = VGroup(*[HX(s, 22, GOLD, BOLD) for s in ("0x17B9", "0400", "0000", "20A7")]).arrange(RIGHT, buff=0.22).move_to([-0.6, -2.3, 0])
        hxt = ytag("bizim hesabımız").next_to(hx, RIGHT, buff=0.25)
        self.play(FadeIn(pre), FadeIn(efr), run_time=0.4)
        self.at(self.cue("önsöz atılır", 0.8))
        self.play(Create(prx), pre.animate.set_opacity(0.4), run_time=0.4)
        self.at(self.cue("denetim dizisi kalır", 4.9))
        self.play(FadeIn(fcs, shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("birinci bölümün kimlikleriyle", 7.4))
        self.play(FadeIn(port, shift=RIGHT * 0.05), *self.stk.go("o", 1), run_time=0.5)
        self.at(self.cue("Yük dördün katına", 12.2))
        self.play(FadeIn(xh), FadeIn(xhl), FadeIn(xp), FadeIn(xpl), run_time=0.4)
        self.at(self.cue("bin beş yüz yirmi bayt", 14.7))
        self.play(FadeIn(p4[0], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("iki dolgu baytı", 16.6))
        self.play(FadeIn(xd), FadeIn(xdl), FadeIn(tot), FadeIn(p4[1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("AES-CTR şifrelemesi", 17.9))
        self.play(FadeIn(aes, shift=UP * 0.05), FadeIn(hcl), xp.animate.set_fill(PINK, 0.25), run_time=0.45)
        self.at(self.cue("Sekiz baytlık başlık", 25.0))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in fx], lag_ratio=0.08), FadeIn(fv), run_time=0.7)
        for k, (key, d) in enumerate((("bir yedi be dokuz", 26.8), ("sıfır dört sıfır sıfır", 31.4), ("dört sıfır,", 33.4), ("iki sıfır a yedi", 34.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(hx[k], shift=UP * 0.05), *([FadeIn(hxt)] if k == 0 else []), run_time=0.25)
        self.end(pad=0.05)

        # e3 — 10G FEC-on FS payload ≤ 135 424 B: 88 whole frames fit, the 89th is fragmented (our arithmetic); HLend, BWmap, PLOAMs in front, BIP-32 behind
        #      (S2·B4, S2·B5); then S2·B2's steps tied to S1·B4: Reed-Solomon, scrambling, PSBd; our frame takes 1.41 µs on the line
        self.beat("e3")
        h, ch = self.step("↓ FS çerçevesi ve PHY", ["S2·B4", "S2·B5", "S2·B2", "S1·B4"], src="G.989.3 §8.1.1 · §9.3 · §10.1.1–10.1.4 · hesap: bizim")
        cap = VGroup(T("10G · FEC açık: FS yükü ≤", 16, TXT, BOLD), T("135 424 B", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.12).move_to([-3.9, 1.95, 0], aligned_edge=LEFT)
        fit_ = VGroup(T("→ 88 çerçeve tam sığar · 89.'su bölünür", 15, TXT, BOLD), ytag("bizim hesabımız")).arrange(RIGHT, buff=0.15)
        fit_.move_to([-3.9, 1.45, 0], aligned_edge=LEFT)
        yf = 0.55
        fs = strip([(0.76, "HLend", HLC, 0.3), (0.85, "BWmap", BWC, 0.3), (0.85, "PLOAM", PLDC, 0.3), (3.91, "XGEM × 88 · 1528 B", SAC, 0.18),
                    (0.85, "952 B", SAC, 0.4), (0.58, "BIP", BIPC, 0.3)], -3.9, yf, 0.5, 15)
        fl = VGroup(T("LF = 0 · kalan 566 B → sonraki çerçeve", 14, SAC, BOLD).next_to(fs[4], DOWN, buff=0.08).align_to(fs[5], RIGHT))
        pre_l = brace_lbl(VGroup(fs[0], fs[1], fs[2]), "önde", MUTED, DOWN, 14)
        bip_l = T("arkada", 14, MUTED, BOLD).next_to(fs[5], UP, buff=0.06)
        yp = -0.85
        ph = VGroup(sbox("Reed-Solomon", "RS(248,216)", PARC, 2.2, 0.72, 16, 14), sbox("karıştırma", "x⁵⁸ + x³⁹ + 1", PHC, 2.2, 0.72, 16, 14),
                    sbox("PSBd", "24 B", PSC, 1.45, 0.72, 16, 14)).arrange(RIGHT, buff=0.42).move_to([-0.35, yp, 0])
        pa = VGroup(*[arrow(ph[i][0].get_right(), ph[i + 1][0].get_left(), MUTED, 2, 0.1) for i in range(2)])
        fr = T("PHY çerçevesi: 155 520 B / 125 µs", 14, MUTED, BOLD).next_to(ph, DOWN, buff=0.12)
        ln = VGroup(T("çerçevemiz hatta:", 16, MUTED, BOLD), T("1528 B ≈ 1,23 µs · FEC ile", 16, TXT, BOLD), T("1,41 µs", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.12)
        fit(ln, 7.8).move_to([0, -2.15, 0])
        self.at(self.cue("çerçeve yükü yüz otuz beş", 2.1))
        self.play(FadeIn(cap, shift=RIGHT * 0.05), *self.stk.go("o", 2), run_time=0.45)
        self.at(self.cue("seksen sekiz çerçeve tam", 7.6))
        self.play(FadeIn(fs[3]), FadeIn(fit_, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("seksen dokuzuncusu bölünür", 11.8))
        self.play(FadeIn(fs[4]), FadeIn(fl), run_time=0.4)
        self.at(self.cue("Önüne HLend", 14.0))
        self.play(FadeIn(fs[0]), run_time=0.25)
        self.at(self.cue("harita ve PLOAM'lar", 15.1))
        self.play(FadeIn(fs[1:3]), FadeIn(pre_l), run_time=0.3)
        self.at(self.cue("arkasına BIP-32", 16.8))
        self.play(FadeIn(fs[5]), FadeIn(bip_l), run_time=0.3)
        self.at(self.cue("dördüncü ve beşinci bölümler", 18.6))
        self.play(Indicate(ch[0][0], color=ACC), Indicate(ch[0][1], color=ACC), run_time=0.5)
        self.at(self.cue("Sonra ikinci bölümün", 21.1))
        self.play(*self.stk.go("o", 3), Indicate(ch[0][2], color=ACC), run_time=0.45)
        self.at(self.cue("birinci sezonun dördüncü", 22.8))
        self.play(Indicate(ch[0][3], color=S1C), run_time=0.45)
        self.at(self.cue("Reed Solomon", 27.2))
        self.play(FadeIn(ph[0], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("karıştırma ve PSBd", 28.3))
        self.play(GrowArrow(pa[0]), FadeIn(ph[1]), GrowArrow(pa[1]), FadeIn(ph[2]), FadeIn(fr), run_time=0.45)
        self.at(self.cue("bir virgül kırk bir", 29.9))
        self.play(FadeIn(ln, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # e4 — PMD bridge: S1·B3/B4 OLT Tx 187.8 THz, +3…+7 dBm; S1·B2 N1 14–29 dB, 20 km ≈ 100 µs; S1·B5 ONU Rx −28 dBm at BER 10⁻³ pre-FEC
        self.beat("e4")
        h = self.reset_keep("PMD Köprüsü — ışık", "pmd", self.stk.keep(), 0.5, w=6.6, extra=[self.src_in("S1·B3 · S1·B4 · S1·B2 · S1·B5 · G.989.2 Tablo 11-2 · 11-5 · 6-1 · 6-2")])
        rows = VGroup(VGroup(chipz("S1·B3", "S1·B4"), T("OLT vericisi", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                      VGroup(T("187,8 THz (1596,34 nm)", 19, CH[1], BOLD), T("· +3 … +7 dBm", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.15),
                      VGroup(chipz("S1·B2"), T("ODN", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                      VGroup(T("N1: 14–29 dB", 19, TXT, BOLD), T("· 20 km", 19, TXT, BOLD), T("· ≈ 100 µs", 19, TMRC, BOLD)).arrange(RIGHT, buff=0.15),
                      VGroup(chipz("S1·B5"), T("ONU alıcısı", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                      VGroup(T("−28 dBm", 19, GOLD, BOLD), T("@ BER 10⁻³ (FEC öncesi)", 18, TXT, BOLD)).arrange(RIGHT, buff=0.15))
        for k, y in enumerate((1.9, 1.35, 0.45, -0.1, -1.0, -1.55)):
            rows[k].move_to([-3.9, y, 0], aligned_edge=LEFT)
        self.at(self.cue("üçüncü ve dördüncü bölümleri", 1.0))
        self.play(FadeIn(rows[0], shift=RIGHT * 0.05), *self.stk.go("o", 4), run_time=0.45)
        self.at(self.cue("yüz seksen yedi virgül sekiz", 4.8))
        self.play(FadeIn(rows[1][0], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("artı üç ile artı yedi", 9.3))
        self.play(FadeIn(rows[1][1], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("İkinci bölümü", 13.1))
        self.play(FadeIn(rows[2], shift=RIGHT * 0.05), FadeOut(self.stk.hl), run_time=0.35)
        self.at(self.cue("N1 sınıfında kayıp", 14.2))
        self.play(FadeIn(rows[3][0], shift=RIGHT * 0.05), MoveAlongPath(self.stk.pkt, self.stk.fib), run_time=1.6)
        self.at(self.cue("yirmi kilometre,", 18.5))
        self.play(FadeIn(rows[3][1]), run_time=0.25)
        self.at(self.cue("yaklaşık yüz mikrosaniye", 19.9))
        self.play(FadeIn(rows[3][2]), run_time=0.3)
        self.at(self.cue("Beşinci bölümü", 22.0))
        self.stk.hl.move_to(self.stk.cols["n"][4][0].get_center())
        self.play(FadeIn(rows[4], shift=RIGHT * 0.05), FadeIn(self.stk.hl), self.stk.pkt.animate.move_to(self.stk.pos("n", 4)), run_time=0.4)
        self.at(self.cue("FEC öncesi on üzeri", 24.3))
        self.play(FadeIn(rows[5], shift=RIGHT * 0.05), run_time=0.35)
        self.end(pad=0.1)
        self.save_timeline("ep20_p4A")


class E20P4B(P4Act):
    HDR, MANIFEST, PREV_BADGE = H20[4], M20("p4"), "pmd"

    def construct(self):
        # e5 — at the ONU (S2·B2): hunt → pre-sync → sync, descramble, FEC corrects up to 16 bytes per codeword; keep own BWmap allocations; PLOAM integrity
        #      (S2·B5); XGEM delineation, Port filter, decrypt, drop the padding → UNI; S2·B9's counters count every step
        self.beat("e5")
        self.stage("n", 4)
        h, ch = self.step("↓ ONU'da — yukarı doğru", ["S2·B2", "S2·B5", "S2·B3", "S2·B8", "S2·B9"], src="G.989.3 §10.1.1.3 · §10.1.3 · §8.1.1 · §11.1.2 · §9.2 · §15.4 · Tablo 14-1")
        steps = [("S2·B2", "av → ön senkron → senkron", 3), ("S2·B2", "karıştırma çözülür · FEC: kod sözcüğü başına ≤ 16 bayt", 3),
                 ("S2·B4", "haritadaki kendi tahsislerini saklar (↑ için)", 2), ("S2·B5", "PLOAM bütünlüğü (MIC) denetlenir", 2),
                 ("S2·B3", "XGEM sınırları bulunur · Port 0x0400 süzülür", 1), ("S2·B8", "yük çözülür · KI 01 → tek alıcılı anahtar", 1),
                 ("S2·B3", "2 dolgu baytı atılır → 1518 B → abone arayüzü", 0), ("S2·B9", "sayaçlar her adımı sayar", 0)]
        rows = VGroup()
        for k, (c, s, _) in enumerate(steps):
            r = VGroup(tag(c, ACC, 14), T(s, 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
            fit(r, 7.8).move_to([-3.9, 1.9 - 0.56 * k, 0], aligned_edge=LEFT)
            rows.add(r)
        keys = [("av,", 3.2), ("karıştırma çözülür", 5.3), ("haritadaki kendi", 11.3), ("PLOAM bütünlüğünü", 14.8), ("XGEM sınırlarını", 19.0),
                ("yükü çözer", 22.0), ("dolguyu atar", 22.9), ("dokuzuncu bölümün sayaçları", 26.9)]
        for k, (key, d) in enumerate(keys):
            self.at(self.cue(key, d))
            lay = steps[k][2]
            self.play(FadeIn(rows[k], shift=RIGHT * 0.05), *self.stk.go("n", lay if k < 7 else 0), run_time=0.35)
            if k == 1:
                self.at(self.cue("FEC kod sözcüğü", 6.9))
                self.play(Indicate(rows[1][1], color=PARC, scale_factor=1.03), run_time=0.4)
        self.end(pad=0.05)

        # e6 — upstream: a same-size frame enters the ONU; the OMCI mapping (S2·B1, S2·B4) puts it on Port 1024 and T-CONT 1024; the DBRu reports 380 four-byte
        #      units (headers excluded); our CRC: 00 01 7C 66
        self.beat("e6")
        h, ch = self.step("↑ ONU'dan — kuyruk raporu", ["S2·B1", "S2·B4", "S2·B2"], src="G.989.3 §6.1.5 · §8.1.2.2 (8-1) · DBRu CRC-8: bizim hesabımız")
        e = VGroup(tile("1518 B", GOOD, 1.3, 0.42, 15, 0.25), T("→ OMCI eşlemesi →", 15, MUTED, BOLD), tag("Port 0x0400", PIDC, 15),
                   T("·", 15, MUTED, BOLD), tag("T-CONT · Alloc-ID 1024", ACC, 15)).arrange(RIGHT, buff=0.12)
        fit(e, 7.8).move_to([-3.9, 1.9, 0], aligned_edge=LEFT)
        q = queue(3, SAC, 5, 0.22, 0.4).move_to([-3.3, 0.85, 0])
        bo = VGroup(T("BufOcc = ⌈1518 / 4⌉ =", 17, TXT, BOLD), T("380", 21, GOLD, BOLD), T("(4 B birim)", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.12).next_to(q, RIGHT, buff=0.3)
        hx_ = T("başlıklar hariç", 15, WARN, BOLD).next_to(bo, DOWN, buff=0.08).align_to(bo, LEFT)
        db = fields([("BufOcc · 24 bit", 24, GOLD), ("CRC-8", 8, PINK)], 6.0, 0.5, 16, 14, show_w=False).move_to([-0.6, -0.7, 0])
        dbl = T("DBRu", 16, GOLD, BOLD).next_to(db, LEFT, buff=0.2)
        by = VGroup(*[HX(s, 24, c, BOLD) for s, c in (("00", GOLD), ("01", GOLD), ("7C", GOLD), ("66", PINK))]).arrange(RIGHT, buff=0.3).move_to([-0.9, -1.7, 0])
        byt = ytag("bizim CRC hesabımız").next_to(by, RIGHT, buff=0.3)
        self.at(self.cue("Aynı boyda bir çerçeve", 0.9))
        self.play(FadeIn(e[0], shift=RIGHT * 0.05), *self.stk.go("n", 0), run_time=0.4)
        self.at(self.cue("OMCI'ın kurduğu eşleme", 4.0))
        self.play(FadeIn(e[1:], shift=RIGHT * 0.05), *self.stk.go("n", 1), run_time=0.45)
        self.at(self.cue("ONU kuyruğunu DBRu", 13.2))
        self.play(FadeIn(q), FadeIn(db), FadeIn(dbl), run_time=0.4)
        self.at(self.cue("dört baytlık birimlerle", 15.9))
        self.play(FadeIn(bo, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("başlıklar hariç", 19.2))
        self.play(FadeIn(hx_, shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("bizim CRC hesabımızla", 20.5))
        self.play(FadeIn(byt), run_time=0.3)
        for k, (key, d) in enumerate((("sıfır sıfır,", 22.4), ("sıfır bir,", 25.0), ("yedi ce,", 25.9), ("altı altı", 26.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(by[k], shift=UP * 0.05), run_time=0.2)
        self.end(pad=0.05)

        # e7 — DBA (S2·B4) sizes the grant: XGEM + 4-byte report = 1532 B; 10G grants in 16-byte blocks: 96 blocks, the 4 spare bytes are S2·B3's short idle;
        #      the BWmap entry (S2·B2): Alloc-ID 1024, DBRu 1, StartTime 2000, GrantSize 96 → 0x1002 07D0 0060 1F9B (our HEC)
        self.beat("e7")
        h, ch = self.step("↑ DBA ve harita girdisi", ["S2·B4", "S2·B3", "S2·B2"], src="G.989.3 §7 · §8.1.1.2 · §9.1.4 · tahsis yapısı HEC: bizim hesabımız")
        sz = VGroup(T("XGEM 1528 B + DBRu 4 B =", 17, TXT, BOLD), T("1532 B", 20, GOLD, BOLD)).arrange(RIGHT, buff=0.12).move_to([-3.9, 1.9, 0], aligned_edge=LEFT)
        bl = VGroup(*[Rectangle(width=0.0775, height=0.4, stroke_width=0.6, stroke_color=BG, fill_color=TIMC, fill_opacity=0.6) for _ in range(96)]).arrange(RIGHT, buff=0)
        bl.move_to([-3.9, 1.1, 0], aligned_edge=LEFT)
        idl = Rectangle(width=0.06, height=0.4, stroke_width=0, fill_color=IDC, fill_opacity=0.95).move_to(bl[-1].get_right() + LEFT * 0.03)
        bll = VGroup(T("96 × 16 B = 1536 B", 16, TIMC, BOLD), T("· 4 B artan →", 15, TXT, BOLD), tag("kısa boş çerçeve (↑)", IDC, 14)).arrange(RIGHT, buff=0.12)
        fit(bll, 7.8).move_to([-3.9, 0.55, 0], aligned_edge=LEFT)
        ya = -0.55
        spec = [(n, b, c) if b > 2 else ("", b, c) for n, b, c in ALLOC14]
        fa = fields(spec, 7.8, 0.46, 14, 14, show_w=False, lpos=UP).move_to([0, ya, 0])
        top = ya + 0.23
        for i, (nm, dx) in ((1, ("DBRu", -0.42)), (2, ("PLOAMu", 0.5)), (5, ("FWI", -0.36)), (6, ("Profil", 0.42))):
            cx = fa[i][0].get_x()
            lb = T(nm, 14, ALLOC14[i][2], BOLD).move_to([cx + dx, top + 0.3, 0])
            fa[i].add(VGroup(lb, Line([cx, top, 0], [cx + dx * 0.55, top + 0.18, 0], color=ALLOC14[i][2], stroke_width=1.2)))
        fav = vals(fa, ["1024", "1", "0", "2000", "96", "0", "0", "0x1F9B"], ya - 0.42, GOLD, 14)
        for i, dx in ((1, -0.42), (2, 0.5), (5, -0.36), (6, 0.42)):
            fav[i].shift(RIGHT * dx)
        hx = VGroup(*[HX(s, 22, GOLD, BOLD) for s in ("0x1002", "07D0", "0060", "1F9B")]).arrange(RIGHT, buff=0.22).move_to([-0.6, -1.85, 0])
        hxt = ytag("bizim hesabımız").next_to(hx, RIGHT, buff=0.25)
        self.play(*self.stk.go("n", 2), run_time=0.4)
        self.at(self.cue("XGEM çerçevesi artı dört", 3.5))
        self.play(FadeIn(sz[0], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("bin beş yüz otuz iki", 6.8))
        self.play(FadeIn(sz[1]), run_time=0.25)
        self.at(self.cue("on altı baytlık bloklarla", 8.9))
        self.play(LaggedStart(*[FadeIn(b) for b in bl], lag_ratio=0.01), run_time=0.8)
        self.at(self.cue("doksan altı blok", 13.5))
        self.play(FadeIn(bll[0], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("artan dört bayt", 14.9))
        self.play(FadeIn(idl), FadeIn(bll[1]), run_time=0.3)
        self.at(self.cue("kısa boş çerçevesidir", 16.3))
        self.play(FadeIn(bll[2], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Harita girdisi", 19.4))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in fa], lag_ratio=0.06), run_time=0.6)
        for idx, (key, d) in zip(((0,), (1, 2), (3,), (4, 5, 6, 7)), (("tahsis kimliği bin yirmi dört", 22.8), ("rapor bayrağı bir", 25.3),
                                                                        ("başlangıç zamanı iki bin", 26.9), ("boyut doksan altı", 29.0))):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(fav[i], shift=UP * 0.05) for i in idx], run_time=0.25)
        self.play(FadeIn(hx), FadeIn(hxt), run_time=0.35)
        self.end(pad=0.05)

        # e8 — timing (S2·B6, S1·B2): the ONU sends RspTime 35 µs + EqD after the frame carrying the BWmap; Teqd ≥ 236 µs at DD20; an ONU at 10 km has
        #      EqD ≈ 101 µs; StartTime 2000 = 25.72 µs
        self.beat("e8")
        h, ch = self.step("↑ zamanlama", ["S2·B6", "S1·B2"], src="G.989.3 §13.1.1–13.1.5 · (13-6) · S1·B2 · hesap: bizim")
        X = lambda t: -3.9 + t * 0.0262
        ya = -1.95
        ax = Line([X(0), ya, 0], [X(300), ya, 0], color=MUTED, stroke_width=2)
        tk = VGroup(*[VGroup(Line([X(t), ya - 0.07, 0], [X(t), ya + 0.07, 0], color=MUTED, stroke_width=1.5),
                             T(str(t), 14, MUTED, BOLD).next_to([X(t), ya, 0], DOWN, buff=0.08)) for t in (0, 50, 100, 150, 200, 250, 300)])
        tku = T("µs", 14, MUTED, BOLD).next_to(tk[-1][1], RIGHT, buff=0.1)
        m0 = VGroup(Line([X(0), ya, 0], [X(0), 1.6, 0], color=GOLD, stroke_width=2.4), T("↓ BWmap'i taşıyan çerçeve", 15, GOLD, BOLD).move_to([X(0), 1.82, 0], aligned_edge=LEFT))
        yb = 0.75
        r1 = Rectangle(width=X(35) - X(0), height=0.45, stroke_color=TIMC, stroke_width=1.8, fill_color=TIMC, fill_opacity=0.4).move_to([(X(0) + X(35)) / 2, yb, 0])
        r1l = T("35", 15, TXT, BOLD).move_to(r1)
        r1n = T("RspTime 35 µs", 14, TIMC, BOLD).next_to(r1, UP, buff=0.06).align_to(r1, LEFT)
        r2 = Rectangle(width=X(135) - X(35), height=0.45, stroke_color=FEED, stroke_width=1.8, fill_color=FEED, fill_opacity=0.15).move_to([(X(35) + X(135)) / 2, yb, 0])
        r2l = T("gidiş-dönüş ≈ 100 µs", 14, TXT, BOLD).move_to(r2)
        r2n = T("ONU 10 km'de", 14, MUTED, BOLD).next_to(r2, UP, buff=0.06)
        r3 = Rectangle(width=X(236) - X(135), height=0.45, stroke_color=EQC, stroke_width=1.8, fill_color=EQC, fill_opacity=0.35).move_to([(X(135) + X(236)) / 2, yb, 0])
        r3l = T("EqD ≈ 101 µs", 15, TXT, BOLD).move_to(r3)
        br = brace_lbl(VGroup(r1, r2, r3), "T_eqd ≥ 236 µs (DD20, Lmin = 0)", GOLD, DOWN, 16)
        st = Rectangle(width=X(261.72) - X(236), height=0.45, stroke_color=ONUC, stroke_width=1.8, fill_color=ONUC, fill_opacity=0.45).move_to([(X(236) + X(261.72)) / 2, yb, 0])
        stl = VGroup(T("StartTime 2000 × 12,86 ns", 14, ONUC, BOLD), T("= 25,72 µs", 15, ONUC, BOLD)).arrange(DOWN, buff=0.03).next_to(st, UP, buff=0.08)
        stl.align_to(st, RIGHT).shift(RIGHT * 0.25)
        ufr = DashedLine([X(236), ya, 0], [X(236), yb - 0.3, 0], color=ONUC, stroke_width=1.8)
        ufl = T("↑ çerçeve başı", 14, ONUC, BOLD).next_to([X(236), ya + 0.25, 0], LEFT, buff=0.08)
        self.at(self.cue("bu sezonun altıncı", 0.8))
        self.play(Create(ax), FadeIn(tk), FadeIn(tku), FadeIn(m0), *self.stk.go("n", 3), run_time=0.6)
        self.at(self.cue("otuz beş mikrosaniyelik", 5.3))
        self.play(GrowFromEdge(r1, LEFT), FadeIn(r1l), FadeIn(r1n), run_time=0.45)
        self.at(self.cue("artı eşitleme gecikmesi", 10.5))
        self.play(GrowFromEdge(r2, LEFT), FadeIn(r2l), FadeIn(r2n), GrowFromEdge(r3, LEFT), FadeIn(r3l), run_time=0.6)
        self.at(self.cue("T eqd en az iki yüz", 14.5))
        self.play(FadeIn(br, shift=UP * 0.05), Create(ufr), FadeIn(ufl), run_time=0.5)
        self.at(self.cue("on kilometredeki ONU'nun", 20.4))
        self.play(Indicate(r3, color=EQC, scale_factor=1.06), Indicate(r3l, color=EQC), run_time=0.6)
        self.at(self.cue("Başlangıç zamanı iki bin", 25.8))
        self.play(GrowFromEdge(st, LEFT), FadeIn(stl[0]), run_time=0.45)
        self.at(self.cue("yirmi beş virgül yetmiş", 27.9))
        self.play(FadeIn(stl[1], shift=UP * 0.05), run_time=0.3)
        self.end(pad=0.05)
        self.save_timeline("ep20_p4B")


class E20P4C(P4Act):
    HDR, MANIFEST, PREV_BADGE = H20[4], M20("p4"), "std"

    def construct(self):
        # e9 — the burst (S2·B2): header + allocation + BIP-32 = 1544 B (FS header 0x014013F1, ours); FEC 7 full + 1 shortened codeword → 1800 B; preamble,
        #      delimiter and guard per S1·B6's table: 256 B; the whole slot 1.65 µs = 1.32 % of a frame (our arithmetic)
        self.beat("e9")
        self.stage("n", 3)
        h, ch = self.step("↑ burst", ["S2·B2", "S1·B6"], src="G.989.3 §8.1.2 · §10.1.2–10.1.3 · G.989.2 Tablo 11-11 · başlık + hesap: bizim")
        x0 = -3.9
        y1 = 1.75
        b1 = strip([(0.85, "başlık 4", HLC, 0.35), (4.75, "tahsis 1536 B: DBRu 4 + XGEM 1528 + boş 4", SAC, 0.2), (0.8, "BIP 4", BIPC, 0.35)], x0, y1, 0.48, 14)
        b1t = T("= 1544 B", 16, GOLD, BOLD).next_to(b1, RIGHT, buff=0.12)
        fh = VGroup(HX("0x014013F1", 16, GOLD, BOLD), ytag("bizim hesabımız", GOLD, 14)).arrange(RIGHT, buff=0.12).next_to(b1[0], UP, buff=0.08).align_to(b1[0], LEFT)
        y2 = 0.65
        cw = VGroup()
        for k in range(8):
            w_ = 0.86 if k < 7 else 0.3
            d = Rectangle(width=w_ * 0.78, height=0.44, stroke_color=SAC, stroke_width=1.4, fill_color=SAC, fill_opacity=0.25)
            p = Rectangle(width=w_ * 0.22 if k < 7 else 0.22, height=0.44, stroke_color=PARC, stroke_width=1.4, fill_color=PARC, fill_opacity=0.5)
            cw.add(VGroup(d, p).arrange(RIGHT, buff=0))
        cw.arrange(RIGHT, buff=0.03).move_to([x0, y2, 0], aligned_edge=LEFT)
        cwl = VGroup(T("FEC: 7 tam + 1 kısaltılmış kod sözcüğü →", 15, TXT, BOLD), T("1800 B", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.12)
        cwl.next_to(cw, DOWN, buff=0.1).align_to(cw, LEFT)
        y3 = -0.65
        b3 = strip([(1.05, "Tplo 256 B", OVC, 0.4), (5.35, "FEC'li burst 1800 B", SAC, 0.2)], x0, y3, 0.48, 14)
        b3l = T("önsöz · sınırlayıcı · koruma (S1·B6 tablosu)", 14, OVC, BOLD).next_to(b3[0], DOWN, buff=0.08).align_to(b3[0], LEFT)
        b3t = T("= 2056 B", 16, GOLD, BOLD).next_to(b3, RIGHT, buff=0.12)
        y4 = -1.95
        frm = Rectangle(width=7.8, height=0.4, stroke_color=MUTED, stroke_width=1.6, fill_color=MUTED, fill_opacity=0.06).move_to([0, y4, 0])
        frl = T("125 µs ↑ çerçeve", 14, MUTED, BOLD).next_to(frm, UP, buff=0.05).align_to(frm, LEFT)
        sl = Rectangle(width=7.8 * 0.0132, height=0.4, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to([frm.get_left()[0] + 2.0, y4, 0])
        sll = VGroup(T("1,65 µs = çerçevenin", 15, TXT, BOLD), T("% 1,32", 17, GOLD, BOLD), ytag("bizim hesabımız")).arrange(RIGHT, buff=0.12)
        sll.next_to(frm, DOWN, buff=0.1)
        self.at(self.cue("başlık,", 2.6))
        self.play(FadeIn(b1[0]), *self.stk.go("n", 2), run_time=0.3)
        self.at(self.cue("tahsis ve BIP-32", 3.2))
        self.play(FadeIn(b1[1:]), run_time=0.35)
        self.at(self.cue("bin beş yüz kırk dört", 4.6))
        self.play(FadeIn(b1t), FadeIn(fh, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("FEC yedi tam", 6.9))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.05) for c in cw], lag_ratio=0.1), *self.stk.go("n", 3), run_time=0.7)
        self.play(FadeIn(cwl, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Önsöz,", 13.2))
        self.play(FadeIn(b3[0]), run_time=0.3)
        self.at(self.cue("sınırlayıcı ve koruma", 13.7))
        self.play(FadeIn(b3l), FadeIn(b3[1]), run_time=0.35)
        self.at(self.cue("iki yüz elli altı bayt", 16.1))
        self.play(FadeIn(b3t), Indicate(ch[0][1], color=S1C), run_time=0.45)
        self.at(self.cue("Bütün dilim", 21.8))
        self.play(FadeIn(frm), FadeIn(frl), FadeIn(sl, scale=2), FadeIn(sll[0]), run_time=0.45)
        self.at(self.cue("yüzde bir virgül otuz", 25.7))
        self.play(FadeIn(sll[1:], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # e10 — PMD bridge: S1·B6/B7 ONU Tx on within 128.6 ns, Type A link +4…+9 dBm, dark outside its burst; S1·B8 OLT burst Rx −26 dBm; arrival 261.72 µs after
        #       the frame carrying the BWmap; the OLT unwinds it and hands it to the service interface
        self.beat("e10")
        h = self.reset_keep("PMD Köprüsü — dönüş", "pmd", self.stk.keep(), 0.5, w=6.6, extra=[self.src_in("S1·B6 · S1·B7 · S1·B8 · G.989.2 Tablo 11-7 · 11-11 · hesap: bizim")])
        rows = VGroup(VGroup(chipz("S1·B6", "S1·B7"), T("ONU vericisi", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                      VGroup(T("açılma ≤ 128,6 ns", 18, GOLD, BOLD), T("· A tipi bağlantı +4 … +9 dBm", 18, TXT, BOLD)).arrange(RIGHT, buff=0.12),
                      T("burst'ü dışında karanlık", 17, WARN, BOLD),
                      VGroup(chipz("S1·B8"), T("OLT burst alıcısı:", 17, TXT, BOLD), T("−26 dBm", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.15),
                      VGroup(T("varış: ↓ BWmap çerçevesi + 236 + 25,72 =", 16, TXT, BOLD), T("261,72 µs", 19, GOLD, BOLD), ytag("bizim hesabımız")).arrange(RIGHT, buff=0.12),
                      T("OLT geri açar → servis arayüzü (SNI)", 17, GOOD, BOLD))
        for k, y in enumerate((1.9, 1.35, 0.85, 0.05, -0.85, -1.75)):
            fit(rows[k], 7.85).move_to([-3.9, y, 0], aligned_edge=LEFT)
        back = self.stk.fib.copy().reverse_points()
        self.at(self.cue("altıncı ve yedinci bölümleri", 1.0))
        self.play(FadeIn(rows[0], shift=RIGHT * 0.05), *self.stk.go("n", 4), run_time=0.45)
        self.at(self.cue("yüz yirmi sekiz virgül altı", 4.8))
        self.play(FadeIn(rows[1][0], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("artı dört ile artı dokuz", 9.9))
        self.play(FadeIn(rows[1][1], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("burst'ü dışında karanlıktır", 15.3))
        self.play(FadeIn(rows[2], shift=RIGHT * 0.05), FadeOut(self.stk.hl), run_time=0.3)
        self.play(MoveAlongPath(self.stk.pkt, back), run_time=1.6)
        self.at(self.cue("Sekizinci bölümü", 17.7))
        self.stk.hl.move_to(self.stk.cols["o"][4][0].get_center())
        self.play(FadeIn(rows[3][:2], shift=RIGHT * 0.05), FadeIn(self.stk.hl), self.stk.pkt.animate.move_to(self.stk.pos("o", 4)), run_time=0.4)
        self.at(self.cue("eksi yirmi altı dBm", 19.1))
        self.play(FadeIn(rows[3][2]), run_time=0.3)
        self.at(self.cue("haritayı taşıyan çerçeveden iki yüz", 23.3))
        self.play(FadeIn(rows[4], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("OLT onu geri açar", 30.7))
        self.play(FadeIn(rows[5], shift=RIGHT * 0.05), *self.stk.go("o", 3), run_time=0.35)
        for i in (2, 1, 0):
            self.play(*self.stk.go("o", i), run_time=0.25)
        self.end(pad=0.05)

        # e11 — the equation under the language: DS +3 − 29 = −26 = −28 + 2 (OPP); US +4 − 29 = −25 = −26 + 1; zero margin both ways, by design
        self.beat("e11")
        h = self.reset("Bütçe — sıfır marj", "neden", 0.5, extra=[self.src_in("G.989.2 Tablo 11-5 · 11-7 · Tablo 6-1 (N1) · hesap: bizim")])
        Y = lambda d: -2.35 + (d + 30) * 0.105
        ax = Line([-5.3, Y(-30), 0], [-5.3, Y(10), 0], color=MUTED, stroke_width=2)
        tk = VGroup(*[VGroup(Line([-5.37, Y(d), 0], [-5.23, Y(d), 0], color=MUTED, stroke_width=1.5), T(f"{d:+d}" if d else "0", 14, MUTED, BOLD).next_to([-5.37, Y(d), 0], LEFT, buff=0.08))
                      for d in (10, 0, -10, -20, -30)])
        axl = T("dBm", 15, MUTED, BOLD).move_to([-5.3, Y(10) + 0.32, 0])

        def col(xt, xr, tx, rx, sens, opp, color, name):
            g = VGroup()
            g.add(T(name, 18, color, BOLD).move_to([(xt + xr) / 2, Y(10) + 0.25, 0]))
            dt = Dot([xt, Y(tx), 0], radius=0.09, color=GOLD)
            dr = Dot([xr, Y(rx), 0], radius=0.09, color=color)
            a = arrow([xt + 0.1, Y(tx), 0], [xr - 0.1, Y(rx), 0], color, 2.6, 0.14)
            lt = T(f"Tx en zayıf {tx:+d} dBm".replace("-", "−"), 15, GOLD, BOLD).next_to(dt, UP, buff=0.1)
            la = T("− 29 dB (N1 en kötü)", 15, TXT, BOLD).next_to(a.get_center(), RIGHT, buff=0.15).shift(UP * 0.15)
            lr = T(f"{rx} dBm".replace("-", "−"), 17, color, BOLD).next_to(dr, RIGHT, buff=0.12).shift(UP * 0.22)
            req = DashedLine([xt - 0.4, Y(rx), 0], [xr + 1.9, Y(rx), 0], color=WARN, stroke_width=1.8, dash_length=0.08)
            rq = T(f"gerekli: {sens} + {opp} (yol cezası) = {rx}".replace("-", "−"), 15, WARN, BOLD).next_to(req, DOWN, buff=0.12).align_to(req, RIGHT)
            mg = tag("marj 0", WARN, 16).next_to(lr, RIGHT, buff=0.15)
            return VGroup(g, dt, lt, a, la, dr, lr, req, rq, mg)
        ds = col(-4.4, -2.6, 3, -26, -28, 2, CH[1], "↓ aşağı yön")
        us = col(0.9, 2.7, 4, -25, -26, 1, ONUC, "↑ yukarı yön")
        z = VGroup(T("İki yönde de pay sıfır —", 19, TXT, BOLD), T("tasarım gereği", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0.3, -2.62, 0])
        fin = T("Bir paketin hayatı, sıfır marjla kapanan bir bütçenin üstünde yaşanır.", 20, GOLD, BOLD).move_to([0.3, -3.1, 0])
        fit(fin, 12.0)
        self.play(Create(ax), FadeIn(tk), FadeIn(axl), run_time=0.5)
        self.at(self.cue("Aşağı yönde en zayıf", 3.7))
        self.play(FadeIn(ds[0]), FadeIn(ds[1], scale=1.5), FadeIn(ds[2]), run_time=0.4)
        self.at(self.cue("en kötü kayıp yirmi", 7.1))
        self.play(GrowArrow(ds[3]), FadeIn(ds[4]), run_time=0.5)
        self.at(self.cue("alıcıya eksi yirmi altı", 9.9))
        self.play(FadeIn(ds[5], scale=1.5), FadeIn(ds[6]), run_time=0.35)
        self.at(self.cue("eksi yirmi sekizlik hassasiyet", 12.5))
        self.play(Create(ds[7]), FadeIn(ds[8]), FadeIn(ds[9]), run_time=0.5)
        self.at(self.cue("Yukarı yönde artı dört", 18.2))
        self.play(FadeIn(us[0]), FadeIn(us[1], scale=1.5), FadeIn(us[2]), GrowArrow(us[3]), FadeIn(us[4]), run_time=0.6)
        self.at(self.cue("eksi yirmi beş:", 21.6))
        self.play(FadeIn(us[5], scale=1.5), FadeIn(us[6]), run_time=0.3)
        self.at(self.cue("eksi yirmi altı artı bir", 22.8))
        self.play(Create(us[7]), FadeIn(us[8]), FadeIn(us[9]), run_time=0.45)
        self.at(self.cue("İki yönde de pay sıfırdır", 24.9))
        self.play(FadeIn(z[0], shift=DOWN * 0.05), Indicate(ds[9], color=WARN), Indicate(us[9], color=WARN), run_time=0.6)
        self.at(self.cue("tasarım gereği", 27.1))
        self.play(FadeIn(z[1], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Bir paketin hayatı,", 28.4))
        self.play(FadeIn(fin, shift=UP * 0.05), run_time=0.6)
        self.end(pad=0.1)

        self.note11("e12", [("1", "Bu yolculuğu ne durdurabilir? Her biri bir bölüm",
                             "Besleyici kesiği → B tipi · kanal kaybı → ONU tarafı koruma ·\nyabancı burst → başıboşluk araçları · yanlış anahtar → şifreleme sayaçları ·\nFEC sınırını aşan hata → senkron kaybı.", "bu yolculuğu ne durdurabilir"),
                            ("2", "Analizördeki başlıkları bizim değerlerimizle karşılaştırın",
                             "0x17B90400000020A7 · 0x100207D000601F9B · 0x014013F1 · DBRu 00 01 7C 66\n— ama altın vektör saymayın.", "İki:")])
        self.bridge_beat("e13", "Paket evine ulaştı.\nŞimdi son kez laboratuvara.")
        self.save_timeline("ep20_p4C")
