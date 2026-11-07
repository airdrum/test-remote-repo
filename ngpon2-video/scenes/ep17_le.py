"""S2·B7 · Laboratuvarda (merdiven, ayar süresi üç parçada, öncülük süresi, NACK / ROLLBACK matrisleri, zamanlayıcılar ve OLT makinesi,
sıcaklıkta kilitleme, bağlama) and Kapanış."""
from ep17_common import *


def pw_trace(X, Y, t0, t1, hi, lo, rise, color, falling=True, n=40):
    """Power vs time trace: flat, then a smooth transition between t0 and t1, then flat."""
    pts = []
    for t in np.linspace(X.lo, X.hi, n * 3):
        if t <= t0:
            v = hi if falling else lo
        elif t >= t1:
            v = lo if falling else hi
        else:
            u = (t - t0) / (t1 - t0)
            s = 0.5 - 0.5 * np.cos(np.pi * u)
            v = hi + (lo - hi) * s if falling else lo + (hi - lo) * s
        pts.append([X(t), Y(v), 0])
    return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(pts)


class _X:
    def __init__(self, lo, hi, x0, x1):
        self.lo, self.hi, self.x0, self.x1 = lo, hi, x0, x1

    def __call__(self, t):
        return self.x0 + (t - self.lo) / (self.hi - self.lo) * (self.x1 - self.x0)


