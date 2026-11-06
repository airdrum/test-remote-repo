"""B02 — 'Bu bölümde' opening + 'Önceki bölümde' recap with answers to B01 quiz."""
from kit import *

EP = SERIES["episodes"][1]
AGENDA = ["ODN'in anatomisi", "Yol kaybı sınıfları ve bütçe", "Mesafe, dispersiyon, yansıma", "TC köprüsü: ranging ve EqD", "Referans test ODN'i"]
PX, PY = 3.4, -0.45


def segments_teaser():
    y = PY + 0.2
    ct = VGroup(*[box(0.9, 0.36, f"CT{i + 1}", CH[i], 13).move_to([PX - 3.0, y + 0.75 - i * 0.5, 0]) for i in range(4)])
    wm = box(0.45, 2.0, "WM", "#3B4A75", 13).move_to([PX - 1.95, y, 0])
    att = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=GOLD, stroke_width=3) for c in ct])
    sp = splitter(0.25).move_to([PX + 1.2, y, 0])
    feed = Line(wm.get_right(), sp.get_left(), color=ACC, stroke_width=5)
    onus = VGroup(*[box(0.8, 0.34, "ONU", "#94A3B8", 12).move_to([PX + 2.9, y + 0.9 - i * 0.6, 0]) for i in range(4)])
    dist = VGroup(*[Line(sp.get_right(), o.get_left(), color=PINK, stroke_width=2.5) for o in onus])
    labs = VGroup(T("kanal bağlantı", 15, GOLD, BOLD).next_to(att, DOWN, buff=0.9).shift(LEFT * 0.4),
                  T("besleme", 15, ACC, BOLD).next_to(feed, DOWN, buff=0.2),
                  T("dağıtım", 15, PINK, BOLD).next_to(dist, DOWN, buff=0.35))
    return VGroup(ct, wm, att, feed, sp, dist, onus, labs)


class Ep02Open(Narrated):
    MANIFEST = "build/ep02/open/audio_proc/manifest.json"

    def construct(self):
        self.beat("o1")
        tag = T(f"BÖLÜM {EP['n']} · {EP['title'].upper()}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 23, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=7.0, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([PX, PY, 0])
        self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        num = T(f"{EP['n']:02d}", 120, ACC, BOLD)
        sub = T(EP["sub"], 24, TXT, SEMIBOLD)
        refs = T(EP["refs"], 16, MUTED, MEDIUM)
        for m in (sub, refs):
            if m.width > 6.2:
                m.scale_to_fit_width(6.2)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.3).move_to([PX, PY, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        self.end(pad=0.05)
        self.items, self.cur = items, cover

        # o2 — ODN anatomy
        self.beat("o2")
        t = segments_teaser()
        self.focus(0, t)
        self.play(FadeIn(t[0]), FadeIn(t[1]), Create(t[2]), run_time=0.8)
        self.play(Create(t[3]), FadeIn(t[4]), Create(t[5]), FadeIn(t[6]), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(l) for l in t[7]], lag_ratio=0.3), run_time=1.0)
        self.end(pad=0.05)

        # o3 — classes and budget equation
        self.beat("o3")
        sc = 0.17
        x0 = PX - 3.0
        bars = VGroup()
        for i, (nm, lo, c) in enumerate([("N1", 14, CH[0]), ("N2", 16, CH[1]), ("E1", 18, CH[2]), ("E2", 20, CH[3])]):
            r = Rectangle(width=15 * sc * 2, height=0.36, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x0 + (lo - 10 + 7.5) * sc * 2, PY + 1.6 - 0.5 * i, 0])
            bars.add(VGroup(r, T(f"{nm} {lo}–{lo + 15} dB", 15, BG, BOLD).move_to(r)))
        eq = T("P_min − S  ≥  OPL_maks + OPP", 30, GOLD, BOLD).move_to([PX, PY - 1.3, 0])
        self.focus(1, VGroup(bars, eq))
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.2), run_time=1.2)
        self.at(self.cues[1] if len(self.cues) > 1 else 2.0)
        self.play(Write(eq), run_time=1.2)
        self.end(pad=0.05)

        # o4 — distance, dispersion, reflection
        self.beat("o4")
        fib = Line([PX - 3.0, PY + 0.4, 0], [PX + 3.0, PY + 0.4, 0], color=FEED, stroke_width=5)
        cons = VGroup(*[Rectangle(width=0.18, height=0.45, stroke_width=2, color=GOLD, fill_color=BG, fill_opacity=1).move_to([x, PY + 0.4, 0]) for x in (PX - 1.5, PX + 0.2, PX + 1.8)])
        refl = VGroup(*[Arrow([c.get_x(), PY + 0.75, 0], [c.get_x() - 0.9, PY + 0.75, 0], buff=0, color=WARN, stroke_width=2.5, max_tip_length_to_length_ratio=0.25) for c in cons])
        lim = VGroup(pill("ORL ≥ 32 dB", ACC, 18), pill("ayrık yansıma < −35 dB", WARN, 18), pill("DD20 / DD40", GOLD, 18)).arrange(DOWN, buff=0.18).move_to([PX, PY - 1.3, 0])
        self.focus(2, VGroup(fib, cons, refl, lim))
        self.play(Create(fib), FadeIn(cons), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in refl], lag_ratio=0.3), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in lim], lag_ratio=0.3), run_time=1.0)
        self.end(pad=0.05)

        # o5 — timing
        self.beat("o5")
        y = PY + 0.2
        tl = Line([PX - 3.1, y, 0], [PX + 3.1, y, 0], color=MUTED, stroke_width=2)
        bursts = VGroup(*[Rectangle(width=0.55, height=0.4, stroke_width=0, fill_color=CH[i % 4], fill_opacity=0.9).move_to([PX - 2.6 + 0.7 * i, y + 0.3, 0]) for i in range(3)],
                        *[Rectangle(width=0.55, height=0.4, stroke_width=0, fill_color=CH[i % 4], fill_opacity=0.9).move_to([PX + 1.2 + 0.7 * i, y + 0.3, 0]) for i in range(3)])
        qw = Rectangle(width=2.4, height=0.9, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.12).move_to([PX - 0.65 + 0.4, y + 0.35, 0])
        qt = T("sessiz pencere", 16, GOLD, BOLD).next_to(qw, UP, buff=0.08)
        f = VGroup(T("EqDᵢ = T_eqd − RTDᵢ", 26, ACC, BOLD), T("20 km → 250 µs · 40 km → 450 µs", 18, MUTED)).arrange(DOWN, buff=0.15).move_to([PX, PY - 1.4, 0])
        self.focus(3, VGroup(tl, bursts, qw, qt, f))
        self.play(Create(tl), LaggedStart(*[FadeIn(b) for b in bursts], lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(qw), FadeIn(qt), run_time=0.6)
        self.play(FadeIn(f, shift=UP * 0.1), run_time=0.8)
        self.end(pad=0.05)

        # o6 — lab chain
        self.beat("o6")
        names = ["CT+WM", "kuplör", "VOA", "makara", "ayırıcı", "ONU"]
        chain = VGroup(*[box(1.0, 0.55, n, c, 13) for n, c in zip(names, [GOLD, MUTED, MUTED, CH[1], FEED, "#94A3B8"])]).arrange(RIGHT, buff=0.18).move_to([PX, PY + 0.3, 0])
        lines = VGroup(*[Line(a.get_right(), b.get_left(), color=FEED, stroke_width=2.5) for a, b in zip(chain[:-1], chain[1:])])
        cap = T("referans test ODN'i", 22, GOOD, BOLD).next_to(chain, DOWN, buff=0.5)
        self.focus(4, VGroup(chain, lines, cap))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chain], lag_ratio=0.15), Create(lines), run_time=1.4)
        self.play(FadeIn(cap), run_time=0.5)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep02_open")

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


