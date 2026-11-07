"""S2·B3 — 'Bu bölümde' opening + 'Önceki bölümde' recap with the answers to the S2·B2 quiz."""
from ep13_common import *

AGENDA = ["XGEM çerçevesi: başlık, yük, boş çerçeve", "Sınırlama: aramadan bulmak", "Parçalama: ↓ ve ↑ kuralları",
          "Servisler ve şifreleme", "Laboratuvarda: çöz · say · sına · ölç"]
PX, PY = 3.4, -0.45
CX = PX + 0.2


class Ep13Open(Act13):
    MANIFEST, FIRST = M13("open"), True

    def construct(self):
        # o1 — title, agenda, cover; the FS payload opens into XGEM frames
        self.beat("o1")
        tag_ = T(f"SEZON 2 · BÖLÜM {EP13['n']} · {tr_upper(EP13['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([CX, PY, 0])
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.8)
        s2 = pill("SEZON 2", GOLD, 18).move_to([CX, PY + 2.4, 0])
        num = T(f"{EP13['n']:02d}", 110, ACC, BOLD)
        sub = fit(T(EP13["sub"], 22, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP13["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.25).move_to([CX, PY + 0.95, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(s2), run_time=0.9)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.6)
        x0, y = CX - 2.9, PY - 2.3
        fs = strip([FS_(0.45, "HL"), FS_(0.8, "BWmap", BWC), FS_(0.8, "PLOAM", PLDC, 0.25), (3.35, "yük", PAYC, 0.12), FS_(0.4, "BIP", BIPC)], x0, y, 0.5, 15)
        fl = T("↓ FS çerçevesi (S2·B2)", 15, MUTED, BOLD).next_to(fs, UP, buff=0.1).align_to(fs, LEFT)
        px0 = fs[3].get_left()[0]
        xg = strip([H_(0.26), P_(0.55, "veri"), H_(0.26), P_(0.64, "OMCI", OMC), H_(0.26), P_(0.58, "parça"), H_(0.26), IP_(0.43)], px0, y, 0.5, 14)
        src_t = VGroup(tile("kullanıcı verisi", SAC, 1.9, 0.44, 15, 0.15), tile("OMCI", OMC, 1.2, 0.44, 15, 0.15)).arrange(RIGHT, buff=0.3).move_to([fs[3].get_x(), PY - 1.35, 0])
        ar = VGroup(*[arrow(t.get_bottom(), [t.get_x(), y + 0.3, 0], MUTED, 2, 0.1) for t in src_t])
        lk = lock(GOLD, 0.26).next_to(xg[5], UP, buff=0.08)
        self.at(self.cue("Geçen bölümde çerçeveyi", 2.0))
        self.play(FadeIn(fl), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in fs], lag_ratio=0.12), run_time=0.9)
        self.at(self.cue("Şimdi yükünü açıyoruz", 4.7))
        self.play(Indicate(fs[3], color=SAC, scale_factor=1.06), run_time=0.7)
        self.at(self.cue("kullanıcı verisinin ve yönetim", 6.5))
        self.play(FadeIn(src_t, shift=DOWN * 0.1), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.3), run_time=0.7)
        self.play(FadeOut(fs[3][1]), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.06) for s in xg[:4]], lag_ratio=0.15), run_time=0.9)
        self.at(self.cue("bölündüğünü ve korunduğunu", 13.6))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.06) for s in xg[4:]], lag_ratio=0.15), FadeIn(lk, shift=DOWN * 0.08), run_time=0.8)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(s2, cover, fs, fl, xg, src_t, ar, lk)

        # o2 — header, 4-byte rounding, idle, short idle
        self.beat("o2")
        hd = fields(XH, 5.8, 0.55, 15, 13, show_w=False, lpos=DOWN).move_to([CX, PY + 1.75, 0])
        hl = T("XGEM başlığı · 8 bayt", 16, GOLD, BOLD).next_to(hd, UP, buff=0.12)
        rnd = VGroup(eqline(("L", PLIC), ("→", MUTED), ("P = 4·⌈L/4⌉", TXT), size=20),
                     T("yük 4 bayta yuvarlanır", 15, MUTED, BOLD)).arrange(DOWN, buff=0.1).move_to([CX, PY + 0.45, 0])
        idl = strip([IH_(0.34), IP_(1.4), IH_(0.34), IP_(0.9), IH_(0.34), IP_(2.1)], CX - 2.71, PY - 0.75, 0.48, 14)
        idl_l = T("boş çerçeveler · Port-ID 0xFFFF", 15, IDC, BOLD).next_to(idl, DOWN, buff=0.08)
        si = VGroup(HX("00 00 00 00", 18, TXT, BOLD), tag("kısa boş · yalnızca ↑", PADC, 16)).arrange(RIGHT, buff=0.3).move_to([CX, PY - 2.15, 0])
        self.focus(0, VGroup(hd, hl, rnd, idl, idl_l, si))
        self.at(self.cue("sekiz baytlık başlık", 1.7))
        self.play(FadeIn(hl), LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in hd], lag_ratio=0.12), run_time=0.9)
        self.at(self.cue("yükün dört bayta", 3.5))
        self.play(FadeIn(rnd, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("boş çerçeveler", 6.4))
        self.play(FadeIn(idl, shift=RIGHT * 0.1), FadeIn(idl_l), run_time=0.6)
        self.at(self.cue("yalnızca yukarı yönde var olan", 7.7))
        self.play(FadeIn(si, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        # o3 — delineation without hunting; one bad header; counters
        self.beat("o3")
        x0, y = CX - 2.9, PY + 0.9
        ch = strip([H_(), P_(0.9), H_(), P_(1.3), H_(), P_(0.7), H_(), P_(1.65)], x0, y, 0.5, 14)
        hops = VGroup(*[hop(ch[2 * i].get_x(), ch[2 * i + 2].get_x(), y + 0.27, GOLD, 2.2, -1.0) for i in range(3)])
        nl = T("aramadan: PLI → bir sonraki başlık", 16, GOLD, BOLD).next_to(ch, DOWN, buff=0.15)
        bad = xmark(ch[4][0], WARN, 4)
        lost = Rectangle(width=ch[7].get_right()[0] - ch[2].get_left()[0], height=0.62, stroke_color=WARN, stroke_width=2.5,
                         fill_color=WARN, fill_opacity=0.15).move_to([(ch[2].get_left()[0] + ch[7].get_right()[0]) / 2, y, 0])
        lost_l = T("bölümün kalanı atılır", 16, WARN, BOLD).move_to([CX, PY - 0.75, 0])
        cnt = VGroup(tag("HEC hata sayacı", HECC, 16), T("+1", 22, WARN, BOLD)).arrange(RIGHT, buff=0.2).move_to([CX, PY - 1.85, 0])
        self.focus(1, VGroup(ch, hops, nl, bad, lost, lost_l, cnt))
        self.play(FadeIn(ch), run_time=0.4)
        self.at(self.cue("hiç aramadan nasıl", 1.3))
        self.play(LaggedStart(*[Create(hh) for hh in hops], lag_ratio=0.35), FadeIn(nl), run_time=1.2)
        self.at(self.cue("bir başlık bozulunca", 6.0))
        self.play(Create(bad), FadeIn(lost), FadeIn(lost_l, shift=UP * 0.08), run_time=0.7)
        self.at(self.cue("hangi sayaçların", 9.1))
        self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        # o4 — fragmentation: DS vs US, LF bit, reassembly, tiny grants
        self.beat("o4")
        rows = VGroup()
        for i, (lab, c) in enumerate((("↓ OLT", OLTC), ("↑ ONU", ONUC))):
            rl = T(lab, 17, c, BOLD)
            s = strip([H_(0.3), P_(1.5, "parça 1"), (0.25, "", BG, 0.0), H_(0.3), P_(1.0, "parça 2")], 0, 0, 0.48, 14)
            rows.add(VGroup(rl, s).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([CX, PY + 1.35, 0])
        lf = VGroup(*[VGroup(tag("LF = 0", LFC, 14).next_to(r[1][1], UP, buff=0.06), tag("LF = 1", LFC, 14).next_to(r[1][4], UP, buff=0.06)) for r in rows])
        rb = VGroup(tile("parça 1", SAC, 1.3, 0.42, 14, 0.15), T("+", 18, MUTED, BOLD), tile("parça 2", SAC, 1.3, 0.42, 14, 0.15),
                    T("→", 20, MUTED, BOLD), tile("birim", SAC, 1.3, 0.42, 14, 0.3)).arrange(RIGHT, buff=0.15).move_to([CX, PY - 0.6, 0])
        rbl = T("yeniden birleştirme", 15, MUTED, BOLD).next_to(rb, UP, buff=0.08)
        sm = VGroup(words([("DBRu", BWC, 0.4), ("", IDC, 0.12), ("", IDC, 0.12), ("", IDC, 0.12)], 0.66, 0.42, 14), T("küçük tahsis · 4 sözcük", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.3)
        sm.move_to([CX, PY - 1.95, 0])
        self.focus(2, VGroup(rows, lf, rb, rbl, sm))
        self.at(self.cue("aşağı ve yukarı yönün", 1.6))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.3), run_time=0.8)
        self.at(self.cue("son parça biti", 4.9))
        self.play(FadeIn(lf), run_time=0.5)
        self.at(self.cue("yeniden birleştirme", 6.2))
        self.play(FadeIn(rb, shift=UP * 0.08), FadeIn(rbl), run_time=0.6)
        self.at(self.cue("çok küçük tahsisler", 7.9))
        self.play(FadeIn(sm, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # o5 — services and encryption
        self.beat("o5")
        mp = VGroup(tile("Ethernet", R10, 1.7, 0.48, 16, 0.15), tile("OMCI", OMC, 1.3, 0.48, 16, 0.15)).arrange(RIGHT, buff=0.25)
        tgt = tile("XGEM yükü", SAC, 1.8, 0.48, 16, 0.2)
        mrow = VGroup(mp, tgt).arrange(RIGHT, buff=0.6).move_to([CX, PY + 1.65, 0])
        ma = arrow(mp.get_right(), tgt.get_left(), MUTED, 2.2, 0.12)
        fs_ = VGroup(T("diğer servisler:", 16, MUTED, BOLD), tag("daha fazla çalışma konusu", MUTED, 15)).arrange(RIGHT, buff=0.2).move_to([CX, PY + 0.65, 0])
        x0, y = CX - 2.4, PY - 0.75
        fr = strip([(1.3, "başlık", SAC, 0.55), (3.5, "yük + dolgu", SAC, 0.14)], x0, y, 0.6, 16)
        lo = lock(GOOD, 0.3, opened=True).next_to(fr[0], DOWN, buff=0.15)
        lc = lock(GOLD, 0.3).next_to(fr[1], DOWN, buff=0.15)
        lol = T("açık", 15, GOOD, BOLD).next_to(lo, RIGHT, buff=0.12)
        lcl = T("şifreli", 15, GOLD, BOLD).next_to(lc, RIGHT, buff=0.12)
        self.focus(3, VGroup(mrow, ma, fs_, fr, lo, lc, lol, lcl))
        self.at(self.cue("Ethernet ve OMCI'ın", 2.4))
        self.play(FadeIn(mp, shift=RIGHT * 0.1), GrowArrow(ma), FadeIn(tgt), run_time=0.7)
        self.at(self.cue("çalışma konusu olarak", 4.9))
        self.play(FadeIn(fs_, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("şifrelemenin XGEM başlığına", 7.5))
        self.play(FadeIn(fr), run_time=0.4)
        self.play(FadeIn(lo), FadeIn(lol), FadeIn(lc), FadeIn(lcl), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab: traffic generator + analyzer
        self.beat("o6")
        tg = tg_icon(2.2, 1.45).move_to([CX - 1.4, PY + 1.15, 0])
        pa = pa_icon(2.2, 1.45).move_to([CX + 1.4, PY + 1.15, 0])
        ts = VGroup(*[tag(s, GOOD, 16) for s in ("başlık çöz", "boş say", "parçalama", "verim")]).arrange(RIGHT, buff=0.15).move_to([CX, PY - 1.25, 0])
        fit(ts, 6.1)
        self.focus(4, VGroup(tg, pa, ts))
        self.play(FadeIn(tg, shift=UP * 0.1), FadeIn(pa, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(ts[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("boş çerçeveleri sayacağız", 6.9))
        self.play(FadeIn(ts[1], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("parçalamayı sınayacağız", 9.1))
        self.play(FadeIn(ts[2], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("verimi ölçeceğiz", 10.8))
        self.play(FadeIn(ts[3], shift=UP * 0.08), run_time=0.4)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep13_open")

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


class Ep13Recap(Act13):
    HDR, MANIFEST, FIRST = f"SEZON 2 · BÖLÜM {K13} · ÖNCEKİ BÖLÜMDE", M13("recap"), True

    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.2)

    def construct(self):
        # a1 — 2.5G DS: 157 RS codewords, the shortened last one
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Sezon 2 · Bölüm 2 · Çerçeve")
        self.at(self.cue("Birinci soru", 1.9))
        self.to_header(tc)
        self.set_badge("ozet")
        q1 = self.qhead(1, "2,5G aşağı yön çerçevesi kaç RS kod sözcüğüne bölünür? Sonuncusuna ne olur?", CH[0])
        y = 0.75
        x0 = -6.3
        full = VGroup()
        bw = 1.55
        for i in range(4):
            full.add(strip([(bw * 232 / 248, "248 B", PAYC, 0.16 if i % 2 else 0.26), (bw * 16 / 248, "", PARC, 0.55)], x0 + i * bw, y, 0.55, 15))
        dots = T("…", 30, MUTED, BOLD).move_to([x0 + 4 * bw + 0.55, y, 0])
        x1 = x0 + 4 * bw + 1.1
        full2 = strip([(bw * 232 / 248, "248 B", PAYC, 0.26), (bw * 16 / 248, "", PARC, 0.55)], x1, y, 0.55, 15)
        sw = bw * 168 / 248
        short = strip([(sw - bw * 16 / 248, "168 B", GOLD, 0.3), (bw * 16 / 248, "", PARC, 0.55)], x1 + bw, y, 0.55, 15)
        b156 = brace_lbl(VGroup(full, full2), "156 tam sözcük × 248 B (232 veri + 16 eşlik)", PAYC, UP, 16)
        bsh = brace_lbl(short, "kısa son sözcük", GOLD, UP, 16)
        bsh[1].shift(RIGHT * 0.4)
        n157 = pill("157 kod sözcüğü", ACC, 20).move_to([5.1, y, 0])
        y2 = -1.35
        zx0 = -4.6
        u = 0.022
        zpad = seg(zx0, 80 * u, y2, MUTED, "80 × 0x00", 0.6, 0.1, 16, dashed=True)
        zdat = seg(zx0 + 80 * u, 152 * u, y2, GOLD, "152 B veri", 0.6, 0.3, 16)
        zpar = seg(zx0 + 232 * u, 16 * u * 2.2, y2, PARC, "16", 0.6, 0.55, 15)
        zl = zoom_lines(short, VGroup(zdat, zpar), GOLD)
        bz = brace_lbl(VGroup(zpad, zdat), "232 B · kodlayıcının veri bloğu", MUTED, DOWN, 16)
        nos = T("gönderilmez", 17, WARN, BOLD).next_to(zpad, UP, buff=0.12)
        onu = VGroup(tag("ONU", ONUC, 16), T("çözmeden önce 80 sıfırı geri ekler", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([3.6, -2.75, 0])
        self.play(FadeIn(q1, shift=RIGHT * 0.2), self.set_src("G.989.3 §10.1.3.1.1 · Tablo 8-1 · Ek IV.4"), run_time=0.6)
        self.at(self.cue("Yüz elli yedi", 7.5))
        self.play(FadeIn(n157, scale=0.9), run_time=0.5)
        self.at(self.cue("iki yüz kırk sekiz baytlık yüz elli altı", 9.9))
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.08) for f in full], lag_ratio=0.15), FadeIn(dots), FadeIn(full2), FadeIn(b156), run_time=1.0)
        self.at(self.cue("yüz altmış sekiz baytlık kısa", 14.2))
        self.play(FadeIn(short, shift=RIGHT * 0.08), FadeIn(bsh), run_time=0.6)
        self.at(self.cue("Sonuncunun yüz elli iki", 18.2))
        self.play(Create(zl), FadeIn(zdat), FadeIn(zpar), run_time=0.7)
        self.at(self.cue("başına seksen sıfır bayt", 21.5))
        self.play(FadeIn(zpad, shift=RIGHT * 0.1), FadeIn(bz), run_time=0.6)
        self.at(self.cue("Bu sıfırlar gönderilmez", 26.7))
        self.play(FadeIn(nos, shift=DOWN * 0.08), run_time=0.4)
        self.at(self.cue("ONU çözmeden önce", 28.7))
        self.play(FadeIn(onu, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        # a2 — 3 PSync bit errors: Re-Sync, no LODS; LODS after M−1 = 2 more
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "Senkrondaki bir ONU, PSync'te 3 bit hatalı bir çerçeve alırsa?", CH[1])
        sm = SyncSM(y=0.05)
        rng = np.random.default_rng(13)
        err = set(rng.choice(64, 3, replace=False).tolist())
        bits = VGroup()
        bw = 6.4 / 64
        for i in range(64):
            c = WARN if i in err else PSC
            bits.add(Rectangle(width=bw, height=0.32, stroke_color=c, stroke_width=1.2, fill_color=c, fill_opacity=0.85 if i in err else 0.25).move_to([-6.2 + bw * (i + 0.5), -2.5, 0]))
        bl = T("PSync · 64 bit · 3 hatalı", 15, PSC, BOLD).next_to(bits, UP, buff=0.08).align_to(bits, LEFT)
        mt = VGroup(T("61 / 64 eşleşme", 18, TXT, BOLD), T("< 62", 18, WARN, BOLD), ok_x(False, 20)).arrange(RIGHT, buff=0.2).next_to(bits, RIGHT, buff=0.35)
        cur = glow(sm.b[2], GOLD, 0.06)
        nol = tag("LODS yok", GOOD, 16).next_to(sm.b[3], DOWN, buff=0.5)
        lods = tag("LODS ilan edilir", WARN, 16).next_to(sm.b[0], DOWN, buff=0.5)
        tot = pill("3 çerçeve × 125 µs = 375 µs", WARN, 19).move_to([4.4, -3.1, 0])
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.3 §10.1.1.3 · Şekil 10-4 · Tablo 14-3"), run_time=0.6)
        self.play(FadeIn(sm.all()), Create(cur), run_time=0.8)
        self.at(self.cue("senkron deseninde üç bit", 2.7))
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(b) for b in bits], lag_ratio=0.01), run_time=0.8)
        self.at(self.cue("Doğrulama en az", 7.0))
        self.play(FadeIn(mt[0], shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("altmış bir yetmez", 11.1))
        self.play(FadeIn(mt[1:], shift=LEFT * 0.08), run_time=0.4)
        self.at(self.cue("Makine yeniden senkron", 12.6))
        self.play(Indicate(sm.sr, color=WARN, scale_factor=1.05), cur.animate.move_to(sm.b[3]), run_time=0.7)
        self.at(self.cue("ama senkron kaybı ilan edilmez", 15.8))
        self.play(FadeIn(nol, shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("yani iki ardışık kötü", 19.4))
        self.play(Indicate(sm.rh, color=WARN, scale_factor=1.03), run_time=0.8)
        self.at(self.cue("ve kayıp ancak o zaman", 24.4))
        self.play(cur.animate.move_to(sm.b[0]), FadeIn(lods, shift=UP * 0.08), run_time=0.7)
        self.at(self.cue("toplam üç çerçeve", 27.4))
        self.play(FadeIn(tot, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.1)

        # a3 — 10G ONU without an ID, FEC on, SN grant: 56 B → 88 B, ONU-ID 1023
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "Kimliği olmayan 10G ONU, FEC açıkken seri numarası tahsisine ne gönderir?", CH[3])
        y = 0.75
        u = 0.075
        pre = strip([(1.3, "önsöz", PHC, 0.3), (0.75, "sın.", PHC, 0.65)], -6.2, y, 0.6, 16)
        bx0 = pre.get_right()[0]
        bur = strip([(1.25, "başlık · 4 B", HLC, 0.3), (3.0, "PLOAMu · 48 B", PLDC, 0.25), (1.15, "BIP · 4 B", BIPC, 0.3)], bx0, y, 0.6, 15)
        b56 = brace_lbl(bur, "56 B", GOLD, UP, 18)
        pl = T("profilin önsözü ve sınırlayıcısı", 15, PHC, BOLD).next_to(pre, DOWN, buff=0.12).align_to(pre, LEFT)
        y2 = -0.95
        cw = strip([(bur.width, "56 B", GOLD, 0.25), (bur.width * 32 / 56, "32 B eşlik", PARC, 0.5)], bx0, y2, 0.6, 16)
        b88 = brace_lbl(cw, "88 B · tek kısaltılmış RS(248, 216) sözcüğü", ACC, DOWN, 17)
        ca = arrow([bur.get_x(), y - 0.35, 0], [bur.get_x(), y2 + 0.35, 0], MUTED, 2.2, 0.12)
        hd = fields([("ONU-ID", 10, ACC), ("Ind", 9, MUTED), ("HEC", 13, MUTED)], 4.6, 0.55, 16, 14, show_w=False).move_to([-3.9, -2.65, 0])
        hv = HX("1023", 18, GOLD, BOLD).move_to(hd[0][0])
        hl = T("= 0x3FF · atanmamış ONU-ID", 17, GOLD, BOLD).next_to(hd, RIGHT, buff=0.3)
        hl2 = T("↑ FS başlığı", 15, MUTED, BOLD).next_to(hd, UP, buff=0.08).align_to(hd, LEFT)
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.3 §8.1.1.2 · §8.1.2.1.1 · §10.1.3.2"), run_time=0.6)
        self.at(self.cue("Dört bayt başlık", 7.5))
        self.play(FadeIn(bur[0], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("kırk sekiz bayt PLOAM", 9.8))
        self.play(FadeIn(bur[1], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("dört bayt kuyruk", 11.7))
        self.play(FadeIn(bur[2], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("elli altı bayt", 13.1))
        self.play(FadeIn(b56), run_time=0.4)
        self.at(self.cue("Tek bir kısaltılmış kod", 14.3))
        self.play(GrowArrow(ca), FadeIn(cw, shift=DOWN * 0.08), run_time=0.7)
        self.at(self.cue("seksen sekiz bayt", 19.3))
        self.play(FadeIn(b88), run_time=0.5)
        self.at(self.cue("önünde profilin önsözü", 20.9))
        self.play(FadeIn(pre, shift=RIGHT * 0.08), FadeIn(pl), run_time=0.6)
        self.at(self.cue("Başlıktaki ONU kimliği", 24.5))
        self.play(Indicate(bur[0], color=ACC, scale_factor=1.08), FadeIn(hd), FadeIn(hl2), run_time=0.6)
        self.at(self.cue("atanmamış değer olan bin yirmi üç", 26.4))
        self.play(FadeOut(hd[0][1]), FadeIn(hv, scale=0.8), FadeIn(hl, shift=LEFT * 0.08), run_time=0.5)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep13_recap")
