"""S2·B6 · Laboratuvarda (merdiven, aktivasyon süresi, yanıt süresi, ranging, sessiz pencere, kayma, zamanlayıcılar,
günün saati, acil durdurma) and Kapanış."""
from ep16_common import *


class E16LabA(Act16):
    HDR, MANIFEST, FIRST = H16["L"], M16("lab"), True

    def construct(self):
        # g1 — bench: analyzer on a splitter, OLT emulator, real ONU, traffic generator, 0/10/20 km spools, OTDR, power meter, time-interval counter
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Bir aktivasyonu ölçmek")
        self.at(self.cue("Düzenek", 1.2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Düzenek")
        y1, y2 = 1.15, -1.05
        pa = pa_icon(2.0, 1.35, "Analizör · ayırıcıdan").move_to([-5.1, y1, 0])
        em = emu_icon(2.0, 1.35, "OLT emülatörü").move_to([-1.7, y1, 0])
        onu = VGroup(onu_box("ONU", ONUC, 1.6, 0.8, 20, "gerçek"), T("aktive edilecek ONU", 16, TXT, SEMIBOLD)).arrange(DOWN, buff=0.25).move_to([1.7, y1 - 0.1, 0])
        tg = tg_icon(2.0, 1.35, "Trafik üreteci").move_to([5.1, y1, 0])
        sp = VGroup(*[spool(s, FEED, 0.3) for s in ("0 km", "10 km", "20 km")]).arrange(RIGHT, buff=0.18).move_to([-4.9, y2, 0])
        ot = otdr_icon(2.0, 1.35, "OTDR").move_to([-1.6, y2, 0])
        pm = instr("PM", 2.0, 1.35, "−∞ dBm", None, MUTED).move_to([1.5, y2, 0])
        ct = counter_icon(2.0, 1.35, "Zaman aralığı sayacı", "ns").move_to([4.8, y2, 0])
        st = VGroup(VGroup(T("standart: test yöntemi vermez", 18, TXT, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.1),
                    VGroup(T("ölçütler standarttan", 18, TXT, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.6).move_to([0, -2.9, 0])
        self.play(self.set_src("G.989.3 §12–13 · tezgâh ve yöntemler: yorum"), run_time=0.3)
        self.at(self.cue("protokol analizörü", 2.5))
        self.play(FadeIn(pa, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("bir OLT emülatörü", 6.4))
        self.play(FadeIn(em, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("gerçek bir ONU", 7.9))
        self.play(FadeIn(onu, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bir trafik üreteci", 9.2))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("sıfır,", 10.8))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in sp], lag_ratio=0.25), run_time=0.8)
        self.at(self.cue("bir OTDR", 14.9))
        self.play(FadeIn(ot, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bir güç ölçer", 15.7))
        self.play(FadeIn(pm, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(ct, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("test yöntemi vermez", 19.3))
        self.play(FadeIn(st[0], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("ölçütler standarttandır", 22.3))
        self.play(FadeIn(st[1], shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.05)

        # g2 — TEST 1: the PLOAM ladder of one activation; MICs with the default key (0x55 × 16)
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "Aktivasyonun merdiveni")
        p = apanel(12.6, 4.65, "Analizör · bir aktivasyonun PLOAM sırası", ACC).move_to([0, -0.55, 0])
        rows = [("↓", "System · Channel · Burst_Profile", "profiller", GOLD), ("↓", "SN tahsisi · Alloc-ID 1021/1022/1023 · GrantSize 0", "keşif", SNC),
                ("↑", "Serial_Number_ONU · ONU-ID 0x03FF = 1023", "O2-3", SNC), ("↓", "Assign_ONU-ID · 0x03", "→ O4", SNC),
                ("↓", "ranging tahsisi → varsayılan Alloc-ID", "O4", RGC), ("↑", "Registration · SeqNo 0", "O4", RGC),
                ("↓", "Ranging_Time · P = 1 (mutlak)", "→ O5", EQC), ("↑", "Acknowledgement", "O5", OPC)]
        lad = VGroup()
        for d, s, n, c in rows:
            lad.add(VGroup(T(d, 18, c, BOLD), HX(s, 16, TXT, BOLD), T(n, 15, c, BOLD), ok_x(True, 17)))
        top = panel_top(p, 0.25)
        for k, r in enumerate(lad):
            yy = top - 0.18 - k * 0.43
            r[0].move_to([-5.9, yy, 0])
            r[1].move_to([-5.55, yy, 0], aligned_edge=LEFT)
            r[2].move_to([3.4, yy, 0], aligned_edge=LEFT)
            r[3].move_to([5.7, yy, 0])
            for m in r[1:3]:
                m.set_opacity(1)
            r[3].set_opacity(0)
        mic = VGroup(T("MIC:", 17, HECC, BOLD), HX("varsayılan PLOAM_IK = 0x55 × 16", 17, HECC, BOLD), T("→ hepsi tutmalı", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        mic.move_to([0, top - 0.18 - 8 * 0.43 - 0.05, 0])
        self.play(self.set_src("G.989.3 §12.1.3 · Tablo 11-6/11-7/11-25/11-26/11-28 · §15.3.3"), FadeIn(p), run_time=0.4)
        cues = (("profiller,", 5.5), ("seri numarası tahsisi", 6.3), ("kimliği bin yirmi üç", 8.2), ("kimlik atama", 12.2), ("varsayılan tahsis kimliğine", 13.3),
                ("kayıt,", 17.0), ("mutlak eşitleme", 17.5), ("ve onay", 19.2))
        for k, (key, d) in enumerate(cues):
            self.at(self.cue(key, d))
            self.play(FadeIn(lad[k][:3], shift=RIGHT * 0.05), lad[k][3].animate.set_opacity(1), run_time=0.3)
        self.at(self.cue("bütünlük kodları", 20.4))
        self.play(FadeIn(mic, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g3 — TEST 2: activation time from DS light to the EqD ACK; no target in the text; split; lower bounds from the text
        self.beat("g3")
        self.play(FadeOut(VGroup(p, lad, mic)), run_time=0.4)
        h = step_head(self, 2, "Aktivasyon süresi", h)
        x0 = -5.8
        bar = strip([(1.6, "↓ senkron", O1C, 0.3), (4.4, "profil öğrenme", O1C, 0.18), (3.4, "keşif", SNC, 0.25), (2.2, "ranging", RGC, 0.25)], x0, 0.7, 0.62, 16)
        m0 = VGroup(DashedLine([x0, 1.3, 0], [x0, 0.1, 0], color=GOLD, stroke_width=2), T("↓ ışık", 15, GOLD, BOLD))
        m0[1].next_to(m0[0], UP, buff=0.05)
        m1 = VGroup(DashedLine([x0 + 11.6, 1.3, 0], [x0 + 11.6, 0.1, 0], color=GOLD, stroke_width=2), T("EqD onayı", 15, GOLD, BOLD))
        m1[1].next_to(m1[0], UP, buff=0.05).align_to(m1[0], RIGHT)
        tot = brace_lbl(bar, "aktivasyon süresi · ölçülen", GOLD, DOWN, 16)
        nt = VGroup(T("standartta hedef:", 17, TXT, BOLD), T("yok", 17, WARN, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, 1.85, 0])
        lb = VGroup(tag("profil aralığı 1–5 s · §17.1", GOLD, 16), tag("profil bekleme ≥ 10 s · Tablo 12-1", TMRC, 16), tag("SN tahsis aralığı: OLT'nin seçimi", SNC, 16))
        lb.arrange(RIGHT, buff=0.25)
        fit(lb, 12.6).move_to([0, -1.9, 0])
        lbl = T("↑ alt sınırlar metinden", 16, MUTED, BOLD).next_to(lb, DOWN, buff=0.15).align_to(lb, LEFT)
        ye = tot.get_bottom()[1] - 0.08
        la = VGroup(arrow(lb[0].get_top(), [bar[1].get_x() - 0.8, ye, 0], GOLD, 1.8, 0.08),
                    arrow(lb[1].get_top(), [bar[1].get_x() + 0.6, ye, 0], TMRC, 1.8, 0.08),
                    arrow(lb[2].get_top(), [bar[2].get_x() + 0.6, ye, 0], SNC, 1.8, 0.08))
        self.play(self.set_src("G.989.3 Tablo 12-1 (O1.2) · §17.1 · §12.1.5 · yöntem: yorum"), run_time=0.3)
        self.at(self.cue("aşağı yön ışığından", 2.6))
        self.play(Create(m0[0]), FadeIn(m0[1]), Create(m1[0]), FadeIn(m1[1]), run_time=0.6)
        self.at(self.cue("Standartta hedef yoktur", 7.3))
        self.play(FadeIn(nt, shift=UP * 0.05), run_time=0.4)
        for k, (key, d) in enumerate((("süreyi senkron", 9.3), ("profil öğrenme", 10.6), ("keşif ve ranging", 11.9))):
            self.at(self.cue(key, d))
            if k < 2:
                self.play(GrowFromEdge(bar[k], LEFT), run_time=0.35)
            else:
                self.play(GrowFromEdge(bar[2], LEFT), run_time=0.3)
                self.play(GrowFromEdge(bar[3], LEFT), FadeIn(tot), run_time=0.4)
        self.at(self.cue("Alt sınırlar metinden", 14.4))
        self.play(FadeIn(lbl), run_time=0.3)
        for k, (key, d) in enumerate((("bir ile beş saniyelik", 16.8), ("en az on saniyelik", 19.9), ("OLT'nin seçtiği", 23.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(lb[k], shift=UP * 0.05), GrowArrow(la[k]), run_time=0.4)
        self.end(pad=0.05)

        # g4 — TEST 3: response time: ~0 fibre, EqD = 0; arrival − StartTime·Q0 = RspTime + 2 × patch delay; 34–36 µs; = value reported via OMCC
        self.beat("g4")
        self.play(FadeOut(VGroup(bar, m0, m1, tot, nt, lb, lbl, la)), run_time=0.4)
        h = step_head(self, 3, "Yanıt süresi", h)
        y = 1.3
        em = emu_icon(1.8, 1.25, "OLT emülatörü").move_to([-4.8, y, 0])
        onu = onu_box("ONU", ONUC, 1.3, 0.6, 17, "EqD = 0").move_to([-0.6, y, 0])
        cab = Line(em[0].get_right(), onu.get_left(), color=FEED, stroke_width=3)
        cabl = T("≈ 0 km · bağlantı kablosu", 15, FEED, BOLD).next_to(cab, UP, buff=0.06)
        eq = VGroup(term("Registration varışı − StartTime·Q0", "ölçülen", RGC, 20, 14), T("=", 20, TXT, BOLD), term("RspTime", "yanıt süresi", TIMC, 20, 14),
                    T("+", 20, TXT, BOLD), term("2 × kablo", "gidiş + dönüş", FEED, 20, 14)).arrange(RIGHT, buff=0.18, aligned_edge=UP).move_to([0, -0.2, 0])
        ax, X = lin_axis(33, 37, -4.0, 4.0, -2.05, [33, 34, 35, 36, 37], size=15, fmt=lambda v: f"{v} µs")
        ok = Rectangle(width=X(36) - X(34), height=0.5, stroke_width=0, fill_color=GOOD, fill_opacity=0.25).move_to([(X(34) + X(36)) / 2, -1.75, 0])
        okl = T("35 ± 1 µs", 16, GOOD, BOLD).next_to(ok, LEFT, buff=0.2)
        mk = VGroup(Triangle(color=TXT, fill_color=TXT, fill_opacity=1).scale(0.09).rotate(PI).move_to([X(35.2), -1.45, 0]))
        om = VGroup(T("= ONU'nun OMCC üzerinden bildirdiği RspTime i", 17, TXT, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.12).move_to([4.0, 1.3, 0])
        fit(om, 6.0)
        om.next_to(onu, RIGHT, buff=0.4)
        self.play(self.set_src("G.989.3 §13.1.1 · §13.1.8 · (13-7) · yöntem: yorum"), FadeIn(em), run_time=0.4)
        self.at(self.cue("Neredeyse sıfır fiberle", 2.2))
        self.play(Create(cab), FadeIn(cabl), FadeIn(onu), run_time=0.6)
        self.at(self.cue("kayıt burst'ünün varışından", 6.8))
        self.play(FadeIn(eq[0], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("yanıt süresi artı iki kez", 11.9))
        self.play(FadeIn(eq[1:], shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("Otuz dört ile otuz altı", 16.8))
        self.play(FadeIn(ax), FadeIn(ok), FadeIn(okl), run_time=0.5)
        self.play(FadeIn(mk, shift=DOWN * 0.1), run_time=0.3)
        self.at(self.cue("OMCC üzerinden", 21.5))
        self.play(FadeIn(om, shift=LEFT * 0.05), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep16_labA")


class E16LabB(Act16):
    HDR, MANIFEST, PREV_BADGE = H16["L"], M16("lab"), "lab"

    def construct(self):
        # g5 — TEST 4: EqD vs fibre length (0/10/20 km): ≈ −24 400 bit per km (calc); (13-8) vs OTDR within 200 m at 20 km; burst phase within 3.2 ns
        self.beat("g5")
        h = step_head(self, 4, "Fiber uzunluğuna karşı ranging")
        ox, oy, sx, sy = -5.6, -2.3, 0.26, 3.2
        xa = arrow([ox, oy, 0], [ox + 21.5 * sx, oy, 0], MUTED, 2, 0.1)
        ya = arrow([ox, oy, 0], [ox, oy + 3.7, 0], MUTED, 2, 0.1)
        xl = VGroup(*[T(f"{k} km", 15, MUTED, BOLD).next_to([ox + k * sx, oy, 0], DOWN, buff=0.08) for k in (0, 10, 20)])
        yl = T("EqD (bit)", 15, EQC, BOLD).next_to(ya, UP, buff=0.06)
        P = lambda k: np.array([ox + k * sx, oy + sy * (1 - k / 20 * 0.97), 0])
        pts = VGroup(*[Dot(P(k), radius=0.09, color=EQC) for k in (0, 10, 20)])
        sps = VGroup(*[spool(f"{k} km", FEED, 0.3) for k in (0, 10, 20)]).arrange(RIGHT, buff=0.35).move_to([3.7, 1.55, 0])
        spl = T("sırayla takın →", 15, MUTED, BOLD).next_to(sps, LEFT, buff=0.25)
        ln = Line(P(0), P(20), color=EQC, stroke_width=2.5)
        sl = VGroup(tag("hesap", GOLD, 14), T("≈ −24 400 bit / km", 17, EQC, BOLD)).arrange(RIGHT, buff=0.15).next_to(ln.get_center(), UR, buff=0.15)
        cmp_ = VGroup(otdr_icon(1.7, 1.15, "OTDR"), VGroup(T("(13-8) mesafesi ↔ OTDR", 17, TXT, BOLD), T("20 km'de fark ≤ 200 m", 17, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        cmp_.arrange(RIGHT, buff=0.3).move_to([3.7, -0.35, 0])
        ph = VGroup(tag("OLT'de burst fazı", RGC, 16), T("≤ 3,2 ns (8 bit)", 17, GOOD, BOLD)).arrange(RIGHT, buff=0.2).move_to([3.7, -1.9, 0])
        self.play(self.set_src("G.989.3 §13.1.4 · (13-7) · (13-8) · hesap"), Create(xa), Create(ya), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.at(self.cue("Makaraları sırayla", 3.8))
        self.play(FadeIn(spl), run_time=0.2)
        for k in range(3):
            self.play(FadeIn(sps[k], shift=DOWN * 0.05), FadeIn(pts[k], scale=0.5), run_time=0.4)
        self.at(self.cue("kilometre başına", 9.5))
        self.play(Create(ln), FadeIn(sl, shift=UP * 0.05), run_time=0.7)
        self.at(self.cue("Formülün mesafesini OTDR", 15.2))
        self.play(FadeIn(cmp_[0], shift=UP * 0.05), FadeIn(cmp_[1][0]), run_time=0.5)
        self.at(self.cue("iki yüz metre içinde", 19.5))
        self.play(FadeIn(cmp_[1][1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("burst'ün fazı", 23.4))
        self.play(FadeIn(ph, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g6 — TEST 5: quiet-window cost: loaded ONUs, open discovery windows; no burst inside; throughput dip 2 (20 km) / 3.6 (40 km) frames per SN grant; latency spike
        self.beat("g6")
        self.play(FadeOut(VGroup(xa, ya, xl, yl, pts, sps, spl, ln, sl, cmp_, ph)), run_time=0.4)
        h = step_head(self, 5, "Sessiz pencerenin bedeli", h)
        fw = 0.62
        ox, base, top = -5.6, -0.2, 1.4
        fa, FX = frame_axis(18, ox, ox + 18 * fw, base, labels=False)
        fal = T("↑ çerçeveler (125 µs)", 15, MUTED, BOLD).next_to(fa, DOWN, buff=0.1).align_to(fa, RIGHT)
        tl = T("↑ verim", 15, MUTED, BOLD).next_to([ox, top, 0], LEFT, buff=0.1)
        d1, d2 = (3, 5), (10, 13.6)
        pts = [[FX(0), top, 0], [FX(d1[0]), top, 0], [FX(d1[0]), base + 0.1, 0], [FX(d1[1]), base + 0.1, 0], [FX(d1[1]), top, 0],
               [FX(d2[0]), top, 0], [FX(d2[0]), base + 0.1, 0], [FX(d2[1]), base + 0.1, 0], [FX(d2[1]), top, 0], [FX(18), top, 0]]
        tp = VMobject(stroke_color=GOOD, stroke_width=3).set_points_as_corners(pts)
        q1 = Rectangle(width=FX(d1[1]) - FX(d1[0]), height=top - base, stroke_width=0, fill_color=QWC, fill_opacity=0.15).move_to([(FX(d1[0]) + FX(d1[1])) / 2, (top + base) / 2, 0])
        q2 = Rectangle(width=FX(d2[1]) - FX(d2[0]), height=top - base, stroke_width=0, fill_color=QWC, fill_opacity=0.15).move_to([(FX(d2[0]) + FX(d2[1])) / 2, (top + base) / 2, 0])
        l1 = T("20 km: 2 çerçeve", 16, SNC, BOLD).next_to(q1, UP, buff=0.08)
        l2 = T("40 km: 3,6 çerçeve", 16, SNC, BOLD).next_to(q2, UP, buff=0.08)
        nb = VGroup(T("pencerede burst yok", 16, GOOD, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.1).move_to([FX(16.0), 0.6, 0])
        nb.move_to([4.6, 1.95, 0])
        tgi = tg_icon(1.6, 1.1, "yük").move_to([-4.6, -1.95, 0])
        lat = VGroup(T("gecikmeye duyarlı T-CONT:", 16, TXT, BOLD), T("gecikme sıçraması (2–3 BWmap)", 16, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([2.6, -1.95, 0])
        lx = -2.4
        lp = [[lx, -2.6, 0], [lx + 1.0, -2.6, 0], [lx + 1.15, -1.45, 0], [lx + 1.35, -2.6, 0], [lx + 2.6, -2.6, 0]]
        lpl = VMobject(stroke_color=WARN, stroke_width=2.5).set_points_as_corners(lp)
        self.play(self.set_src("G.989.3 §13.1.2 · §13.1.7 · hesap"), Create(fa), FadeIn(fal), FadeIn(tl), run_time=0.5)
        self.at(self.cue("Trafik üreteciyle", 3.2))
        self.play(FadeIn(tgi, shift=UP * 0.05), Create(tp), run_time=0.8)
        self.at(self.cue("keşif pencereleri açın", 6.9))
        self.play(FadeIn(q1), FadeIn(q2), run_time=0.5)
        self.at(self.cue("hiçbir burst düşmemelidir", 9.1))
        self.play(FadeIn(nb, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("yirmi kilometrede iki", 14.5))
        self.play(FadeIn(l1, shift=DOWN * 0.05), Indicate(q1, color=SNC, scale_factor=1.0), run_time=0.5)
        self.at(self.cue("kırk kilometrede üç virgül altı", 18.2))
        self.play(FadeIn(l2, shift=DOWN * 0.05), run_time=0.5)
        self.at(self.cue("Gecikmeye duyarlı", 23.7))
        self.play(Create(lpl), FadeIn(lat, shift=LEFT * 0.05), run_time=0.7)
        self.end(pad=0.05)

        # g7 — TEST 6: drift injection: shift an emulated ONU's burst bit by bit or heat the fibre; DOW → relative Ranging_Time; TIW after 3 corrections
        self.beat("g7")
        self.play(FadeOut(VGroup(fa, fal, tl, tp, q1, q2, l1, l2, nb, tgi, lat, lpl)), run_time=0.4)
        h = step_head(self, 6, "Kayma enjeksiyonu", h)
        ox, oy, sx, sy = -5.6, -1.6, 0.4, 0.11
        xa = arrow([ox, oy, 0], [ox + 25 * sx, oy, 0], MUTED, 2, 0.1)
        ya = arrow([ox, oy, 0], [ox, oy + 24 * sy, 0], MUTED, 2, 0.1)
        xal = T("zaman", 14, MUTED, BOLD).next_to(xa, DOWN, buff=0.06).align_to(xa, RIGHT)
        yal = T("kayma (bit @ 2,5G)", 15, MUTED, BOLD).next_to(ya, UP, buff=0.06)
        P = lambda t, d: [ox + t * sx, oy + d * sy, 0]
        dow = VGroup(DashedLine(P(0, 8), P(24, 8), color=GOLD, stroke_width=2), T("DOW · 8 bit (10G: 32)", 15, GOLD, BOLD))
        dow[1].next_to(P(24, 8), RIGHT, buff=0.1)
        tiw = VGroup(DashedLine(P(0, 16), P(24, 16), color=WARN, stroke_width=2), T("TIW · 16 bit (10G: 64)", 15, WARN, BOLD))
        tiw[1].next_to(P(24, 16), RIGHT, buff=0.1)
        c1 = [P(0, 0), P(1, 1), P(2, 2), P(3, 3), P(4, 4), P(5, 5), P(6, 6), P(7, 7), P(8, 8), P(9, 9), P(9, 0)]
        dr1 = VMobject(stroke_color=ONUC, stroke_width=3).set_points_as_corners(c1)
        cor = VGroup(arrow(P(9, 11), P(9, 9.3), EQC, 2, 0.08), T("göreli Ranging_Time", 14, EQC, BOLD))
        cor[1].next_to(P(9, 11), UP, buff=0.04)
        c2 = [P(9, 0), P(12, 19), P(13, 19), P(13, 17.5), P(15, 20), P(15, 18), P(17, 20), P(17, 18), P(19, 20)]
        dr2 = VMobject(stroke_color=WARN, stroke_width=3).set_points_as_corners(c2)
        fixes = VGroup(*[T(str(k), 14, EQC, BOLD).next_to(P(t, 21), UP, buff=0.0) for k, t in ((1, 13), (2, 15), (3, 17))])
        warn_ = VGroup(tag("3 düzeltmeden sonra hâlâ dışarıda", WARN, 15), T("→ TIW uyarısı", 17, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        warn_.move_to([4.3, 0.55, 0])
        mt = VGroup(tag("emüle ONU: burst'ü bit bit kaydır", ONUC, 15), tag("ya da fiberi ısıt", LDC, 15)).arrange(RIGHT, buff=0.2).move_to([0.6, -2.55, 0])
        self.play(self.set_src("G.989.3 §13.1.6 · Tablo 13-1 · Tablo 14-2 · yöntem: yorum"), Create(xa), Create(ya), FadeIn(xal), FadeIn(yal), run_time=0.5)
        self.at(self.cue("bit bit kaydırın", 3.5))
        self.play(FadeIn(mt[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ya da fiberi ısıtın", 7.0))
        self.play(FadeIn(mt[1], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Kayma iki buçuk gigabitte sekiz", 8.7))
        self.play(Create(dow[0]), FadeIn(dow[1]), Create(dr1), run_time=1.0)
        self.at(self.cue("göreli bir eşitleme", 14.0))
        self.play(GrowArrow(cor[0]), FadeIn(cor[1]), run_time=0.5)
        self.at(self.cue("On altı ya da altmış dört", 18.3))
        self.play(Create(tiw[0]), FadeIn(tiw[1]), Create(dr2), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(f) for f in fixes], lag_ratio=0.3), run_time=0.6)
        self.at(self.cue("iletim girişimi uyarısı", 24.2))
        self.play(FadeIn(warn_, shift=LEFT * 0.05), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep16_labB")


class E16LabC(Act16):
    HDR, MANIFEST, PREV_BADGE = H16["L"], M16("lab"), "lab"

    def construct(self):
        # g8 — TEST 7: timers: withhold EqD → after 10 s back to O2-3 with code 9; O5 without grants → exactly 10 s, no own code; DS flaps → TO6 not reset
        self.beat("g8")
        h = step_head(self, 7, "Zamanlayıcılar")
        x0, sc = -3.2, 0.62

        def lane(y, segs, endtxt, endc):
            g = VGroup()
            for a, b_, n, c in segs:
                r = Rectangle(width=(b_ - a) * sc, height=0.42, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.28).move_to([x0 + (a + b_) / 2 * sc, y, 0])
                g.add(VGroup(r, T(n, 15, TXT, BOLD).move_to(r)))
            e = T(endtxt, 16, endc, BOLD).next_to(g, RIGHT, buff=0.2)
            return VGroup(g, e)
        r1 = lane(1.45, [(0, 10, "O4 · EqD verilmez", RGC), (10, 11.5, "O2-3", SNC)], "debug 1001 = 9", WARN)
        r2 = lane(0.25, [(0, 10, "O5 · hiç tahsis yok", OPC), (10, 11.5, "O1", O1C)], "kendi kodu yok", WARN)
        r3 = lane(-0.95, [(0, 3, "O5", OPC), (3, 4, "O6", LDC), (4, 6.5, "O5", OPC), (6.5, 7.5, "O6", LDC), (7.5, 12, "O5", OPC), (12, 13, "O1", O1C)], "", GOOD)
        lbs = VGroup(*[VGroup(tag(t, TMRC, 16), T(d, 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([-6.6, y, 0], aligned_edge=LEFT)
                       for t, d, y in (("TO1", "önerilen 10 s", 1.45), ("TO6", "zorunlu 10 s", 0.25), ("TO6", "↓ ışık kesintili", -0.95))])
        b10 = VGroup(*[VGroup(DashedLine([x0 + 10 * sc, y + 0.3, 0], [x0 + 10 * sc, y - 0.3, 0], color=GOLD, stroke_width=2), T("10 s", 14, GOLD, BOLD))
                       for y in (1.45, 0.25)])
        for b_, y in zip(b10, (1.45, 0.25)):
            b_[1].next_to([x0 + 10 * sc, y + 0.3, 0], UP, buff=0.03)
        cum = VGroup(T("TO6: O5 süreleri toplanır (3 + 2,5 + 4,5 = 10 s)", 16, GOOD, BOLD), T("O6'da durur · sıfırlanmaz ✓", 16, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cum.move_to([0.5, -2.0, 0])
        cum[0].set_opacity(1)
        hk = tag("örnek", GOLD, 14).next_to(cum, LEFT, buff=0.25)
        self.play(self.set_src("G.989.3 Tablo 12-2 · Tablo 12-4 · Tablo 11-25 (oktet 40) · Amd.1"), run_time=0.3)
        self.at(self.cue("Eşitleme gecikmesini vermeyin", 2.4))
        self.play(FadeIn(lbs[0]), FadeIn(r1[0][0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("önerilen on saniye", 4.9))
        self.play(FadeIn(b10[0]), FadeIn(r1[0][1], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("dokuz koduyla", 9.3))
        self.play(FadeIn(r1[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("O5'teki bir ONU'ya", 11.4))
        self.play(FadeIn(lbs[1]), FadeIn(r2[0][0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("tam on saniye", 14.7))
        self.play(FadeIn(b10[1]), FadeIn(r2[0][1], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("kendine ait bir kod", 18.5))
        self.play(FadeIn(r2[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("kısa kısa kesin", 21.0))
        self.play(FadeIn(lbs[2]), LaggedStart(*[FadeIn(s) for s in r3[0]], lag_ratio=0.12), run_time=0.9)
        self.at(self.cue("sıfırlanmamalı", 24.3))
        self.play(FadeIn(hk), FadeIn(cum[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("kaldığı yerden", 26.9))
        self.play(FadeIn(cum[1], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g9 — TEST 8: ToD: ONU 1PPS vs OLT reference with a time-interval counter at 0/20/40 km; < 9.4 ns general, < 3.2 ns fixed pairing (20 km); wrong ratio → near ONU worst
        self.beat("g9")
        self.play(FadeOut(VGroup(r1, r2, r3, lbs, b10, cum, hk)), run_time=0.4)
        h = step_head(self, 8, "Günün saati", h)
        ct = counter_icon(2.3, 1.55, "Zaman aralığı sayacı", "± 3,1 ns").move_to([0, 1.0, 0])
        ref = VGroup(ct_box("OLT ref.", OLTC, 1.6, 0.5, 15), clock_icon(0.25)).arrange(RIGHT, buff=0.15).move_to([-4.6, 1.3, 0])
        onu = VGroup(onu_box("ONU", ONUC, 1.2, 0.5, 15), T("1PPS", 15, TODC, BOLD)).arrange(RIGHT, buff=0.15).move_to([4.6, 1.3, 0])
        a1 = arrow(ref.get_right(), ct[0].get_left() + UP * 0.25, OLTC, 2, 0.1)
        a2 = arrow(onu.get_left(), ct[0].get_right() + UP * 0.25, TODC, 2, 0.1)
        sp = VGroup(*[spool(s, FEED, 0.24) for s in ("0 km", "20 km", "40 km")]).arrange(RIGHT, buff=0.3).move_to([4.6, -0.2, 0])
        crit = VGroup(T("20 km'de:", 17, MUTED, BOLD), pill("genel < 9,4 ns", TODC, 17), pill("sabit eşleşme < 3,2 ns", GOOD, 17)).arrange(RIGHT, buff=0.25).move_to([-1.0, -1.1, 0])
        xo = -5.3
        bars = VGroup(*[Rectangle(width=0.5, height=v, stroke_color=WARN, stroke_width=1.5, fill_color=WARN, fill_opacity=0.4).move_to([xo + k * 0.75, -2.95 + v / 2, 0])
                        for k, v in enumerate((0.95, 0.75, 0.55, 0.38, 0.22))])
        bl = VGroup(T("ONU'ya bilerek yanlış oran:", 16, TXT, BOLD), T("hata en çok yakın ONU'da büyür", 16, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        bl.next_to(bars, RIGHT, buff=0.35)
        bxl = T("yakın → uzak", 14, MUTED, BOLD).next_to(bars, UP, buff=0.06)
        self.play(self.set_src("G.989.3 §13.2 · Ek II · yöntem: yorum"), run_time=0.3)
        self.at(self.cue("saniye darbesini", 2.6))
        self.play(FadeIn(ct, shift=UP * 0.05), FadeIn(ref), FadeIn(onu), run_time=0.6)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.at(self.cue("sıfır,", 9.4))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.05) for s in sp], lag_ratio=0.3), run_time=0.8)
        self.at(self.cue("hata genel durumda", 12.5))
        self.play(FadeIn(crit[:2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("sabit eşleşmede üç", 16.7))
        self.play(FadeIn(crit[2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("bilerek yanlış bir oran", 22.0))
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(bxl), FadeIn(bl[0]), run_time=0.7)
        self.at(self.cue("yakın ONU'da büyümelidir", 25.0))
        self.play(FadeIn(bl[1], shift=LEFT * 0.05), Indicate(bars[0], color=WARN), run_time=0.5)
        self.end(pad=0.05)

        # g10 — TEST 9: emergency stop: disable with 0xFF, power-cycle, stays dark (power meter); enable with 0x00 → reactivates with code 5; 0x3F only on an O2-3 ONU
        self.beat("g10")
        self.play(FadeOut(VGroup(ct, ref, onu, a1, a2, sp, crit, bars, bl, bxl)), run_time=0.4)
        h = step_head(self, 9, "Acil durdurma", h)
        steps = VGroup(tile("Disable_SN 0xFF = 255", WARN, 2.7, 0.6, 16, 0.2), tile("⏻ güç kes / aç", GOLD, 2.2, 0.6, 16, 0.2),
                       tile("güç ölçer: karanlık", MUTED, 2.5, 0.6, 16, 0.2), tile("0x00 ile serbest bırak", GOOD, 2.7, 0.6, 16, 0.2))
        steps.arrange(RIGHT, buff=0.42).move_to([0, 1.3, 0])
        ars = VGroup(*[arrow(steps[k].get_right(), steps[k + 1].get_left(), MUTED, 2, 0.1) for k in range(3)])
        pm = instr("PM", 2.15, 1.45, "karanlık", None, MUTED).move_to([-2.6, -0.65, 0])
        dk = VGroup(T("O7 güç kesintisinden sağ çıkar", 17, TXT, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.12).next_to(pm, RIGHT, buff=0.4)
        rea = VGroup(T("yeniden aktivasyon · Serial_Number_ONU oktet 40:", 17, TXT, BOLD), HX("0101 = 5", 19, WARN, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.2)
        rea.move_to([0, -2.05, 0])
        dd = VGroup(HX("0x3F = 63", 17, GOLD, BOLD), T("yalnızca keşfi engeller → yalnızca O2-3'teki ONU'da deneyin", 16, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.85, 0])
        self.play(self.set_src("G.989.3 Tablo 11-9 · Tablo 12-1 (O7) · Tablo 11-25 · yöntem: yorum"), run_time=0.3)
        self.at(self.cue("iki yüz elli beşle", 3.5))
        self.play(FadeIn(steps[0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("gücünü kesip açın", 6.7))
        self.play(GrowArrow(ars[0]), FadeIn(steps[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("güç ölçerle", 9.0))
        self.play(GrowArrow(ars[1]), FadeIn(steps[2], shift=RIGHT * 0.05), FadeIn(pm, shift=UP * 0.05), run_time=0.5)
        self.play(FadeIn(dk, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Sıfırla serbest", 12.6))
        self.play(GrowArrow(ars[2]), FadeIn(steps[3], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("beş kodunu", 17.0))
        self.play(FadeIn(rea, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Altmış üçü", 19.8))
        self.play(FadeIn(dd, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g11 — lab note
        self.note11("g11", [("1", "Her aktivasyonu tam kaydedin",
                             "hata ayıklama kodu · zamanlayıcı süreleri · eşitleme gecikmesi: aynı satırda", "her aktivasyonu tam"),
                            ("2", "Değeri olmayan zamanlayıcıları ölçüp belgeleyin",
                             "TO2 … TO5, AMCC keşif süresi: birlikte çalışabilirlik testinde ilk soru bunlar", "değeri standartta olmayan")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep16_labC")


POINTS = [("ONU 8 adımda uyanır: O1 → O2-3 → O4 → O5\nAmd.2: aktivasyon kararı · Amd.1: TO6 düzeltmesi", "§12.1 · Tablo 12-4"),
          ("Tek zorunlu aktivasyon zamanlayıcısı: TO6 = 10 s\nTO2 … TO5: değer yok", "Tablo 12-2"),
          ("Serial_Number_ONU: rastgele gecikme (0–48 µs)\nve oktet 40 hata ayıklama kodu", "Tablo 11-25"),
          ("Keşif penceresi 250 µs · ranging 202 µs (20 km)\nEqD 1 bit @ 2,5G · kayma: DOW / TIW", "§13.1 · Tablo 13-1"),
          ("Günün saati: (N, Tstamp) · 20 km'de\n± 9,4 ns genel · ± 3,2 ns sabit eşleşme", "§13.2 · Ek II")]


class E16End(Act16):
    HDR, MANIFEST, FIRST = H16["E"], M16("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header(tc)
        self.set_badge("ozet")
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.4)
            ch = tag(c, GOLD, 16)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.75, -2.4, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.6, y, 0])
        for k, (key, d) in enumerate((("ONU sekiz adımda", 1.5), ("tek zorunlu aktivasyon", 14.0), ("seri numarası mesajı rastgele", 21.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((3, 4), (("keşif penceresi", 0.4), ("günün saati bir çerçeve", 16.1))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Değeri zorunlu tek aktivasyon\nzamanlayıcısı hangisi, değeri ne,\n2023 değişikliği onda neyi\ndeğiştirdi?", CH[0]),
            ("L min = 0, D maks = 40 km:\nönerilen SN penceresi kaç µs,\nparçaları nereden gelir,\nneden 10G'de de aynı?", CH[1]),
            ("20 km'de günün saati hatası\nneden sabit eşleşmede ± 3,2,\ngenel durumda ± 9,4 ns?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 13.0), ("Üçüncü soru", 26.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 38.3))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: Renk Değiştirmek (channel management, handover, locking, bonding; O8/O9 step by step)
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e7 = SERIES["season2"]["episodes"][6]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e7['n']} · {e7['title']}", 50, TXT, BOLD), T(e7["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        fit(nxt[1], 12.6)
        ch = VGroup(*[tile(n, c, 1.3, 0.55, 18, 0.25) for n, c in (("O5", OPC), ("O8", TUC), ("O9", TUC), ("O5", OPC))]).arrange(RIGHT, buff=0.55).move_to([0, -1.0, 0])
        ca = VGroup(*[arrow(ch[k].get_right(), ch[k + 1].get_left(), MUTED, 2, 0.1) for k in range(3)])
        lam = VGroup(VGroup(Rectangle(width=0.5, height=0.18, stroke_width=0, fill_color=CH[0], fill_opacity=0.9), T("λ1", 16, CH[0], BOLD)).arrange(RIGHT, buff=0.1).next_to(ch[0], DOWN, buff=0.15),
                     VGroup(Rectangle(width=0.5, height=0.18, stroke_width=0, fill_color=CH[2], fill_opacity=0.9), T("λ3", 16, CH[2], BOLD)).arrange(RIGHT, buff=0.1).next_to(ch[3], DOWN, buff=0.15))
        tg_ = VGroup(*[tag(s, TUC, 16) for s in ("kanal yönetimi", "devir", "kilitleme", "bağlama")]).arrange(RIGHT, buff=0.2).move_to([0, -2.35, 0])
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("Kanal yönetimi", 3.0))
        self.play(FadeIn(nxt[2]), FadeIn(tg_[0], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("devir,", 4.2))
        self.play(FadeIn(tg_[1], shift=UP * 0.06), run_time=0.3)
        self.at(self.cue("kilitleme ve bağlama", 4.8))
        self.play(FadeIn(tg_[2:], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("O8 ve O9'u", 7.5))
        self.play(LaggedStart(*[FadeIn(c) for c in ch], lag_ratio=0.15), LaggedStart(*[GrowArrow(a) for a in ca], lag_ratio=0.15), run_time=0.9)
        self.at(self.cue("bir renkten ötekine", 11.5))
        self.play(FadeIn(lam[0]), run_time=0.3)
        self.play(TransformFromCopy(lam[0], lam[1]), run_time=0.8)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(ch, ca, lam, tg_)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP16['n']} · {EP16['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep16_end")
