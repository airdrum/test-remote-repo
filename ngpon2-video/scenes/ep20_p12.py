"""S2·B10 · Perde 1 (B tipi koruma, TC derinliğinde — G.989.3 §18.1–§18.3, Tablo 18-1…18-4, Şekil 18-1…18-3; PMD: S1·B10, S1·B2)
and Perde 2 (ONU tarafında koruma ve ICTP — §11.3.3.15, Tablo 12-1…12-5, Ek J.2.2, TPST, Tablo 14-1, Ek V, Ek VI; PMD: S1·B7)."""
from ep20_common import *


class Topo:
    """Dual-parented 1:1 Type B (Fig. 18-1, simplified): two chassis × 3 CTs (λ1 peers on top) → WM → feeder → 2:N splitter → ONUs."""

    def __init__(self, cx=-5.55, wx=-3.35, sx=-0.1, ox=2.2):
        self.ct1, self.ct2 = VGroup(), VGroup()
        for i in range(3):
            self.ct1.add(ctu(f"CT λ{i + 1}", CH[i], False, 1.45, 0.36, 15).move_to([cx, 1.7 - 0.45 * i, 0]))
            self.ct2.add(ctu(f"CT λ{i + 1}′", CH[i], False, 1.45, 0.36, 15).move_to([cx, -0.8 - 0.45 * i, 0]))
        self.ch = VGroup(*[RoundedRectangle(corner_radius=0.12, width=1.8, height=1.55, stroke_color=MUTED, stroke_width=2, fill_opacity=0).move_to([cx, y, 0])
                           for y in (1.25, -1.25)])
        self.chl = VGroup(T("OLT 1 · şasi 1", 15, MUTED, BOLD).next_to(self.ch[0], UP, buff=0.07),
                          T("OLT 2 · şasi 2", 15, MUTED, BOLD).next_to(self.ch[1], DOWN, buff=0.07))
        self.wm = VGroup(sbox("WM", None, FEED, 0.62, 1.3, 17).move_to([wx, 1.25, 0]), sbox("WM", None, FEED, 0.62, 1.3, 17).move_to([wx, -1.25, 0]))
        self.att1 = VGroup(*[Line(c.get_right(), [self.wm[0].get_left()[0], 1.25 + (c.get_y() - 1.25) * 0.7, 0], color=CH[i], stroke_width=2.5) for i, c in enumerate(self.ct1)])
        self.att2 = VGroup(*[Line(c.get_right(), [self.wm[1].get_left()[0], -1.25 + (c.get_y() + 1.25) * 0.7, 0], color=CH[i], stroke_width=2.5) for i, c in enumerate(self.ct2)])
        self.sp = splitter(0.3).move_to([sx, 0, 0])
        sl = self.sp.get_left()
        self.fd = VGroup(VMobject(stroke_color=FEED, stroke_width=3.5).set_points_as_corners([self.wm[0].get_right(), [sx - 1.3, 1.25, 0], sl + UP * 0.1]),
                         VMobject(stroke_color=FEED, stroke_width=3.5).set_points_as_corners([self.wm[1].get_right(), [sx - 1.3, -1.25, 0], sl + DOWN * 0.1]))
        self.onus = VGroup(*[onu_box("ONU", ONUC, 1.05, 0.44, 16).move_to([ox, y, 0]) for y in (1.1, 0.0, -1.1)])
        sr = self.sp.get_right()
        self.dist = VGroup(*[VMobject(stroke_color=FEED, stroke_width=2.5).set_points_as_corners([sr, [sx + 1.1, o.get_y(), 0], o.get_left()]) for o in self.onus])
        self.lab = VGroup(T("bağlantı fiberleri", 14, MUTED, BOLD).move_to([(cx + wx) / 2 + 0.1, 0, 0]),
                          T("besleyici", 14, MUTED, BOLD).move_to([sx - 1.95, 1.45, 0]), T("besleyici", 14, MUTED, BOLD).move_to([sx - 1.95, -1.45, 0]),
                          T("ayırıcı 2:N", 14, MUTED, BOLD).next_to(self.sp, DOWN, buff=0.12),
                          T("dağıtım", 14, MUTED, BOLD).move_to([sx + 1.1, -1.5, 0]))

    def all(self):
        return VGroup(self.ch, self.chl, self.ct1, self.ct2, self.att1, self.att2, self.wm, self.fd, self.sp, self.dist, self.onus, self.lab)


def tbmini(k, w=1.95, h=0.8, dashed=False, size=15):
    """Compact Type B state box for chains: '(k)' + Turkish name on two lines, Tx lamp in the upper right corner."""
    a = TB[k][0]
    c = tbcol(k)
    on = tx_on(k)
    if dashed:
        r = VGroup(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_width=0, fill_color=PANEL, fill_opacity=1),
                   DashedVMobject(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=c, stroke_width=2.4), num_dashes=36))
    else:
        r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=c, stroke_width=2.4, fill_color=c if on else PANEL, fill_opacity=0.18 if on else 1)
    t = VGroup(T(f"({k})", size + 1, TXT, BOLD), T(a, size, c, BOLD)).arrange(DOWN, buff=0.04)
    fit(t, w - 0.2)
    lm = txlamp(on, 0.075).move_to([w / 2 - 0.18, h / 2 - 0.17, 0])
    return VGroup(r, t, lm)


def chain(ks, y, x0=-6.3, w=1.95, gap=1.42, dashed=(), labels=(), colors=(), size=14):
    """Linear chain of tbmini boxes with labelled arrows between them. Returns (boxes, arrows)."""
    bx = VGroup()
    for i, k in enumerate(ks):
        bx.add(tbmini(k, w, 0.8, k in dashed).move_to([x0 + w / 2 + i * (w + gap), y, 0]))
    ar = VGroup()
    for i in range(len(ks) - 1):
        a = arrow(bx[i][0].get_right() if not isinstance(bx[i][0], VGroup) else bx[i][0][0].get_right(),
                  bx[i + 1][0].get_left() if not isinstance(bx[i + 1][0], VGroup) else bx[i + 1][0][0].get_left(),
                  colors[i] if colors else MUTED, 2.4, 0.13)
        g = VGroup(a)
        if labels and labels[i]:
            g.add(tf(labels[i], size, colors[i] if colors else MUTED, BOLD, w=gap - 0.1).next_to(a, UP, buff=0.06))
        ar.add(g)
    return bx, ar


