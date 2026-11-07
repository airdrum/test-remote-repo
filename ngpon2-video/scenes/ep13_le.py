"""S2·B3 · Laboratuvarda (başlık çözücü, boş çerçeveler, verim, parçalama, küçük tahsisler, doluluk, anahtar indeksi, hat deseni)
and Kapanış."""
from ep13_common import *

GOLDEN = [["boş · yalnızca başlık", "0", "00", "0xFFFF", "1", "0x0000FFFF0000299E"],
          ["boş · 4 B yük (12 B)", "4", "00", "0xFFFF", "1", "0x0010FFFF0000268D"],
          ["OMCI · ONU-ID 5", "48", "00", "0x0005", "1", "0x00C00005000025A4"],
          ["64 B Ethernet · 1. anahtar", "64", "01", "0x0400", "1", "0x01010400000030E3"],
          ["1000 B · ilk parça", "1000", "00", "0x0400", "0", "0x0FA0040000001C48"]]
GOODPUT = [["10G · FEC kapalı", "8,845", "9,366", "9,798", "9,886", "9,942"],
           ["10G · FEC açık", "7,704", "8,157", "8,533", "8,610", "8,659"],
           ["2,5G · FEC kapalı", "2,210", "2,340", "2,448", "2,469", "2,483"],
           ["2,5G · FEC açık", "2,067", "2,188", "2,289", "2,310", "2,323"]]


