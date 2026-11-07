"""S2·B2 · Perde 3 (↓ FS çerçevesi, BWmap — G.989.3 §8.1.1, Tablo 6-5) and Perde 4 (↑ burst — §8.1.2, §10.1.2, Ek III)."""
from ep12_common import *

TIMC, FWIC, PRFC = "#60A5FA", PINK, "#C084FC"
ALLOC = [("Alloc-ID", 14, ACC), ("DBRu", 1, GOLD), ("PLOAMu", 1, GOLD), ("StartTime", 16, TIMC), ("GrantSize", 16, TIMC),
         ("FWI", 1, FWIC), ("Profil", 2, PRFC), ("HEC", 13, HECC)]


def fs_bar(y, h=0.6, size=16, x0=-6.0):
    return strip([(1.0, "HLend", HLC, 0.3), (2.2, "BWmap · 8N", BWC, 0.3), (2.0, "PLOAMd · 48P", PLDC, 0.25),
                  (5.7, "yük (XGEM çerçeveleri)", PAYC, 0.12), (0.9, "BIP", BIPC, 0.35)], x0, y, h, size)


def mini_burst(x0, w, y, frac, color=TW_US, h=0.42):
    """Expected burst (dashed outline) and what is actually sent (filled fraction)."""
    exp = DashedVMobject(Rectangle(width=w, height=h, stroke_color=MUTED, stroke_width=1.8), num_dashes=24).move_to([x0 + w / 2, y, 0])
    g = VGroup(exp)
    if frac > 0:
        g.add(Rectangle(width=w * frac, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.45).move_to([x0 + w * frac / 2, y, 0]))
    else:
        g.add(T("burst yok", 15, WARN, BOLD).move_to(exp))
    return g


