"""B01 · Perde 4 — Referans mimari (G.989.2 Şekil 6-1, yeniden çizim)."""
from kit import *

HDR4 = "BÖLÜM 1 · PERDE 4 — Referans mimari"
MAN4 = "build/v4/ep01_p4/audio_proc/manifest.json"


def arch():
    """Logical reference architecture (redrawn after G.989.2 Figure 6-1). Returns dict of parts."""
    d = {}
    yc = -0.55
    tw = VGroup(*[box(1.55, 0.46, f"TWDM CT{i + 1}", CH[i], 14).move_to([-5.75, yc + 1.75 - i * 0.6, 0]) for i in range(4)])
    pp = VGroup(*[box(1.55, 0.46, f"PtP CT{i + 1}", PINK, 14).move_to([-5.75, yc - 0.75 - i * 0.6, 0]) for i in range(2)])
    d["tw"], d["pp"] = tw, pp
    wm = box(0.75, 4.1, None, "#3B4A75").move_to([-3.55, yc + 0.3, 0])
    d["wm"] = VGroup(wm, T("WM", 18, TXT, BOLD).move_to(wm))
    d["ct_lines"] = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=c[0].get_stroke_color(), stroke_width=2.5) for c in [*tw, *pp]])
    ce = box(0.95, 1.1, "CE", "#3B4A75", 18).move_to([-1.35, yc + 0.3, 0])
    d["ce"] = ce
    d["wm_ce"] = Line(wm.get_right() + UP * 0.0, [ce.get_left()[0], wm.get_y(), 0], color=FEED, stroke_width=3.5)
    leg = VGroup(*[box(1.75, 0.42, s, LEGACY, 13) for s in ("GPON OLT", "XG(S)-PON OLT", "RF video")]).arrange(DOWN, buff=0.08)
    leg.move_to([-1.2, 0, 0]).align_to([0, -1.0, 0], UP)
    d["leg"] = leg
    d["leg_line"] = Line(ce.get_bottom(), leg.get_top(), color=LEGACY, stroke_width=2.5)
    sp = splitter(0.36).move_to([2.55, yc + 0.3, 0])
    d["sp"] = sp
    d["feeder"] = Line(ce.get_right(), sp.get_left(), color=FEED, stroke_width=4)
    onus = VGroup()
    for i in range(4):
        b = box(2.15, 0.62, None, "#94A3B8").move_to([5.55, yc + 1.95 - i * 1.1, 0])
        lab = T("ONU", 16, TXT, BOLD).move_to(b).align_to(b, LEFT).shift(RIGHT * 0.12)
        tx = T("Tx⟳", 14, GOLD, BOLD).next_to(lab, RIGHT, buff=0.2)
        rx = T("Rx⟳", 14, CH[1], BOLD).next_to(tx, RIGHT, buff=0.15)
        onus.add(VGroup(b, lab, tx, rx))
    d["onus"] = onus
    d["drops"] = VGroup(*[Line(sp.get_right(), o.get_left(), color="#94A3B8", stroke_width=2) for o in onus])
    br = BraceBetweenPoints([ce.get_right()[0], yc - 2.25, 0], [onus.get_left()[0] - 0.1, yc - 2.25, 0], direction=DOWN, color=MUTED)
    d["odn"] = VGroup(br, T("ODN — fiber + pasif ayırıcılar", 16, MUTED).next_to(br, DOWN, buff=0.05))
    d["olt_lbl"] = T("OLT tarafı", 16, MUTED).move_to([-4.6, yc + 2.55, 0])
    d["all"] = VGroup(d["tw"], d["pp"], d["ct_lines"], d["wm"], d["wm_ce"], d["ce"], d["leg"], d["leg_line"], d["feeder"], d["sp"], d["drops"], d["onus"], d["odn"], d["olt_lbl"])
    return d


def marker(x, y0, y1, label, color, below=True):
    l = DashedLine([x, y0, 0], [x, y1, 0], color=color, stroke_width=2.5, dash_length=0.08)
    t = T(label, 15, color, BOLD).next_to(l, DOWN if below else UP, buff=0.05)
    return VGroup(l, t)