class E13LabA(Act13):
    HDR, MANIFEST, FIRST = H13["L"], M13("lab"), True

    def construct(self):
        # g1 — bench
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Başlıklar, boş çerçeveler, parçalama ve verim")
        self.at(self.cue("Düzenek", 1.2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Düzenek")
        pa = pa_icon(2.4, 1.6, "Protokol analizörü · ↓ ↑").move_to([-4.8, 1.2, 0])
        em = emu_icon(2.4, 1.6, "OLT emülatörü · BWmap").move_to([-1.6, 1.2, 0])
        tg = tg_icon(2.4, 1.6, "Trafik üreteci · 64 … 9000 B").move_to([1.6, 1.2, 0])
        dut = onu_box("ONU (DUT)", ONUC, 1.9, 0.75, 18).move_to([4.9, 1.3, 0])
        vec = VGroup(T("standardın hazır vektörleri:", 18, MUTED, BOLD), tag("Ek A · HEC sözcükleri (Tablo A.2 / A.3)", GOLD, 17),
                     tag("Ek IV · örnekler", GOLD, 17)).arrange(RIGHT, buff=0.3).move_to([0, -1.05, 0])
        fit(vec, 12.6)
        rest = VGroup(interp("yorum", GOLD, 15), T("diğer yöntemler: mühendislik pratiği", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.1, 0])
        self.at(self.cue("iki yönü izleyen bir protokol", 1.8))
        self.play(self.set_src("G.989.3 Ek A · Ek IV · tezgâh ve yöntemler: yorum"), FadeIn(pa, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("harita yazan bir OLT", 5.2))
        self.play(FadeIn(em, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("altmış dört ile dokuz bin bayt", 7.8))
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("ve sınanan ONU", 13.8))
        self.play(FadeIn(dut, shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("Standardın verdiği hazır", 15.0))
        self.play(FadeIn(vec[0]), LaggedStart(*[FadeIn(v, shift=UP * 0.06) for v in vec[1:]], lag_ratio=0.3), run_time=0.8)
        self.at(self.cue("diğer yöntemler mühendislik", 22.7))
        self.play(FadeIn(rest, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # g2 — TEST 1: header decoder with our golden headers; 1/2/3-bit flips
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "Başlık çözücü — altın başlıklar")
        tb = mtable(["durum", "PLI", "KI", "Port-ID", "LF", "64 bit başlık"], GOLDEN, [3.5, 0.95, 0.8, 1.45, 0.6, 4.3], size=17, hsize=15, row_h=0.42,
                    mono=(1, 2, 3, 4, 5)).move_to([0, 0.95, 0])
        for r in tb[1:]:
            r[6].set_color(GOLD)
        hk = tag("hesap · standartta yok", GOLD, 15).next_to(tb, UP, buff=0.1).align_to(tb, RIGHT)
        r1 = glow(tb[1], IDC, 0.03)
        grp = VGroup(*[HX(s, 34, TXT, BOLD) for s in ("0000", "FFFF", "0000", "299E")]).arrange(RIGHT, buff=0.45).move_to([0.4, -1.1, 0])
        ox = T("0x", 26, MUTED, BOLD).next_to(grp, LEFT, buff=0.2)
        fl = VGroup(VGroup(tag("1 bit çevir", MUTED, 16), T("→ düzeltilir", 17, GOOD, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.12),
                    VGroup(tag("2 bit", MUTED, 16), T("→ düzeltilir", 17, GOOD, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.12),
                    VGroup(tag("3 bit · eşlik ✗", WARN, 16), T("→ yükün kalanı atılır · HEC sayacı +1", 17, WARN, BOLD)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.45)
        fl.move_to([0, -2.35, 0])
        fit(fl, 12.6)
        self.at(self.cue("Kendi altın başlıklarımızı", 1.9))
        self.play(self.set_src("G.989.3 Ek A · §9.2 · Tablo 14-1 · altın başlıklar: hesap"), FadeIn(tb[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[1:]], lag_ratio=0.15), run_time=1.0)
        self.at(self.cue("standartta yoklar", 4.9))
        self.play(FadeIn(hk), run_time=0.3)
        self.at(self.cue("yalnızca başlıktan oluşan", 6.5))
        self.play(Create(r1), run_time=0.5)
        self.at(self.cue("on altılık tabanda", 10.7))
        self.play(FadeIn(ox), run_time=0.3)
        self.at(self.cue_n("sıfır sıfır sıfır sıfır", 1, 12.3))
        self.play(FadeIn(grp[0], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue("ef ef ef ef", 14.3))
        self.play(FadeIn(grp[1], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue_n("sıfır sıfır sıfır sıfır", 2, 15.4))
        self.play(FadeIn(grp[2], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue("iki dokuz dokuz e", 17.4))
        self.play(FadeIn(grp[3], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue("Sonra bir", 18.9))
        self.play(FadeIn(fl[0][0]), run_time=0.3)
        self.at(self.cue("iki ve üç bit çevirin", 19.8))
        self.play(FadeIn(fl[1][0]), FadeIn(fl[2][0]), run_time=0.4)
        self.at(self.cue("bir ve iki bit düzeltilmeli", 21.6))
        self.play(FadeIn(fl[0][1:]), FadeIn(fl[1][1:]), run_time=0.4)
        self.at(self.cue("eşlik hatalı üç bit ise", 24.0))
        self.play(FadeIn(fl[2][1], shift=LEFT * 0.06), run_time=0.4)
        self.end(pad=0.05)

        # g3 — TEST 2: idle with PLI 4 must skip 12 B; count idles on an empty channel (10G FEC off)
        self.beat("g3")
        self.clear(h)
        h = step_head(self, 2, "Boş çerçeveler", h)
        p = apanel(6.0, 2.3, "Analizör · enjekte edilen boş çerçeve", IDC).move_to([-3.4, 1.0, 0])
        rows = VGroup(kv("Port-ID", "0xFFFF · boş", kw=2.3), kv("PLI", "4", kw=2.3), kv("sonraki başlık", "+12 B", kw=2.3, vcolor=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows.move_to(p[0]).shift(DOWN * 0.15)
        no16 = VGroup(T("+16 B değil", 17, WARN, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.1).next_to(rows[2], RIGHT, buff=0.3)
        cfg = VGroup(tag("trafiksiz kanal", MUTED, 16), T("10G · FEC kapalı · FS yükü 155 488 B", 17, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cfg.move_to([0.2, 1.5, 0], aligned_edge=LEFT)
        bw = 12.0

        def idle_bar(n, y):
            g = VGroup()
            w = bw / n
            for i in range(n):
                g.add(VGroup(seg(-6.0 + i * w, 0.12, y, IDC, None, 0.5, 0.55), seg(-6.0 + i * w + 0.12, w - 0.12, y, IDC, None, 0.5, 0.12)))
            return g
        b10 = idle_bar(10, -0.95)
        b18 = idle_bar(18, -2.25)
        l10 = T("en büyük boş yük 16 380 B → en az 10 boş çerçeve", 17, TXT, BOLD).next_to(b10, UP, buff=0.1).align_to(b10, LEFT)
        l18 = T("en büyük boş yük 9000 B → en az 18 boş çerçeve", 17, TXT, BOLD).next_to(b18, UP, buff=0.1).align_to(b18, LEFT)
        hk3 = tag("hesap", GOLD, 15).next_to(l10, RIGHT, buff=0.3)
        self.at(self.cue("Göstergesi dört olan bir boş", 2.3))
        self.play(self.set_src("G.989.3 §9.1.4 · Tablo 8-1 · sayılar: hesap"), FadeIn(p), FadeIn(rows[:2], shift=RIGHT * 0.06), run_time=0.6)
        self.at(self.cue("çözücü on altı değil", 6.5))
        self.play(FadeIn(no16, shift=LEFT * 0.06), run_time=0.4)
        self.at(self.cue("on iki bayt atlamalıdır", 8.2))
        self.play(FadeIn(rows[2], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("Sonra trafiksiz bir kanalda", 10.3))
        self.play(FadeIn(cfg[0]), run_time=0.4)
        self.at(self.cue("on gigabitte FEC kapalıyken", 15.8))
        self.play(FadeIn(cfg[1:], shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("en büyük boş yük on altı bin", 18.2))
        self.play(FadeIn(l10), FadeIn(hk3), LaggedStart(*[FadeIn(s) for s in b10], lag_ratio=0.08), run_time=0.8)
        self.at(self.cue("dokuz bin baytsa en az on sekiz", 23.2))
        self.play(FadeIn(l18), LaggedStart(*[FadeIn(s) for s in b18], lag_ratio=0.05), run_time=0.8)
        self.end(pad=0.05)

        # g4 — TEST 3: downstream goodput sweep vs frame size
        self.beat("g4")
        self.clear(h)
        h = step_head(self, 3, "Verim taraması — ↓", h)
        tb = mtable(["yapılandırma", "64 B", "128 B", "512 B", "1518 B", "9000 B"], GOODPUT, [2.9, 1.6, 1.6, 1.6, 1.6, 1.6], size=19, hsize=16, row_h=0.55,
                    mono=(1, 2, 3, 4, 5)).move_to([-0.4, 0.75, 0])
        for k, r in enumerate(tb[1:]):
            r[1].set_color(R10 if k < 2 else R25)
        sub = VGroup(T("Gbit/s · Ethernet baytı (DA … FCS) · en hafif FS başlığı (N = 0, P = 0) · §9.3 ↓ kuralları", 15, MUTED, BOLD), tag("hesap", GOLD, 15)).arrange(RIGHT, buff=0.2)
        sub.next_to(tb, DOWN, buff=0.15).align_to(tb, LEFT)
        fit(sub, 12.6)
        g = [glow(tb[1][2], GOLD, 0.03), glow(tb[1][5], GOLD, 0.03), glow(tb[2][2], GOLD, 0.03), glow(tb[2][5], GOLD, 0.03)]
        cmp_ = VGroup(T("karşılaştır:", 18, MUTED, BOLD), tag("Tablo 14-1 · boş olmayan XGEM baytları (Z)", GOOD, 16)).arrange(RIGHT, buff=0.2).move_to([0, -2.55, 0])
        self.at(self.cue("Aşağı yönde altmış dört ile", 2.3))
        self.play(self.set_src("G.989.3 §9.3 · Tablo 8-1 · Tablo 14-1 · değerler: hesap"), FadeIn(tb[0]), run_time=0.5)
        self.at(self.cue("en hafif başlıkla", 9.1))
        self.play(FadeIn(sub), run_time=0.4)
        self.at(self.cue("on gigabitte FEC kapalıyken altmış", 10.6))
        self.play(FadeIn(tb[1], shift=UP * 0.05), Create(g[0]), run_time=0.6)
        self.at(self.cue("bin beş yüz on sekiz baytta dokuz", 16.9))
        self.play(Create(g[1]), run_time=0.4)
        self.at(self.cue("FEC açıkken yedi virgül", 22.4))
        self.play(FadeIn(tb[2], shift=UP * 0.05), Create(g[2]), Create(g[3]), run_time=0.6)
        self.play(FadeIn(tb[3], shift=UP * 0.05), FadeIn(tb[4], shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("boş olmayan bayt sayaçlarıyla", 28.9))
        self.play(FadeIn(cmp_, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep13_labA")


class E13LabB(Act13):
    HDR, MANIFEST, PREV_BADGE = H13["L"], M13("lab"), "lab"

    def construct(self):
        # g5 — 64-byte frame rate vs one 10 Gbit/s Ethernet generator port
        self.beat("g5")
        h = step_head(self, 3, "Verim taraması — 64 B çerçeve hızı")
        s = 0.42
        x0 = -2.8
        rows = [("10G ↓ · FEC kapalı", 17.28, R10), ("10G ↓ · FEC açık", 15.05, R10), ("10 Gbit/s Ethernet portu", 14.88, MUTED)]
        bars = VGroup()
        for k, (lab, v, c) in enumerate(rows):
            y = 1.45 - k * 0.8
            b = Rectangle(width=v * s, height=0.48, stroke_width=0, fill_color=c, fill_opacity=0.75).move_to([x0 + v * s / 2, y, 0])
            l = T(lab, 17, TXT, BOLD).next_to(b, LEFT, buff=0.25)
            n = T(f"{tr(v)} M/s", 19, c if c != MUTED else TXT, BOLD).next_to(b, RIGHT, buff=0.2)
            bars.add(VGroup(l, b, n))
        hk = VGroup(tag("hesap", GOLD, 15), T("Ethernet portu: 10¹⁰ / (84 × 8) — 10 Gbit/s varsayımı (yorum)", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.2)
        hk.next_to(bars, DOWN, buff=0.2).align_to(bars, LEFT)
        y = -1.95
        tg = tg_icon(1.9, 1.25, "üreteç").move_to([-5.3, y + 0.1, 0])
        prt = VGroup(*[arrow([-4.2, y + 0.25 - 0.3 * i, 0], [-2.6, y + 0.1, 0], R10, 2.2, 0.1) for i in range(2)])
        comb = tile("birleştir", MUTED, 1.4, 0.5, 15, 0.12).move_to([-1.85, y + 0.1, 0])
        olt = tile("OLT ↓ · PON", OLTC, 1.7, 0.5, 15, 0.15).move_to([0.3, y + 0.1, 0])
        ca = arrow(comb.get_right(), olt.get_left(), MUTED, 2.2, 0.12)
        msg = VGroup(VGroup(interp("çıkarım", GOLD, 15), T("küçük paketlerde: birden fazla port", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                     T("yoksa ölçtüğünüz şey üreteçtir", 17, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(olt, RIGHT, buff=0.35)
        fit(msg, 6.9 - olt.get_right()[0] - 0.4)
        msg.next_to(olt, RIGHT, buff=0.35)
        self.at(self.cue("altmış dört baytta bu", 0.6))
        self.play(self.set_src("hesap (§9.3 ↓ modeli) · Ethernet portu hızı: varsayım"), FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), run_time=0.6)
        self.at(self.cue("saniyede on yedi milyondan", 2.4))
        self.play(FadeIn(bars[0][2], shift=LEFT * 0.06), FadeIn(bars[1]), run_time=0.6)
        self.at(self.cue("tek bir on gigabitlik Ethernet", 6.1))
        self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]), FadeIn(hk), run_time=0.7)
        self.at(self.cue("küçük paketlerde aşağı yönü", 14.7))
        self.play(FadeIn(tg), *[GrowArrow(a) for a in prt], FadeIn(comb), GrowArrow(ca), FadeIn(olt), FadeIn(msg[0]), run_time=0.9)
        self.at(self.cue("yoksa ölçtüğünüz şey", 21.2))
        self.play(FadeIn(msg[1], shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.05)

        # g6 — TEST 4: DS fragmentation seen on the analyzer
        self.beat("g6")
        self.clear(h)
        h = step_head(self, 4, "↓ parçalama — analizörde", h)
        st = VGroup(tag("1518 B akış", R10, 16), tag("9000 B akış", R10, 16)).arrange(RIGHT, buff=0.25).move_to([-4.3, 1.65, 0])
        y = 0.55
        fk = strip([P_(0.6, "…"), H_(0.32), P_(1.6, "SDU"), H_(0.32), P_(2.2, "X · parça 1"), FS_(0.5, "BIP", BIPC)], -6.2, y, 0.55, 15)
        fk1 = strip([FS_(0.65, "FS b."), H_(0.32), P_(1.7, "X · parça 2"), H_(0.32), P_(1.4, "SDU"), P_(0.5, "…")], 0.0, y, 0.55, 15)
        l0 = tag("LF 0", LFC, 14).next_to(fk[4], UP, buff=0.06)
        l1 = tag("LF 1 · aynı Port-ID", LFC, 14).next_to(fk1[2], UP, buff=0.06)
        full = VGroup(ok_x(True, 18), T("yük sonuna kadar, dolgusuz", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.08).next_to(fk[4], DOWN, buff=0.1)
        an = VGroup(Triangle(color=GOOD, fill_color=GOOD, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI), T("devam ilk sırada", 15, GOOD, BOLD))
        an.arrange(RIGHT, buff=0.08).next_to(fk1[1:3], DOWN, buff=0.1)
        cnt = VGroup(tag("Tablo 14-1 · LF = 0 iletilen XGEM çerçevesi sayısı (İ)", MUTED, 16), T("≈ 8000 / s", 22, GOLD, BOLD), tag("benzetim", GOLD, 15)).arrange(RIGHT, buff=0.25).move_to([0, -1.05, 0])
        fit(cnt, 12.6)
        ghost = strip([P_(0.6, "…"), H_(0.32), P_(2.0, "SDU"), (0.85, "4 × 00", PADC, 0.45), FS_(0.5, "BIP", BIPC)], -2.2, -2.3, 0.5, 15)
        gx = xmark(ghost[3], WARN, 4)
        gl = T("↓ yük asla kısa boşla bitmez", 17, WARN, BOLD).next_to(ghost, LEFT, buff=0.3)
        self.at(self.cue("Bin beş yüz on sekiz ve dokuz", 3.0))
        self.play(self.set_src("G.989.3 §9.3 · §9.1.4 · Tablo 14-1 · ≈ 8000/s: benzetim"), FadeIn(st, shift=RIGHT * 0.06), run_time=0.5)
        self.at(self.cue("her çerçevenin son XGEM", 7.3))
        self.play(FadeIn(fk), FadeIn(l0), run_time=0.5)
        self.play(FadeIn(full, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("aynı porttan devamla", 16.8))
        self.play(FadeIn(fk1, shift=RIGHT * 0.08), FadeIn(l1), FadeIn(an), run_time=0.6)
        self.at(self.cue("Bizim benzetimimize göre", 19.6))
        self.play(FadeIn(cnt, shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("Aşağı yön yükü asla kısa", 26.0))
        self.play(FadeIn(ghost), Create(gx), FadeIn(gl), run_time=0.6)
        self.end(pad=0.05)

        # g7 — TEST 5: tiny 2.5G grants with DBRu
        self.beat("g7")
        self.clear(h)
        h = step_head(self, 5, "Küçük tahsisler — 2,5G, DBRu istenmiş", h)
        em = emu_icon(2.1, 1.4, "OLT emülatörü").move_to([-5.3, 0.6, 0])
        D = ("D", BWC, 0.45)
        wsets = [[D], [D, ("00", PADC, 0.45)], [D, ("H", IDC, 0.55), ("", IDC, 0.55)], [D, ("H", IDC, 0.55), ("", IDC, 0.55), ("", IDC, 0.12)]]
        exp = ["yalnızca DBRu", "kısa boş (4 × 00)", "boş · PLI 0", "boş · PLI 4"]
        rws = VGroup()
        for k, (ws, e) in enumerate(zip(wsets, exp)):
            yy = 1.55 - k * 0.68
            gs = T(f"GrantSize {k + 1}", 17, R25, BOLD).move_to([-3.6, yy, 0], aligned_edge=LEFT)
            wd = words(ws, 0.48, 0.4, 14).move_to([-1.2, yy, 0], aligned_edge=LEFT)
            ex = T(e, 18, TXT, BOLD).move_to([1.4, yy, 0], aligned_edge=LEFT)
            rws.add(VGroup(gs, wd, ex))
        lg = T("D = DBRu · 1 kare = 4 B", 15, MUTED, BOLD).next_to(rws, UP, buff=0.12).align_to(rws, LEFT)
        q = VGroup(tag("kuyrukta", MUTED, 16), tile("1518 B", R10, 1.4, 0.48, 16, 0.2), T("→ < 16 B yükte parçalama yok", 18, WARN, BOLD), ok_x(False, 20)).arrange(RIGHT, buff=0.25).move_to([0, -1.9, 0])
        self.at(self.cue("Emülatörle iki buçuk", 2.5))
        self.play(self.set_src("G.989.3 §8.1.1.2.4 · §9.1.4 · §9.3 · beklenen çözümler: hesap"), FadeIn(em, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("üç ve dört sözcüklük", 6.9))
        self.play(FadeIn(lg), LaggedStart(*[FadeIn(VGroup(r[0], r[1]), shift=RIGHT * 0.06) for r in rws], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("sırasıyla yalnızca rapor", 10.1))
        self.play(FadeIn(rws[0][2], shift=LEFT * 0.06), run_time=0.4)
        self.at(self.cue("kısa boş çerçeve", 12.2))
        self.play(FadeIn(rws[1][2], shift=LEFT * 0.06), run_time=0.4)
        self.at(self.cue("göstergesi sıfır ve dört", 13.6))
        self.play(FadeIn(rws[2][2], shift=LEFT * 0.06), FadeIn(rws[3][2], shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("Kuyrukta bin beş yüz on sekiz", 18.5))
        self.play(FadeIn(q[:2], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("on altı bayttan küçük bir yükte", 23.6))
        self.play(FadeIn(q[2:], shift=LEFT * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # g8 — TEST 6: BufOcc vs received bytes
        self.beat("g8")
        self.clear(h)
        h = step_head(self, 6, "Doluluk ve başlık", h)
        tb = mtable(["kuyruk", "BufOcc (sözcük)", "× 4 (B)", "+ 8 B / SDU", "alınan (B)"], [["10 × 64 B", "160", "640", "+ 80", "720"], ["1 × 1518 B", "380", "1520", "+ 8", "1528"]],
                    [2.4, 2.4, 1.6, 2.0, 1.8], size=19, hsize=16, row_h=0.6, mono=(1, 2, 3, 4)).move_to([-0.6, 0.6, 0])
        hk = tag("hesap · (8-1), (9-1)", GOLD, 15).next_to(tb, UP, buff=0.1).align_to(tb, RIGHT)
        f = pill("alınan bayt = 4 × BufOcc + 8 × SDU sayısı", GOLD, 21).move_to([0, -1.6, 0])
        self.at(self.cue("ONU'ya bilinen bir kuyruk", 2.6))
        self.play(self.set_src("G.989.3 (8-1) · §8.1.2.2.1 · (9-1) · hesap"), FadeIn(tb[0]), FadeIn(hk), run_time=0.5)
        self.at(self.cue("on tane altmış dört baytlık", 5.5))
        self.play(FadeIn(tb[1][:3], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("tek bir bin beş yüz on sekiz", 10.0))
        self.play(FadeIn(tb[2][:3], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Sonra bir sonraki tahsiste", 16.8))
        self.play(FadeIn(tb[1][3:], shift=UP * 0.05), FadeIn(tb[2][3:], shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("raporun dört katını", 20.5))
        self.play(FadeIn(f, shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep13_labB")


class E13LabC(Act13):
    HDR, MANIFEST, PREV_BADGE = H13["L"], M13("lab"), "lab"

    def construct(self):
        # g9 — TEST 7: key index handling; decryptor against App IV.6 / IV.7
        self.beat("g9")
        h = step_head(self, 7, "Anahtar indeksi")
        inj = VGroup(*[VGroup(tag("enjekte", MUTED, 15), T(s, 18, TXT, BOLD)).arrange(RIGHT, buff=0.2) for s in
                       ("KI = 11 (ayrılmış)", "KI → kurulmamış bir anahtar", "KI ≠ 00 · şifre için yapılandırılmamış port")])
        inj.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-6.2, 1.0, 0], aligned_edge=LEFT)
        res = VGroup(VGroup(T("yük atılır", 19, WARN, BOLD), ok_x(False, 20)).arrange(RIGHT, buff=0.12),
                     VGroup(tag("XGEM anahtar hatası sayısı (Z)", GOLD, 16), T("+1", 22, WARN, BOLD)).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        res.move_to([3.6, 1.0, 0])
        br = Brace(inj, RIGHT, color=MUTED).next_to(inj, RIGHT, buff=0.2)
        ra = arrow(br.get_right() + RIGHT * 0.1, res.get_left() + LEFT * 0.1, MUTED, 2.2, 0.12)
        vv = VGroup(T("şifre çözücüyü doğrula:", 18, MUTED, BOLD), tag("Ek IV.6 · ↓ · IFC = 120 (0x0078)", GOLD, 17), tag("Ek IV.7 · ↑ · IFC = 2428 (0x097c)", GOLD, 17))
        vv.arrange(RIGHT, buff=0.3).move_to([0, -1.55, 0])
        fit(vv, 12.6)
        vok = T("bayt bayt aynı olmalı", 17, GOOD, BOLD).next_to(vv, DOWN, buff=0.2)
        self.at(self.cue("İndeksi bir bir olan", 2.4))
        self.play(self.set_src("G.989.3 §9.1.2 · §15.5 · Tablo 14-1 · Ek IV.6 / IV.7"), FadeIn(inj[0], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("kurulmamış bir anahtarı", 4.2))
        self.play(FadeIn(inj[1], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("ya da şifre için yapılandırılmamış", 7.0))
        self.play(FadeIn(inj[2], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("yük atılmalı", 14.6))
        self.play(GrowFromCenter(br), GrowArrow(ra), FadeIn(res[0], shift=LEFT * 0.06), run_time=0.6)
        self.at(self.cue("zorunlu anahtar hatası sayacı", 15.7))
        self.play(FadeIn(res[1], shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("Sonra şifre çözücüyü dördüncü", 19.1))
        self.play(FadeIn(vv[0]), run_time=0.4)
        self.at(self.cue("aşağı yönde çerçeve içi sayaç", 24.2))
        self.play(FadeIn(vv[1], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("yukarı yönde iki bin dört yüz", 27.5))
        self.play(FadeIn(vv[2], shift=UP * 0.06), FadeIn(vok), run_time=0.5)
        self.end(pad=0.05)

        # g10 — TEST 8: line-pattern stress (our method)
        self.beat("g10")
        self.clear(h)
        h = step_head(self, 8, "Hat deseni", h)
        ip = VGroup(interp("yöntem: yorum", GOLD, 15), T("Ek I'in gövdesi elimizde yok", 17, MUTED, BOLD)).arrange(RIGHT, buff=0.2).move_to([-6.2, 1.85, 0], aligned_edge=LEFT)
        fl = VGroup(tile("PSBd · SFC", PHC, 1.8, 0.55, 16, 0.25), tile("karıştırıcı modeli", PHC, 2.3, 0.55, 16, 0.15), tile("k (konum)", GOLD, 1.7, 0.55, 16, 0.2),
                    tile("şifresiz boş / çoklu yayın yük = k", SAC, 3.9, 0.55, 15, 0.15), tile("hat: uzun dizi", TW_DS, 2.0, 0.55, 16, 0.15)).arrange(RIGHT, buff=0.3).move_to([0, 0.75, 0])
        fit(fl, 12.6)
        fa = VGroup(*[arrow(fl[i].get_right(), fl[i + 1].get_left(), MUTED, 2, 0.1) for i in range(4)])
        fsub = T("x⁵⁸ + x³⁹ + 1 · §10.1.4 (S2·B2)", 14, MUTED, BOLD).next_to(fl[1], DOWN, buff=0.08)
        X = lambda v: -5.6 + v / 150 * 11.0
        ya = -1.6
        ax = Line([X(0), ya, 0], [X(150), ya, 0], color=MUTED, stroke_width=2)
        ok_r = Rectangle(width=X(72) - X(0), height=0.5, stroke_width=0, fill_color=GOOD, fill_opacity=0.2).move_to([(X(0) + X(72)) / 2, ya + 0.3, 0])
        mg_r = Rectangle(width=X(150) - X(72), height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.15).move_to([(X(72) + X(150)) / 2, ya + 0.3, 0])
        m72 = VGroup(Line([X(72), ya - 0.1, 0], [X(72), ya + 0.65, 0], color=GOLD, stroke_width=3), T("72 bit", 17, GOLD, BOLD).next_to([X(72), ya, 0], DOWN, buff=0.12))
        z = T("0", 15, MUTED, BOLD).next_to([X(0), ya, 0], DOWN, buff=0.12)
        axl = T("özdeş bit dizisi uzunluğu", 15, MUTED, BOLD).next_to(ax, DOWN, buff=0.12).align_to(ax, RIGHT)
        okl = T("ONU senkronu ve BER korunmalı", 16, GOOD, BOLD).move_to(ok_r)
        fit(okl, ok_r.width - 0.2)
        mgl = T("daha uzun → payı ölç", 16, GOLD, BOLD).move_to(mg_r)
        self.at(self.cue("Bu yöntem bizimdir", 2.2))
        self.play(self.set_src("G.989.2 Tablo 11-4 / 11-5 · G.989.3 §10.1.4 · yöntem: yorum"), FadeIn(ip[0]), run_time=0.3)
        self.at(self.cue("çünkü birinci ekin gövdesi", 3.8))
        self.play(FadeIn(ip[1]), run_time=0.4)
        self.at(self.cue("A ekindeki karıştırıcı modeliyle", 7.1))
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.05) for t in fl[:3]], lag_ratio=0.25), GrowArrow(fa[0]), GrowArrow(fa[1]), FadeIn(fsub), run_time=0.9)
        self.at(self.cue("ve şifresiz bir boş ya da çoklu", 16.4))
        self.play(GrowArrow(fa[2]), FadeIn(fl[3]), GrowArrow(fa[3]), FadeIn(fl[4]), run_time=0.7)
        self.at(self.cue("Yetmiş iki bite kadar dizilerde", 21.6))
        self.play(Create(ax), FadeIn(z), FadeIn(axl), FadeIn(ok_r), FadeIn(m72), FadeIn(okl), run_time=0.7)
        self.at(self.cue("daha uzunlarda payınızı", 27.9))
        self.play(FadeIn(mg_r), FadeIn(mgl), run_time=0.5)
        self.end(pad=0.05)

        # g11 — lab note
        self.note11("g11", [("1", "Test planını zorunlu sayaçlara dayandırın",
                             "XGEM sayaçlarının çoğu isteğe bağlı · zorunlular: HEC hata sayısı,\nanahtar hatası sayısı, boş olmayan bayt sayaçları (Tablo 14-1).", "XGEM sayaçlarının çoğu"),
                            ("2", "Her verim ölçümünü FEC durumuyla kaydedin",
                             "10G'de aynı akış FEC açıkken ≈ %13 daha az taşır.", "her verim ölçümünü")], badge="lab")
        self.wait(0.3)
        self.clear()
        self.save_timeline("ep13_labC")


POINTS = [("XGEM başlığı 8 B: PLI · KI · Port-ID · Options · LF · HEC\ndolu yük 4'e yuvarlanır, en az 8 B · boş çerçevede PLI = gerçek boy", "§9.1"),
          ("Sınırlama aramaz: her yük bölümü bir başlıkla başlar;\nbozuk başlık bölümün kalanını götürür", "§9.2"),
          ("↓ en çok iki parça · ↑ parçalar Alloc-ID içinde sıralı;\ndevir beklerken yeni bölme yok", "§9.3"),
          ("Yalnızca Ethernet ve MPLS eşlenir: önsöz atılır, FCS kalır;\nOMCI varsayılan portta", "§9.4"),
          ("Şifre yalnızca yükü kapsar; anahtar akışı\nbaşlığın çerçevedeki konumuna bağlı", "§15.4")]


class E13End(Act13):
    HDR, MANIFEST, FIRST = H13["E"], M13("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header(tc)
        self.set_badge("ozet")
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 21, TXT, line_spacing=0.85), 9.6)
            ch = tag(c, GOLD, 17)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.75, -2.35, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.7, y, 0])
        for k, (key, d) in enumerate((("XGEM başlığı sekiz bayttır", 1.5), ("sınırlama hiç aramaz", 18.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((2, 3, 4), (("aşağı yönde bir birim en çok", 0.2), ("yalnızca Ethernet ve etiket", 12.5), ("şifre yalnızca yükü kapsar", 22.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("1518 B'lık Ethernet çerçevesi\ntek XGEM çerçevesinde ↓:\nPLI, dolgu, toplam boy?\nÖnsöze ne olur?", CH[0]),
            ("Kuyruğunda 1518 B olan\n2,5G ONU, DBRu istenen\n4 sözcüklük tahsiste\nne gönderir?", CH[1]),
            ("PLI = 4 olan boş çerçeveden\nsonraki başlık kaç bayt ileride?\nDört sıfır baytı neden\nyalnızca ONU gönderir?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 13.0), ("Üçüncü soru", 22.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 39.3))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: Paylaşım (DBA)
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e4 = SERIES["season2"]["episodes"][3]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e4['n']} · {e4['title']}", 50, TXT, BOLD), T(e4["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.1)
        fit(nxt[1], 12.6)
        y = -1.55
        onus = VGroup(*[onu_box(f"ONU {i + 1}", ONUC, 1.2, 0.5, 15) for i in range(3)]).arrange(DOWN, buff=0.15).move_to([-4.6, y, 0])
        dba = sbox("OLT · DBA", "tahsis", OLTC, 2.0, 0.85, 19, 14).move_to([0, y, 0])
        up = VGroup(*[arrow(o.get_right(), dba.get_left(), BWC, 2, 0.1) for o in onus])
        upl = T("DBRu · trafik izleme", 15, BWC, BOLD).next_to(up, UP, buff=0.05)
        bm = strip([FS_(0.9, "BWmap", BWC), (1.0, "A", ACC, 0.25), (0.8, "B", PINK, 0.25), (1.2, "C", GOLD, 0.25)], 1.6, y, 0.55, 15)
        bma = arrow(dba.get_right(), bm.get_left(), MUTED, 2, 0.1)
        tg_ = VGroup(tag("iş birlikli tahsis · düşük gecikme", ACC, 15), tag("çekişmeli tahsis", GOLD, 15)).arrange(RIGHT, buff=0.2).next_to(bm, DOWN, buff=0.2)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("Kaynak tahsisi ve dinamik", 2.3))
        self.play(FadeIn(nxt[2]), FadeIn(dba), run_time=0.5)
        self.at(self.cue("durum raporları ve trafik", 6.4))
        self.play(FadeIn(onus), *[GrowArrow(a) for a in up], FadeIn(upl), GrowArrow(bma), FadeIn(bm, shift=RIGHT * 0.08), run_time=0.8)
        self.at(self.cue("düşük gecikme için iş birlikli", 9.2))
        self.play(FadeIn(tg_[0], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("ve çekişmeli tahsisler", 12.4))
        self.play(FadeIn(tg_[1], shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(onus, dba, up, upl, bm, bma, tg_)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP13['n']} · {EP13['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep13_end")
