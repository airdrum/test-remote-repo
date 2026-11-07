"""B09 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to the B08 quiz."""
from ep09_common import *

AGENDA = ["Mimari ve spektrum: seçilen ↔ yönlendirilen", "A ekinin tabloları: hız sınıfları, FEC, bütçe",
          "AMCC: 10 Gbit/s üstünde 115 kb/s", "C eki (düşük kayıp) · TC köprüsü", "Laboratuvar: verici, bütçe, AMCC"]
PX, PY = 3.4, -0.45
CX = PX + 0.2


class Ep09Open(Narrated):
    MANIFEST = M9("open")

    def q(self, sub, default):
        b = self.bmap[self.timeline[-1]["id"]]
        cues = b["cues"]
        for k, c in enumerate(cues):
            if sub in c["text"]:
                t1 = cues[k + 1]["t"] if k + 1 < len(cues) else b["duration"]
                frac = c["text"].index(sub) / max(len(c["text"]), 1)
                return max(0.0, c["t"] + frac * (t1 - c["t"]) - 0.2)
        print(f"CUE MISS [{b['id']}] {sub!r}", file=sys.stderr)
        return default

    def construct(self):
        self.beat("o1")
        tag_ = T(f"BÖLÜM {EP9['n']} · {tr_upper(EP9['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([CX, PY, 0])
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP9['n']:02d}", 120, ACC, BOLD)
        sub = T(EP9["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP9["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            fit(m, 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([CX, PY + 0.35, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        xs = [CX - 1.65 + 1.1 * i for i in range(4)]
        yd, yb = PY - 2.5, PY - 1.75
        onus = VGroup(*[Dot([x, yd, 0], radius=0.11, color=TXT) for x in xs])
        shared = Line([xs[0] - 0.3, yb, 0], [xs[-1] + 0.3, yb, 0], color=TW_DS, stroke_width=6)
        taps = VGroup(*[Line([x, yb, 0], [x, yd + 0.11, 0], color=TW_DS, stroke_width=2) for x in xs])
        st = T("TWDM: paylaşılan", 15, TW_DS, BOLD).next_to(shared, UP, buff=0.08)
        own = VGroup(*[Line([x, yb + 0.15, 0], [x, yd + 0.11, 0], color=CH[i], stroke_width=6) for i, x in enumerate(xs)])
        ot = T("PtP WDM: her aboneye kendi λ çifti", 15, PTP, BOLD).next_to(own, UP, buff=0.08)
        self.at(self.q("paylaşılan TWDM", 5.5))
        self.play(FadeIn(onus), Create(shared), Create(taps), FadeIn(st), run_time=0.8)
        self.at(self.q("her aboneye kendi", 8.3))
        self.play(ReplacementTransform(VGroup(shared, taps), own), FadeTransform(st, ot), run_time=0.9)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(cover, onus, own, ot)

        # o2 — architecture + spectrum
        self.beat("o2")
        lx, rx, yy = CX - 1.55, CX + 1.55, PY + 1.6
        spl = splitter(0.24).move_to([lx - 0.7, yy, 0])
        onu = sbox("ONU", "λ seçici", PTP, 1.2, 0.75, 15, 14).move_to([lx + 0.65, yy, 0])
        l1 = Line(spl.get_right(), onu.get_left(), color=FEED, stroke_width=2.5)
        c1 = T("seçici ONU'da", 16, PTP, BOLD).move_to([lx, yy - 0.75, 0])
        aw = awg_icon(0.8, 1.0, PTP).move_to([rx - 0.55, yy + 0.05, 0])
        ro = VGroup(*[Line(aw[0].get_right() + UP * (0.3 - 0.2 * k), [rx + 0.9, yy + 0.3 - 0.2 * k, 0], color=CH[k], stroke_width=2.5) for k in range(4)])
        c2 = T("seçici düğümde (AWG)", 16, PTP, BOLD).move_to([rx, yy - 0.75, 0])
        axg, X = nm_axis(1520, 1630, x0=CX - 2.7, x1=CX + 2.5, y=PY - 2.2, step=20, size=14)
        tw = band(X, 1596, 1603, PY - 1.85, 0.5, TW_DS)
        sh = band(X, 1603, 1625, PY - 1.85, 0.5, PTP)
        shl = T("paylaşılan", 14, PTP, BOLD).next_to(sh, UP, buff=0.08).align_to(sh, RIGHT)
        ex = outline_band(X, 1524, 1625, PY - 1.0, 0.36, PTP, "genişletilmiş", 14)
        self.focus(0, VGroup(spl, onu, l1, c1, aw, ro, c2, axg, tw, sh, shl, ex))
        self.at(self.q("ONU'nun seçtiği", 2.2))
        self.play(FadeIn(spl), Create(l1), FadeIn(onu), FadeIn(c1), run_time=0.7)
        self.at(self.q("ağın yönlendirdiği", 4.8))
        self.play(FadeIn(aw), Create(ro), FadeIn(c2), run_time=0.7)
        self.at(self.q("ve paylaşılan", 8.6))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(tw), FadeIn(sh), FadeIn(shl), run_time=0.7)
        self.play(Create(ex[0]), FadeIn(ex[1]), run_time=0.6)
        self.end(pad=0.05)

        # o3 — tables
        self.beat("o3")
        pills = VGroup(*[pill(s, c, 16) for s, c in (("sınıf 1 · ~1,25G", CH[0]), ("sınıf 2 · ~2,5G", CH[1]), ("sınıf 3 · ~10G", CH[2]))]).arrange(RIGHT, buff=0.2)
        fit(pills, 6.0).move_to([CX, PY + 2.3, 0])
        fec = VGroup(pill("FEC'siz · 10⁻¹²", MUTED, 16), pill("FEC'li · 10⁻⁴ / 10⁻³", GOLD, 16)).arrange(RIGHT, buff=0.3).move_to([CX, PY + 1.5, 0])
        ag, Y = v_axis(-34, 8, PY - 2.6, PY + 0.75, CX - 2.6, [-30, -10, 0], size=14, fmt=lambda v: sgn(v))
        cx = [CX - 1.7 + 0.85 * i for i in range(4)]
        dots = VGroup(*[Dot([x, Y(v), 0], radius=0.08, color=PTP) for x, v in zip(cx, [-1, 1, 3, 5])])
        nm = VGroup(*[T(c, 14, MUTED, BOLD).move_to([x, PY - 2.85, 0]) for c, x in zip(CLS, cx)])
        sl = DashedLine([CX - 2.6, Y(-31.5), 0], [cx[-1] + 0.3, Y(-31.5), 0], color=GOOD, stroke_width=2.5)
        slt = T("ONU: sabit", 14, GOOD, BOLD).next_to(sl, UP, buff=0.06).align_to(sl, RIGHT)
        olt_t = T("OLT +2 dB / sınıf", 14, PTP, BOLD).next_to(dots[-1], UP, buff=0.12)
        who = T("sınıf farkını OLT taşır", 18, GOOD, BOLD).move_to([CX + 1.75, PY - 0.4, 0])
        self.focus(1, VGroup(pills, fec, ag, dots, nm, sl, slt, olt_t, who))
        self.at(self.q("üç hat hızı", 1.9))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pills], lag_ratio=0.2), run_time=0.8)
        self.at(self.q("FEC'li ve FEC'siz", 3.5))
        self.play(FadeIn(fec, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ve sınıf farkını", 5.8))
        self.play(Create(ag[0]), FadeIn(ag[1:]), FadeIn(nm), Create(sl), FadeIn(slt), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), run_time=0.9)
        self.play(FadeIn(olt_t), FadeIn(who, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o4 — AMCC whisper
        self.beat("o4")
        bits = [1, 0, 1, 1, 0, 0, 1, 0]
        cur, et, eb, _ = overmod(CX - 2.6, CX + 2.6, PY - 1.25, 2.2, bits, nbits=170, depth=0.24)
        pl = T("yük: 10,3125 Gbit/s", 17, PTP, BOLD).move_to([CX - 1.2, PY + 2.0, 0])
        al = T("AMCC: 115 kb/s · %10", 17, AMC, BOLD).move_to([CX + 1.35, PY + 2.0, 0])
        ab = VGroup(*[T(str(b), 14, AMC, BOLD).move_to([CX - 2.6 + (k + 0.5) * 5.2 / 8, PY - 1.65, 0]) for k, b in enumerate(bits)])
        ex = T("görsel ölçek abartılı", 14, MUTED).move_to([CX, PY - 2.15, 0])
        wh = T("bir fısıltı", 24, AMC, BOLD).move_to([CX, PY - 2.7, 0])
        self.focus(2, VGroup(cur, et, eb, pl, al, ab, ex, wh))
        self.at(self.q("on gigabitlik", 3.9))
        self.play(Create(cur), FadeIn(pl), run_time=1.0)
        self.at(self.q("saniyede yüz on beş", 7.1))
        self.play(Create(et), Create(eb), FadeIn(al), FadeIn(ab), FadeIn(ex), run_time=0.8)
        self.play(FadeIn(wh, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # o5 — Annex C + TC
        self.beat("o5")
        aw = awg_icon(0.9, 1.25, PTP).move_to([CX - 1.6, PY + 1.6, 0])
        ys = [PY + 2.2 - 0.4 * k for k in range(4)]
        drops = VGroup(*[Line(aw[0].get_right() + UP * (0.45 - 0.3 * k), [CX + 1.4, ys[k], 0], color=CH[k], stroke_width=2.5) for k in range(4)])
        ons = VGroup(*[sbox(f"ONU {k + 1}", None, CH[k], 1.0, 0.34, 14).move_to([CX + 1.95, ys[k], 0]) for k in range(4)])
        feed = Line([CX - 2.8, PY + 1.6, 0], aw[0].get_left(), color=FEED, stroke_width=3)
        ll = T("düşük kayıp · λ = port", 15, PTP, BOLD).move_to([CX - 1.25, PY + 0.45, 0])
        fb = frame_bar([("PSB", 1.15, TW_DS), ("başlık", 1.0, AMC), ("PLOAM", 1.25, TW_US), ("yük", 1.2, GOOD), ("BIP", 0.7, MUTED)], CX - 2.65, PY - 0.8, 0.55, 15)
        fbt = T("AMCC çerçevesi", 15, AMC, BOLD).next_to(fb, UP, buff=0.1)
        tcp = pill("kod dönüştürme: 32B/34B · 64B/66B", ACC, 16).move_to([CX, PY - 2.1, 0])
        self.focus(3, VGroup(aw, drops, ons, feed, ll, fb, fbt, tcp))
        self.at(self.q("düşük kayıplı", 1.0))
        self.play(Create(feed), FadeIn(aw), run_time=0.5)
        self.play(LaggedStart(*[Create(d) for d in drops], lag_ratio=0.1), FadeIn(ons), FadeIn(ll), run_time=0.8)
        self.at(self.q("AMCC'nin çerçevesi", 3.6))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in fb], lag_ratio=0.1), FadeIn(fbt), run_time=0.8)
        self.at(self.q("kod dönüştürme", 5.6))
        self.play(FadeIn(tcp, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab
        self.beat("o6")
        pm = instr("PM", 2.15, 1.45, "+3,0 dBm").move_to([CX - 1.55, PY + 1.7, 0])
        bert = instr("BERT", 2.15, 1.45, "BER 10⁻¹²", None, GOOD).move_to([CX + 1.55, PY + 1.7, 0])
        cur, et, eb, _ = overmod(CX - 2.5, CX + 2.5, PY - 1.35, 1.2, [1, 0, 1, 1, 0, 1], nbits=120, depth=0.24, seed=5)
        mt = T("M = %10", 18, AMC, BOLD).next_to(et, UP, buff=0.12)
        pen = pill("AMCC cezası = ?  (standartta yok)", WARN, 16).move_to([CX, PY - 2.35, 0])
        self.focus(4, VGroup(pm, bert, cur, et, eb, mt, pen))
        self.play(FadeIn(pm, shift=UP * 0.15), run_time=0.6)
        self.at(self.q("alıcı bütçesini", 2.2))
        self.play(FadeIn(bert, shift=UP * 0.15), run_time=0.6)
        self.at(self.q("modülasyon indeksini", 3.6))
        self.play(Create(cur), Create(et), Create(eb), FadeIn(mt), run_time=0.8)
        self.at(self.q("AMCC'nin bedelini", 5.6))
        self.play(FadeIn(pen, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep09_open")

    def focus(self, k, teaser):
        it = self.items[k]
        anims = [it.animate.set_opacity(1), it[0].animate.set_color(ACC)]
        if k:
            anims += [self.items[k - 1].animate.set_opacity(0.4), self.items[k - 1][0].animate.set_color(MUTED)]
        tgt = self.bar.copy().next_to(it, LEFT, buff=0.22)
        anims.append(FadeIn(tgt) if k == 0 else Transform(self.bar, tgt))
        if k == 0:
            self.bar = tgt
        if self.cur is not None:
            anims.append(FadeOut(self.cur, shift=LEFT * 0.3))
        self.play(*anims, run_time=0.5)
        self.cur = teaser


class Ep09Recap(Act9):
    HDR, MANIFEST, FIRST = "BÖLÜM 9 · ÖNCEKİ BÖLÜMDE", M9("recap"), True

    def construct(self):
        qa = [("Soru 1", "PtP WDM kanalları neden TWDM'den\nfarklı bir banda yerleştirilir?", CH[0], "a1", 1,
               [("her PtP kanalı tek aboneye ait ve sürekli ↔ TWDM: paylaşılan, burst'lü", "Çünkü her PtP"),
                ("iç içe geçme yasak · koruma bandı ≥ 3 nm ya da ≥ 100 GHz", "iç içe geçmesini"),
                ("paylaşılan spektrumda PtP WDM: 1603 … 1625 nm", "bin altı yüz üç ile")]),
              ("Soru 2", "AMCC nedir ve neden gereklidir?", CH[1], "a2", 2,
               [("PtP hattı istemciyi (10G Ethernet, CPRI) çerçevesine dokunmadan taşır", "örneğin on gigabitlik"),
                ("λ ataması + işletme bilgisi için ayrı bir kanal gerekir", "Dalga boyu ataması"),
                ("AMCC: aynı λ üstünde düşük hız, düşük indeks · PtP WDM'de zorunlu", "aynı dalga boyunun")]),
              ("Soru 3", "Düşük kayıplı PtP WDM neden\nayrı bir ekte (C eki) tanımlanır?", CH[3], "a3", 0,
               [("başka bir ağ: λ seçimi ONU'da değil, dallanma düğümündeki AWG'de", "dalga boyu seçimi ONU'da"),
                ("daha düşük kayıp sınıfları · daha çok kanal · farklı girişim varsayımları", "Daha düşük kayıp"),
                ("→ A ekinin tabloları o ağ için geçersiz", "A ekinin tablolarını")])]
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 8 · Kalabalığı Dinlemek")
        self.at(self.cue("Birinci soru", 1.7))
        self.to_header(tc)
        self.set_badge("ozet")
        prev = None
        first = True
        for title, qs, c, bid, hl, ans_lines in qa:
            if not first:
                self.beat(bid)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            qt = VGroup(T(title, 26, c, BOLD), T(qs, 28, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.25).to_edge(LEFT, buff=1.0)
            box_ = RoundedRectangle(corner_radius=0.18, width=11.8, height=2.5, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.45)
            lines = VGroup(*[T(s, 22, GOOD if k == hl else TXT, BOLD if k == hl else NORMAL) for k, (s, _) in enumerate(ans_lines)])
            at = VGroup(T("Cevap", 20, GOOD, BOLD), *lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            fit(at, 11.2)
            at.move_to(box_).align_to(box_, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(self.q(ans_lines[0][1], 2.0))
            self.play(FadeIn(box_), FadeIn(at[0]), FadeIn(lines[0], shift=UP * 0.1), run_time=0.6)
            for k in (1, 2):
                self.at(self.q(ans_lines[k][1], 7 + 7 * k))
                self.play(FadeIn(lines[k], shift=UP * 0.1), run_time=0.5)
            prev = VGroup(qt, box_, at)
            self.end(pad=0.1)
            first = False
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep09_recap")
