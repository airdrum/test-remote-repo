"""B10 · Perde 3 (uyumluluk: test matrisi) and Perde 4 (bir ONU'nun hayatı)."""
from ep10_common import *

ODNC, LAMC, TUNC, SELC, CORE, SIDE = "#FB923C", CH[1], PINK, WARN, ACC, "#A78BFA"
PROF_C = "#A78BFA"


def tile_row(labels, x0, y, color, w=1.0, h=0.48, step=1.1, size=16, subs=None, ssize=14):
    g = VGroup()
    for i, s in enumerate(labels):
        t = tile(s, color, w, h, size)
        t.move_to([x0 + i * step, y, 0])
        if subs:
            t.add(tf(subs[i], ssize, color, SEMIBOLD, w=step).next_to(t[0], DOWN, buff=0.06))
        g.add(t)
    return g


def glabel(s, y, color, x=-6.55, size=19):
    return T(s, size, color, BOLD).move_to([x, y, 0], aligned_edge=LEFT)


# ================================ PERDE 3 ======================================
class E10P3A(Act10):
    HDR, MANIFEST, FIRST = H10[3], M10("p3"), True

    def construct(self):
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Uyumluluk: test matrisi")
        self.at(self.cue("Bu sezon G.989.2", 1.6))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("Kaç tablo?")

        def block(n, cols, color, dashed=False, labels=None):
            g = VGroup()
            for i in range(n):
                if dashed:
                    sq = VGroup(DashedVMobject(Square(0.5, stroke_color=color, stroke_width=2), num_dashes=16))
                else:
                    sq = VGroup(Square(0.5, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.25))
                if labels:
                    sq.add(tf(labels[i], 14, color, BOLD, w=0.46).move_to(sq[0]))
                g.add(sq)
            return g.arrange_in_grid(cols=cols, buff=0.12, flow_order="rd")
        bm = block(19, 5, ACC).move_to([-4.2, 0.4, 0])
        ba = block(23, 6, CH[1]).move_to([0.4, 0.4, 0])
        bf = block(6, 2, GOLD, True, ["11-7", "11-8", "11-9", "A.3", "A.4", "A.5"]).move_to([4.75, 0.4, 0])
        lm = T("19 · ana metin", 22, ACC, BOLD).next_to(bm, UP, buff=0.3)
        la = T("23 · ekler", 22, CH[1], BOLD).next_to(ba, UP, buff=0.3).set_y(lm.get_y())
        lf = T("6 · şekil içi", 22, GOLD, BOLD).next_to(bf, UP, buff=0.3).set_y(lm.get_y())
        outl = VGroup(*[DashedVMobject(SurroundingRectangle(b, buff=0.15, color=LINE, corner_radius=0.08), num_dashes=40) for b in (bm, ba, bf)])
        eq = T("19 + 23 = 42 normatif tablo", 34, TXT, BOLD).move_to([-0.6, -1.75, 0])
        eq2 = T("+ 6 şekil içi parametre seti", 23, GOLD, BOLD).move_to([-0.6, -2.5, 0])
        self.at(self.cue("tek bir test matrisinde", 6.8))
        self.play(Create(outl), self.set_src("G.989.2 (2019) + Cor.1 + Amd.1 — tablo envanteri"), run_time=0.8)
        self.at(self.cue("ana metinde on dokuz", 11.6))
        self.play(LaggedStart(*[FadeIn(s, scale=0.7) for s in bm], lag_ratio=0.04), FadeIn(lm), run_time=1.0)
        self.at(self.cue("eklerde yirmi üç", 13.3))
        self.play(LaggedStart(*[FadeIn(s, scale=0.7) for s in ba], lag_ratio=0.03), FadeIn(la), run_time=1.0)
        self.at(self.cue("toplam kırk iki", 14.8))
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("şekillerin içine", 17.4))
        self.play(LaggedStart(*[FadeIn(s, scale=0.7) for s in bf], lag_ratio=0.1), FadeIn(lf), FadeIn(eq2, shift=UP * 0.1), run_time=1.0)
        self.end(pad=0.05)

        # d2 — main body groups
        self.beat("d2")
        self.clear(h)
        h = self.show_heading("Ana metin: gruplar", h)
        X0 = -4.3
        rows = [("ODN", ["6-1", "6-2", "11-3"], ODNC, 1.95, "yol kaybı · mesafe sınıfları · basit ODN"),
                ("Dalga boyu", ["9-1", "11-2"], LAMC, 1.35, "bantlar · ↓ frekans planı"),
                ("Ayar", ["9-2"], TUNC, 0.75, "ayar süresi sınıfları"),
                ("Seçicilik", ["10-1", "10-2"], SELC, 0.15, "X/S: ↓ ONU · ↑ OLT (madde 10)")]
        self.g = {}
        caps = VGroup()
        for name, labs, col, y, cap in rows:
            lab = glabel(name, y, col)
            tl = tile_row(labs, X0, y, col)
            c = T(cap, 17, TXT).next_to(tl, RIGHT, buff=0.35)
            caps.add(c)
            self.g[name] = (lab, tl, c)
        self.play(self.set_src("G.989.2 madde 6, 9, 10, 11"), run_time=0.3)
        cues = [("ODN:", 3.6), ("bantlar ve aşağı", 12.6), ("ayar süresi sınıfları", 16.0), ("onuncu maddedeki", 18.7)]
        for (name, *_), (key, d) in zip(rows, cues):
            lab, tl, c = self.g[name]
            self.at(self.cue(key, d))
            if name == "ODN":
                self.play(FadeIn(lab, shift=RIGHT * 0.1), FadeIn(tl[:2], shift=UP * 0.05), run_time=0.5)
                self.at(self.cue("basit bir ODN", 8.0))
                self.play(FadeIn(tl[2], shift=UP * 0.05), FadeIn(c), run_time=0.5)
            else:
                self.play(FadeIn(lab, shift=RIGHT * 0.1), FadeIn(tl, shift=UP * 0.05), FadeIn(c), run_time=0.5)
        self.end(pad=0.05)

        # d3 — the core: four interface tables
        self.beat("d3")
        h2 = self.heading("Çekirdek: dört arayüz tablosu")
        self.play(FadeTransform(h, h2), FadeOut(caps), run_time=0.5)
        h = h2
        yc, ys = -0.65, -1.75
        core = tile_row(["11-4", "11-5", "11-6", "11-7"], X0, yc, CORE, w=1.0, h=0.56, size=17)
        csub = VGroup(*[tf(s, 14, CORE, SEMIBOLD, w=1.05).next_to(t, DOWN, buff=0.06) for s, t in zip(["2,5G ↓", "10G ↓", "2,5G ↑", "10G ↑"], core)])
        clab = glabel("Arayüz", yc, CORE)
        side = tile_row(["11-1", "11-7bis", "11-7ter", "11-8", "11-9", "11-10", "11-11"], X0, ys, SIDE, w=0.98, h=0.46, step=1.06, size=15)
        slab = glabel("Yan", ys, SIDE)
        sb = [("hız ↔ tablo", 0, 0), ("izin verilen bölge", 1, 2), ("göz", 3, 4), ("titreşim", 5, 5), ("↑ ek yük", 6, 6)]
        ssub = VGroup(*[tf(s, 14, SIDE, SEMIBOLD, w=1.06 * (b - a + 1)).next_to(VGroup(side[a], side[b]), DOWN, buff=0.08) for s, a, b in sb])
        RX = 4.45
        rt = T("tek tablo = verici + karşı uçtaki alıcı", 19, TXT, BOLD).move_to([RX, 1.9, 0])
        fit(rt, 4.6)
        txb = sbox("Tx", None, GOLD, 0.9, 0.55, 18).move_to([RX - 1.6, 1.15, 0])
        rxb = sbox("Rx", None, SIG, 0.9, 0.55, 18).move_to([RX + 1.6, 1.15, 0])
        lnk = VGroup(Line(txb.get_right(), rxb.get_left(), color=FEED, stroke_width=3), T("ODN", 15, MUTED, BOLD).move_to([RX, 1.32, 0]))
        brc = Brace(VGroup(txb, rxb), DOWN, color=ACC, buff=0.08)
        dn = VGroup(T("↓  11-4 · 11-5", 20, CORE, BOLD), T("OLT vericisi → ONU alıcısı", 18, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([RX, 0.05, 0])
        up = VGroup(T("↑  11-6 · 11-7", 20, CORE, BOLD), T("ONU vericisi → OLT alıcısı", 18, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([RX, -0.95, 0])
        up.align_to(dn, LEFT)
        tot = pill("ana metin: 19 tablo", ACC, 18).move_to([RX, -2.75, 0])
        self.at(self.cue("dört arayüz tablosu", 1.0))
        self.play(FadeIn(clab, shift=RIGHT * 0.1), LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in core], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("İki buçuk ve on", 2.7))
        self.play(FadeIn(csub), run_time=0.5)
        self.at(self.cue("Her biri bir vericiyi", 6.4))
        self.play(FadeIn(rt), FadeIn(txb), FadeIn(rxb), Create(lnk[0]), FadeIn(lnk[1]), run_time=0.7)
        self.play(FadeIn(brc), run_time=0.4)
        self.at(self.cue("aşağı yön tabloları OLT", 11.7))
        self.play(FadeIn(dn, shift=UP * 0.1), Indicate(VGroup(core[0], core[1]), color=GOLD, scale_factor=1.06), run_time=0.7)
        self.at(self.cue("yukarı yön tabloları ONU", 16.0))
        self.play(FadeIn(up, shift=UP * 0.1), Indicate(VGroup(core[2], core[3]), color=GOLD, scale_factor=1.06), run_time=0.7)
        self.at(self.cue("izin verilen bölge", 20.4))
        self.play(FadeIn(slab, shift=RIGHT * 0.1), FadeIn(side[1:3], shift=UP * 0.05), FadeIn(ssub[1]), run_time=0.6)
        self.at(self.cue("iki göz maskesi", 26.2))
        self.play(FadeIn(side[3:5], shift=UP * 0.05), FadeIn(ssub[2]), run_time=0.5)
        self.at(self.cue("titreşim üretimi ve", 28.3))
        self.play(FadeIn(side[5:7], shift=UP * 0.05), FadeIn(ssub[3:5]), run_time=0.5)
        self.play(FadeIn(side[0], shift=UP * 0.05), FadeIn(ssub[0]), FadeIn(tot, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # d4 — annexes
        self.beat("d4")
        self.clear(h)
        h = self.show_heading("Ekler: 23 tablo — hepsi PtP WDM", h)
        ya, yb, yc2, yd = 1.85, 0.7, -0.45, -1.6
        A = tile_row([f"A.{i}" for i in range(1, 10)], -4.35, ya, CH[1], w=0.92, h=0.46, step=1.04, size=15,
                     subs=["hız", "1 ↓", "1 ↑", "2 ↓", "2 ↑", "3 ↓", "3 ↑", "göz", "titreşim"])
        B = tile_row(["B.1", "B.2"], -4.35, yb, GOLD, w=0.92, h=0.46, step=1.04, size=15)
        bcap = T("AMCC: üst modülasyon · pilot ton", 17, TXT).next_to(B, RIGHT, buff=0.3)
        C = tile_row([f"C.{i}" for i in range(1, 13)], -4.35, yc2, GOOD, w=0.8, h=0.46, step=0.88, size=14)
        cs = [("LL ODN", 0, 0), ("hız", 1, 1), ("altı arayüz tablosu", 2, 7), ("göz", 8, 8), ("titreşim", 9, 11)]
        csub = VGroup(*[tf(s, 14, GOOD, SEMIBOLD, w=0.88 * (b - a + 1)).next_to(VGroup(C[a], C[b]), DOWN, buff=0.08) for s, a, b in cs])
        D = dtile("tablo yok", MUTED, 1.8, 0.46, 15).move_to([-4.35 + 0.44, yd, 0])
        dcap = T("güç dengeleme — sayılar metnin içinde", 17, TXT).next_to(D, RIGHT, buff=0.3)
        la, lb, lc, ld = glabel("Ek A", ya, CH[1]), glabel("Ek B", yb, GOLD), glabel("Ek C", yc2, GOOD), glabel("Ek D", yd, MUTED)
        tot = T("9 + 2 + 12 + 0 = 23", 30, TXT, BOLD).move_to([0, -2.6, 0])
        self.play(self.set_src("G.989.2 Ek A, B, C, D"), run_time=0.3)
        self.at(self.cue("A ekinde hat hızı", 3.5))
        self.play(FadeIn(la, shift=RIGHT * 0.1), FadeIn(A[0], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("üç sınıfın aşağı", 5.9))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in A[1:7]], lag_ratio=0.12), run_time=0.8)
        self.at(self.cue("göz maskesi ve titreşim", 9.3))
        self.play(FadeIn(A[7:], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("B ekinde iki", 11.4))
        self.play(FadeIn(lb, shift=RIGHT * 0.1), FadeIn(B, shift=UP * 0.05), FadeIn(bcap), run_time=0.5)
        self.at(self.cue("C ekinde düşük", 13.6))
        self.play(FadeIn(lc, shift=RIGHT * 0.1), FadeIn(C[:2], shift=UP * 0.05), FadeIn(csub[:2]), run_time=0.5)
        self.at(self.cue("altı arayüz tablosu", 16.7))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in C[2:8]], lag_ratio=0.1), FadeIn(csub[2]), run_time=0.7)
        self.at(self.cue("üç titreşim", 18.4))
        self.play(FadeIn(C[8:], shift=UP * 0.05), FadeIn(csub[3:]), run_time=0.5)
        self.at(self.cue("D ekinde ise", 21.3))
        self.play(FadeIn(ld, shift=RIGHT * 0.1), Create(D[0]), FadeIn(D[1]), run_time=0.6)
        self.at(self.cue("sayılar metnin", 26.1))
        self.play(FadeIn(dcap), FadeIn(tot, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p3A")


def chk(label, num=None, size=16, w=2.95):
    parts = [T("✓", size + 1, GOOD, BOLD), T(label, size, TXT)]
    if num:
        parts.append(T(num, size, GOLD, BOLD))
    g = VGroup(*parts).arrange(RIGHT, buff=0.12)
    return fit(g, w)


class TestBlock(VGroup):
    def __init__(self, title, color, col1, col2, ref, pos, w=6.45, h=2.32):
        super().__init__()
        self.r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=LINE, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to(pos)
        self.t = T(title, 22, color, BOLD).move_to(self.r.get_corner(UL) + [0.25, -0.3, 0], aligned_edge=LEFT)
        self.rf = tf(ref, 14, MUTED, w=w - 0.5).move_to(self.r.get_corner(DL) + [0.25, 0.18, 0], aligned_edge=LEFT)
        self.items = []
        x1, x2 = self.r.get_left()[0] + 0.25, self.r.get_x() + 0.12
        y0 = self.r.get_top()[1] - 0.68
        for k, it in enumerate(col1):
            m = chk(*it).move_to([x1, y0 - k * 0.29, 0], aligned_edge=LEFT)
            self.items.append(m)
        for k, it in enumerate(col2):
            m = chk(*it).move_to([x2, y0 - k * 0.29, 0], aligned_edge=LEFT)
            self.items.append(m)
        self.color = color
        self.add(self.r, self.t, self.rf, *self.items)


class E10P3B(Act10):
    HDR, MANIFEST, PREV_BADGE = H10[3], M10("p3"), "std"

    def construct(self):
        P = [(-3.35, 1.27, 0), (3.35, 1.27, 0), (-3.35, -1.2, 0), (3.35, -1.2, 0)]
        blocks = [
            TestBlock("OLT vericisi", TW_DS, [("başlatma gücü (sınıf)",), ("spektral sapma", "±20 GHz"), ("sönüm oranı", "8,2 dB"), ("SMSR", "30 dB")],
                      [("bant dışı PSD",), ("kanal dışı PSD",), ("karanlık PSD (WNE)",), ("göz maskesi",), ("titreşim üretimi",)], "Tablo 11-4 / 11-5 · 11-8 · 11-10", P[0]),
            TestBlock("ONU alıcısı", SIG, [("hassasiyet @ BER ref",), ("aşırı yük @ BER ref",), ("yol cezası (OPP)",), ("bant içi karışma",), ("CID", "72 bit")],
                      [("titreşim toleransı",), ("titreşim aktarımı",), ("ayar adımı", "5 GHz"), ("ayar sınıfı",), ("dar bant X/S: X·Y·Z",)],
                      "Tablo 11-4 / 11-5 · 10-1 · 9-2 · Şekil 11-7…11-9", P[1]),
            TestBlock("ONU vericisi", TW_US, [("burst gücü A / B tipi",), ("(P̄, ER) bölgesi · 10G",), ("spektral sapma (CS)",), ("ayar penceresi",), ("ayar adımı", "CS/20")],
                      [("ayar süresi sınıfı",), ("λ'ya bağlı güç",), ("Tx aç/kapa", "320 / 1280 bit"), ("karanlık güç (WNE)",), ("burst boyunca göz",)],
                      "Tablo 11-6 / 11-7 · 11-7bis / ter · 11-9 · 9-2", P[2]),
            TestBlock("OLT burst alıcısı", ACC, [("hassasiyet A / B tipi",), ("aşırı yük A / B tipi",), ("4 kanal açıkken",)],
                      [("OPP (Raman dahil)",), ("bant içi karışma",), ("X/S: X = S +", "20 dB"), ("burst edinimi (önsöz)",)], "Tablo 11-6 / 11-7 · 10-2 · 11-11", P[3])]
        heads = ["Test blokları — OLT vericisi", "Test blokları — ONU alıcısı", "Test blokları — ONU vericisi", "Test blokları — OLT burst alıcısı"]
        keys = [[("sınıfa göre", 5.1, [0]), ("artı eksi yirmi", 7.3, [1]), ("sekiz virgül iki", 11.0, [2]), ("otuz desibellik", 14.4, [3]), ("bant dışı", 17.2, [4]),
                 ("kanal dışı ve karanlık", 18.0, [5, 6]), ("göz maskesi ve titreşim", 22.1, [7]), ("titreşim üretimi", 23.0, [8])],
                [("referans hata oranında", 1.0, [0, 1]), ("yol cezası", 5.0, [2]), ("bant içi karışma", 5.9, [3]), ("yetmiş iki bitlik", 7.4, [4]),
                 ("titreşim toleransı", 11.6, [5, 6]), ("beş gigahertzlik", 14.2, [7]), ("ve ayar sınıfı", 16.0, [8]), ("Z girişimcileriyle", 18.5, [9])],
                [("burst başlatma gücü", 1.1, [0]), ("izin verilen bölgesi", 3.8, [1]), ("kanal aralığına göre", 9.3, [2]), ("ayar penceresi ve", 12.3, [3]),
                 ("yirmide biri", 14.5, [4]), ("ayar süresi sınıfı", 17.8, [5]), ("dalga boyuna bağlı", 19.4, [6]), ("açma ve kapama", 22.1, [7]),
                 ("karanlık güç", 24.5, [8]), ("burst boyunca göz", 25.6, [9])],
                [("dört kanal açıkken", 1.5, [2]), ("A ve B tipi hassasiyet", 3.0, [0, 1]), ("Raman dahil", 6.1, [3]), ("bant içi karışma", 8.1, [4]),
                 ("S artı yirmi", 9.5, [5]), ("önsöz süresi içinde", 14.4, [6])]]
        ids = ["d5", "d6", "d7", "d8"]
        h = None
        for k, (b, bid) in enumerate(zip(blocks, ids)):
            self.beat(bid)
            h2 = self.heading(heads[k])
            anims = [FadeTransform(h, h2)] if h is not None else [FadeIn(h2, shift=RIGHT * 0.2)]
            if k == 0:
                anims.append(self.set_src("G.989.2 madde 9–11 · tablo notları"))
            self.play(*anims, FadeIn(b.r), FadeIn(b.t), FadeIn(b.rf), *([blocks[k - 1].r.animate.set_stroke(LINE, 2.5)] if k else []), run_time=0.6)
            self.play(b.r.animate.set_stroke(b.color, 3.5), run_time=0.3)
            h = h2
            for key, d, idx in keys[k]:
                self.at(self.cue(key, d))
                self.play(*[FadeIn(b.items[i], shift=RIGHT * 0.1) for i in idx], run_time=0.35)
            if k < 3:
                self.end(pad=0.05)
        ex = VGroup(pill("+ güç dengeleme adımları", PINK, 16), pill("+ izleme doğruluğu (Ek II)", ACC, 16), pill("+ PtP WDM (Ek A–C)", CH[1], 16)).arrange(RIGHT, buff=0.2)
        done = pill("matris tamam ✓", GOOD, 18)
        row = VGroup(ex, done).arrange(RIGHT, buff=0.35)
        fit(row, 13.2).move_to([0.2, -2.95, 0])
        self.at(self.cue("güç dengeleme adımlarını", 17.5))
        self.play(FadeIn(ex[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("izleme doğruluğunu", 20.3))
        self.play(FadeIn(ex[1], shift=UP * 0.1), FadeIn(ex[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("matris tamamdır", 24.5))
        self.play(FadeIn(done, scale=0.9), *[bl.r.animate.set_stroke(bl.color, 3) for bl in blocks], run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p3B")


class E10P3C(Act10):
    HDR, MANIFEST, PREV_BADGE = H10[3], M10("p3"), "std"

    def construct(self):
        # d9 — measurement conditions
        self.beat("d9")
        h = self.show_heading("Ölçüm koşulları da bağlayıcı — §11.1")
        conds = VGroup(card("en kötü işletme", "sıcaklık · nem · yaşlanma", None, WARN, w=3.15, h=1.2, tsize=19, bsize=16),
                       card("en kötü OPL", "Tablo 6-1", None, ODNC, w=3.15, h=1.2, tsize=19, bsize=16),
                       card("en kötü dispersiyon", "kromatik", None, LAMC, w=3.15, h=1.2, tsize=19, bsize=16),
                       card("BER referansı", "10⁻⁴ (2,5G) · 10⁻³ (10G)", None, GOOD, w=3.15, h=1.2, tsize=19, bsize=16)).arrange(RIGHT, buff=0.18).move_to([0, 1.55, 0])

        def pipe(y, label, boxes, col):
            lab = T(label, 19, col, BOLD).move_to([-6.45, y, 0], aligned_edge=LEFT)
            bx = VGroup(*[sbox(a, b, c, 2.85, 0.95, 17, 14) for a, b, c in boxes]).arrange(RIGHT, buff=0.55).move_to([1.2, y, 0])
            ar = VGroup(*[arrow(bx[i].get_right(), bx[i + 1].get_left(), MUTED, 2.5, 0.14) for i in range(len(bx) - 1)])
            return lab, bx, ar
        er = pipe(-0.55, "Sönüm oranı", [("verici", "S/R-CG", TW_DS), ("referans BPF", "G.959.1 Ek B", GOLD), ("ER ölçümü", "G.957 Şekil B.1", TXT)], TW_DS)
        sm = pipe(-2.0, "Yan mod bastırma", [("lazer çıkışı", "filtre yok", WARN), ("OSA", "spektrum", TXT), ("SMSR", "≥ 30 dB (↓)", TXT)], WARN)
        self.play(self.set_src("G.989.2 §11.1 · §9.3.2 · §9.3.8"), run_time=0.3)
        self.at(self.cue("en kötü işletme", 3.9))
        self.play(FadeIn(conds[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("nem ve yaşlanma", 8.4))
        self.play(Indicate(conds[0][2], color=WARN, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("en kötü yol kaybında", 10.2))
        self.play(FadeIn(conds[1], shift=UP * 0.1), FadeIn(conds[2], shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("referans hata oranına", 14.8))
        self.play(FadeIn(conds[3], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("Sönüm oranı bir referans", 18.6))
        self.play(FadeIn(er[0], shift=RIGHT * 0.1), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in er[1]], lag_ratio=0.25), Create(er[2]), run_time=1.0)
        self.at(self.cue("yan mod bastırma ise", 23.8))
        self.play(FadeIn(sm[0], shift=RIGHT * 0.1), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in sm[1]], lag_ratio=0.25), Create(sm[2]), run_time=1.0)
        self.at(self.cue("doğrudan lazer", 28.2))
        self.play(Indicate(sm[1][0], color=WARN, scale_factor=1.06), run_time=0.7)
        self.end(pad=0.05)

        # d10 — S/R-CG vs S/R-CP
        self.beat("d10")
        self.clear(h)
        h = self.show_heading("İki ölçüm noktası: S/R-CG ve S/R-CP", h)

        def setup_(y, four):
            srcs = VGroup(*[Line([-6.2, y + 0.33 - 0.22 * i, 0], [-4.9, y + 0.33 - 0.22 * i, 0], color=CH[i], stroke_width=4) for i in range(4 if four else 1)])
            st = T("test vericileri", 14, MUTED).next_to(srcs, UP, buff=0.08) if four else T("tek kanal", 14, MUTED).next_to(srcs, UP, buff=0.08)
            ct = sbox("OLT CT Rx", "λ1", OLTC, 1.9, 0.75, 17, 14).move_to([1.3, y, 0])
            g = VGroup(srcs, st, ct)
            cp = VGroup(DashedLine([0.05, y - 0.55, 0], [0.05, y + 0.55, 0], color=GOLD, stroke_width=2), T("S/R-CP", 15, GOLD, BOLD).move_to([0.05, y + 0.75, 0]))
            if four:
                wm = sbox("WM", None, FEED, 0.8, 1.0, 16).move_to([-1.75, y, 0])
                conv = VGroup(*[Line(s.get_end(), [-3.35, y, 0], color=CH[i], stroke_width=2.5) for i, s in enumerate(srcs)])
                cg = VGroup(DashedLine([-3.35, y - 0.55, 0], [-3.35, y + 0.55, 0], color=GOLD, stroke_width=2), T("S/R-CG", 15, GOLD, BOLD).move_to([-3.35, y + 0.75, 0]))
                l1 = Line([-3.35, y, 0], wm.get_left(), color=FEED, stroke_width=3)
                l2 = Line(wm.get_right(), ct.get_left(), color=CH[0], stroke_width=3)
                g.add(wm, conv, cg, l1, l2, cp)
            else:
                l = Line(srcs[0].get_end(), ct.get_left(), color=CH[0], stroke_width=3)
                g.add(l, cp)
            return g
        top = setup_(1.15, True)
        bot = setup_(-1.25, False)
        tt = VGroup(T("hassasiyet @ S/R-CG", 20, TXT, BOLD), T("4 kanal birden açık · fiber yok", 18, CH[1], BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.75, 1.15, 0])
        bt = VGroup(T("hassasiyet @ S/R-CP", 20, TXT, BOLD), T("başka kanal yok · fiber yok", 18, CH[1], BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.75, -1.25, 0])
        bt.align_to(tt, LEFT)
        both = pill("aynı alıcı · iki sayı — ikisi de doğru", GOOD, 19).move_to([1.6, -2.75, 0])
        self.play(self.set_src("G.989.2 Ek XI · Tablo XI.2, Not 1 (bilgilendirici)"), run_time=0.3)
        self.at(self.cue("S/R-CG noktasındaki", 2.7))
        self.play(FadeIn(top[2:], shift=RIGHT * 0.05), FadeIn(tt[0]), run_time=0.7)
        self.at(self.cue("dört kanal birden", 7.8))
        self.play(LaggedStart(*[Create(s) for s in top[0]], lag_ratio=0.15), FadeIn(top[1]), FadeIn(tt[1]), run_time=0.8)
        self.at(self.cue("S/R-CP noktasındaki", 12.4))
        self.play(FadeIn(bot, shift=RIGHT * 0.05), FadeIn(bt), run_time=0.8)
        self.at(self.cue("iki farklı sayısı", 19.1))
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # d11 — edition tracking
        self.beat("d11")
        self.clear(h)
        h = self.show_heading("Sürüm takibi", h)
        yt = 1.7
        tl = Line([-6.2, yt, 0], [6.2, yt, 0], color=MUTED, stroke_width=2.5)
        nodes = [(-5.3, "02/2019", "G.989.2 baskı 2.0", MUTED), (-1.6, "08/2019", "Cor.1", GOLD), (3.1, "10/2020", "Amd.1", ACC)]
        nd = VGroup()
        for x, d, n, c in nodes:
            nd.add(VGroup(Dot([x, yt, 0], radius=0.11, color=c), T(d, 16, MUTED).next_to([x, yt, 0], UP, buff=0.18), T(n, 18, c, BOLD).next_to([x, yt, 0], DOWN, buff=0.18)))
        one = pill("tablo değerlerinde tek düzeltme", GOLD, 17).move_to([-4.0, 0.45, 0])
        cc = RoundedRectangle(corner_radius=0.16, width=4.9, height=2.75, stroke_color=GOLD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-3.0, -1.45, 0])
        c1 = T("Tablo 10-1 · Y satırı", 20, TXT, BOLD)
        old = VGroup(T("S + 6 dB", 26, MUTED, BOLD))
        old.add(strike(old[0]))
        new = T("S + 7 dB", 30, GOOD, BOLD)
        chg = VGroup(old, Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=MUTED, stroke_width=2.5), new).arrange(RIGHT, buff=0.2)
        cgr = VGroup(c1, chg).arrange(DOWN, buff=0.35).move_to(cc).shift(UP * 0.35)
        ac = RoundedRectangle(corner_radius=0.16, width=6.9, height=2.75, stroke_color=ACC, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([3.2, -1.45, 0])
        a1 = T("yalnızca Ek D metni", 20, TXT, BOLD)
        a2 = VGroup(T("kanal dışı örneği:", 17, MUTED), T("−45,7 → −41,6 dBm/15 GHz", 19, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        a3 = VGroup(T("yeni örnek:", 17, MUTED), T("+9 − (−41) = 50 dB", 19, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        a4 = T("12 dB dengeleme → SMSR 50 → 38 dB", 20, GOLD, BOLD)
        agr = VGroup(a1, a2, a3, a4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit(agr, 6.4).move_to(ac)
        self.play(Create(tl), FadeIn(nd[0]), self.set_src("G.989.2 Cor.1 (08/2019) · Amd.1 (10/2020) · Ek D.3 / D.4"), run_time=0.7)
        self.at(self.cue("tek bir düzeltme var", 3.0))
        self.play(FadeIn(one, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("birinci düzeltmede", 8.7))
        self.play(FadeIn(nd[1], scale=0.8), FadeIn(cc), run_time=0.6)
        self.at(self.cue("Y satırı", 10.2))
        self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(old[0]), run_time=0.5)
        self.at(self.cue("S artı altıdan", 13.7))
        self.play(Create(old[1]), FadeIn(chg[1:], shift=LEFT * 0.1), run_time=0.7)
        self.at(self.cue("İki bin yirmideki", 16.6))
        self.play(FadeIn(nd[2], scale=0.8), FadeIn(ac), FadeIn(a1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("kanal dışı güç örneği", 22.5))
        self.play(FadeIn(a2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("on iki desibellik dengelemenin", 25.6))
        self.play(FadeIn(a3, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(a4, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # d12 — PSD rows optimised for 4 ch / 20 km
        self.beat("d12")
        self.clear(h)
        h = self.show_heading("PSD satırları: 4 kanal · 20 km için", h)

        def panel(cx, n, title, sub, col, dashed):
            r = RoundedRectangle(corner_radius=0.16, width=6.1, height=3.1, stroke_color=col, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([cx, 0.35, 0])
            t = VGroup(T(title, 22, TXT, BOLD), T(sub, 18, col, BOLD)).arrange(DOWN, buff=0.08).move_to([cx, 1.45, 0])
            base = Line([cx - 2.6, -0.9, 0], [cx + 2.6, -0.9, 0], color=MUTED, stroke_width=2)
            xs = np.linspace(cx - 2.2, cx + 2.2, n)
            lobes = VGroup(*[lobe(lambda v: v, x, -0.9, 1.2, 0.09, CH[i % 4], op=0.3) for i, x in enumerate(xs)])
            if dashed:
                lobes = VGroup(*[DashedVMobject(l[1], num_dashes=14) for l in lobes])
            return VGroup(r, t, base, lobes)
        p4 = panel(-3.35, 4, "4 kanal · 20 km", "PSD değerleri optimize ✓", GOOD, False)
        p8 = panel(3.35, 8, "8 kanal · 40 km", "inceleme sürüyor (FFS)", GOLD, True)
        rows = T("OOB · OOC · WNE PSD satırları (madde 11)", 17, MUTED).move_to([-3.35, -1.4, 0])
        tail = pill("8 kanalda bu satırlar: kesin sınır değil — başlangıç noktası", GOLD, 20).move_to([0, -2.6, 0])
        self.play(self.set_src("G.989.2 §6.3"), run_time=0.3)
        self.at(self.cue("on birinci maddedeki", 3.0))
        self.play(FadeIn(p4[0]), FadeIn(p4[1]), Create(p4[2]), LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in p4[3]], lag_ratio=0.15), FadeIn(rows), run_time=1.0)
        self.at(self.cue("sekiz kanal ve kırk", 12.1))
        self.play(FadeIn(p8[0]), FadeIn(p8[1]), Create(p8[2]), LaggedStart(*[Create(l) for l in p8[3]], lag_ratio=0.1), run_time=1.0)
        self.at(self.cue("Sekiz kanallı bir sistemi", 16.7))
        self.play(FadeIn(tail, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.note10("d13", [("1", "Matrisi ölçüm düzeneğine göre gruplayın", "Tek OSA ölçümü: spektral sapma + SMSR + kanal dışı güç birlikte.", "Bir:"),
                            ("2", "Yüksek yol cezasında gerçek OPP'yi ölçün", "Bant içi karışmaya maruz alıcıyla, birlikte çalışabilirlik testinde (tablo notları).", "İki:")])
        self.bridge_beat("d14", "Tablolar tamam.\nŞimdi onları tek bir cihazın ömrüne yerleştirelim.")
        self.save_timeline("ep10_p3C")


# ================================ PERDE 4 ======================================
LIFE = [("güç verilir", 6), ("↓ arama", 5), ("senkron", 5), ("profiller", 7), ("seri no", 6), ("λ düzeltme", 7), ("mesafe", 2), ("kimlik", "S2"),
        ("çalışma", 8), ("güç dengeleme", 8), ("λ devri", 7), ("λ kilitleme", 7), ("koruma", 10), ("izleme", 10), ("arızalar", 5), ("ayrılış", None)]
SY = 2.6


class Strip:
    def __init__(self):
        xs = np.linspace(-6.0, 6.0, 16)
        self.xs = xs
        self.line = Line([xs[0], SY, 0], [xs[-1], SY, 0], color=LINE, stroke_width=2)
        self.chips, self.labels = VGroup(), VGroup()
        for i, (name, _) in enumerate(LIFE):
            r = RoundedRectangle(corner_radius=0.08, width=0.54, height=0.38, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([xs[i], SY, 0])
            self.chips.add(VGroup(r, T(str(i), 15, MUTED, BOLD).move_to(r)))
            self.labels.add(T(name, 14, MUTED).move_to([xs[i], SY - 0.38 - (0.24 if i % 2 else 0), 0]))
        self.pairs = VGroup(*[VGroup(c, l) for c, l in zip(self.chips, self.labels)])
        self.group = VGroup(self.line, self.pairs)

    def style(self, i, state):
        c, l = self.chips[i], self.labels[i]
        if state == "done":
            return [c[0].animate.set_stroke(ACC, 2).set_fill(ACC, 0.22), c[1].animate.set_color(TXT), l.animate.set_color(TXT)]
        if state == "cur":
            return [c[0].animate.set_stroke(GOLD, 3).set_fill(GOLD, 0.4), c[1].animate.set_color(TXT), l.animate.set_color(GOLD)]
        return []

    def preset(self, upto):
        for i in range(upto):
            self.chips[i][0].set_stroke(ACC, 2).set_fill(ACC, 0.22)
            self.chips[i][1].set_color(TXT)
            self.labels[i].set_color(TXT)


class LifeAct(Act10):
    def open_strip(self, upto):
        self.strip = Strip()
        self.strip.preset(upto)
        self.cur, self.ttl = [], VGroup()
        self.play(FadeIn(self.strip.group), run_time=0.6)

    def step(self, ks, name, ep, num=None):
        anims = []
        for i in self.cur:
            anims += self.strip.style(i, "done")
        for k in ks:
            anims += self.strip.style(k, "cur")
        self.cur = list(ks)
        num = num if num is not None else str(ks[0])
        t = VGroup(T(f"Adım {num} · {name}", 30, TXT, BOLD), epill(ep)).arrange(RIGHT, buff=0.35)
        fit(t, 13.0).move_to([-6.45, 1.45, 0], aligned_edge=LEFT)
        anims.append(FadeTransform(self.ttl, t) if len(self.ttl) else FadeIn(t, shift=RIGHT * 0.15))
        self.play(*anims, run_time=0.6)
        self.ttl = t

    def stage_clear(self):
        self.clear(self.strip.group, self.strip.line, self.strip.pairs, self.ttl)


def lab_onu(on=False, w=2.0, h=1.05):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=ONUC, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    t = T("ONU", 20, TXT, BOLD).move_to(r).shift(UP * 0.22)
    tx = VGroup(T("Tx", 15, MUTED, BOLD), lamp(on, 0.1)).arrange(RIGHT, buff=0.12).move_to(r).shift(DOWN * 0.22 + LEFT * 0.45)
    rx = VGroup(T("Rx", 15, MUTED, BOLD), gauge(0.15, TW_DS, 0.4)).arrange(RIGHT, buff=0.12).move_to(r).shift(DOWN * 0.22 + RIGHT * 0.45)
    return VGroup(r, t, tx, rx)


def onu_lamp(u, on):
    return Transform(u[2][1], lamp(on, 0.1).move_to(u[2][1].get_center()))


class E10P4A(LifeAct):
    HDR, MANIFEST, FIRST = H10[4], M10("p4"), True

    def construct(self):
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Bir ONU'nun hayatı")
        self.at(self.cue("Sezon boyunca", 2.5))
        self.to_header(tc)
        self.set_badge("ozet")
        self.strip = Strip()
        self.cur, self.ttl = [], VGroup()
        self.at(self.cue("zaman çizelgesine", 6.5))
        self.play(Create(self.strip.line), FadeIn(self.strip.pairs, shift=UP * 0.1, lag_ratio=0.06), run_time=1.6)
        q1 = card("Optik ne yapıyor?", "G.989.2 · fiziksel katman", None, ACC, w=5.6, h=1.5, tsize=26, bsize=20).move_to([-3.2, -0.3, 0])
        q2 = card("TC katmanı ne söylüyor?", "G.989.3 · iletim yakınsama", None, STATE, w=5.6, h=1.5, tsize=26, bsize=20).move_to([3.2, -0.3, 0])
        ep = T("her adımda: sezonun hangi bölümüne bağlandığı", 18, PINK, BOLD).move_to([0, -1.85, 0])
        self.at(self.cue("optik ne yapıyor", 12.8))
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.5)
        self.at(self.cue("TC katmanı ne", 14.2))
        self.play(FadeIn(q2, shift=UP * 0.15), FadeIn(ep), run_time=0.6)
        self.end(pad=0.05)

        # e2 — step 0: power-up
        self.beat("e2")
        self.stage_clear()
        self.step([0], "Güç verilir", 6)
        onu = lab_onu(False).move_to([-4.9, 0.2, 0])
        o1 = sbox("O1 · Başlangıç", "verici kapalı", STATE, 2.6, 0.85, 18, 14).move_to([-4.9, -1.1, 0])
        ar1 = arrow(onu.get_bottom(), o1.get_top(), STATE, 2.5, 0.12)
        px0, px1, py0, py1 = 0.2, 6.4, -2.55, 0.55
        pax = VGroup(Line([px0, py0, 0], [px1, py0, 0], color=MUTED, stroke_width=2), Line([px0, py0, 0], [px0, py1, 0], color=MUTED, stroke_width=2),
                     T("frekans", 14, MUTED).next_to([px1, py0, 0], DOWN, buff=0.08).shift(LEFT * 0.4), T("PSD", 14, MUTED).next_to([px0, py1, 0], RIGHT, buff=0.1))
        lim = DashedLine([px0, -1.45, 0], [px1, -1.45, 0], color=WARN, stroke_width=3)
        limt = VGroup(T("≤ −62,6 dBm / 15 GHz", 20, WARN, BOLD), T("etkin olmayan verici (WNE-PSD) · Tablo 11-6 / 11-7", 15, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        limt.move_to([px0 + 0.2, -0.75, 0], aligned_edge=LEFT)
        rng = np.random.default_rng(5)
        xs = np.linspace(px0 + 0.1, px1 - 0.1, 90)
        noise = VMobject(stroke_color=TW_US, stroke_width=2).set_points_as_corners([[x, -2.15 + 0.18 * rng.standard_normal() * 0.6, 0] for x in xs])
        ntag = tag("iz temsili", MUTED, 14).move_to([px1 - 0.75, -2.15 + 0.45, 0])
        dark = T("kapalı ama tamamen karanlık değil", 17, TW_US, BOLD).move_to([3.3, 0.2, 0])
        o7 = sbox("O7 · Acil durdurma", None, WARN, 2.6, 0.62, 17).move_to([-4.9, -2.45, 0])
        o7a = arrow(o1.get_bottom() + LEFT * 0.0, o7.get_top(), WARN, 2.5, 0.12)
        o7t = T("son durum O7 ise →\ndoğrudan O7 (Tablo 12-4)", 15, WARN, BOLD, line_spacing=0.85).next_to(o7, RIGHT, buff=0.2)
        self.at(self.cue("ilk durumuna girer", 1.9))
        self.play(FadeIn(onu, shift=UP * 0.1), GrowArrow(ar1), FadeIn(o1), self.set_src("G.989.3 Tablo 12-4 · G.989.2 Tablo 11-6 / 11-7"), run_time=0.7)
        self.at(self.cue("vericisi kapalıdır", 3.9))
        self.play(Indicate(onu[2], color=MUTED, scale_factor=1.3), run_time=0.6)
        self.at(self.cue("kapalı bir verici bile", 5.7))
        self.play(Create(pax[:2]), FadeIn(pax[2:]), FadeIn(dark), run_time=0.6)
        self.play(Create(noise), FadeIn(ntag), run_time=1.0)
        self.at(self.cue("on beş gigahertz başına", 14.1))
        self.play(Create(lim), FadeIn(limt, shift=UP * 0.1), run_time=0.7)
        self.at(self.cue("önceki durumu acil", 20.1))
        self.play(GrowArrow(o7a), FadeIn(o7), FadeIn(o7t), run_time=0.7)
        self.end(pad=0.05)

        # e3 — step 1: downstream search
        self.beat("e3")
        self.stage_clear()
        self.step([1], "↓ kanalını aramak", 5)
        ya = -1.75
        axg, X = lin_axis(187.05, 187.85, -5.8, 2.2, ya, [187.1 + 0.1 * i for i in range(8)], size=14, fmt=lambda v: tr(round(v, 1)), unit="THz")
        lobes = VGroup(*[lobe(X, 187.1 + 0.1 * i, ya, 1.1, 0.012, TW_DS, op=0.3) for i in range(8)])
        flt = Rectangle(width=X(187.14) - X(187.06), height=1.55, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.12).move_to([X(187.8), ya + 0.78, 0])
        fl = T("ayarlanabilir alıcı filtresi", 15, GOLD, BOLD).next_to(flt, UP, buff=0.08)
        onu = lab_onu(False, 1.9, 1.0).move_to([-5.3, 0.5, 0])
        pas = VGroup(T("pasif dinler", 18, TXT, BOLD), T("Tx kapalı", 16, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(onu, RIGHT, buff=0.3)
        rngt = T("187,8 … 187,1 THz · 8 kanal (Tablo 11-2)", 17, TW_DS, BOLD).move_to([X(187.45), -2.8, 0])
        step_ = card("ayar adımı", "≤ 5 GHz (Tablo 11-4 / 11-5)", None, GOLD, w=4.0, h=1.15, tsize=20, bsize=17).move_to([4.95, 0.25, 0])
        cls = card("Rx ayar süresi sınıfı", "zorunlu değil (Tablo 9-2)", None, MUTED, w=4.0, h=1.15, tsize=20, bsize=17).move_to([4.95, -1.25, 0])
        self.at(self.cue("pasif kalarak", 2.9))
        self.play(FadeIn(onu, shift=UP * 0.1), FadeIn(pas), self.set_src("G.989.2 §9.3.7 · Tablo 11-2 · Tablo 9-2"), run_time=0.6)
        self.at(self.cue("ayarlanabilir olmalıdır", 5.0))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(flt), FadeIn(fl), run_time=0.7)
        self.at(self.cue("aşağı yön kanalları", 7.7))
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in lobes], lag_ratio=0.08), FadeIn(rngt), run_time=1.0)
        self.play(VGroup(flt, fl).animate.shift(LEFT * (X(187.8) - X(187.4))), run_time=2.0, rate_func=smooth)
        self.play(Indicate(lobes[3], color=GOLD, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("Ayar adımı en çok", 15.8))
        self.play(FadeIn(step_, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("ayar süresi sınıfı ise", 18.8))
        self.play(FadeIn(cls, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # e4 — step 2: sync
        self.beat("e4")
        self.stage_clear()
        self.step([2], "Senkron", 5)
        cdr = sbox("CDR", "saat ↓ sinyalden", ACC, 2.2, 0.85, 19, 14).move_to([-5.3, 0.35, 0])
        cells = VGroup(*[Rectangle(width=0.105, height=0.42, stroke_width=0.8, stroke_color=BG, fill_color=STATE, fill_opacity=0.6) for _ in range(64)]).arrange(RIGHT, buff=0.025)
        cells.move_to([1.15, 0.35, 0])
        cl = T("PSync · 64 bit", 17, STATE, BOLD).next_to(cells, UP, buff=0.1)
        st1 = T("av: 64 / 64 birebir", 18, GOOD, BOLD).next_to(cells, DOWN, buff=0.15).align_to(cells, LEFT)
        st2 = T("senkronda: ≥ 62 / 64", 18, GOLD, BOLD).next_to(cells, DOWN, buff=0.15).align_to(cells, RIGHT)
        fw, fx0, fy = 1.25, -5.6, -1.45
        fr = frames_row(9, fx0, fy, fw, 0.5, TW_DS, op=0.12)
        heads = VGroup(*[Rectangle(width=0.14, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(f.get_left() + RIGHT * 0.07) for f in fr])
        ft = T("125 µs", 15, MUTED).next_to(fr[0], DOWN, buff=0.08)
        bad = VGroup(*[xmark(fr[k], WARN, 3.5, -0.08) for k in (5, 6, 7)])
        bb = Brace(VGroup(fr[5], fr[7]), DOWN, color=WARN)
        bbt = T("M = 3 ardışık kötü çerçeve (önerilen)", 17, WARN, BOLD).next_to(bb, DOWN, buff=0.06)
        lods = T("→ LODS · senkron kaybı", 20, WARN, BOLD).move_to([-2.6, -2.35, 0])
        self.at(self.cue("saatini aşağı yön", 1.4))
        self.play(FadeIn(cdr, shift=RIGHT * 0.1), self.set_src("G.989.3 §10.1.1.3 · G.989.2 §9.3.6.5"), run_time=0.5)
        self.at(self.cue("çerçeve başındaki", 5.0))
        self.play(FadeIn(fr), FadeIn(heads), FadeIn(ft), run_time=0.6)
        self.at(self.cue("altmış dört bitlik", 8.7))
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), FadeIn(cl), Indicate(heads[0], color=GOLD, scale_factor=1.5), run_time=0.9)
        self.at(self.cue("birebir eşleşmelidir", 11.1))
        self.play(cells.animate.set_fill(GOOD, 0.85), FadeIn(st1), run_time=0.6)
        self.at(self.cue("en az altmış ikisi", 14.2))
        self.play(cells[17].animate.set_fill(WARN, 1), cells[44].animate.set_fill(WARN, 1), FadeIn(st2), run_time=0.6)
        self.at(self.cue("yüz yirmi beş mikrosaniyelik", 20.0))
        self.play(Indicate(ft, color=TXT), LaggedStart(*[Indicate(h_, color=GOLD, scale_factor=1.3) for h_ in heads[:5]], lag_ratio=0.2), run_time=1.0)
        self.at(self.cue("üç ardışık kötü", 24.3))
        self.play(LaggedStart(*[Create(b) for b in bad], lag_ratio=0.25), FadeIn(bb), FadeIn(bbt), run_time=0.8)
        self.at(self.cue("senkron kaybı demektir", 27.7))
        self.play(FadeIn(lods, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # e5 — step 3: profiles
        self.beat("e5")
        self.stage_clear()
        self.step([3], "Profilleri öğrenmek", 7)
        pr = RoundedRectangle(corner_radius=0.16, width=5.6, height=2.75, stroke_color=PROF_C, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-3.6, -0.75, 0])
        prt = T("Channel_Profile (PLOAM)", 21, PROF_C, BOLD).move_to(pr.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        flds = VGroup(*[VGroup(T("•", 18, PROF_C, BOLD), T(s, 18, TXT)).arrange(RIGHT, buff=0.15) for s in
                        ["frekans (↓ ofset, 0,1 GHz adım)", "FEC kullanımı", "bağlantı tipi (A / B)", "varsayılan zayıflatma"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        flds.next_to(prt, DOWN, buff=0.25, aligned_edge=LEFT)
        t0, ty = 0.9, 0.0
        tax = Arrow([t0, ty, 0], [6.6, ty, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.15)
        k = 0.48
        ticks = VGroup(*[Line([t0 + k * s, ty, 0], [t0 + k * s, ty + 0.45, 0], color=PROF_C, stroke_width=4) for s in (0.5, 3.0, 5.5, 8.0, 10.5)])
        tkt = T("profiller her 1–5 s yinelenir", 16, PROF_C, BOLD).next_to(ticks, UP, buff=0.1).align_to(tax, LEFT)
        dw = BraceBetweenPoints([t0, ty - 0.1, 0], [t0 + 10 * k, ty - 0.1, 0], DOWN, color=GOLD)
        dwt = T("profil bekleme ≥ 10 s", 16, GOLD, BOLD).next_to(dw, DOWN, buff=0.06)
        tol = card("PSBd · TOL", "OLT başlatma gücü — aynı anda okunur", None, GOLD, w=5.4, h=1.1, tsize=19, bsize=16).move_to([3.7, -2.2, 0])
        self.at(self.cue("kanal profillerini dinler", 2.4))
        self.play(FadeIn(pr), FadeIn(prt), self.set_src("G.989.3 §17.1 · Tablo 12-1 (O1.2) · §10.1.1.1.3"), run_time=0.6)
        for i, (key, d) in enumerate((("her kanalın frekansı", 4.9), ("FEC kullanımı", 6.7), ("bağlantı tipi ve", 7.8), ("varsayılan zayıflatma", 9.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(flds[i], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("bir ile beş saniye", 11.1))
        self.play(GrowArrow(tax), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.15), FadeIn(tkt), run_time=0.9)
        self.at(self.cue("profil bekleme süresi", 16.2))
        self.play(FadeIn(dw), FadeIn(dwt), run_time=0.5)
        self.at(self.cue("TOL alanından", 19.7))
        self.play(FadeIn(tol, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # e6 — step 4: serial number (first light)
        self.beat("e6")
        self.stage_clear()
        self.step([4], "Seri numarası", 6)
        onu = lab_onu(False, 1.9, 1.0).move_to([-5.35, 0.35, 0])
        dv = T("devrede:", 17, MUTED, BOLD).move_to([-3.75, 0.7, 0], aligned_edge=LEFT)
        chips = VGroup(*[pill(s, TW_US, 16) for s in ["burst başlatma gücü", "spektral sapma", "ayar penceresi", "ayar adımı = CS / 20"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        chips.next_to(dv, DOWN, buff=0.15, aligned_edge=LEFT)
        bx0, bx1, yl, yh = 0.9, 6.5, -1.0, 0.4
        dark = Line([bx0, yl, 0], [2.4, yl, 0], color=MUTED, stroke_width=3)
        ramp = Line([2.4, yl, 0], [3.5, yh, 0], color=TW_US, stroke_width=3)
        data = VMobject(stroke_color=TW_US, stroke_width=2.5).set_points_as_corners(nrz([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1], 3.5, (bx1 - 3.5) / 12, yh - 0.55, yh, rise=0.02))
        burst = VGroup(dark, ramp, data)
        br = BraceBetweenPoints([2.4, yl - 0.12, 0], [3.5, yl - 0.12, 0], DOWN, color=GOLD)
        brt = T("Tx açma süresi", 16, GOLD, BOLD).next_to(br, DOWN, buff=0.06)
        n1 = T("2,5G: 320 bit", 21, TXT, BOLD)
        n2 = T("10G: 1280 bit", 21, TXT, BOLD)
        n3 = T("ikisi de 128,6 ns", 22, GOLD, BOLD)
        ns = VGroup(n1, n2, n3).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.9, -2.45, 0], aligned_edge=LEFT)
        self.at(self.cue("ilk kez ışık verir", 2.0))
        self.play(FadeIn(onu), self.set_src("G.989.2 Tablo 11-6 / 11-7 · G.989.3 §12.1.3"), run_time=0.4)
        self.play(onu_lamp(onu, True), run_time=0.4)
        self.at(self.cue("altıncı ve yedinci", 4.0))
        self.play(FadeIn(dv), run_time=0.3)
        for i, (key, d) in enumerate((("burst başlatma gücü", 9.4), ("spektral sapma", 11.1), ("ayar penceresi", 12.3), ("yirmide biri", 13.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(chips[i], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("verici açma süresi", 17.6))
        self.play(Create(dark), Create(ramp), Create(data), run_time=0.9)
        self.play(FadeIn(br), FadeIn(brt), run_time=0.4)
        self.at(self.cue("üç yüz yirmi", 19.4))
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("bin iki yüz seksen", 22.2))
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("yüz yirmi sekiz virgül", 25.3))
        self.play(FadeIn(n3, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # e6a — step 4 (cont.): timing of the SN response
        self.beat("e6a")
        self.stage_clear()
        K = 1 / 60.0          # units per µs
        x0, yax = -5.6, -0.25
        ax = Arrow([x0 - 0.2, yax, 0], [2.4, yax, 0], buff=0, color=MUTED, stroke_width=2.5, tip_length=0.15)
        axl = T("zaman", 14, MUTED).next_to(ax, UP, buff=0.06).align_to(ax, RIGHT)
        t0 = VGroup(Line([x0, yax - 0.15, 0], [x0, yax + 0.6, 0], color=TXT, stroke_width=3), T("SN isteği", 15, TXT, BOLD).next_to([x0, yax + 0.6, 0], UP, buff=0.05))
        rsp = Rectangle(width=35 * K, height=0.36, stroke_width=0, fill_color=ACC, fill_opacity=0.8).move_to([x0 + 17.5 * K, yax + 0.2, 0])
        rnd = Rectangle(width=48 * K, height=0.36, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.25).move_to([x0 + 35 * K + 24 * K, yax + 0.2, 0])
        sn = Rectangle(width=0.22, height=0.36, stroke_width=0, fill_color=TW_US, fill_opacity=0.95).next_to(rnd, RIGHT, buff=0)
        lr = VGroup(T("rastgele gecikme 0 … 48 µs", 17, GOLD, BOLD))
        lr.next_to(rnd, DOWN, buff=0.35).align_to(rsp, LEFT)
        lp = T("yanıt süresi 35 ± 1 µs", 17, ACC, BOLD).next_to(lr, DOWN, buff=0.1).align_to(rsp, LEFT)
        q20 = VGroup(Rectangle(width=250 * K, height=0.42, stroke_width=0, fill_color=MUTED, fill_opacity=0.5), T("sessiz pencere · 20 km: 250 µs", 16, TXT, BOLD))
        q20[0].move_to([x0 + 125 * K, -1.95, 0])
        q20[1].move_to(q20[0])
        q40 = VGroup(Rectangle(width=450 * K, height=0.42, stroke_width=0, fill_color=MUTED, fill_opacity=0.35), T("40 km: 450 µs", 16, TXT, BOLD))
        q40[0].move_to([x0 + 225 * K, -2.5, 0])
        q40[1].move_to(q40[0])
        olt = T("OLT:", 17, MUTED, BOLD).next_to(q20, LEFT, buff=0.12)
        sc = RoundedRectangle(corner_radius=0.14, width=3.9, height=3.3, stroke_color=TW_US, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([4.75, -0.75, 0])
        sct = T("Serial_Number_ONU taşır:", 18, TW_US, BOLD).move_to(sc.get_corner(UL) + [0.25, -0.35, 0], aligned_edge=LEFT)
        sf = VGroup(*[VGroup(T("•", 17, TW_US, BOLD), T(s, 17, TXT)).arrange(RIGHT, buff=0.12) for s in ["↓ kanal", "kalibrasyon durumu", "ayar adımı", "tek adım ayar süresi"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        sf.next_to(sct, DOWN, buff=0.28, aligned_edge=LEFT)
        self.at(self.cue("sıfır ile kırk sekiz", 0.3))
        self.play(GrowArrow(ax), FadeIn(axl), FadeIn(t0), self.set_src("G.989.3 §13.1.2 · §12.1.3"), run_time=0.6)
        self.play(FadeIn(rnd), FadeIn(sn), FadeIn(lr), run_time=0.6)
        self.at(self.cue("otuz beş artı eksi", 5.9))
        self.play(GrowFromEdge(rsp, LEFT), FadeIn(lp), run_time=0.6)
        self.at(self.cue("sessiz pencere açar", 12.0))
        self.play(FadeIn(olt), run_time=0.3)
        self.at(self.cue("iki yüz elli", 15.2))
        self.play(GrowFromEdge(q20[0], LEFT), FadeIn(q20[1]), run_time=0.6)
        self.at(self.cue("dört yüz elli", 17.8))
        self.play(GrowFromEdge(q40[0], LEFT), FadeIn(q40[1]), run_time=0.6)
        self.at(self.cue("Seri numarası mesajı", 21.4))
        self.play(FadeIn(sc), FadeIn(sct), FadeIn(sf[0], shift=RIGHT * 0.1), run_time=0.6)
        self.at(self.cue("kalibrasyon durumunu", 25.4))
        self.play(FadeIn(sf[1], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("tek adımlık ayar", 27.6))
        self.play(FadeIn(sf[2:], shift=RIGHT * 0.1), run_time=0.45)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p4A")


class E10P4B(LifeAct):
    HDR, MANIFEST, PREV_BADGE = H10[4], M10("p4"), "ozet"

    def construct(self):
        # e7 — step 5: upstream wavelength correction
        self.beat("e7")
        self.open_strip(5)
        self.step([5], "↑ dalga boyunu düzeltmek", 7)
        ya = -1.9
        axg, X = lin_axis(-60, 60, -6.0, 1.6, ya, [-60, -40, -20, 0, 20, 40, 60], size=14, fmt=lambda v: "C" if v == 0 else ("+" if v > 0 else "−") + str(abs(int(v))), unit="↑ kanal merkezine göre (GHz)")
        mse = Rectangle(width=X(20) - X(-20), height=2.2, stroke_width=0, fill_color=GOOD, fill_opacity=0.14).move_to([X(0), ya + 1.1, 0])
        mset = T("±20 GHz (MSE)", 17, GOOD, BOLD).next_to(mse, UP, buff=0.08)
        ol = lobe(X, 44, ya, 1.5, 4.5, WARN, op=0.3)
        olt = T("kalibre edilmemiş", 16, WARN, BOLD).move_to([X(44), ya + 1.8, 0])
        nl = lobe(X, 3, ya, 1.5, 4.5, TW_US, op=0.35)
        cmd = VGroup(arrow([X(38), ya + 0.75, 0], [X(14), ya + 0.75, 0], GOLD, 3, 0.15), T("ayar komutları", 15, GOLD, BOLD))
        cmd[1].next_to(cmd[0], UP, buff=0.06)
        pc = RoundedRectangle(corner_radius=0.16, width=4.5, height=2.3, stroke_color=TW_US, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([4.5, -0.85, 0])
        pct = T("λ'ya bağlı güç değişimi", 19, TW_US, BOLD).move_to(pc.get_corner(UL) + [0.25, -0.35, 0], aligned_edge=LEFT)
        p1 = VGroup(T("2,5G:", 19, MUTED, BOLD), T("±0,05 dB/GHz", 22, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        p2 = VGroup(T("10G:", 19, MUTED, BOLD), T("±0,02 dB/GHz", 22, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        ps = VGroup(p1, p2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(pct, DOWN, buff=0.3, aligned_edge=LEFT)
        self.at(self.cue("Kalibre edilmemiş", 3.6))
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(ol), FadeIn(olt), self.set_src("G.989.2 Tablo 11-6 / 11-7 · G.989.3 §12.1.3"), run_time=0.7)
        self.at(self.cue("doğru kanala çekilir", 5.8))
        self.play(GrowArrow(cmd[0]), FadeIn(cmd[1]), run_time=0.5)
        self.play(Transform(ol, nl), FadeOut(olt), run_time=1.0)
        self.at(self.cue("Optik tarafta sınır", 9.0))
        self.play(FadeIn(mse), run_time=0.5)
        self.at(self.cue("yirmi gigahertzlik", 10.7))
        self.play(FadeIn(mset, shift=DOWN * 0.1), run_time=0.4)
        self.at(self.cue("Dalga boyuna bağlı", 14.7))
        self.play(FadeIn(pc), FadeIn(pct), FadeIn(p1, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("sıfır virgül sıfır iki", 22.7))
        self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # e8 — step 6: ranging
        self.beat("e8")
        self.stage_clear()
        self.step([6], "Mesafe ölçümü", 2)
        bx = -4.2
        rows = [("yakın ONU", 0.45, 1.4, 5.4), ("uzak ONU", -0.45, 4.9, 1.9)]
        rtd, eqd, labs = VGroup(), VGroup(), VGroup()
        for name, y, a, b in rows:
            labs.add(T(name, 18, TXT, BOLD).move_to([-6.45, y, 0], aligned_edge=LEFT))
            r1 = VGroup(Rectangle(width=a, height=0.42, stroke_width=0, fill_color=TW_US, fill_opacity=0.75), T("gidiş-dönüş", 15, BG, BOLD))
            r1[0].move_to([bx + a / 2, y, 0])
            r1[1].move_to(r1[0])
            fit(r1[1], a - 0.1)
            r2 = VGroup(Rectangle(width=b, height=0.42, stroke_width=0, fill_color=GOLD, fill_opacity=0.75), T("EqD", 15, BG, BOLD))
            r2[0].move_to([bx + a + b / 2, y, 0])
            r2[1].move_to(r2[0])
            rtd.add(r1)
            eqd.add(r2)
        al = VGroup(DashedLine([bx + 6.8, 0.9, 0], [bx + 6.8, -0.9, 0], color=GOOD, stroke_width=3), T("ortak zaman ekseni", 17, GOOD, BOLD).move_to([bx + 6.8 + 1.55, 0, 0]))
        K = 1 / 50.0
        w20 = VGroup(Rectangle(width=202 * K, height=0.42, stroke_width=0, fill_color=MUTED, fill_opacity=0.5), T("mesafe ölçüm penceresi · 20 km: 202 µs", 15, TXT, BOLD))
        w20[0].move_to([bx + 101 * K, -1.55, 0])
        w20[1].next_to(w20[0], RIGHT, buff=0.15)
        w40 = VGroup(Rectangle(width=402 * K, height=0.42, stroke_width=0, fill_color=MUTED, fill_opacity=0.35), T("40 km: 402 µs", 15, TXT, BOLD))
        w40[0].move_to([bx + 201 * K, -2.1, 0])
        w40[1].next_to(w40[0], RIGHT, buff=0.15)
        eq = pill("EqD: 1 bit doğruluk @ 2,48832 Gbit/s", GOLD, 18).move_to([2.6, -2.85, 0])
        self.at(self.cue("gidiş dönüş gecikmesini", 2.4))
        self.play(FadeIn(labs), *[GrowFromEdge(r[0], LEFT) for r in rtd], *[FadeIn(r[1]) for r in rtd], self.set_src("G.989.3 §13.1.3–13.1.4 · G.989.2 Tablo 6-2"), run_time=0.8)
        self.at(self.cue("eşitleme gecikmesi verir", 5.5))
        self.play(*[GrowFromEdge(r[0], LEFT) for r in eqd], *[FadeIn(r[1]) for r in eqd], run_time=0.8)
        self.at(self.cue("ortak bir zaman", 8.6))
        self.play(Create(al[0]), FadeIn(al[1]), run_time=0.6)
        self.at(self.cue("iki yüz iki", 13.4))
        self.play(GrowFromEdge(w20[0], LEFT), FadeIn(w20[1]), run_time=0.6)
        self.at(self.cue("dört yüz iki", 17.8))
        self.play(GrowFromEdge(w40[0], LEFT), FadeIn(w40[1]), run_time=0.6)
        self.at(self.cue("bir bit doğruluğundadır", 21.6))
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # e9 — step 7: identity
        self.beat("e9")
        self.stage_clear()
        self.step([7], "Kimlik", "S2")
        c1 = card("Registration_ID", "zorunlu · her NG-PON2 cihazında (§15.2)", None, GOOD, w=6.1, h=1.3, tsize=22, bsize=18).move_to([-3.25, 0.25, 0])
        c2 = card("karşılıklı kimlik doğrulama", "isteğe bağlı · OMCI (Ek C) · IEEE 802.1X (Ek D)", None, MUTED, w=6.1, h=1.3, tsize=22, bsize=18).move_to([3.25, 0.25, 0])
        fl = VGroup(sbox("aktivasyon tamam", "O5", STATE, 3.0, 0.85, 18, 14), sbox("kimlik doğrulama", "isteğe bağlı", MUTED, 3.0, 0.85, 18, 14),
                    sbox("kullanıcı verisi", None, ACC, 3.0, 0.85, 18)).arrange(RIGHT, buff=0.7).move_to([0, -1.75, 0])
        fa = VGroup(*[arrow(fl[i].get_right(), fl[i + 1].get_left(), MUTED, 2.5, 0.14) for i in range(2)])
        self.at(self.cue("Kayıt kimliği", 1.4))
        self.play(FadeIn(c1, shift=UP * 0.1), self.set_src("G.989.3 §15.2"), run_time=0.5)
        self.at(self.cue("İsteğe bağlı olarak", 5.4))
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("aktivasyon tamamlandıktan", 11.0))
        self.play(LaggedStart(FadeIn(fl[0]), GrowArrow(fa[0]), FadeIn(fl[1]), GrowArrow(fa[1]), FadeIn(fl[2]), lag_ratio=0.3), run_time=1.2)
        self.end(pad=0.05)

        # e10 — step 8: operation
        self.beat("e10")
        self.stage_clear()
        self.step([8], "Çalışma", 8)
        clk = VGroup(pill("↓ saat", TW_DS, 18), arrow(ORIGIN, RIGHT * 0.8, MUTED, 2.5, 0.14), pill("↑ saat", TW_US, 18)).arrange(RIGHT, buff=0.15)
        clk.move_to([-3.6, 0.55, 0])
        clt = T("aynı frekans doğruluğu (§11.1.1.2)", 16, MUTED).next_to(clk, DOWN, buff=0.12)
        gs = VGroup(*[VGroup(gauge(0.34, c, f), T(s, 16, c, BOLD)) for s, c, f in (("RSSI", ACC, 0.6), ("faz", GOLD, 0.45), ("BER", GOOD, 0.3))])
        for g_ in gs:
            g_[1].next_to(g_[0], DOWN, buff=0.1)
        gs.arrange(RIGHT, buff=0.55).move_to([3.4, 0.45, 0])
        gt = T("OLT her ONU'yu izler", 16, MUTED).next_to(gs, DOWN, buff=0.12)
        yp = -1.55
        pax = Line([-5.5, yp, 0], [5.5, yp, 0], color=MUTED, stroke_width=2.5)
        pl = T("faz", 15, MUTED).next_to(pax, RIGHT, buff=0.1)
        win = Rectangle(width=4.0, height=0.62, stroke_color=GOOD, stroke_width=2, fill_color=GOOD, fill_opacity=0.13).move_to([0, yp, 0])
        wl = T("DOW penceresi", 15, GOOD, BOLD).next_to(win, UP, buff=0.06)
        dot = Dot([0, yp, 0], radius=0.11, color=TW_US)
        rt = T("Ranging_Time → yeni EqD", 16, GOLD, BOLD).move_to([3.6, yp + 0.55, 0])
        vals = VGroup(T("2,5G: ±8 bit", 19, TXT, BOLD), T("10G: ±32 bit", 19, TXT, BOLD), T("≈ ±3,2 ns", 21, GOLD, BOLD)).arrange(RIGHT, buff=0.55).move_to([0, -2.55, 0])
        self.at(self.cue("ONU artık yukarı yönde", 1.6))
        self.play(FadeIn(clk, shift=RIGHT * 0.1), FadeIn(clt), self.set_src("G.989.3 §12.1.3 · §13.1.5–13.1.6"), run_time=0.6)
        self.at(self.cue("gelen gücünü", 8.8))
        self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.1) for g_ in gs], lag_ratio=0.2), FadeIn(gt), run_time=0.8)
        self.at(self.cue("Faz kayması bir pencereyi", 13.7))
        self.play(Create(pax), FadeIn(pl), FadeIn(win), FadeIn(wl), FadeIn(dot), run_time=0.6)
        self.play(dot.animate.move_to([2.7, yp, 0]).set_color(WARN), run_time=1.2)
        self.play(FadeIn(rt), run_time=0.3)
        self.play(dot.animate.move_to([0, yp, 0]).set_color(TW_US), run_time=0.8)
        self.at(self.cue("iki buçuk gigabitte sekiz", 20.0))
        self.play(FadeIn(vals[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("otuz iki bit", 22.2))
        self.play(FadeIn(vals[1], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("üç virgül iki", 24.4))
        self.play(FadeIn(vals[2], shift=UP * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # e11 — step 9: power levelling
        self.beat("e11")
        self.stage_clear()
        self.step([9], "Güç dengeleme", 8)
        X = lambda v: -4.9 + (v + 20) / 16 * 6.0
        Y = lambda a: -2.5 + a / 12 * 2.9
        xa = VGroup(Line([X(-20), Y(0), 0], [X(-4), Y(0), 0], color=MUTED, stroke_width=2), T("alınan güç (dBm)", 14, MUTED).next_to([X(-12), Y(0), 0], DOWN, buff=0.38))
        yax = VGroup(Line([X(-20), Y(0), 0], [X(-20), Y(12.8), 0], color=MUTED, stroke_width=2), T("zayıflatma (dB)", 14, MUTED).next_to([X(-20), Y(12.8), 0], UP, buff=0.06))
        lev = [(-20, -16, 0), (-16, -13, 3), (-13, -10, 6), (-10, -7, 9), (-7, -4, 12)]
        segs = VGroup(*[Line([X(a), Y(v), 0], [X(b), Y(v), 0], color=PINK, stroke_width=5) for a, b, v in lev])
        risers = VGroup(*[Line([X(b), Y(v), 0], [X(b), Y(v + 3), 0], color=PINK, stroke_width=2, stroke_opacity=0.6) for a, b, v in lev[:-1]])
        vl = VGroup(*[T(f"{v} dB", 16, PINK, BOLD).next_to([(X(a) + X(b)) / 2, Y(v), 0], UP, buff=0.08) for a, b, v in lev])
        thr = VGroup(*[VGroup(DashedLine([X(t), Y(0), 0], [X(t), Y(12.8), 0], color=MUTED, stroke_width=1.5), T(tr(t), 15, TXT, BOLD).next_to([X(t), Y(0), 0], DOWN, buff=0.1))
                       for t in (-7, -10, -13, -16)])
        c1 = card("OLT yönlendirmeli (D.5)", "+ 6 … 9 dB ek aralık", None, GOLD, w=4.6, h=1.15, tsize=19, bsize=18).move_to([4.45, 0.3, 0])
        c2 = card("TC katmanı (§12.1.6)", "adımlar 3 dB'in katları\nen az 3 ve 6 dB desteklenir", None, STATE, w=4.6, h=1.45, tsize=19, bsize=17).move_to([4.45, -1.3, 0])
        self.at(self.cue("gücünü kısar", 2.1))
        self.play(Create(xa[0]), FadeIn(xa[1]), Create(yax[0]), FadeIn(yax[1]), run_time=0.6)
        self.at(self.cue("D ekindeki özerk", 4.8))
        self.play(self.set_src("G.989.2 Ek D.3 / D.5 · G.989.3 §12.1.6"), Create(risers), *[Create(s) for s in segs], run_time=0.8)
        for k, (key, d) in zip([4, 3, 2], (("on iki,", 7.2), ("dokuz,", 9.2), ("altı,", 9.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(vl[k]), segs[k].animate.set_stroke(GOLD, 6), run_time=0.3)
        self.at(self.cue("üç ya da sıfır", 10.2))
        self.play(FadeIn(vl[1]), FadeIn(vl[0]), run_time=0.3)
        for k, (key, d) in enumerate((("eşikler eksi yedi", 13.1), ("eksi on,", 14.6), ("eksi on üç", 15.3))):
            self.at(self.cue(key, d))
            self.play(Create(thr[k][0]), FadeIn(thr[k][1]), *([Create(thr[3][0]), FadeIn(thr[3][1])] if k == 2 else []), run_time=0.35)
        self.at(self.cue("OLT yönlendirmeli", 18.2))
        self.play(FadeIn(c1, shift=LEFT * 0.1), run_time=0.5)
        self.at(self.cue("TC katmanında adımlar", 24.5))
        self.play(FadeIn(c2, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # e12 — step 10: wavelength handover
        self.beat("e12")
        self.stage_clear()
        self.step([10], "Dalga boyu devri", 7)
        chs = VGroup(*[pill(f"λ{i + 1}", CH[i], 20) for i in range(4)]).arrange(RIGHT, buff=0.8).move_to([-2.4, 0.35, 0])
        mk = VGroup(Triangle(color=ONUC, fill_color=ONUC, fill_opacity=1).scale(0.13).rotate(PI), T("ONU", 15, ONUC, BOLD))
        mk[1].next_to(mk[0], UP, buff=0.04)
        mk.next_to(chs[1], UP, buff=0.08)
        hop = CurvedArrow(chs[1].get_top() + UP * 0.05 + RIGHT * 0.2, chs[2].get_top() + UP * 0.05 + LEFT * 0.2, angle=-1.0, color=GOLD, stroke_width=3, tip_length=0.14)
        rule = card("G.989.2 §9.3.7", "ayar boyunca tüm tablo değerleri geçerli\n→ başıboş verici yok", None, GOLD, w=5.6, h=1.45, tsize=18, bsize=17).move_to([3.7, 0.35, 0])
        yb = -1.7
        segs = [("hazırlık", 2.4, STATE), ("fiziksel ayar (PMD)", 3.6, TW_US), ("yeniden senkron", 2.8, GOOD)]
        bar = VGroup()
        x = -4.6
        for s, w_, c in segs:
            r = Rectangle(width=w_, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.75).move_to([x + w_ / 2, yb, 0])
            bar.add(VGroup(r, T(s, 16, BG, BOLD).move_to(r)))
            x += w_
        bt = T("TC devir süresi (Ek F.2) =", 17, TXT, BOLD).next_to(bar, UP, buff=0.12).align_to(bar, LEFT)
        sfc = VGroup(Line([-4.6, yb - 0.45, 0], [-4.6, yb + 0.45, 0], color=GOLD, stroke_width=4),
                     T("an: zamanlanmış SFC (süper çerçeve sayacı)", 16, GOLD, BOLD).next_to([-4.6, yb - 0.45, 0], DOWN, buff=0.1, aligned_edge=LEFT))
        self.at(self.cue("başka bir kanala taşır", 2.4))
        self.play(FadeIn(chs), FadeIn(mk), self.set_src("G.989.2 §9.3.7 · G.989.3 §17.3 · Ek F"), run_time=0.5)
        self.play(Create(hop), mk.animate.next_to(chs[2], UP, buff=0.08), run_time=1.0)
        self.at(self.cue("ayar süresince bütün", 7.7))
        self.play(FadeIn(rule, shift=LEFT * 0.1), run_time=0.6)
        self.at(self.cue("TC tarafında devir", 15.9))
        self.play(FadeIn(bt), run_time=0.4)
        self.at(self.cue("hazırlık,", 18.1))
        self.play(GrowFromEdge(bar[0], LEFT), run_time=0.35)
        self.at(self.cue("fiziksel ayar ve", 18.8))
        self.play(GrowFromEdge(bar[1], LEFT), run_time=0.35)
        self.play(GrowFromEdge(bar[2], LEFT), run_time=0.35)
        self.at(self.cue("süper çerçeve sayacıyla", 23.6))
        self.play(Create(sfc[0]), FadeIn(sfc[1]), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep10_p4B")


class E10P4C(LifeAct):
    HDR, MANIFEST, PREV_BADGE = H10[4], M10("p4"), "ozet"

    def construct(self):
        # e13 — step 11: wavelength locking
        self.beat("e13")
        self.open_strip(11)
        self.step([11], "Dalga boyu kilitleme", 7)
        ya = -1.9
        X = lambda v: -3.4 + v / 40 * 2.7
        filt = VMobject(stroke_color=GOOD, stroke_width=3).set_points_smoothly([[X(v), ya + 2.0 * np.exp(-(v / 18) ** 2 / 2), 0] for v in np.linspace(-40, 40, 50)])
        fb = Line([X(-42), ya, 0], [X(42), ya, 0], color=MUTED, stroke_width=2)
        ft = T("WM süzgeci", 15, GOOD, BOLD).move_to([X(-30), ya + 1.35, 0])
        on = lobe(X, 6, ya, 1.3, 2.5, TW_US, op=0.4)
        tick = DashedLine([X(0), ya, 0], [X(0), ya + 2.15, 0], color=MUTED, stroke_width=1.5)
        dt = T("küçük düzeltmeler (Adjust_Tx_Wavelength)", 15, GOLD, BOLD).move_to([X(0), ya - 0.35, 0])
        fw, fx0, fy = 0.6, 1.0, 0.15
        fr = frames_row(9, fx0, fy, fw, 0.45, STATE, op=0.1)
        cor = VGroup(Line([fx0, fy - 0.4, 0], [fx0, fy + 0.4, 0], color=GOLD, stroke_width=4), T("F: düzeltme", 14, GOLD, BOLD).move_to([fx0, fy + 0.6, 0]))
        b6 = BraceBetweenPoints([fx0, fy - 0.3, 0], [fx0 + 6 * fw, fy - 0.3, 0], DOWN, color=STATE)
        b6t = T("6 çerçeve", 16, STATE, BOLD).next_to(b6, DOWN, buff=0.06)
        b6u = T("= 750 µs", 18, GOLD, BOLD).next_to(b6t, RIGHT, buff=0.15)
        stt = VGroup(Line([fx0 + 6 * fw, fy - 0.4, 0], [fx0 + 6 * fw, fy + 0.4, 0], color=GOOD, stroke_width=4),
                     T("istatistik", 14, GOOD, BOLD).move_to([fx0 + 6 * fw + 0.05, fy + 0.6, 0]))
        dc = card("DOTXi kusuru", "düzeltme istekleri çok sık / çok büyük\n→ verici kayıyor", None, WARN, w=5.2, h=1.35, tsize=20, bsize=17).move_to([3.85, -1.85, 0])
        self.at(self.cue("küçük düzeltmelerle", 3.1))
        self.play(Create(fb), Create(filt), FadeIn(ft), Create(tick), FadeIn(on), self.set_src("G.989.3 §17.4 · Tablo 14-2 · G.989.2 Ek VIII.1"), run_time=0.8)
        self.play(FadeIn(dt), on.animate.shift(LEFT * (X(6) - X(-3))), run_time=0.6)
        self.play(on.animate.shift(RIGHT * (X(1) - X(-3))), run_time=0.5)
        self.at(self.cue("düzeltmeden altı çerçeve", 10.5))
        self.play(FadeIn(fr), Create(cor[0]), FadeIn(cor[1]), run_time=0.5)
        self.play(FadeIn(b6), FadeIn(b6t), Create(stt[0]), FadeIn(stt[1]), run_time=0.5)
        self.at(self.cue("yedi yüz elli", 12.6))
        self.play(FadeIn(b6u, shift=LEFT * 0.1), run_time=0.4)
        self.at(self.cue("Çok sık ya da", 17.2))
        self.play(FadeIn(dc, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("vericinin kaydığını", 23.3))
        self.play(Indicate(dc[2], color=WARN, scale_factor=1.04), run_time=0.6)
        self.end(pad=0.05)

        # e14 — steps 12–13: protection and monitoring
        self.beat("e14")
        self.stage_clear()
        self.step([12, 13], "Koruma ve izleme", 10, num="12–13")
        c1 = ct_box("CT 1", CT_A, 1.3, 0.48, 16, on=True).move_to([-5.6, 0.55, 0])
        c2 = ct_box("CT 2", CT_B, 1.3, 0.48, 16, on=False).move_to([-5.6, -0.75, 0])
        spl = splitter(0.25).move_to([-3.2, -0.1, 0])
        f1 = Line(c1.get_right(), spl.get_left() + UP * 0.07, color=FEED, stroke_width=3)
        f2 = Line(c2.get_right(), spl.get_left() + DOWN * 0.07, color=FEED, stroke_width=3)
        onu = onu_icon("ONU", ONUC, 1.2, 0.55, 16).move_to([-1.35, -0.1, 0])
        fo = Line(spl.get_right(), onu.get_left(), color=FEED, stroke_width=3)
        cut = xmark(Square(0.26).move_to(f1.point_from_proportion(0.45)), WARN, 4)
        ok = T("ONU: ayar yok ✓", 18, GOOD, BOLD).next_to(onu, DOWN, buff=0.25)
        mc = RoundedRectangle(corner_radius=0.16, width=6.0, height=3.2, stroke_color=ACC, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([3.5, -0.85, 0])
        mt = T("Ek II izleme (ONU + OLT)", 19, ACC, BOLD).move_to(mc.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        mr = VGroup(*[VGroup(T(a, 17, MUTED, BOLD), T(b, 18, TXT, BOLD)).arrange(RIGHT, buff=0.25) for a, b in
                      (("sıcaklık", "−45 … +90 °C"), ("gerilim", "0 … 6,55 V"), ("akım", "0 … 819 mA"), ("optik güç", "Tx −28 … +20 · Rx −53 … −4,9 dBm"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for m in mr:
            fit(m, 5.5)
        mr.next_to(mt, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(c1), FadeIn(c2), Create(f1), Create(f2), FadeIn(spl), Create(fo), FadeIn(onu), self.set_src("G.989.3 §18 · G.989.2 Ek II · Tablo II.1"), run_time=0.7)
        self.at(self.cue("Besleyici kesilirse", 3.2))
        self.play(Create(cut), f1.animate.set_stroke(WARN, opacity=0.5), run_time=0.5)
        self.play(set_lamp_(c1, False), set_lamp_(c2, True), f2.animate.set_stroke(GOOD), run_time=0.6)
        self.at(self.cue("ONU yeniden ayarlanmaz", 8.2))
        self.play(FadeIn(ok, shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("Bütün bu süre boyunca", 10.1))
        self.play(FadeIn(mc), FadeIn(mt), run_time=0.5)
        self.at(self.cue("sıcaklığını", 12.9))
        self.play(FadeIn(mr[0], shift=RIGHT * 0.1), run_time=0.35)
        self.at(self.cue("gerilimini", 16.7))
        self.play(FadeIn(mr[1], shift=RIGHT * 0.1), run_time=0.3)
        self.at(self.cue("akımını ve optik", 17.6))
        self.play(FadeIn(mr[2], shift=RIGHT * 0.1), FadeIn(mr[3], shift=RIGHT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        # e15 — step 14: faults
        self.beat("e15")
        self.stage_clear()
        self.step([14], "Arızalar", 5)
        oc = card("ONU: tek kusur", "LODS — senkron kaybı (Tablo 14-3)", None, WARN, w=4.6, h=1.25, tsize=21, bsize=17).move_to([-4.15, 0.35, 0])
        dfs = [("LOBi", "burst kaybı"), ("LOS", "sinyal kaybı"), ("TIWi", "zamanlama kayması"), ("DFi", "devre dışı bırakma hatası")]
        dch = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.1, width=3.7, height=0.55, stroke_color=OLTC, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                              VGroup(T(a, 17, OLTC, BOLD), T(b, 16, TXT)).arrange(RIGHT, buff=0.2)) for a, b in dfs])
        for d in dch:
            fit(d[1], 3.5).move_to(d[0])
        dch.arrange_in_grid(rows=2, cols=2, buff=(0.2, 0.15)).move_to([2.85, 0.35, 0])
        dct = T("OLT CT kusurları (Tablo 14-2)", 16, OLTC, BOLD).next_to(dch, UP, buff=0.12)
        es = RoundedRectangle(corner_radius=0.16, width=12.6, height=1.45, stroke_color=WARN, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([0, -1.85, 0])
        est = T("O7 · Acil durdurma", 22, WARN, BOLD).move_to(es.get_corner(UL) + [0.3, -0.38, 0], aligned_edge=LEFT)
        esb = T("Disable_Serial_Number → ONU vericisini kapatır", 18, TXT).next_to(est, DOWN, buff=0.12, aligned_edge=LEFT)
        lp = VGroup(T("Tx", 16, MUTED, BOLD), lamp(True, 0.11)).arrange(RIGHT, buff=0.12).move_to([1.0, -1.85, 0])
        keep = VGroup(tag("yeniden başlatma ✓", WARN, 16), tag("güç kesintisi ✓", WARN, 16)).arrange(DOWN, buff=0.12).move_to([4.9, -1.85, 0])
        kt = T("durum korunur:", 15, MUTED).next_to(keep, LEFT, buff=0.15)
        self.at(self.cue("tek kusurudur", 1.9))
        self.play(FadeIn(oc, shift=UP * 0.1), self.set_src("G.989.3 Tablo 14-2 / 14-3 · §11.3.3.5 · Tablo 12-1 (O7)"), run_time=0.5)
        self.at(self.cue("burst kaybı", 4.9))
        self.play(FadeIn(dct), FadeIn(dch[0], shift=UP * 0.1), run_time=0.4)
        self.at(self.cue("sinyal kaybı", 7.4))
        self.play(FadeIn(dch[1], shift=UP * 0.1), run_time=0.3)
        self.at(self.cue("zamanlama kayması ve", 8.5))
        self.play(FadeIn(dch[2], shift=UP * 0.1), FadeIn(dch[3], shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("En sert olanı", 14.2))
        self.play(FadeIn(es), FadeIn(est), FadeIn(lp), run_time=0.5)
        self.at(self.cue("devre dışı bırakılan", 16.8))
        self.play(FadeIn(esb, shift=UP * 0.1), Transform(lp[1], lamp(False, 0.11).move_to(lp[1])), run_time=0.6)
        self.at(self.cue("yeniden başlatmada ve", 22.0))
        self.play(FadeIn(kt), FadeIn(keep, shift=LEFT * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # e16 — step 15: leaving
        self.beat("e16")
        self.stage_clear()
        self.step([15], "Ayrılış", None)
        o5 = sbox("O5 · Çalışma", None, STATE, 2.5, 0.7, 18).move_to([4.4, 0.45, 0])
        o1 = sbox("O1 · Başlangıç", None, STATE, 2.5, 0.7, 18).move_to([-4.4, 0.45, 0])
        back = CurvedArrow(o5.get_left() + DOWN * 0.15, o1.get_right() + DOWN * 0.15, angle=-0.35, color=WARN, stroke_width=3, tip_length=0.16)
        bt = T("Deactivate_ONU-ID", 18, WARN, BOLD).move_to([0, 0.75, 0])
        sc = RoundedRectangle(corner_radius=0.16, width=10.6, height=2.0, stroke_color=TW_US, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([0, -1.75, 0])
        sct = T("sonraki Serial_Number_ONU · Activation Debug (oktet 40)", 19, TW_US, BOLD).move_to(sc.get_corner(UL) + [0.3, -0.35, 0], aligned_edge=LEFT)
        rows = VGroup(*[VGroup(T(a, 17, GOLD, BOLD), T(b, 17, TXT)).arrange(RIGHT, buff=0.25) for a, b in
                        (("1101", "güç kaybı"), ("0110 / 0111", "LODS (O2-3 / O4)"), ("1000 … 1100", "zamanlayıcı: TOZ · TO1 · TO2 · TO4 · TO5"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.next_to(sct, DOWN, buff=0.18, aligned_edge=LEFT)
        self.at(self.cue("ONU kimliği iptal", 1.7))
        self.play(FadeIn(o5), FadeIn(o1), self.set_src("G.989.3 §11.3 (Deactivate_ONU-ID) · Serial_Number_ONU oktet 40"), run_time=0.5)
        self.play(Create(back), FadeIn(bt), run_time=0.7)
        self.at(self.cue("baştan başlar", 5.7))
        self.play(Indicate(self.strip.chips[0], color=GOLD, scale_factor=1.4), Indicate(o1, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.at(self.cue("Bir sonraki aktivasyonda", 7.8))
        self.play(FadeIn(sc), run_time=0.4)
        self.at(self.cue("aktivasyon hata ayıklama", 10.2))
        self.play(FadeIn(sct, shift=UP * 0.1), run_time=0.5)
        for i, (key, d) in enumerate((("güç kaybı mı", 18.1), ("senkron kaybı mı", 19.2), ("bir zamanlayıcı mı", 20.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[i], shift=RIGHT * 0.1), run_time=0.3)
        self.end(pad=0.05)

        self.note10("e17", [("1", "Tek ızgara: 125 µs", "LODS 3 kötü çerçeve · LOBi 4 burst · LOS 4 çerçeve · kilit ölçümü 6 çerçeve (750 µs).", "Bir:"),
                            ("2", "ONU optiği N1 … E1 aynı (G.989.3 Ek X)", "Bölüm 2'deki kural doğrulanır: ODN sınıfını OLT taşır.", "İki:")])
        self.bridge_beat("e18", "Kâğıt üstünde hikâye tamam.\nSahada ise işler her zaman bu sırayla gitmez.", label="Sıradaki: Sahada", pad=0.3)
        self.save_timeline("ep10_p4C")


def set_lamp_(ct, on):
    return Transform(ct[2], lamp(on, 0.08).move_to(ct[2].get_center()))