# ================================ PERDE 1 ======================================
class E20P1A(Act20):
    HDR, MANIFEST, FIRST = H20[1], M20("p1"), True

    def construct(self):
        # b1 — season 1 saw protection from the optics (no ONU retuning, G.989.2 defines no protection, Type B *link* = amplified OLT receiver);
        #      now the TC side; clause 18 unchanged since 2021
        self.beat("b1")
        tc = self.title_card("PERDE 1", "B tipi koruma, TC derinliğinde")
        h = self.heading("Optikten TC'ye — §18")
        self.at(self.cue("Birinci sezonun onuncu", 2.0))
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        lf = frame_box("Sezon 1 · optik görünüm", S1C, 6.1, 3.3, 18).move_to([-3.3, 0.35, 0])
        ll = VGroup(chk("ONU yeniden ayarlanmaz", True, 17), chk("G.989.2 korumayı tanımlamaz", False, 17),
                    VGroup(T("B tipi bağlantı =", 17, TXT, BOLD), T("yükselteçli OLT alıcısı", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.12))
        ll.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(ll, 5.5).move_to(lf[0]).shift(DOWN * 0.2)
        ch10 = s1chip(10, 16).next_to(lf, DOWN, buff=0.18)
        rf = frame_box("Sezon 2 · TC görünümü", ACC, 6.1, 3.3, 18).move_to([3.3, 0.35, 0])
        rl = VGroup(VGroup(tag("§18.1", GOLD, 15), T("yapılandırma · roller", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                    VGroup(tag("§18.2", GOLD, 15), T("10 durum · 6 zamanlayıcı · olaylar", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                    VGroup(tag("§18.3", GOLD, 15), T("ICTP'siz sadeleşmiş makine", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15))
        rl.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(rl, 5.5).move_to(rf[0]).shift(DOWN * 0.2)
        ed = VGroup(ed_chips(15, GOOD), T("§18: 2021'den beri değişmedi", 16, GOOD, BOLD)).arrange(DOWN, buff=0.1).next_to(rf, DOWN, buff=0.15)
        self.play(FadeIn(lf), self.set_src("S1·B10 · G.989.3 §18 (2021 · Amd.1 · Amd.2)"), run_time=0.4)
        self.play(FadeIn(ch10, shift=UP * 0.05), run_time=0.3)
        for k, (key, d) in enumerate((("ONU yeniden ayarlanmaz", 6.9), ("G.989.2 korumayı", 8.8), ("B tipi bağlantı yalnızca", 11.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(ll[k], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Bu kez TC tarafındayız", 16.8))
        self.play(FadeIn(rf), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.05) for r in rl], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("On sekizinci madde", 18.7))
        self.play(FadeIn(ed, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # b2 — two OLT CTs per channel pair (Type B peers), separate or same chassis; protected: attachment fibre, feeder, WM, CT, chassis;
        #      feeder/WM/chassis fault → all pairs of the group switch; CT/attachment fault → only that pair; our reading: splitter + distribution not protected
        self.beat("b2")
        h = self.reset("Yapılandırma — Şekil 18-1", "std", 0.5)
        tp = Topo()
        px = 4.95

        def pt(m, y):
            fit(m, 3.15)
            return m.move_to([px, y, 0])
        peer = DashedVMobject(VMobject(stroke_color=GOLD, stroke_width=2.4).set_points_as_corners(
            [tp.ct1[0].get_left(), [-6.62, tp.ct1[0].get_y(), 0], [-6.62, tp.ct2[0].get_y(), 0], tp.ct2[0].get_left()]), num_dashes=30)
        r_peer = pt(VGroup(T("B tipi eşler:", 16, GOLD, BOLD), T("CT λ1 ↔ CT λ1′", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12), 1.95)
        r_par = VGroup(pt(tag("çift ebeveyn · ayrı şasiler", MUTED, 15), 1.45), pt(tag("tek ebeveyn · aynı şasi", MUTED, 15), 1.0))
        r_pt = pt(T("korunur:", 16, PROTC, BOLD), 0.4)
        pc = VGroup(*[tag(s, PROTC, 15) for s in ("bağlantı fiberi", "besleyici", "WM", "CT", "şasi")])
        VGroup(VGroup(*pc[:2]).arrange(RIGHT, buff=0.1), VGroup(*pc[2:]).arrange(RIGHT, buff=0.1)).arrange(DOWN, buff=0.1)
        pt(pc, -0.2)
        r_all = pt(VGroup(T("✂ besleyici · WM · şasi", 15, WARN, BOLD), T("→ gruptaki bütün çiftler", 15, TXT, BOLD)).arrange(DOWN, buff=0.04, aligned_edge=LEFT), -1.15)
        r_one = pt(VGroup(T("✂ CT · bağlantı fiberi", 15, WARN, BOLD), T("→ yalnızca o çift", 15, TXT, BOLD)).arrange(DOWN, buff=0.04, aligned_edge=LEFT), -1.95)
        r_unp = pt(VGroup(ytag("bizim yorumumuz"), T("ayırıcı · dağıtım: korunmaz", 15, TXT, BOLD)).arrange(DOWN, buff=0.06), -2.75)
        dim = [*tp.ct1[1:], *tp.ct2[1:], *tp.att1[1:], *tp.att2[1:]]   # real submobjects only: a new wrapper group would split `topo`
        topo = tp.all()
        self.play(FadeIn(topo), self.set_src("G.989.3 §18.1 · Şekil 18-1 (sadeleştirilmiş)"), run_time=0.8)
        self.play(*[m.animate.set_opacity(0.35) for m in dim], run_time=0.4)
        self.at(self.cue("birbirinin B tipi eşi", 4.7))
        self.play(Create(peer), FadeIn(r_peer, shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("ayrı ya da aynı şasilerde", 6.5))
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.05) for r in r_par], lag_ratio=0.3), Indicate(tp.ch, color=GOLD, scale_factor=1.02), run_time=0.6)
        self.at(self.cue("Korunanlar:", 8.7))
        self.play(FadeIn(r_pt), *[m.animate.set_opacity(1) for m in dim], run_time=0.35)
        self.at(self.cue("bağlantı fiberi,", 9.7))
        self.play(*[l.animate.set_stroke(PROTC, 3.5) for l in [*tp.att1, *tp.att2]], FadeIn(pc[0]), run_time=0.3)
        self.at(self.cue("besleyici,", 11.0))
        self.play(*[f.animate.set_stroke(PROTC, 4.5) for f in tp.fd], FadeIn(pc[1]), run_time=0.3)
        self.at(self.cue("WM,", 11.9))
        self.play(*[w[0].animate.set_stroke(PROTC) for w in tp.wm], FadeIn(pc[2]), run_time=0.25)
        self.at(self.cue("sonlandırıcı ve şasi", 12.1))
        self.play(*[c[0].animate.set_stroke(PROTC) for c in [*tp.ct1, *tp.ct2]], tp.ch.animate.set_stroke(PROTC), FadeIn(pc[3:]), run_time=0.4)
        cut = cutmark([-1.95, 1.25, 0])
        allr = VGroup(SurroundingRectangle(tp.ct1, color=GOLD, buff=0.06, stroke_width=2.5), SurroundingRectangle(tp.ct2, color=GOLD, buff=0.06, stroke_width=2.5))
        self.at(self.cue("WM ya da şasi arızasında", 14.7))
        self.play(FadeIn(cut, scale=1.4), run_time=0.3)
        self.play(Create(allr), FadeIn(r_all, shift=LEFT * 0.05), run_time=0.5)
        cut2 = cutmark(tp.att1[1].point_from_proportion(0.5), CUTC, 0.13)
        oner = VGroup(SurroundingRectangle(tp.ct1[1], color=GOLD, buff=0.05, stroke_width=2.5), SurroundingRectangle(tp.ct2[1], color=GOLD, buff=0.05, stroke_width=2.5))
        self.at(self.cue("sonlandırıcı ya da bağlantı fiberi", 19.6))
        self.play(FadeOut(cut), FadeOut(allr), FadeIn(cut2, scale=1.4), run_time=0.4)
        self.play(Create(oner), FadeIn(r_one, shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("Bizim yorumumuz", 25.9))
        self.play(FadeOut(cut2), FadeOut(oner), tp.sp.animate.set_stroke(UNPC).set_fill(UNPC, 0.4), *[d.animate.set_stroke(UNPC) for d in tp.dist], run_time=0.5)
        self.play(FadeIn(r_unp, shift=LEFT * 0.05), Indicate(tp.sp, color=WARN, scale_factor=1.08), Indicate(tp.lab[3], color=WARN), Indicate(tp.lab[4], color=WARN), run_time=0.6)
        self.end(pad=0.05)

        # b3 — roles: exactly one Active (DS, serves ONUs), the other Standby (Tx off, listens upstream); default Primary/Secondary resolved in the ICTP
        #      handshake; persistent when revertive; the machine also progresses without ICTP
        self.beat("b3")
        h = self.reset_keep("Roller — etkin ve bekleme", "std", keep=[topo], rt=0.5,
                            extra=[*[l.animate.set_stroke(CH[i % 3], 2.5) for i, l in enumerate([*tp.att1, *tp.att2])],
                                   *[f.animate.set_stroke(FEED, 3.5) for f in tp.fd], *[w[0].animate.set_stroke(FEED) for w in tp.wm],
                                   *[c[0].animate.set_stroke(CH[i % 3]) for i, c in enumerate([*tp.ct1, *tp.ct2])], tp.ch.animate.set_stroke(MUTED),
                                   tp.sp.animate.set_stroke(FEED).set_fill(PANEL, 1), *[d.animate.set_stroke(FEED) for d in tp.dist],
                                   *[m.animate.set_opacity(0.3) for m in dim]])
        ra = pt(VGroup(pill("CT λ1 · etkin (Active)", TXON, 16), T("↓ yayın · ONU'lara hizmet", 15, TXT, BOLD)).arrange(DOWN, buff=0.1), 1.65)
        rs = pt(VGroup(pill("CT λ1′ · bekleme (Standby)", STBC, 16), T("verici kapalı · ↑ dinler", 15, TXT, BOLD)).arrange(DOWN, buff=0.1), 0.45)
        rd = pt(VGroup(T("varsayılan rol:", 15, MUTED, BOLD), T("birincil · ikincil", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12), -0.55)
        rv = pt(VGroup(T("geri dönüşlü → roller kalıcı", 15, GOOD, BOLD), T("geri dönüşsüz → bırakılır", 15, MUTED, BOLD)).arrange(DOWN, buff=0.06, aligned_edge=LEFT), -1.45)
        rn = pt(VGroup(tag("ICTP'siz de ilerler · §18.2", ICTPC, 15)), -2.4)
        dsa = VGroup(arrow([-3.0, 1.25, 0], [-1.65, 1.25, 0], TXON, 4, 0.16), *[arrow([0.95, o.get_y(), 0], [1.6, o.get_y(), 0], TXON, 3, 0.13) for o in tp.onus])
        usa = VGroup(arrow([-1.65, -1.25, 0], [-3.0, -1.25, 0], ONUC, 3, 0.14), arrow([-3.7, -0.92, 0], [-4.75, -0.8, 0], ONUC, 2.5, 0.12))
        ictp = VMobject(stroke_color=ICTPC, stroke_width=4).set_points_as_corners([[-6.45, 1.25, 0], [-6.65, 1.25, 0], [-6.65, -1.25, 0], [-6.45, -1.25, 0]])
        il = T("ICTP", 15, ICTPC, BOLD).move_to([-6.05, 0.0, 0])
        self.at(self.cue("tam olarak biri etkindir", 0.6))
        self.play(set_lamp(tp.ct1[0], True), FadeIn(ra[0], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("aşağı yönde yayın", 5.5))
        self.play(LaggedStart(*[GrowArrow(a) for a in dsa], lag_ratio=0.15), FadeIn(ra[1]), run_time=0.7)
        self.at(self.cue("ONU'lara hizmet", 7.5))
        self.play(Indicate(tp.onus, color=TXON, scale_factor=1.05), run_time=0.5)
        self.at(self.cue("Öteki beklemededir", 9.4))
        self.play(FadeIn(rs[0], shift=LEFT * 0.05), Indicate(tp.ct2[0], color=STBC, scale_factor=1.06), run_time=0.5)
        self.at(self.cue("yukarı yönü dinler", 12.3))
        self.play(*[GrowArrow(a) for a in usa], FadeIn(rs[1]), run_time=0.5)
        self.at(self.cue("Varsayılan roller", 14.0))
        self.play(FadeIn(rd, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("ICTP el sıkışmasında", 17.4))
        self.play(Create(ictp), FadeIn(il), run_time=0.5)
        self.at(self.cue("geri dönüşlü", 19.9))
        self.play(FadeIn(rv, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ICTP'siz de", 23.1))
        ic = cutmark([-6.65, 0.55, 0], CUTC, 0.13)
        self.play(FadeIn(ic, scale=1.4), FadeIn(rn, shift=LEFT * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # b4 — ten states (Table 18-1): four standby (Tx off), three active (Tx on, shaded in Fig. 18-2), three exceptional (Helpme: Tx off, peer take over;
        #      COMM-FAIL: expected upstream missing; EQPT-FAIL: peer gets Unprotected() and sets Tpfail to infinity)
        self.beat("b4")
        h = self.reset("On durum — Tablo 18-1", "std", 0.5)
        pos = {1: (-4.95, 1.45), 2: (-1.65, 1.45), 3: (1.65, 1.45), 4: (4.95, 1.45), 5: (-3.3, -0.05), 6: (0, -0.05), 7: (3.3, -0.05),
               8: (-3.3, -1.55), 9: (0, -1.55), 10: (3.3, -1.55)}
        bx = {k: tbbox(k, 3.05, 0.84).move_to([x, y, 0]) for k, (x, y) in pos.items()}
        g1 = VGroup(tag("bekleme · verici kapalı", STBC, 15), txlamp(False)).arrange(RIGHT, buff=0.12).move_to([-6.45, 2.08, 0], aligned_edge=LEFT)
        g2 = VGroup(tag("etkin · verici açık", ACTC, 15), txlamp(True)).arrange(RIGHT, buff=0.12).move_to([-4.8, 0.58, 0], aligned_edge=LEFT)
        g3 = tag("ayrıksı durumlar", EXCC, 15).move_to([-4.8, -0.92, 0], aligned_edge=LEFT)
        d8 = T("Tx kapat · eşine: devral", 14, EXCC, BOLD).next_to(bx[8], DOWN, buff=0.1)
        d9 = T("beklenen ↑ gelmez", 14, EXCC, BOLD).next_to(bx[9], DOWN, buff=0.1)
        d10 = VGroup(T("eşi: Unprotected()", 14, EXCC, BOLD), T("→ eşinin Tpfail = ∞", 14, EXCC, BOLD)).arrange(DOWN, buff=0.04).next_to(bx[10], DOWN, buff=0.1)
        fn = T("(9) · (10): Tx metinde yok · Şekil 18-2'de gölgesiz → kapalı", 14, MUTED, BOLD).move_to([3.2, -3.1, 0])
        self.play(self.set_src("G.989.3 §18.2.1 · Tablo 18-1 · Şekil 18-2"), run_time=0.3)
        self.at(self.cue("Vericisi kapalı dört", 0.8))
        self.play(FadeIn(g1, shift=RIGHT * 0.05), run_time=0.35)
        for k, (key, d) in zip((1, 2, 3, 4), (("başlatma,", 3.8), ("koruma öncesi,", 4.6), ("koruyan,", 5.8), ("koruyan tarafta sinyal", 6.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(bx[k], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Vericisi açık üç", 9.2))
        self.play(FadeIn(g2, shift=RIGHT * 0.05), run_time=0.35)
        for k, (key, d) in zip((5, 6, 7), (("çalışma öncesi,", 11.7), ("çalışan,", 13.0), ("çalışan tarafta sinyal", 13.7))):
            self.at(self.cue(key, d))
            self.play(FadeIn(bx[k], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("üç ayrıksı durum", 16.4))
        self.play(FadeIn(g3, shift=RIGHT * 0.05), run_time=0.35)
        for k, d_, key, dd in ((8, d8, "yardım isteme", 18.1), (9, d9, "iletişim arızası", 22.2), (10, d10, "donanım arızası", 26.0)):
            self.at(self.cue(key, dd))
            self.play(FadeIn(bx[k], shift=UP * 0.05), run_time=0.3)
            self.play(FadeIn(d_, shift=UP * 0.05), run_time=0.3)
        self.play(FadeIn(fn), run_time=0.3)
        self.end(pad=0.05)

        # b5 — events (Table 18-3): SLOS = 0.5 ms (4 frames) of upstream silence in non-transmitting states; QLOS = 4 frames + LOBi for all relevant ONUs in
        #      transmitting states, subject to exclusions (ONU population, power management, dying gasp); LOS cleared = one burst, BWmap-consistent when Active
        self.beat("b5")
        h = self.reset("Olaylar — Tablo 18-3", "std", 0.5)
        x0, fw = -2.9, 0.85

        def row(y, name, sub, color):
            lb = VGroup(T(name, 19, color, BOLD), T(sub, 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([-6.4, y, 0], aligned_edge=LEFT)
            return lb

        def frames(y, n=4):
            g = VGroup(*[DashedVMobject(Rectangle(width=fw - 0.06, height=0.42, stroke_color=MUTED, stroke_width=1.5), num_dashes=16)
                         .move_to([x0 + fw * (k + 0.5), y, 0]) for k in range(n)])
            lb = VGroup(*[T(f"{k + 1}", 14, MUTED, BOLD).next_to(g[k], DOWN, buff=0.04) for k in range(n)])
            return VGroup(g, lb)
        y1, y2, y3 = 1.5, -0.2, -1.9
        l1 = row(y1, "SLOS", "basit sinyal kaybı", STBC)
        f1 = frames(y1)
        v1 = VGroup(T("0,5 ms = 4 × 125 µs", 18, STBC, BOLD), T("↑ sessizlik", 15, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([0.75, y1, 0], aligned_edge=LEFT)
        s1 = VGroup(T("yayın yapmayan durumlarda:", 14, MUTED, BOLD), *[tile(f"({k})", tbcol(k), 0.44, 0.32, 14, 0.2) for k in (1, 2, 3, 4, 8, 9, 10)]).arrange(RIGHT, buff=0.06)
        s1.move_to([3.6, y1 - 0.65, 0])
        l2 = row(y2, "QLOS", "nitelikli sinyal kaybı", ACTC)
        f2 = frames(y2)
        lobs = VGroup(*[VGroup(tile("ONU", ONUC, 0.62, 0.32, 14, 0.15), T("LOBi", 14, DEFC, BOLD)).arrange(DOWN, buff=0.03) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        v2 = VGroup(T("4 çerçeve sessizlik +", 17, ACTC, BOLD), VGroup(lobs, T("bütün ilgili ONU'lar", 14, TXT, BOLD)).arrange(DOWN, buff=0.05)).arrange(RIGHT, buff=0.2)
        v2.move_to([0.75, y2 + 0.08, 0], aligned_edge=LEFT)
        s2 = VGroup(T("yayın yapan durumlarda:", 14, MUTED, BOLD), *[tile(f"({k})", tbcol(k), 0.44, 0.32, 14, 0.3) for k in (5, 6, 7)]).arrange(RIGHT, buff=0.06)
        ex = VGroup(T("dışlamalar:", 14, WARN, BOLD), *[tag(s, WARN, 14) for s in ("ONU sayısı", "güç yönetimi", "son nefes")]).arrange(RIGHT, buff=0.08)
        VGroup(s2, ex).arrange(RIGHT, buff=0.3).move_to([1.2, y2 - 0.68, 0])
        l3 = row(y3, "LOS temizlendi", "", GOOD)
        bu = Rectangle(width=fw - 0.06, height=0.42, stroke_color=GOOD, stroke_width=1.8, fill_color=GOOD, fill_opacity=0.45).move_to([x0 + fw * 0.5, y3, 0])
        bul = T("1 burst", 15, TXT, BOLD).move_to(bu)
        v3 = VGroup(T("tek bir ↑ burst", 17, GOOD, BOLD), T("etkin durumlarda: BWmap ile tutarlı", 16, TXT, BOLD)).arrange(RIGHT, buff=0.25)
        fit(v3, 8.4).move_to([x0 + fw + 0.2, y3, 0], aligned_edge=LEFT)
        self.play(self.set_src("G.989.3 Tablo 18-3 · Tablo 14-2 (LOBi)"), run_time=0.3)
        self.at(self.cue("Basit sinyal kaybı", 0.7))
        self.play(FadeIn(l1, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("yayın yapmayan durumlarda", 2.3))
        self.play(LaggedStart(*[Create(f) for f in f1[0]], lag_ratio=0.15), FadeIn(f1[1]), FadeIn(s1, shift=UP * 0.05), run_time=0.7)
        self.at(self.cue("dört çerçevelik", 6.1))
        self.play(FadeIn(v1, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Nitelikli sinyal kaybı", 9.6))
        self.play(FadeIn(l2, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("yayın yapan durumlarda dört", 11.5))
        self.play(LaggedStart(*[Create(f) for f in f2[0]], lag_ratio=0.15), FadeIn(f2[1]), FadeIn(s2, shift=UP * 0.05), run_time=0.6)
        self.play(FadeIn(v2, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("ONU sayısına", 19.2))
        self.play(FadeIn(ex[:2], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("güç yönetimine ve son", 20.3))
        self.play(FadeIn(ex[2:], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Temizlenme tek bir", 25.1))
        self.play(FadeIn(l3, shift=RIGHT * 0.05), FadeIn(bu), FadeIn(bul), FadeIn(v3[0], shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("haritayla tutarlı", 27.5))
        self.play(FadeIn(v3[1], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.1)
        self.save_timeline("ep20_p1A")


class E20P1B(Act20):
    HDR, MANIFEST, PREV_BADGE = H20[1], M20("p1"), "std"

    def construct(self):
        # b6 — six timers (Table 18-2); the only number: Tract ≈ 0.5 ms; the rest have no value but an order: Tpfail > Thold, Tpfail > Twfail
        #      (else the Protecting CT may talk before the Working one stops), Thold > Twfail (else holding is disabled); without ICTP Tsstart, Tpfail largest
        self.beat("b6")
        h = self.reset("Altı zamanlayıcı — Tablo 18-2", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 18-2 · §18.2.5 (Tablo 18-4'ün ardındaki metin)")])
        tms = [("Tsstart", "sessiz başlangıç", None), ("Tpfail", "koruma arızası", None), ("Tract", "onay", "≈ 0,5 ms"),
               ("Thold", "tutma", None), ("Twfail", "çalışma arızası", None), ("Tictp", "ICTP", None)]
        cards = VGroup()
        for nm, tr_, v in tms:
            r = RoundedRectangle(corner_radius=0.1, width=2.02, height=1.05, stroke_color=TMRC, stroke_width=2, fill_color=PANEL, fill_opacity=1)
            g = VGroup(T(nm, 19, TMRC, BOLD), T(tr_, 14, MUTED, BOLD), T(v or "değer yok", 16, GOOD if v else WARN, BOLD)).arrange(DOWN, buff=0.05)
            fit(g, 1.85).move_to(r)
            cards.add(VGroup(r, g))
        cards.arrange(RIGHT, buff=0.12).move_to([0, 1.65, 0])
        one = VGroup(T("tek sayı:", 17, MUTED, BOLD), T("Tract için “makul başlangıç değeri” 0,5 ms", 17, GOOD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, 0.75, 0])
        bx0 = -6.2
        bars = VGroup()
        for k, (nm, w, c) in enumerate((("Tpfail", 4.6, STBC), ("Thold", 3.2, ACTC), ("Twfail", 2.1, ACTC))):
            y = -0.05 - 0.55 * k
            r = Rectangle(width=w, height=0.34, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.35).move_to([bx0 + w / 2, y, 0])
            bars.add(VGroup(r, T(nm, 15, TXT, BOLD).move_to(r)))
        ineq = VGroup(T("Tpfail > Thold > Twfail", 20, GOLD, BOLD), tag("ölçeksiz · sıra yeter", MUTED, 14)).arrange(RIGHT, buff=0.2).move_to([bx0, -1.75, 0], aligned_edge=LEFT)
        # overlap sketch (right): working Tx goes off after Thold & Twfail; protecting Tx goes on after Tpfail
        ox0, ox1 = 0.9, 6.5
        la = side_lbl("çalışan Tx", 0.05, ACTC, x=ox0, size=15)
        lb_ = side_lbl("koruyan Tx", -0.65, STBC, x=ox0, size=15)
        sx = ox0 + 1.5
        wa = txbar(sx, sx + 2.6, 0.05, 0.22)
        wb_ok = txbar(sx + 3.0, ox1, -0.65, 0.22, STBC)
        wb_bad = txbar(sx + 1.8, ox1, -0.65, 0.22, WARN)
        ovl = Rectangle(width=0.8, height=1.05, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.15).move_to([sx + 2.2, -0.3, 0])
        ovt = T("Tpfail ≤ Thold: iki verici birlikte ✗", 15, WARN, BOLD).move_to([(ox0 + ox1) / 2 + 0.2, -1.25, 0])
        okt = T("Tpfail > Thold, Twfail: boşluk ✓", 15, GOOD, BOLD).move_to([(ox0 + ox1) / 2 + 0.2, -1.25, 0])
        hd = VGroup(T("Thold > Twfail", 17, ACTC, BOLD), T("aksi: tutma özelliği kapanır", 16, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([bx0, -2.45, 0], aligned_edge=LEFT)
        ni = VGroup(T("ICTP yoksa:", 16, ICTPC, BOLD), T("Tsstart ve Tpfail en büyük kalır", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([bx0, -3.0, 0], aligned_edge=LEFT)
        self.at(self.cue("Altı zamanlayıcı", 0.0))
        for k, (key, d) in enumerate((("sessiz başlangıç,", 1.4), ("koruma arızası,", 2.9), ("onay,", 4.2), ("tutma,", 4.6), ("çalışma arızası ve", 5.1), ("ve ICTP", 5.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(cards[k][0]), FadeIn(cards[k][1][:2], shift=UP * 0.05), run_time=0.25)
        self.at(self.cue("Tek sayı", 7.2))
        self.play(FadeIn(one[0]), run_time=0.3)
        self.at(self.cue("yarım milisaniye", 11.0))
        self.play(FadeIn(cards[2][1][2], scale=1.3), FadeIn(one[1], shift=LEFT * 0.05), Indicate(cards[2][0], color=GOOD, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("Gerisinin değeri yok", 12.4))
        self.play(*[FadeIn(cards[k][1][2], scale=1.2) for k in (0, 1, 3, 4, 5)], run_time=0.45)
        self.at(self.cue("sıralaması var", 14.2))
        self.play(LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in bars], lag_ratio=0.2), *[FadeIn(b[1]) for b in bars], run_time=0.7)
        self.at(self.cue("Koruma arızası tutmadan", 15.5))
        self.play(FadeIn(ineq, shift=UP * 0.05), FadeIn(la), FadeIn(lb_), GrowFromEdge(wa, LEFT), run_time=0.5)
        self.at(self.cue("yoksa koruyan", 20.6))
        self.play(GrowFromEdge(wb_bad, LEFT), FadeIn(ovl), FadeIn(ovt, shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("Tutma çalışma arızasından", 24.3))
        self.play(FadeOut(wb_bad), FadeOut(ovl), FadeOut(ovt), GrowFromEdge(wb_ok, LEFT), FadeIn(okt), run_time=0.5)
        self.play(FadeIn(hd, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ICTP yoksa sessiz", 29.4))
        self.play(FadeIn(ni, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # b7 — Table 18-4, standby side: (1) LOS cleared → 2; Tsstart / Active() → 5; Standby*() → 3; (2) SLOS → 1, Standby*() / Tictp → 3; (3) ⇄ (4)
        #      SLOS / LOS cleared; (4) Tpfail / Active() → 5, Standby-Clear() → 9, Standby-LOS() restarts Tpfail
        self.beat("b7")
        h = self.reset("Tablo 18-4 — bekleme tarafı", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 18-4 (Amd.2 PDF s.211–212) · NOT 1–3")])
        tb = TbTable()
        lg = T("* öz geçiş   ·   koyu: imkânsız olay / protokol ihlali   ·   N1–N3: tablo notları", 14, MUTED, BOLD).move_to([2.6, -3.12, 0])
        self.play(FadeIn(tb.head), LaggedStart(*[FadeIn(l, shift=RIGHT * 0.05) for l in tb.labels], lag_ratio=0.04), FadeIn(tb.bg), run_time=1.0)
        self.play(FadeIn(tb.fixed), FadeIn(lg), *[tb.colhead[c].animate.set_opacity(0.35) for c in range(5, 11)], run_time=0.5)
        steps = [([("LOSc", 1)], "Başlatmada yukarı yön", 2.4), ([("Tss", 1), ("Act", 1)], "sessiz başlangıç dolar", 6.4),
                 ([("SbL", 1), ("SbC", 1)], "bekleme mesajı gelirse koruyana", 12.0), ([("SLOS", 2)], "Koruma öncesinde basit", 15.4),
                 ([("SbL", 2), ("SbC", 2), ("Tic", 2)], "bekleme mesajı ya da ICTP", 18.7), ([("SLOS", 3), ("LOSc", 4)], "Koruyan ile kaybı", 23.5),
                 ([("Tpf", 4), ("Act", 4)], "Kayıpta koruma arızası", 28.9), ([("SbC", 4)], "bekleme ve temiz mesajı", 33.9),
                 ([("SbL", 4)], "bekleme ve kayıp mesajı", 38.1)]
        for keys, sub, d in steps:
            self.at(self.cue(sub, d))
            self.cells_in(tb, keys, 0.4)
        self.end(pad=0.05)

        # b8 — active side: (5) BWmap-consistent burst → 6, Tract → 9; (6) ⇄ (7) QLOS / LOS cleared; (7) Thold & Twfail → 8; (6) EMS:Forced() → 8;
        #      (8) LOS cleared / Standby-LOS() / Tictp → 3, Standby-Clear() → 9; (9) one burst → 2; (10) only CTreset → 1 (+ EQPT row, CTreset row)
        self.beat("b8")
        h2 = self.heading("Tablo 18-4 — etkin taraf")
        self.play(FadeTransform(h, h2), *[tb.colhead[c].animate.set_opacity(1) for c in range(5, 11)],
                  *[tb.colhead[c].animate.set_opacity(0.35) for c in range(1, 5)], run_time=0.5)
        steps = [([("LOSc", 5)], "Çalışma öncesinde haritayla", 1.0), ([("Tra", 5)], "onay zamanlayıcısı iletişim", 5.6),
                 ([("QLOS", 6), ("LOSc", 7)], "Çalışan ile kaybı", 9.5), ([("Thw", 7)], "kayıpta tutma ve", 15.2),
                 ([("For", 6)], "yönetimin zorlama", 19.4), ([("LOSc", 8), ("SbL", 8), ("Tic", 8)], "Oradan temizlenme", 25.1),
                 ([("SbC", 8)], "bekleme ve temiz mesajı iletişim", 31.5), ([("LOSc", 9)], "Oradan bir burst", 35.1)]
        for keys, sub, d in steps:
            self.at(self.cue(sub, d))
            self.cells_in(tb, keys, 0.4)
        self.at(self.cue("donanım arızasından yalnızca", 38.5))
        self.play(*[tb.colhead[c].animate.set_opacity(1) for c in range(1, 5)], run_time=0.2)
        self.cells_in(tb, [("CTr", 10)], 0.35)
        self.play(*[FadeIn(tb.cell("EQ", c), shift=LEFT * 0.03) for c in range(1, 11)], *[FadeIn(tb.cell("CTr", c), shift=LEFT * 0.03) for c in range(1, 10)],
                  run_time=0.5)
        self.end(pad=0.05)

        # b9 — feeder cut, ICTP up: ONUs LODS after 3 frames → O6, TO6 stops; Working CT QLOS → LOS-W, keeps transmitting; Standby SLOS after 0.5 ms → LOS-P;
        #      Thold & Twfail → Helpme, Tx off, Active() to the peer → Pre-Working, Tx on; ONUs resync (≥ 2 frames) → O5, TO6 resumes; first
        #      BWmap-consistent burst → Working
        self.beat("b9")
        h = self.reset("Besleyici kesiği — ICTP çalışıyor", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 18-3 · 18-4 · Tablo 12-1 / 12-4 (TO6) · §10.1.1.3 · sıralama: bizim")])
        xa0, xe = -4.6, 6.5
        F = lambda f: xa0 + 1.05 * f
        y1, y2, y3, ya = 1.35, 0.05, -1.25, -2.05
        xh, xac, xs, xb = 0.65, 1.0, 2.3, 3.95
        lab = VGroup(side_lbl("CT 1 · çalışan", y1, CT1C, size=16), side_lbl("CT 2 · bekleme", y2, CT2C, size=16), side_lbl("ONU'lar", y3, ONUC, size=16))
        ax = VGroup(Line([xa0, ya, 0], [-0.3, ya, 0], color=MUTED, stroke_width=2), Line([0.3, ya, 0], [xe, ya, 0], color=MUTED, stroke_width=2),
                    VMobject(stroke_color=MUTED, stroke_width=2).set_points_as_corners([[-0.3, ya, 0], [-0.15, ya + 0.12, 0], [0.0, ya - 0.12, 0], [0.15, ya + 0.12, 0], [0.3, ya, 0]]))
        tk = VGroup(*[Line([F(f), ya - 0.07, 0], [F(f), ya + 0.07, 0], color=MUTED, stroke_width=1.5) for f in range(5)],
                    *[T(str(f), 14, MUTED, BOLD).next_to([F(f), ya, 0], DOWN, buff=0.08) for f in range(5)],
                    T("× 125 µs", 14, MUTED, BOLD).next_to([F(4), ya, 0], DOWN, buff=0.08).shift(RIGHT * 0.65))
        brk = T("Thold · Twfail: değer yok", 14, WARN, BOLD).move_to([2.2, ya - 0.32, 0])
        cutl = VGroup(DashedLine([xa0, y3 - 0.3, 0], [xa0, y1 + 0.55, 0], color=CUTC, stroke_width=2), cutmark([xa0, y1 + 0.72, 0], CUTC, 0.12),
                      T("besleyici kesildi (CT 1 tarafı)", 15, CUTC, BOLD).move_to([xa0 + 0.25, y1 + 0.72, 0], aligned_edge=LEFT))
        it = tag("ICTP çalışıyor", ICTPC, 15).move_to([5.4, y1 + 0.72, 0])
        c1a = VGroup(tbseg(xa0, F(4), y1, 6), txbar(xa0, F(4), y1 - 0.31))
        c1b = VGroup(tbseg(F(4), xh, y1, 7), txbar(F(4), xh, y1 - 0.31))
        c1c = tbseg(xh, xe, y1, 8)
        c2a = tbseg(xa0, F(4), y2, 3)
        c2b = tbseg(F(4), xac, y2, 4)
        c2c = VGroup(tbseg(xac, xb, y2, 5), txbar(xac, xb, y2 - 0.31))
        c2d = VGroup(tbseg(xb, xe, y2, 6), txbar(xb, xe, y2 - 0.31))
        o1 = oseg(xa0, F(3), y3, "O5.1", label="O5")
        o2 = oseg(F(3), xs, y3, "O6")
        o3 = oseg(xs, xe, y3, "O5.1", label="O5")
        e_lods = T("LODS: 3 çerçeve → O6 · TO6 durur", 14, LDC, BOLD).move_to([F(3) + 0.9, y3 - 0.45, 0], aligned_edge=RIGHT)
        e_q = T("QLOS → (7) · Twfail ▶ · yayın sürer", 14, ACTC, BOLD).move_to([F(4) + 0.3, y1 + 0.42, 0], aligned_edge=RIGHT)
        e_s = T("SLOS 0,5 ms → (4) · Tpfail ▶", 14, STBC, BOLD).move_to([F(4) + 0.3, y2 + 0.42, 0], aligned_edge=RIGHT)
        e_h = T("Thold & Twfail → (8) · Tx kapalı", 14, EXCC, BOLD).move_to([xh - 0.15, y1 + 0.42, 0], aligned_edge=LEFT)
        ia = ictp_arrow(xh + 0.08, y1 - 0.24, xac, y2 + 0.24, "Active()", 14, RIGHT, 0.08)
        e_on = T("(5): Tx açık · Tract ▶", 14, ACTC, BOLD).move_to([xac, y2 - 0.55, 0], aligned_edge=LEFT)
        e_sy = T("≥ 2 çerçeve senkron → O5 · TO6 sürer", 14, OPC, BOLD).move_to([xs - 0.1, y3 - 0.45, 0], aligned_edge=LEFT)
        fb = arrow([xb, y3 + 0.24, 0], [xb, y2 - 0.36, 0], ONUC, 2.4, 0.12)
        e_fb = T("ilk BWmap-tutarlı burst → (6)", 14, ONUC, BOLD).next_to(fb, RIGHT, buff=0.1).shift(DOWN * 0.08)
        self.play(FadeIn(lab), FadeIn(ax), FadeIn(tk), FadeIn(c1a), FadeIn(c2a), FadeIn(o1), run_time=0.6)
        self.play(Create(cutl[0]), FadeIn(cutl[1:], scale=1.2), run_time=0.45)
        self.at(self.cue("ICTP çalışıyor", 1.7))
        self.play(FadeIn(it, shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("ONU'lar üç çerçevede", 2.9))
        self.play(GrowFromEdge(o2, LEFT), FadeIn(e_lods, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Çalışan taraf nitelikli", 8.1))
        self.play(GrowFromEdge(c1b, LEFT), FadeIn(e_q, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("bekleme tarafı yarım", 12.9))
        self.play(GrowFromEdge(c2b, LEFT), FadeIn(e_s, shift=UP * 0.05), FadeIn(brk), run_time=0.5)
        self.at(self.cue("Tutma ve çalışma arızası dolunca", 16.8))
        self.play(GrowFromEdge(c1c, LEFT), FadeIn(e_h, shift=UP * 0.05), run_time=0.5)
        self.play(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in ia], run_time=0.4)
        self.at(self.cue("bekleme tarafı vericisini", 22.6))
        self.play(GrowFromEdge(c2c, LEFT), FadeIn(e_on, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("ONU'lar en az iki", 25.2))
        self.play(GrowFromEdge(o3, LEFT), FadeIn(e_sy, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Haritayla tutarlı ilk burst", 31.7))
        self.play(GrowArrow(fb), FadeIn(e_fb), run_time=0.4)
        self.play(GrowFromEdge(c2d, LEFT), run_time=0.4)
        self.end(pad=0.1)
        self.save_timeline("ep20_p1B")


class E20P1C(Act20):
    HDR, MANIFEST, PREV_BADGE = H20[1], M20("p1"), "std"

    def construct(self):
        # b10 — §18.3: Tictp = 0, two states become pass-through; the text names Pre-Working and Helpme, Fig. 18-3 dashes Pre-Protecting (and Helpme);
        #       our reading: the text is wrong, Tract runs in Pre-Working; Working goes silent after Thold & Twfail, Standby talks after Tpfail — only the order separates them
        self.beat("b10")
        h = self.reset("ICTP'siz makine — §18.3 · Şekil 18-3", "std", 0.5, extra=[self.src_in("G.989.3 §18.3 · Şekil 18-3 · Tablo 18-2")])
        c0b, c0a = chain([1, 2, 3], 1.65, labels=["LOS temiz", "geçiş"], colors=[GOOD, MUTED], dashed=(2,))
        c1b, c1a = chain([3, 4, 5, 6], 0.25, labels=["SLOS", "Tpfail doldu", "LOS temiz"], colors=[STBC, TMRC, GOOD])
        c2b, c2a = chain([6, 7, 8, 3], -1.15, labels=["QLOS", "Thold & Twfail", "geçiş"], colors=[ACTC, TMRC, MUTED], dashed=(8,))
        rl = VGroup(T("bekleme → etkin", 14, CT2C, BOLD).next_to(c1b, UP, buff=0.08).align_to(c1b, RIGHT),
                    T("etkin → bekleme", 14, CT1C, BOLD).next_to(c2b, UP, buff=0.08).align_to(c2b, RIGHT))
        t0 = VGroup(tag("Tictp = 0", ICTPC, 16), T("ICTP altyapısı yok", 15, MUTED, BOLD)).arrange(DOWN, buff=0.08).move_to([4.6, 1.65, 0])
        txt = VGroup(T("§18.3 metni:", 15, MUTED, BOLD), T("(5) çalışma öncesi + (8) yardım isteme → geçiş", 15, WARN, BOLD)).arrange(RIGHT, buff=0.12)
        fig = VGroup(T("Şekil 18-3:", 15, MUTED, BOLD), T("(2) koruma öncesi + (8) yardım isteme kesik", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.12)
        cmp_ = VGroup(txt, fig).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-6.4, -2.2, 0], aligned_edge=LEFT)
        rd = VGroup(ytag("bizim okumamız"), T("metin hatalı: Tract (5)'te çalışır", 15, TXT, BOLD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        rd.move_to([2.5, -2.2, 0], aligned_edge=LEFT)
        ordr = VGroup(T("iki vericiyi yalnızca sıralama ayırır:", 16, TXT, BOLD), T("Tpfail > Thold, Twfail", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0.3, -3.05, 0])
        tr5 = SurroundingRectangle(c1b[2], color=TMRC, buff=0.06, stroke_width=2.5)
        tr5l = T("Tract ▶", 14, TMRC, BOLD).next_to(tr5, DOWN, buff=0.05)
        self.at(self.cue("ICTP yoksa ICTP", 0.0))
        self.play(FadeIn(t0, shift=LEFT * 0.05), run_time=0.4)
        self.play(FadeIn(c0b), *[FadeIn(a) for a in c0a], run_time=0.5)
        self.play(FadeIn(c1b), *[FadeIn(a) for a in c1a], FadeIn(c2b), *[FadeIn(a) for a in c2a], FadeIn(rl), run_time=0.7)
        self.at(self.cue("iki durum geçiş durumu", 4.1))
        self.play(Indicate(VGroup(c0b[1], c2b[2]), color=MUTED, scale_factor=1.06), run_time=0.6)
        self.at(self.cue("Metin bunlara", 6.7))
        self.play(FadeIn(txt, shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("şekil koruma öncesini", 10.9))
        self.play(FadeIn(fig, shift=RIGHT * 0.05), Indicate(c0b[1], color=GOOD, scale_factor=1.06), run_time=0.5)
        self.at(self.cue("bizim okumamızla", 13.7))
        self.play(FadeIn(rd[0], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("onay zamanlayıcısı çalışma", 16.5))
        self.play(Create(tr5), FadeIn(tr5l), FadeIn(rd[1], shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("Çalışan taraf tutma", 20.8))
        self.play(Indicate(c2a[1], color=TMRC, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("bekleme tarafı koruma arızasından", 25.4))
        self.play(Indicate(c1a[1], color=TMRC, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("iki vericiyi yalnızca", 29.4))
        self.play(FadeIn(ordr, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # b11 — PMD bridge (S1·B10, S1·B2): Type B leaves the ONU optics alone, but Tract meets distance. Our inference: the ONU syncs on the first frame
        #       after Tx-on and answers with the second frame's BWmap ≈ 125 µs + Teqd → DD20 361 µs, DD40 561 µs > 0.5 ms → false COMM-FAIL
        self.beat("b11")
        h, chp = self.pmd_reset2("PMD Köprüsü — Tract ve mesafe", [s1chip(10, 16), s1chip(2, 16)])
        self.play(self.set_src("S1·B10 · S1·B2 (DD20/DD40) · §18.2.5 · (13-6) · hesap: bizim"), run_time=0.3)
        X = lambda t: -5.0 + t * 0.01514
        ya = -2.05
        ax = Line([X(0), ya, 0], [X(700), ya, 0], color=MUTED, stroke_width=2)
        tk = VGroup(*[Line([X(t), ya - 0.07, 0], [X(t), ya + 0.07, 0], color=MUTED, stroke_width=1.5) for t in range(0, 701, 125)],
                    *[T(str(t), 14, MUTED, BOLD).next_to([X(t), ya, 0], DOWN, buff=0.08) for t in range(0, 701, 125)],
                    T("µs · verici açıldıktan sonra", 14, MUTED, BOLD).next_to([X(700), ya, 0], DOWN, buff=0.08).shift(LEFT * 1.0 + DOWN * 0.3))
        n1 = VGroup(T("S1·B10: B tipi ONU optiğine dokunmaz ✓", 16, S1C, BOLD), T("· ama onay zamanlayıcısı mesafeye dokunur", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.12)
        fit(n1, 12.6).move_to([0, 2.05, 0])
        inf = VGroup(ytag("bizim çıkarımımız"), T("ONU 1. çerçevede senkron · 2. çerçevenin haritasıyla gönderir → ≈ 125 µs + T_eqd", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(inf, 12.6).move_to([0, 1.5, 0])
        trl = VGroup(DashedLine([X(500), ya, 0], [X(500), 0.85, 0], color=WARN, stroke_width=2.4), T("Tract ≈ 0,5 ms", 16, WARN, BOLD).move_to([X(500), 1.02, 0]))
        f1 = Rectangle(width=X(125) - X(0), height=0.36, stroke_color=ACC, stroke_width=1.8, fill_color=ACC, fill_opacity=0.3).move_to([(X(0) + X(125)) / 2, 0.5, 0])
        f1l = T("1. çerçeve: senkron", 14, ACC, BOLD).next_to(f1, DOWN, buff=0.06)
        b20 = Rectangle(width=X(361) - X(125), height=0.38, stroke_color=GOOD, stroke_width=1.8, fill_color=GOOD, fill_opacity=0.3).move_to([(X(125) + X(361)) / 2, -0.35, 0])
        b20l = T("125 + T_eqd 236 (DD20) = 361 µs", 15, TXT, BOLD).move_to(b20)
        b40 = Rectangle(width=X(561) - X(125), height=0.38, stroke_color=WARN, stroke_width=1.8, fill_color=WARN, fill_opacity=0.25).move_to([(X(125) + X(561)) / 2, -1.15, 0])
        b40l = T("125 + T_eqd 436 (DD40) = 561 µs", 15, TXT, BOLD).move_to(b40)
        ok20 = T("✓ zamanında", 15, GOOD, BOLD).next_to(b20, RIGHT, buff=0.15)
        bad = T("> 0,5 ms → sahte COMM-FAIL", 16, WARN, BOLD).next_to(b40, RIGHT, buff=0.15)
        fit(bad, X(700) + 0.9 - b40.get_right()[0])
        txo = VGroup(Line([X(0), 0.2, 0], [X(0), ya, 0], color=TXON, stroke_width=2.5), T("Tx açık", 14, TXON, BOLD).next_to([X(0), 0.75, 0], LEFT, buff=0.12))
        self.at(self.cue("Birinci sezonun onuncu", 1.0))
        self.play(FadeIn(n1[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("mesafeye dokunur", 7.5))
        self.play(FadeIn(n1[1], shift=LEFT * 0.05), Create(ax), FadeIn(tk), run_time=0.6)
        self.at(self.cue("Bizim çıkarımımız", 10.8))
        self.play(FadeIn(inf[0]), FadeIn(txo), run_time=0.35)
        self.at(self.cue("ilk çerçevede senkron", 12.3))
        self.play(GrowFromEdge(f1, LEFT), FadeIn(f1l), FadeIn(inf[1], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("yüz yirmi beş mikrosaniye artı", 19.0))
        self.play(Create(trl[0]), FadeIn(trl[1]), run_time=0.45)
        self.at(self.cue("yirmi kilometre sınıfında", 22.9))
        self.play(GrowFromEdge(b20, LEFT), FadeIn(b20l), run_time=0.5)
        self.play(FadeIn(ok20), run_time=0.3)
        self.at(self.cue("kırk kilometrede", 29.5))
        self.play(GrowFromEdge(b40, LEFT), FadeIn(b40l), run_time=0.6)
        self.at(self.cue("yarım milisaniyeyi aşar", 33.5))
        self.play(FadeIn(bad, shift=LEFT * 0.05), Indicate(trl[1], color=WARN, scale_factor=1.1), run_time=0.5)
        self.end(pad=0.05)

        # b12 — second inference: a silent receiver on the old side (fibre intact); without ICTP that CT sees SLOS in Protecting, Tpfail expires and it turns
        #       its transmitter on next to the new Working CT until Tract expires (≈ 0.5 ms); with ICTP the peer answers Standby-Clear() and it stays dark
        self.beat("b12")
        h = self.reset("İkinci çıkarım — sessiz alıcı", "neden", 0.5, extra=[self.src_in("G.989.3 Şekil 18-3 · Tablo 18-4 · çıkarım: bizim")])
        xs0, xe = -3.9, 6.4
        ia_, ib_ = 1.45, 0.55
        ja, jb = -0.95, -1.85
        tA = VGroup(T("ICTP yok", 18, WARN, BOLD), T("Şekil 18-3", 14, MUTED, BOLD)).arrange(RIGHT, buff=0.15).move_to([-6.4, 2.05, 0], aligned_edge=LEFT)
        tB = VGroup(T("ICTP var", 18, ICTPC, BOLD), T("Şekil 18-2", 14, MUTED, BOLD)).arrange(RIGHT, buff=0.15).move_to([-6.4, -0.3, 0], aligned_edge=LEFT)
        lab = VGroup(side_lbl("eski taraf", ia_, CT1C, size=16), side_lbl("yeni çalışan", ib_, CT2C, size=16),
                     side_lbl("eski taraf", ja, CT1C, size=16), side_lbl("yeni çalışan", jb, CT2C, size=16))
        sil = tag("fiber sağlam · alıcı sessiz", WARN, 15).move_to([4.9, 2.27, 0])
        a1 = tbseg(xs0, -2.4, ia_, 3, 0.42, 14)
        a2 = tbseg(-2.4, 0.2, ia_, 4, 0.42, 14)
        a3 = VGroup(tbseg(0.2, 3.4, ia_, 5, 0.42, 14), txbar(0.2, 3.4, ia_ - 0.28))
        a4 = tbseg(3.4, xe, ia_, 9, 0.42, 14)
        an = VGroup(tbseg(xs0, xe, ib_, 6, 0.42, 14), txbar(xs0, xe, ib_ - 0.28))
        ea = VGroup(T("SLOS", 14, STBC, BOLD).move_to([-2.4, ia_ + 0.38, 0]), T("Tpfail doldu · Tx açık", 14, TMRC, BOLD).move_to([0.25, ia_ + 0.38, 0], aligned_edge=LEFT),
                    T("Tract doldu", 14, TMRC, BOLD).move_to([3.45, ia_ + 0.38, 0], aligned_edge=LEFT))
        ov = Rectangle(width=3.2, height=1.45, stroke_color=WARN, stroke_width=2.2, fill_color=WARN, fill_opacity=0.12).move_to([1.8, (ia_ + ib_) / 2 - 0.05, 0])
        ovl = T("iki verici birlikte ≈ 0,5 ms (Tract)", 15, WARN, BOLD).move_to([1.8, ib_ - 0.5, 0])
        b1 = tbseg(xs0, -2.4, ja, 3, 0.42, 14)
        b2 = tbseg(-2.4, -0.3, ja, 4, 0.42, 14)
        b3 = tbseg(-0.3, xe, ja, 9, 0.42, 14)
        bn = VGroup(tbseg(xs0, xe, jb, 6, 0.42, 14), txbar(xs0, xe, jb - 0.28))
        eb = T("SLOS", 14, STBC, BOLD).move_to([-2.4, ja + 0.38, 0])
        pe = ictp_arrow(-1.75, ja - 0.22, -1.75, jb + 0.22, "Peering()", 14, LEFT, 0.08)
        sc = ictp_arrow(-0.75, jb + 0.22, -0.75, ja - 0.22, "Standby-Clear()", 14, RIGHT, 0.08)
        dk = T("karanlıkta kalır ✓", 15, GOOD, BOLD).move_to([3.6, ja + 0.4, 0])
        cnc = VGroup(ytag("bizim çıkarımımız"), T("sadeleşmiş makine “hiçbir an birlikte yayın yok” hedefini tam karşılayamaz", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(cnc, 12.6).move_to([0, -2.75, 0])
        self.play(FadeIn(lab[:2]), FadeIn(tA), FadeIn(an), FadeIn(a1), run_time=0.5)
        self.at(self.cue("sessiz bir alıcıysa", 1.6))
        self.play(FadeIn(sil, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("basit kayıp görür", 6.4))
        self.play(GrowFromEdge(a2, LEFT), FadeIn(ea[0]), run_time=0.45)
        self.at(self.cue("koruma arızası dolar", 11.4))
        self.play(FadeIn(ea[1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("yeni çalışanın yanında", 13.2))
        self.play(GrowFromEdge(a3, LEFT), run_time=0.5)
        self.play(FadeIn(ov), FadeIn(ovl), run_time=0.4)
        self.at(self.cue("onay zamanlayıcısı dolana", 16.7))
        self.play(FadeIn(ea[2]), GrowFromEdge(a4, LEFT), run_time=0.45)
        self.at(self.cue("Sadeleşmiş makine", 21.6))
        self.play(FadeIn(cnc[0]), run_time=0.3)
        self.at(self.cue("hiçbir an birlikte", 23.1))
        self.play(FadeIn(cnc[1], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ICTP varsa", 28.0))
        self.play(FadeIn(tB), FadeIn(lab[2:]), FadeIn(bn), FadeIn(b1), GrowFromEdge(b2, LEFT), FadeIn(eb), run_time=0.6)
        self.play(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in pe], run_time=0.35)
        self.play(*[GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m) for m in sc], GrowFromEdge(b3, LEFT), run_time=0.5)
        self.at(self.cue("karanlıkta kalır", 32.6))
        self.play(FadeIn(dk, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # b13 — engineer note
        self.note11("b13", [("1", "Ne 50 ms hedefi var, ne bir anahtarlama süresi",
                             "Yarış: B tipi zamanlayıcılar ↔ ONU'nun yeniden ayarlanma kararı (TO2 / TO3).\nİkisinin de değeri yok — hepsini üreticiden yazılı isteyin.", "elli milisaniye"),
                            ("2", "Nitelikli kaybın dışlama kurallarını hiçbir madde yazmaz",
                             "Toplu bir son nefeste (örneğin bina elektrik kesintisi)\nyanlış kural, gereksiz bir anahtarlamadır.", "İki:")])
        self.bridge_beat("b14", "OLT tarafı kendini korudu.\nPeki bütün bir kanal kaybolursa, ONU kendini nasıl kurtarır?")
        self.save_timeline("ep20_p1C")


# ================================ PERDE 2 ======================================
def onode(name, sub=None, w=2.3, h=0.8, key=None):  # noqa: E302
    return sbox(name, sub if sub is not None else SM_SUB.get(key or name, ""), SM_COL.get(key or name, MUTED), w, h, 20, 15)


class E20P2A(Act20):
    HDR, MANIFEST, FIRST = H20[2], M20("p2"), True

    def construct(self):
        # c1 — §17 hands wavelength channel protection to §18, which only has Type B; the ONU-side mechanism is scattered: one PLOAM message,
        #      the activation tables, PM counters and Annex J
        self.beat("c1")
        tc = self.title_card("PERDE 2", "ONU tarafında koruma ve ICTP")
        h = self.heading("§17 → §18: yalnızca B tipi")
        self.at(self.cue("On yedinci madde", 2.6))
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        d17 = doc_card("§17", ["dalga boyu kanalı", "koruması → §18"], GOLD, 3.2, 1.35, 20, 16).move_to([-4.4, 1.0, 0])
        d18 = doc_card("§18", ["yalnızca B tipi", "(OLT CT'ler)"], GOLD, 3.2, 1.35, 20, 16).move_to([0.0, 1.0, 0])
        a1 = arrow(d17.get_right() + RIGHT * 0.1, d18.get_left() + LEFT * 0.1, GOLD, 2.6, 0.14)
        no = VGroup(T("ONU tarafı?", 18, TXT, BOLD), T("✗ orada yok", 18, WARN, BOLD)).arrange(DOWN, buff=0.08).move_to([3.9, 1.0, 0])
        sc = T("ONU tarafının mekanizması: dağınık", 18, TXT, BOLD).move_to([0, -0.5, 0])
        dc = VGroup(doc_card("§11.3.3.15", ["Protection_Control", "PLOAM · 0x19"], GOOD, 2.95, 1.3, 18, 15),
                    doc_card("Tablo 12-1…12-5", ["aktivasyon:", "O6 · O8 · O9"], SM_COL["O6"], 2.95, 1.3, 18, 15),
                    doc_card("Tablo 14-1", ["sayaçlar:", "LODS · devirler"], "#C084FC", 2.95, 1.3, 18, 15),
                    doc_card("Ek J.2.2", ["çekişmeli", "koruma tahsisi"], GOLD, 2.95, 1.3, 18, 15)).arrange(RIGHT, buff=0.22).move_to([0, -1.75, 0])
        self.play(FadeIn(d17, shift=RIGHT * 0.05), self.set_src("G.989.3 §17 giriş · §18 · §11.3.3.15 · Tablo 12-x · Tablo 14-1 · Ek J"), run_time=0.45)
        self.play(GrowArrow(a1), FadeIn(d18, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("ama orada yalnızca", 8.9))
        self.play(FadeIn(no, shift=LEFT * 0.05), Indicate(d18, color=WARN, scale_factor=1.03), run_time=0.5)
        self.at(self.cue("dağınıktır", 11.7))
        self.play(FadeIn(sc, shift=UP * 0.05), run_time=0.35)
        for k, (key, d) in enumerate((("bir PLOAM mesajı", 14.9), ("aktivasyon tabloları", 16.3), ("sayaçlar ve", 18.1), ("J eki", 18.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(dc[k], shift=UP * 0.08), run_time=0.3)
        self.end(pad=0.05)

        # c2 — Protection_Control (Table 11-20): directed or broadcast to one DS wavelength; two 32-bit PON-IDs point at the protection channel profiles;
        #      flag 0x00 enables (WLCP ON), any other value disables; the ONU stores it and acknowledges; only Enable SN (leaving O7) discards them (set VI)
        self.beat("c2")
        h = self.reset("Protection_Control — Tablo 11-20", "std", 0.5, extra=[self.src_in("G.989.3 §11.3.3.15 · Tablo 11-20 · Tablo 11-2 · Tablo 12-5 (küme VI)")])
        mt = VGroup(mtile(0x19, "Protection_Control ↓", "prot", 3.6, 0.44, 17), tag("değişmez · TWDM ve PtP WDM", MUTED, 15)).arrange(RIGHT, buff=0.3)
        mt.move_to([-6.4, 1.95, 0], aligned_edge=LEFT)
        spec = [("ONU-ID", 1.3, OIDC, "1–2"), ("0x19", 0.85, TYC, "3"), ("SeqNo", 0.95, SQC, "4"), ("↓ koruma PON-ID", 2.45, CH[1], "5–8"),
                ("↑ koruma PON-ID", 2.45, CH[3], "9–12"), ("bayrak", 1.0, GOLD, "13"), ("dolgu", 1.9, MUTED, "14–40"), ("MIC", 1.35, MICC, "41–48")]
        oc = octets(spec, 12.4, 0.58, 16, 14).move_to([0, 1.0, 0])
        o1 = VGroup(T("ONU-ID:", 16, OIDC, BOLD), T("tek ONU", 16, TXT, BOLD), T("ya da", 15, MUTED, BOLD), HX("0x03FF", 16, OIDC, BOLD),
                    T("→ bir ↓ dalga boyundaki bütün ONU'lar", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12).move_to([-6.4, -0.45, 0], aligned_edge=LEFT)
        pid = brace_lbl(VGroup(oc[3][0], oc[4][0]), "32 + 32 bit → koruma kanalının ↓ / ↑ kanal profili", ACC, DOWN, 16)
        pid.shift(DOWN * 0.22)
        fl = VGroup(T("bayrak", 16, GOLD, BOLD), HX("0x00", 17, GOOD, BOLD), T("→ koruma açık (WLCP ON)", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.12)
        fl.move_to([-6.4, -1.1, 0], aligned_edge=LEFT)
        fl2 = VGroup(T("başka her değer", 16, WARN, BOLD), T("→ kapalı · PON-ID'ler yok sayılır", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12).next_to(fl, RIGHT, buff=0.45)
        ack = VGroup(onu_box("ONU", ONUC, 1.0, 0.42, 15), T("saklar →", 16, TXT, BOLD), mtile(0x09, "Acknowledgement ↑", "ack", 3.2, 0.42, 16)).arrange(RIGHT, buff=0.2)
        ack.move_to([-6.4, -1.82, 0], aligned_edge=LEFT)
        st = VGroup(tag("küme VI", SETC[5], 15), T("koruma PON-ID'lerini yalnızca", 16, TXT, BOLD), tag("Enable SN · O7'den çıkış", ESC, 15), T("siler", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        st.move_to([-6.4, -2.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(mt, shift=RIGHT * 0.05), LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in oc], lag_ratio=0.08), run_time=0.9)
        self.play(FadeIn(o1, shift=RIGHT * 0.05), Indicate(oc[0], color=OIDC, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("Otuz iki bitlik", 7.1))
        self.play(Indicate(VGroup(oc[3], oc[4]), color=ACC, scale_factor=1.03), run_time=0.5)
        self.at(self.cue("koruma kanalının aşağı", 9.8))
        self.play(FadeIn(pid, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("Bayrak sıfırsa", 14.7))
        self.play(FadeIn(fl, shift=RIGHT * 0.05), Indicate(oc[5], color=GOLD, scale_factor=1.08), run_time=0.5)
        self.at(self.cue("başka her değer", 17.1))
        self.play(FadeIn(fl2, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ONU bilgiyi saklar", 19.1))
        self.play(FadeIn(ack, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("acil durdurmadan çıkış", 21.6))
        self.play(FadeIn(st, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # c3 — the ONU's path: O5 → LODS → O6 (WLCP ON: TO3, OFF: TO2); DSYNC in time → O5 (Type B success); TO2 → O1; TO3 → forget burst profiles → O8
        #      (target / previous / protection / matching channel); channel OK → O9, TO5 starts
        self.beat("c3")
        h = self.reset("ONU'nun yolu — O5 → O6 → O8 → O9 → O5", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 12-1 · 12-2 · 12-4 (Amd.1 TO6) · Tablo 12-5")])
        yb = 0.95
        n5 = onode("O5", "çalışma", 2.0, key="O5.1").move_to([-5.45, yb, 0])
        n6 = onode("O6", None, 2.0).move_to([-2.0, yb, 0])
        n8 = onode("O8", "↓ ayar", 2.0, key="O8.1").move_to([1.55, yb, 0])
        n9 = onode("O9", None, 2.0).move_to([5.15, yb, 0])
        n1 = onode("O1", "başlangıç", 2.0, key="O1.1").move_to([-2.0, -1.25, 0])
        e56 = VGroup(arrow(n5[0].get_right() + UP * 0.17, n6[0].get_left() + UP * 0.17, LDC, 2.4, 0.13),
                     T("LODS", 15, LDC, BOLD).move_to([-3.72, yb + 0.4, 0]))
        e65 = VGroup(arrow(n6[0].get_left() + DOWN * 0.17, n5[0].get_right() + DOWN * 0.17, OPC, 2.4, 0.13),
                     T("DSYNC", 15, OPC, BOLD).move_to([-3.72, yb - 0.4, 0]))
        tbs = tag("B tipinin başarısı", OPC, 15).move_to([-4.1, yb - 0.85, 0])
        tmr = VGroup(T("WLCP açık → TO3 ▶", 15, LDC, BOLD), T("·", 15, MUTED, BOLD), T("kapalı → TO2 ▶", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.1).move_to([-2.0, yb + 0.72, 0])
        e61 = VGroup(arrow(n6[0].get_bottom(), n1[0].get_top(), O1C, 2.4, 0.13), T("TO2 doldu", 15, O1C, BOLD).move_to([-1.2, -0.22, 0]))
        e68 = VGroup(arrow(n6[0].get_right(), n8[0].get_left(), LDC, 2.4, 0.13), T("TO3 doldu", 15, LDC, BOLD).move_to([-0.22, yb + 0.25, 0]))
        fg = VGroup(T("küme I: burst", 14, SETC[0], BOLD), T("profilleri unutulur", 14, SETC[0], BOLD)).arrange(DOWN, buff=0.03).move_to([-0.22, yb - 0.55, 0])
        chs = VGroup(T("yeni kanal:", 14, TUC, BOLD), *[tag(s, TUC, 14) for s in ("hedef", "önceki", "koruma", "eşleşen")])
        VGroup(chs[0], VGroup(*chs[1:3]).arrange(RIGHT, buff=0.08), VGroup(*chs[3:]).arrange(RIGHT, buff=0.08)).arrange(DOWN, buff=0.08)
        chs.move_to([1.6, yb - 1.35, 0])
        chs[3][0].set_stroke(GOOD, 2.5)
        chs[3][1].set_color(GOOD)
        e89 = VGroup(arrow(n8[0].get_right(), n9[0].get_left(), TUC, 2.4, 0.13), T("kanal uygun", 15, TUC, BOLD).move_to([3.35, yb + 0.25, 0]),
                     T("TO5 ▶", 15, TMRC, BOLD).move_to([3.35, yb - 0.25, 0]))
        self.play(FadeIn(n5), run_time=0.3)
        self.at(self.cue("O5'te senkron kaybolunca", 1.1))
        self.play(GrowArrow(e56[0]), FadeIn(e56[1]), FadeIn(n6), run_time=0.45)
        self.at(self.cue("koruma açıksa TO3", 4.2))
        self.play(FadeIn(tmr[0], shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("kapalıysa TO2", 5.9))
        self.play(FadeIn(tmr[1:], shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("Senkron süre dolmadan", 8.1))
        self.play(GrowArrow(e65[0]), FadeIn(e65[1]), run_time=0.4)
        self.at(self.cue("B tipinin başarısı", 11.6))
        self.play(FadeIn(tbs, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("TO2 dolarsa", 13.7))
        self.play(GrowArrow(e61[0]), FadeIn(e61[1]), FadeIn(n1, shift=DOWN * 0.05), run_time=0.45)
        self.at(self.cue("TO3 dolarsa", 15.7))
        self.play(GrowArrow(e68[0]), FadeIn(e68[1]), FadeIn(n8), run_time=0.45)
        self.play(FadeIn(fg, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("yeni kanal hedef", 20.1))
        self.play(FadeIn(chs[0]), FadeIn(chs[1]), run_time=0.3)
        self.at(self.cue("önceki,", 21.5))
        self.play(FadeIn(chs[2]), run_time=0.25)
        self.at(self.cue("koruma ya da eşleşen", 22.1))
        self.play(FadeIn(chs[3]), FadeIn(chs[4]), run_time=0.3)
        self.at(self.cue("Kanal uygun bulununca", 25.5))
        self.play(GrowArrow(e89[0]), FadeIn(e89[1]), FadeIn(n9), run_time=0.45)
        self.at(self.cue("TO5 başlar", 28.3))
        self.play(FadeIn(e89[2]), run_time=0.3)
        self.end(pad=0.05)

        # c4 — O9: Tuning_Response(Complete_u) on every directed PLOAM grant or broadcast contention-based protection grant, until feedback or TO5;
        #      a directed confirmation restarts TO6 → O5; TO2 … TO5 have no values
        self.beat("c4")
        gr = VGroup(tile("yönlü PLOAM tahsisi", ACC, 2.75, 0.4, 15, 0.18), tile("çekişmeli koruma tahsisi", GOLD, 2.75, 0.4, 15, 0.22)).arrange(DOWN, buff=0.1)
        gr.move_to([5.15, -0.2, 0])
        tr_ = VGroup(T("↓", 18, MUTED, BOLD), mtile(0x1A, "Tuning_Response ↑", "tun", 2.85, 0.4, 15), T("Complete_u", 15, GOLD, BOLD)).arrange(DOWN, buff=0.05)
        tr_.next_to(gr, DOWN, buff=0.08)
        un = T("geri bildirim ya da TO5'e kadar", 14, TMRC, BOLD).next_to(tr_, DOWN, buff=0.06)
        yb2 = -2.5
        back = VMobject(stroke_color=OPC, stroke_width=2.6).set_points_as_corners([[5.15, -2.12, 0], [5.15, yb2, 0], [-5.9, yb2, 0], [-5.9, yb - 0.4, 0]])
        tip = arrow([-5.9, yb - 0.8, 0], [-5.9, yb - 0.4, 0], OPC, 2.6, 0.14)
        bl = T("yönlü onay → TO6 baştan → O5", 15, OPC, BOLD).move_to([-0.4, yb2 - 0.25, 0])
        nv = VGroup(*[tag(s, TMRC, 14) for s in ("TO2", "TO3", "TO4", "TO5")]).arrange(RIGHT, buff=0.08)
        nvg = VGroup(nv, T("değer yok", 15, WARN, BOLD)).arrange(DOWN, buff=0.08).move_to([-4.35, -1.3, 0])
        self.at(self.cue("her yönlü PLOAM", 0.8))
        self.play(FadeIn(gr[0], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("yayınlanan çekişmeli", 3.5))
        self.play(FadeIn(gr[1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("tamamlandı kipinde", 7.2))
        self.play(FadeIn(tr_, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("geri bildirim gelene", 10.6))
        self.play(FadeIn(un), run_time=0.3)
        self.at(self.cue("Yönlü bir onay", 14.2))
        self.play(Create(back), run_time=0.6)
        self.play(GrowArrow(tip), FadeIn(bl), run_time=0.35)
        self.at(self.cue("ONU O5'e döner", 17.4))
        self.play(Indicate(n5, color=OPC, scale_factor=1.06), run_time=0.5)
        self.at(self.cue("TO2'den TO5'e", 18.7))
        self.play(FadeIn(nvg, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.1)
        self.save_timeline("ep20_p2A")


class E20P2B(Act20):
    HDR, MANIFEST, PREV_BADGE = H20[2], M20("p2"), "std"

    def construct(self):
        # c5 — Annex J.2.2: directed allocations to protected ONUs are wasted; the protection CT may withhold them and give one contention-based allocation
        #      (pre-ranged, frequent) where each ONU signals its arrival; success → that ONU's directed allocations back at once; collision → everyone's;
        #      the broadcast Assign_Alloc-ID carries a retransmission timeout
        self.beat("c5")
        h = self.reset("Koruma tarafı — Ek J.2.2", "std", 0.5, extra=[self.src_in("G.989.3 Ek J.2.2 · Tablo J.1 · J.2 (Assign_Alloc-ID, işlev 0x02)")])
        x0, fw, n = -3.3, 1.18, 8
        ax, X = frame_axis(n, x0, x0 + fw * n, -1.55, True, 14, MUTED)
        y1, y2 = 1.35, 0.25
        l1 = VGroup(T("yönlü × N", 17, ACC, BOLD), T("her korunan ONU", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-6.4, y1, 0], aligned_edge=LEFT)
        l2 = VGroup(T("çekişmeli × 1", 17, GOLD, BOLD), T("işlev 0x02", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-6.4, y2, 0], aligned_edge=LEFT)
        dg = VGroup()
        for f in range(n):
            for j in range(4):
                dg.add(Rectangle(width=0.2, height=0.36, stroke_color=ACC, stroke_width=1.2, fill_color=ACC, fill_opacity=0.35).move_to([X(f) + 0.22 + 0.25 * j, y1, 0]))
        was = VGroup(T("kayıp: anahtarlamaya kadar kimse kullanmaz", 15, WARN, BOLD).move_to([X(4), y1 + 0.42, 0]))
        cs = VGroup(*[Rectangle(width=0.42, height=0.36, stroke_color=GOLD, stroke_width=1.6, fill_color=GOLD, fill_opacity=0.35).move_to([X(f) + 0.35, y2, 0]) for f in range(n)])
        csl = VGroup(*[T("C", 14, TXT, BOLD).move_to(c) for c in cs])
        pr = VGroup(tag("önceden mesafesi ölçülmüş", GOLD, 14), tag("sık", GOLD, 14)).arrange(RIGHT, buff=0.12).move_to([X(4), y2 + 0.45, 0])
        y3 = -0.65
        l3 = VGroup(T("anahtarlamada", 17, TXT, BOLD), T("Tuning_Response ↑", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-6.4, y3, 0], aligned_edge=LEFT)
        okb = VGroup(Rectangle(width=0.42, height=0.36, stroke_color=GOOD, stroke_width=2, fill_color=GOOD, fill_opacity=0.5).move_to([X(2) + 0.35, y3, 0]),
                     T("A", 14, BG, BOLD).move_to([X(2) + 0.35, y3, 0]))
        okl = T("✓ başarı → A'nın yönlü tahsisleri hemen", 14, GOOD, BOLD).next_to(okb, RIGHT, buff=0.12)
        cb = VGroup(Rectangle(width=0.42, height=0.36, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.35).move_to([X(6) + 0.3, y3, 0]),
                    Rectangle(width=0.42, height=0.36, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.35).move_to([X(6) + 0.42, y3 - 0.08, 0]))
        cbl = VGroup(T("✗ çarpışma →", 14, WARN, BOLD), T("bütün korunanlara", 14, WARN, BOLD)).arrange(DOWN, buff=0.03, aligned_edge=LEFT).next_to(cb, RIGHT, buff=0.12)
        aa = VGroup(mtile(0x0A, "Assign_Alloc-ID ↓ · 0x03FF", "alloc", 4.1, 0.42, 15), T("oktet 10: işlev", 15, TXT, BOLD), HX("0x02", 16, GOLD, BOLD),
                    T("· oktet 11: yeniden iletim zaman aşımı (çerçeve)", 15, TXT, BOLD)).arrange(RIGHT, buff=0.12)
        fit(aa, 12.6).move_to([0, -2.55, 0])
        self.play(FadeIn(ax), run_time=0.3)
        self.at(self.cue("Korunan ONU'lara yönlü", 3.4))
        self.play(FadeIn(l1, shift=RIGHT * 0.05), LaggedStart(*[FadeIn(r) for r in dg], lag_ratio=0.01), run_time=0.8)
        stk = Line([X(0), y1, 0], [X(n), y1, 0], color=WARN, stroke_width=3)
        self.play(FadeIn(was, shift=UP * 0.05), dg.animate.set_opacity(0.3), Create(stk), run_time=0.4)
        self.at(self.cue("geri tutup tek bir", 7.2))
        self.play(FadeIn(l2, shift=RIGHT * 0.05), LaggedStart(*[FadeIn(c) for c in cs], lag_ratio=0.08), FadeIn(csl), run_time=0.8)
        self.at(self.cue("anahtarlamada her ONU", 12.8))
        self.play(FadeIn(l3, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("zorunlu olarak önceden", 17.0))
        self.play(FadeIn(pr, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Başarıda o ONU'nun", 23.2))
        self.play(FadeIn(okb, scale=1.2), FadeIn(okl, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("çarpışmada bütün", 24.8))
        self.play(FadeIn(cb, scale=1.2), FadeIn(cbl, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Atama mesajı", 30.3))
        self.play(FadeIn(aa, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # c6 — TPST > 0: longest wait from DS sync on the protection channel to the first allocation to the default Alloc-ID; sets the protection CT's grant
        #      frequency (§7.3.7); no value — nor for the retransmission timeout
        self.beat("c6")
        h = self.reset("TPST — koruma anahtarlama gecikme toleransı", "std", 0.5, extra=[self.src_in("G.989.3 §7.1.1 · §7.3.7 · Ek J Tablo J.1")])
        yl = 0.9
        lne = Line([-6.0, yl, 0], [6.2, yl, 0], color=MUTED, stroke_width=2)
        on = side_lbl("ONU", yl + 0.4, ONUC, x=-6.0, size=16)
        t0x, t1x = -2.6, 3.2
        m0 = tmark(t0x, yl - 0.25, yl + 0.35, "koruma kanalında ↓ senkron", OPC, 15)
        m1 = tmark(t1x, yl - 0.25, yl + 0.35, "varsayılan Alloc-ID'ye ilk tahsis", ACC, 15)
        br = brace_lbl(Line([t0x, yl - 0.3, 0], [t1x, yl - 0.3, 0]), "≤ TPST", GOLD, DOWN, 20)
        gt = VGroup(T("TPST > 0", 22, GOLD, BOLD), T("NG-PON2'ye özgü · §7.1.1", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, 2.0, 0])
        fq = VGroup(T("→ koruma CT'nin tahsis sıklığını belirler", 17, TXT, BOLD), T("(ONU hâlâ birincil kanalında çalışırken · §7.3.7)", 15, MUTED, BOLD)).arrange(DOWN, buff=0.08)
        fq.move_to([0, -1.05, 0])
        ticks = VGroup(*[Rectangle(width=0.16, height=0.3, stroke_width=0, fill_color=ACC, fill_opacity=0.8).move_to([-4.0 + 1.0 * k, -1.85, 0]) for k in range(9)])
        tkl = T("koruma CT'nin tahsisleri", 14, ACC, BOLD).next_to(ticks, LEFT, buff=0.2)
        nv = VGroup(T("değer yok:", 17, WARN, BOLD), tag("TPST", TMRC, 15), tag("yeniden iletim zaman aşımı", TMRC, 15)).arrange(RIGHT, buff=0.15).move_to([0, -2.7, 0])
        self.at(self.cue("koruma anahtarlama gecikme", 1.3))
        self.play(FadeIn(gt[1], shift=DOWN * 0.05), run_time=0.35)
        self.at(self.cue("sıfırdan büyük", 4.4))
        self.play(FadeIn(gt[0], scale=0.9), run_time=0.35)
        self.at(self.cue("ONU'nun koruma kanalında senkron", 5.6))
        self.play(Create(lne), FadeIn(on), FadeIn(m0, shift=DOWN * 0.05), run_time=0.5)
        self.play(FadeIn(m1, shift=DOWN * 0.05), run_time=0.4)
        self.play(FadeIn(br, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("tahsis sıklığını belirler", 13.8))
        self.play(FadeIn(fq, shift=UP * 0.05), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.08), FadeIn(tkl), run_time=0.8)
        self.at(self.cue("Değeri yoktur", 18.4))
        self.play(FadeIn(nv[:2], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("yeniden iletim zaman aşımının", 19.5))
        self.play(FadeIn(nv[2], shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # c7 — our comparison table, Type B vs ONU-side (WLCP)
        self.beat("c7")
        h = self.reset("B tipi ve ONU tarafı — karşılaştırma", "neden", 0.5, extra=[self.src_in("G.989.3 §18 · §11.3.3.15 · Tablo 12-x · Ek J · Tablo 14-1 · derleme: bizim")])
        tg = self.chips_at([ytag("bizim derlememiz")], h)
        rows = [["korur", "bağlantı fiberi · besleyici · WM · CT · şasi", "ONU'nun çalışma kanalı"],
                ["ONU kanal değiştirir", "hayır", "evet · O6 → TO3 → O8 → O9 → O5"],
                ["kararı veren", "sonlandırıcılar · durum makinesi + ICTP", "ONU · TO3 dolunca"],
                ["sayılar", "SLOS 0,5 ms · QLOS 4 çerçeve · Tract ≈ 0,5 ms", "hiç yok"],
                ["sayaçlar · Tablo 14-1", "B tipi anahtarlamayı sayan satır yok", "LODS: hangi kanalda geri geldi"]]
        tb = mtable(["", "B tipi · §18", "ONU tarafı · WLCP"], rows, [2.9, 4.95, 4.75], size=16, hsize=17, row_h=0.66).move_to([0, -0.15, 0])
        for r in tb[1:]:
            r[1].set_color(MUTED)
        tb[4][3].set_color(WARN)
        tb[5][2].set_color(WARN)
        self.play(FadeIn(tg, shift=LEFT * 0.05), FadeIn(tb[0]), *[FadeIn(VGroup(r[0], r[1])) for r in tb[1:]], run_time=0.6)
        cells = [(1, 2, "B tipi besleyiciyi", 2.6), (2, 2, "ONU kanal değiştirmez", 7.3), (3, 2, "kararı sonlandırıcılar", 9.1),
                 (1, 3, "ONU tarafı koruma ONU'nun", 11.6), (2, 3, "ONU kanal değiştirir", 15.1), (3, 3, "kararı TO3 dolunca", 16.8),
                 (4, 2, "B tipinin üç sayısı", 19.3), (4, 3, "ONU tarafının hiç", 21.6), (5, 3, "Sayaçlar kaybın", 23.1), (5, 2, "B tipi anahtarlamaları", 27.4)]
        for r, c, key, d in cells:
            self.at(self.cue(key, d))
            self.play(FadeIn(tb[r][c], shift=RIGHT * 0.05), run_time=0.3)
        self.end(pad=0.05)

        # c8 — PMD bridge S1·B7: tuning classes become time (class 1 < 10 µs … class 3 25 ms–1 s); our reading: profiles may dominate — TO3 expiry discards
        #      the burst profiles, and no grant can be answered until one arrives
        self.beat("c8")
        h, chp = self.pmd_reset2("PMD Köprüsü — ayar süresi", [s1chip(7, 16)])
        self.play(self.set_src("S1·B7 · G.989.2 Tablo 9-2 · G.989.3 Tablo 12-1 / 12-4 (TO3: küme I)"), run_time=0.3)
        ax, X = log_axis(1, 2e7, -4.6, 6.3, -0.95, [(1, "1 µs"), (10, "10 µs"), (100, "100 µs"), (1e3, "1 ms"), (1e4, "10 ms"), (1e5, "100 ms"),
                                                    (1e6, "1 s"), (1e7, "10 s")], 15)
        cls = [("Sınıf 1", 1, 10, "< 10 µs", CLC["1"], 1.55), ("Sınıf 2", 10, 25e3, "10 µs … 25 ms", CLC["2"], 0.95), ("Sınıf 3", 25e3, 1e6, "25 ms … 1 s", CLC["3"], 0.35)]
        bars = VGroup()
        for name, a, b, txt, c, yy in cls:
            r = Rectangle(width=X(b) - X(a), height=0.42, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.35).move_to([(X(a) + X(b)) / 2, yy, 0])
            nm = T(name, 16, c, BOLD).move_to([-6.4, yy, 0], aligned_edge=LEFT)
            v = T(txt, 16, TXT, BOLD)
            if v.width < r.width - 0.2:
                v.move_to(r)
            else:
                v.next_to(r, RIGHT, buff=0.12)
            bars.add(VGroup(r, nm, v))
        bars[1].set_opacity(0.45)
        pb = VGroup(DashedVMobject(Rectangle(width=X(2e7) - X(1e6), height=0.42, stroke_color=PINK, stroke_width=2), num_dashes=30).move_to([(X(1e6) + X(2e7)) / 2, -0.25, 0]),
                    T("?", 18, PINK, BOLD).move_to([(X(1e6) + X(2e7)) / 2, -0.25, 0]))
        pb.add(T("profil gelene kadar", 14, PINK, BOLD).next_to(pb[0], LEFT, buff=0.15))
        pbn = T("+ Burst_Profile", 16, PINK, BOLD).move_to([-6.4, -0.25, 0], aligned_edge=LEFT)
        rd = VGroup(ytag("bizim yorumumuz"), T("süreye profiller de hükmedebilir", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -1.95, 0])
        sq = VGroup(sbox("O6", None, LDC, 0.9, 0.42, 16), T("TO3 doldu → küme I: profiller unutulur →", 15, TXT, BOLD), sbox("O8", None, TUC, 0.9, 0.42, 16),
                    T("→ profil gelmeden hiçbir tahsise cevap yok", 15, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        fit(sq, 12.6).move_to([0, -2.7, 0])
        self.at(self.cue("ayar sınıfları burada", 1.0))
        self.play(Create(ax[0]), FadeIn(ax[1:]), run_time=0.6)
        self.at(self.cue("birinci sınıf on", 7.1))
        self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]), FadeIn(bars[1]), run_time=0.5)
        self.at(self.cue("üçüncü sınıf yirmi", 10.4))
        self.play(GrowFromEdge(bars[2][0], LEFT), FadeIn(bars[2][1:]), run_time=0.5)
        self.at(self.cue("bizim yorumumuzla süreye", 16.1))
        self.play(FadeIn(rd, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("TO3 dolunca ONU burst", 20.7))
        self.play(FadeIn(sq[:3], shift=RIGHT * 0.05), FadeIn(pbn), run_time=0.45)
        self.at(self.cue("profil gelmeden", 24.2))
        self.play(FadeIn(sq[3], shift=LEFT * 0.05), Create(pb[0]), FadeIn(pb[1:]), run_time=0.5)
        self.end(pad=0.05)
        self.save_timeline("ep20_p2B")


UC = ["profil\npaylaşımı", "sessiz başlangıç\nCT ilk kurulumu", "sıfır mesafe\nEqD seçimi", "ilk ONU\ndoğrulaması", "SN · ONU-ID\ntutarlılığı",
      "kimlik doğrulama\nbilgisi", "Alloc-ID\ntutarlılığı", "devir\nbaşlatma", "devir\nkapanışı", "LOB\nhafifletme", "başarım\nizleme",
      "başıboş\nONU", "koruma · yük\npaylaşım ön ayarı", "yük paylaşımı\nyapılandırması"]
PRIM = [("prmNotify", "M"), ("prmInquiry", "M"), ("prmConflict", "M"), ("prtHandshake", "T"), ("bulkData", "T"), ("onuAuthent", "M"), ("onuClaim", "M"),
        ("initHandover", "T"), ("abortHandover", "M"), ("confHandover", "T"), ("rogueAlert", "M"), ("rogueClear", "M"), ("onuAlert", "M"), ("onuClear", "M")]


class E20P2C(Act20):
    HDR, MANIFEST, PREV_BADGE = H20[2], M20("p2"), "pmd"

    def construct(self):
        # c9 — Appendix VI (informative): CTs may span chassis, central offices, service providers; the protocol itself is BBF TR-352 (not in our sources);
        #      Table VI.1 lists 14 use cases from profile sharing to protection and load sharing
        self.beat("c9")
        h = self.reset("ICTP — Ek VI (bilgilendirici)", "std", 0.5, extra=[self.src_in("G.989.3 Ek VI · Tablo VI.1 · §6.1.4.4")])
        doms = VGroup()
        for nm, k in (("şasi", 2), ("merkez ofis", 2), ("servis sağlayıcı", 2)):
            cts = VGroup(*[ctu("CT", OLTC, False, 0.95, 0.4, 15) for _ in range(k)]).arrange(RIGHT, buff=0.15)
            fr = RoundedRectangle(corner_radius=0.12, width=cts.width + 0.4, height=1.05, stroke_color=MUTED, stroke_width=1.8, fill_opacity=0)
            cts.move_to(fr).shift(DOWN * 0.12)
            doms.add(VGroup(fr, cts, T(nm, 15, MUTED, BOLD).move_to(fr.get_top() + DOWN * 0.18)))
        doms.arrange(RIGHT, buff=0.9).move_to([-1.6, 1.4, 0])
        il = VGroup(*[ictp_bar(doms[i][0].get_right()[0] + 0.08, doms[i + 1][0].get_left()[0] - 0.08, 1.4, "", ICTPC, 14) for i in range(2)])
        ill = T("soyut ICTP taşıma kanalı", 14, ICTPC, BOLD).next_to(doms, DOWN, buff=0.12)
        tr = doc_card("BBF TR-352", ["Issue 2 · 2020", "kaynaklarımızda yok"], WARN, 2.7, 1.25, 18, 15).move_to([5.25, 1.4, 0])
        ucs = VGroup()
        for i, s in enumerate(UC):
            c = GOOD if i == 12 else (ICTPC if i in (1, 11) else MUTED)
            r = RoundedRectangle(corner_radius=0.07, width=1.74, height=0.86, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.1)
            t = VGroup(T(f"UC{i + 1}", 14, c, BOLD), tf(s, 14, TXT, BOLD, w=1.62, line_spacing=0.8)).arrange(DOWN, buff=0.03)
            fit(t, 1.62).move_to(r)
            ucs.add(VGroup(r, t))
        VGroup(VGroup(*ucs[:7]).arrange(RIGHT, buff=0.08), VGroup(*ucs[7:]).arrange(RIGHT, buff=0.08)).arrange(DOWN, buff=0.1)
        ucs.move_to([0, -1.55, 0])
        ul = T("Tablo VI.1 · 14 kullanım durumu", 16, TXT, BOLD).next_to(ucs, UP, buff=0.12)
        self.at(self.cue("bilgilendirici", 1.9))
        self.play(FadeIn(tag("bilgilendirici", MUTED, 15).move_to([5.25, 2.45, 0])), run_time=0.3)
        for k, (key, d) in enumerate((("birden fazla şasiye", 3.1), ("merkez ofise", 6.2), ("servis sağlayıcıya", 7.3))):
            self.at(self.cue(key, d))
            anims = [FadeIn(doms[k], shift=UP * 0.05)] + ([FadeIn(il[k - 1])] if k else [])
            self.play(*anims, run_time=0.35)
        self.play(FadeIn(ill), run_time=0.3)
        self.at(self.cue("Broadband Forum", 10.4))
        self.play(FadeIn(tr, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("kaynaklarımızda yoktur", 17.4))
        self.play(Indicate(tr, color=WARN, scale_factor=1.04), run_time=0.5)
        self.at(self.cue("profil paylaşımından", 19.6))
        self.play(FadeIn(ul), LaggedStart(*[FadeIn(u, shift=UP * 0.05) for u in ucs], lag_ratio=0.08), run_time=1.2)
        self.at(self.cue("on dört kullanım", 23.6))
        self.play(Indicate(ucs[12], color=GOOD, scale_factor=1.06), run_time=0.5)
        self.end(pad=0.05)

        # c10 — 14 primitives (M = single message, T = atomic transaction); §18's Peering / Active / Standby-LOS / Standby-Clear / Unprotected are absent;
        #       the table's prtHandshake is per ONU and tied to authentication (UC6); no primitive for UC11 / UC14; Appendix V intentionally empty (all editions)
        self.beat("c10")
        h = self.reset("İlkeller — Tablo VI.3 · ve Ek V", "std", 0.5, extra=[self.src_in("G.989.3 Tablo VI.2 · VI.3 · §18.2 · Ek V (2021 · Amd.1 · Amd.2)")])
        pr = VGroup()
        for i, (nm, ty) in enumerate(PRIM):
            c = ICTPC if ty == "T" else ACC
            r = RoundedRectangle(corner_radius=0.06, width=2.75, height=0.36, stroke_color=c, stroke_width=1.4, fill_color=c, fill_opacity=0.1)
            a = HX(f"{nm}()", 15, TXT, BOLD)
            fit(a, 2.1).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.1)
            b = T(ty, 14, c, BOLD).move_to(r.get_right() + LEFT * 0.2)
            pr.add(VGroup(r, a, b))
        VGroup(VGroup(*pr[:7]).arrange(DOWN, buff=0.08), VGroup(*pr[7:]).arrange(DOWN, buff=0.08)).arrange(RIGHT, buff=0.15)
        pr.move_to([-3.65, 0.7, 0])
        lg = VGroup(T("M: tek mesaj", 14, ACC, BOLD), T("T: bölünmez işlem", 14, ICTPC, BOLD)).arrange(RIGHT, buff=0.3).next_to(pr, DOWN, buff=0.12)
        hd = T("§18'in ICTP sözcükleri", 17, TXT, BOLD).move_to([3.6, 2.05, 0])
        nms = VGroup(*[VGroup(HX(s, 16, ICTPC, BOLD), T("✗ tabloda yok", 15, WARN, BOLD)).arrange(RIGHT, buff=0.25)
                       for s in ("Peering()", "Active()", "Standby-LOS()", "Standby-Clear()", "Unprotected()")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        nms.move_to([3.6, 0.75, 0])
        ph = VGroup(T("tablodaki prtHandshake():", 15, TXT, BOLD), T("ONU başına · UC6 kimlik doğrulamaya bağlı", 15, GOLD, BOLD)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        ph.move_to([3.6, -0.75, 0])
        nu = VGroup(T("ilkel yok:", 15, WARN, BOLD), tag("UC11 başarım izleme", MUTED, 14), tag("UC14 yük paylaşımı", MUTED, 14)).arrange(RIGHT, buff=0.12).move_to([3.4, -1.55, 0])
        e5 = VGroup(doc_card("Ek V · koruma örnekleri", ["“This appendix is intentionally empty.”"], GOLD, 5.6, 1.0, 17, 15), ed_chips(14, MUTED)).arrange(RIGHT, buff=0.3)
        fit(e5, 12.6).move_to([0, -2.6, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.05) for p in pr], lag_ratio=0.05), run_time=1.0)
        self.play(FadeIn(lg), run_time=0.3)
        self.at(self.cue("on dört tanedir", 4.3))
        self.play(Indicate(pr, color=ACC, scale_factor=1.02), run_time=0.5)
        self.at(self.cue("maddenin eşleşme", 5.6))
        self.play(FadeIn(hd), FadeIn(nms[0]), run_time=0.35)
        self.at(self.cue("etkin,", 8.5))
        self.play(FadeIn(nms[1]), run_time=0.25)
        self.at(self.cue("bekleme ve korumasız", 9.0))
        self.play(FadeIn(nms[2:]), run_time=0.35)
        self.at(self.cue("tablodaki koruma el sıkışması", 12.9))
        self.play(Indicate(pr[3], color=GOLD, scale_factor=1.08), FadeIn(ph, shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("Sayaç ve yük paylaşımının", 19.2))
        self.play(FadeIn(nu, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Beşinci ek", 22.8))
        self.play(FadeIn(e5[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("kasıtlı olarak boştur", 25.5))
        self.play(FadeIn(e5[1], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        self.note11("c11", [("1", "ONU tarafı korumanın her değerini yapılandırma belgenize yazın",
                             "TO2 … TO5, TPST ve yeniden iletim zaman aşımı;\nkoruma kanalının burst profilini de önceden ulaştırın.", "ONU tarafı korumanın"),
                            ("2", "İki üreticinin sonlandırıcıları eş olacaksa",
                             "Mesaj adlarını standarttan değil,\nuyguladıkları ICTP sürümünden (BBF TR-352) doğrulayın.", "İki:")])
        self.bridge_beat("c12", "Kendi ONU'larımızı kurtardık.\nPeki kurallara uymayan bir ONU'yla ne yapacağız?")
        self.save_timeline("ep20_p2C")