class P4A(Act):
    HDR, MANIFEST, FIRST = HDR4, MAN4, True

    def construct(self):
        self.beat("s1")
        tc = self.title_card("PERDE 4", "Referans mimari")
        self.at(self.cues[2] - 0.2)
        self.to_header(tc)
        h = self.show_heading("Şekil 6-1: mantıksal referans mimari")
        note = T("(G.989.2 Şekil 6-1'in sadeleştirilmiş yeniden çizimi)", 15, MUTED).next_to(h, DOWN, buff=0.08, aligned_edge=LEFT)
        self.play(FadeIn(note), self.set_src("G.989.2 §6, Şekil 6-1"), run_time=0.5)
        self.end(pad=0.05)
        d = arch()
        self.beat("s2")
        self.play(FadeIn(d["olt_lbl"]), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in d["tw"]], lag_ratio=0.15), run_time=1.2)
        pair = T("kanal çifti = λ↓ + λ↑", 18, ACC, BOLD).next_to(d["pp"], DOWN, buff=0.25)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(pair), *[Indicate(c, color=c[0].get_stroke_color(), scale_factor=1.05) for c in d["tw"]], run_time=0.9)
        self.at(self.cues[3])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in d["pp"]], lag_ratio=0.2), run_time=0.7)
        self.end(pad=0.05)

        self.beat("s3")
        self.play(FadeOut(pair), FadeIn(d["wm"]), LaggedStart(*[Create(l) for l in d["ct_lines"]], lag_ratio=0.08), run_time=1.2)
        self.at(self.cues[3])
        self.play(Create(d["wm_ce"]), run_time=0.5)
        dots = [glow_dot(d["ct_lines"][i].get_stroke_color(), 0.05).move_to(d["ct_lines"][i].get_start()) for i in range(6)]
        paths = [VMobject().set_points_as_corners([d["ct_lines"][i].get_start(), d["ct_lines"][i].get_end(), d["wm_ce"].get_end()]) for i in range(6)]
        self.add(*dots)
        self.play(*[MoveAlongPath(dd, p) for dd, p in zip(dots, paths)], run_time=1.3, rate_func=linear)
        self.remove(*dots)
        self.end(pad=0.05)

        self.beat("s4")
        self.play(FadeIn(d["ce"], scale=0.9), run_time=0.6)
        self.at(self.cues[1])
        self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.15) for l in d["leg"]], lag_ratio=0.2), Create(d["leg_line"]), run_time=1.1)
        ce_t = T("birlikte çalışma\nelemanı", 14, MUTED).next_to(d["ce"], UP, buff=0.12)
        self.play(FadeIn(ce_t), run_time=0.4)
        self.end(pad=0.05)

        self.beat("s5")
        self.play(Create(d["feeder"]), FadeIn(d["sp"]), run_time=0.8)
        self.play(LaggedStart(*[Create(l) for l in d["drops"]], lag_ratio=0.1), FadeIn(d["odn"]), run_time=0.8)
        wl = T("güç ayırıcı esas · dalga boyu ayırıcıya da izin var", 15, MUTED).next_to(d["sp"], UP, buff=0.55)
        self.at(self.cues[2])
        self.play(FadeIn(wl), run_time=0.5)
        self.at(self.cues[4])
        self.play(LaggedStart(*[FadeIn(o, shift=LEFT * 0.2) for o in d["onus"]], lag_ratio=0.15), run_time=1.0)
        self.play(*[Indicate(VGroup(o[2], o[3]), color=WHITE, scale_factor=1.2) for o in d["onus"]], run_time=0.8)
        self.end(pad=0.05)

        self.beat("s6")
        grp = VGroup(d["tw"], d["pp"], d["wm"], d["ce"])
        one = DashedVMobject(SurroundingRectangle(grp, buff=0.18, corner_radius=0.15, color=GOLD), num_dashes=70)
        one_t = T("tek cihazda bütünleşik olabilir", 16, GOLD, BOLD).next_to(one, DOWN, buff=0.08)
        self.at(self.cues[2] - 0.3)
        self.play(Create(one), FadeIn(one_t), run_time=0.9)
        sep1 = DashedVMobject(SurroundingRectangle(VGroup(d["tw"], d["pp"]), buff=0.12, corner_radius=0.12, color=GOLD), num_dashes=50)
        sep2 = DashedVMobject(SurroundingRectangle(VGroup(d["wm"], d["ce"]), buff=0.12, corner_radius=0.12, color=GOLD), num_dashes=50)
        sep_t = T("ya da ayrı kutular / saha paneli", 16, GOLD, BOLD).move_to(one_t)
        self.at(self.cues[4] - 0.3)
        self.play(ReplacementTransform(one, VGroup(sep1, sep2)), FadeTransform(one_t, sep_t), self.set_src("G.989.2 §6.1"), run_time=1.0)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p4A")