# ================================ PERDE 3 ======================================
class E12P3A(Act12):
    HDR, MANIFEST, FIRST = H12[3], M12("p3"), True

    def construct(self):
        # d1 — FS frame sizes and parts
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Aşağı yön çerçevesi")
        self.at(self.cue("FEC kapalıyken on gigabitte", 4.5))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("↓ FS çerçevesi — Tablo 8-1")
        tb = mtable(["", "10G · 9,95328 Gbit/s", "2,5G · 2,48832 Gbit/s"],
                    [["PHY çerçevesi (125 µs)", "155 520 B", "38 880 B"], ["FS çerçevesi · FEC kapalı", "155 496 B", "38 856 B"], ["FS çerçevesi · FEC açık", "135 432 B", "36 344 B"]],
                    [4.4, 3.4, 3.4], size=21, hsize=17, row_h=0.58).move_to([0, 1.35, 0])
        for r in tb[1:]:
            r[2].set_color(R10)
            r[3].set_color(R25)
        fs = fs_bar(-1.5)
        braces = VGroup(brace_lbl(fs[:3], "başlık", MUTED, UP, 17), brace_lbl(fs[3], "yük", MUTED, UP, 17), brace_lbl(fs[4], "kuyruk", MUTED, UP, 17))
        fixed = T("sabit 4 B", 16, HLC, BOLD).next_to(fs[0], DOWN, buff=0.12)
        var = brace_lbl(fs[1:3], "iki değişken bölme", GOLD, DOWN, 17)
        self.play(FadeIn(tb[0]), FadeIn(tb[1]), self.set_src("G.989.3 §8.1.1 · Tablo 8-1 · Şekil 8-1"), run_time=0.5)
        self.play(FadeIn(tb[2], shift=UP * 0.08), run_time=0.4)
        self.play(Indicate(tb[2][2], color=GOLD), run_time=0.5)
        self.at(self.cue("FEC açıkken yüz otuz beş", 10.0))
        self.play(FadeIn(tb[3], shift=UP * 0.08), run_time=0.4)
        self.play(Indicate(tb[3][2], color=GOLD), run_time=0.5)
        self.at(self.cue("Üç bölümden oluşur", 14.6))
        self.play(LaggedStart(*[FadeIn(s) for s in fs], lag_ratio=0.12), run_time=0.7)
        self.at(self.cue("başlık", 16.2))
        self.play(FadeIn(braces[0]), run_time=0.3)
        self.at(self.cue("yük ve kuyruk", 16.8))
        self.play(FadeIn(braces[1]), FadeIn(braces[2]), run_time=0.4)
        self.at(self.cue("sabit dört baytlık", 19.0))
        self.play(FadeIn(fixed, shift=UP * 0.08), Indicate(fs[0], color=GOLD), run_time=0.5)
        self.at(self.cue("bant genişliği haritası ve aşağı yön PLOAM", 23.8))
        self.play(FadeIn(var), Indicate(VGroup(fs[1], fs[2]), color=GOLD, scale_factor=1.04), run_time=0.6)
        self.end(pad=0.05)

        # d2 — HLend
        self.beat("d2")
        self.clear(h)
        h = self.show_heading("HLend — 4 bayt, en önde", h)
        fs = fs_bar(1.95, 0.5, 15)
        hl = fields([("BWmap uzunluğu (N)", 11, BWC), ("PLOAM sayısı (P)", 8, PLDC), ("HEC", 13, HECC)], 10.0, 0.62, 18, 14, unit=" bit").move_to([0.4, 0.55, 0])
        zl = zoom_lines(fs[0], hl, HLC)
        f1 = VGroup(T("BWmap =", 24, BWC, BOLD), T("8 × N bayt", 24, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([-3.2, -0.85, 0])
        f2 = VGroup(T("PLOAMd =", 24, PLDC, BOLD), T("48 × P bayt", 24, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([2.6, -0.85, 0])
        a1 = arrow(hl[0][0].get_bottom() + DOWN * 0.3, f1.get_top() + UP * 0.05, BWC, 2, 0.1)
        a2 = arrow(hl[1][0].get_bottom() + DOWN * 0.3, f2.get_top() + UP * 0.05, PLDC, 2, 0.1)
        hec = T("13 bitlik HEC: 31 bitlik alanın üstünde (32 bit biçimi)", 16, MUTED, BOLD).next_to(hl, RIGHT, buff=0.15)
        bip = VGroup(tag("kuyruk", BIPC, 18), T("BIP-32 · 4 bayt · bütün FS çerçevesi üzerinden", 20, TXT)).arrange(RIGHT, buff=0.25).move_to([0, -2.35, 0])
        ba = CurvedArrow(bip.get_right() + RIGHT * 0.1, fs[4].get_bottom() + DOWN * 0.05, angle=0.9, color=BIPC, stroke_width=2, tip_length=0.12)
        self.play(FadeIn(fs), self.set_src("G.989.3 §8.1.1.1 · §8.1.1.5 · Şekil 8-1"), run_time=0.5)
        self.at(self.cue("on bir bitlik bir harita", 1.8))
        self.play(Create(zl), FadeIn(hl[0]), run_time=0.6)
        self.at(self.cue("sekiz bitlik bir PLOAM", 4.6))
        self.play(FadeIn(hl[1], shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("on üç bitlik HEC", 6.8))
        self.play(FadeIn(hl[2], shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("Harita uzunluğu N ise", 8.8))
        self.play(GrowArrow(a1), FadeIn(f1, shift=UP * 0.08), Indicate(fs[1], color=BWC), run_time=0.6)
        self.at(self.cue("PLOAM sayısı P ise", 13.0))
        self.play(GrowArrow(a2), FadeIn(f2, shift=UP * 0.08), Indicate(fs[2], color=PLDC), run_time=0.6)
        self.at(self.cue("Kuyruk ise bütün çerçeve", 18.0))
        self.play(FadeIn(bip, shift=UP * 0.08), Create(ba), run_time=0.6)
        self.end(pad=0.05)

        # d3 — allocation structure, 64 bits
        self.beat("d3")
        self.clear(h)
        h = self.show_heading("BWmap tahsis yapısı — 8 bayt", h)
        al = fields(ALLOC, 12.4, 0.62, 17, 14, unit="").move_to([0, 1.65, 0])
        rows = [("Alloc-ID · 14", ACC, "alıcı: T-CONT ya da ↑ OMCC"), ("DBRu · 1", GOLD, "bu tahsiste durum raporu iste"),
                ("PLOAMu · 1", GOLD, "burst başlığında PLOAM iste"), ("StartTime · 16", TIMC, "burst'ün başlangıç anı"),
                ("GrantSize · 16", TIMC, "tahsis boyu"), ("FWI · 1", FWIC, "zorunlu uyandırma"),
                ("Profil · 2", PRFC, "burst profili indeksi (0 – 3)"), ("HEC · 13", HECC, "Ek A · 64 bit biçimi")]
        colL = num_rows(rows[:4], size=18, gap=0.55)
        colR = num_rows(rows[4:], size=18, gap=0.55)
        colL.move_to([-6.3, -0.75, 0], aligned_edge=LEFT)
        colR.move_to([0.6, -0.75, 0], aligned_edge=LEFT)
        allr = VGroup(*colL, *colR)
        pl = pill("yukarı yönün bütün zamanlaması bu 64 bitte", GOLD, 19).move_to([0, -2.75, 0])
        self.play(self.set_src("G.989.3 §8.1.1.2 · Şekil 8-2"), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in al], lag_ratio=0.08), run_time=1.0)
        self.at(self.cue("bütün zamanlaması bu altmış dört", 4.8))
        self.play(FadeIn(pl, shift=UP * 0.08), run_time=0.5)
        keys = (("On dört bitlik tahsis kimliği", 10.2), ("biri o tahsiste", 15.4), ("diğeri burst başlığında", 18.7),
                ("on altı bitlik başlangıç zamanı", 22.7), ("on altı bitlik tahsis boyu", 25.5), ("Bir bit zorunlu uyandırma", 28.4),
                ("iki bit burst profili", 30.6), ("on üç bitlik HEC", 33.1))
        for k, (key, d) in enumerate(keys):
            self.at(self.cue(key, d))
            self.play(FadeIn(allr[k], shift=RIGHT * 0.08), Indicate(al[k][0], color=WHITE, scale_factor=1.08), run_time=0.45)
        self.end(pad=0.05)

        # d4 — Alloc-ID value ranges
        self.beat("d4")
        self.clear(h)
        h = self.show_heading("Alloc-ID değer aralıkları — Tablo 6-5", h)
        rb = range_bar([("varsayılan = ONU-ID", "0", "1020", ACC, 4.0), ("SN", "1021", None, GOLD, 1.05), ("SN 10G", "1022", None, R10, 1.35),
                        ("SN 2,5G", "1023", None, R25, 1.35), ("açıkça atanan", "1024", "16383", SAC, 4.2)], 12.4, 0.7, 17, 15).move_to([0, 1.5, 0])
        e0 = VGroup(T("Alloc-ID = ONU-ID", 19, ACC, BOLD), T("örn. ONU-ID 19 → Alloc-ID 19", 16, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-4.3, 0.15, 0])
        sn = VGroup(VGroup(tag("1021", GOLD, 17), T("SN tahsisi · her hızdan ONU", 18, TXT)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("1022", R10, 17), T("SN tahsisi · yalnız 10G ↑ ONU", 18, TXT)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("1023", R25, 17), T("SN tahsisi · yalnız 2,5G ↑ ONU", 18, TXT)).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0.2, -1.05, 0])
        e4 = VGroup(T("Assign_Alloc-ID ile", 19, SAC, BOLD), T("T-CONT'lar, çekişmeli işlevler", 16, MUTED)).arrange(DOWN, aligned_edge=RIGHT, buff=0.06).move_to([4.4, 0.15, 0])
        leads = VGroup(*[DashedLine(rb[i][0].get_bottom() + DOWN * 0.35, sn[i - 1][0].get_top() + UP * 0.05, color=c, stroke_width=1.5, dash_length=0.07)
                         for i, c in ((1, GOLD), (2, R10), (3, R25))])
        dual = pill("1022 / 1023: çift hızlı kanalda SN tahsisi hıza göre ayrılır", GOLD, 18).move_to([0, -2.75, 0])
        self.play(self.set_src("G.989.3 Tablo 6-5 · §6.1.5.6 · §8.1.1.2.1"), run_time=0.3)
        self.at(self.cue("Sıfırdan bin yirmiye", 3.6))
        self.play(FadeIn(rb[0]), run_time=0.5)
        self.at(self.cue("ONU kimliğine eşit", 7.0))
        self.play(FadeIn(e0, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("Bin yirmi bir", 11.0))
        self.play(FadeIn(rb[1]), run_time=0.4)
        self.at(self.cue("her hızdan ONU'ya açık", 12.2))
        self.play(Create(leads[0]), FadeIn(sn[0], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("bin yirmi iki yalnızca", 16.6))
        self.play(FadeIn(rb[2]), Create(leads[1]), FadeIn(sn[1], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("bin yirmi üç yalnızca", 19.4))
        self.play(FadeIn(rb[3]), Create(leads[2]), FadeIn(sn[2], shift=RIGHT * 0.08), run_time=0.5)
        self.play(FadeIn(dual, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("Bin yirmi dörtten itibaren", 25.1))
        self.play(FadeIn(rb[4]), FadeIn(e4, shift=UP * 0.08), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p3A")


class E12P3B(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[3], M12("p3"), "std"

    def construct(self):
        # d5 — the time quantum
        self.beat("d5")
        self.set_badge("neden")
        h = self.show_heading("Zaman kuantumu — tek birim, iki hız")
        y0 = 1.85
        bar = Rectangle(width=12.0, height=0.5, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([0, y0, 0])
        tk = VGroup(*[Line([-6 + i * 0.2, y0 - 0.25, 0], [-6 + i * 0.2, y0 - 0.1, 0], color=MUTED, stroke_width=1) for i in range(1, 60)])
        bl = T("125 µs = 9720 zaman kuantumu (TQ)", 18, TXT, BOLD).move_to(bar)
        first = Rectangle(width=0.2, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=0.7).move_to([-5.9, y0, 0])
        qx0, qw = -6.0, 1.62
        tqs = VGroup(*[Rectangle(width=qw, height=0.5, stroke_color=ACC, stroke_width=2, fill_color=ACC, fill_opacity=0.12).move_to([qx0 + qw * (i + 0.5), 0.75, 0]) for i in range(6)])
        tql = VGroup(*[T(f"TQ {i}", 15, ACC, BOLD).move_to(r) for i, r in enumerate(tqs)])
        zl = VGroup(DashedLine(first.get_corner(DL), tqs.get_corner(UL), color=ACC, stroke_width=1.5), DashedLine(first.get_corner(DR), tqs.get_corner(UR), color=ACC, stroke_width=1.5))
        tqv = T("1 TQ = 125 µs / 9720 = 12,86 ns", 22, ACC, BOLD).move_to([-1.15, 0.05, 0])

        def byterow(n, y, color):
            cw = qw / n
            g = VGroup()
            for i in range(6):
                for j in range(n):
                    g.add(Rectangle(width=cw, height=0.36, stroke_color=color, stroke_width=1, fill_color=color, fill_opacity=0.35 if (i + j) % 2 else 0.18)
                          .move_to([qx0 + qw * i + cw * (j + 0.5), y, 0]))
            return g
        r25 = byterow(4, -0.75, R25)
        r10 = byterow(16, -1.4, R10)
        l25 = T("2,5G: 4 B / TQ", 17, R25, BOLD).next_to(r25, RIGHT, buff=0.2)
        l10 = T("10G: 16 B / TQ", 17, R10, BOLD).next_to(r10, RIGHT, buff=0.2)
        unit = VGroup(tag("StartTime", TIMC, 17), tag("GrantSize", TIMC, 17), T("→ hıza göre değişmeyen birim", 17, TXT, BOLD)).arrange(RIGHT, buff=0.18).move_to([-3.1, -2.5, 0])
        one = pill("tek BWmap → 2,5G ve 10G ONU'lar aynı ızgarada", GOLD, 18).move_to([3.4, -2.5, 0])
        self.play(self.set_src("G.989.3 §8.1.1.2.3–4 · §13.1 (32 bit @ 2,48832 Gbit/s)"), run_time=0.3)
        self.at(self.cue("Başlangıç zamanı ve tahsis boyu", 3.8))
        self.play(FadeIn(unit[:2], shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("hıza göre değişmeyen", 6.5))
        self.play(FadeIn(unit[2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("bir zaman kuantumu", 9.9))
        self.play(FadeIn(bar), FadeIn(tk), run_time=0.5)
        self.at(self.cue("dokuz bin yedi yüz yirmide", 11.5))
        self.play(FadeIn(bl), run_time=0.4)
        self.play(FadeIn(first), Create(zl), LaggedStart(*[FadeIn(t) for t in tqs], lag_ratio=0.1), FadeIn(tql), run_time=0.9)
        self.at(self.cue("on iki virgül sekiz altı", 17.1))
        self.play(FadeIn(tqv, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("iki buçuk gigabitte dört bayt", 20.1))
        self.play(LaggedStart(*[FadeIn(c) for c in r25], lag_ratio=0.01), FadeIn(l25), run_time=0.7)
        self.at(self.cue("on gigabitte on altı bayttır", 23.3))
        self.play(LaggedStart(*[FadeIn(c) for c in r10], lag_ratio=0.004), FadeIn(l10), run_time=0.8)
        self.at(self.cue("tek bir harita", 25.7))
        self.play(FadeIn(one, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("aynı kanalda iki buçuk", 27.6))
        self.play(Indicate(VGroup(r25, l25), color=R25, scale_factor=1.02), Indicate(VGroup(r10, l10), color=R10, scale_factor=1.02), run_time=0.9)
        self.end(pad=0.05)

        # d5a — StartTime points at the FS header; GrantSize content; zero-size grants
        self.beat("d5a")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("StartTime nereyi gösterir?", h)
        y = 0.75
        xb = -1.8
        prev = Rectangle(width=xb + 6.4, height=1.25, stroke_width=0, fill_color=MUTED, fill_opacity=0.08).move_to([(-6.4 + xb) / 2, y, 0])
        prl = T("çerçeve N − 1", 15, MUTED, BOLD).move_to([-5.5, y + 0.85, 0])
        nl = T("çerçeve N", 15, ACC, BOLD).move_to([xb + 0.8, y + 0.85, 0])
        bd = DashedLine([xb, y - 0.75, 0], [xb, y + 1.05, 0], color=ACC, stroke_width=2.5)
        gt = seg(-3.8, 0.5, y, MUTED, None, 0.55, 0.05, dashed=True)
        bu = strip([(0.9, "önsöz", PHC, 0.3), (0.6, "sın.", PHC, 0.65), (0.8, "başlık", HLC, 0.3), (0.75, "DBRu", BWC, 0.3),
                    (3.6, "yük", PAYC, 0.15), (0.6, "BIP", BIPC, 0.3)], -3.3, y, 0.55, 15)
        st = VGroup(Arrow([xb, y + 1.6, 0], [xb, y + 0.32, 0], buff=0, color=TIMC, stroke_width=3, tip_length=0.15, max_tip_length_to_length_ratio=0.2),
                    T("StartTime → FS başlığının ilk baytı", 17, TIMC, BOLD).move_to([xb + 2.6, y + 1.55, 0]))
        rng_ = tag("StartTime: 0 … 9719", TIMC, 17).move_to([4.9, y + 1.55, 0])
        psl = T("PSBu önceki çerçeveye taşabilir", 16, PHC, BOLD).next_to(bu[:2], DOWN, buff=0.15).align_to(bu[1], RIGHT).shift(LEFT * 0.15)
        gs = BraceBetweenPoints(bu[3].get_corner(DL), bu[4].get_corner(DR), DOWN, color=TIMC)
        gsl = T("GrantSize = DBRu + yük", 17, TIMC, BOLD).next_to(gs, DOWN, buff=0.05)
        nx = VGroup(xmark(bu[2][0], WARN, 3, 0.0), xmark(bu[5][0], WARN, 3, 0.0))
        nxl = T("sayılmaz: başlık · kuyruk · FEC", 16, WARN, BOLD).move_to([4.65, y - 0.98, 0])
        y2 = -2.15
        zg = strip([(0.9, "önsöz", PHC, 0.3), (0.6, "sın.", PHC, 0.65), (0.8, "başlık", HLC, 0.3), (2.4, "PLOAMu · 48 B", PLDC, 0.25), (0.6, "BIP", BIPC, 0.3)], -6.2, y2, 0.55, 15)
        zgl = VGroup(T("GrantSize = 0 → yalnızca PLOAM", 19, GOLD, BOLD), T("seri numarası ve mesafe ölçümü tahsisleri", 16, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(zg, RIGHT, buff=0.35)
        self.play(self.set_src("G.989.3 §8.1.1.2.3–4 · Şekil 8-3 · §10.1.2"), run_time=0.3)
        self.at(self.cue("sıfırdan dokuz bin yedi yüz on dokuza", 1.0))
        self.play(FadeIn(prev), FadeIn(prl), FadeIn(nl), Create(bd), FadeIn(rng_, shift=LEFT * 0.08), run_time=0.7)
        self.at(self.cue("burst'ün önsözünü değil", 5.4))
        self.play(FadeIn(gt), FadeIn(bu), run_time=0.6)
        self.at(self.cue("çerçeveleme başlığının ilk baytını", 7.6))
        self.play(GrowArrow(st[0]), FadeIn(st[1]), Indicate(bu[2], color=TIMC), run_time=0.7)
        self.at(self.cue("önceki çerçeveye taşabilir", 11.3))
        self.play(FadeIn(psl, shift=UP * 0.08), Indicate(VGroup(bu[0], bu[1]), color=GOLD, scale_factor=1.05), run_time=0.7)
        self.at(self.cue("Tahsis boyu ise yükü", 16.1))
        self.play(FadeIn(gs), FadeIn(gsl), run_time=0.5)
        self.at(self.cue("kuyruğu ve FEC'i saymaz", 20.5))
        self.play(Create(nx), FadeIn(nxl), run_time=0.5)
        self.at(self.cue("Sıfır boyutlu bir tahsis", 22.5))
        self.play(FadeIn(zg, shift=RIGHT * 0.08), FadeIn(zgl[0]), run_time=0.6)
        self.at(self.cue("seri numarası ve mesafe", 26.4))
        self.play(FadeIn(zgl[1]), run_time=0.4)
        self.end(pad=0.05)

        # d6 — the 11 BWmap rules
        self.beat("d6")
        self.clear(h)
        h = self.show_heading("BWmap'in 11 kuralı — §8.1.1.3", h)
        rules = ["seriler artan StartTime ile", "burst aralıkları: §10.1.2", "en küçük StartTime = 0", "en büyük StartTime = 9719",
                 "BWmap başına ≤ 512 yapı", "seri başına ≤ 16 yapı", "ONU başına ≤ 64 yapı", "ONU başına ≤ 16 seri",
                 "GrantSize ≤ 9718 (2,5G) / 9719 (10G)", "FS burst ≤ 38 880 B / 155 520 B", "StartTime + Σ GrantSize ≤ 14 580"]
        rl = VGroup(*[VGroup(T(f"{i + 1}", 17, ACC, BOLD), T(s, 17, TXT, MEDIUM)).arrange(RIGHT, buff=0.2) for i, s in enumerate(rules)])
        rl.arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([-6.4, -0.2, 0], aligned_edge=LEFT)
        for r in rl:
            r[1].set_x(rl.get_left()[0] + 0.45 + r[1].width / 2)
        rl.set_opacity(0.35)
        stats = VGroup()
        for big, sm_, c in (("512", "yapı / BWmap", BWC), ("16", "yapı / seri", BWC), ("64", "yapı / ONU", GOLD), ("16", "seri / ONU", GOLD)):
            r = RoundedRectangle(corner_radius=0.12, width=2.7, height=1.05, stroke_color=c, stroke_width=2, fill_color=PANEL, fill_opacity=1)
            stats.add(VGroup(r, VGroup(T(big, 32, c, BOLD), T(sm_, 15, TXT, BOLD)).arrange(DOWN, buff=0.04).move_to(r)))
        stats.arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.2)).move_to([3.6, 1.15, 0])
        ax0, ax1, ay = 0.7, 6.4, -1.55
        X = lambda v: ax0 + v / 14580 * (ax1 - ax0)
        fN = Rectangle(width=X(9720) - X(0), height=0.5, stroke_color=ACC, stroke_width=2, fill_color=ACC, fill_opacity=0.1).move_to([(X(0) + X(9720)) / 2, ay, 0])
        fN1 = Rectangle(width=X(14580) - X(9720), height=0.5, stroke_color=MUTED, stroke_width=2, fill_color=MUTED, fill_opacity=0.1).move_to([(X(9720) + X(14580)) / 2, ay, 0])
        fl = VGroup(T("çerçeve N", 15, ACC, BOLD).move_to(fN), T("N + 1 · yarısı", 15, MUTED, BOLD).move_to(fN1))
        tv = VGroup(*[T(s, 15, MUTED, BOLD).next_to([X(v), ay - 0.25, 0], DOWN, buff=0.08) for v, s in ((0, "0"), (9720, "9720"), (14580, "14 580"))])
        tv[0].shift(RIGHT * 0.05)
        tv[2].shift(LEFT * 0.2)
        bst = Rectangle(width=X(14580) - X(7400), height=0.3, stroke_color=TW_US, stroke_width=2, fill_color=TW_US, fill_opacity=0.5).move_to([(X(7400) + X(14580)) / 2, ay + 0.48, 0])
        lim = DashedLine([X(14580), ay - 0.3, 0], [X(14580), ay + 0.75, 0], color=WARN, stroke_width=3)
        f11 = T("14 580 = 1,5 × 9720", 18, WARN, BOLD).move_to([3.55, ay + 1.0, 0])
        hf = T("→ en çok yarım çerçeve · 62,5 µs taşar", 18, GOLD, BOLD).move_to([3.55, ay - 1.05, 0])
        self.play(FadeIn(rl), self.set_src("G.989.3 §8.1.1.3 · 14 580 = 1,5 × 9720 (hesaplanmıştır)"), run_time=0.6)
        self.at(self.cue("Seriler artan başlangıç", 2.6))
        self.play(rl[0].animate.set_opacity(1), run_time=0.4)
        for i, (key, d, idx) in enumerate((("beş yüz on iki tahsis", 6.1, (4,)), ("bir seride en çok", 10.2, (5,)), ("bir ONU için en çok", 12.4, (6, 7)))):
            self.at(self.cue(key, d))
            anims = [rl[j].animate.set_opacity(1) for j in idx]
            sti = (0,) if i == 0 else ((1,) if i == 1 else (2, 3))
            self.play(*anims, *[FadeIn(stats[j], scale=0.9) for j in sti], run_time=0.5)
        self.at(self.cue("on dört bin beş yüz sekseni", 17.6))
        self.play(rl[10].animate.set_opacity(1), FadeIn(fN), FadeIn(fN1), FadeIn(fl), FadeIn(tv), Create(lim), FadeIn(f11), run_time=0.8)
        self.at(self.cue("bir sonraki çerçeveye en çok yarım", 25.5))
        self.play(GrowFromEdge(bst, LEFT), run_time=0.7)
        self.at(self.cue("altmış iki virgül beş", 29.1))
        self.play(FadeIn(hf, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # d6a — why 9718 vs 9719
        self.beat("d6a")
        self.clear(h)
        self.set_badge("neden")
        h = self.show_heading("Neden 9718 ve 9719?", h)
        x0, W = -4.6, 10.8
        r25 = strip([(0.6, "4 B", HLC, 0.35), (W - 1.2, "GrantSize ≤ 9718 TQ × 4 B", R25, 0.15), (0.6, "4 B", BIPC, 0.35)], x0, 1.25, 0.6, 15)
        r10 = strip([(0.6, "8 B", HLC, 0.35), (W - 0.6, "GrantSize ≤ 9719 TQ × 16 B", R10, 0.15)], x0, -0.55, 0.6, 15)
        hdr25 = VGroup(T("başlık", 15, HLC, BOLD).next_to(r25[0], UP, buff=0.08), T("kuyruk", 15, BIPC, BOLD).next_to(r25[2], UP, buff=0.08))
        hdr10 = T("başlık + kuyruk · 1 blok (16 B)", 15, HLC, BOLD).next_to(r10[0], UP, buff=0.08).align_to(r10[0], LEFT)
        l25 = T("2,5G · 1 TQ = 4 B", 18, R25, BOLD).next_to(r25, LEFT, buff=0.2)
        l10 = T("10G · 1 TQ = 16 B", 18, R10, BOLD).next_to(r10, LEFT, buff=0.2)
        fit(l25, 1.9)
        fit(l10, 1.9)
        b25 = brace_lbl(r25, "9720 TQ = 38 880 B (125 µs)", MUTED, DOWN, 16)
        b10 = brace_lbl(r10, "9720 TQ = 155 520 B (125 µs)", MUTED, DOWN, 16)
        q25 = VGroup(tag("2 TQ", R25, 17), T("başlık + kuyruk = 2 × 4 B  →  9718 + 2 = 9720", 18, TXT, BOLD)).arrange(RIGHT, buff=0.25)
        q10 = VGroup(tag("1 TQ", R10, 17), T("4 B + 4 B = 8 B tek bir 16 B bloğa sığar  →  9719 + 1 = 9720", 18, TXT, BOLD)).arrange(RIGHT, buff=0.25)
        qq = VGroup(q25, q10).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -2.55, 0])
        fit(qq, 12.6)
        self.play(self.set_src("G.989.3 §8.1.1.3 kural 9 ve NOT · aritmetik hesaplanmıştır"), run_time=0.3)
        self.at(self.cue("iki buçuk gigabitte dokuz bin yedi yüz on sekiz", 4.8))
        self.play(FadeIn(l25), FadeIn(r25[1]), FadeIn(b25), run_time=0.6)
        self.at(self.cue("on gigabitte dokuz bin yedi yüz on dokuz", 8.8))
        self.play(FadeIn(l10), FadeIn(r10[1]), FadeIn(b10), run_time=0.6)
        self.at(self.cue("Dört baytlık başlık ve dört baytlık kuyruk", 12.5))
        self.play(FadeIn(r25[0], shift=RIGHT * 0.08), FadeIn(r25[2], shift=LEFT * 0.08), FadeIn(hdr25), FadeIn(r10[0]), FadeIn(hdr10), run_time=0.6)
        self.at(self.cue("iki zaman kuantumu tutar", 16.4))
        self.play(FadeIn(q25, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("tek bir on altı baytlık bloğa", 20.2))
        self.play(FadeIn(q10, shift=UP * 0.08), Indicate(r10[0], color=GOLD, scale_factor=1.2), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p3B")


class E12P3C(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[3], M12("p3"), "neden"

    def construct(self):
        # d7 — ONU behaviour on bad BWmaps
        self.beat("d7")
        self.set_badge("std")
        h = self.show_heading("Hatalı BWmap → ONU ne yapar?")
        pr = pill("ilke: ↑ çarpışma olasılığını en aza indir", GOLD, 19).move_to([0, -2.8, 0])
        hd = VGroup(T("durum", 16, MUTED, BOLD).move_to([-6.3, 1.75, 0], aligned_edge=LEFT), T("ONU davranışı", 16, MUTED, BOLD).move_to([-0.9, 1.75, 0], aligned_edge=LEFT),
                    T("optik çıkış", 16, MUTED, BOLD).move_to([3.2, 1.75, 0], aligned_edge=LEFT))
        data = [("tahsis yapısında düzeltilemez hata", "burst'ün kalanını bastır", 0.3),
                ("StartTime sınır dışı (> 9719)", "hiç gönderme", 0.0),
                ("diğer kurallar (5 – 11) ihlal", "kurallar sağlanmış gibi kısa kes", 0.72),
                ("kendi serisinde bilinmeyen Alloc-ID", "kalanını bastır", 0.45)]
        rows = VGroup()
        for i, (c, a, f) in enumerate(data):
            y = 1.1 - i * 0.88
            bg = Rectangle(width=12.9, height=0.74, stroke_width=0, fill_color=PANEL if i % 2 == 0 else "#0E1628", fill_opacity=1).move_to([0, y, 0])
            ct = fit(T(c, 18, TXT, MEDIUM), 5.2).move_to([-6.3, y, 0], aligned_edge=LEFT)
            at_ = fit(T(a, 18, WARN if f == 0 else GOLD, BOLD), 3.9).move_to([-0.9, y, 0], aligned_edge=LEFT)
            mb = mini_burst(3.2, 3.1, y, f)
            rows.add(VGroup(bg, ct, at_, mb))
        self.play(self.set_src("G.989.3 §8.1.1.3"), run_time=0.3)
        self.at(self.cue("Kural açıktır", 1.8))
        self.play(FadeIn(hd), run_time=0.3)
        self.at(self.cue("yukarı yön çarpışması olasılığını", 3.8))
        self.play(FadeIn(pr, shift=UP * 0.08), run_time=0.5)
        for k, (key, d) in enumerate((("düzeltilemeyen bir hata varsa", 9.5), ("sınırın dışındaysa hiç", 16.0), ("Diğer kurallar ihlal", 20.2), ("bilmediği bir tahsis kimliği", 26.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:3], shift=RIGHT * 0.08), FadeIn(rows[k][3]), run_time=0.6)
        self.end(pad=0.05)

        # d8 — PLOAMd partition
        self.beat("d8")
        self.clear(h)
        h = self.show_heading("PLOAMd — 48 baytlık mesajlar", h)
        names = [("yayın", GOLD), ("ONU 3", PLDC), ("ONU 7", PLDC), ("ONU 12", PLDC)]
        msgs = VGroup(*[seg(0, 2.25, 0, c, n, 0.62, 0.25 if i else 0.4, 17) for i, (n, c) in enumerate(names)]).arrange(RIGHT, buff=0.08).move_to([-1.05, 1.6, 0])
        bad = seg(0, 2.25, 0, WARN, "ONU 3 (ikinci)", 0.62, 0.12, 16).next_to(msgs, RIGHT, buff=0.08)
        badx = xmark(bad[0], WARN, 4, 0.0)
        sz = VGroup(*[T("48 B", 15, MUTED, BOLD).next_to(m, UP, buff=0.08) for m in msgs])
        pl = VGroup(T("P = 4", 18, PLDC, BOLD), T("örnek", 14, MUTED)).arrange(DOWN, buff=0.04).next_to(msgs, LEFT, buff=0.2)
        fw = VGroup(tag("alan", MUTED, 17), T("PLOAM sayısı 8 bit → P ≤ 255", 20, TXT, BOLD)).arrange(RIGHT, buff=0.25)
        rk = VGroup(tag("kural", GOLD, 17), T("çerçeve başına ≤ 1 yayın + ONU başına ≤ 1 tek alıcılı mesaj", 20, TXT, BOLD)).arrange(RIGHT, buff=0.25)
        fr = VGroup(fw, rk).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.05, 0])
        ps = fields([("ONU-ID", 2, PLDC), ("tip", 1, PLDC), ("sıra", 1, PLDC), ("içerik · 36 B", 36, PLDC), ("MIC · 8 B", 8, GOLD)], 9.6, 0.55, 16, 14, unit=" B", show_w=False).move_to([0.3, -1.75, 0])
        psl = T("PLOAM mesajı (Tablo 11-1)", 16, MUTED, BOLD).next_to(ps, DOWN, buff=0.12).align_to(ps, LEFT)
        nx = VGroup(T("içi:", 16, MUTED, BOLD), s2chip(5, 16)).arrange(RIGHT, buff=0.15).move_to([3.6, -2.8, 0])
        self.play(self.set_src("G.989.3 §8.1.1.4 · §11.1.2 · Tablo 11-1"), run_time=0.3)
        self.at(self.cue("PLOAM bölmesi", 0.2))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.08) for m in msgs], lag_ratio=0.15), FadeIn(pl), run_time=0.8)
        self.at(self.cue("kırk sekiz baytlık sıfır", 1.2))
        self.play(FadeIn(sz), run_time=0.4)
        self.at(self.cue("iki yüz elli beşe kadar", 6.4))
        self.play(FadeIn(fw, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("en çok bir yayın mesajına", 12.1))
        self.play(FadeIn(rk, shift=UP * 0.08), run_time=0.5)
        self.play(FadeIn(bad, shift=LEFT * 0.08), run_time=0.4)
        self.play(Create(badx), run_time=0.4)
        self.at(self.cue("beşinci bölümde açacağız", 21.3))
        self.play(FadeIn(ps), FadeIn(psl), FadeIn(nx, shift=UP * 0.08), run_time=0.7)
        self.end(pad=0.05)

        # d9 — header overhead vs N and P
        self.beat("d9")
        self.clear(h)
        h = self.show_heading("Kapasite hesabı — başlık yükü", h)
        fm = VGroup(T("başlık + kuyruk =", 26, TXT, BOLD), T("4 + 8N + 48P + 4", 26, MUTED, BOLD), T("= 8 + 8N + 48P bayt", 26, GOLD, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, 1.85, 0])
        fit(fm, 12.4)
        ex = T("örnek: N = 512 (kural 5), P = 1 → 4152 B", 19, MUTED, BOLD).move_to([0, 0.95, 0])
        bx0, bw = -3.6, 8.4

        def share(lbl, color, frac, y, pct):
            l = T(lbl, 18, color, BOLD).move_to([bx0 - 0.25, y, 0], aligned_edge=RIGHT)
            full = Rectangle(width=bw, height=0.55, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.1).move_to([bx0 + bw / 2, y, 0])
            part = Rectangle(width=bw * frac, height=0.55, stroke_width=0, fill_color=GOLD, fill_opacity=0.8).move_to([bx0 + bw * frac / 2, y, 0])
            p = T(pct, 24, GOLD, BOLD).next_to(full, RIGHT, buff=0.2)
            return VGroup(l, full, part, p)
        s10 = share("10G · FEC açık", R10, 4152 / 135432, -0.1, "%3,1")
        s25 = share("2,5G · FEC açık", R25, 4152 / 36344, -1.0, "%11,4")
        neg = T("ihmal edilebilir", 17, GOOD, BOLD).next_to(s10[2], RIGHT, buff=0.15).shift(UP * 0.0)
        lite = pill("2,5G kanallar → daha hafif BWmap", GOLD, 20).move_to([0, -2.35, 0])
        nt = T("FS çerçevesinin payı · hesaplanmıştır", 15, MUTED).next_to(s25, DOWN, buff=0.12).align_to(s25[1], LEFT)
        self.play(self.set_src("G.989.3 §8.1.1.1 · Tablo 8-1 · paylar hesaplanmıştır"), run_time=0.3)
        self.at(self.cue("sekiz artı sekiz N", 1.3))
        self.play(FadeIn(fm, shift=UP * 0.08), run_time=0.6)
        self.at(self.cue("On gigabitte bu ihmal", 6.1))
        self.play(FadeIn(s10[:3]), FadeIn(neg), run_time=0.6)
        self.at(self.cue("beş yüz on iki girdili", 8.8))
        self.play(FadeIn(ex), FadeIn(s10[3]), run_time=0.5)
        self.at(self.cue("yüzde on birinden fazlasını", 12.3))
        self.play(FadeIn(s25[:2]), GrowFromEdge(s25[2], LEFT), FadeIn(s25[3]), FadeIn(nt), run_time=0.8)
        self.at(self.cue("daha hafif haritalarla", 18.8))
        self.play(FadeIn(lite, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # d10 — engineer note
        self.note11("d10", [("1", "Alan genişliği ≠ kural",
                             "BWmap uzunluğu 11 bit → 2047 girdi; kural 5 → en çok 512. Çözücüyü kurala göre yazın.", "alan genişlikleri ile kurallar"),
                            ("2", "StartTime başlığı gösterir, önsözü değil",
                             "PSBu önceki çerçeveye düşebilir — zamanlama hatalarının sık kaynağı.", "başlangıç zamanının önsözü")])
        self.bridge_beat("d11", "Aşağı yön haritayı gönderdi.\nŞimdi ONU'nun cevabı: yukarı yön burst'ü.")
        self.save_timeline("ep12_p3C")


# ================================ PERDE 4 ======================================
class E12P4A(Act12):
    HDR, MANIFEST, FIRST = H12[4], M12("p4"), True

    def construct(self):
        # e1 — two kinds of 125 µs
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Yukarı yön burst'ü")
        self.at(self.cue("Önce iki tür", 1.9))
        self.to_header(tc)
        self.set_badge("neden")
        h = self.show_heading("İki tür 125 µs")
        x0, fw = -4.3, 3.3
        yd = 1.55
        dl = T("↓ OLT CT", 18, TW_DS, BOLD).move_to([-6.4, yd, 0], aligned_edge=LEFT)
        ds = VGroup(*[VGroup(seg(x0 + i * fw, 0.35, yd, PHC, None, 0.55, 0.8), seg(x0 + i * fw + 0.35, fw - 0.35, yd, TW_DS, None, 0.55, 0.12)) for i in range(3)])
        ev = VGroup(*[Line([x0 + i * fw, yd - 0.3, 0], [x0 + i * fw, yd + 0.42, 0], color=GOLD, stroke_width=3) for i in range(4)])
        evl = T("fiziksel olay: PSBd'nin ilk biti", 17, GOLD, BOLD).next_to(ds, DOWN, buff=0.18).align_to(ds, LEFT).shift(RIGHT * 0.2)

        def grid(y, off, label, c):
            l = T(label, 17, c, BOLD).move_to([-6.4, y, 0], aligned_edge=LEFT)
            g = VGroup(*[DashedVMobject(Rectangle(width=fw, height=0.45, stroke_color=c, stroke_width=1.8), num_dashes=30).move_to([x0 + off + i * fw + fw / 2, y, 0]) for i in range(3)])
            return VGroup(l, g)
        g0 = grid(-0.2, 0.45, "↑ OLT", OLTC)
        g1 = grid(-0.9, 0.85, "↑ ONU A", ONUC)
        g2 = grid(-1.6, 0.2, "↑ ONU B", R25)
        vl = T("sanal ızgara: herkes farklı anda yerleştirir", 17, MUTED, BOLD).move_to([0.6, -2.3, 0])
        nx = VGroup(T("mesafe ölçümüyle:", 16, MUTED, BOLD), s2chip(6, 16)).arrange(RIGHT, buff=0.15).move_to([3.6, -2.95, 0])
        self.play(self.set_src("G.989.3 §10.1.1 · §10.1.2 · §8.1.1.2.3"), run_time=0.3)
        self.at(self.cue("çerçeve sınırı fiziksel", 7.0))
        self.play(FadeIn(dl), LaggedStart(*[FadeIn(d, shift=RIGHT * 0.1) for d in ds], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("PSBd'nin ilk biti", 10.9))
        self.play(LaggedStart(*[Create(e) for e in ev], lag_ratio=0.15), FadeIn(evl), run_time=0.7)
        self.at(self.cue("sanal bir ızgaradır", 12.4))
        self.play(FadeIn(g0, shift=RIGHT * 0.1), run_time=0.5)
        self.at(self.cue("OLT ve her ONU", 16.2))
        self.play(FadeIn(g1, shift=RIGHT * 0.1), FadeIn(g2, shift=RIGHT * 0.1), FadeIn(vl), run_time=0.7)
        self.at(self.cue("Bunu altıncı bölümde", 20.0))
        self.play(FadeIn(nx, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # e2 — upstream PHY burst = PSBu + payload; silence between bursts
        self.beat("e2")
        self.clear(h)
        self.set_badge("std")
        h = self.show_heading("Yukarı yön fiziksel burst'ü", h)
        y = 1.2
        b1 = VGroup(seg(-6.2, 1.2, y, PHC, "önsöz", 0.6, 0.3, 16), seg(-5.0, 0.7, y, PHC, "sın.", 0.6, 0.65, 15, BG), seg(-4.3, 3.7, y, TW_US, None, 0.6, 0.12))
        sc1 = scramble(b1[2][0], 55, 2, PHC)
        b2 = VGroup(seg(0.8, 1.2, y, PHC, "önsöz", 0.6, 0.3, 16), seg(2.0, 0.7, y, PHC, "sın.", 0.6, 0.65, 15, BG), seg(2.7, 3.5, y, TW_US, None, 0.6, 0.12))
        sc2 = scramble(b2[2][0], 50, 6, PHC)
        gap = DashedLine([-0.55, y - 0.3, 0], [0.75, y - 0.3, 0], color=MUTED, stroke_width=2)
        gl = T("Tx kapalı · sessiz", 15, MUTED, BOLD).move_to([0.1, y + 0.55, 0])
        bp = brace_lbl(VGroup(b1[0], b1[1]), "PSBu", PHC, DOWN, 18)
        by = brace_lbl(b1[2], "burst yükü: FS burst → FEC → karıştır", TW_US, DOWN, 17)
        rx = sbox("OLT burst alıcısı", None, OLTC, 3.0, 0.8, 19).move_to([-3.6, -1.75, 0])
        o1 = VGroup(tag("önsöz", PHC, 17), T("→ sinyal düzeyine uyum", 18, TXT)).arrange(RIGHT, buff=0.2)
        o2 = VGroup(tag("sınırlayıcı", PHC, 17), T("→ burst'ün sınırını bul", 18, TXT)).arrange(RIGHT, buff=0.2)
        oo = VGroup(o1, o2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rx, RIGHT, buff=0.6)
        oa = VGroup(*[arrow(rx.get_right(), o[0].get_left(), MUTED, 2, 0.1) for o in oo])
        self.play(self.set_src("G.989.3 §10.1.2 · §10.1.2.1 – .2 · Şekil 10-5 / 10-6"), run_time=0.3)
        self.at(self.cue("önsöz ve sınırlayıcıdan oluşan", 3.4))
        self.play(FadeIn(b1[0], shift=RIGHT * 0.08), FadeIn(b1[1], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("PSBu", 8.1))
        self.play(FadeIn(bp), run_time=0.3)
        self.at(self.cue("FEC ile korunmuş", 8.6))
        self.play(FadeIn(b1[2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("karıştırılmış burst yükü", 10.2))
        self.play(LaggedStart(*[Create(l) for l in sc1], lag_ratio=0.01), FadeIn(by), run_time=0.8)
        self.at(self.cue("Burst'ler arasında ONU", 12.3))
        self.play(Create(gap), FadeIn(gl), FadeIn(b2), LaggedStart(*[Create(l) for l in sc2], lag_ratio=0.01), run_time=0.9)
        self.at(self.cue("PSBu'nun görevi", 17.2))
        self.play(FadeIn(rx, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("sinyal düzeyine uyum", 18.5))
        self.play(GrowArrow(oa[0]), FadeIn(o1, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("burst'ün sınırını bulmasıdır", 22.5))
        self.play(GrowArrow(oa[1]), FadeIn(o2, shift=RIGHT * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # e3 — PMD bridge: Table 11-11, 512 / 2048 bits = 205.76 ns = 16 TQ
        self.beat("e3")
        self.clear()
        self.set_badge("pmd")
        h = self.show_heading("PMD Köprüsü — burst başına fiziksel ek yük")
        ch = self.chip_at(s1chip(6), h)
        bx0, bw = -3.3, 9.2
        t = tag("G.989.2 Tablo 11-11", MUTED, 17).move_to([-5.1, 2.1, 0])

        def obar(y, color, lbl, bits):
            r = Rectangle(width=bw, height=0.62, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.15).move_to([bx0 + bw / 2, y, 0])
            return VGroup(T(lbl, 19, color, BOLD).next_to(r, LEFT, buff=0.25), r, T(bits, 21, TXT, BOLD).move_to(r))
        r25 = obar(1.25, R25, "2,5G", "512 bit")
        r10 = obar(0.35, R10, "10G", "2048 bit")
        ticks = VGroup(*[Line([bx0 + i * bw / 16, -0.05, 0], [bx0 + i * bw / 16, 1.65, 0], color=MUTED, stroke_width=1, stroke_opacity=0.6) for i in range(1, 16)])
        br = BraceBetweenPoints([bx0, -0.05, 0], [bx0 + bw, -0.05, 0], DOWN, color=GOLD)
        brl = T("aynı süre: 205,76 ns", 22, GOLD, BOLD).next_to(br, DOWN, buff=0.06)
        tq = T("= 16 zaman kuantumu", 20, ACC, BOLD).next_to(brl, RIGHT, buff=0.3)
        dec = strip([(2.0, "koruma Tg", MUTED, 0.15, True), (5.6, "önsöz Tp", PHC, 0.3), (1.6, "sın. Td", PHC, 0.65)], bx0, -1.95, 0.62, 17)
        dl = T("Tplo =", 20, TXT, BOLD).next_to(dec, LEFT, buff=0.25)
        dn = T("oranlar temsilî", 15, MUTED).next_to(dec, DOWN, buff=0.1).align_to(dec, RIGHT)
        self.play(FadeIn(ch, shift=LEFT * 0.1), self.set_src("G.989.2 Tablo 11-11 · Ek III · TQ = 12,86 ns"), run_time=0.5)
        self.at(self.cue("fiziksel katman ek yükünü", 5.0))
        self.play(FadeIn(t), run_time=0.4)
        self.at(self.cue("iki buçuk gigabitte beş yüz", 8.6))
        self.play(FadeIn(r25, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("iki bin kırk sekiz bit", 11.5))
        self.play(FadeIn(r10, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("İkisi de aynı süredir", 14.6))
        self.play(FadeIn(br), run_time=0.4)
        self.at(self.cue("iki yüz beş virgül", 16.4))
        self.play(FadeIn(brl, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("on altı zaman kuantumu", 19.8))
        self.play(LaggedStart(*[Create(l) for l in ticks], lag_ratio=0.04), FadeIn(tq, shift=LEFT * 0.08), run_time=0.8)
        self.at(self.cue("Koruma süresi", 22.5))
        self.play(FadeIn(dl), FadeIn(dec[0]), run_time=0.4)
        self.at(self.cue("önsöz ve sınırlayıcı bu bütçenin", 23.7))
        self.play(FadeIn(dec[1:], shift=RIGHT * 0.08), FadeIn(dn), run_time=0.6)
        self.end(pad=0.05)

        # e4 — burst profiles via Burst_Profile PLOAM
        self.beat("e4")
        self.clear()
        self.set_badge("std")
        h = self.show_heading("Burst profili — Burst_Profile PLOAM")
        olt = ct_box("OLT CT", OLTC, 1.5, 0.6, 18).move_to([-5.6, 1.7, 0])
        onu = onu_box("ONU", ONUC, 1.4, 0.6, 18).move_to([-1.7, 1.7, 0])
        m = msg(olt.get_right()[0], onu.get_left()[0], 1.7, "Burst_Profile · önceden", GOLD, 15)
        slots = VGroup(*[tile(f"profil {i}", PHC, 1.15, 0.45, 15, 0.15) for i in range(4)]).arrange(RIGHT, buff=0.1).move_to([-3.45, 0.65, 0])
        sl = T("ONU'da saklanan profiller", 15, MUTED, BOLD).next_to(slots, UP, buff=0.1)
        al = strip([(1.3, "Alloc-ID", MUTED, 0.12), (2.3, "…", MUTED, 0.12), (1.0, "Profil", PRFC, 0.3), (1.0, "HEC", MUTED, 0.12)], -6.25, -1.15, 0.5, 15)
        alt = T("BWmap tahsis yapısı: 2 bitlik indeks (ölçeksiz)", 15, MUTED, BOLD).next_to(al, DOWN, buff=0.12)
        pv = HX("= 2", 16, PRFC, BOLD).next_to(al[2], DOWN, buff=0.08).shift(RIGHT * 0.0)
        alt.next_to(pv, DOWN, buff=0.08).align_to(al, LEFT)
        pa = CurvedArrow(al[2][0].get_top(), slots[2].get_bottom(), angle=0.3, color=PRFC, stroke_width=2.2, tip_length=0.12)
        p = apanel(6.7, 4.75, "Analizör · Burst_Profile (Tablo 11-4)", GOLD).move_to([3.2, -0.2, 0])
        prow = [("oktet 3 · tip", "0x01"), ("oktet 5 · VVVV R F PP", "sürüm · hız (F) · indeks"), ("oktet 6 · … C F", "F: ↑ FEC açık / kapalı"),
                ("oktet 7 · sınırlayıcı uz.", "0 – 8 bayt"), ("oktet 8–15", "sınırlayıcı deseni"), ("oktet 16 · önsöz uz.", "1 – 8 bayt"),
                ("oktet 17 · tekrar sayısı", "0 – 255"), ("oktet 18–25", "önsöz deseni")]
        rows = VGroup(*[VGroup(T(k, 15, MUTED, BOLD), T(v, 17, TXT, BOLD)) for k, v in prow])
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.2)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r in rows:
            r[1].set_x(rows.get_left()[0] + 2.75 + r[1].width / 2)
        fit(rows, 6.3).move_to(p[0]).shift(DOWN * 0.2)
        self.play(self.set_src("G.989.3 §10.1.2.1 · §11.3.3.1 · Tablo 11-4"), run_time=0.3)
        self.at(self.cue("burst'ün profilini oluşturur", 3.8))
        self.play(FadeIn(p), run_time=0.5)
        self.at(self.cue("OLT profilleri önceden", 6.2))
        self.play(FadeIn(olt), FadeIn(onu), GrowArrow(m[0]), FadeIn(m[1]), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.08) for s_ in slots], lag_ratio=0.15), FadeIn(sl), run_time=0.7)
        self.at(self.cue("iki bitlik indeksle", 10.6))
        self.play(FadeIn(al), FadeIn(alt), run_time=0.5)
        self.play(FadeIn(pv), Create(pa), Indicate(slots[2], color=GOLD, scale_factor=1.1), run_time=0.7)
        for k, (key, d, idx) in enumerate((("bir sürüm alanı", 14.5, (0, 1)), ("hangi hız için", 16.5, ()), ("FEC'in açık mı", 19.1, (2,)),
                                          ("sıfır ile sekiz bayt", 22.7, (3, 4)), ("bir ile sekiz bayt", 26.0, (5,)), ("iki yüz elli beş kereye", 28.3, (6, 7)))):
            self.at(self.cue(key, d))
            if idx:
                self.play(*[FadeIn(rows[j], shift=RIGHT * 0.08) for j in idx], run_time=0.45)
            else:
                self.play(Indicate(rows[1][1], color=GOLD, scale_factor=1.06), run_time=0.5)
        self.end(pad=0.05)

        # e4a — profile rules
        self.beat("e4a")
        self.clear(h)
        h = self.show_heading("Profil kuralları", h)
        tx0, tx1, ty = -5.6, 6.2, 1.55
        tl = Arrow([tx0, ty, 0], [tx1, ty, 0], buff=0, color=MUTED, stroke_width=2, tip_length=0.14, max_tip_length_to_length_ratio=0.03)
        tll = T("OLT · Burst_Profile yayını", 16, MUTED, BOLD).move_to([-6.3, ty + 0.8, 0], aligned_edge=LEFT)
        xs = [tx0 + 0.4 + i * 1.25 for i in range(9)]
        sends = VGroup(*[VGroup(Line([x, ty - 0.18, 0], [x, ty + 0.18, 0], color=GOLD if i >= 3 else MUTED, stroke_width=3),
                                T("v2" if i >= 3 else "v1", 15, GOLD if i >= 3 else MUTED, BOLD).move_to([x, ty + 0.4, 0])) for i, x in enumerate(xs)])
        gapl = BraceBetweenPoints([xs[0], ty - 0.25, 0], [xs[1], ty - 0.25, 0], DOWN, color=MUTED)
        gapt = T("yüzlerce ms", 15, MUTED, BOLD).next_to(gapl, DOWN, buff=0.04)
        ra = VGroup(T("ONU A", 16, ONUC, BOLD).move_to([-6.3, 0.35, 0], aligned_edge=LEFT), *[T("✓", 20, GOOD, BOLD).move_to([xs[i], 0.35, 0]) for i in (3, 4)])
        rb = VGroup(T("ONU B", 16, ONUC, BOLD).move_to([-6.3, -0.25, 0], aligned_edge=LEFT), *[T("✓", 20, GOOD, BOLD).move_to([xs[i], -0.25, 0]) for i in (4, 5)],
                    T("✗", 20, WARN, BOLD).move_to([xs[3], -0.25, 0]))
        use = VGroup(DashedLine([xs[5] + 0.45, ty + 0.3, 0], [xs[5] + 0.45, -0.6, 0], color=GOOD, stroke_width=2.5),
                     T("v2 artık kullanılabilir", 16, GOOD, BOLD).move_to([xs[5] + 2.15, -0.65, 0]))
        rule = T("her ONU en az iki kez alma fırsatı bulmadan değişen profil kullanılmaz", 17, TXT, BOLD).move_to([0, -1.25, 0])
        c1 = card("Saklanmaz", "profiller ONU aktivasyonları\narasında korunmaz", None, WARN, w=5.9, h=1.35, tsize=20, bsize=17).move_to([-3.2, -2.55, 0])
        c2 = card("Profil yoksa cevap yok", "ONU, karşılık gelen profili almadan\nbir tahsise cevap veremez", None, WARN, w=5.9, h=1.35, tsize=20, bsize=17).move_to([3.2, -2.55, 0])
        self.play(self.set_src("G.989.3 §11.3.3.1 · Ek III"), run_time=0.3)
        self.at(self.cue("yüzlerce milisaniyelik", 2.4))
        self.play(GrowArrow(tl), FadeIn(tll), LaggedStart(*[FadeIn(sends[i]) for i in range(3)], lag_ratio=0.2), FadeIn(gapl), FadeIn(gapt), run_time=1.0)
        self.at(self.cue("en az iki kez", 7.7))
        self.play(LaggedStart(*[FadeIn(sends[i]) for i in range(3, 9)], lag_ratio=0.12), run_time=0.9)
        self.play(FadeIn(ra), FadeIn(rb), run_time=0.6)
        self.play(Create(use[0]), FadeIn(use[1]), FadeIn(rule, shift=UP * 0.08), run_time=0.6)
        self.at(self.cue("aktivasyonlar arasında saklanmaz", 14.8))
        self.play(FadeIn(c1, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("karşılık gelen profili almadan", 18.7))
        self.play(FadeIn(c2, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p4A")


T31 = [["0xBB52 1E26", "0x4BDE 1B90", "0xA376 70C9"], ["0xAAAA AAAA", "0xA566 79E0", "0xAD4C C30F"]]
T32 = [["2,5G · hedef", "128", "320", "32", "480", "512", "✗"], ["10G · hedef", "512", "1280", "32", "1824", "2048", "✗"],
       ["2,5G · en kötü", "512", "1472", "64", "2048", "2048", "✓"], ["10G · en kötü", "2048", "6080", "64", "8192", "8192", "✓"]]


class E12P4B(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[4], M12("p4"), "std"

    def construct(self):
        # e5 — Appendix III example at 2.5G and Table III.1
        self.beat("e5")
        h = self.show_heading("Ek III önerisi — 2,5G burst başı")
        u = 0.04
        bx0 = -5.12
        bb = strip([(64 * u, "koruma · 64 bit (2 TQ)", MUTED, 0.12, True), (160 * u, "önsöz · 160 bit (5 TQ)", PHC, 0.3), (32 * u, "sın. 32", PHC, 0.65)], bx0, 1.6, 0.62, 16)
        tq = VGroup(*[Line([bx0 + i * 32 * u, 1.93, 0], [bx0 + i * 32 * u, 2.05, 0], color=ACC, stroke_width=2) for i in range(9)])
        br = brace_lbl(bb, "256 bit = 8 TQ = 102,9 ns", GOLD, DOWN, 19)
        hb = VGroup(tag("yüksek BER", WARN, 17), T("→ 64 bitlik sınırlayıcı", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([-3.3, 0.2, 0])
        pr = VGroup(tag("sınırlayıcı çifti", GOLD, 17), T("→ FEC açık / kapalı bilgisini taşır", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([3.0, 0.2, 0])
        tb = mtable(["önsöz deseni", "32 bit sınırlayıcı · FEC açık", "· FEC kapalı (varsayılan)"], T31, [3.1, 4.1, 4.1], size=19, hsize=16, row_h=0.55, mono=(0, 1, 2)).move_to([0, -1.45, 0])
        tbl = T("Tablo III.1 (seçme)", 15, MUTED, BOLD).next_to(tb, UP, buff=0.08).align_to(tb, LEFT)
        dc = VGroup(tag("hepsi doğru akım dengeli", GOOD, 17), T("her desende birler = sıfırlar", 17, TXT)).arrange(RIGHT, buff=0.2).move_to([0, -2.75, 0])
        self.play(self.set_src("G.989.3 Ek III · Tablo III.1 · süre ve denge hesaplanmıştır"), run_time=0.3)
        self.at(self.cue("iki zaman kuantumluk koruma", 2.4))
        self.play(FadeIn(bb[0], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("yüz altmış bitlik önsöz", 7.0))
        self.play(FadeIn(bb[1], shift=RIGHT * 0.08), run_time=0.4)
        self.play(FadeIn(bb[2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("toplam iki yüz elli altı", 11.6))
        self.play(FadeIn(br), FadeIn(tq), run_time=0.5)
        self.at(self.cue("yüz iki virgül dokuz", 14.1))
        self.play(Indicate(br[1], color=GOLD, scale_factor=1.06), run_time=0.5)
        self.at(self.cue("altmış dört bitlik sınırlayıcı", 16.7))
        self.play(FadeIn(hb, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("bir çift farklı sınırlayıcı", 21.8))
        self.play(FadeIn(pr, shift=UP * 0.08), FadeIn(tbl), FadeIn(tb), run_time=0.7)
        self.at(self.cue("FEC'in açık mı kapalı mı olduğunu da", 24.4))
        self.play(Indicate(VGroup(tb[1][2], tb[1][3], tb[2][2], tb[2][3]), color=GOLD, scale_factor=1.05), run_time=0.7)
        self.at(self.cue("doğru akım dengelidir", 28.6))
        self.play(FadeIn(dc, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # e6 — guard time: three documents, three numbers
        self.beat("e6")
        self.clear(h)
        h = self.show_heading("Koruma süresi: üç belge, üç sayı", h)
        ax0, ax1 = -2.4, 6.3
        Xb = lambda b: ax0 + b / 1350 * (ax1 - ax0)

        def gbar(y, bits, color, lbl, val):
            l = T(lbl, 17, color, BOLD).move_to([-6.4, y, 0], aligned_edge=LEFT)
            r = Rectangle(width=Xb(bits) - ax0, height=0.5, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.35).move_to([(ax0 + Xb(bits)) / 2, y, 0])
            v = T(val, 17, TXT, BOLD).next_to(r, RIGHT, buff=0.15)
            return VGroup(l, r, v)
        g1 = gbar(1.6, 64, ACC, "G.989.3 §10.1.2.3", "64 bit · hız belirtilmemiş (10G'de 6,4 ns)")
        g2 = gbar(0.65, 256, GOLD, "G.989.3 Ek III", "2 TQ = 256 bit @ 10G")
        g3 = gbar(-0.3, 1280, WARN, "G.989.2: Tg ≥ Ton + Tu", "")
        g3v = T("Ton ≤ 1280 bit (10G) = 128,6 ns", 17, BG, BOLD).move_to(g3[1])
        axl = Line([ax0, -0.85, 0], [ax1, -0.85, 0], color=MUTED, stroke_width=2)
        axt = VGroup(*[VGroup(Line([Xb(b), -0.92, 0], [Xb(b), -0.78, 0], color=MUTED, stroke_width=1.5), T(str(b), 14, MUTED).move_to([Xb(b), -1.12, 0])) for b in (0, 256, 512, 1024, 1280)])
        axn = T("bit (10G)", 14, MUTED).next_to(axl, LEFT, buff=0.15)
        ws = pill("64 bitlik koruma ancak çok hızlı açılan vericilerle güvenli", WARN, 19).move_to([-0.6, -2.1, 0])
        it = interp("yorum", GOLD, 16).next_to(ws, RIGHT, buff=0.25)
        ref = T("G.989.2 Tablo 11-6 / 11-7 · Ek III", 15, MUTED).move_to([0, -2.8, 0])
        self.play(self.set_src("G.989.3 §10.1.2.3 · Ek III · G.989.2 Ek III, Tablo 11-6 / 11-7"), run_time=0.3)
        self.at(self.cue("tutarsızlık var", 1.5))
        self.play(Create(axl), FadeIn(axt), FadeIn(axn), run_time=0.6)
        self.at(self.cue("koruma süresi için tek bir sayı", 5.7))
        self.play(FadeIn(g1[0]), run_time=0.4)
        self.at(self.cue("altmış dört bit", 9.6))
        self.play(GrowFromEdge(g1[1], LEFT), run_time=0.4)
        self.at(self.cue("hız belirtmeden", 10.9))
        self.play(FadeIn(g1[2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("Üçüncü ek iki zaman", 12.2))
        self.play(FadeIn(g2[0]), run_time=0.4)
        self.at(self.cue("on gigabitte bu iki yüz elli altı", 15.0))
        self.play(GrowFromEdge(g2[1], LEFT), FadeIn(g2[2], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("G.989.2 ise korumanın", 18.4))
        self.play(FadeIn(g3[0]), run_time=0.4)
        self.at(self.cue("bin iki yüz seksen bite", 24.0))
        self.play(GrowFromEdge(g3[1], LEFT), FadeIn(g3v), FadeIn(ref), run_time=0.7)
        self.at(self.cue("Altmış dört bitlik bir koruma", 30.3))
        self.play(FadeIn(ws, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("çok hızlı açılan", 32.8))
        self.play(FadeIn(it), run_time=0.4)
        self.end(pad=0.05)

        # e6a — preamble citation; Table III.2 rows that do not add up
        self.beat("e6a")
        self.clear(h)
        h = self.show_heading("Bir tutarsızlık daha — önsöz", h)
        ch = self.chip_at(s1chip(6), h)
        b1 = card("G.989.3 Ek III", "2,5G önsöz: 160 bit\n“see Appendix III of [ITU-T G.989.2]”", None, ACC, w=5.6, h=1.45, tsize=20, bsize=17).move_to([-3.5, 1.5, 0])
        b2 = card("G.989.2 Tablo III.2", "Tp (hedef) = 320 bit\nTp (en kötü) = 1472 bit", None, WARN, w=5.0, h=1.45, tsize=20, bsize=17).move_to([3.6, 1.5, 0])
        ne = T("≠", 40, WARN, BOLD).move_to([0.45, 1.5, 0])
        tb = table(["G.989.2 Tablo III.2", "Tg", "Tp", "Td", "Tg+Tp+Td", "Tplo", ""], T32, [3.0, 1.1, 1.2, 0.9, 1.9, 1.3, 0.8], size=18, hsize=15, row_h=0.5).move_to([0, -1.1, 0])
        for i, r in enumerate(tb[1:]):
            r[7].set_color(WARN if i < 2 else GOOD)
            r[5].set_color(GOLD)
        self.play(self.set_src("G.989.3 Ek III ↔ G.989.2 Ek III · Tablo III.2 · toplamlar hesaplanmıştır"), FadeIn(ch, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("yüz altmış bitlik önsöz için", 4.0))
        self.play(FadeIn(b1, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("orada önsöz üç yüz yirmi", 9.6))
        self.play(FadeIn(b2, shift=LEFT * 0.08), FadeIn(ne, scale=0.8), run_time=0.6)
        self.at(self.cue("hedef satırları toplanınca", 12.6))
        self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(tb[2]), run_time=0.6)
        self.at(self.cue("en kötü durum satırları", 18.6))
        self.play(FadeIn(tb[3]), FadeIn(tb[4]), run_time=0.6)
        self.at(self.cue("birinci sezonun altıncı", 21.9))
        self.play(Indicate(ch, color=S1C, scale_factor=1.08), run_time=0.6)
        self.end(pad=0.05)

        # e7 — upstream FS header
        self.beat("e7")
        self.clear()
        self.set_badge("std")
        h = self.show_heading("↑ FS başlığı — 4 bayt (+ 48)")
        hf = fields([("ONU-ID", 10, ACC), ("Ind", 9, GOLD), ("HEC", 13, HECC)], 9.6, 0.62, 19, 14, unit=" bit").move_to([0, 1.75, 0])
        v = VGroup(HX("0x3FF", 18, GOLD, BOLD), T("= 1023 · atanmamış", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([hf[0][0].get_x() - 0.7, 0.85, 0])
        bits = VGroup(*[Square(0.5, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.12) for _ in range(9)]).arrange(RIGHT, buff=0.04).move_to([0, -0.25, 0])
        bn = VGroup(*[T(f"b{8 - i}", 14, MUTED, BOLD).move_to(b) for i, b in enumerate(bits)])
        zl = zoom_lines(hf[1][0], bits, GOLD)
        bits[0].set_fill(GOLD, 0.5)
        bits[8].set_fill(WARN, 0.5)
        bits[8].set_stroke(WARN)
        rs = T("b7 – b1 ayrılmış", 15, MUTED, BOLD).next_to(bits[1:8], DOWN, buff=0.12)
        t8 = VGroup(T("b8 · PLOAM kuyruğu", 17, GOLD, BOLD), T("bekleyen başka PLOAM var", 16, TXT)).arrange(DOWN, aligned_edge=RIGHT, buff=0.06).next_to(bits, LEFT, buff=0.3)
        t0 = VGroup(T("b0 · DG", 17, WARN, BOLD), T("son nefes (dying gasp)", 16, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(bits, RIGHT, buff=0.3)
        y2 = -1.95
        pu = strip([(0.8, "4 B", HLC, 0.35), (9.2, "PLOAMu · 48 B (bir PLOAM mesajı)", PLDC, 0.22)], -5.0, y2, 0.6, 17)
        pul = T("PLOAMu bayrağı = 1 ise:", 17, PLDC, BOLD).next_to(pu, UP, buff=0.12).align_to(pu, LEFT)
        hl_ = T("başlık", 15, HLC, BOLD).next_to(pu[0], DOWN, buff=0.1)
        self.play(self.set_src("G.989.3 §8.1.2.1 · Şekil 8-5 · Tablo 6-4"), run_time=0.3)
        self.at(self.cue("on bitlik ONU kimliği", 3.1))
        self.play(FadeIn(hf[0]), run_time=0.4)
        self.at(self.cue("dokuz bitlik gösterge", 5.0))
        self.play(FadeIn(hf[1], shift=LEFT * 0.08), FadeIn(hf[2], shift=LEFT * 0.08), run_time=0.5)
        self.at(self.cue("Henüz kimliği olmayan", 9.0))
        self.play(Indicate(hf[0], color=GOLD, scale_factor=1.05), run_time=0.5)
        self.at(self.cue("bin yirmi üç değeriyle", 11.5))
        self.play(FadeIn(v, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("Gösterge alanının en anlamlı", 16.4))
        self.play(Create(zl), FadeIn(bits), FadeIn(bn), FadeIn(rs), run_time=0.7)
        self.at(self.cue("bekleyen başka PLOAM", 19.3))
        self.play(FadeIn(t8, shift=RIGHT * 0.08), Indicate(bits[0], color=GOLD), run_time=0.5)
        self.at(self.cue("en az anlamlı biti ise", 22.6))
        self.play(FadeIn(t0, shift=LEFT * 0.08), Indicate(bits[8], color=WARN), run_time=0.5)
        self.at(self.cue("dying gasp", 25.4))
        self.play(Indicate(t0, color=WARN, scale_factor=1.04), run_time=0.5)
        self.at(self.cue("kırk sekiz baytlık bir PLOAM", 28.1))
        self.play(FadeIn(pul), FadeIn(pu, shift=RIGHT * 0.08), FadeIn(hl_), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep12_p4B")


EFF = [(8, 98.6, 85.7), (32, 94.4, 81.9), (64, 88.7, 76.9)]


class E12P4C(Act12):
    HDR, MANIFEST, PREV_BADGE = H12[4], M12("p4"), "std"

    def construct(self):
        # e8 — DBRu
        self.beat("e8")
        h = self.show_heading("DBRu — durum raporu, 4 bayt")
        db = fields([("BufOcc · tampon doluluğu", 24, BWC), ("CRC-8", 8, GOLD)], 8.0, 0.62, 18, 14, unit=" bit").move_to([-2.4, 1.75, 0])
        wh = tag("DBRu bayrağı = 1 → tahsisin başında", BWC, 16).next_to(db, RIGHT, buff=0.35)
        un = VGroup(tag("birim", BWC, 17), T("4 bayt", 20, TXT, BOLD), T("W = ⌈L / 4⌉ (L > 8) · W = 2 (0 < L ≤ 8)", 17, MUTED)).arrange(RIGHT, buff=0.25).move_to([-6.3, 0.55, 0], aligned_edge=LEFT)
        mx = VGroup(tag("en büyük", BWC, 17), HX("0xFFFFFE × 4 B", 18, TXT, BOLD), T("≈ 64 MiB", 20, GOLD, BOLD), T("(0xFFFFFF = geçersiz)", 16, MUTED)).arrange(RIGHT, buff=0.25).move_to([-6.3, -0.2, 0], aligned_edge=LEFT)
        c1 = card("ATM HEC (I.432.1)", "CRC-8 · g(x) = x⁸ + x² + x + 1\nsonra XOR 0x55", None, MUTED, w=5.6, h=1.45, tsize=20, bsize=18).move_to([-3.3, -1.6, 0])
        c2 = card("DBRu CRC", "aynı g(x) = x⁸ + x² + x + 1\nXOR 0x55 YOK", None, GOLD, w=5.6, h=1.45, tsize=20, bsize=18).move_to([3.3, -1.6, 0])
        ne = T("≠", 36, WARN, BOLD).move_to([0, -1.6, 0])
        bad = pill("eski ATM kodu → her DBRu reddedilir", WARN, 19).move_to([0, -2.8, 0])
        self.play(self.set_src("G.989.3 §8.1.2.2 · formül (8-1) · ≈ 64 MiB hesaplanmıştır"), run_time=0.3)
        self.at(self.cue("dört baytlık bir durum raporuyla", 0.9))
        self.play(FadeIn(db), FadeIn(wh, shift=LEFT * 0.08), run_time=0.6)
        self.at(self.cue("yirmi dört bitlik tampon", 5.2))
        self.play(Indicate(db[0], color=BWC, scale_factor=1.04), run_time=0.5)
        self.at(self.cue("dört baytlık birimlerle", 10.1))
        self.play(FadeIn(un, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("altmış dört mebibayt", 13.4))
        self.play(FadeIn(mx, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("ATM başlık hata denetiminin", 17.8))
        self.play(FadeIn(c1, shift=UP * 0.08), Indicate(db[1], color=GOLD), run_time=0.6)
        self.at(self.cue("sıfır elli beş deseniyle", 23.5))
        self.play(FadeIn(c2, shift=UP * 0.08), FadeIn(ne), run_time=0.6)
        self.at(self.cue("her raporu reddeder", 32.2))
        self.play(FadeIn(bad, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # e9 — BIP trailer, one FEC block, short last codeword; SN response 56 → 88 B
        self.beat("e9")
        self.clear(h)
        h = self.show_heading("Burst sonu: BIP ve kısa kod sözcüğü", h)
        y = 1.75
        bu = strip([(1.1, "PSBu", PHC, 0.45), (0.65, "başlık", HLC, 0.3), (0.6, "DBRu", BWC, 0.3), (3.4, "yük · Alloc-ID a", PAYC, 0.15),
                    (0.6, "DBRu", BWC, 0.3), (2.6, "yük · b", PAYC, 0.15), (0.75, "BIP", BIPC, 0.4)], -5.6, y, 0.6, 15)
        fsx0, fsx1 = bu[1].get_left()[0], bu[6].get_right()[0]
        cw_w = (fsx1 - fsx0) / 3.45
        cws = VGroup()
        x = fsx0
        for i in range(3):
            cws.add(strip([(cw_w * 0.87, "216 B", PAYC, 0.18), (cw_w * 0.13, "", PARC, 0.6)], x, 0.65, 0.5, 15))
            x += cw_w
        cws.add(strip([(cw_w * 0.45 - cw_w * 0.13, "kısa", GOLD, 0.3), (cw_w * 0.13, "", PARC, 0.6)], x, 0.65, 0.5, 15))
        cwl = T("FEC açık: ONU'nun bütün tahsisleri tek blok", 16, MUTED, BOLD).next_to(cws, DOWN, buff=0.12).align_to(cws, LEFT)
        shl = T("en fazla 1 kısa sözcük · sonda", 16, GOLD, BOLD).next_to(cws, DOWN, buff=0.12).align_to(cws, RIGHT)
        ex = VGroup(T("Örnek · 10G · kimliği olmayan ONU · SN cevabı", 19, TXT, BOLD), tag("ONU-ID 0x3FF", GOLD, 16)).arrange(RIGHT, buff=0.3).move_to([-0.6, -0.55, 0])
        u = 0.07
        ey = -1.55
        ps = seg(-6.2, 1.3, ey, PHC, "PSBu", 0.6, 0.12, 15, dashed=True)
        hd = seg(-4.6, 4 * u * 2.2, ey, HLC, None, 0.6, 0.35)
        pl = seg(hd[0].get_right()[0], 48 * u, ey, PLDC, "PLOAMu · 48 B", 0.6, 0.25, 16)
        bp = seg(pl[0].get_right()[0], 4 * u * 2.2, ey, BIPC, None, 0.6, 0.4)
        par = seg(bp[0].get_right()[0], 32 * u, ey, PARC, "eşlik · 32 B", 0.6, 0.45, 15)
        hl_ = T("4 B", 15, HLC, BOLD).next_to(hd, UP, buff=0.08)
        bl_ = T("4 B", 15, BIPC, BOLD).next_to(bp, UP, buff=0.08)
        b56 = BraceBetweenPoints(hd[0].get_corner(DL), bp[0].get_corner(DR), DOWN, color=GOLD)
        b56l = T("56 B", 19, GOLD, BOLD).next_to(b56, DOWN, buff=0.04)
        b88 = BraceBetweenPoints(hd[0].get_corner(DL) + DOWN * 0.55, par[0].get_corner(DR) + DOWN * 0.55, DOWN, color=PARC)
        b88l = T("FEC ile 88 B (tek kısa RS(248, 216) sözcüğü)", 18, PARC, BOLD).next_to(b88, DOWN, buff=0.04)
        psl = VGroup(T("+ profilin önsöz", 15, PHC, BOLD), T("ve sınırlayıcısı", 15, PHC, BOLD)).arrange(DOWN, buff=0.04).next_to(ps, DOWN, buff=0.12).align_to(ps, LEFT)
        self.play(self.set_src("G.989.3 §8.1.2.3 · §10.1.3.2 · 56 → 88 B hesaplanmıştır"), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(s_) for s_ in bu], lag_ratio=0.1), run_time=0.8)
        self.at(self.cue("BIP kuyruğuyla biter", 1.0))
        self.play(Indicate(bu[6], color=GOLD, scale_factor=1.15), run_time=0.6)
        self.at(self.cue("tek bir blok olarak kodlanır", 4.7))
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.08) for c in cws[:3]], lag_ratio=0.2), FadeIn(cwl), run_time=0.9)
        self.at(self.cue("en fazla bir kısa kod", 9.6))
        self.play(FadeIn(cws[3], shift=DOWN * 0.08), run_time=0.4)
        self.at(self.cue("burst'ün sonunda", 12.9))
        self.play(FadeIn(shl), Indicate(cws[3], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("kimliği olmayan bir ONU'nun", 15.9))
        self.play(FadeIn(ex, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("Dört bayt başlık", 20.1))
        self.play(FadeIn(hd), FadeIn(hl_), run_time=0.4)
        self.at(self.cue("kırk sekiz bayt PLOAM", 21.6))
        self.play(FadeIn(pl, shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("dört bayt kuyruk", 23.4))
        self.play(FadeIn(bp), FadeIn(bl_), run_time=0.4)
        self.at(self.cue("elli altı bayt", 24.9))
        self.play(FadeIn(b56), FadeIn(b56l), run_time=0.4)
        self.at(self.cue("FEC ile seksen sekiz", 26.1))
        self.play(FadeIn(par, shift=RIGHT * 0.08), FadeIn(b88), FadeIn(b88l), run_time=0.6)
        self.at(self.cue("artı profilin önsözü", 28.3))
        self.play(FadeIn(ps, shift=RIGHT * 0.08), FadeIn(psl), run_time=0.5)
        self.end(pad=0.05)

        # e10 — upstream efficiency vs number of bursts
        self.beat("e10")
        self.clear(h)
        h = self.show_heading("Verimlilik — burst sayısı belirler", h)
        lw = 4.4
        o25 = VGroup(T("2,5G", 18, R25, BOLD), Rectangle(width=lw, height=0.55, stroke_color=R25, stroke_width=2, fill_color=R25, fill_opacity=0.2)).arrange(RIGHT, buff=0.25)
        o10 = VGroup(T("10G", 18, R10, BOLD), Rectangle(width=lw, height=0.55, stroke_color=R10, stroke_width=2, fill_color=R10, fill_opacity=0.2)).arrange(RIGHT, buff=0.25)
        oo = VGroup(o25, o10).arrange(DOWN, aligned_edge=RIGHT, buff=0.35).move_to([-3.6, 1.2, 0])
        o25.add(T("512 bit = 64 B", 18, TXT, BOLD).move_to(o25[1]))
        o10.add(T("2048 bit = 256 B", 18, TXT, BOLD).move_to(o10[1]))
        ot = T("burst başına fiziksel ek yük", 16, MUTED, BOLD).next_to(oo, UP, buff=0.15).align_to(oo[0][1], LEFT)
        same = brace_lbl(VGroup(o25[1], o10[1]), "aynı süre: 205,76 ns", GOLD, DOWN, 18)
        four = pill("10G: 4 × bayt", R10, 18).next_to(same, DOWN, buff=0.25)
        cx0, cy0, ch_ = 1.0, -2.2, 3.7
        Y = lambda p: cy0 + p / 100 * ch_
        axl = VGroup(Line([cx0, cy0, 0], [6.4, cy0, 0], color=MUTED, stroke_width=2), Line([cx0, cy0, 0], [cx0, Y(100), 0], color=MUTED, stroke_width=2))
        yl = VGroup(*[T(f"%{v}", 14, MUTED).next_to([cx0, Y(v), 0], LEFT, buff=0.08) for v in (50, 100)])
        ytk = VGroup(*[Line([cx0 - 0.05, Y(v), 0], [cx0 + 0.05, Y(v), 0], color=MUTED, stroke_width=1.5) for v in (50, 100)])
        bars = VGroup()
        for k, (n, off, on) in enumerate(EFF):
            gx = 2.0 + k * 1.6
            b1 = Rectangle(width=0.55, height=Y(off) - cy0, stroke_width=0, fill_color=ACC, fill_opacity=0.75).move_to([gx - 0.3, (cy0 + Y(off)) / 2, 0])
            b2 = Rectangle(width=0.55, height=Y(on) - cy0, stroke_width=0, fill_color=PARC, fill_opacity=0.75).move_to([gx + 0.3, (cy0 + Y(on)) / 2, 0])
            v1 = T(tr(off), 14, ACC, BOLD).next_to(b1, UP, buff=0.05)
            v2 = T(tr(on), 14, PARC, BOLD).next_to(b2, UP, buff=0.05)
            nl = T(f"{n} ONU", 15, TXT, BOLD).next_to([gx, cy0, 0], DOWN, buff=0.1)
            bars.add(VGroup(b1, b2, v1, v2, nl))
        leg = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=ACC, fill_opacity=0.75), T("FEC kapalı", 15, TXT)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=PARC, fill_opacity=0.75), T("FEC açık", 15, TXT)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.3)
        ctl = T("10G ↑ · yüke kalan pay", 16, MUTED, BOLD)
        VGroup(ctl, leg).arrange(RIGHT, buff=0.35).move_to([3.7, 2.25, 0])
        hl64 = SurroundingRectangle(bars[2], color=GOLD, buff=0.08, stroke_width=3)
        est = interp("türetilmiş · 1 burst / ONU / çerçeve, 1 tahsis + DBRu", GOLD, 15).move_to([-3.6, -2.6, 0])
        msg_ = pill("küçük ve çok burst: ek yükü burst sayısı belirler", GOLD, 18).move_to([-3.6, -1.75, 0])
        self.play(self.set_src("G.989.2 Tablo 11-11 · G.989.3 §8.1.2 · verimlilik hesaplanmıştır (yorum)"), run_time=0.3)
        self.at(self.cue("Burst başına fiziksel ek yük", 2.5))
        self.play(FadeIn(ot), FadeIn(oo), run_time=0.6)
        self.at(self.cue("zaman olarak aynıdır", 4.9))
        self.play(FadeIn(same), run_time=0.4)
        self.at(self.cue("dört kat bayt", 7.8))
        self.play(FadeIn(four, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("altmış dört ONU ile", 11.3))
        self.play(FadeIn(axl), FadeIn(yl), FadeIn(ytk), FadeIn(leg), FadeIn(ctl), FadeIn(est), *[FadeIn(b[4]) for b in bars], run_time=0.6)
        self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], *[FadeIn(b[2]) for b in bars], run_time=0.7)
        self.at(self.cue("yüzde seksen dokuzunu", 15.8))
        self.play(Create(hl64), Indicate(bars[2][2], color=GOLD, scale_factor=1.3), run_time=0.6)
        self.at(self.cue("yüzde yetmiş yedisini", 23.8))
        self.play(*[GrowFromEdge(b[1], DOWN) for b in bars], *[FadeIn(b[3]) for b in bars], run_time=0.7)
        self.at(self.cue("ek yükü FEC değil", 28.7))
        self.play(FadeIn(msg_, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("burst sayısı belirler", 32.7))
        self.play(Indicate(msg_, color=GOLD, scale_factor=1.04), run_time=0.5)
        self.end(pad=0.05)

        # e11 — PMD bridge: PtP WDM management frame
        self.beat("e11")
        self.clear()
        self.set_badge("pmd")
        h = self.show_heading("PMD Köprüsü — PtP WDM yönetim çerçevesi")
        ch = self.chip_at(s1chip(9), h)
        fr = strip([(1.4, "PSB · 24 B", PHC, 0.55), (1.6, "başlık 64 bit", HLC, 0.3), (2.2, "PLOAM · 48 × n", PLDC, 0.22), (5.4, "yük", PAYC, 0.12), (0.9, "BIP", BIPC, 0.35)], -5.75, 1.55, 0.6, 15)
        flex = DoubleArrow([fr.get_left()[0], 2.15, 0], [fr.get_right()[0], 2.15, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12, max_tip_length_to_length_ratio=0.03)
        flexl = T("esnek çerçeve süresi", 16, GOLD, BOLD).next_to(flex, UP, buff=0.04)
        same = T("aynı PSB: PSync · SFC · OC", 15, PHC, BOLD).next_to(fr[0], DOWN, buff=0.12).align_to(fr[0], LEFT)
        hf = fields([("PLOAM sayısı", 8, PLDC), ("yük uzunluğu", 16, PAYC), ("SFC ofseti", 17, SFCC), ("Ind", 10, GOLD), ("HEC", 13, HECC)], 11.6, 0.55, 16, 14, unit=" bit").move_to([0.1, -0.15, 0])
        zl = zoom_lines(fr[1], hf, HLC)
        cA = card("TWDM ↓ senkronu", "SFC: HEC geçerli VE yerel kopya + 1", None, ACC, w=6.0, h=1.15, tsize=19, bsize=18).move_to([-3.2, -2.05, 0])
        cB = card("PtP WDM yönetim senkronu", "SFC: yalnızca HEC geçerli", None, PTPC, w=6.0, h=1.15, tsize=19, bsize=18).move_to([3.2, -2.05, 0])
        nop = T("+ 1 beklenmez", 18, WARN, BOLD).next_to(cB[2], RIGHT, buff=0.25)
        self.play(FadeIn(ch, shift=LEFT * 0.1), self.set_src("G.989.3 §8.2 · §10.2 · Şekil 8-6 / 10-16 / 10-17"), run_time=0.5)
        self.at(self.cue("PtP WDM'in yönetim çerçevesini", 1.6))
        self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.08) for s_ in fr], lag_ratio=0.12), run_time=0.8)
        self.at(self.cue("Aynı senkron bloğu", 7.8))
        self.play(Indicate(fr[0], color=GOLD, scale_factor=1.1), FadeIn(same), run_time=0.6)
        self.at(self.cue("altmış dört bitlik bir başlık", 9.4))
        self.play(Create(zl), FadeIn(hf), run_time=0.7)
        self.at(self.cue("esnek bir çerçeve süresi", 13.6))
        self.play(GrowFromCenter(flex), FadeIn(flexl), run_time=0.5)
        self.at(self.cue("Oradaki senkron makinesi", 16.0))
        self.play(FadeIn(cA, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("yalnızca HEC geçerliliğine", 18.1))
        self.play(FadeIn(cB, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("bir fazla olmasını beklemez", 21.6))
        self.play(FadeIn(nop, shift=LEFT * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # e12 — engineer note; e13 — bridge
        self.note11("e12", [("1", "Koruma süresini G.989.2'den türetin",
                             "Tg ≥ Ton + Tu (verici açma / kapama süreleri) — G.989.3'teki 64 bitten değil.", "koruma süresini G.989.2'deki"),
                            ("2", "↑ FEC profile bağlı: karışık kanal",
                             "Aynı kanalda FEC'li ve FEC'siz ONU'lar — analizör profili her burst için ayrı çözmeli.", "yukarı yön FEC'i burst profiline")])
        self.bridge_beat("e13", "Çerçeveler hazır.\nŞimdi bir çözücüyü standardın kendi vektörleriyle sınayalım.", label="Sıradaki: Laboratuvarda")
        self.save_timeline("ep12_p4C")
