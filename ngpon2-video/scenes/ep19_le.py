"""S2·B9 · Laboratuvarda (çözücü öz sınaması Ek IV.10 + bizim MIC'lerimiz, izin kapısı, durumlara göre güç, uyuyan ONU, uyanma gecikmesi ve
FWI, OLT makinesi, sayaçlar ve hata enjeksiyonu, kusur enjeksiyonu, kalan kusurlar, son nefes) and Kapanış."""
from ep19_common import *

ALLOC = [("Alloc-ID", 14, ACC), ("DBRu", 1, GOLD), ("PLOAMu", 1, GOLD), ("StartTime", 16, "#60A5FA"), ("GrantSize", 16, "#60A5FA"),
         ("FWI", 1, FWIC), ("Profil", 2, "#C084FC"), ("HEC", 13, HECC)]


class LabAct(Act19):
    def next_test(self, n, title, h, rt=0.4):
        keep = {self.hdr, self.badge, h}
        out = [m for m in self.mobjects if m not in keep]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=rt)
        if self.src is not None and self.src in out:
            self.src = None
        return step_head(self, n, title, h)


def exp(s, ok=True, size=16):
    """Expected outcome line: ✓ / ✗ + text."""
    return VGroup(ok_x(ok, size + 2), T(s, size, TXT, BOLD)).arrange(RIGHT, buff=0.12)


def wire(a, b, color=FEED, sw=2.2, dashed=False):
    return (DashedLine(a, b, color=color, stroke_width=sw, dash_length=0.08) if dashed else Line(a, b, color=color, stroke_width=sw))


