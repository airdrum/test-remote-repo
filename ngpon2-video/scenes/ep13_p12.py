"""S2·B3 · Perde 1 (XGEM çerçevesi — G.989.3 §9.1, §6.1.3.1, §6.1.5.1) and Perde 2 (sınırlama — §9.2, Tablo 14-1)."""
from ep13_common import *


def legend_row(name, c, desc, size=17):
    return VGroup(tag(name, c, size - 1), T(desc, size, TXT)).arrange(RIGHT, buff=0.2)


# ================================ PERDE 1 ======================================
class E13P1A(Act13):
    HDR, MANIFEST, FIRST = H13[1], M13("p1"), True

    def construct(self):
        # b1 — §9 opening sentence: what XGEM carries, where; inherited from G.987.3; unchanged since 2021
        self.beat("b1")
        tc = self.title_card("PERDE 1", "XGEM çerçevesi")
        self.at(self.cue("Dokuzuncu madde", 2.1))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("§9 — XGEM neyi, nerede taşır?")
        s1 = tile("kullanıcı çerçeveleri", SAC, 2.6, 0.55, 17, 0.15).move_to([-5.0, 1.45, 0])
        s2 = tile("OMCI mesajları", OMC, 2.6, 0.55, 17, 0.15).move_to([-5.0, 0.35, 0])
        xb = sbox("XGEM", "kapsülleme", SAC, 2.0, 1.1, 26, 16).move_to([-1.75, 0.9, 0])
        org = tag("G.987.3 §9 · XG-PON'dan", MUTED, 15).next_to(xb, DOWN, buff=0.15)
        sa = VGroup(arrow(s1.get_right(), xb.get_left() + UP * 0.2, MUTED, 2.2, 0.12), arrow(s2.get_right(), xb.get_left() + DOWN * 0.2, MUTED, 2.2, 0.12))
        x0 = 0.35
        ds = strip([FS_(0.5, "HL"), FS_(0.9, "BWmap", BWC), FS_(0.95, "PLOAM", PLDC, 0.25), (3.2, "FS yükü", PAYC, 0.14), FS_(0.5, "BIP", BIPC)], x0, 1.55, 0.55, 15)
        us = strip([FS_(1.0, "başlık"), FS_(0.75, "DBRu", BWC), (3.8, "FS yükü", PAYC, 0.14), FS_(0.5, "BIP", BIPC)], x0, 0.25, 0.55, 15)
        dl = T("↓ FS çerçevesi", 15, MUTED, BOLD).next_to(ds, UP, buff=0.08).align_to(ds, LEFT)
        ul = T("↑ FS burst'ü", 15, MUTED, BOLD).next_to(us, UP, buff=0.08).align_to(us, LEFT)
        xa = VGroup(arrow(xb.get_right() + UP * 0.2, ds.get_left() + LEFT * 0.06, SAC, 2.2, 0.12),
                    arrow(xb.get_right() + DOWN * 0.2, us.get_left() + LEFT * 0.06, SAC, 2.2, 0.12))
        dsx = strip([H_(0.26), P_(0.9), H_(0.26), P_(1.1), H_(0.26), P_(0.36)], ds[3].get_left()[0] + 0.03, 1.55, 0.47, 14)
        usx = strip([H_(0.26), P_(1.2), H_(0.26), P_(0.8), H_(0.26), P_(0.9)], us[2].get_left()[0] + 0.03, 0.25, 0.47, 14)
        caps = VGroup(*[tag(s, SAC, 19) for s in ("parçalama", "kapsülleme", "sınırlama")]).arrange(RIGHT, buff=0.35)
        capl = T("iki yönde de:", 19, MUTED, BOLD)
        crow = VGroup(capl, caps).arrange(RIGHT, buff=0.3).move_to([0, -1.25, 0])
        ed = VGroup(*[tile(s, c, 2.2, 0.5, 16, 0.15) for s, c in (("G.989.3 · 2021", ACC), ("Amd.1 · 2023", GOLD), ("Amd.2 · 2025", GOLD))]).arrange(RIGHT, buff=0.45)
        ea = VGroup(*[arrow(ed[i].get_right(), ed[i + 1].get_left(), MUTED, 2, 0.1) for i in range(2)])
        same = T("§9: değişiklik yok", 18, GOOD, BOLD)
        erow = VGroup(VGroup(ed, ea), same).arrange(RIGHT, buff=0.4).move_to([0, -2.5, 0])
        self.play(self.set_src("G.989.3 §9 · Amd.1 / Amd.2: değişiklik yok"), run_time=0.3)
        self.at(self.cue("kullanıcı çerçeveleri ve OMCI", 4.5))
        self.play(FadeIn(s1, shift=RIGHT * 0.1), FadeIn(s2, shift=RIGHT * 0.1), run_time=0.6)
        self.at(self.cue("aşağı yön çerçevelerinin", 7.9))
        self.play(FadeIn(dl), FadeIn(ds), run_time=0.5)
        self.play(FadeIn(ul), FadeIn(us), run_time=0.5)
        self.at(self.cue("XG-PON'dan gelen", 13.1))
        self.play(FadeIn(xb, scale=0.9), FadeIn(org, shift=UP * 0.08), run_time=0.6)
        self.at(self.cue("XGEM ile taşınır", 16.3))
        self.play(*[GrowArrow(a) for a in sa], *[GrowArrow(a) for a in xa], FadeOut(ds[3][1]), FadeOut(us[2][1]), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(q) for q in dsx], lag_ratio=0.1), LaggedStart(*[FadeIn(q) for q in usx], lag_ratio=0.1), run_time=0.7)
        self.at(self.cue("XGEM iki yönde de", 17.8))
        self.play(FadeIn(capl), FadeIn(caps[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("kapsüllemeyi ve sınırlamayı", 20.3))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in caps[1:]], lag_ratio=0.3), run_time=0.6)
        self.at(self.cue("Bu metin iki bin yirmi", 23.5))
        self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.08) for e in ed], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in ea], lag_ratio=0.2), run_time=0.8)
        self.play(FadeIn(same, shift=LEFT * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # b2 — transmit / receive chains; DS one multiplexing key, US two levels
        self.beat("b2")
        self.clear(h)
        h = self.show_heading("Hizmet uyarlama: verici ve alıcı", h)
        tx_n = [("SDU", 0.9, SAC), ("parçala", 1.35, SAC), ("Port-ID ata", 1.75, PIDC), ("kapsülle", 1.45, SAC), ("şifrele (ops.)", 1.9, GOLD), ("FS yükü", 1.4, PAYC)]
        rx_n = [("FS yükü", 1.4, PAYC), ("sınırla", 1.35, SAC), ("Port-ID süz", 1.75, PIDC), ("şifre çöz", 1.45, GOLD), ("birleştir", 1.4, SAC), ("teslim", 1.1, SAC)]

        def chain(nodes, lab):
            ts = VGroup(*[tile(s, c, w, 0.5, 16, 0.15) for s, w, c in nodes]).arrange(RIGHT, buff=0.42)
            ll = T(lab, 17, MUTED, BOLD).next_to(ts, LEFT, buff=0.35)
            ar = VGroup(*[arrow(ts[i].get_right(), ts[i + 1].get_left(), MUTED, 2, 0.1) for i in range(len(ts) - 1)])
            return VGroup(ll, ts, ar)
        tx = chain(tx_n, "verici")
        rx = chain(rx_n, "alıcı")
        tx.move_to([0, 1.55, 0])
        rx.next_to(tx, DOWN, buff=0.5).align_to(tx[1], LEFT).shift(LEFT * (rx[1].get_left()[0] - tx[1].get_left()[0]))
        rx[0].align_to(tx[0], RIGHT)
        txa, rxa = tx[2], rx[2]
        cl = frame_box("↓ tek düzey", OLTC, 6.0, 2.3, 20)
        cr = frame_box("↑ iki düzey", ONUC, 6.0, 2.3, 20)
        VGroup(cl, cr).arrange(RIGHT, buff=0.35).move_to([0, -1.85, 0])
        dsx = strip([H_(0.42, "A", ACC), P_(0.9), H_(0.42, "B", GOLD), P_(1.3), H_(0.42, "A", ACC), P_(0.7)], cl[0].get_left()[0] + 0.35, cl[0].get_y() - 0.05, 0.5, 15)
        dsl = T("XGEM Port-ID = tek çoğullama anahtarı", 16, PIDC, BOLD).next_to(dsx, DOWN, buff=0.2).align_to(dsx, LEFT)
        bw = tag("BWmap: Alloc-ID → kim gönderir", BWC, 15).next_to(cr[1], DOWN, buff=0.15).align_to(cr[1], LEFT)
        usx = strip([FS_(0.65, "DBRu", BWC), H_(0.42, "A", ACC), P_(1.0), H_(0.42, "C", PINK), P_(1.2)], 0, 0, 0.45, 14)
        usx.next_to(bw, DOWN, buff=0.2).align_to(bw, LEFT).shift(RIGHT * 0.07)
        alb = SurroundingRectangle(usx, color=BWC, buff=0.07, stroke_width=2)
        usl = T("XGEM başlığındaki Port-ID → hangi akış", 15, PIDC, BOLD).next_to(alb, DOWN, buff=0.12).align_to(bw, LEFT)
        self.play(self.set_src("G.989.3 §6.1.3.1 · §6.1.5.1"), FadeIn(tx[0]), run_time=0.4)
        self.at(self.cue("Verici bir birimi gerekirse", 0.3))
        self.play(FadeIn(tx[1][0]), GrowArrow(txa[0]), FadeIn(tx[1][1]), run_time=0.6)
        self.at(self.cue("XGEM port kimliği atar", 3.1))
        self.play(GrowArrow(txa[1]), FadeIn(tx[1][2]), run_time=0.4)
        self.at(self.cue("kapsüller", 5.7))
        self.play(GrowArrow(txa[2]), FadeIn(tx[1][3]), run_time=0.4)
        self.at(self.cue("isterse yükü şifreler", 6.6))
        self.play(GrowArrow(txa[3]), FadeIn(tx[1][4]), GrowArrow(txa[4]), FadeIn(tx[1][5]), run_time=0.6)
        self.at(self.cue("alıcı tersini yapar", 8.7))
        self.play(FadeIn(rx[0]), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.06) for t in rx[1]], lag_ratio=0.12), LaggedStart(*[GrowArrow(a) for a in rxa], lag_ratio=0.12), run_time=1.0)
        self.at(self.cue("Aşağı yönde tek çoğullama", 10.3))
        self.play(FadeIn(cl), FadeIn(dsx, shift=RIGHT * 0.08), run_time=0.6)
        self.play(FadeIn(dsl), run_time=0.4)
        self.at(self.cue("Yukarı yönde iki düzey", 14.6))
        self.play(FadeIn(cr), run_time=0.4)
        self.at(self.cue("tahsis kimliği kimin", 17.2))
        self.play(FadeIn(bw, shift=RIGHT * 0.08), FadeIn(usx), Create(alb), run_time=0.6)
        self.at(self.cue("port kimliği ise o tahsisin", 20.1))
        self.play(FadeIn(usl, shift=LEFT * 0.08), Indicate(VGroup(usx[1], usx[3]), color=PIDC, scale_factor=1.15), run_time=0.7)
        self.end(pad=0.05)

        # b3 — PMD bridge: broadcast DS (S1·B1) ↔ Port-ID filtering; privacy from encryption
        self.beat("b3")
        self.clear()
        h, chp = self.pmd_head("PMD Köprüsü — yayın ↓ ve süzme", s1chip(1))
        olt = ct_box("OLT CT", OLTC, 1.3, 0.6, 17).move_to([-6.1, 0.45, 0])
        spl = splitter(0.38).move_to([-4.55, 0.45, 0])
        ys = (1.55, 0.45, -0.65)
        onus = VGroup(*[onu_box(f"ONU {i + 1}", ONUC, 1.2, 0.55, 16).move_to([-2.65, y, 0]) for i, y in enumerate(ys)])
        fib = VGroup(Line(olt.get_right(), spl.get_left(), color=FEED, stroke_width=3),
                     *[Line(spl.get_right(), o.get_left(), color=FEED, stroke_width=2.5) for o in onus])
        own = [ACC, GOLD, PINK]
        rows = VGroup()
        for i, y in enumerate(ys):
            s = strip([H_(0.42, "1", own[0]), P_(1.2), H_(0.42, "2", own[1]), P_(1.5), H_(0.42, "3", own[2]), P_(1.0), H_(0.42, "1", own[0]), P_(0.95)], -1.75, y, 0.48, 15)
            rows.add(s)
        rl = T("aynı bitler, her ONU'da", 15, MUTED, BOLD).next_to(rows, UP, buff=0.1).align_to(rows, LEFT)
        reads = VGroup(*[VGroup(*[SurroundingRectangle(r[k], color=GOLD, buff=0.02, stroke_width=2.2) for k in (0, 2, 4, 6)]) for r in rows])
        keep = {0: (1, 7), 1: (3,), 2: (5,)}
        dims = [VGroup(*[r[k] for k in (1, 3, 5, 7) if k not in keep[i]]) for i, r in enumerate(rows)]
        mine = VGroup(*[VGroup(*[r[k] for k in keep[i]]) for i, r in enumerate(rows)])
        fl = VGroup(tag("her başlık okunur", GOLD, 16), tag("yalnızca kendi portunun yükü işlenir", ONUC, 16)).arrange(RIGHT, buff=0.3).move_to([1.1, -1.55, 0])
        nt = VGroup(tag("süzme ≠ gizlilik", WARN, 18), T("→", 22, MUTED, BOLD), lock(GOLD, 0.3), T("yük şifrelemesi · Perde 4", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -2.65, 0])
        self.play(FadeIn(chp, shift=LEFT * 0.1), self.set_src("G.989.3 §6.1.5.1 · S1·B1 (yayın ↓, güç bölücü)"), run_time=0.5)
        self.at(self.cue("Birinci sezonun birinci", 1.0))
        self.play(FadeIn(olt), FadeIn(spl), Create(fib[0]), run_time=0.6)
        self.at(self.cue("güç bölücü", 6.7))
        self.play(*[Create(f) for f in fib[1:]], LaggedStart(*[FadeIn(o) for o in onus], lag_ratio=0.2), Indicate(spl, color=FEED), run_time=0.8)
        self.at(self.cue("kanalın her bitini her ONU'ya", 7.6))
        self.play(FadeIn(rl), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.2), run_time=1.0)
        self.at(self.cue("Port kimliğiyle süzme", 10.8))
        self.play(*[Indicate(VGroup(*[r[k] for k in (0, 2, 4, 6)]), color=GOLD, scale_factor=1.05) for r in rows], run_time=0.7)
        self.at(self.cue("her ONU kanaldaki her XGEM", 15.6))
        self.play(*[Create(r) for r in reads], FadeIn(fl[0], shift=UP * 0.08), run_time=0.7)
        self.at(self.cue("ama yalnızca kendi portlarının", 19.1))
        self.play(*[d.animate.set_opacity(0.18) for d in dims], *[m.animate.set_fill(opacity=0.45) for m in mine], FadeIn(fl[1], shift=UP * 0.08), run_time=0.7)
        self.at(self.cue("Gizlilik süzmeden değil", 22.8))
        self.play(FadeIn(nt[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("dördüncü perdedeki yük", 24.8))
        self.play(FadeIn(nt[1:], shift=LEFT * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # b4 — FS payload sections DS / US; all sizes multiples of 4 → frames tile exactly, headers on word boundaries
        self.beat("b4")
        self.clear()
        self.set_badge("std")
        h = self.show_heading("XGEM çerçeveleri yük bölümlerini doldurur")
        x0 = -6.2
        ds = strip([FS_(0.9, "HLend"), FS_(1.5, "BWmap", BWC), FS_(1.4, "PLOAMd", PLDC, 0.25), (7.2, "FS yükü", PAYC, 0.14), FS_(0.8, "BIP", BIPC)], x0, 1.5, 0.55, 15)
        dl = T("↓ FS çerçevesi", 15, MUTED, BOLD).next_to(ds, UP, buff=0.08).align_to(ds, LEFT)
        db = brace_lbl(ds[3], "FS yükü = FS çerçevesi − başlık − kuyruk", PAYC, DOWN, 16)
        us = strip([(1.0, "PSBu", PHC, 0.2), FS_(0.95, "başlık"), FS_(0.75, "DBRu", BWC), (3.3, "yük · tahsis 1", PAYC, 0.14), (3.45, "yük · tahsis 2", PAYC, 0.22), FS_(0.8, "BIP", BIPC)], x0, -0.35, 0.55, 15)
        ul = T("↑ FS burst'ü", 15, MUTED, BOLD).next_to(us, UP, buff=0.08).align_to(us, LEFT)
        ub = brace_lbl(VGroup(us[3], us[4]), "her tahsisin kendi yük bölümü", PAYC, DOWN, 15)
        dbr = tag("istenmişse 4 B DBRu düşülür", BWC, 15).next_to(us[2], DOWN, buff=0.15)
        y = -2.45
        cw = 0.42
        frames = [("H", 2), ("", 3), ("H", 2), ("", 6), ("H", 2), ("", 1), ("H", 2), ("", 9)]
        cw = 0.36
        wk, hidx = [], []
        for lab, n in frames:
            if lab:
                hidx.append(len(wk))
            for j in range(n):
                wk.append(("H" if (lab and j == 0) else "", SAC, 0.55 if lab else 0.14))
        wr = words(wk, cw, 0.45, 14).move_to([0.9, y, 0])
        ticks = VGroup(*[Line([c.get_left()[0], y - 0.32, 0], [c.get_left()[0], y - 0.4, 0], color=MUTED, stroke_width=1.5) for c in wr] +
                       [Line([wr.get_right()[0], y - 0.32, 0], [wr.get_right()[0], y - 0.4, 0], color=MUTED, stroke_width=1.5)])
        wl = T("1 kare = 4 bayt", 15, MUTED, BOLD).next_to(wr, LEFT, buff=0.3)
        hk = tag("hesap", GOLD, 15).next_to(wr, UP, buff=0.12).align_to(wr, LEFT)
        st = VGroup(T("yük, FS alanları ve XGEM çerçeveleri: hepsi 4'ün katı", 17, TXT, BOLD),
                    T("→ yük tam döşenir · her başlık bir sözcük sınırında", 17, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        st.next_to(hk, RIGHT, buff=0.3).align_to(hk, DOWN)
        hs = VGroup(*[SurroundingRectangle(wr[i:i + 2], color=GOLD, buff=0.02, stroke_width=2.5) for i in hidx])
        self.play(self.set_src("G.989.3 §9.1.1 · §6.1.3.2 · 4'ün katı: hesap"), run_time=0.3)
        self.at(self.cue("XGEM çerçeveleri yük bölümlerini", 0.3))
        self.play(FadeIn(dl), FadeIn(ds), run_time=0.6)
        self.at(self.cue("çerçeveden başlık ve kuyruk", 4.5))
        self.play(Indicate(VGroup(ds[0], ds[1], ds[2], ds[4]), color=HLC, scale_factor=1.04), FadeIn(db), run_time=0.7)
        self.at(self.cue("yukarı yönde her tahsisin", 8.5))
        self.play(FadeIn(ul), FadeIn(us), FadeIn(ub), run_time=0.7)
        self.at(self.cue("istenmişse dört baytlık", 11.7))
        self.play(FadeIn(dbr, shift=DOWN * 0.08), Indicate(us[2], color=BWC, scale_factor=1.1), run_time=0.6)
        self.at(self.cue("Bizim hesabımız", 15.6))
        self.play(FadeIn(hk), FadeIn(wl), FadeIn(ticks), run_time=0.4)
        self.at(self.cue("bu boyların hepsi", 17.0))
        self.play(FadeIn(st[0], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("Çerçeveler yükü tam döşer", 21.6))
        self.play(LaggedStart(*[FadeIn(c) for c in wr], lag_ratio=0.03), run_time=1.0)
        self.at(self.cue("her başlık bir sözcük sınırında", 23.8))
        self.play(FadeIn(st[1], shift=RIGHT * 0.08), Create(hs), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep13_p1A")


class E13P1B(Act13):
    HDR, MANIFEST, PREV_BADGE = H13[1], M13("p1"), "std"

    def construct(self):
        # b5 — the 64-bit header, six fields; 51 protected bits + 13-bit HEC
        self.beat("b5")
        h = self.show_heading("XGEM başlığı — 64 bit, altı alan")
        hd = xhdr(12.4, 0.75, 20, 15).move_to([0, 1.2, 0])
        outl = Rectangle(width=12.4, height=0.75, stroke_color=MUTED, stroke_width=2).move_to(hd)
        ol = T("64 bit = 8 bayt", 18, MUTED, BOLD).move_to(outl)
        leg = [("PLI", PLIC, "yük uzunluğu göstergesi"), ("KI", KIC, "anahtar indeksi"), ("XGEM Port-ID", PIDC, "port kimliği"),
               ("Options", OPTC, "seçenekler"), ("LF", LFC, "son parça biti"), ("HEC", HECC, "BCH(63, 12, 2) + eşlik")]
        lr = VGroup(*[legend_row(a, c, d, 18) for a, c, d in leg])
        col1 = VGroup(*lr[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        col2 = VGroup(*lr[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        VGroup(col1, col2).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, -0.6, 0])
        pb = BraceBetweenPoints([hd[0][0].get_left()[0], 1.61, 0], [hd[4][0].get_right()[0], 1.61, 0], UP, color=GOLD)
        pbl = T("51 korunan bit", 17, GOLD, BOLD).next_to(pb, UP, buff=0.04)
        hb = BraceBetweenPoints([hd[5][0].get_left()[0], 1.61, 0], [hd[5][0].get_right()[0], 1.61, 0], UP, color=HECC)
        hbl = T("13 bit HEC", 17, HECC, BOLD).next_to(hb, UP, buff=0.04)
        same = VGroup(T("aynı HEC biçimi:", 17, MUTED, BOLD), *[tile(s, c, w, 0.48, 16, 0.15) for s, c, w in (("BWmap tahsis yapısı", BWC, 2.7), ("SFC yapısı", SFCC, 1.7), ("OC yapısı", OCC, 1.6))], s2chip(2, 16))
        same.arrange(RIGHT, buff=0.25).move_to([0, -2.6, 0])
        fit(same, 12.6)
        self.play(self.set_src("G.989.3 §9.1.2 · Şekil 9-2 · Ek A.1"), run_time=0.3)
        self.play(Create(outl), FadeIn(ol), run_time=0.6)
        steps = (("On dört bitlik yük", 3.0), ("iki bitlik anahtar", 6.3), ("on altı bitlik XGEM port", 8.6),
                 ("on sekiz bitlik seçenekler", 11.4), ("bir bitlik son parça", 14.2), ("on üç bitlik HEC", 16.4))
        for k, (key, d) in enumerate(steps):
            self.at(self.cue(key, d))
            anims = [FadeIn(hd[k], shift=UP * 0.06), FadeIn(lr[k], shift=RIGHT * 0.08)]
            if k == 0:
                anims += [FadeOut(ol), FadeOut(outl)]
            self.play(*anims, run_time=0.45)
        self.at(self.cue("İlk beş alan elli bir", 18.1))
        self.play(GrowFromCenter(pb), FadeIn(pbl), GrowFromCenter(hb), FadeIn(hbl), run_time=0.6)
        self.at(self.cue("HEC onları geçen bölümde", 20.7))
        self.play(FadeIn(same[0]), FadeIn(same[4], shift=LEFT * 0.08), run_time=0.5)
        self.at(self.cue("tahsis yapısı", 25.1))
        self.play(FadeIn(same[1], shift=UP * 0.08), run_time=0.35)
        self.at(self.cue("sayaç ve OC ile aynı", 26.2))
        self.play(FadeIn(same[2], shift=UP * 0.08), FadeIn(same[3], shift=UP * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # b6 — PLI: 14 bits, 0 … 16 383; examples 2000 / 9000; byte-exact, payload is 4-byte aligned
        self.beat("b6")
        self.clear(hd)
        h = self.show_heading("PLI — yük uzunluğu göstergesi", h)
        self.play(hd.animate.move_to([0, 1.8, 0]), run_time=0.5)
        gl = glow(hd[0][0], PLIC, 0.05)
        X = lambda v: -5.6 + v / 16383 * 11.2
        ay = 0.2
        ax = Line([X(0), ay, 0], [X(16383), ay, 0], color=MUTED, stroke_width=2.5)
        ends = VGroup(T("0", 17, MUTED, BOLD).next_to([X(0), ay, 0], DOWN, buff=0.12),
                      T("16 383 = 2¹⁴ − 1", 17, PLIC, BOLD).next_to([X(16383), ay, 0], DOWN, buff=0.12).shift(LEFT * 0.6))
        etk = VGroup(*[Line([X(v), ay - 0.08, 0], [X(v), ay + 0.08, 0], color=MUTED, stroke_width=2) for v in (0, 16383)])
        mk = VGroup()
        for v, s in ((2000, "2000 B · genişletilmiş Ethernet"), (9000, "9000 B · jumbo Ethernet")):
            d = Dot([X(v), ay, 0], radius=0.08, color=GOLD)
            t = T(s, 16, GOLD, BOLD).next_to(d, UP, buff=0.15)
            mk.add(VGroup(d, t))
        al = T("L, bayt: SDU ya da SDU parçasının boyu", 16, MUTED, BOLD).next_to(ax, DOWN, buff=0.22)
        bx = -6.2
        cells = VGroup()
        for i in range(12):
            c = SAC if i < 9 else PADC
            r = Rectangle(width=0.5, height=0.5, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.3 if i < 9 else 0.5)
            cells.add(r)
        cells.arrange(RIGHT, buff=0).move_to([bx + 3.0, -2.15, 0])
        wbs = VGroup(*[Line([cells[4 * k].get_left()[0], -2.48, 0], [cells[4 * k].get_left()[0], -1.82, 0], color=TXT, stroke_width=3.5) for k in range(3)],
                     Line([cells.get_right()[0], -2.48, 0], [cells.get_right()[0], -1.82, 0], color=TXT, stroke_width=3.5))
        bL = brace_lbl(cells[:9], "PLI = 9 · bayta kadar doğru", PLIC, UP, 16)
        bP = brace_lbl(cells, "yük P = 12 · 4 bayta hizalı", SAC, DOWN, 16)
        ex = VGroup(tag("örnek", MUTED, 15), T("L = 9 → P = 12, 3 bayt dolgu (§9.1.3)", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).next_to(cells, RIGHT, buff=0.6)
        self.play(self.set_src("G.989.3 §9.1.2 · §9.1.3"), Create(gl), run_time=0.5)
        self.at(self.cue("başlıktan sonra gelen birimin", 2.0))
        self.play(Create(ax), FadeIn(etk), FadeIn(al), run_time=0.6)
        self.at(self.cue("sıfırdan on altı bin", 8.1))
        self.play(FadeIn(ends), run_time=0.5)
        self.at(self.cue("iki bin baytlık genişletilmiş", 12.8))
        self.play(FadeIn(mk[0], shift=DOWN * 0.08), run_time=0.5)
        self.at(self.cue("dokuz bin baytlık jumbo", 17.4))
        self.play(FadeIn(mk[1], shift=DOWN * 0.08), run_time=0.5)
        self.at(self.cue("Değer bayta kadar doğrudur", 21.0))
        self.play(FadeIn(cells[:9]), FadeIn(bL), run_time=0.6)
        self.at(self.cue("ama yükün boyu değildir", 23.3))
        self.play(FadeIn(cells[9:]), FadeIn(bP), FadeIn(ex, shift=LEFT * 0.08), run_time=0.6)
        self.at(self.cue("yük dört bayta hizalanır", 25.3))
        self.play(Create(wbs), run_time=0.5)
        self.end(pad=0.05)

        # b7 — KI (later), Options (FFS, 0x00000 = 20 bits vs 18), LF
        self.beat("b7")
        self.play(FadeOut(VGroup(ax, etk, ends, mk, al, cells, wbs, bL, bP, ex)), FadeOut(gl), run_time=0.4)
        h = self.heading12("KI · Options · LF", h)
        g1 = glow(hd[1][0], KIC, 0.05)
        kt = tag("→ Perde 4: şifreleme", KIC, 16).move_to([hd[1][0].get_x() + 0.9, 0.55, 0])
        g2 = glow(hd[3][0], OPTC, 0.05)
        ot = tag("“for further study”", OPTC, 16).move_to([hd[3][0].get_x(), 0.55, 0])
        rr = VGroup(legend_row("verici", MUTED, "0 yazar", 18), legend_row("alıcı", MUTED, "yok sayar", 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rr.move_to([-4.5, -0.35, 0])
        hx = VGroup(T("metin:", 17, MUTED, BOLD), HX("0x00000", 26, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([-1.0, -0.35, 0])
        b20 = bitcells("0" * 20, 5.6, 0.3, OPTC, stroke=OPTC).move_to([-3.4, -1.35, 0])
        b18 = bitcells("0" * 18, 5.04, 0.3, OPTC, stroke=OPTC).move_to([-3.4, -2.0, 0]).align_to(b20, RIGHT)
        ex2 = VGroup(*[SurroundingRectangle(b20[i], color=WARN, buff=0.0, stroke_width=3) for i in (0, 1)])
        l20 = T("5 hane × 4 = 20 bit", 16, TXT, BOLD).next_to(b20, RIGHT, buff=0.25)
        l18 = T("alan: 18 bit", 16, OPTC, BOLD).next_to(b18, RIGHT, buff=0.25)
        l18.align_to(l20, LEFT)
        lfx = 2.6
        lfr = VGroup()
        for lab, lf, c in (("tam birim", "1", SAC), ("parça 1 (ilk)", "0", SAC), ("son parça", "1", SAC)):
            s = strip([H_(0.42), P_(1.9, lab)], 0, 0, 0.48, 15)
            t = VGroup(T("LF =", 17, LFC, BOLD), HX(lf, 20, LFC, BOLD)).arrange(RIGHT, buff=0.12)
            lfr.add(VGroup(s, t).arrange(RIGHT, buff=0.3))
        lfr.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([lfx + 1.6, -1.2, 0])
        g3 = glow(hd[4][0], LFC, 0.05)
        self.play(self.set_src("G.989.3 §9.1.2 · Şekil 9-2"), run_time=0.3)
        self.at(self.cue("Anahtar indeksini dördüncü", 0.3))
        self.play(Create(g1), FadeIn(kt, shift=UP * 0.08), run_time=0.6)
        self.at(self.cue("Seçenekler alanı hâlâ", 3.7))
        self.play(Create(g2), FadeIn(ot, shift=UP * 0.08), run_time=0.6)
        self.at(self.cue("verici sıfır yazar", 7.1))
        self.play(FadeIn(rr[0], shift=RIGHT * 0.08), run_time=0.35)
        self.at(self.cue("alıcı yok sayar", 8.7))
        self.play(FadeIn(rr[1], shift=RIGHT * 0.08), run_time=0.35)
        self.at(self.cue("Metin bu sıfırı beş haneli", 10.0))
        self.play(FadeIn(hx, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("yani yirmi bit", 14.0))
        self.play(FadeIn(b20), FadeIn(l20), run_time=0.5)
        self.at(self.cue("alan on sekiz bittir", 16.4))
        self.play(FadeIn(b18), FadeIn(l18), Create(ex2), run_time=0.6)
        self.at(self.cue("Son parça biti", 18.1))
        self.play(Create(g3), run_time=0.4)
        self.at(self.cue("taşınan şey bir birimin son", 19.4))
        self.play(FadeIn(lfr[0], shift=LEFT * 0.08), FadeIn(lfr[2], shift=LEFT * 0.08), run_time=0.5)
        self.at(self.cue("değilse sıfırdır", 24.1))
        self.play(FadeIn(lfr[1], shift=LEFT * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # b8 — formula (9-1) and 0x55 padding
        self.beat("b8")
        self.clear()
        h = self.show_heading("Yük boyu — formül (9-1)")
        p = apanel(6.2, 3.0, "(9-1) · dolu (boş olmayan) XGEM çerçevesi", PLIC).move_to([-3.35, 0.75, 0])
        fr = [("P = 4 · ⌈L / 4⌉", "L ≥ 8"), ("P = 8", "0 < L < 8"), ("P = 0", "L = 0")]
        frm = VGroup()
        for a, b in fr:
            frm.add(VGroup(HX(a, 22, TXT, BOLD), T(b, 19, PLIC, BOLD)))
        for r in frm:
            r[1].next_to(r[0], RIGHT, buff=0.3)
        frm.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(p[0]).shift(DOWN * 0.15)
        for r in frm:
            r[1].set_x(p[0].get_left()[0] + 4.7, direction=LEFT)
        lp = T("L = PLI (bayt) · P = yük (bayt)", 15, MUTED, BOLD).next_to(p, DOWN, buff=0.12)
        x0 = 0.6
        fx = strip([H_(1.2, "başlık 8 B"), P_(3.0, "SDU / parça · L bayt"), PAD_(1.4, "dolgu")], x0, 1.4, 0.6, 16)
        fxb = brace_lbl(VGroup(fx[1], fx[2]), "yük P", SAC, UP, 16)
        f93 = T("Şekil 9-3: dolgu 0 … 7 bayt", 15, MUTED, BOLD).next_to(fx, DOWN, buff=0.12).align_to(fx, LEFT)
        pads = VGroup(*[VGroup(Rectangle(width=0.8, height=0.55, stroke_color=PADC, stroke_width=2, fill_color=PADC, fill_opacity=0.3), HX("55", 20, TXT, BOLD)) for _ in range(3)])
        for q in pads:
            q[1].move_to(q[0])
        pads.arrange(RIGHT, buff=0).move_to([3.2, -0.45, 0])
        pl = T("0x", 18, MUTED, BOLD).next_to(pads, LEFT, buff=0.15)
        bits = bitcells("01010101", 4.0, 0.42, PADC).move_to([3.2, -1.45, 0])
        bl = VGroup(*[T(b, 15, TXT, BOLD).move_to(c) for b, c in zip("01010101", bits)])
        bt = T("0x55 = 0101 0101 · sıfır ve bir dönüşümlü", 17, PADC, BOLD).next_to(bits, DOWN, buff=0.15)
        zl = zoom_lines(fx[2], pads, PADC)
        rx = VGroup(tag("alıcı", MUTED, 16), T("dolguyu atar → yalnızca L bayt teslim", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([-3.35, -2.55, 0])
        self.play(self.set_src("G.989.3 §9.1.3 · formül (9-1) · Şekil 9-3"), run_time=0.3)
        self.at(self.cue("Yükün boyunu bir formül", 0.3))
        self.play(FadeIn(p), FadeIn(lp), run_time=0.5)
        for k, (key, d) in enumerate((("Uzunluk sekiz ya da daha", 2.5), ("Bir ile yedi arasındaysa", 9.7), ("Sıfırsa yük de sıfırdır", 13.3))):
            self.at(self.cue(key, d))
            self.play(FadeIn(frm[k], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("Dolgu yükün sonuna", 15.3))
        self.play(FadeIn(fx, shift=RIGHT * 0.08), FadeIn(fxb), FadeIn(f93), run_time=0.6)
        self.at(self.cue("beş beş yazar", 17.6))
        self.play(Create(zl), FadeIn(pads), FadeIn(pl), run_time=0.6)
        self.at(self.cue("sıfırlar ve birler dönüşümlü", 22.7))
        self.play(FadeIn(bits), FadeIn(bl), FadeIn(bt), run_time=0.5)
        self.at(self.cue("Alıcı dolguyu atar", 25.1))
        self.play(FadeIn(rx, shift=UP * 0.08), fx[2].animate.set_opacity(0.25), run_time=0.5)
        self.end(pad=0.05)

        # b9 — worked examples (derived): 64 → 72, 1518 → 1528, min 16, max 16 392; 4–7 B padding only for L ≤ 4
        self.beat("b9")
        self.clear()
        h = self.show_heading("Örnekler — L → P → XGEM çerçevesi")
        rows = [["64 · Ethernet", "64", "0", "72"], ["1518 · Ethernet", "1520", "2", "1528"],
                ["1 … 7", "8", "7 … 1", "16 · en küçük dolu"], ["16 383 · en büyük PLI", "16 384", "1", "16 392 · en büyük"]]
        tb = mtable(["SDU L (B)", "yük P (B)", "dolgu (B)", "XGEM çerçevesi (B)"], rows, [3.4, 2.1, 1.9, 3.6], size=19, hsize=16, row_h=0.5, mono=(1, 2, 3)).move_to([0, 0.75, 0])
        hk = tag("hesap · (9-1)", GOLD, 15).next_to(tb, UP, buff=0.12).align_to(tb, RIGHT)
        for r in tb[1:]:
            r[4].set_color(GOLD)
        base = -2.85
        uh = 0.19
        bars = VGroup()
        lab = VGroup()
        for L in range(1, 17):
            pd = pay(L) - L
            x = -5.0 + (L - 1) * 0.48
            c = PADC if 1 <= L <= 4 else MUTED
            b = Rectangle(width=0.36, height=max(pd * uh, 0.02), stroke_width=0, fill_color=c, fill_opacity=0.85 if pd else 0.4).move_to([x, base + max(pd * uh, 0.02) / 2, 0])
            bars.add(b)
            if L in (1, 4, 8, 12, 16):
                lab.add(T(str(L), 15, MUTED, BOLD).next_to([x, base, 0], DOWN, buff=0.08))
        bax = Line([-5.35, base, 0], [2.55, base, 0], color=MUTED, stroke_width=1.5)
        byl = T("dolgu (B)", 15, MUTED, BOLD).next_to(bax, LEFT, buff=0.2).shift(UP * 0.5)
        bxl = T("L", 15, MUTED, BOLD).next_to(bax, RIGHT, buff=0.15)
        bnote = VGroup(T("L ≤ 4 → 4 … 7 B dolgu", 18, PADC, BOLD), T("L ≥ 8 → 0 … 3 B dolgu", 18, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.8, -2.3, 0])
        self.play(self.set_src("G.989.3 (9-1) · Şekil 9-5 · değerler: hesap"), run_time=0.3)
        self.at(self.cue("bizim hesabımızla", 0.8))
        self.play(FadeIn(tb[0]), FadeIn(hk), run_time=0.5)
        self.at(self.cue("Altmış dört baytlık bir Ethernet", 2.3))
        self.play(FadeIn(tb[1][:3], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("yetmiş iki baytlık bir XGEM", 6.7))
        self.play(FadeIn(tb[1][3:], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("bin beş yüz on sekiz bayt", 10.3))
        self.play(FadeIn(tb[2][:2], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("iki bayt dolguyla", 12.5))
        self.play(FadeIn(tb[2][2:4], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("bin beş yüz yirmi sekiz", 14.0))
        self.play(FadeIn(tb[2][4], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("En küçük dolu XGEM", 16.1))
        self.play(FadeIn(tb[3], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("en büyüğü on altı bin", 19.2))
        self.play(FadeIn(tb[4], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("Dört ile yedi baytlık dolgu", 23.2))
        self.play(Create(bax), FadeIn(byl), FadeIn(bxl), FadeIn(lab), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=1.0)
        self.at(self.cue("yalnızca dört bayt ya da daha kısa", 25.6))
        self.play(FadeIn(bnote, shift=LEFT * 0.08), Indicate(bars[:4], color=PADC, scale_factor=1.1), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep13_p1B")


class E13P1C(Act13):
    HDR, MANIFEST, PREV_BADGE = H13[1], M13("p1"), "std"

    def construct(self):
        # b10 — idle XGEM frames: when, identity (Port-ID 0xFFFF), KI 00, LF 1, receiver ignores
        self.beat("b10")
        h = self.show_heading("Boş (idle) XGEM çerçeveleri")
        why = VGroup(legend_row("1", GOLD, "gönderecek birim yok (planlayıcı izin vermese de)", 18),
                     legend_row("2", GOLD, "sıradaki birim sığmıyor ve bölmek §9.3'ü çiğner", 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        why.move_to([-6.3, 1.55, 0], aligned_edge=LEFT)
        x0, y = -6.2, -0.05
        filled = strip([H_(), P_(2.4, "SDU"), H_(), P_(1.6, "SDU")], x0, y, 0.55, 15)
        rest_x = filled.get_right()[0]
        rest = seg(rest_x, 6.2 - rest_x, y, MUTED, "kalan alan", 0.55, 0.05, 15, dashed=True)
        idle = strip([IH_(), IP_(2.6), IH_(), IP_(3.08)], rest_x, y, 0.55, 15)
        sl = T("FS yük bölümü", 15, MUTED, BOLD).next_to(filled, UP, buff=0.08).align_to(filled, LEFT)
        hd = xhdr(12.4, 0.62, 18, 14).move_to([0, -1.75, 0])
        hv = [("4'ün katı", PLIC), ("00", KIC), ("0xFFFF = 65 535", PIDC), ("0", OPTC), ("1", LFC), ("", HECC)]
        vals = VGroup()
        for (s, c), cell in zip(hv, hd):
            vals.add(HX(s, 17, c, BOLD).move_to(cell[0]) if s and s[0] in "0x1" else (T(s, 17, c, BOLD).move_to(cell[0]) if s else VGroup()))
        hdl = T("boş çerçeve başlığı", 15, IDC, BOLD).next_to(hd, UP, buff=0.12).align_to(hd, LEFT)
        ign = VGroup(*[xmark(m, MUTED, 3, 0.04) for m in (hd[1][0], hd[4][0])])
        ign_l = T("alıcı yok sayar: KI · LF · yük", 17, MUTED, BOLD).move_to([3.0, -2.85, 0])
        pid_g = glow(hd[2][0], PIDC, 0.05)
        self.play(self.set_src("G.989.3 §9.1.4 · Tablo 6-6"), FadeIn(sl), FadeIn(filled), FadeIn(rest), run_time=0.6)
        self.at(self.cue("Vericinin gönderecek birimi", 1.8))
        self.play(FadeIn(why[0], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("ya da sıradaki birim kalan", 4.6))
        self.play(FadeIn(why[1], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("verici yükün kalanını boş", 11.2))
        self.play(FadeOut(rest), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in idle], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("Boş çerçeve,", 15.2))
        self.play(FadeIn(hdl), FadeIn(hd), run_time=0.5)
        self.at(self.cue("port kimliği altmış beş bin", 16.2))
        self.play(FadeOut(hd[2][1]), FadeIn(vals[2], scale=0.9), Create(pid_g), FadeOut(hd[0][1]), FadeIn(vals[0]), run_time=0.6)
        self.at(self.cue("Şifresiz gider", 22.3))
        self.play(FadeOut(hd[1][1]), FadeIn(vals[1], scale=0.9), FadeOut(hd[3][1]), FadeIn(vals[3]), run_time=0.4)
        self.at(self.cue("son parça biti birdir", 23.5))
        self.play(FadeOut(hd[4][1]), FadeIn(vals[4], scale=0.9), run_time=0.4)
        self.at(self.cue("alıcı onun indeksini", 25.4))
        self.play(Create(ign), FadeIn(ign_l, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("son parça bitini ve yükünü", 27.1))
        self.play(idle[1].animate.set_opacity(0.25), idle[3].animate.set_opacity(0.25), run_time=0.5)
        self.end(pad=0.05)

        # b11 — idle PLI = actual size (0, 4, 8 …); PLI 4 → 12-byte frame (formula would give 16); check Port-ID first
        self.beat("b11")
        self.clear()
        h = self.show_heading("Boş çerçevede PLI formüle uymaz", h)
        r1 = VGroup(tag("dolu çerçeve", SAC, 17), eqline(("P =", TXT), ("(9-1)", PLIC), size=20)).arrange(RIGHT, buff=0.25)
        r2 = VGroup(tag("boş · 0xFFFF", IDC, 17), eqline(("P = PLI", TXT), ("· 4'ün herhangi bir katı, 0 ve 4 dahil", MUTED), size=20)).arrange(RIGHT, buff=0.25)
        rr = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-6.3, 1.6, 0], aligned_edge=LEFT)
        sz = VGroup()
        for n, s in ((0, "8 B"), (1, "12 B"), (2, "16 B")):
            st_ = words([("H", IDC, 0.55), ("", IDC, 0.55)] + [("", IDC, 0.12)] * n, 0.38, 0.38, 14)
            sz.add(VGroup(st_, T(s, 16, IDC, BOLD)).arrange(DOWN, buff=0.08))
        sz.add(T("…", 22, MUTED, BOLD))
        sz.arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to([4.3, 1.55, 0])
        y = -0.35
        wk = [("H", IDC, 0.55), ("", IDC, 0.55), ("4 B", IDC, 0.12), ("H", SAC, 0.55), ("", SAC, 0.55), ("", SAC, 0.14), ("", SAC, 0.14), ("", SAC, 0.14), ("", SAC, 0.14)]
        wr = words(wk, 0.8, 0.55, 15).move_to([-0.6, y, 0])
        wl = VGroup(T("boş · PLI = 4", 17, IDC, BOLD).next_to(wr, LEFT, buff=0.3), T("sonraki başlık →", 15, SAC, BOLD).next_to(wr, RIGHT, buff=0.2))
        ok = hop(wr[0].get_left()[0], wr[3].get_left()[0], y + 0.3, GOOD, 3, -1.0, 0.16)
        okl = T("+12 B ✓", 18, GOOD, BOLD).next_to(ok, UP, buff=0.04)
        bad = hop(wr[0].get_left()[0], wr[4].get_left()[0], y - 0.3, WARN, 3, 1.0, 0.16)
        badl = T("(9-1) uygulanırsa +16 B ✗ — başlığın ortası", 17, WARN, BOLD).next_to(bad, DOWN, buff=0.06)
        dec = VGroup(tile("Port-ID = 0xFFFF ?", PIDC, 2.7, 0.55, 17, 0.15))
        yes = tile("P = PLI", IDC, 1.7, 0.5, 17, 0.2)
        no = tile("P = (9-1)", SAC, 1.7, 0.5, 17, 0.2)
        VGroup(yes, no).arrange(DOWN, buff=0.25).next_to(dec, RIGHT, buff=1.0)
        da = VGroup(arrow(dec.get_right(), yes.get_left(), GOOD, 2.2, 0.12), arrow(dec.get_right(), no.get_left(), MUTED, 2.2, 0.12))
        dl = VGroup(T("evet", 15, GOOD, BOLD).next_to(da[0], UP, buff=0.02), T("hayır", 15, MUTED, BOLD).next_to(da[1], DOWN, buff=0.02))
        dgrp = VGroup(dec, yes, no, da, dl).move_to([-3.0, -2.62, 0])
        dfirst = T("önce Port-ID, sonra yük boyu", 16, PIDC, BOLD).next_to(dgrp, UP, buff=0.12).align_to(dgrp, LEFT)
        cid = card("Boş yükün içeriği", "verici seçer — hat deseni ve\nardışık özdeş rakamlar (CID) gözetilerek", None, IDC, w=5.0, h=1.45, tsize=19, bsize=16).move_to([3.7, -2.55, 0])
        self.play(self.set_src("G.989.3 §9.1.3 · §9.1.4 · 12 B / 16 B: hesap"), run_time=0.3)
        self.at(self.cue("Boş çerçevenin göstergesi formüle", 0.3))
        self.play(FadeIn(r1, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("yükün gerçek boyunu taşır", 3.4))
        self.play(FadeIn(r2, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("sıfır ve dört de dahil", 8.7))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in sz], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("Göstergesi dört olan bir boş", 10.6))
        self.play(FadeIn(wr), FadeIn(wl), run_time=0.5)
        self.play(Create(ok), FadeIn(okl), run_time=0.6)
        self.at(self.cue("formül on altı derdi", 15.0))
        self.play(Create(bad), FadeIn(badl, shift=LEFT * 0.08), run_time=0.6)
        self.at(self.cue("yük boyunu hesaplamadan önce", 17.7))
        self.play(FadeIn(dfirst), FadeIn(dec), GrowArrow(da[0]), GrowArrow(da[1]), FadeIn(yes), FadeIn(no), FadeIn(dl), run_time=0.8)
        self.at(self.cue("Boş yükün içeriğini verici", 22.4))
        self.play(FadeIn(cid[0]), FadeIn(cid[1]), run_time=0.5)
        self.at(self.cue("ama hat desenini", 25.1))
        self.play(FadeIn(cid[2:], shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # b12 — short idle: 4 zero bytes, upstream only; the OLT avoids it because XG-PON reads the BIP as one
        self.beat("b12")
        self.clear()
        self.set_badge("neden")
        h = self.show_heading("Kısa boş çerçeve — yalnızca ↑", h)
        lx, sx = -6.3, -2.9

        def row(y, lab, color, parts):
            ll = T(lab, 17, color, BOLD).move_to([lx, y, 0], aligned_edge=LEFT)
            fit(ll, 3.3)
            ll.move_to([lx, y, 0], aligned_edge=LEFT)
            s = strip([P_(0.6, "…"), H_(), P_(2.6, "SDU")] + parts, sx, y, 0.55, 15)
            return VGroup(ll, s)
        r_us = row(1.6, "↑ ONU · tahsis sonu", ONUC, [(0.95, "4 × 00", PADC, 0.5)])
        r_ds = row(0.35, "↓ G.989.3 OLT", OLTC, [FS_(0.95, "BIP 4 B", BIPC)])
        r_xg = row(-0.9, "XG-PON ONU'nun gözüyle", MUTED, [(0.95, "kısa boş", PADC, 0.25)])
        r_if = row(-2.3, "OLT kısa boş ekleseydi", WARN, [(0.95, "4 × 00", PADC, 0.5), FS_(0.95, "BIP 4 B", BIPC)])
        t_us = tag("4 B kaldı → kısa boş", PADC, 16).next_to(r_us[1], RIGHT, buff=0.3)
        t_ds = tag("OLT kısa boş üretmez", OLTC, 16).next_to(r_ds[1], RIGHT, buff=0.3)
        t_xg = VGroup(tag("BIP = kısa boş sanılır", MUTED, 16), ok_x(True, 20)).arrange(RIGHT, buff=0.15).next_to(r_xg[1], RIGHT, buff=0.3)
        ip = interp("yorum", GOLD, 15).next_to(r_if[0], UP, buff=0.12).align_to(r_if[0], LEFT)
        b8 = brace_lbl(VGroup(r_if[1][3], r_if[1][4]), "8 artık bayt", WARN, DOWN, 16)
        t_if = VGroup(tag("başlık gibi çözülür", WARN, 16), ok_x(False, 20)).arrange(RIGHT, buff=0.15).next_to(r_if[1], RIGHT, buff=0.3)
        za = DashedLine(r_ds[1][3].get_bottom(), r_xg[1][3].get_top(), color=MUTED, stroke_width=1.5, dash_length=0.06)
        self.play(self.set_src("G.989.3 §9.1.4 · §9.3 · 8 bayt senaryosu: yorum"), run_time=0.3)
        self.at(self.cue("yük bölümünün sonunda tam dört", 1.3))
        self.play(FadeIn(r_us[0]), FadeIn(r_us[1][:3]), run_time=0.5)
        self.at(self.cue("dört sıfır bayttan oluşan", 4.9))
        self.play(FadeIn(r_us[1][3], shift=LEFT * 0.08), run_time=0.5)
        self.at(self.cue("ama yalnızca yukarı yönde", 10.1))
        self.play(FadeIn(t_us, shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("OLT bundan kaçınır", 12.2))
        self.play(FadeIn(r_ds), FadeIn(t_ds, shift=LEFT * 0.08), run_time=0.6)
        self.at(self.cue("çünkü XG-PON'un TC katmanı", 13.8))
        self.play(Create(za), FadeIn(r_xg), run_time=0.6)
        self.play(FadeIn(t_xg, shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("Bizim yorumumuz", 21.9))
        self.play(FadeIn(ip), run_time=0.3)
        self.at(self.cue("OLT bir de kendi kısa", 23.3))
        self.play(FadeIn(r_if), run_time=0.6)
        self.at(self.cue("sekiz artık bayt görür", 27.3))
        self.play(FadeIn(b8), run_time=0.5)
        self.at(self.cue("bir başlık gibi çözmeye", 30.4))
        self.play(FadeIn(t_if, shift=LEFT * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # b13 — engineer note
        self.note11("b13", [("1", "PLI yükün boyu değildir — boş çerçeveler formülü bozar",
                             "(9-1)'i PLI = 4'lük boş çerçeveye uygulayan çözücü 16 B atlar → sınırlama kaybolur.", "gösterge yükün boyu değildir"),
                            ("2", "16 sihirli sayıdır",
                             "En küçük dolu çerçeve 16 B · 16 B'tan küçük artık → boş çerçeve\n8 B'tan kısa son parça → 8'e doldurulur.", "on altı sihirli sayıdır")])
        self.bridge_beat("b14", "Çerçeve belli.\nPeki alıcı bu çerçevelerin sınırlarını nasıl bulur?")
        self.save_timeline("ep13_p1C")


# ================================ PERDE 2 ======================================
RULES = ["her ↓ ve ↑ yük bölümü bir XGEM başlığıyla başlar",
         "PLI → yük boyu → bir sonraki başlığın yeri; bölüm sonuna kadar",
         "doğrulama: bir sonraki çerçevenin başlığında HEC",
         "HEC ✗ → o anki çerçeve + yük bölümünün kalanı atılır"]


class E13P2A(Act13):
    HDR, MANIFEST, FIRST = H13[2], M13("p2"), True

    def construct(self):
        # c1 — §9.2 sentences 1–2: header at every section start, PLI chain
        self.beat("c1")
        tc = self.title_card("PERDE 2", "Sınırlama")
        self.at(self.cue("Standardın kuralı dört", 1.7))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("§9.2 — dört cümle")
        rl = num_rows([(str(i + 1), GOLD, s) for i, s in enumerate(RULES)], size=19, gap=0.5)
        rl.move_to([-6.3, 1.1, 0], aligned_edge=LEFT)
        y = -1.35
        x0 = -6.2
        parts = [FS_(1.15, "FS başlığı")]
        pw = [1.6, 2.2, 1.0, 1.9, 1.55]
        for w in pw:
            parts += [H_(0.38), P_(w)]
        parts.append(FS_(0.6, "BIP", BIPC))
        st = strip(parts, x0, y, 0.55, 15)
        hdrs = [st[1 + 2 * i] for i in range(5)]
        sl = brace_lbl(VGroup(*st[1:-1]), "FS yük bölümü", PAYC, DOWN, 16)
        anc = VGroup(Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI).next_to(hdrs[0], UP, buff=0.06))
        anc.add(T("başlangıç: başlık", 15, GOLD, BOLD).next_to(anc[0], UP, buff=0.06))
        hops = VGroup(*[hop(hdrs[i].get_x(), hdrs[i + 1].get_x(), y + 0.3, GOLD, 2.5, -0.9, 0.13) for i in range(4)])
        hl = T("PLI → 8 + P", 15, GOLD, BOLD).next_to(hops[0], UP, buff=0.04)
        self.play(self.set_src("G.989.3 §9.2"), FadeIn(st), FadeIn(sl), run_time=0.6)
        self.at(self.cue("her aşağı ve yukarı yön yük", 5.6))
        self.play(FadeIn(rl[0], shift=RIGHT * 0.08), FadeIn(anc, shift=DOWN * 0.08), Indicate(hdrs[0], color=GOLD, scale_factor=1.3), run_time=0.7)
        self.at(self.cue("alıcı ilk başlığın yerini", 13.2))
        self.play(FadeIn(rl[1], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("göstergeyi okuyup", 16.5))
        self.play(FadeOut(anc[1]), Create(hops[0]), FadeIn(hl), run_time=0.7)
        self.at(self.cue("ve bunu bölümün sonuna", 22.3))
        self.play(LaggedStart(*[Create(hh) for hh in hops[1:]], lag_ratio=0.3), run_time=1.0)
        self.end(pad=0.05)

        # c2 — sentences 3–4: HEC of the next header verifies; failure → current frame + rest discarded
        self.beat("c2")
        oks = VGroup(*[ok_x(True, 18).next_to(hdrs[i], DOWN, buff=0.08) for i in range(1, 3)])
        bad = xmark(hdrs[3][0], WARN, 4)
        cur = VGroup(hdrs[2], st[6])
        red = Rectangle(width=st[-2].get_right()[0] - hdrs[2].get_left()[0], height=0.7, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.18)
        red.move_to([(hdrs[2].get_left()[0] + st[-2].get_right()[0]) / 2, y, 0])
        b1 = brace_lbl(cur, "o anki çerçeve", WARN, UP, 15)
        b2 = brace_lbl(VGroup(*st[7:-1]), "bölümün kalanı", WARN, UP, 15)
        self.play(FadeOut(sl), run_time=0.3)
        self.at(self.cue("alıcı bir çerçevenin doğru", 0.2))
        self.play(FadeIn(rl[2], shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("bir sonraki çerçevenin başlığında", 3.8))
        self.play(LaggedStart(*[FadeIn(o, scale=0.8) for o in oks], lag_ratio=0.4), run_time=0.8)
        self.at(self.cue("varsayılan başlığın HEC", 9.8))
        self.play(FadeIn(rl[3], shift=RIGHT * 0.08), Create(bad), run_time=0.6)
        self.at(self.cue("alıcı o anki XGEM", 14.3))
        self.play(FadeOut(hops[2:]), FadeOut(hl), FadeIn(b1), run_time=0.5)
        self.at(self.cue("yük bölümünün kalanıyla", 16.8))
        self.play(FadeIn(red), FadeIn(b2), run_time=0.6)
        self.end(pad=0.05)

        # c3 — no hunt machine; anchored delineation restarts at every payload section
        self.beat("c3")
        self.clear()
        self.set_badge("neden")
        h = self.show_heading("Arama yok — sınırlama demirli", h)
        sm = VGroup(*[tile(s, STATE, 1.6, 0.48, 16, 0.18) for s in ("Av", "Ön senkron", "Senkron", "Yen. senkron")]).arrange(RIGHT, buff=0.35).move_to([-2.3, 1.55, 0])
        sma = VGroup(*[arrow(sm[i].get_right(), sm[i + 1].get_left(), MUTED, 2, 0.1) for i in range(3)])
        smc = s2chip(2, 16).next_to(sm, RIGHT, buff=0.35)
        smx = xmark(VGroup(sm, sma), WARN, 4, 0.06)
        no = T("XGEM'de böyle bir makine yok · başlık hiç aranmaz", 18, WARN, BOLD).next_to(sm, DOWN, buff=0.25).align_to(sm, LEFT)
        dem = VGroup(interp("yorum", GOLD, 15), pill("demirli: her yük bölümünün başında yeniden başlar", GOLD, 19)).arrange(RIGHT, buff=0.25).move_to([0, 0.25, 0])
        yd = -0.95
        x0 = -5.6
        fw = 3.9
        dsr = VGroup()
        for i in range(3):
            dsr.add(strip([FS_(0.7, "FS b."), (fw - 0.75, "yük", PAYC, 0.14)], x0 + i * fw, yd, 0.5, 14))
        dl = T("↓", 22, OLTC, BOLD).next_to(dsr, LEFT, buff=0.2)
        tks = VGroup(*[T(s, 14, MUTED, BOLD).move_to([x0 + i * fw, yd - 0.45, 0]) for i, s in enumerate(("0", "125 µs", "250 µs", "375 µs"))])
        tks[0].shift(RIGHT * 0.08)
        tks[3].shift(LEFT * 0.3)

        def anchor(x, y):
            return Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(0.1).rotate(PI).move_to([x, y + 0.38, 0])
        dan = VGroup(*[anchor(r[1].get_left()[0] + 0.12, yd) for r in dsr])
        yu = -2.35
        ur = VGroup()
        bx = [-5.6, -2.2, 1.6]
        for k, bx0 in enumerate(bx):
            ur.add(strip([(0.45, "", PHC, 0.3), FS_(0.35, ""), (1.15, "tahsis", PAYC, 0.14), (1.0, "tahsis", PAYC, 0.24)], bx0, yu, 0.5, 14))
        ul = T("↑", 22, ONUC, BOLD).next_to(ur, LEFT, buff=0.2).set_y(yu)
        uan = VGroup(*[anchor(r[i].get_left()[0] + 0.12, yu) for r in ur for i in (2, 3)])
        ull = T("her tahsisin kendi yük bölümü", 15, ONUC, BOLD).next_to(ur, DOWN, buff=0.12).align_to(ur, RIGHT)
        self.play(self.set_src("G.989.3 §9.2 · §9.1.1 · S2·B2 Şekil 10-4 · 'demirli': yorum"), run_time=0.3)
        self.at(self.cue("Geçen bölümdeki senkron", 0.3))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in sm], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in sma], lag_ratio=0.2), FadeIn(smc), run_time=1.2)
        self.at(self.cue("XGEM'de böyle bir makine", 7.4))
        self.play(Create(smx), run_time=0.5)
        self.at(self.cue("sınırlama hiçbir zaman", 10.1))
        self.play(FadeIn(no, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("sınırlama demirlidir", 14.6))
        self.play(FadeIn(dem, shift=UP * 0.08), run_time=0.6)
        self.at(self.cue("aşağı yönde her yüz yirmi beş", 19.8))
        self.play(FadeIn(dl), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.08) for r in dsr], lag_ratio=0.2), FadeIn(tks), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.08) for a in dan], lag_ratio=0.2), run_time=0.6)
        self.at(self.cue("yukarı yönde her tahsiste", 23.5))
        self.play(FadeIn(ul), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.08) for r in ur], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("çünkü her tahsisin kendi", 25.7))
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.08) for a in uan], lag_ratio=0.1), FadeIn(ull), run_time=0.8)
        self.end(pad=0.05)

        # c4 — what "fails" means (Table A.4); why the current frame goes too
        self.beat("c4")
        self.clear()
        h = self.show_heading("“Başarısız” ne demek?", h)
        rows = [["1 bit", "düzeltilir", "yok"], ["2 bit", "düzeltilir", "yok"], ["3 bit · eşlik ✗", "düzeltilemez", "bölümün kalanı"], ["tanımsız sendrom", "düzeltilemez", "bölümün kalanı"]]
        tb = mtable(["başlıktaki hata", "HEC sonucu (Ek A)", "kayıp"], rows, [3.4, 3.2, 3.0], size=19, hsize=16, row_h=0.5).move_to([-1.3, 1.1, 0])
        for i in (1, 2):
            tb[i][2].set_color(GOOD)
            tb[i][3].set_color(GOOD)
        for i in (3, 4):
            tb[i][2].set_color(WARN)
            tb[i][3].set_color(WARN)
        ip = interp("okuma: yorum · Ek A Tablo A.4", GOLD, 15).next_to(tb, RIGHT, buff=0.3).align_to(tb, UP)
        y = -1.9
        x0 = -6.0
        st = strip([H_(0.55, "H k"), P_(3.0, "çerçeve k"), H_(0.65, "H k+1"), P_(4.2, "…")], x0, y, 0.6, 15)
        okk = VGroup(ok_x(True, 18), T("sağlam", 15, GOOD, BOLD)).arrange(RIGHT, buff=0.08).next_to(st[0], DOWN, buff=0.1)
        bx = xmark(st[2][0], WARN, 4)
        pa = hop(st[0].get_x(), st[2].get_x(), y + 0.33, GOLD, 2.5, -0.8, 0.14)
        pl = T("PLI k = ?", 16, GOLD, BOLD).next_to(pa, UP, buff=0.04)
        red = Rectangle(width=st.get_right()[0] - x0, height=0.72, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.15).move_to([(x0 + st.get_right()[0]) / 2, y, 0])
        why = VGroup(T("bozuk sonraki başlık", 17, WARN, BOLD), T("= PLI k yanlış olabilir", 17, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(st, RIGHT, buff=0.3)
        self.play(self.set_src("G.989.3 §9.2 · Ek A Tablo A.4 · okuma: yorum"), run_time=0.3)
        self.at(self.cue("A ekinin tablosuna", 3.4))
        self.play(FadeIn(tb[0]), FadeIn(ip), run_time=0.5)
        self.at(self.cue("eşlik hatalı üç bit", 7.6))
        self.play(FadeIn(tb[3], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("ya da tanımsız bir sendrom", 9.3))
        self.play(FadeIn(tb[4], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("Bir ve iki bitlik hatalar", 11.6))
        self.play(FadeIn(tb[1][:3], shift=UP * 0.06), FadeIn(tb[2][:3], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("ve hiçbir şey kaybolmaz", 14.7))
        self.play(FadeIn(tb[1][3]), FadeIn(tb[2][3]), run_time=0.4)
        self.at(self.cue("Kuralın ilginç yanı", 16.7))
        self.play(FadeIn(st), run_time=0.5)
        self.at(self.cue("o anki çerçeveyi de atmasıdır", 18.4))
        self.play(FadeIn(red), run_time=0.5)
        self.at(self.cue("oysa onun kendi başlığı", 20.9))
        self.play(FadeIn(okk, shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("bozuk bir sonraki başlık", 24.6))
        self.play(Create(bx), Create(pa), FadeIn(pl), run_time=0.6)
        self.at(self.cue("o anki göstergenin yanlış", 26.8))
        self.play(FadeIn(why, shift=LEFT * 0.08), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep13_p2A")


class E13P2B(Act13):
    HDR, MANIFEST, PREV_BADGE = H13[2], M13("p2"), "neden"

    def construct(self):
        # c5 — what the text does not say: end-of-section check, recognising the short idle
        self.beat("c5")
        self.set_badge("std")
        h = self.show_heading("Metnin söylemedikleri")
        x0 = -5.6
        y = 1.25
        st = strip([P_(0.6, "…"), H_(), P_(2.4), H_(), P_(3.2, "son çerçeve")], x0, y, 0.55, 15)
        end_x = st.get_right()[0]
        eln = DashedLine([end_x, y - 0.55, 0], [end_x, y + 0.55, 0], color=MUTED, stroke_width=2)
        q = VGroup(T("?", 30, WARN, BOLD), T("ardında başlık yok", 16, WARN, BOLD)).arrange(DOWN, buff=0.04).next_to(eln, RIGHT, buff=0.25)
        ca = VGroup(tag("A", GOOD, 16), strip([H_(), P_(3.6, "son çerçeve")], 0, 0, 0.5, 15), T("| bölüm sonu", 17, MUTED, BOLD), ok_x(True, 20))
        cb = VGroup(tag("B", GOOD, 16), strip([H_(), P_(2.66, "son çerçeve"), (0.94, "4 × 00", PADC, 0.5)], 0, 0, 0.5, 15), T("| bölüm sonu · kısa boş", 17, MUTED, BOLD), ok_x(True, 20))
        for c in (ca, cb):
            c.arrange(RIGHT, buff=0.25)
        cases = VGroup(ca, cb).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-0.6, -0.55, 0])
        nt = VGroup(VGroup(tag("bu denetim", WARN, 16), T("metinde yazılı değil", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2),
                    VGroup(tag("kısa boşu tanıma kuralı", WARN, 16), T("metinde yok", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        nt.move_to([-1.2, -2.45, 0])
        ip = interp("çıkarım", GOLD, 16).next_to(nt, RIGHT, buff=0.5)
        self.play(self.set_src("G.989.3 §9.2 · §9.1.4 · çıkarım"), run_time=0.3)
        self.at(self.cue("Bir bölümün son çerçevesinin", 2.4))
        self.play(FadeIn(st), Create(eln), run_time=0.6)
        self.play(FadeIn(q, shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("sonu yükün sonuyla", 6.7))
        self.play(FadeIn(ca, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("ya da kısa boş çerçeve için", 8.3))
        self.play(FadeIn(cb, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("ama metin bu denetimi", 13.2))
        self.play(FadeIn(nt[0], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("alıcının kısa boş çerçeveyi", 15.6))
        self.play(FadeIn(nt[1], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("Bunlar bizim çıkarımlarımızdır", 19.8))
        self.play(FadeIn(ip, scale=0.9), run_time=0.4)
        self.end(pad=0.05)

        # c6 — cost of one event: rest of section (DS ≤ 155 488 B at 10G FEC off), rest of one allocation (US); recovery next section
        self.beat("c6")
        self.clear()
        self.set_badge("neden")
        h = self.show_heading("Bedel — tek olay, bölümün kalanı", h)
        y = 1.15
        f1 = strip([FS_(0.6, "FS b."), H_(0.32), P_(0.9), H_(0.32), P_(3.5, "…"), FS_(0.4, "", BIPC)], -6.2, y, 0.55, 14)
        f2 = strip([FS_(0.6, "FS b."), H_(0.32), P_(1.4), H_(0.32), P_(1.2), H_(0.32), P_(1.48), FS_(0.4, "", BIPC)], 0.1, y, 0.55, 14)
        fl = T("↓ 10G · FEC kapalı · her FS çerçevesi 125 µs", 15, MUTED, BOLD).next_to(f1, UP, buff=0.1).align_to(f1, LEFT)
        bad = xmark(f1[3][0], WARN, 4)
        red = Rectangle(width=f1[4].get_right()[0] - f1[1].get_left()[0], height=0.66, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.18)
        red.move_to([(f1[1].get_left()[0] + f1[4].get_right()[0]) / 2, y, 0])
        rec = SurroundingRectangle(VGroup(*f2[1:-1]), color=GOOD, buff=0.06, stroke_width=2.5)
        recl = T("kurtarma: bir sonraki yük bölümü ✓", 16, GOOD, BOLD).next_to(rec, DOWN, buff=0.1)
        nums = VGroup(eqline(("≤ 155 488 B", WARN), ("kayıp", MUTED), size=24), eqline(("≈ 102 ×", TXT), ("1518 B çerçeve", TXT), size=20)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        nums.next_to(f1, DOWN, buff=0.3).align_to(f1, LEFT)
        hk = tag("hesap · Tablo 8-1 (N = 0, P = 0)", GOLD, 15).next_to(nums, RIGHT, buff=0.3).align_to(nums, UP)
        yu = -1.75
        us = strip([(0.45, "", PHC, 0.3), FS_(0.4, "b."), (4.2, "", PAYC, 0.0), (3.3, "tahsis 2", PAYC, 0.14), FS_(0.4, "", BIPC)], -6.2, yu, 0.55, 14)
        a1 = strip([H_(0.32), P_(0.8), H_(0.32), P_(2.7, "…")], us[2].get_left()[0] + 0.03, yu, 0.47, 14)
        ul = T("↑ burst: tahsis 1 · tahsis 2", 15, MUTED, BOLD).next_to(us, UP, buff=0.1).align_to(us, LEFT)
        ubad = xmark(a1[2][0], WARN, 4)
        ured = Rectangle(width=a1[3].get_right()[0] - a1[0].get_left()[0], height=0.6, stroke_color=WARN, stroke_width=2.5, fill_color=WARN, fill_opacity=0.18)
        ured.move_to([(a1[0].get_left()[0] + a1[3].get_right()[0]) / 2, yu, 0])
        uok = ok_x(True, 20).next_to(us[3], UP, buff=0.08)
        unum = T("en çok bir tahsisin kalanı", 18, WARN, BOLD).next_to(us, RIGHT, buff=0.3)
        fit(unum, 6.6 - us.get_right()[0])
        self.play(self.set_src("G.989.3 §9.2 · §9.1.1 · Tablo 8-1 · değerler: hesap"), FadeIn(fl), FadeIn(f1), run_time=0.6)
        self.at(self.cue("Tek bir olay", 2.0))
        self.play(Create(bad), run_time=0.4)
        self.at(self.cue("bölümün bütün kalanına", 3.1))
        self.play(FadeIn(red), run_time=0.6)
        self.at(self.cue("bu yüz elli beş bin", 8.6))
        self.play(FadeIn(nums[0], shift=UP * 0.06), FadeIn(hk), run_time=0.5)
        self.at(self.cue("yaklaşık yüz iki tane", 13.4))
        self.play(FadeIn(nums[1], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("Yukarı yönde kayıp", 18.4))
        self.play(FadeIn(ul), FadeIn(us), FadeIn(a1), run_time=0.6)
        self.play(Create(ubad), FadeIn(ured), FadeIn(uok), run_time=0.5)
        self.at(self.cue("en çok bir tahsisin kalanıdır", 20.0))
        self.play(FadeIn(unum, shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("Kurtarma kendiliğindendir", 22.6))
        self.play(FadeIn(f2, shift=RIGHT * 0.08), run_time=0.5)
        self.at(self.cue("bir sonraki yük bölümünde", 24.8))
        self.play(Create(rec), FadeIn(recl), run_time=0.5)
        self.end(pad=0.05)

        # c7 — rare: header vs payload odds (independent errors)
        self.beat("c7")
        self.clear()
        h = self.show_heading("Ama olay çok seyrek", h)
        P = [("10⁻³", "4,0 × 10⁻⁵", "≈ 1", 4.0e-5, 1.0), ("10⁻⁴", "4,2 × 10⁻⁸", "0,70", 4.2e-8, 0.70), ("10⁻⁶", "4,2 × 10⁻¹⁴", "1,2 × 10⁻²", 4.2e-14, 1.2e-2)]
        tb = mtable(["BER", "P(başlık düzeltilemez)", "P(1518 B yük bozuk)"], [[a, b, c] for a, b, c, _, _ in P], [1.8, 4.2, 4.2], size=20, hsize=16, row_h=0.52)
        tb.move_to([-1.3, 1.25, 0])
        for r in tb[1:]:
            r[2].set_color(HECC)
            r[3].set_color(SAC)
        hk = tag("hesap · bağımsız hatalar", GOLD, 15).next_to(tb, RIGHT, buff=0.25).align_to(tb, UP)
        ax, X = log_axis(1e-15, 1.0, -4.6, 5.6, -2.35, [(1e-15, "10⁻¹⁵"), (1e-12, "10⁻¹²"), (1e-9, "10⁻⁹"), (1e-6, "10⁻⁶"), (1e-3, "10⁻³"), (1.0, "1")], size=15)
        ays = [-0.6, -1.15, -1.7]
        dots = VGroup()
        for (a, _, _, ph, pp), yy in zip(P, ays):
            lab = T(f"BER {a}", 15, MUTED, BOLD).move_to([-5.6, yy, 0])
            ln = Line([X(ph), yy, 0], [X(pp), yy, 0], color=MUTED, stroke_width=1.5)
            dh = Dot([X(ph), yy, 0], radius=0.09, color=HECC)
            dp = Dot([X(pp), yy, 0], radius=0.09, color=SAC)
            dots.add(VGroup(lab, ln, dh, dp))
        leg = VGroup(VGroup(Dot(radius=0.08, color=HECC), T("başlık", 15, HECC, BOLD)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(radius=0.08, color=SAC), T("1518 B yük", 15, SAC, BOLD)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.3)
        leg.next_to(ax, DOWN, buff=0.15).align_to(ax, RIGHT).shift(DOWN * 0.3)
        msg = pill("başlık, yükün bozulduğu yerde neredeyse hiç bozulmaz", GOOD, 19).move_to([-1.0, -3.05, 0])
        self.play(self.set_src("bağımsız bit hataları · Ek A Tablo A.4 · olasılıklar: hesap"), run_time=0.3)
        self.at(self.cue("Bağımsız hatalarla", 1.9))
        self.play(FadeIn(tb[0]), FadeIn(hk), FadeIn(ax), run_time=0.6)
        self.at(self.cue("on üzeri eksi dörtte bir başlığın", 3.5))
        self.play(FadeIn(tb[2][:3], shift=UP * 0.06), FadeIn(dots[1][:3]), run_time=0.5)
        self.at(self.cue("bin beş yüz on sekiz baytlık bir yükün", 12.0))
        self.play(FadeIn(tb[2][3], shift=UP * 0.06), FadeIn(dots[1][3]), FadeIn(leg), run_time=0.5)
        self.at(self.cue("On üzeri eksi altıda", 18.7))
        self.play(FadeIn(tb[3][:2], shift=UP * 0.06), FadeIn(dots[2][0]), run_time=0.4)
        self.at(self.cue("dört çarpı on üzeri eksi on dört", 21.4))
        self.play(FadeIn(tb[3][2:], shift=UP * 0.06), FadeIn(dots[2][1:]), run_time=0.5)
        self.at(self.cue("yükün bozulduğu yerde", 27.1))
        self.play(FadeIn(msg, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # c8 — PMD bridge: G.989.2 DS reference BER (S1·B5): 10⁻⁴ at 2.5G, 10⁻³ at 10G
        self.beat("c8")
        self.play(FadeOut(msg), FadeOut(hk), run_time=0.3)
        h, chp = self.pmd_head("PMD Köprüsü — referans BER", s1chip(5), h)
        t25 = tag("2,5G ↓ referans", R25, 15).next_to(tb[2], RIGHT, buff=0.2)
        t10 = tag("10G ↓ referans", R10, 15).next_to(tb[1], RIGHT, buff=0.2)
        hc = glow(tb[1][2], HECC, 0.04)
        pc = glow(tb[1][3], SAC, 0.04)
        fin = VGroup(VGroup(tag("HEC", HECC, 17), T("→ sınırlamayı kurtarır", 18, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                     VGroup(tag("FEC", PARC, 17), T("→ yükü kurtaran tek şey", 18, TXT, BOLD)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).move_to([-0.6, -3.05, 0])
        self.play(self.set_src("G.989.2 Tablo 11-4 / 11-5 · S1·B5 · olasılıklar: hesap"), run_time=0.3)
        self.at(self.cue("iki buçuk gigabitte on üzeri", 8.3))
        self.play(FadeIn(t25, shift=LEFT * 0.08), Indicate(tb[2][1], color=R25), run_time=0.5)
        self.at(self.cue("on gigabitte on üzeri eksi üç", 11.6))
        self.play(FadeIn(tb[1], shift=UP * 0.06), FadeIn(dots[0]), FadeIn(t10, shift=LEFT * 0.08), run_time=0.6)
        self.at(self.cue("On üzeri eksi üçte bile", 14.1))
        self.play(Create(hc), Indicate(dots[0][2], color=HECC, scale_factor=1.6), run_time=0.6)
        self.at(self.cue("ama bin beş yüz on sekiz baytlık bir yük", 21.0))
        self.play(Create(pc), Indicate(dots[0][3], color=SAC, scale_factor=1.6), run_time=0.6)
        self.at(self.cue("Sınırlamayı HEC kurtarır", 26.5))
        self.play(FadeIn(fin[0], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("yükü ise yalnızca FEC", 28.6))
        self.play(FadeIn(fin[1], shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.05)

        # c9 — no payload check in XGEM; the client (Ethernet FCS) catches it; line BER from FEC / BIP counters
        self.beat("c9")
        self.clear()
        self.set_badge("neden")
        h = self.show_heading("XGEM yükünün denetimi yok", h)
        y = 1.3
        fr = strip([(3.0, "başlık · HEC ✓", SAC, 0.55), (6.6, "yük", SAC, 0.14)], -6.2, y, 0.6, 16)
        noc = brace_lbl(fr[1], "yük için denetim alanı yok", WARN, DOWN, 17)
        flips = VGroup(*[T("✗", 18, WARN, BOLD).move_to([fr[1].get_left()[0] + d, y, 0]) for d in (0.9, 2.2, 4.6, 5.7)])
        yp = -0.75
        pp = VGroup(tile("XGEM alıcısı", SAC, 2.2, 0.6, 17, 0.15), tile("yük olduğu gibi teslim", MUTED, 3.2, 0.6, 17, 0.12),
                    tile("istemci: Ethernet MAC", R10, 3.0, 0.6, 17, 0.15), tile("FCS ✗ → atılır", WARN, 2.4, 0.6, 17, 0.15)).arrange(RIGHT, buff=0.42).move_to([0, yp, 0])
        pa = VGroup(*[arrow(pp[i].get_right(), pp[i + 1].get_left(), MUTED, 2.2, 0.12) for i in range(3)])
        ip = interp("yorum: istemci davranışı", GOLD, 15).next_to(pp, UP, buff=0.15).align_to(pp, RIGHT)
        ctr = VGroup(T("hat hata oranı:", 18, MUTED, BOLD), tag("FEC düzeltme sayaçları", PARC, 16), tag("BIP", BIPC, 16), s2chip(2, 16)).arrange(RIGHT, buff=0.25).move_to([0, -2.35, 0])
        self.play(self.set_src("G.989.3 §9 · Tablo 14-1 · istemci davranışı: yorum"), run_time=0.3)
        self.at(self.cue("Çünkü XGEM'in yük denetimi", 0.3))
        self.play(FadeIn(fr), run_time=0.5)
        self.play(FadeIn(noc), run_time=0.4)
        self.at(self.cue("Bozuk bir yük alıcıya", 2.9))
        self.play(LaggedStart(*[FadeIn(f, scale=0.7) for f in flips], lag_ratio=0.2), FadeIn(pp[0]), GrowArrow(pa[0]), FadeIn(pp[1]), run_time=0.8)
        self.at(self.cue("onu ancak istemci", 6.9))
        self.play(GrowArrow(pa[1]), FadeIn(pp[2]), run_time=0.5)
        self.at(self.cue("örneğin Ethernet'in çerçeve", 8.4))
        self.play(GrowArrow(pa[2]), FadeIn(pp[3]), run_time=0.5)
        self.at(self.cue("Bu bizim yorumumuz", 12.7))
        self.play(FadeIn(ip), run_time=0.3)
        self.at(self.cue("standartta yük için bir denetim", 14.3))
        self.play(Indicate(noc, color=WARN, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("Hat hata oranını", 18.6))
        self.play(FadeIn(ctr[0]), FadeIn(ctr[1], shift=UP * 0.06), FadeIn(ctr[2], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("geçen bölümün FEC ve BIP", 20.1))
        self.play(FadeIn(ctr[3], shift=LEFT * 0.08), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep13_p2B")


BYTEMAP = [(PLIC, 8, "PLI[13:6]"), ((PLIC, 6, KIC, 2), None, "PLI[5:0]\n‖ KI"), (PIDC, 8, "Port-ID\n[15:8]"), (PIDC, 8, "Port-ID\n[7:0]"),
           (OPTC, 8, "Options\n[17:10]"), (OPTC, 8, "Options\n[9:2]"), ((OPTC, 2, LFC, 1, HECC, 5), None, "Opt[1:0] ‖ LF\n‖ HEC[12:8]"),
           (HECC, 8, "HEC[7:0]\nson bit: eşlik")]


class E13P2C(Act13):
    HDR, MANIFEST, PREV_BADGE = H13[2], M13("p2"), "neden"

    def construct(self):
        # c10 — Table 14-1 counters
        self.beat("c10")
        self.set_badge("std")
        h = self.show_heading("Sayaçlar — Tablo 14-1")
        rows = [["XGEM başlık HEC hatası sayısı", "Z", "evet", "evet", "hayır"],
                ["HEC hatasıyla kaybedilen FS sözcükleri", "İ", "evet", "evet", "—"]]
        tb = mtable(["parametre", "Z / İ", "ONU · kanal başına", "OLT CT · ONU başına", "OLT CT"], rows, [4.9, 1.1, 2.3, 2.5, 1.4], size=18, hsize=15, row_h=0.55)
        tb.move_to([0, 1.55, 0])
        tb[1][2].set_color(GOLD)
        tb[2][2].set_color(MUTED)
        zl = T("Z = zorunlu · İ = isteğe bağlı", 15, MUTED, BOLD).next_to(tb, DOWN, buff=0.12).align_to(tb, RIGHT)
        qd = self.quote("Tablo 14-1 · tanım", "“Number of events involving loss of XGEM channel delineation.”",
                        "XGEM kanal sınırlaması kaybı olaylarının sayısı — çerçeve sayısı değil", width=11.6)
        qd.move_to([-0.3, -0.45, 0])
        nt = self.quote("Tablo 14-1 · ikinci sayacın notu", "“Note that the number of lost XGEM frames is not available.”",
                        "kaybedilen XGEM çerçevesi sayısı elde edilemez", width=11.6)
        nt.move_to([-0.3, -2.35, 0])
        for g in (qd, nt):
            g.align_to(tb, LEFT).shift(RIGHT * 0.3)
        self.play(self.set_src("G.989.3 Tablo 14-1"), FadeIn(tb[0]), run_time=0.5)
        self.at(self.cue("XGEM başlık HEC hatası sayacıdır", 4.7))
        self.play(FadeIn(tb[1][:3], shift=UP * 0.06), FadeIn(zl), run_time=0.5)
        self.at(self.cue("XGEM kanal sınırlaması kaybı", 9.5))
        self.play(FadeIn(qd[0]), FadeIn(qd[1]), FadeIn(qd[2], shift=UP * 0.06), run_time=0.7)
        self.at(self.cue("ONU'da her kanal için", 13.5))
        self.play(FadeIn(tb[1][3], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("OLT'de her ONU için", 15.4))
        self.play(FadeIn(tb[1][4:], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("İsteğe bağlı ikinci sayaç", 17.8))
        self.play(FadeIn(tb[2], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("Notu açıktır", 23.4))
        self.play(FadeIn(nt[0]), FadeIn(nt[1]), run_time=0.5)
        self.at(self.cue("kaybedilen XGEM çerçevesi sayısı", 24.6))
        self.play(FadeIn(nt[2], shift=UP * 0.06), run_time=0.5)
        self.end(pad=0.05)

        # c11 — byte map for analyzers (our derivation)
        self.beat("c11")
        self.clear()
        h = self.show_heading("Analizör için bayt haritası", h)
        hd = xhdr(12.4, 0.6, 18, 14).move_to([0, 1.7, 0])
        ub = 0.18
        gap = 0.12
        bw = 8 * ub
        x = -(8 * bw + 7 * gap) / 2
        yb = 0.15
        byts = VGroup()
        for k, (c, n, desc) in enumerate(BYTEMAP):
            parts = [(c, n)] if n else [(c[i], c[i + 1]) for i in range(0, len(c), 2)]
            g = VGroup()
            xx = x
            for cc, nn in parts:
                r = Rectangle(width=nn * ub, height=0.62, stroke_color=cc, stroke_width=2, fill_color=cc, fill_opacity=0.25).move_to([xx + nn * ub / 2, yb, 0])
                g.add(r)
                xx += nn * ub
            num = T(f"bayt {k + 1}", 15, TXT, BOLD).move_to([x + bw / 2, yb, 0])
            d = T(desc, 15, MUTED, BOLD, line_spacing=0.8).next_to([x + bw / 2, yb - 0.31, 0], DOWN, buff=0.12)
            fit(d, bw + 0.08)
            byts.add(VGroup(g, num, d))
            x += bw + gap
        bl = VGroup(*[DashedLine([hd.get_left()[0] + 12.4 / 8 * k, 1.4, 0], [byts[k][0].get_left()[0] if k < 8 else byts[7][0].get_right()[0], yb + 0.31, 0],
                                 color=MUTED, stroke_width=1.2, dash_length=0.06) for k in range(8)],
                    DashedLine([hd.get_right()[0], 1.4, 0], [byts[7][0].get_right()[0], yb + 0.31, 0], color=MUTED, stroke_width=1.2, dash_length=0.06))
        ip = interp("çıkarım · Şekil 9-2'den", GOLD, 15).next_to(hd, UP, buff=0.12).align_to(hd, RIGHT)
        hexr = VGroup(*[HX(b, 22, TXT, BOLD).move_to([byts[k][0].get_x(), -1.75, 0]) for k, b in enumerate(("00", "00", "FF", "FF", "00", "00", "29", "9E"))])
        hexl = T("boş başlık (PLI 0):", 15, IDC, BOLD).next_to(hexr, UP, buff=0.12).align_to(byts, LEFT)
        b7 = VGroup(HX("0x29 = 00 1 01001", 18, TXT, BOLD), T("→ Options 00 · LF 1 · HEC[12:8]", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.2)
        b8 = VGroup(HX("0x9E = 1001111", 18, TXT, BOLD), HX("0", 18, GOLD, BOLD), T("← eşlik biti", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.04)
        b8[2].shift(RIGHT * 0.15)
        bb = VGroup(b7, b8).arrange(RIGHT, buff=0.7).move_to([0, -2.6, 0])
        fit(bb, 12.6)
        pid = glow(VGroup(byts[2][0], byts[3][0]), PIDC, 0.06)
        self.play(self.set_src("G.989.3 Şekil 9-2 · bayt haritası ve örnek: çıkarım / hesap"), FadeIn(hd), run_time=0.5)
        self.at(self.cue("Analizör için bir bayt", 0.3))
        self.play(Create(bl), run_time=0.6)
        self.at(self.cue("bizim çıkarımımız", 2.7))
        self.play(FadeIn(ip), run_time=0.3)
        for ks, key, d in (((0,), "Birinci bayt göstergenin", 4.2), ((1,), "ikinci bayt alt altı", 7.6), ((2, 3), "Üçüncü ve dördüncü bayt", 11.3),
                           ((4, 5), "Beşinci ve altıncı bayt", 16.8), ((6,), "Yedinci bayt seçeneklerin", 19.7)):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(byts[k], shift=DOWN * 0.08) for k in ks], run_time=0.5)
            if ks == (2, 3):
                self.at(self.cue("bayta hizalı tek alan", 14.4))
                self.play(Create(pid), run_time=0.5)
        self.at(self.cue("son parça biti ve HEC'in üst", 23.0))
        self.play(FadeIn(hexl), FadeIn(hexr[:7]), FadeIn(b7, shift=UP * 0.06), run_time=0.6)
        self.at(self.cue("sekizinci bayt HEC'in kalanı", 26.2))
        self.play(FadeIn(byts[7], shift=DOWN * 0.08), FadeIn(hexr[7]), run_time=0.5)
        self.at(self.cue("en son bit eşlik", 28.6))
        self.play(FadeIn(b8, shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.05)

        # c12 — engineer note
        self.note11("c12", [("1", "XGEM asla başlık aramaz",
                             "Bozuk bir başlık bölümün kalanını götürür; bir sonraki bölümde her şey kendiliğinden toparlanır.", "XGEM asla başlık aramaz"),
                            ("2", "Artan HEC sayacı ≠ hat sorunu (yorum)",
                             "Yüksek BER ve senkron kaybı yokken artan sayaç\n→ büyük olasılıkla kapsülleme hatası, ör. yanlış bir PLI.", "rastgele hatalar başlığı")])
        self.bridge_beat("c13", "Sınırları bulduk.\nPeki bir birim kalan yere sığmazsa?")
        self.save_timeline("ep13_p2C")
