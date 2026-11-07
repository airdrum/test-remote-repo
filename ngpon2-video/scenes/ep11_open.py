"""S2·B1 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to the season-1 finale quiz (S1·B10)."""
from ep11_common import *

AGENDA = ["Katmanlar: alt katmanlar, hızlar, paketin yolu", "Yönetim kanalları: gömülü, PLOAM, OMCC, ICTP",
          "Kimlikler: genişlikler ve ayrılmış değerler", "Ortam erişimi · PtP WDM · sürümler", "Laboratuvarda: protokol analizörü"]
PX, PY = 3.4, -0.45


class Ep11Open(Act11):
    MANIFEST, FIRST = M11("open"), True

    def construct(self):
        self.beat("o1")
        tag_ = T(f"SEZON 2 · BÖLÜM {EP11['n']} · {tr_upper(EP11['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX + 0.2, PY, 0])
        cx = PX + 0.2
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        s2 = pill("SEZON 2", GOLD, 18).move_to([cx, PY + 2.4, 0])
        num = T(f"{EP11['n']:02d}", 110, ACC, BOLD)
        sub = fit(T(EP11["sub"], 22, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP11["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.25).move_to([cx, PY + 0.95, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(s2), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        l1 = T("Sezon 1", 18, MUTED, BOLD)
        t1 = VGroup(*[tile(s, MUTED, 1.55, 0.44, 16, 0.12) for s in ("dalga boyları", "güç bütçeleri", "burst'ler")]).arrange(RIGHT, buff=0.12)
        r1 = VGroup(l1, t1).arrange(RIGHT, buff=0.25).move_to([cx, PY - 1.45, 0])
        l2 = T("Sezon 2", 18, ACC, BOLD)
        t2 = tile("G.989.3 · iletim yakınsama (TC) katmanı", ACC, 4.85, 0.5, 17, 0.2)
        r2 = VGroup(l2, t2).arrange(RIGHT, buff=0.25)
        r2.move_to([cx, PY - 2.35, 0]).align_to(r1, LEFT)
        self.at(self.cue("Birinci sezonda ışığın kendisini", 2.7))
        self.play(FadeIn(l1, shift=RIGHT * 0.1), run_time=0.4)
        for k, key in enumerate(("dalga boyları", "güç bütçeleri", "burst'ler")):
            self.at(self.cue(key, 6.3 + 1.2 * k))
            self.play(FadeIn(t1[k], shift=UP * 0.1), run_time=0.35)
        self.at(self.cue("Bu sezon ışığın taşıdığı dili", 9.6))
        self.play(FadeIn(l2, shift=RIGHT * 0.1), t1.animate.set_opacity(0.5), run_time=0.4)
        self.at(self.cue("G.989.3", 13.2))
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(s2, cover, r1, r2)

        # o2 — layers, rates, the path of a packet
        self.beat("o2")
        names = [("Servis uyarlama", SAC), ("Çerçeveleme", FSC), ("Fiziksel uyarlama", PHC)]
        sl = VGroup(*[tile(n, c, 4.4, 0.52, 18, 0.18) for n, c in names]).arrange(DOWN, buff=0.08)
        pmd = tile("PMD (G.989.2)", PMDC, 4.4, 0.42, 16, 0.12, MUTED)
        stack = VGroup(sl, pmd).arrange(DOWN, buff=0.16).move_to([cx, PY + 1.45, 0])
        rates = VGroup(*[tile(s, R10 if i >= 1 else R25, 1.35, 0.44, 15, 0.15) for i, s in enumerate(("2,5 / 2,5", "10 / 2,5", "10 / 10", "10 / 10+2,5"))]).arrange(RIGHT, buff=0.1)
        rates.move_to([cx, PY - 0.55, 0])
        rl = T("↓ / ↑ Gbit/s", 14, MUTED).next_to(rates, DOWN, buff=0.08)
        chain = ["paket", "XGEM", "FS", "FEC", "PHY"]
        ch = VGroup()
        for i, s in enumerate(chain):
            ch.add(tile(s, [MUTED, SAC, FSC, PHC, PHC][i], 0.95, 0.44, 15, 0.15))
        ch.arrange(RIGHT, buff=0.28).move_to([cx, PY - 1.95, 0])
        arr = VGroup(*[Arrow(ch[i].get_right(), ch[i + 1].get_left(), buff=0.03, color=MUTED, stroke_width=2, tip_length=0.1, max_tip_length_to_length_ratio=0.5) for i in range(4)])
        ph = T("ışık", 16, GOLD, BOLD).next_to(ch, RIGHT, buff=0.15)
        self.focus(0, VGroup(stack, rates, rl, ch, arr, ph))
        self.at(self.cue("üç alt katmanı", 1.3))
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in sl], lag_ratio=0.25), FadeIn(pmd), run_time=0.9)
        self.at(self.cue("hat hızı kombinasyonları", 3.7))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rates], lag_ratio=0.15), FadeIn(rl), run_time=0.8)
        self.at(self.cue("kullanıcı paketinin", 5.8))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in ch], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.2), run_time=1.2)
        self.play(FadeIn(ph, shift=RIGHT * 0.1), run_time=0.3)
        self.end(pad=0.05)

        # o3 — management channels
        self.beat("o3")
        chs = VGroup(*[tile(s, c, 1.9, 0.6, 17, 0.18) for s, c in (("Gömülü OAM", EMB), ("PLOAM", PLC), ("OMCC", OMC))]).arrange(RIGHT, buff=0.15)
        chs.move_to([cx, PY + 1.2, 0])
        onu = onu_box("ONU", ONUC, 1.4, 0.55).move_to([cx, PY + 0.05, 0])
        lk = VGroup(*[Line(c.get_bottom(), onu.get_top(), color=c[0].get_stroke_color(), stroke_width=2) for c in chs])
        c1 = ct_box("OLT CT 1", OLTC, 1.6, 0.5, 16).move_to([cx - 1.9, PY - 1.6, 0])
        c2 = ct_box("OLT CT 2", OLTC, 1.6, 0.5, 16).move_to([cx + 1.9, PY - 1.6, 0])
        ic = DoubleArrow(c1.get_right(), c2.get_left(), buff=0.08, color=ICT, stroke_width=3, tip_length=0.15)
        icl = T("ICTP", 18, ICT, BOLD).next_to(ic, UP, buff=0.08)
        self.focus(1, VGroup(chs, onu, lk, c1, c2, ic, icl))
        self.play(FadeIn(onu), run_time=0.3)
        self.at(self.cue("gömülü işletme alanları", 2.0))
        self.play(FadeIn(chs[0], shift=DOWN * 0.1), Create(lk[0]), run_time=0.4)
        self.at(self.cue("PLOAM", 4.0))
        self.play(FadeIn(chs[1], shift=DOWN * 0.1), Create(lk[1]), run_time=0.3)
        self.at(self.cue("OMCC ve", 4.5))
        self.play(FadeIn(chs[2], shift=DOWN * 0.1), Create(lk[2]), run_time=0.3)
        self.at(self.cue("kanal sonlandırıcıları arasındaki", 5.5))
        self.play(FadeIn(c1), FadeIn(c2), GrowFromCenter(ic), FadeIn(icl), run_time=0.7)
        self.end(pad=0.05)

        # o4 — identifiers
        self.beat("o4")
        ids = [("NG2SYS ID", 20), ("PON-ID", 32), ("ONU-ID", 10), ("Alloc-ID", 14), ("XGEM Port-ID", 16)]
        rows = VGroup()
        for nm, b in ids:
            bar = Rectangle(width=b * 0.11, height=0.36, stroke_color=ACC, stroke_width=1.5, fill_color=ACC, fill_opacity=0.22)
            rows.add(VGroup(T(nm, 17, TXT, BOLD), bar, T(f"{b} bit", 15, ACC, BOLD)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.2)
            r[2].next_to(r[1], RIGHT, buff=0.12)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for r in rows:
            r[1].align_to(rows, LEFT).shift(RIGHT * 1.75)
            r[2].next_to(r[1], RIGHT, buff=0.12)
        rows.move_to([cx, PY + 0.95, 0])
        res = VGroup(*[tag(s, GOLD, 16) for s in ("1021", "1022", "1023", "65535")]).arrange(RIGHT, buff=0.15).move_to([cx, PY - 1.05, 0])
        fg = VGroup(pill("kanal devri: kalır", GOOD, 16), pill("O1: unutulur", WARN, 16)).arrange(RIGHT, buff=0.25).move_to([cx, PY - 2.0, 0])
        self.focus(2, VGroup(rows, res, fg))
        self.at(self.cue("kimin kim olduğunu", 1.6))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15), run_time=1.0)
        self.at(self.cue("genişlikleri", 6.7))
        self.play(LaggedStart(*[Indicate(r[2], color=GOLD, scale_factor=1.15) for r in rows], lag_ratio=0.1), run_time=0.8)
        self.at(self.cue("ayrılmış değerleri", 7.8))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in res], lag_ratio=0.15), run_time=0.7)
        self.at(self.cue("ne zaman unutulduğu", 9.4))
        self.play(FadeIn(fg, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o5 — media access, PtP WDM, edition history
        self.beat("o5")
        fx0, fx1, fy = cx - 2.7, cx + 2.7, PY + 1.45
        frame = Rectangle(width=fx1 - fx0, height=0.5, stroke_color=MUTED, stroke_width=1.5).move_to([cx, fy, 0])
        bursts = VGroup(*[Rectangle(width=w, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.6).move_to([fx0 + a + w / 2, fy, 0])
                          for a, w, c in ((0.25, 1.2, R10), (1.65, 0.8, R25), (2.7, 1.5, R10), (4.4, 0.7, R25))])
        fl = T("↑ 125 µs · BWmap", 15, MUTED).next_to(frame, DOWN, buff=0.08)
        ptp = pill("PtP WDM · AMCC TC", PTPC, 18).move_to([cx, PY + 0.05, 0])
        yrs = ["2015", "2021", "2023", "2025"]
        tl = VGroup(*[VGroup(Dot(radius=0.08, color=ACC if i == 3 else MUTED), T(y, 16, ACC if i == 3 else MUTED, BOLD)) for i, y in enumerate(yrs)])
        for d in tl:
            d[1].next_to(d[0], DOWN, buff=0.1)
        tl.arrange(RIGHT, buff=1.0).move_to([cx, PY - 1.6, 0])
        tln = Line(tl[0][0].get_center(), tl[-1][0].get_center(), color=MUTED, stroke_width=2)
        self.focus(3, VGroup(frame, bursts, fl, ptp, tl, tln))
        self.play(Create(frame), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bursts], lag_ratio=0.2), FadeIn(fl), run_time=0.9)
        self.at(self.cue("noktadan noktaya WDM", 1.7))
        self.play(FadeIn(ptp, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("sürüm geçmişi", 5.0))
        self.play(Create(tln), LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in tl], lag_ratio=0.15), run_time=0.8)
        self.end(pad=0.05)

        # o6 — lab bench 2.0
        self.beat("o6")
        pm = instr("PM", 1.6, 1.15, "−18,2 dBm", None, ACC).move_to([cx - 1.6, PY + 1.45, 0])
        osa = instrument("OSA", 1.6, 1.15).move_to([cx + 1.6, PY + 1.45, 0])
        pa = pa_icon(2.2, 1.45).move_to([cx - 1.4, PY - 1.2, 0])
        em = emu_icon(2.2, 1.45).move_to([cx + 1.4, PY - 1.2, 0])
        nw = T("yeni", 15, GOLD, BOLD).next_to(VGroup(pa, em), UP, buff=0.12)
        self.focus(4, VGroup(pm, osa, pa, em, nw))
        self.play(FadeIn(pm, shift=UP * 0.1), FadeIn(osa, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("bu kez bir güç ölçer", 3.9))
        self.play(pm.animate.set_opacity(0.45), osa.animate.set_opacity(0.45), run_time=0.5)
        self.at(self.cue("bir protokol analizörü", 7.6))
        self.play(FadeIn(pa, shift=UP * 0.15), FadeIn(nw), run_time=0.6)
        self.at(self.cue("OLT emülatörüyle", 9.3))
        self.play(FadeIn(em, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep11_open")

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


def ct_lamp(name, color, on, w=1.75, h=0.5, size=16):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.2, fill_color=PANEL, fill_opacity=1)
    t = tf(name, size, TXT, BOLD, w=w - 0.45).move_to(r).shift(LEFT * 0.15)
    return VGroup(r, t, lamp(on, 0.08).move_to(r.get_right() + LEFT * 0.2))


class Ep11Recap(Act11):
    HDR, MANIFEST, FIRST = f"SEZON 2 · BÖLÜM {K11} · ÖNCEKİ BÖLÜMDE", M11("recap"), True

    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.2)

    def construct(self):
        # a1 — Type B protection: why no retuning, and the condition
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Sezon 1 · Bölüm 10 · Sahaya İniş")
        self.at(self.cue("Birinci soru", 4.0))
        self.to_header(tc)
        self.set_badge("ozet")
        q1 = self.qhead(1, "B tipi korumada ONU neden yeniden ayarlanmaz? Etkili olması için koşul ne?", CH[0])
        ca = ct_lamp("CT · aktif", ACC, True).move_to([-5.2, 0.75, 0])
        cb = ct_lamp("CT · bekleme", S1C, False).move_to([-5.2, -0.65, 0])
        spl = splitter(0.26).move_to([-2.6, 0.05, 0])
        fa = Line(ca.get_right(), spl.get_left() + UP * 0.08, color=FEED, stroke_width=3)
        fb = Line(cb.get_right(), spl.get_left() + DOWN * 0.08, color=FEED, stroke_width=3)
        onu = onu_box("ONU", ONUC, 1.2, 0.6).move_to([-0.75, 0.05, 0])
        fo = Line(spl.get_right(), onu.get_left(), color=FEED, stroke_width=3)
        cp = T("aynı kanal çifti", 16, GOLD, BOLD).next_to(VGroup(ca, cb), UP, buff=0.18)
        cut = xmark(Square(0.26).move_to(fa.point_from_proportion(0.45)), WARN, 4)
        olt_sw = T("anahtarlama: OLT tarafı", 18, GOOD, BOLD).next_to(VGroup(ca, cb), DOWN, buff=0.3).align_to(ca, LEFT)
        ok = T("ayar yok ✓", 18, GOOD, BOLD).next_to(onu, DOWN, buff=0.22)
        x0, x1, yt = 0.9, 6.5, -0.15
        tax = Arrow([x0, yt, 0], [x1, yt, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.15)
        tlb = T("zaman", 14, MUTED).next_to(tax, DOWN, buff=0.08).align_to(tax, RIGHT)
        mk = lambda x, s, c, up: VGroup(Line([x, yt - 0.18, 0], [x, yt + 0.18, 0], color=c, stroke_width=4),
                                        tf(s, 16, c, BOLD, w=2.4).next_to([x, yt, 0], UP if up else DOWN, buff=0.28))
        m0 = mk(1.25, "kesinti", WARN, True)
        m1 = mk(3.2, "↓ senkron geri", GOOD, False)
        m2 = mk(5.6, "ONU ayar kararı", WARN, True)
        cond = pill("koşul: ↓ senkron, ayar kararından ÖNCE gelmeli", GOOD, 18).move_to([3.7, -1.75, 0])
        fit(cond, 5.9)
        self.play(FadeIn(q1, shift=RIGHT * 0.2), self.set_src("G.989.3 §18.1 (B tipi koruma)"), run_time=0.6)
        self.play(FadeIn(ca), FadeIn(cb), Create(fa), Create(fb), FadeIn(spl), Create(fo), FadeIn(onu), run_time=0.8)
        self.at(self.cue("anahtarlama OLT tarafında", 8.0))
        self.play(Create(cut), fa.animate.set_stroke(WARN, opacity=0.5), FadeIn(olt_sw, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("aynı kanal çiftine bakan", 12.0))
        self.play(FadeIn(cp), run_time=0.4)
        self.at(self.cue("bekleme tarafındaki devralır", 16.0))
        self.play(Transform(ca[2], lamp(False, 0.08).move_to(ca[2])), Transform(cb[2], lamp(True, 0.08).move_to(cb[2])), fb.animate.set_stroke(GOOD), run_time=0.7)
        self.at(self.cue("ONU aynı kanal çiftinde kalır", 19.3))
        self.play(FadeIn(ok, shift=UP * 0.1), Indicate(onu, color=GOOD, scale_factor=1.06), run_time=0.6)
        self.at(self.cue("Korumanın etkili olması", 22.0))
        self.play(GrowArrow(tax), FadeIn(tlb), FadeIn(m0), run_time=0.6)
        self.at(self.cue("aşağı yön senkronunun", 25.0))
        self.play(FadeIn(m1, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("karar vermeden önce", 27.5))
        self.play(FadeIn(m2, shift=DOWN * 0.1), run_time=0.4)
        self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        # a2 — why the OLT Rx power reading depends on burst length
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "OLT'nin alınan güç ölçümü neden burst'ün uzunluğuna bağlıdır?", CH[1])
        x0, yb = -6.2, -1.6
        base = Line([x0, yb, 0], [-0.4, yb, 0], color=MUTED, stroke_width=2)
        bl = T("zaman", 14, MUTED).next_to(base, DOWN, buff=0.08).align_to(base, RIGHT)
        bx0, bx1, bh = -5.4, -1.2, 1.6
        burst = Polygon([bx0, yb, 0], [bx0 + 0.12, yb + bh, 0], [bx1 - 0.12, yb + bh, 0], [bx1, yb, 0], stroke_color=TW_US, stroke_width=2.5, fill_color=TW_US, fill_opacity=0.25)
        btl = T("burst", 16, TW_US, BOLD).next_to(burst, UP, buff=0.1).align_to(burst, LEFT)
        avg = DashedLine([bx0 + 0.12, yb + bh * 0.62, 0], [bx1 - 0.12, yb + bh * 0.62, 0], color=GOLD, stroke_width=2.5)
        avgl = T("ortalama güç", 16, GOLD, BOLD).next_to(avg, UP, buff=0.06).align_to(avg, RIGHT).shift(LEFT * 0.1)
        wx0, wx1 = -3.6, -2.2
        win = Rectangle(width=wx1 - wx0, height=bh + 0.25, stroke_color=ACC, stroke_width=2.5, fill_color=ACC, fill_opacity=0.12).move_to([(wx0 + wx1) / 2, yb + (bh + 0.25) / 2, 0])
        wl = T("300 ns", 18, ACC, BOLD).next_to(win, DOWN, buff=0.38)
        wl2 = T("dedektör tepki süresi", 15, ACC).next_to(wl, DOWN, buff=0.04)
        tb = table(["Hız", "300 ns içindeki bit"], [["2,48832 Gbit/s", "746 bit"], ["9,95328 Gbit/s", "≈ 3000 bit (2986)"]], [2.6, 3.0], size=19, hsize=16, row_h=0.55)
        tb.move_to([3.4, 0.55, 0])
        r1 = VGroup(T("✓ doğru anda ölç", 19, GOOD, BOLD), T("✓ burst ≥ tepki süresi", 19, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, -1.5, 0])
        short = Rectangle(width=0.5, height=bh * 0.8, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.2).move_to([5.6, -1.45, 0])
        shx = T("kısa burst ✗", 15, WARN, BOLD).next_to(short, DOWN, buff=0.08)
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.2 Ek II · Tablo II.1, Not 3"), run_time=0.6)
        self.play(Create(base), FadeIn(bl), FadeIn(burst), FadeIn(btl), run_time=0.7)
        self.at(self.cue("bir burst sırasındaki ortalama güçtür", 6.5))
        self.play(Create(avg), FadeIn(avgl), run_time=0.6)
        self.at(self.cue("tepki süresi üç yüz", 10.6))
        self.play(FadeIn(win), FadeIn(wl), FadeIn(wl2), run_time=0.6)
        self.at(self.cue("yedi yüz kırk altı", 14.6))
        self.play(FadeIn(tb[0]), FadeIn(tb[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("yaklaşık üç bin bit", 18.2))
        self.play(FadeIn(tb[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("doğru anda yapılmalı", 20.9))
        self.play(FadeIn(r1[0], shift=RIGHT * 0.1), win.animate.shift(RIGHT * 0.4), run_time=0.6)
        self.at(self.cue("yetecek kadar uzun", 24.3))
        self.play(FadeIn(r1[1], shift=RIGHT * 0.1), FadeIn(short), FadeIn(shx), run_time=0.6)
        self.end(pad=0.1)

        # a3 — emergency stop survives power cycling
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "Acil durdurmadaki bir ONU, gücü kesilip geri gelince ne yapar?", CH[3])
        o7 = sbox("O7 · Acil durdurma", None, WARN, 3.2, 0.8, 21).move_to([-3.6, 0.45, 0])
        lp = VGroup(T("Tx", 16, MUTED, BOLD), lamp(False, 0.11)).arrange(RIGHT, buff=0.12).next_to(o7, DOWN, buff=0.15)
        l1 = CurvedArrow(o7.get_corner(UL) + RIGHT * 0.4, o7.get_corner(UR) + LEFT * 0.4, angle=-2.2, color=WARN, stroke_width=2.5, tip_length=0.14)
        l1t = T("yeniden başlatma · güç kesintisi", 16, WARN, BOLD).next_to(l1, UP, buff=0.08)
        scan_y = -1.2
        chs = VGroup(*[VGroup(Line([0, -0.3, 0], [0, 0.3, 0], color=CH[i], stroke_width=5), T(f"λ{i + 1}", 15, CH[i], BOLD)) for i in range(4)])
        for c in chs:
            c[1].next_to(c[0], DOWN, buff=0.06)
        chs.arrange(RIGHT, buff=0.55).move_to([-3.6, scan_y, 0])
        cur = SurroundingRectangle(chs[0], color=GOLD, buff=0.08)
        scl = T("kanalları tarar", 16, GOLD, BOLD).next_to(chs, LEFT, buff=0.3)
        bx0, by0 = 0.6, -2.2
        bars = VGroup()
        labs = ["Tseek", "2·Tseek", "4·Tseek", "8·Tseek"]
        for i, s in enumerate(labs):
            hgt = 0.22 * 2 ** i
            r = Rectangle(width=0.8, height=hgt, stroke_width=0, fill_color=GOLD, fill_opacity=0.6).move_to([bx0 + i * 1.1, by0 + hgt / 2, 0])
            bars.add(VGroup(r, T(s, 14, GOLD, BOLD).next_to(r, DOWN, buff=0.08)))
        dots = T("…", 24, GOLD, BOLD).move_to([bx0 + 4 * 1.1 - 0.2, by0 + 0.3, 0])
        cap = tag("≈ 1 dk", GOLD, 18).move_to([bx0 + 5 * 1.1 - 0.1, by0 + 0.35, 0])
        bt = T("her başarısız turda bekleme ×2", 17, GOLD, BOLD).move_to([2.9, -0.15, 0])
        rel = Arrow([6.3, 0.45, 0], o7.get_right(), buff=0.08, color=GOOD, stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.1)
        rlt = T("yalnızca OLT: yeniden etkinleştirme komutu", 17, GOOD, BOLD).next_to(rel, UP, buff=0.1)
        s2 = pill("→ Sezon 2", ACC, 20).move_to([5.3, 2.2, 0])
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.3 Tablo 12-1 (O7) · Ek XI (Amd.1, 2023) · §11.3.3.5"), run_time=0.6)
        self.play(FadeIn(o7, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Acil durdurmada kalır", 6.5))
        self.play(Create(l1), FadeIn(l1t), run_time=0.7)
        self.at(self.cue("Vericisi kapalı kalır", 13.3))
        self.play(FadeIn(lp), run_time=0.4)
        self.at(self.cue("kanalları tarar", 15.2))
        self.play(FadeIn(chs), FadeIn(scl), Create(cur), run_time=0.5)
        self.play(cur.animate.move_to(chs[3]), run_time=0.8)
        self.at(self.cue("ikiye katlayarak", 18.0))
        self.play(FadeIn(bt), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3), LaggedStart(*[FadeIn(b[1]) for b in bars], lag_ratio=0.3), run_time=1.4)
        self.at(self.cue("bir dakikaya kadar", 21.5))
        self.play(FadeIn(dots), FadeIn(cap, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("yeniden etkinleştirme komutu", 25.5))
        self.play(GrowArrow(rel), FadeIn(rlt), o7[0].animate.set_stroke(GOOD), run_time=0.7)
        self.at(self.cue("Şimdi ikinci sezona", 29.6))
        self.play(FadeIn(s2, shift=LEFT * 0.15), run_time=0.5)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep11_recap")