class P4B(Act):
    HDR, MANIFEST = HDR4, MAN4

    def construct(self):
        self.beat("s6a")
        h = self.show_heading("Senaryo: çalışan bir GPON ağına NG-PON2 eklemek")
        g_olt = box(1.8, 0.7, "GPON OLT", LEGACY, 16).move_to([-5.2, 1.1, 0])
        sp = splitter(0.38).move_to([1.4, -0.3, 0])
        feed = Line([-3.2, -0.3, 0], sp.get_left(), color=FEED, stroke_width=4)
        g_link = VMobject(color=LEGACY, stroke_width=3).set_points_as_corners([g_olt.get_right(), [-3.6, g_olt.get_y(), 0], [-3.6, -0.3, 0], [-3.2, -0.3, 0]])
        users = VGroup(*[box(1.6, 0.5, "GPON ONU", LEGACY, 13).move_to([5.2, 1.6 - i * 0.65, 0]) for i in range(6)])
        drops = VGroup(*[Line(sp.get_right(), u.get_left(), color="#94A3B8", stroke_width=1.8) for u in users])
        self.at(self.cues[1] - 0.2)
        self.play(FadeIn(g_olt), Create(g_link), Create(feed), FadeIn(sp), Create(drops), FadeIn(users), run_time=1.4)
        ce = box(0.9, 0.9, "CE", GOLD, 18).move_to([-3.2, -0.3, 0])
        n_olt = box(1.8, 0.7, "NG-PON2 OLT", ACC, 15).move_to([-5.2, -1.7, 0])
        n_link = VMobject(color=ACC, stroke_width=3).set_points_as_corners([n_olt.get_right(), [-3.2, n_olt.get_y(), 0], ce.get_bottom()])
        co = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=4.0, height=4.0, color=MUTED).move_to([-4.7, -0.3, 0]), num_dashes=60)
        co_t = T("merkez ofis", 15, MUTED).next_to(co, UP, buff=0.05)
        self.at(self.cues[2])
        self.play(FadeIn(co), FadeIn(co_t), FadeIn(ce, scale=0.8), run_time=0.8)
        self.play(FadeIn(n_olt, shift=RIGHT * 0.2), Create(n_link), run_time=0.8)
        ok = T("✓ kesinti yok", 20, GOOD, BOLD).next_to(users, UP, buff=0.15)
        self.at(self.cues[3])
        self.play(FadeIn(ok), run_time=0.5)
        self.at(self.cues[4])
        self.play(*[users[i].animate.become(box(1.6, 0.5, "NG-PON2 ONU", CH[i % 4], 12).move_to(users[i])) for i in (1, 3, 4)], run_time=1.0)
        self.end(pad=0.05)

        self.beat("s6b")
        strip = Line([-6.2, -2.55, 0], [6.2, -2.55, 0], color=MUTED, stroke_width=2)
        X = lambda nm: -6.2 + (nm - 1260) / (1625 - 1260) * 12.4
        bands = VGroup(*[Rectangle(width=X(b) - X(a), height=0.35, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([(X(a) + X(b)) / 2, -2.37, 0])
                         for a, b, c in [(1260, 1280, LEGACY), (1290, 1330, LEGACY), (1480, 1500, LEGACY), (1550, 1560, LEGACY), (1575, 1581, LEGACY),
                                         (1524, 1544, "#A78BFA"), (1596, 1603, ACC)]])
        bl = T("eski sistemler (gri) ve NG-PON2 (renkli) farklı bantlarda", 16, MUTED).next_to(strip, DOWN, buff=0.08)
        self.at(self.cues[1])
        self.play(Create(strip), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bands], lag_ratio=0.1), FadeIn(bl), run_time=1.4)
        nx = T("→ Bölüm 3: Renk Haritası", 20, ACC, BOLD).next_to(bl, DOWN, buff=0.15)
        self.at(self.cues[3])
        self.play(FadeIn(nx), run_time=0.5)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p4B")