class Ep02Recap(Act):
    HDR, MANIFEST, FIRST = "BÖLÜM 2 · ÖNCEKİ BÖLÜMDE", "build/ep02/recap/audio_proc/manifest.json", True

    def construct(self):
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Bölüm 1 · Işığa Dönüş")
        self.at(1.2)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["PON'un üç problemi: bölünen güç, yayın, sıralı burst'ler", "NG-PON2: hız değil renk — TWDM + PtP WDM",
               "G.989 ailesi: PMD ↔ TC sınırı, 125 µs çerçeve", "Referans noktaları: S/R-CG (birincil) ve S/R-CP (alternatif)"]
        items = VGroup(*[VGroup(T("✓", 26, GOOD, BOLD), T(s, 23, TXT)).arrange(RIGHT, buff=0.3) for s in pts]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.35), run_time=2.6)
        self.end(pad=0.05)
        self.clear()
        qa = [("Soru 1", "PMD tabloları hangi referans noktasına göre yazılmıştır?", "S/R-CG — WM çıkışındaki kanal grubu noktası.\nS/R-CP: CG erişilemezse ya da transceiver için\nWM'den bağımsız şartname gerekirse.", CH[0], "a2"),
              ("Soru 2", "10G NG-PON2 alıcısının hassasiyeti hangi BER'de?", "FEC öncesi BER = 10⁻³", CH[1], "a3"),
              ("Soru 3", "64 ONU'lu kanalda kapalı vericilerin sızıntısı?", "63 girişimci → 10·log₁₀63 ≈ +18 dB\nWNE-PSD limiti de 63 girişimciyle hesaplanmış\n(G.989.2 Tablo 11-6, Not 9)", CH[3], "a4")]
        prev = None
        for title, q, a, c, bid in qa:
            self.beat(bid)
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.4)
            qt = VGroup(T(title, 26, c, BOLD), T(q, 28, TXT, SEMIBOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.2).to_edge(LEFT, buff=1.0)
            ans = RoundedRectangle(corner_radius=0.18, width=11.5, height=2.3, stroke_color=GOOD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(DOWN * 1.3)
            at = VGroup(T("Cevap", 20, GOOD, BOLD), T(a, 24, TXT, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ans).align_to(ans, LEFT).shift(RIGHT * 0.4)
            self.play(FadeIn(qt, shift=RIGHT * 0.2), run_time=0.6)
            self.at(max(1.0, self.cues[1] - 0.2) if len(self.cues) > 1 else 1.0)
            self.play(FadeIn(ans), FadeIn(at, shift=UP * 0.1), run_time=0.7)
            prev = VGroup(qt, ans, at)
            self.end(pad=0.1)
        self.play(FadeOut(prev), FadeOut(self.badge), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep02_recap")