class E17LabA(Act17):
    HDR, MANIFEST, FIRST = H17["L"], M17("lab"), True

    def construct(self):
        # g1 — bench: OLT (or emulator) with two CTs, analyzer on both DS channels and US, tunable ONU + ONU emulator, traffic generator,
        #      wavelength meter, temperature chamber; ICTP is not on the PON → read it from the OLT logs
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Bir devri ölçmek")
        self.at(self.cue("Düzenek", 1.2))
        h = self.heading("Düzenek")
        self.to_header_badge(tc, "lab", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        y1, y2 = 1.15, -1.05
        em = emu_icon(2.0, 1.35, "OLT · 2 CT / emülatör").move_to([-5.1, y1, 0])
        pa = pa_icon(2.0, 1.35, "Analizör · 2 × ↓ + ↑").move_to([-1.7, y1, 0])
        onu = VGroup(onu_box("ONU", ONUC, 1.6, 0.8, 20, "ayarlanabilir"), T("gerçek ONU", 16, TXT, SEMIBOLD)).arrange(DOWN, buff=0.25).move_to([1.7, y1 - 0.1, 0])
        oe = emu_icon(2.0, 1.35, "ONU emülatörü").move_to([5.1, y1, 0])
        tg = tg_icon(2.0, 1.35, "Trafik üreteci").move_to([-5.1, y2, 0])
        wm = inst("OSA", "Dalga boyu ölçer", 2.0, 1.35, "λ · GHz", ACC).move_to([-1.7, y2, 0])
        chm = chamber_icon(2.0, 1.35, "Sıcaklık kabini").move_to([1.7, y2, 0])
        ictp = VGroup(T("ICTP", 18, ICTC, BOLD), T("PON'da görünmez", 16, TXT, BOLD), T("→ OLT kayıtlarından oku", 16, GOLD, BOLD)).arrange(DOWN, buff=0.08).move_to([5.1, y2, 0])
        ib = SurroundingRectangle(ictp, color=ICTC, buff=0.18, corner_radius=0.12, stroke_width=1.8)
        self.at(self.cue("iki kanal sonlandırıcılı", 1.9))
        self.play(FadeIn(em, shift=UP * 0.1), self.set_src("G.989.3 §17 · Ek F · Ek H · Ek X · tezgâh ve yöntemler: yorum"), run_time=0.45)
        self.at(self.cue("protokol analizörü", 8.5))
        self.play(FadeIn(pa, shift=UP * 0.1), run_time=0.45)
        self.at(self.cue("ayarlanabilir bir ONU", 11.9))
        self.play(FadeIn(onu, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bir ONU emülatörü", 13.6))
        self.play(FadeIn(oe, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bir trafik üreteci", 15.5))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bir dalga boyu ölçer", 17.1))
        self.play(FadeIn(wm, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bir sıcaklık kabini", 19.0))
        self.play(FadeIn(chm, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("ICTP PON'da görünmez", 20.8))
        self.play(FadeIn(ib), FadeIn(ictp[:2]), run_time=0.45)
        self.at(self.cue("OLT'nin kayıtlarından", 22.6))
        self.play(FadeIn(ictp[2], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g2 — TEST 1: the handover ladder (expected PON-side order); validate the analyzer's MIC with S2·B5's golden vectors first;
        #      then every tuning message must verify with the default key
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "Devrin merdiveni")
        p = apanel(12.6, 4.6, "Analizör · bir devrin PLOAM sırası", ACC).move_to([0, -0.55, 0])
        rows = [("↓ K", "Tuning_Control 0x15 · Request · SeqNo s", "ayar isteği", GOLD), ("↑ K", "Tuning_Response 0x1A · ACK · SeqNo s", "aynı SeqNo", ACKC),
                ("—", "planlı çerçeve · SFC'nin 16 LSB'si = planlı değer", "ayar", GOLD), ("↓ H", "yalnız PLOAM taşıyan tahsisler", "hedef", TGTC),
                ("↑ H", "Tuning_Response · Complete_u", "tamamlandı", CMPC), ("↓ H", "Tuning_Control · Complete_d + veri tahsisi", "hedef", TGTC),
                ("↑ H", "Acknowledgement", "ONU onayı", OPC), ("↕ H", "veri", "çalışma", OPC)]
        lad = VGroup()
        top = panel_top(p, 0.25)
        for k, (d, s, n, c) in enumerate(rows):
            r = VGroup(T(d, 17, c, BOLD), HX(s, 16, TXT, BOLD), T(n, 15, c, BOLD), ok_x(True, 17))
            yy = top - 0.15 - k * 0.42
            r[0].move_to([-5.75, yy, 0])
            r[1].move_to([-5.2, yy, 0], aligned_edge=LEFT)
            r[2].move_to([3.5, yy, 0], aligned_edge=LEFT)
            r[3].move_to([5.7, yy, 0]).set_opacity(0)
            lad.add(r)
        mic = VGroup(T("MIC:", 17, HECC, BOLD), T("önce S2·B5 altın vektörleri", 17, TXT, BOLD), T("→ sonra her ayar mesajı:", 17, TXT, BOLD), keychip(True, 16)).arrange(RIGHT, buff=0.2)
        fit(mic, 12.0).move_to([0, top - 0.15 - 8 * 0.42 - 0.08, 0])
        self.play(self.set_src("G.989.3 §17.3.1 · Ek F.1.1 · Tablo 11-16 · Tuning_Response · §11.2.3 · Ek IV"), FadeIn(p), run_time=0.4)
        cues = (("ayar isteği;", 3.4), ("aynı sıra numarasıyla", 4.4), ("planlı çerçeve;", 6.7), ("yalnızca PLOAM taşıyan", 8.0), ("tamamlandı yanıtı;", 11.4),
                ("hedeften tamamlandı biçimi", 13.0), ("ONU'nun onayı", 16.9), ("veri.", 18.1))
        for k, (key, d) in enumerate(cues):
            self.at(self.cue(key, d))
            self.play(FadeIn(lad[k][:3], shift=RIGHT * 0.05), lad[k][3].animate.set_opacity(1), run_time=0.3)
        self.at(self.cue("altın vektörleriyle", 21.0))
        self.play(FadeIn(mic[:2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("varsayılan anahtarla", 27.5))
        self.play(FadeIn(mic[2:], shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g3 — TEST 2: tuning time in three parts: trigger on the source PSBd frame whose SFC LSBs = Scheduled SFC; stamp the first Complete_u
        #      burst at the target; interval = TC tuning time + O8.2 decision + grant wait; repeat with and without pre-sent burst profiles
        self.beat("g3")
        self.play(FadeOut(VGroup(p, lad, mic)), run_time=0.4)
        h = step_head(self, 2, "Ayar süresi, üç parçasıyla", h)
        fw = 0.42
        frames = VGroup(*[Rectangle(width=fw, height=0.42, stroke_color=SRCC, stroke_width=1.5, fill_color=SRCC, fill_opacity=0.1) for _ in range(6)]).arrange(RIGHT, buff=0)
        frames.move_to([-5.6, 1.2, 0], aligned_edge=LEFT)
        frames[4].set_fill(GOLD, 0.6).set_stroke(GOLD)
        fl = T("kaynak PSBd · SFC 16 LSB", 15, SRCC, BOLD).next_to(frames, UP, buff=0.1).align_to(frames, LEFT)
        trg = VGroup(arrow(frames[4].get_bottom() + DOWN * 0.55, frames[4].get_bottom(), GOLD, 2.4, 0.12), T("= planlı değer → tetik", 15, GOLD, BOLD))
        trg[1].next_to(trg[0], DOWN, buff=0.06)
        x0 = frames[4].get_left()[0]
        sb = stack_bar([(1.0, "hazırlık", PREPC), (1.4, "PMD", PMDTC), (1.4, "yen. senkron", RSYC), (1.5, "O8.2 kararı", TUC), (1.6, "tahsis bekleme", TGTC)], x0, -0.55, 0.55, 14, 1.0)
        cu = VGroup(Rectangle(width=0.32, height=0.55, stroke_color=CMPC, stroke_width=2, fill_color=CMPC, fill_opacity=0.7).next_to(sb, RIGHT, buff=0.0),
                    T("ilk Complete_u · damga", 15, CMPC, BOLD))
        cu[1].next_to(cu[0], RIGHT, buff=0.12)
        b1 = brace_lbl(sb[:3], "TC ayar süresi", GOLD, DOWN, 15)
        b2 = brace_lbl(sb, "ölçülen aralık", TXT, UP, 15)
        cmp_ = VGroup(VGroup(T("profiller önceden", 16, TXT, BOLD), tag("gönderildi", GOOD, 15), T("→ kısa", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.15),
                      VGroup(T("profiller önceden", 16, TXT, BOLD), tag("gönderilmedi", WARN, 15), T("→ 1–5 s'e kadar?", 16, WARN, BOLD)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cmp_.move_to([0, -2.65, 0])
        self.play(self.set_src("G.989.3 Ek F.2 · §17.3.1 adım 7–8 · Tablo 12-4"), run_time=0.3)
        self.at(self.cue("Kaynak PSBd'sinde", 3.2))
        self.play(FadeIn(fl), LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.1), run_time=0.7)
        self.at(self.cue("çerçeveyi tetik alın", 8.5))
        self.play(GrowArrow(trg[0]), FadeIn(trg[1]), run_time=0.5)
        self.at(self.cue("ilk tamamlandı burst", 10.8))
        self.play(FadeIn(cu[0]), FadeIn(cu[1]), run_time=0.5)
        self.at(self.cue("Aradaki süre", 14.6))
        self.play(FadeOut(trg), LaggedStart(*[GrowFromEdge(b, LEFT) for b in sb], lag_ratio=0.2), FadeIn(b2), run_time=1.0)
        self.at(self.cue("TC ayar süresi artı", 15.7))
        self.play(FadeIn(b1), run_time=0.4)
        self.at(self.cue("önceden gönderilerek", 22.5))
        self.play(FadeIn(cmp_[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("gönderilmeden tekrarlayın", 25.5))
        self.play(FadeIn(cmp_[1], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g4 — the PMD part optically (G.989.2 App VIII.3): Gaussian reference filter 0.5 dB @ 8 GHz, two O/E; start = origin power −0.5 dB;
        #      end = destination within 0.5 dB and stays; preparation = start of the drop − SFC frame; compare with the declared class
        self.beat("g4")
        self.play(FadeOut(VGroup(frames, fl, sb, cu, b1, b2, cmp_)), run_time=0.4)
        onu = onu_box("ONU Tx", ONUC, 1.3, 0.55, 16).move_to([-5.6, 1.35, 0])
        flt = VGroup(*[sbox(f"süzgeç {l}", "Gauss · 0,5 dB @ 8 GHz", c, 2.6, 0.62, 15, 14).move_to([-2.6, y, 0]) for l, c, y in (("λ1", SRCC, 1.75), ("λ3", TGTC, 0.95))])
        oes = VGroup(*[tile("O/E", c, 0.8, 0.45, 15, 0.2).move_to([-0.5, y, 0]) for c, y in ((SRCC, 1.75), (TGTC, 0.95))])
        ln = VGroup(*[Line(onu.get_right(), f[0].get_left(), color=FEED, stroke_width=1.8) for f in flt], *[Line(f[0].get_right(), o.get_left(), color=FEED, stroke_width=1.8) for f, o in zip(flt, oes)])
        X = _X(0, 10, 0.6, 6.5)
        Y = lambda v: -2.0 + v * 2.2
        ax = Line([X(0), Y(0), 0], [X(10), Y(0), 0], color=MUTED, stroke_width=1.6)
        axl = T("zaman", 14, MUTED, BOLD).next_to(ax, DOWN, buff=0.08).align_to(ax, RIGHT)
        tk = pw_trace(X, Y, 3.0, 6.0, 1.0, 0.05, 0, SRCC, True)
        tt = pw_trace(X, Y, 3.6, 6.8, 1.0, 0.05, 0, TGTC, False)
        lk = T("λ1 gücü", 15, SRCC, BOLD).move_to([X(1.2), Y(1.0) + 0.2, 0])
        lt = T("λ3 gücü", 15, TGTC, BOLD).move_to([X(8.6), Y(1.0) + 0.2, 0])
        msfc = tmark(X(1.5), Y(0) - 0.1, Y(1.25), "planlı SFC", GOLD, 14)
        mst = tmark(X(3.25), Y(0) - 0.1, Y(1.25), "−0,5 dB", SRCC, 14)
        men = tmark(X(6.6), Y(0) - 0.1, Y(1.25), "0,5 dB içinde · kalır", TGTC, 14)
        bp = brace_lbl(Line([X(1.5), Y(0), 0], [X(3.25), Y(0), 0]), "hazırlık", PREPC, DOWN, 14)
        bm = brace_lbl(Line([X(3.25), Y(0), 0], [X(6.6), Y(0), 0]), "PMD", PMDTC, DOWN, 14)
        cl = VGroup(T("PMD parçası ↔ beyan edilen sınıf", 16, TXT, BOLD), VGroup(*[tag(f"Sınıf {k}", CLC[k], 14) for k in "123"]).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cl.move_to([-3.5, -1.5, 0])
        self.at(self.cue("PMD parçasını optik", 0.3))
        self.play(FadeIn(onu), self.set_src("G.989.2 Ek VIII.3 · §9.3.7 · Tablo 9-2 · G.989.3 Ek F.2"), run_time=0.3)
        self.at(self.cue("Gauss biçimli", 8.5))
        self.play(FadeIn(flt), Create(ln[:2]), run_time=0.6)
        self.at(self.cue("iki optik alıcı", 12.0))
        self.play(FadeIn(oes), Create(ln[2:]), Create(ax), FadeIn(axl), Create(tk), Create(tt), FadeIn(lk), FadeIn(lt), run_time=0.9)
        self.at(self.cue("kaynak kanaldaki gücün", 14.8))
        self.play(FadeIn(mst), run_time=0.4)
        self.at(self.cue("hedef kanalın yarım", 19.1))
        self.play(FadeIn(men), FadeIn(bm), run_time=0.5)
        self.at(self.cue("Hazırlık,", 23.6))
        self.play(FadeIn(msfc), run_time=0.3)
        self.at(self.cue("güç düşüşünün başlangıcı", 24.4))
        self.play(FadeIn(bp), run_time=0.4)
        self.at(self.cue("beyan edilen sınıfla", 28.8))
        self.play(FadeIn(cl, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_labA")


class E17LabB(Act17):
    HDR, MANIFEST, PREV_BADGE = H17["L"], M17("lab"), "lab"

    def construct(self):
        # g5 — TEST 3: Scheduled SFC lead time: step toward the current frame, find the shortest accepted lead; below: NACK INT_SFC + counter;
        #      also near the wrap and in the past; no traffic loss; our arithmetic: target PLOAM bursts cost 0.2–0.3 % of a frame
        self.beat("g5")
        h = step_head(self, 3, "Öncülük süresi taraması")
        ax = Line([-5.8, 0.6, 0], [5.8, 0.6, 0], color=MUTED, stroke_width=2)
        axl = T("öncülük k (çerçeve) ←", 15, MUTED, BOLD).next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        now = tmark(-5.6, 0.45, 1.6, "şimdiki çerçeve", TXT, 14)
        ks = [4.8, 3.4, 2.0, 0.6, -0.8, -2.2, -3.6]
        res = VGroup()
        for k, x in enumerate(ks):
            ok = k < 4
            res.add(VGroup(Dot([x, 0.6, 0], radius=0.08, color=GOOD if ok else WARN), T("ACK" if ok else "NACK", 15, GOOD if ok else WARN, BOLD).move_to([x, 1.05, 0])))
        mn = VGroup(Line([ks[3], 0.35, 0], [ks[3], 1.35, 0], color=GOLD, stroke_width=2.4), T("en kısa kabul", 15, GOLD, BOLD))
        mn[1].next_to(mn[0], UP, buff=0.06)
        nk = VGroup(code_chip(0x0001, "INT_SFC", "INT", 15), T("+ sayacı artar", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([-3.4, -0.35, 0])
        ext = VGroup(VGroup(T("ayrıca:", 16, MUTED, BOLD), tag("dönüşe yakın · ≈ 65 536", GOLD, 15), tag("geçmişte kalan değer", GOLD, 15)).arrange(RIGHT, buff=0.15)).move_to([0, -1.25, 0])
        tr_ = VGroup(tg_icon(1.4, 0.95, "trafik"), VGroup(T("ONU trafiği:", 16, TXT, BOLD), T("kayıp yok", 16, GOOD, BOLD), ok_x(True, 16)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.3)
        tr_.move_to([-3.5, -2.55, 0])
        cost = VGroup(interp("hesap", GOLD, 14), T("hedefin PLOAM burst'leri:", 16, TXT, BOLD), T("binde 2–3 / çerçeve", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.12)
        cost2 = T("2,5G: %0,31 · 10G: %0,20", 15, MUTED, BOLD).next_to(cost, DOWN, buff=0.08).align_to(cost, LEFT)
        VGroup(cost, cost2).move_to([3.0, -2.55, 0])
        self.play(self.set_src("G.989.3 §17.3.1 · Tablo 17-3 · Tablo 14-1 · hesap"), Create(ax), FadeIn(axl), FadeIn(now), run_time=0.5)
        self.at(self.cue("adım adım yaklaştırın", 3.5))
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.05) for r in res[:4]], lag_ratio=0.3), run_time=1.2)
        self.at(self.cue("en kısa öncülüğü", 6.8))
        self.play(FadeIn(mn), run_time=0.4)
        self.at(self.cue("iç grubun tek koduyla", 10.0))
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.05) for r in res[4:]], lag_ratio=0.3), run_time=0.9)
        self.play(FadeIn(nk, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Sayacın dönüşüne yakın", 16.2))
        self.play(FadeIn(ext[0][:2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("geçmişte kalan", 19.8))
        self.play(FadeIn(ext[0][2], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("trafiğinde kayıp", 22.4))
        self.play(FadeIn(tr_, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("binde iki ile", 29.5))
        self.play(FadeIn(cost), FadeIn(cost2), run_time=0.5)
        self.end(pad=0.05)

        # g6 — TEST 4: the NACK matrix — each provocation sets its own bit and PM counter; uncalibrated target: cal flag 0 → US_CLBR, flag 1 → ACK;
        #      several conditions → OR-ed bits
        self.beat("g6")
        self.play(FadeOut(VGroup(ax, axl, now, res, mn, nk, ext, tr_, cost, cost2)), run_time=0.4)
        h = step_head(self, 4, "Olumsuz cevap matrisi", h)
        data = [("yabancı yönetim etiketi", "DS_ALBL · US_ALBL", "Yabancı etiket"), ("boş tanım (D / U)", "DS_VOID · US_VOID", "boş tanım"),
                ("başka bölüm", "DS_PART", "bölüm,"), ("aralık dışı hedef", "DS_TUNR · US_TUNR", "aralık dışı hedef"),
                ("hız · bağlantı tipi", "DS_LNRT · US_LNRT · US_LKTP", "hız ve bağlantı tipi")]
        tb = mtable(["kışkırtma", "beklenen bit", "PM"], [[a, b, "+1"] for a, b, _ in data], [4.2, 5.0, 1.0], size=17, hsize=15, row_h=0.46, mono=(1,))
        tb.move_to([-1.2, 0.55, 0])
        each = T("her biri: kendi biti + kendi başarım sayacı", 16, GOLD, BOLD).next_to(tb, DOWN, buff=0.15).align_to(tb, LEFT)
        cal = VGroup(VGroup(T("kalibre olmayan hedef · kal. biti 0 →", 16, TXT, BOLD), code_chip(0x0400, "US_CLBR", "US", 15)).arrange(RIGHT, buff=0.15),
                     VGroup(T("kal. biti 1 →", 16, TXT, BOLD), tag("ACK", ACKC, 15)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cal.move_to([-3.0, -2.45, 0])
        orr = VGroup(T("çok koşul →", 16, TXT, BOLD), HX("0x0010 | 0x0200 = 0x0210", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([3.6, -2.45, 0])
        self.play(self.set_src("G.989.3 Tablo 17-3 · Tablo 11-16 (kal. biti) · Tablo 14-1"), FadeIn(tb[0]), run_time=0.4)
        for k, (_, _, key) in enumerate(data):
            self.at(self.cue(key, 3.0 + 1.0 * k))
            self.play(FadeIn(tb[k + 1], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("kendi bitini", 9.5))
        self.play(FadeIn(each, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Kalibre olmayan bir hedefi", 13.6))
        self.play(FadeIn(cal[0][0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("kalibrasyon kodu gelmeli", 18.7))
        self.play(FadeIn(cal[0][1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Bit birken", 20.9))
        self.play(FadeIn(cal[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Birden çok koşullu", 23.1))
        self.play(FadeIn(orr, shift=LEFT * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # g7 — TEST 5: the ROLLBACK matrix with R = 1: target DS dark → COM_DS; PSBd label / link type; target Channel_Profile contradictions;
        #      expect Complete_d from the source and ICTP abort to the target; R = 0: TO4 → reactivation, SN octet 40 code 11; US failure: TO5 → 12
        self.beat("g7")
        self.play(FadeOut(VGroup(tb, each, cal, orr)), run_time=0.4)
        h = step_head(self, 5, "Geri dönüş matrisi", h)
        r1 = tag("R = 1", RBC, 17).move_to([-5.9, 1.55, 0])
        data = [("hedef ↓ karart", "COM_DS 0x0001", "Hedef aşağı yönü", "iletişim kodu"), ("PSBd etiketi / bağlantı tipi", "DS_ALBL 0x0002 · DS_LKTP 0x0004", "PSBd'deki etiketi", None),
                ("hedef kanal profili çeliştir", "US_* 0x0008 … 0x0100", "hedef kanal profilini", None)]
        tb = mtable(["kışkırtma", "ROLLBACK biti"], [[a, b] for a, b, _, _ in data], [4.4, 5.6], size=17, hsize=15, row_h=0.46, mono=(1,)).move_to([0.4, 1.0, 0])
        exp = VGroup(T("beklenen:", 16, TXT, BOLD), mbox("kaynaktan Complete_d", SRCC, None, 0.38, 15), mbox("hedefe ICTP iptal", ICTC, None, 0.38, 15)).arrange(RIGHT, buff=0.18)
        exp.move_to([0.4, -0.55, 0])
        r0 = tag("R = 0", WARN, 17).move_to([-5.9, -1.5, 0])
        nr = T("geri dönemez", 16, WARN, BOLD).next_to(r0, RIGHT, buff=0.2)
        p1 = VGroup(tag("TO4 doldu", TMRC, 15), T("→ yeniden aktivasyon → SN oktet 40:", 16, TXT, BOLD), HX("1011", 17, GOLD, BOLD), T("= 11", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.12)
        p2 = VGroup(tag("↑ başarısız · TO5 doldu", TMRC, 15), T("→", 16, TXT, BOLD), HX("1100", 17, GOLD, BOLD), T("= 12", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.12)
        pp = VGroup(p1, p2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-6.2, -2.55, 0], aligned_edge=LEFT)
        self.play(self.set_src("G.989.3 Tablo 17-4 · Tablo 17-9 · Ek F.1.2 · Tablo 11-25 oktet 40"), run_time=0.3)
        self.at(self.cue("geri dönüş biti bir", 2.7))
        self.play(FadeIn(r1, shift=RIGHT * 0.05), FadeIn(tb[0]), run_time=0.4)
        self.at(self.cue("Hedef aşağı yönü", 4.4))
        self.play(FadeIn(tb[1][:2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("iletişim kodu", 6.6))
        self.play(FadeIn(tb[1][2:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("PSBd'deki etiketi", 7.8))
        self.play(FadeIn(tb[2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("hedef kanal profilini", 11.2))
        self.play(FadeIn(tb[3], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("Kaynaktan tamamlandı", 14.4))
        self.play(FadeIn(exp[:2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("hedefe ICTP iptali", 16.8))
        self.play(FadeIn(exp[2], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Bit sıfırken", 19.2))
        self.play(FadeIn(r0, shift=RIGHT * 0.05), FadeIn(nr), run_time=0.4)
        self.at(self.cue("TO4 dolunca", 21.7))
        self.play(FadeIn(p1[:2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("on bir hata ayıklama", 24.4))
        self.play(FadeIn(p1[2:], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("TO5 ile on iki", 29.3))
        self.play(FadeIn(p2, shift=RIGHT * 0.05), run_time=0.45)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_labB")


class E17LabC(Act17):
    HDR, MANIFEST, PREV_BADGE = H17["L"], M17("lab"), "lab"

    def construct(self):
        # g8 — TEST 6: timers and the OLT machine: withhold target DS / target grants → TO4 / TO5; ONU emulator: repeated Complete_u in Hosting
        #      ignored; no ACK → Tsource expires → alert
        self.beat("g8")
        h = step_head(self, 6, "Zamanlayıcılar ve OLT makinesi")
        m1 = VGroup(T("hedef ↓ esirge", 16, TXT, BOLD), arrow(ORIGIN, RIGHT * 0.6, MUTED, 2, 0.1), tag("TO4 = ?", TMRC, 16), T("ölç", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        m2 = VGroup(T("hedef tahsisleri esirge", 16, TXT, BOLD), arrow(ORIGIN, RIGHT * 0.6, MUTED, 2, 0.1), tag("TO5 = ?", TMRC, 16), T("ölç", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        ms = VGroup(m1, m2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-6.2, 1.2, 0], aligned_edge=LEFT)
        oe = emu_icon(1.7, 1.15, "ONU emülatörü").move_to([4.8, 1.25, 0])
        c1 = VGroup(ostate(3, 2.4, 0.72, 17, 14), mbox("Complete_u · yine", CMPC, None, 0.38, 15), T("→ yok say", 16, GOOD, BOLD), T("Tablo 17-9: *", 14, MUTED, BOLD)).arrange(RIGHT, buff=0.18)
        c2 = VGroup(ostate(4, 2.4, 0.72, 17, 14), T("ACK yok →", 16, TXT, BOLD), tag("Tsource doldu", TMRC, 15), T("→ ICTP uyarısı → (3)", 16, ICTC, BOLD)).arrange(RIGHT, buff=0.18)
        cs = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-6.2, -1.6, 0], aligned_edge=LEFT)
        self.play(self.set_src("G.989.3 Tablo 12-2 · Tablo 17-6 · Tablo 17-9 · Tablo 14-1"), run_time=0.3)
        self.at(self.cue("Hedef aşağı yönü ya da", 3.7))
        self.play(FadeIn(m1, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("TO4 ve TO5'i ölçün", 7.0))
        self.play(FadeIn(m2, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("ONU emülatörüyle", 9.6))
        self.play(FadeIn(oe, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("barındırmada yinelenen", 12.4))
        self.play(FadeIn(c1, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("hiç onay gelmezse", 17.0))
        self.play(FadeIn(c2, shift=RIGHT * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g9 — TEST 7: locking under temperature: wavemeter on the ONU Tx; one Adjust_Tx_Wavelength: ≥ 90 % within the reported step time;
        #      OLT statistics not before F + N × T + 6; heat the ONU: message count and amplitude estimator rise; DOTXi above the threshold
        self.beat("g9")
        self.play(FadeOut(VGroup(ms, oe, cs)), run_time=0.4)
        h = step_head(self, 7, "Sıcaklık altında kilitleme", h)
        wm = inst("OSA", "Dalga boyu ölçer", 1.7, 1.15, "λ · GHz", ACC).move_to([-5.6, 1.15, 0])
        X = _X(0, 10, -3.6, 0.6)
        Y = lambda v: -0.2 + v * 1.6
        ax = Line([X(0), Y(0) - 0.15, 0], [X(10), Y(0) - 0.15, 0], color=MUTED, stroke_width=1.5)
        stp = pw_trace(X, Y, 2.0, 5.5, 1.0, 0.0, 0, GOLD, False)
        p90 = DashedLine([X(0), Y(0.9), 0], [X(10), Y(0.9), 0], color=MUTED, stroke_width=1.2)
        p9l = T("%90", 14, MUTED, BOLD).next_to(p90, RIGHT, buff=0.08)
        mF = tmark(X(2.0), Y(0) - 0.15, Y(1.25), "F", GOLD, 14)
        mT = tmark(X(5.0), Y(0) - 0.15, Y(1.25), "T içinde", GOOD, 14)
        st = tmark(X(8.6), Y(0) - 0.15, Y(1.25), "≥ F + N × T + 6", ACC, 14)
        nb = T("istatistik bundan önce değil", 15, ACC, BOLD).next_to(ax, DOWN, buff=0.15).align_to(ax, RIGHT)
        ch = chamber_icon(1.7, 1.15, "kabin · ısıt").move_to([2.4, 1.15, 0])
        th = arrow([2.4, 0.15, 0], [2.4, -0.55, 0], WARN, 2.4, 0.12)
        bars = VGroup()
        for k, (lab, c) in enumerate((("Adjust_Tx sayısı", GOLD), ("genlik tahmincisi", ACC))):
            b = Rectangle(width=0.5, height=0.4, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.45).move_to([4.0 + 1.8 * k, -2.2, 0], aligned_edge=DOWN)
            b.align_to([0, -2.6, 0], DOWN)
            bars.add(VGroup(b, T(lab, 14, c, BOLD).move_to([4.0 + 1.8 * k, -2.85, 0])))
        thr = DashedLine([3.3, -0.9, 0], [6.4, -0.9, 0], color=WARN, stroke_width=1.8)
        thl = T("eşik", 14, WARN, BOLD).next_to(thr, RIGHT, buff=0.06)
        dx = tag("DOTXi", WARN, 16).move_to([4.9, -0.45, 0])
        self.play(self.set_src("G.989.3 §17.4 · Tablo 11-15 · Tablo 14-1/14-2"), run_time=0.3)
        self.at(self.cue("Dalga boyu ölçeri", 3.4))
        self.play(FadeIn(wm, shift=UP * 0.05), Create(ax), FadeIn(mF), run_time=0.6)
        self.play(Create(stp), run_time=0.8)
        self.at(self.cue("adımın yüzde doksanına", 9.6))
        self.play(Create(p90), FadeIn(p9l), run_time=0.4)
        self.at(self.cue("bildirilen adım süresi", 11.6))
        self.play(FadeIn(mT), run_time=0.4)
        self.at(self.cue("kuraldaki çerçeveden önce", 16.5))
        self.play(FadeIn(st), FadeIn(nb), run_time=0.5)
        self.at(self.cue("kabinde ısıtın", 21.5))
        self.play(FadeIn(ch, shift=UP * 0.05), GrowArrow(th), FadeIn(bars), Create(thr), FadeIn(thl), run_time=0.6)
        self.at(self.cue("genlik tahmincisi artmalı", 24.5))
        self.play(*[b[0].animate.stretch_to_fit_height(1.9, about_edge=DOWN) for b in bars], run_time=1.2)
        self.at(self.cue("eşik aşılınca", 27.5))
        self.play(FadeIn(dx, scale=1.2), run_time=0.4)
        self.end(pad=0.05)

        # g10 — TEST 8: bonding: pilot SN message carries 1023; the 2nd interface (another channel in the partition) the same SN and the pilot's
        #       ONU-ID; an OMCI attribute written on one is read on the other; cloned CTs: decode octet 32, subtree ONU-IDs disjoint
        self.beat("g10")
        self.play(FadeOut(VGroup(wm, ax, stp, p90, p9l, mF, mT, st, nb, ch, th, bars, thr, thl, dx)), run_time=0.4)
        h = step_head(self, 8, "Bağlama ve klonlar", h)
        pl = VGroup(tag("PON 1 · öncü", CH[0], 16), T("SN mesajı · ONU-ID", 16, TXT, BOLD), HX("0x03FF = 1023", 17, GOLD, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        p2 = VGroup(tag("PON 2 · bölüm içi başka kanal", CH[1], 16), T("aynı SN · öncünün ONU-ID'si", 16, TXT, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        om = VGroup(T("OMCI özniteliği:", 16, TXT, BOLD), tag("PON 1'den yaz", CH[0], 15), T("→", 16, MUTED), tag("PON 2'den oku", CH[1], 15), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        bl = VGroup(pl, p2, om).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-6.2, 0.75, 0], aligned_edge=LEFT)
        o32 = VGroup(T("klonlu CT'ler · Channel_Profile oktet 32 çöz:", 16, TXT, BOLD), HX("0001 BBBB", 18, GOLD, BOLD), T("→ klonlu · alt ağaç no. B", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        o32.move_to([-6.2, -1.35, 0], aligned_edge=LEFT)
        dj = VGroup(T("alt ağaçların ONU-ID'leri:", 16, TXT, BOLD), tag("ayrık", GOOD, 15), ok_x(True, 17)).arrange(RIGHT, buff=0.15).move_to([-6.2, -2.1, 0], aligned_edge=LEFT)
        self.play(self.set_src("G.989.3 Ek H.1 · Tablo 11-25 · Tablo 11-18 oktet 32 · Ek X"), run_time=0.3)
        self.at(self.cue("öncünün seri numarası", 3.5))
        self.play(FadeIn(pl, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("bölüm içindeki başka", 9.4))
        self.play(FadeIn(p2[0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("aynı seri numarasını ve öncünün", 12.1))
        self.play(FadeIn(p2[1:], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("OMCI özniteliği", 17.5))
        self.play(FadeIn(om, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("otuz ikinci baytı çözün", 22.5))
        self.play(FadeIn(o32, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("ONU kimliklerinin ayrık", 26.5))
        self.play(FadeIn(dj, shift=RIGHT * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # g11 — lab note
        self.note11("g11", [("1", "Değeri olmayan dört zamanlayıcıyı ölçüp belgeleyin",
                             "TO4 · TO5 · Ttarget · Tsource — tek kural: Tsource > Ttarget", "değeri olmayan dört"),
                            ("2", "Devir süresini üç parçasıyla ve profil dağıtım durumuyla raporlayın",
                             "tek bir sayı, hangi katmanın yavaş olduğunu gizler", "devir süresini her zaman")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep17_labC")


POINTS = [("Profiller 1–5 s'de bir yinelenir · kalibrasyon durumu\nkanal başına 2 bit · \"yeterli\" doğruluğun sayısı yok", "§17.1 · §17.2"),
          ("Devir 11 adım: ONU O5.2 → O8 → O9 · OLT 5 durumlu makine\nhata durumunda ONU kaynakta kalır", "§17.3 · Tablo 17-9"),
          ("NACK (0x01) ve ROLLBACK (0x04): aynı bit haritası,\nfarklı anlamlar → önce işlem kodu", "Tablo 17-3 · 17-4"),
          ("TC ayar süresi = hazırlık + PMD + yeniden senkron · hızlı lazerde\nTC katmanı ve profil dağıtımı belirler · zamanlayıcılar: değer yok", "Ek F · Tablo 9-2"),
          ("Kilitleme: istatistik F + N × T + 6 · bağlı ONU: bir kimlik çok kanal\nklonlu CT'ler parametreleri paylaşır, ONU'ları paylaşmaz", "§17.4 · Ek H · Ek X")]


class E17End(Act17):
    HDR, MANIFEST, FIRST = H17["E"], M17("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
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
            r[2].move_to([5.6, y, 0])
        for k, (key, d) in enumerate((("profiller bir ile beş", 1.5), ("devir on bir adımdır", 13.1), ("olumsuz cevap ve geri dönüş", 23.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((3, 4), (("TC ayar süresi hazırlık", 0.4), ("kilitlemede istatistik", 14.9))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("TC katmanı ayar süresi hangi\nüç parçadır, her biri nerede\nbaşlar ve biter, hangisini\nG.989.2 sınıflandırır?", CH[0]),
            ("Ayar yanıtında işlem kodu 0x01\nve 0x0210 ne demek, hangi CT\nne yapar? İşlem kodu 0x04\nolsaydı aynı değer ne derdi?", CH[1]),
            ("T = 8 çerçeve olan ONU'ya\nF çerçevesinde 2 adımlık ayar:\nOLT istatistiği hangi\nçerçeveden toplayabilir?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 11.0), ("Üçüncü soru", 25.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 38.6))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: Güven (authentication, encryption, integrity; where the keys re-derived after a handover come from)
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e8 = SERIES["season2"]["episodes"][7]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e8['n']} · {e8['title']}", 50, TXT, BOLD), T(e8["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        fit(nxt[1], 12.6)
        tg_ = VGroup(*[tag(s, PINK, 16) for s in ("kimlik doğrulama", "şifreleme", "bütünlük")]).arrange(RIGHT, buff=0.2).move_to([0, -0.85, 0])
        ks = VGroup(*[VGroup(lock(PINK, 0.26), T(s, 16, PINK, BOLD)).arrange(RIGHT, buff=0.1) for s in ("SK", "OMCI_IK", "PLOAM_IK", "KEK")]).arrange(RIGHT, buff=0.4)
        q = T("nereden geliyor?", 18, GOLD, BOLD)
        kg = VGroup(ks, q).arrange(RIGHT, buff=0.4).move_to([0, -2.0, 0])
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("Kimlik doğrulama", 2.0))
        self.play(FadeIn(nxt[2]), FadeIn(tg_[0], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("şifreleme ve bütünlük", 3.5))
        self.play(FadeIn(tg_[1:], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("neden yeniden türetildiğini", 6.5))
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.05) for k in ks], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("anahtarların nereden geldiği", 9.8))
        self.play(FadeIn(q, shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(tg_, kg)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP17['n']} · {EP17['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep17_end")