class P4C(Act):
    HDR, MANIFEST = HDR4, MAN4

    def construct(self):
        d = arch()
        h = self.heading("Referans noktaları")
        self.beat("s7")
        d["all"].remove(d["odn"])
        self.play(FadeIn(h, shift=RIGHT * 0.2), FadeIn(d["all"]), self.set_src("G.989.2 §6"), run_time=0.9)
        self.set_badge("std")
        lg = VGroup(T("S: ağa gönderim arayüzü", 18, TXT), T("R: ağdan alım arayüzü", 18, TXT)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.85)
        self.at(self.cues[2])
        self.play(FadeIn(lg[0]), run_time=0.4)
        self.at(self.cues[4])
        self.play(FadeIn(lg[1]), run_time=0.4)
        y0, y1 = -2.7, 1.6
        m_sr = marker((d["wm"].get_right()[0] + d["ce"].get_left()[0]) / 2, y0, y1, "S/R", ACC)
        m_rs = marker(d["onus"].get_left()[0] - 0.12, y0, y1, "R/S", ACC)
        self.at(self.cues[7])
        self.play(Create(m_sr), run_time=0.6)
        self.at(self.cues[8])
        self.play(Create(m_rs), run_time=0.6)
        self.end(pad=0.05)

        self.beat("s8")
        m_cg = marker(m_sr[0].get_x(), y0, y1, "S/R-CG", ACC)
        self.play(FadeOut(lg), Transform(m_sr, m_cg), run_time=0.6)
        cg_t = T("kanal grubu noktası:\nbütün kanallar burada", 16, ACC, BOLD).next_to(m_sr[1], RIGHT, buff=0.1)
        self.at(self.cues[3])
        self.play(FadeIn(cg_t), run_time=0.5)
        tab = pill("§11 PMD tabloları → S/R-CG'ye göre", GOLD, 18).move_to([0.6, 2.85, 0])
        self.at(self.cues[4])
        self.play(FadeIn(tab, shift=DOWN * 0.1), run_time=0.6)
        opl = DoubleArrow([m_sr[0].get_x(), -2.35, 0], [m_rs[0].get_x(), -2.35, 0], buff=0, color=CH[1], stroke_width=3, tip_length=0.18)
        opl_t = T("yol kaybı sınıfları (§6.2): S/R-CG ↔ R/S", 16, CH[1], BOLD).next_to(opl, UP, buff=0.05)
        self.at(self.cues[5])
        self.play(Create(opl), FadeIn(opl_t), run_time=0.9)
        self.end(pad=0.05)

        self.beat("s9")
        m_cp = marker((d["tw"].get_right()[0] + d["wm"].get_left()[0]) / 2, y0, y1, "S/R-CP", GOLD)
        self.at(self.cues[1] - 0.2)
        self.play(Create(m_cp), run_time=0.7)
        cp_t = T("kanal çifti noktası:\ntek transceiver portu", 16, GOLD, BOLD).move_to([-5.3, 2.2, 0])
        self.at(self.cues[3])
        self.play(FadeOut(d["olt_lbl"]), FadeIn(cp_t), Indicate(d["tw"][0], color=GOLD, scale_factor=1.08), run_time=0.8)
        alt = pill("alternatif · bilgilendirici · Ek XI", GOLD, 17).move_to([4.5, 2.3, 0])
        self.at(self.cues[5])
        self.play(FadeIn(alt), self.set_src("G.989.2 §6, Ek XI"), run_time=0.6)
        self.end(pad=0.05)

        # s10 — why two points (quote)
        self.beat("s10")
        keep = Group(*[m for m in self.mobjects if m not in (self.hdr, self.badge, h, self.src)])
        self.play(keep.animate.set_opacity(0.18), run_time=0.5)
        q = self.quote("G.989.2 §6", "“…applicable in the situations when the primary reference point, S/R-CG, is not practical or not accessible\nfor performing measurements or it is desirable to provide a simple sensitivity specification to an OLT transceiver vendor.”",
                       "CG erişilemiyorsa ya da transceiver üreticisine WM'den bağımsız bir şartname gerekiyorsa", width=12.4).move_to(UP * 0.2)
        bd = RoundedRectangle(corner_radius=0.2, width=13.4, height=3.6, stroke_width=0, fill_color=BG, fill_opacity=0.93).move_to(DOWN * 0.1)
        self.play(FadeIn(bd), FadeIn(q, shift=UP * 0.15), run_time=0.9)
        c2 = T("CP değerleri birincil yöntemle tutarlıdır · WM kaybı için sektörün en iyi uygulamalarına dayanır", 19, ACC, BOLD).next_to(q, DOWN, buff=0.4)
        if c2.width > 12.4:
            c2.scale_to_fit_width(12.4)
        self.at(self.cues[4])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.end(pad=0.05)

        # s11 — two meters, two readings
        self.beat("s11")
        self.play(FadeOut(q), FadeOut(c2), FadeOut(bd), keep.animate.set_opacity(1), run_time=0.6)
        self.set_badge("lab")
        def meter(val, sub, color):
            b = RoundedRectangle(corner_radius=0.12, width=2.4, height=0.95, stroke_color=color, stroke_width=2.5, fill_color="#0D1426", fill_opacity=1)
            return VGroup(b, VGroup(T(val, 24, color, BOLD), T(sub, 13, MUTED)).arrange(DOWN, buff=0.05).move_to(b))
        pm_cp = meter("+7,5 dBm", "CP'de ölçüm (örnek)", GOLD).move_to([m_cp[0].get_x() - 0.6, 1.92, 0])
        pm_cg = meter("+4,0 dBm", "CG'de ölçüm (örnek)", ACC).move_to([m_sr[0].get_x() + 0.5, 1.92, 0])
        self.play(*[FadeOut(m) for m in (opl, opl_t, cp_t, cg_t, tab, alt, d["leg"], d["leg_line"])], run_time=0.4)
        self.at(self.cues[1])
        self.play(FadeIn(pm_cp, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(pm_cg, shift=DOWN * 0.2), run_time=0.6)
        diff = pill("fark = WM kaybı (örnek: 3,5 dB)", WHITE, 18).move_to([2.6, 1.92, 0])
        self.at(self.cues[2])
        self.play(FadeIn(diff, shift=LEFT * 0.2), run_time=0.6)
        both = T("iki sayı da doğrudur", 20, GOOD, BOLD).next_to(diff, DOWN, buff=0.15)
        self.at(self.cues[4])
        self.play(FadeIn(both), run_time=0.5)
        self.end(pad=0.15)
        self.clear()
        self.save_timeline("ep01_p4C")


class P4D(Act):
    HDR, MANIFEST, PREV_BADGE = HDR4, MAN4, "lab"

    def construct(self):
        d = arch()
        h = self.heading("Aynı ODN, çok kanal, çok OLT")
        self.beat("s12")
        self.set_badge("std")
        self.play(FadeIn(h), FadeIn(d["all"]), run_time=0.8)
        cnt = VGroup(pill("TWDM: 4 … 8 kanal", ACC, 18), pill("PtP WDM: ≥ 4 kanal", PINK, 18)).arrange(RIGHT, buff=0.3).move_to([3.4, 2.2, 0])
        self.at(self.cues[1])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cnt], lag_ratio=0.3), self.set_src("G.989.2 §6"), run_time=0.9)
        olt2 = box(1.5, 0.6, "OLT #2", ACC, 16).move_to([-1.2, -1.75, 0])
        l2 = Line(d["ce"].get_bottom(), olt2.get_top(), color=ACC, stroke_width=3)
        why = T("kademeli büyüme · spektral esneklik", 16, ACC, BOLD).next_to(olt2, DOWN, buff=0.2)
        self.at(self.cues[3])
        self.play(FadeOut(d["odn"]), FadeOut(d["leg"]), FadeOut(d["leg_line"]), run_time=0.4)
        self.play(FadeIn(olt2, shift=UP * 0.2), Create(l2), FadeIn(why), run_time=1.0)
        self.end(pad=0.05)

        # s13 — OPL reminder + low-loss ODN attenuator
        self.beat("s13")
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.hdr, self.badge, self.src)], run_time=0.5)
        h = self.show_heading("Yol kaybı sınıfları: hatırlatma")
        sc = 0.33
        x0 = -5.8
        axis = NumberLine(x_range=[0, 36, 5], length=36 * sc, include_numbers=False, color=MUTED).move_to([x0 + 18 * sc, -0.6, 0])
        nums = VGroup(*[T(str(v), 16, MUTED).next_to(axis.n2p(v), DOWN, buff=0.08) for v in range(0, 36, 5)], T("dB", 16, MUTED).next_to(axis, RIGHT, buff=0.15))
        cls = VGroup()
        for i, (nm, lo, c) in enumerate([("N1", 14, CH[0]), ("N2", 16, CH[1]), ("E1", 18, CH[2]), ("E2", 20, CH[3])]):
            r = Rectangle(width=15 * sc, height=0.34, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([axis.n2p(lo + 7.5)[0], -0.1 + 0.45 * i, 0])
            cls.add(VGroup(r, T(f"{nm}  {lo}–{lo + 15} dB", 16, BG, BOLD).move_to(r)))
        cl_t = VGroup()
        dif = T("her sınıf 15 dB diferansiyel kaybı kapsar (Tablo 6-1)", 20, ACC, BOLD).next_to(cls, UP, buff=0.3)
        self.at(self.cues[1] - 0.2)
        self.play(FadeIn(axis), FadeIn(nums), LaggedStart(*[GrowFromEdge(c, LEFT) for c in cls], lag_ratio=0.15), FadeIn(cl_t), run_time=1.2)
        self.at(self.cues[2])
        self.play(FadeIn(dif), self.set_src("G.989.2 §6.2, Tablo 6-1"), run_time=0.5)
        olt_s = box(1.2, 0.6, "OLT", "#3B4A75", 16).move_to([-4.8, -2.4, 0])
        sp_s = splitter(0.25).move_to([0.3, -2.4, 0])
        l_s = Line(olt_s.get_right(), sp_s.get_left(), color=FEED, stroke_width=3)
        att = VGroup(Rectangle(width=0.7, height=0.4, stroke_color=WARN, stroke_width=2.5, fill_color=BG, fill_opacity=1), T("ATT", 13, WARN, BOLD))
        att[1].move_to(att[0]); att.move_to(l_s.get_center())
        onu_s = box(1.2, 0.5, "ONU", "#94A3B8", 14).move_to([2.4, -2.4, 0])
        l_o = Line(sp_s.get_right(), onu_s.get_left(), color="#94A3B8", stroke_width=2)
        at_t = T("örnek: kısa ağ + 1:8 ayırıcı → kayıp ≈ 12 dB < 14 dB (N1 alt sınırı) → optik zayıflatıcı", 16, WARN, BOLD).next_to(VGroup(olt_s, onu_s), DOWN, buff=0.25)
        self.at(self.cues[3] - 0.3)
        self.play(FadeIn(VGroup(olt_s, sp_s, l_s, onu_s, l_o)), run_time=0.6)
        self.at(self.cues[4])
        self.play(FadeIn(att, scale=1.3), FadeIn(at_t), run_time=0.8)
        self.end(pad=0.1)

        self.engineer_note("s14", [("1", "CG mi, CP mi?", "Datasheet'teki hassasiyet ve başlatma gücü\nhangi referans noktasına göre verilmiş?", 1),
                                   ("2", "WM kaybı nerede?", "Bütçede bir kez ve doğru yerde sayılmalı.\nEntegrasyondaki sürprizlerin çoğu buradan çıkar.", 3)])
        self.beat("s15")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bu kutular hangi hızlarda konuşuyor,\nve G.989.2'yi nasıl okuyacağız?")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep01_p4D")