class E19LabA(LabAct):
    HDR, MANIFEST, FIRST = H19["L"], M19("lab"), True

    def construct(self):
        # g1 — bench: OLT + ONU emulator, protocol analyzer, traffic generator, BERT + variable attenuator, optical switch on the feeder, data logger
        #      for the ONU supply current; set and record every parameter whose value is not in the standard
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Uyku, sayaçlar ve kusurlar")
        self.at(self.cue("Düzenek", 1.2))
        h = self.heading("Düzenek")
        self.to_header_badge(tc, "lab", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        y1, y2 = 1.25, -1.0
        olt = emu_icon(1.45, 1.0, "OLT emülatörü").move_to([-5.7, y1, 0])
        osw = oswitch_icon(0.55, FEED, "optik anahtar").move_to([-3.95, y1 - 0.08, 0])
        osw[3].next_to(VGroup(osw[0], osw[1]), UP, buff=0.12)
        voa = inst("VOA", "zayıflatıcı", 1.15, 0.85, "dB ↕", c1=GOLD).move_to([-2.45, y1, 0])
        sp = splitter(0.3).move_to([-1.05, y1, 0])
        dut = onu_box("ONU", ONUC, 1.15, 0.55, 17).move_to([0.55, y1, 0])
        tg = tg_icon(1.45, 1.0, "Trafik üreteci").move_to([2.75, y1, 0])
        bert = inst("BERT", "BERT", 1.45, 1.0, "BER").move_to([5.0, y1, 0])
        f1 = wire(olt[0].get_right(), [osw[0].get_x(), y1, 0])
        f2 = wire([osw[1].get_x(), y1, 0], voa[0].get_left())
        f3 = wire(voa[0].get_right(), sp.get_left())
        d1 = wire(sp.get_right(), dut[0].get_left())
        u1 = wire(dut[0].get_right(), tg[0].get_left(), GOOD, 2.0, True)
        u2 = wire(tg[0].get_right(), bert[0].get_left(), GOOD, 2.0, True)
        pa = pa_icon(1.45, 1.0, "Protokol analizörü").move_to([-4.3, y2, 0])
        tp = wire([-3.25, y1, 0], pa[0].get_top(), MUTED, 1.6, True)
        emo = emu_icon(1.45, 1.0, "ONU emülatörü").move_to([-1.05, y2, 0])
        d2 = wire(sp.get_bottom(), emo[0].get_top())
        lg = logger_icon(1.45, 1.0, "Veri kaydedici").move_to([2.2, y2, 0])
        cur = wire(dut[0].get_bottom(), [dut[0].get_x(), y2, 0], GOLD, 1.8, True)
        cur2 = wire([dut[0].get_x(), y2, 0], lg[0].get_left(), GOLD, 1.8, True)
        cl = T("besleme akımı", 14, GOLD, BOLD).next_to(cur, LEFT, buff=0.08)
        rec = VGroup(T("standartta değeri olmayan her parametre → emülatörde kur ve kaydet:", 16, TXT, BOLD),
                     VGroup(*[tag(s, TMRC, 14) for s in ("Ilowpower", "Iaware", "Irxoff", "Ihold", "Itransinit", "Ter_i", "Talerted", "Clob_i")]).arrange(RIGHT, buff=0.1))
        rec.arrange(DOWN, buff=0.15)
        fit(rec, 12.6).move_to([0, -2.7, 0])
        self.at(self.cue("bir OLT ve ONU emülatörü", 1.9))
        self.play(FadeIn(olt, shift=UP * 0.1), Create(f1), FadeIn(sp), Create(d1), FadeIn(dut), Create(d2), FadeIn(emo, shift=UP * 0.1),
                  self.set_src("G.989.3 §16 · §14 · tezgâh ve yöntemler: yorum"), run_time=0.7)
        self.at(self.cue("bir protokol analizörü", 4.0))
        self.play(Create(tp), FadeIn(pa, shift=UP * 0.1), run_time=0.45)
        self.at(self.cue("bir trafik üreteci", 5.9))
        self.play(Create(u1), FadeIn(tg, shift=UP * 0.1), run_time=0.45)
        self.at(self.cue("bir BERT ve ayarlı", 7.5))
        self.play(Create(u2), FadeIn(bert, shift=UP * 0.1), FadeIn(voa), Create(f3), run_time=0.5)
        self.at(self.cue("besleyici fiberde bir optik", 10.1))
        self.play(FadeIn(osw), Create(f2), run_time=0.4)
        self.at(self.cue("besleme akımını kaydeden", 13.1))
        self.play(Create(cur), Create(cur2), FadeIn(cl), FadeIn(lg, shift=UP * 0.1), run_time=0.55)
        self.at(self.cue("Değeri standartta olmayan", 17.8))
        self.play(FadeIn(rec[0], shift=UP * 0.05), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in rec[1]], lag_ratio=0.1), run_time=0.7)
        self.end(pad=0.05)

        # g2 — TEST 1: decoder self-test: App IV.10 is exactly a Sleep_Request(WSleep): ONU-ID 0x13 (19), SeqNo 0x00, Activity_level 0x03, MIC must
        #      match the appendix bytes; then our own MICs (Sleep_Request Awake, Sleep_Allow ON/OFF, broadcast Power_Consumption_Inquire) — not golden
        self.beat("g2")
        h = self.next_test(1, "Çözücünün öz sınaması", h)
        p = apanel(12.6, 2.35, "Analizör · Ek IV.10 · ↑ PLOAM", GOOD).move_to([0, 1.0, 0])
        top = panel_top(p, 0.2)
        r1 = VGroup(kv("ONU-ID", "0x0013", 16, 17, kw=1.3), T("= 19", 16, MUTED, BOLD))
        r2 = VGroup(kv("tür", "0x10", 16, 17, kw=0.7), T("Sleep_Request", 16, MUTED, BOLD))
        r3 = VGroup(kv("SeqNo", "0x00", 16, 17, kw=1.0))
        r4 = VGroup(kv("Activity_level", "0x03", 16, 17, kw=1.7), T("WSleep", 16, SRW, BOLD))
        for r in (r1, r2, r4):
            r[1].next_to(r[0], RIGHT, buff=0.15)
        row = VGroup(r1, r2, r3, r4).arrange(RIGHT, buff=0.5)
        fit(row, 12.0).move_to([0, top - 0.25, 0])
        mic = VGroup(T("MIC", 16, MICC, BOLD), HX("fe af 8d 09 20 8f 0d 9b", 18, MICC, BOLD), T("= Ek IV.10", 16, TXT, BOLD), ok_x(True, 20), tag("altın vektör", GOOD, 15)).arrange(RIGHT, buff=0.2)
        mic.move_to([0, top - 0.95, 0])
        ours = mtable(["bizim mesajımız", "ONU-ID · SeqNo · anahtar", "MIC (bizim hesabımız)"],
                      [["Sleep_Request (Awake) ↑", "0x13 · 0x00 · IV.8 PLOAM_IK", "b36c661bff3b66e1"],
                       ["Sleep_Allow (ON) ↓", "0x13 · 0x05 · IV.8 PLOAM_IK", "96530b1c3a61dc8f"],
                       ["Sleep_Allow (OFF) ↓", "0x13 · 0x06 · IV.8 PLOAM_IK", "601a191779311611"],
                       ["Power_Consumption_Inquire ↓ · yayın", "0x3FF · 0x02 · varsayılan", "1a809e0895f83834"]],
                      [4.6, 4.0, 3.4], size=16, hsize=15, row_h=0.4, mono=(2,)).move_to([0, -1.55, 0])
        ng = tag("altın vektör değil", WARN, 15).next_to(ours, DOWN, buff=0.1).align_to(ours, RIGHT)
        self.play(FadeIn(p), self.set_src("G.989.3 Ek IV.10 · Tablo 11-29 / 11-13 / 11-22 · ek MIC'ler: bizim hesabımız (S2·B9)"), run_time=0.45)
        self.at(self.cue("Dördüncü ekin onuncu", 2.6))
        self.play(FadeIn(r2, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("ONU kimliği on dokuz", 8.3))
        self.play(FadeIn(r1, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("sıra numarası sıfır", 10.1))
        self.play(FadeIn(r3, shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("etkinlik düzeyi üç", 11.8))
        self.play(FadeIn(r4, shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("ekteki sekiz baytla", 13.4))
        self.play(FadeIn(mic[:3], shift=UP * 0.05), run_time=0.4)
        self.play(FadeIn(mic[3:], scale=1.1), run_time=0.3)
        self.at(self.cue("kendi hesapladığımız kodları", 17.2))
        self.play(FadeIn(ours[0]), run_time=0.3)
        for idx, key, d in (((1,), "uyanık isteği", 20.8), ((2, 3), "açık ve kapalı uyku", 22.0), ((4,), "yayın güç sorgusu", 24.1)):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(ours[i], shift=RIGHT * 0.05) for i in idx], run_time=0.35)
        self.at(self.cue("altın vektör değildir", 25.7))
        self.play(FadeIn(ng, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g3 — TEST 2: permission gate: PM not enabled via OMCI → SA(ON) must be ignored; enabled → SR(WSleep) must not come before Ihold; read the
        #      Sleep_Allow / Sleep_Request counters: optional, but if present they must increment
        self.beat("g3")
        h = self.next_test(2, "İzin kapısı", h)
        X0, X1 = -3.4, 6.2
        ya, yb = 1.15, -0.55
        la = VGroup(T("OMCI: güç yönetimi", 15, MUTED, BOLD), T("etkin değil", 17, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.3, ya, 0])
        lb = VGroup(T("OMCI: güç yönetimi", 15, MUTED, BOLD), T("etkin", 17, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.3, yb, 0])
        ta = Line([X0, ya, 0], [X1, ya, 0], color=LINE, stroke_width=2)
        tb_ = Line([X0, yb, 0], [X1, yb, 0], color=LINE, stroke_width=2)
        sa1 = vmsg(X0 + 0.6, ya + 0.6, ya + 0.05, "SA(ON) ↓", SAON, 15)
        ig = exp("ONU yok sayar · cevap yok", True, 16).move_to([2.3, ya + 0.3, 0])
        sa2 = vmsg(X0 + 0.6, yb + 0.6, yb + 0.05, "SA(ON) ↓", SAON, 15)
        th = tbar(X0 + 0.6, X0 + 4.6, yb - 0.25, "Thold ≥ Ihold", TMRC, 0.16, 14, DOWN)
        sr = vmsg(X0 + 5.3, yb - 0.05, yb + 0.6, "SR(WSleep) ↑ · 0x03 · SeqNo 0x00", SRW, 15)
        ok2 = exp("Ihold'dan önce gelmez", True, 16).next_to(th, DOWN, buff=0.45).align_to(th, LEFT)
        cn = VGroup(T("sayaçlar (Tablo 14-1 · O):", 16, MUTED, BOLD), tag("Sleep_Allow", FAM["pm"], 15), tag("Sleep_Request", FAM["pm"], 15),
                    T("→ varsa artmalı", 17, GOOD, BOLD)).arrange(RIGHT, buff=0.2)
        fit(cn, 12.6).move_to([0, -2.75, 0])
        self.play(self.set_src("G.989.3 Tablo 11-2 (Sleep_Allow) · Tablo 16-4 NOT · Tablo 11-29 · Tablo 14-1"), run_time=0.3)
        self.at(self.cue("etkinleştirilmemişken açık uyku", 4.0))
        self.play(FadeIn(la), Create(ta), GrowArrow(sa1[0]), FadeIn(sa1[1]), run_time=0.5)
        self.at(self.cue("ONU yok saymalıdır", 7.8))
        self.play(FadeIn(ig, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Etkinleştirip tekrarlayın", 9.3))
        self.play(FadeIn(lb), Create(tb_), GrowArrow(sa2[0]), FadeIn(sa2[1]), GrowFromEdge(th[0], LEFT), FadeIn(th[1]), run_time=0.6)
        self.at(self.cue("tutma aralığından önce", 13.0))
        self.play(GrowArrow(sr[0]), FadeIn(sr[1]), FadeIn(ok2, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("uyku isteği sayaçlarını", 16.3))
        self.play(FadeIn(cn[:3], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ama varsa artmalıdırlar", 22.2))
        self.play(FadeIn(cn[3], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g4 — TEST 3: power per state: in the burst log Aware periods show bursts, LowPower periods gaps — compare with the intervals; Rx checks are
        #      not visible optically but in the supply current; measure mean power per state, compare with our model and the low-power-time counter
        self.beat("g4")
        h = self.next_test(3, "Durumlara göre güç", h)
        x0, x1 = -4.6, 6.3
        yo, yc = 1.05, -0.85
        lo = VGroup(T("↑ burst günlüğü", 16, TXT, BOLD), T("analizör · optik", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.75, yo, 0])
        lc = VGroup(T("besleme akımı", 16, GOLD, BOLD), T("veri kaydedici", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.75, yc, 0])
        aw = [(x0, x0 + 0.7), (x0 + 4.2, x0 + 4.9), (x0 + 8.4, x0 + 9.1)]
        bx = []
        for a, b in aw:
            bx += list(np.arange(a + 0.08, b - 0.02, 0.17))
        bursts = burst_row(bx, yo, ONUC, 0.09, 0.42, 0.85)
        base = Line([x0, yo - 0.25, 0], [x1, yo - 0.25, 0], color=LINE, stroke_width=1.4)
        pts = [[x0, yc + 0.7, 0]]
        for i, (a, b) in enumerate(aw):
            if i:
                pts += [[a, yc, 0], [a, yc + 0.7, 0]]
            pts += [[b, yc + 0.7, 0], [b, yc, 0]]
            nxt = aw[i + 1][0] if i + 1 < len(aw) else x1
            for c in np.arange(b + 0.85, nxt - 0.3, 0.85):
                pts += [[c, yc, 0], [c, yc + 0.32, 0], [c + 0.06, yc + 0.32, 0], [c + 0.06, yc, 0]]
        pts.append([x1, yc, 0])
        cur = VMobject(stroke_color=GOLD, stroke_width=2.6).set_points_as_corners(pts)
        bd = VGroup(*[DashedLine([a, yo + 0.35, 0], [a, yc - 0.15, 0], color=LINE, stroke_width=1.2, dash_length=0.06) for a, _ in aw[1:]])
        la = VGroup(brace_lbl(Line([aw[0][0], yo + 0.3, 0], [aw[0][1], yo + 0.3, 0]), "farkında", TNC, UP, 14, 0.02),
                    brace_lbl(Line([aw[0][1], yo + 0.3, 0], [aw[1][0], yo + 0.3, 0]), "düşük güç · boşluk", RLC, UP, 14, 0.02))
        cmpi = VGroup(T("≥ Iaware", 15, TMRC, BOLD).next_to(la[0], UP, buff=0.04), T("≤ Ilowpower", 15, TMRC, BOLD).next_to(la[1], UP, buff=0.04))
        rxk = VGroup(arrow([aw[0][1] + 1.7 + 0.5, yc + 0.85, 0], [aw[0][1] + 1.7 + 0.08, yc + 0.38, 0], ACC, 1.8, 0.1),
                     T("alıcı kontrolleri: yalnızca akımda", 15, ACC, BOLD).next_to([aw[0][1] + 2.2, yc + 0.85, 0], RIGHT, buff=0.06))
        res = VGroup(T("durum başına ortalama güç", 17, TXT, BOLD), T("↔", 18, MUTED, BOLD), tag("bizim modelimiz", GOLD, 15), T("↔", 18, MUTED, BOLD),
                     tag("düşük güç süresi sayacı (O)", MUTED, 15)).arrange(RIGHT, buff=0.18)
        fit(res, 12.6).move_to([0, -2.6, 0])
        self.play(FadeIn(lo), FadeIn(lc), Create(base), self.set_src("G.989.3 Tablo 16-1 / 16-2 · Tablo 14-1 (Energy conservation) · yöntem: yorum"), run_time=0.45)
        self.at(self.cue("Burst günlüğünde farkında", 2.6))
        self.play(FadeIn(bursts), FadeIn(la[0]), run_time=0.5)
        self.at(self.cue("düşük güç dönemleri boşluklarla", 6.7))
        self.play(FadeIn(la[1]), run_time=0.35)
        self.at(self.cue("süreleri aralıklarla", 10.0))
        self.play(FadeIn(cmpi, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Alıcı kontrolleri optikte", 13.0))
        self.play(Create(cur), FadeIn(bd), run_time=1.0)
        self.at(self.cue("besleme akımında görünür", 15.7))
        self.play(GrowArrow(rxk[0]), FadeIn(rxk[1]), run_time=0.4)
        self.at(self.cue("ortalama gücünü ölçün", 17.8))
        self.play(FadeIn(res[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("bizim modelimizle", 20.7))
        self.play(FadeIn(res[1:3], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("düşük güç süresi sayacıyla", 22.2))
        self.play(FadeIn(res[3:], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)
        self.save_timeline("ep19_labA")


class E19LabB(LabAct):
    HDR, MANIFEST, PREV_BADGE = H19["L"], M19("lab"), "lab"

    def construct(self):
        # g5 — TEST 4: the sleeping ONU: grants asking for PLOAM and status reports in LowPower → no reply; DS traffic → not forwarded; send a PLOAM
        #      request and see whether your OLT allows extra time or wakes the ONU first
        self.beat("g5")
        h = step_head(self, 4, "Uyuyan ONU")
        st = pst("N", 4, 2.6, 0.8, 18, 14).move_to([-4.6, 1.3, 0])
        rx = VGroup(rx_icon(False, 0.34), T("alıcı kapalı · verici kapalı", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.12).next_to(st, DOWN, buff=0.15)
        t1 = VGroup(mbox("tahsis · PLOAMu = 1 · DBRu = 1", ACC, 3.9, 0.42, 15), T("→", 18, MUTED, BOLD), exp("cevap yok", True, 16)).arrange(RIGHT, buff=0.2)
        t2 = VGroup(mbox("↓ trafik ONU'ya", GOOD, 3.9, 0.42, 15), T("→", 18, MUTED, BOLD), exp("UNI'ye iletilmez", True, 16)).arrange(RIGHT, buff=0.2)
        tt = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.1, 1.05, 0])
        pq = VGroup(mbox("PLOAM isteği ↓", PLC, 2.4, 0.42, 15)).move_to([-4.6, -1.3, 0])
        b1 = VGroup(T("OLT ek süre tanır mı?", 16, TXT, BOLD), T("> 750 µs bekler", 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([0.2, -0.85, 0])
        b2 = VGroup(T("ya da önce uyandırır mı?", 16, TXT, BOLD), T("FWI → SR(Awake) → PLOAM", 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([0.2, -1.95, 0])
        ar = VGroup(arrow(pq.get_right(), b1.get_left() + LEFT * 0.1, PLC, 2, 0.1), arrow(pq.get_right(), b2.get_left() + LEFT * 0.1, PLC, 2, 0.1))
        rec = tag("tavsiye (§16.1.4): önce uyandır", GOOD, 15).next_to(b2, RIGHT, buff=0.35)
        ob = tag("gözlem: OLT'nizin davranışı", GOLD, 15).next_to(b1, RIGHT, buff=0.35)
        self.play(FadeIn(st), FadeIn(rx), self.set_src("G.989.3 §16.1.4 · §11.1.2 · Tablo 16-2"), run_time=0.45)
        self.at(self.cue("PLOAM ve durum raporu isteyen", 2.1))
        self.play(FadeIn(t1[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("cevap gelmemelidir", 7.3))
        self.play(FadeIn(t1[1:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("aşağı yön trafiği gönderin", 8.9))
        self.play(FadeIn(t2[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("iletilmemelidir", 11.8))
        self.play(FadeIn(t2[1:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Bir PLOAM isteği gönderin", 13.2))
        self.play(FadeIn(pq, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("ek süre tanıyıp", 15.3))
        self.play(GrowArrow(ar[0]), FadeIn(b1), FadeIn(ob), run_time=0.45)
        self.at(self.cue("önce ONU'yu uyandırıp", 18.9))
        self.play(GrowArrow(ar[1]), FadeIn(b2), FadeIn(rec), run_time=0.45)
        self.end(pad=0.05)

        # g6 — TEST 5: wake-up latency and FWI: FWI in the first allocation structure of the series → SR(Awake) within Rx check interval + wake-up +
        #      round trip; FWI only in later structures → the ONU must not wake; SA(OFF) alone → measure the miss rate; then ONU-side traffic
        self.beat("g6")
        h = self.next_test(5, "Uyanma gecikmesi ve FWI", h)
        spec = [(n if b > 2 else "", b, c) for n, b, c in ALLOC]
        st = fields(spec, 11.0, 0.5, 15, 14, show_w=True, unit="").move_to([0.4, 1.4, 0])
        for i, tier in ((1, 0), (2, 1), (5, 0), (6, 1)):
            r = st[i][0]
            t = T(ALLOC[i][0], 14, ALLOC[i][2], BOLD).move_to([r.get_x(), r.get_top()[1] + 0.2 + 0.28 * tier, 0])
            st[i][1].add(t, Line(r.get_top(), [r.get_x(), t.get_bottom()[1] - 0.02, 0], color=ALLOC[i][2], stroke_width=1.2))
        stl = T("tahsis yapısı", 15, MUTED, BOLD).next_to(st, LEFT, buff=0.15)
        fw = SurroundingRectangle(st[5][0], color=FWIC, buff=0.06, stroke_width=2.6)

        def series(y, first, rest, label):
            cells = VGroup()
            for k in range(4):
                on = first if k == 0 else rest
                r = Rectangle(width=1.2, height=0.42, stroke_color=ACC, stroke_width=1.6, fill_color=ACC, fill_opacity=0.12)
                b = VGroup(r, T(f"#{k + 1}", 14, MUTED, BOLD).move_to(r).shift(LEFT * 0.3),
                           T("FWI=1" if on else "FWI=0", 14, FWIC if on else MUTED, BOLD).move_to(r).shift(RIGHT * 0.2))
                cells.add(b)
            cells.arrange(RIGHT, buff=0.06).move_to([-3.3, y, 0])
            lab = T(label, 15, TXT, BOLD).next_to(cells, UP, buff=0.08).align_to(cells, LEFT)
            return VGroup(cells, lab)
        s1 = series(0.35, True, False, "seri · FWI ilk yapıda")
        s2 = series(-1.2, False, True, "seri · FWI yalnızca sonrakilerde")
        lat = stack_bar([(2.4, "≤ Irxoff", ACC), (1.0, "Itransinit", TNC), (0.4, "", "#60A5FA")], 0.0, 0.35, 0.42, 14, 1.0)
        latl = VGroup(T("→ SR(Awake)", 16, SRA, BOLD), T("+ RTT", 14, "#60A5FA", BOLD)).arrange(RIGHT, buff=0.15).next_to(lat, RIGHT, buff=0.15)
        no = exp("ONU uyanmamalı", True, 16).move_to([1.6, -1.05, 0])
        sa = VGroup(T("FWI yok · yalnızca SA(OFF) ↓", 16, SAOFF, BOLD), T("→ kaçırma oranı = ? (ölç)", 16, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([-1.0, -2.3, 0])
        lw = VGroup(T("son:", 15, MUTED, BOLD), T("ONU tarafında trafik → LWI → SR(Awake)", 16, ONUC, BOLD)).arrange(RIGHT, buff=0.15).move_to([-1.0, -2.85, 0])
        self.play(FadeIn(st), FadeIn(stl), self.set_src("G.989.3 §8.1.1.2.5 · Şekil 8-2 · Tablo 16-4 / 16-5 · yöntem: yorum"), run_time=0.45)
        self.at(self.cue("Biti serinin ilk tahsis", 4.7))
        self.play(Create(fw), FadeIn(s1, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("uyanık isteği,", 8.1))
        self.play(FadeIn(latl[0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("kontrol aralığı,", 9.3))
        self.play(GrowFromEdge(lat[0], LEFT), run_time=0.35)
        self.at(self.cue("uyanma süresi ve gidiş", 10.6))
        self.play(GrowFromEdge(lat[1], LEFT), GrowFromEdge(lat[2], LEFT), FadeIn(latl[1]), latl.animate.next_to(lat, RIGHT, buff=0.15), run_time=0.5)
        self.at(self.cue("Biti yalnızca sonraki", 15.4))
        self.play(FadeIn(s2, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("ONU uyanmamalıdır", 18.6))
        self.play(FadeIn(no, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Bit olmadan yalnızca", 20.2))
        self.play(FadeIn(sa[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("kaçırma oranını ölçün", 23.7))
        self.play(FadeIn(sa[1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("ONU tarafında trafik", 25.8))
        self.play(FadeIn(lw, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g7 — TEST 6: the OLT machine with an ONU emulator: go silent in LowPowerWatch → SA(OFF) at Ter_i expiry, LOBi after Clob_i misses; ignore
        #      the FWI → after Talerted the OLT returns to AwakeForced without a message; send a stale SR(WSleep) to AwakeForced → SA(OFF) repeated (Note 1)
        self.beat("g7")
        h = self.next_test(6, "OLT makinesi — ONU emülatörüyle", h)
        X0, X1 = -3.0, 6.3
        rows_y = (1.3, -0.25, -1.8)
        labs = [("emülatör susar", "(3) düşük güç gözetiminde"), ("FWI'yi yok sayar", "(4) uyarılmış"), ("gecikmiş SR(WSleep)", "(1) zorla uyanık")]
        L = VGroup(*[VGroup(T(a, 16, ONUC, BOLD), T(b, 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-5.15, y, 0]) for (a, b), y in zip(labs, rows_y)])
        y = rows_y[0]
        a1 = VGroup(sseg(X0, X0 + 3.4, y, "L", 3, 0.45, 14), sseg(X0 + 3.4, X1, y, "L", 1, 0.45, 14))
        a_t = tbar(X0 + 0.1, X0 + 3.4, y + 0.35, "Ter_i", TMRC, 0.12, 14, UP)
        a_m = VGroup(T("SA(OFF) ↓", 15, SAOFF, BOLD).next_to([X0 + 3.4, y - 0.25, 0], DOWN, buff=0.08))
        a_x = VGroup(*[T("✗", 15, WARN, BOLD).move_to([X0 + 4.4 + 0.45 * k, y - 0.42, 0]) for k in range(4)])
        a_l = tag("LOBi · Clob_i (4)", WARN, 15).move_to([X0 + 4.4 + 0.45 * 3 + 1.3, y - 0.42, 0])
        y = rows_y[1]
        b1 = VGroup(sseg(X0, X0 + 3.8, y, "L", 4, 0.45, 14), sseg(X0 + 3.8, X1, y, "L", 1, 0.45, 14))
        b_f = tick_row([X0 + 0.25 + 0.3 * k for k in range(12)], y - 0.33, FWIC, 0.14, 2.4)
        b_t = tbar(X0 + 0.1, X0 + 3.8, y + 0.35, "Talerted", TMRC, 0.12, 14, UP)
        b_m = T("mesaj yok", 15, MUTED, BOLD).next_to([X0 + 3.8, y - 0.25, 0], DOWN, buff=0.08).shift(RIGHT * 0.6)
        y = rows_y[2]
        c1 = VGroup(sseg(X0, X1, y, "L", 1, 0.45, 14))
        c_m = vmsg(X0 + 1.5, y + 0.75, y + 0.25, "SR(WSleep) ↑ · gecikmiş", SRW, 14)
        c_o = vmsg(X0 + 3.2, y - 0.25, y - 0.7, "SA(OFF) ↓ yinelenir", SAOFF, 14)
        c_n = tag("Tablo 16-7 · Not 1", GOLD, 14).move_to([X0 + 7.0, y - 0.55, 0])
        self.play(FadeIn(L[0]), FadeIn(a1[0]), self.set_src("G.989.3 Tablo 16-5 / 16-7 (Not 1) · Tablo 16-1 · Tablo 14-2"), run_time=0.45)
        self.at(self.cue("el sıkışma zamanlayıcısı dolunca", 6.3))
        self.play(GrowFromEdge(a_t[0], LEFT), FadeIn(a_t[1]), run_time=0.45)
        self.play(FadeIn(a1[1], shift=RIGHT * 0.05), FadeIn(a_m), run_time=0.4)
        self.at(self.cue("eşik kadar kaçırmadan sonra", 10.1))
        self.play(LaggedStart(*[FadeIn(x, scale=1.3) for x in a_x], lag_ratio=0.2), run_time=0.6)
        self.play(FadeIn(a_l, scale=0.9), run_time=0.3)
        self.at(self.cue("Uyandırma bitini yok sayın", 14.4))
        self.play(FadeIn(L[1]), FadeIn(b1[0]), LaggedStart(*[Create(t) for t in b_f], lag_ratio=0.06), run_time=0.7)
        self.at(self.cue("uyarı zamanlayıcısından sonra", 16.6))
        self.play(GrowFromEdge(b_t[0], LEFT), FadeIn(b_t[1]), run_time=0.45)
        self.play(FadeIn(b1[1], shift=RIGHT * 0.05), FadeIn(b_m), run_time=0.4)
        self.at(self.cue("gecikmiş bir uyku isteği", 22.3))
        self.play(FadeIn(L[2]), FadeIn(c1), GrowArrow(c_m[0]), FadeIn(c_m[1]), run_time=0.5)
        self.at(self.cue("kapalı izin yinelenmelidir", 26.9))
        self.play(GrowArrow(c_o[0]), FadeIn(c_o[1]), FadeIn(c_n), run_time=0.45)
        self.end(pad=0.05)

        # g8 — TEST 7: counters and error injection: known number of frames → XGEM counters exact; FEC off + attenuator → BIP-32 errors match the BERT;
        #      FEC on → corrected counts rise, uncorrectable stays 0; read faster than the wrap times
        self.beat("g8")
        h = self.next_test(7, "Sayaçlar ve hata enjeksiyonu", h)
        cols = []
        xs = (-4.3, 0.0, 4.3)
        heads = [("bilinen N çerçeve", GOOD), ("FEC kapalı · zayıflatıcı ↑", WARN), ("FEC açık · zayıflatıcı ↑", ACC)]
        for x, (t, c) in zip(xs, heads):
            fr = frame_box(t, c, 4.05, 2.9, 16).move_to([x, 0.15, 0])
            cols.append(fr)
        c1 = VGroup(T("XGEM gönderilen = N", 16, TXT, BOLD), T("XGEM alınan = N", 16, TXT, BOLD), exp("birebir", True, 16)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        c1.move_to(cols[0][0]).shift(DOWN * 0.2)
        c2 = VGroup(T("BIP-32 hataları", 16, TXT, BOLD), T("≈ BERT'in BER'i × bit", 16, TXT, BOLD), exp("uyuşmalı", True, 16)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        c2.move_to(cols[1][0]).shift(DOWN * 0.2)
        c3 = VGroup(VGroup(T("düzeltilen bayt / kod sözcüğü", 16, TXT, BOLD), T("↑", 18, GOOD, BOLD)).arrange(RIGHT, buff=0.1),
                    VGroup(T("düzeltilemeyen", 16, TXT, BOLD), T("= 0", 17, GOOD, BOLD)).arrange(RIGHT, buff=0.1), exp("FEC'in işi", True, 16)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        c3.move_to(cols[2][0]).shift(DOWN * 0.2)
        rd = VGroup(T("okuma aralığı < taşma süresi", 17, GOLD, BOLD), T("(10G · 32 bit BIP-32 sözcükleri: 13,8 s · bizim hesabımız)", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.2)
        fit(rd, 12.6).move_to([0, -2.65, 0])
        self.play(self.set_src("G.989.3 Tablo 14-1 · XGEM / PHY PM · Not 1 · taşma: bizim hesabımız"), run_time=0.3)
        self.at(self.cue("Bilinen sayıda çerçeve", 3.5))
        self.play(FadeIn(cols[0]), FadeIn(c1[:2], shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("XGEM sayaçları birebir", 6.2))
        self.play(FadeIn(c1[2], scale=1.1), run_time=0.3)
        self.at(self.cue("FEC kapalıyken zayıflatıcıyla", 9.1))
        self.play(FadeIn(cols[1]), FadeIn(c2[0], shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("BIP-32 hataları BERT'le", 13.4))
        self.play(FadeIn(c2[1:], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("FEC açıkken düzeltilenler", 16.4))
        self.play(FadeIn(cols[2]), FadeIn(c3[0], shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("düzeltilemeyenler sıfır", 19.3))
        self.play(FadeIn(c3[1:], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("taşma sürelerinden sık", 22.2))
        self.play(FadeIn(rd, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep19_labB")


class E19LabC(LabAct):
    HDR, MANIFEST, PREV_BADGE = H19["L"], M19("lab"), "lab"

    def construct(self):
        # g9 — TEST 8: defect injection: suppress consecutive bursts → LOBi at the 4th, cleared by one burst; repeat with the DG bit; open the feeder →
        #      LOS at 500 µs; acknowledge Change_Power_Level without changing power → ALRFi; compare the OLT power reading with ±0.5 dB repeatability
        self.beat("g9")
        h = step_head(self, 8, "Kusur enjeksiyonu")
        n, cw, x0, y = 9, 0.62, -6.2, 1.35
        fr = VGroup()
        marks = ["ok", "ok", "miss", "miss", "miss", "miss", "none", "ok", "none"]
        for k in range(n):
            r = Rectangle(width=cw, height=0.42, stroke_color=LINE, stroke_width=1.4, fill_color=PANEL, fill_opacity=1).move_to([x0 + cw * (k + 0.5), y, 0])
            m = marks[k]
            g = (Rectangle(width=cw * 0.45, height=0.25, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(r) if m == "ok"
                 else T("✗", 17, WARN, BOLD).move_to(r) if m == "miss" else VGroup())
            fr.add(VGroup(r, g))
        frl = T("burst bastır", 15, ONUC, BOLD).next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
        lb = tag("LOBi · 4.", WARN, 15).next_to(fr[5], DOWN, buff=0.12)
        cl = T("1 burst → temiz", 14, GOOD, BOLD).next_to(fr[7], DOWN, buff=0.12).shift(RIGHT * 0.45)
        dg = VGroup(T("+ DG biti ile tekrar:", 15, GOLD, BOLD), T("rapor DG ile nitelenmeli", 15, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-4.3, -0.45, 0])
        osw = oswitch_icon(0.6, FEED, "besleyici fiber açık", True).move_to([1.3, 1.35, 0])
        los = VGroup(T("→ LOS", 18, WARN, BOLD), T("4 çerçeve = 500 µs", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).next_to(osw, RIGHT, buff=0.3)
        cp = VGroup(mbox("Change_Power_Level ↓", FAM["pwr"], 2.9, 0.42, 15), T("→", 18, MUTED, BOLD), mbox("Acknowledgement OK ↑", GOOD, 2.9, 0.42, 15),
                    T("→ güç aynı", 16, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        cp.move_to([2.6, -0.2, 0])
        al = VGroup(tag("ALRFi", WARN, 16), T("OLT güç okuması ↔ ±0,5 dB tekrarlanabilirlik (G.989.2 Ek II)", 16, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        fit(al, 8.2).next_to(cp, DOWN, buff=0.3).align_to(cp, LEFT)
        self.play(FadeIn(frl), *[FadeIn(c[0]) for c in fr], self.set_src("G.989.3 Tablo 14-2 · Tablo 18-3 · G.989.2 Ek II · yöntem: yorum"), run_time=0.45)
        self.at(self.cue("Art arda burst'leri bastırın", 2.8))
        self.play(LaggedStart(*[FadeIn(fr[k][1], scale=1.2) for k in range(6)], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("dördüncüde gelmeli", 5.2))
        self.play(FadeIn(lb, scale=0.9), run_time=0.35)
        self.at(self.cue("tek bir burst'le temizlenmelidir", 7.8))
        self.play(FadeIn(fr[7][1], scale=1.2), FadeIn(cl), run_time=0.35)
        self.at(self.cue("son nefes bitiyle tekrarlayın", 10.6))
        self.play(FadeIn(dg, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Besleyici fiberi açın", 13.1))
        self.play(FadeIn(osw), run_time=0.35)
        self.at(self.cue("beş yüz mikrosaniyede", 15.0))
        self.play(FadeIn(los, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Güç düzeyi değişikliğini onaylayıp", 17.9))
        self.play(FadeIn(cp, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("zayıflatma düzeyi isteği başarısızlığı", 22.5))
        self.play(FadeIn(al[0], scale=0.9), run_time=0.3)
        self.at(self.cue("yarım desibellik tekrarlanabilirlikle", 25.7))
        self.play(FadeIn(al[1], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g10 — TEST 9: the remaining defects: drift ignoring corrections → TIWi; answer SN, never complete bring-up → SUFi; ignore disable → DFi;
        #       corrupt three consecutive PLOAM MICs → LOPCi; walk the wavelength → DOTXi; corrupt three DS sync patterns → LODS; record when the three
        #       defects without a clearing condition close
        self.beat("g10")
        h = self.next_test(9, "Kalan kusurlar", h)
        rows = [["Ranging_Time düzeltmelerini yok say, kay", "TIWi", "3 düzeltme sonra"],
                ["SN'ye cevap ver, bağlanmayı tamamlama", "SUFi", "→ Deactivate_ONU-ID"],
                ["Disable_Serial_Number'ı yok say", "DFi", "tahsis sürdükçe"],
                ["art arda 3 ↑ PLOAM MIC'i boz", "LOPCi", "temizlenme: ?"],
                ["↑ dalga boyunu kaydır", "DOTXi", "temizlenme: ?"],
                ["↓ 3 PSync'i boz", "LODS (ONU)", "→ O6"]]
        tb = mtable(["enjeksiyon", "beklenen kusur", "not"], rows, [6.4, 2.6, 3.6], size=16, hsize=15, row_h=0.48).move_to([0, 0.35, 0])
        for r in tb[1:]:
            r[2].set_color(WARN)
        for k in (4, 5):
            tb[k][3].set_color(NOCLR)
        rec = VGroup(T("temizlenme koşulu yazılı olmayan üç kusur:", 16, NOCLR, BOLD), *[tag(s, NOCLR, 15) for s in ("LOPCi", "LOOCi", "DOTXi")],
                     T("→ ne zaman kapandı? kaydedin", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(rec, 12.6).move_to([0, -2.6, 0])
        self.play(FadeIn(tb[0]), self.set_src("G.989.3 Tablo 14-2 / 14-3 · Tablo 13-1 · yöntem: yorum"), run_time=0.4)
        for k, (key, d) in enumerate((("Düzeltmeleri yok sayarak", 2.5), ("seri numarasına cevap verip", 5.1), ("devre dışı bırakmayı yok", 8.5),
                                      ("üç PLOAM bütünlük kodunu", 11.1), ("dalga boyunu kaydırın", 14.5), ("üç senkron desenini", 16.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(tb[k + 1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("Temizlenme koşulu yazılı olmayan", 19.5))
        self.play(FadeIn(rec, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # g11 — TEST 10: dying gasp: cut the ONU mains; capture bursts with the DG bit; check the OLT's DG counter and the qualification of the LOBi
        #       report; on power return look for code 1101 (13) in Serial_Number_ONU and read the snapshot records — method not in the standard
        self.beat("g11")
        h = self.next_test(10, "Son nefes", h)
        onu = onu_box("ONU", ONUC, 1.2, 0.55, 17).move_to([-5.3, 1.2, 0])
        plug = VGroup(T("şebeke", 15, MUTED, BOLD), T("✗", 22, WARN, BOLD)).arrange(RIGHT, buff=0.1).next_to(onu, DOWN, buff=0.15)
        bs = VGroup(*[VGroup(Rectangle(width=0.55, height=0.36, stroke_color=GOLD, stroke_width=1.5, fill_color=GOLD, fill_opacity=0.3),
                             T("DG", 14, TXT, BOLD)) for _ in range(4)])
        for b in bs:
            b[1].move_to(b[0])
        bs.arrange(RIGHT, buff=0.15).move_to([-1.9, 1.2, 0])
        bsl = T("↑ Ind bit 0 = 1 · yakala", 15, GOLD, BOLD).next_to(bs, UP, buff=0.1)
        ol = VGroup(T("OLT:", 16, OLTC, BOLD), tag("DG sayısı (O) ↑", GOLD, 15), tag("LOBi raporu DG ile nitelenmiş mi?", WARN, 15)).arrange(RIGHT, buff=0.2)
        fit(ol, 7.6).move_to([2.6, 1.2, 0])
        ar = arrow(onu.get_right(), bs.get_left(), GOLD, 2, 0.1)
        pw = VGroup(T("güç geri gelince:", 16, GOOD, BOLD), mbox("Serial_Number_ONU ↑", ONUC, 2.8, 0.42, 15), T("Activation Debug", 15, MUTED, BOLD), HX("1101", 18, GOOD, BOLD),
                    T("(13) · güç kesildi", 16, TXT, BOLD)).arrange(RIGHT, buff=0.18)
        fit(pw, 12.6).move_to([0, -0.35, 0])
        nv = nvm_icon(10, 4, 2.6, 1.15, GOLD, "anlık görüntüler").move_to([-3.9, -2.05, 0])
        rd = VGroup(T("okuma yöntemi:", 16, TXT, BOLD), tag("standartta yok", WARN, 15), T("→ üreticinin yolunu belgeleyin", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.18)
        rd.next_to(nv, RIGHT, buff=0.4)
        self.play(FadeIn(onu), self.set_src("G.989.3 §8.1.2.1.2 · §14.2.3 · Tablo 14-1 / 14-2 · Activation Debug (S2·B6)"), run_time=0.4)
        self.at(self.cue("şebeke gücünü kesin", 1.9))
        self.play(FadeIn(plug, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Son nefes biti kurulmuş", 4.2))
        self.play(GrowArrow(ar), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.05) for b in bs], lag_ratio=0.15), FadeIn(bsl), run_time=0.7)
        self.at(self.cue("OLT'nin son nefes sayacını", 8.0))
        self.play(FadeIn(ol[:2], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("burst kaybı raporunun nitelenmesini", 10.8))
        self.play(FadeIn(ol[2], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("on üç kodunu arayın", 14.6))
        self.play(FadeIn(pw, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("anlık görüntü kayıtlarını", 19.3))
        self.play(FadeIn(nv, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Okuma yöntemi standartta", 22.3))
        self.play(FadeIn(rd[:2], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("üreticinin yolunu belgeleyin", 25.0))
        self.play(FadeIn(rd[2], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # g12 — lab note
        self.note11("g12", [("1", "Her ölçümün yanına güç yönetimi parametrelerini yazın",
                             "Standart değer vermediği için bir sonuç ancak parametreleriyle birlikte anlamlıdır.", "her ölçümün yanına"),
                            ("2", "Kusur enjekte ederken sayaçları da okuyun",
                             "İlan, temizlenme ve ilgili sayacın artışı aynı zaman çizgisinde durmalıdır.", "İki:")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep19_labC")


POINTS = [("Tek uyku kipi: dikkatli uyku · dört durumlu iki makine kısmen hizalı;\nmesaj yalnızca sarı ↔ gri sınırı geçilince", "§16.1"),
          ("Güç yönetimi parametrelerinde değer yok · PtP hız uyarlamasında üç FFS;\nbizim modelimizde tasarrufu uyurken açık kalan devreler sınırlar", "§16 · T.16-1/16-8"),
          ("Tablo 14-1: 111 satır, 37 zorunlu · PtP için hiçbiri yok;\nsayaç genişlikleri yazılı değil", "§14.1"),
          ("OLT 9, ONU 1 kusur · LOBi varsayılanı 4 burst, LOS 4 çerçeve;\nüç kusurun temizlenme koşulu yok", "§14.2"),
          ("Son nefes bir ipucu, komut değil · anlık görüntü en az 10 kayıt", "§14.2.3")]


class E19End(Act19):
    HDR, MANIFEST, FIRST = H19["E"], M19("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header_badge(tc, "ozet", 0.5)
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.2)
            ch = tag(c, GOLD, 16)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.75, -2.4, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.6, y, 0])
        for k, (key, d) in enumerate((("tek uyku kipi dikkatli", 1.5), ("güç yönetimi parametrelerinin hiçbirinin", 16.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((2, 3, 4), (("başarım tablosu yüz on bir", 0.3), ("OLT dokuz,", 10.2), ("son nefes bir ipucudur", 22.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.7, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Düşük güç gözetimindeki OLT,\nel sıkışma zamanlayıcısı\ndolana kadar hiç burst\nalmazsa ne yapar, ardından\nne gelebilir?", CH[0]),
            ("Varsayılan ayarlarla ve\nçerçeve başına bir burst'le\nLOBi ve LOS ne kadar sürede\nilan edilir? Aralarındaki\nfark nedir?", CH[1]),
            ("G.989.3 hangi uyku kipini\ntanımlar, ONU onu nasıl\nister, OLT uyuyan bir\nONU'yu nasıl zorla\nuyandırır?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 12.5), ("Üçüncü soru", 25.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 35.9))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode, season finale: Ayakta Kalmak (protection, rogue ONU, emergency stop) and the season's last story: the life of a packet
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e10 = SERIES["season2"]["episodes"][9]
        nxt = VGroup(T("SONRAKİ BÖLÜM · SEZON FİNALİ", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e10['n']} · {e10['title']}", 50, TXT, BOLD), T(e10["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        fit(nxt[1], 12.6)
        tg_ = VGroup(*[tag(s, GOOD, 16) for s in ("koruma", "başıboş ONU", "acil durdurma")]).arrange(RIGHT, buff=0.2).move_to([0, -0.8, 0])
        story = VGroup(T("bir paketin hayatı:", 18, GOLD, BOLD), tile("Ethernet", GOOD, 1.4, 0.44, 16, 0.2), T("→", 18, MUTED, BOLD), tile("XGEM", SAC, 1.1, 0.44, 16, 0.2),
                       T("→", 18, MUTED, BOLD), tile("ışık", CH[1], 0.9, 0.44, 16, 0.2), T("→ ve geri", 18, MUTED, BOLD)).arrange(RIGHT, buff=0.18).move_to([0, -1.85, 0])
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("Koruma,", 3.8))
        self.play(FadeIn(nxt[2]), FadeIn(tg_[0], shift=UP * 0.06), run_time=0.45)
        self.at(self.cue("başıboş ONU ve acil", 4.4))
        self.play(FadeIn(tg_[1:], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("bir paketin hayatı", 8.9))
        self.play(FadeIn(story[0]), run_time=0.3)
        self.at(self.cue("XGEM'den ışığa", 10.6))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.05) for s in story[1:]], lag_ratio=0.15), run_time=0.8)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(tg_, story)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP19['n']} · {EP19['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep19_end")
