"""S2·B9 — 'Bu bölümde' opening + 'Önceki bölümde' recap with the answers to the S2·B8 quiz."""
from ep19_common import *

AGENDA = ["Dikkatli uyku ve iki makine", "Tasarruf, kanal seçimi ve PtP hız", "Sayaçlar", "Kusurlar ve son nefes",
          "Laboratuvarda: uyku, sayaçlar, kusurlar"]
PX, PY = 3.4, -0.45
CX = PX + 0.2


class Ep19Open(Act19):
    MANIFEST, FIRST = M19("open"), True

    def construct(self):
        # o1 — title, agenda, cover; two everyday questions (energy, health) → §16 power management + §14 performance monitoring;
        #      not a word changed since 2021, only the references around them
        self.beat("o1")
        tag_ = T(f"SEZON 2 · BÖLÜM {EP19['n']} · {tr_upper(EP19['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
        head = T("Bu bölümde", 54, TXT, BOLD).next_to(tag_, DOWN, buff=0.25, aligned_edge=LEFT)
        items = VGroup(*[VGroup(T(f"{i + 1:02d}", 22, MUTED, BOLD), T(s, 22, TXT, MEDIUM)).arrange(RIGHT, buff=0.3) for i, s in enumerate(AGENDA)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.52).next_to(head, DOWN, buff=0.7, aligned_edge=LEFT)
        for it in items:
            fit(it, 6.0)
        self.bar = Rectangle(width=0.07, height=0.5, stroke_width=0, fill_color=ACC, fill_opacity=1)
        panel = RoundedRectangle(corner_radius=0.2, width=6.6, height=6.0, stroke_color=LINE, stroke_width=1.5, fill_color="#0C1324", fill_opacity=1).move_to([CX, PY, 0])
        self.play(FadeIn(tag_, shift=RIGHT * 0.2), FadeIn(head, shift=RIGHT * 0.3), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(it, shift=RIGHT * 0.25) for it in items], lag_ratio=0.18), FadeIn(panel), run_time=1.0)
        s2 = pill("SEZON 2", GOLD, 18).move_to([CX, PY + 2.4, 0])
        num = T(f"{EP19['n']:02d}", 110, ACC, BOLD)
        sub = fit(T(EP19["sub"], 22, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP19["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.25).move_to([CX, PY + 1.05, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(s2), run_time=0.5)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.3)
        y = PY - 1.0
        qa = VGroup(T("ne kadar enerji?", 17, GOLD, BOLD), T("→ §16 güç yönetimi", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        qb = VGroup(T("sağlığı nasıl?", 17, GOOD, BOLD), T("→ §14 başarım izleme", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        qg = VGroup(qa, qb).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(qg, 6.1).move_to([CX, y, 0])
        ed = VGroup(ed_chips(15, GOOD), T("§14 · §16: değişiklik yok", 16, GOOD, BOLD)).arrange(DOWN, buff=0.1)
        fit(ed, 6.1).move_to([CX, PY - 2.05, 0])
        at = VGroup(T("değişen: atıflar", 15, GOLD, BOLD), T("G.988 (2017 → 2022) · tablo numaraları", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.15)
        fit(at, 6.1).move_to([CX, PY - 2.75, 0])
        self.at(self.cue("ne kadar enerji harcıyor", 6.1))
        self.play(FadeIn(qa[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("ve sağlığı nasıl?", 8.2))
        self.play(FadeIn(qb[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("güç yönetimi ve başarım", 12.5))
        self.play(FadeIn(qa[1], shift=LEFT * 0.05), FadeIn(qb[1], shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("tek bir sözcük değişmedi", 16.2))
        self.play(FadeIn(ed, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("değişen yalnızca çevrelerindeki", 20.4))
        self.play(FadeIn(at, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(s2, cover, qg, ed, at)

        # o2 — watchful sleep: the only sleep mode; two partially aligned state machines; parameters with no values
        self.beat("o2")
        ws = pill("dikkatli uyku · watchful sleep", SRW, 18).move_to([CX, PY + 2.15, 0])
        rn = VGroup(*[tile(f"({k})", pcol("N", k), 0.62, 0.42, 16, 0.25) for k in range(1, 5)]).arrange(RIGHT, buff=0.08)
        rl = VGroup(*[tile(f"({k})", pcol("L", k), 0.62, 0.42, 16, 0.25) for k in range(1, 5)]).arrange(RIGHT, buff=0.08)
        sm = VGroup(VGroup(T("OLT CT", 16, OLTC, BOLD), rl).arrange(RIGHT, buff=0.2), VGroup(T("ONU", 16, ONUC, BOLD), rn).arrange(RIGHT, buff=0.2))
        sm.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to([CX - 0.95, PY + 0.75, 0])
        al = T("≈ kısmen hizalı", 17, GOLD, BOLD).next_to(sm, RIGHT, buff=0.3)
        ps = VGroup(*[tag(s, TMRC, 15) for s in ("Ilowpower", "Iaware", "Irxoff", "Ihold", "Itransinit")]).arrange(RIGHT, buff=0.1)
        fit(ps, 6.1).move_to([CX, PY - 1.0, 0])
        nv = tag("değer yok · birim: 125 µs çerçeve", WARN, 16).move_to([CX, PY - 1.75, 0])
        self.focus(0, VGroup(ws, sm, al, ps, nv))
        self.at(self.cue("standardın bıraktığı tek", 1.6))
        self.play(FadeIn(ws, scale=0.9), run_time=0.4)
        self.at(self.cue("kısmen hizalı iki durum", 4.5))
        self.play(FadeIn(sm[0], shift=DOWN * 0.05), FadeIn(sm[1], shift=UP * 0.05), run_time=0.5)
        self.play(FadeIn(al, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("hiçbirinin değeri olmayan", 9.6))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.05) for p in ps], lag_ratio=0.1), run_time=0.5)
        self.play(FadeIn(nv, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # o3 — the arithmetic of saving; channel selection; PtP WDM line-rate adjustment with timers still "for further study"
        self.beat("o3")
        fm = VGroup(T("tasarruf =", 19, TXT, BOLD), T("R / (1 + R) · (1 − p)", 21, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([CX, PY + 2.0, 0])
        fy = ytag("bizim modelimiz").next_to(fm, DOWN, buff=0.12)
        chs = VGroup(*[Rectangle(width=0.5, height=hh, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.45) for c, hh in zip(CH, (1.0, 0.8, 1.15, 0.6))])
        chs.arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to([CX - 1.6, PY + 0.2, 0])
        pick = SurroundingRectangle(chs[3], color=GOOD, buff=0.06, stroke_width=2.5)
        chl = T("daha az tüketen kanal", 15, GOOD, BOLD).next_to(chs, DOWN, buff=0.12)
        rt = VGroup(T("PtP WDM", 16, PTPC, BOLD), T("10G → 2,5G", 18, TXT, BOLD), T("hız ↓ · güç ↓", 15, MUTED, BOLD)).arrange(DOWN, buff=0.08).move_to([CX + 1.6, PY + 0.3, 0])
        ffs = VGroup(*[tag(s, WARN, 15) for s in ("T_1 · FFS", "T_wait_t_olt · FFS", "T_wait_onu · FFS")]).arrange(RIGHT, buff=0.1)
        fit(ffs, 6.1).move_to([CX, PY - 1.65, 0])
        ffl = T("çalışma konusu (for further study)", 15, WARN, BOLD).next_to(ffs, DOWN, buff=0.12)
        self.focus(1, VGroup(fm, fy, chs, pick, chl, rt, ffs, ffl))
        self.play(FadeIn(fm, shift=UP * 0.05), FadeIn(fy), run_time=0.45)
        self.at(self.cue("daha az tüketen bir kanala", 3.3))
        self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in chs], lag_ratio=0.12), run_time=0.6)
        self.play(Create(pick), FadeIn(chl), run_time=0.4)
        self.at(self.cue("hattı yavaşlatmak", 6.2))
        self.play(FadeIn(rt, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("çalışma konusu olan", 9.9))
        self.play(FadeIn(ffs, shift=UP * 0.05), FadeIn(ffl), run_time=0.45)
        self.end(pad=0.05)

        # o4 — counters: a 111-row table, which are mandatory, who keeps them, numbers that can wrap within seconds at 10G
        self.beat("o4")
        gr = pm_grid(x_lab=0, x0=0, y0=0, dy=0.24, cw=0.13, gap=0.025, h=0.17, size=14)
        mini = VGroup(*[r[1] for r in gr])
        mini.move_to([CX, PY + 1.45, 0])
        ml = T("Tablo 14-1 · 111 satır", 17, TXT, BOLD).next_to(mini, UP, buff=0.15)
        mo = VGroup(VGroup(pm_cell(True, 0.22, 0.26), T("37 zorunlu", 16, MANC, BOLD)).arrange(RIGHT, buff=0.1),
                    VGroup(pm_cell(False, 0.22, 0.26), T("74 isteğe bağlı", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.5)
        mo.next_to(mini, DOWN, buff=0.25)
        who = VGroup(*[tag(s, c, 15) for s, c in (("ONU", ONUC), ("OLT · ONU başına", OLTC), ("OLT · toplam", OLTC))]).arrange(RIGHT, buff=0.12)
        fit(who, 6.1).next_to(mo, DOWN, buff=0.25)
        wr = VGroup(T("10G · 32 bit:", 16, MUTED, BOLD), T("saniyeler içinde taşar", 17, WARN, BOLD)).arrange(RIGHT, buff=0.15).next_to(who, DOWN, buff=0.3)
        wy = ytag("bizim hesabımız").next_to(wr, DOWN, buff=0.1)
        self.focus(2, VGroup(mini, ml, mo, who, wr, wy))
        self.at(self.cue("yüz on bir satırlık", 1.5))
        self.play(FadeIn(ml), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.05) for r in mini], lag_ratio=0.06), run_time=0.7)
        self.at(self.cue("hangisi zorunlu", 4.1))
        self.play(FadeIn(mo, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("kim tutar", 5.4))
        self.play(FadeIn(who, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("saniyeler içinde taşabilecek", 6.6))
        self.play(FadeIn(wr, shift=UP * 0.05), FadeIn(wy), run_time=0.4)
        self.end(pad=0.05)

        # o5 — defects and the dying gasp: nine OLT defects, one ONU defect, three without clearing conditions, the record a dying ONU leaves
        self.beat("o5")
        dn = ["LOBi", "LOS", "TIWi", "SUFi", "DFi", "LOPCi", "LOOCi", "DOTXi", "ALRFi"]
        dt = VGroup(*[tile(s, DEFC, 1.12, 0.42, 15, 0.16) for s in dn])
        VGroup(VGroup(*dt[:5]).arrange(RIGHT, buff=0.08), VGroup(*dt[5:]).arrange(RIGHT, buff=0.08)).arrange(DOWN, buff=0.1)
        dt.move_to([CX, PY + 1.75, 0])
        dl = T("OLT CT · 9", 16, OLTC, BOLD).next_to(dt, UP, buff=0.12)
        od = VGroup(T("ONU · 1", 16, ONUC, BOLD), tile("LODS", LDC, 1.12, 0.42, 15, 0.2)).arrange(RIGHT, buff=0.2).move_to([CX, PY + 0.45, 0])
        nc = VGroup(*[SurroundingRectangle(dt[k], color=NOCLR, buff=0.04, stroke_width=2.5) for k in (5, 6, 7)])
        ncl = T("temizlenme koşulu yok", 16, NOCLR, BOLD).move_to([CX, PY - 0.3, 0])
        nv = nvm_icon(10, 3, 2.4, 1.0).move_to([CX - 1.3, PY - 1.75, 0])
        dg = VGroup(T("son nefes", 17, GOLD, BOLD), T("→ acil durum kaydı", 16, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(nv, RIGHT, buff=0.3)
        self.focus(3, VGroup(dt, dl, od, nc, ncl, nv, dg))
        self.at(self.cue("OLT'nin dokuz kusuru", 2.4))
        self.play(FadeIn(dl), LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in dt], lag_ratio=0.08), run_time=0.7)
        self.at(self.cue("ONU'nun tek kusuru", 4.1))
        self.play(FadeIn(od, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("temizlenme koşulu yazılmamış", 5.7))
        self.play(Create(nc), FadeIn(ncl, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("geride bıraktığı kayıt", 8.9))
        self.play(FadeIn(nv, shift=UP * 0.05), FadeIn(dg, shift=LEFT * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # o6 — lab: power per state, wake-up latency + forced wake-up bit, error / defect injection with counter checks, a dying gasp
        self.beat("o6")
        em = emu_icon(1.6, 1.15, "OLT · ONU emülatörü").move_to([CX - 1.4, PY + 1.6, 0])
        lg = logger_icon(1.6, 1.15, "Akım kaydı").move_to([CX + 1.4, PY + 1.6, 0])
        ts_ = VGroup(*[tag(s, GOOD, 16) for s in ("durumlara göre güç", "uyanma gecikmesi · FWI", "hata · kusur enjeksiyonu → sayaçlar", "son nefes")])
        rows = VGroup(ts_[0], ts_[1], ts_[2], ts_[3]).arrange(DOWN, buff=0.18)
        fit(rows, 6.1).move_to([CX, PY - 1.1, 0])
        self.focus(4, VGroup(em, lg, rows))
        self.play(FadeIn(em, shift=UP * 0.1), FadeIn(lg, shift=UP * 0.1), FadeIn(ts_[0], shift=UP * 0.06), run_time=0.6)
        for k, (key, d) in enumerate((("uyanma gecikmesini", 3.5), ("hata ve kusur enjekte", 8.2), ("bir son nefesi", 12.4))):
            self.at(self.cue(key, d))
            self.play(FadeIn(ts_[k + 1], shift=UP * 0.06), run_time=0.35)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep19_open")

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


class Ep19Recap(Act19):
    HDR, MANIFEST, FIRST = f"SEZON 2 · BÖLÜM {K19} · ÖNCEKİ BÖLÜMDE", M19("recap"), True

    def construct(self):
        # a1 — the upstream counter block: lower 64 bits = bit complement of SFC(49..0) | IFC(13..0); the NOTE's two weak values (≈ 250 µs once
        #      in ~4000 years, remedy: start the SFC small); our finding: only 2^49 is reachable, SFC(49..0) = 0 is a third weak frame → small ≥ 1
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Sezon 2 · Bölüm 8 · Güven")
        q1 = self.qhead(1, "Tek alıcılı anahtar iki yönü şifreler: ↓ ve ↑ yükün aynı anahtar akışını kullanmasını ne engeller,\nnot hangi istisnayı anar?", CH[0])
        self.at(self.cue("Birinci soru", 1.7))
        self.to_header_badge(tc, "ozet", 0.6, [FadeIn(q1, shift=RIGHT * 0.2), self.set_src("G.989.3 §15.4.3 · Şekil 15-2 · NOT · çıkarım: S2·B8 bizim")])
        ib = icb(True, 11.0, 0.55, 16, 14, True).move_to([0.75, 1.0, 0])
        ibl = T("↑ sayaç bloğu", 16, TXT, BOLD).next_to(ib, LEFT, buff=0.15).shift(UP * 0.05)
        lo = brace_lbl(VGroup(ib[2][0], ib[3][0]), "alt 64 bit = SFC(49..0) | IFC(13..0)'ın bit bit tümleyeni", NOTC, DOWN, 15)
        lo.shift(DOWN * 0.25)
        y = -1.25
        ax = Line([-5.6, y, 0], [5.6, y, 0], color=SFCC8, stroke_width=3)
        X = lambda f: -5.6 + 11.2 * f
        al = VGroup(T("SFC(49..0)", 15, SFCC8, BOLD).next_to(ax, LEFT, buff=0.12), T("0", 15, MUTED, BOLD).next_to([X(0), y, 0], DOWN, buff=0.1),
                    T("2⁵⁰", 15, MUTED, BOLD).next_to([X(1), y, 0], DOWN, buff=0.1))
        mid = Rectangle(width=0.1, height=0.42, stroke_width=0, fill_color=WARN, fill_opacity=1).move_to([X(0.5), y, 0])
        wv = VGroup(T("0b1(0)⁴⁹ = 2⁴⁹", 15, WARN, BOLD), T("0b0(1)⁴⁹ = 2⁴⁹ − 1", 15, WARN, BOLD)).arrange(DOWN, buff=0.05).next_to(mid, UP, buff=0.12)
        wt = T("≈ 250 µs · ~4000 yılda bir", 15, WARN, BOLD).next_to(mid, DOWN, buff=0.12)
        rem = VGroup(T("çare:", 15, GOOD, BOLD), T("SFC'yi küçük bir değerle başlat", 15, TXT, BOLD)).arrange(RIGHT, buff=0.12).move_to([-3.0, -2.1, 0])
        ours = VGroup(ytag("bizim çıkarımımız"), T("yalnızca 2⁴⁹ ulaşılır · 2⁴⁹ − 1 için IFC ≥ 15 872 gerekirdi: yasal aralığın dışı", 15, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(ours, 12.4).move_to([0, -2.7, 0])
        z0 = Rectangle(width=0.1, height=0.42, stroke_width=0, fill_color=WARN, fill_opacity=1).move_to([X(0.004), y, 0])
        zl = VGroup(T("SFC(49..0) = 0:", 15, WARN, BOLD), T("üçüncü zayıf çerçeve", 15, TXT, BOLD)).arrange(RIGHT, buff=0.1).next_to(z0, UP, buff=0.12).align_to(z0, LEFT)
        small = VGroup(T("→ küçük, ama", 16, TXT, BOLD), T("en az 1", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.12).move_to([3.4, -2.1, 0])
        self.at(self.cue("aynı anahtar akışını", 3.0))
        self.play(FadeIn(ibl), FadeIn(ib[:2]), run_time=0.5)
        self.at(self.cue("alt altmış dört biti", 7.5))
        self.play(FadeIn(ib[2:], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("bit bit tümleyenidir", 13.0))
        self.play(FadeIn(lo, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("Standardın notu iki zayıf", 16.3))
        self.play(Create(ax), FadeIn(al), run_time=0.5)
        self.at(self.cue("birin ardından kırk dokuz", 19.4))
        self.play(FadeIn(mid, scale=1.4), FadeIn(wv, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("dört bin yılda bir", 25.1))
        self.play(FadeIn(wt, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("sayacı küçük bir değerle", 30.1))
        self.play(FadeIn(rem, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("yalnızca birincisine ulaşılır", 34.6))
        self.play(FadeIn(ours, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("alanın sıfırı da", 37.1))
        self.play(FadeIn(z0, scale=1.4), FadeIn(zl, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("en az bir olmalı", 41.1))
        self.play(FadeIn(small, shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.1)

        # a2 — default Registration_ID → public MSK; SK from SN (Serial_Number_ONU octets 5–12) + PON-TAG (Burst_Profile) → KEK (both AES-CMAC);
        #      the data key = Key_Report fragment decrypted with KEK in AES-ECB; three messages suffice
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "Kayıt kimliği varsayılan kalmış bir ONU'nun veri anahtarına hangi mesajlardan ulaşılır?", CH[1])
        y1, y2, y3 = 1.0, -0.35, -1.65
        rid = VGroup(T("Registration_ID", 16, CNC, BOLD), T("= 36 × 0x00", 16, TXT, BOLD)).arrange(RIGHT, buff=0.12).move_to([-4.6, y1, 0])
        msk = knode("MSK", None, 1.3, 0.48, 16).move_to([-0.9, y1, 0])
        pub = tag("herkesçe bilinir", WARN, 15).next_to(msk, RIGHT, buff=0.25)
        a0 = arrow(rid.get_right() + RIGHT * 0.1, msk.get_left(), MUTED, 2, 0.1)
        sn = mbox("↑ Serial_Number_ONU · oktet 5–12", ONUC, 3.6, 0.4, 15).move_to([-4.6, y2 + 0.25, 0])
        pt = mbox("↓ Burst_Profile · PON-TAG", GOLD, 3.6, 0.4, 15).move_to([-4.6, y2 - 0.25, 0])
        sk = knode("SK", None, 1.1, 0.48, 16).move_to([-0.9, y2, 0])
        kek = knode("KEK", None, 1.2, 0.48, 16).move_to([1.6, y2, 0])
        a1 = VGroup(arrow(msk.get_bottom(), sk.get_top(), MSKC, 2, 0.1), arrow(sn.get_right(), sk.get_left() + UP * 0.08, ONUC, 1.8, 0.09),
                    arrow(pt.get_right(), sk.get_left() + DOWN * 0.08, GOLD, 1.8, 0.09))
        a2 = arrow(sk.get_right(), kek.get_left(), SKC8, 2, 0.1)
        cm = VGroup(tag("AES-CMAC", MICC, 15).move_to([-0.9 + 1.25, y2 + 0.42, 0]))
        cm2 = tag("AES-CMAC", MICC, 15).next_to(a1[0], LEFT, buff=0.12)
        kr = mbox("↑ Key_Report · Key_Fragment", ONUC, 3.6, 0.42, 15).move_to([-4.6, y3, 0])
        ecb = VGroup(T("AES-ECB⁻¹ ( KEK ,", 16, KEKC, BOLD), T("parça )", 16, TXT, BOLD)).arrange(RIGHT, buff=0.1).move_to([0.9, y3, 0])
        dek = knode("DEK", None, 1.2, 0.48, 16).move_to([4.1, y3, 0])
        dkl = T("veri anahtarı", 15, DEKC, BOLD).next_to(dek, RIGHT, buff=0.15)
        a3 = VGroup(arrow(kr.get_right(), ecb.get_left(), ONUC, 1.8, 0.09), arrow(kek.get_bottom(), [kek.get_x(), ecb.get_top()[1] + 0.04, 0], KEKC, 1.8, 0.09),
                    arrow(ecb.get_right(), dek.get_left(), DEKC, 2, 0.1))
        three = VGroup(T("Üç mesaj yeter:", 17, GOLD, BOLD), tag("Serial_Number_ONU", ONUC, 16), tag("Burst_Profile", GOLD, 16), tag("Key_Report", ONUC, 16)).arrange(RIGHT, buff=0.2)
        fit(three, 12.4).move_to([0, -2.75, 0])
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.3 §15.2.1 · §15.3 (15-2 … 15-6) · §15.5.2 · Tablo 11-27"), run_time=0.6)
        self.at(self.cue("kayıt kimliği varsayılansa", 1.0))
        self.play(FadeIn(rid, shift=RIGHT * 0.05), GrowArrow(a0), FadeIn(msk), run_time=0.6)
        self.play(FadeIn(pub, shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("Seri numarası mesajının", 6.4))
        self.play(FadeIn(sn, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("PON etiketiyle", 11.5))
        self.play(FadeIn(pt, shift=RIGHT * 0.05), run_time=0.35)
        self.play(*[GrowArrow(a) for a in a1], FadeIn(sk), run_time=0.5)
        self.at(self.cue("anahtar şifreleme anahtarı", 16.0))
        self.play(GrowArrow(a2), FadeIn(kek), run_time=0.45)
        self.at(self.cue("ikisi de AES-CMAC", 19.9))
        self.play(FadeIn(cm), FadeIn(cm2), run_time=0.35)
        self.at(self.cue("Veri anahtarı", 21.8))
        self.play(FadeIn(kr, shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("elektronik kod defteri", 26.5))
        self.play(GrowArrow(a3[0]), GrowArrow(a3[1]), FadeIn(ecb), run_time=0.5)
        self.play(GrowArrow(a3[2]), FadeIn(dek), FadeIn(dkl), run_time=0.45)
        self.at(self.cue("Üç mesaj yeter", 31.0))
        self.play(FadeIn(three[0]), run_time=0.3)
        for k, (key, d) in enumerate((("seri numarası,", 32.3), ("burst profili ve", 33.5), ("ve anahtar raporu", 34.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(three[k + 1], shift=UP * 0.05), run_time=0.3)
        self.end(pad=0.1)

        # a3 — KL3: TK3 (recommended 10 ms) → new Key_Control(Confirm); whole attempt > TK1 (100 ms) → KL0; the 2021 text named the wrong timers
        #      here and in KL1; Amd.1 fixed the names, not the values
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "Onay beklemedeki OLT'ye mevcut anahtar raporu gelmezse ne olur, ne zaman, ve Amd.1 neyi düzeltti?", CH[3])
        ks = KeySM(y_olt=-0.1, y_onu=-9.0, x0=-5.0, dx=2.5, w=2.1, h=0.78)
        row = ks.row("L")
        lp = ks.loop("L3", "TK3 · 10 ms → Key_Control(Confirm) yeniden", TMRC, True, 15)
        bk = ks.back("L", "TK1 · 100 ms · bütün deneme → KL0", WARN, 0.55, 15, False)
        rec = T("önerilen başlangıç değerleri", 15, MUTED, BOLD).next_to(lp, UP, buff=0.08)
        fx = mtable(["durum metni", "2021", "Amd.1 (2023)"], [["KL1 · istek", "TK1 ✗", "TK2 ✓"], ["KL3 · onay bekleme", "TK2 ✗", "TK3 ✓"]],
                    [3.4, 2.2, 2.6], size=17, hsize=15, row_h=0.42).move_to([-1.6, -2.55, 0])
        for r in fx[1:]:
            r[2].set_color(WARN)
            r[3].set_color(GOOD)
        vv = VGroup(T("değerler:", 16, MUTED, BOLD), T("aynı", 17, GOOD, BOLD)).arrange(RIGHT, buff=0.12).next_to(fx, RIGHT, buff=0.5)
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.3 §15.5.3.2 · Şekil 15-4 · Amd.1 (2023)"),
                  LaggedStart(*[FadeIn(b) for b in row], lag_ratio=0.1), *[GrowArrow(ks.fwd[f"L{k}"]) for k in range(4)], run_time=0.75)
        self.at(self.cue("onay bekleme zamanlayıcısı", 1.0))
        self.play(Indicate(ks.b["L3"], color=TMRC, scale_factor=1.06), run_time=0.5)
        self.at(self.cue("önerilen on milisaniye", 3.3))
        self.play(Create(lp[0]), FadeIn(lp[1]), FadeIn(rec), run_time=0.5)
        self.at(self.cue("Bütün deneme yüz", 8.8))
        self.play(FadeIn(bk[0]), Create(bk[1]), run_time=0.5)
        self.at(self.cue("hiçbir anahtarın geçerli", 15.8))
        self.play(GrowArrow(bk[2]), FadeIn(bk[3]), Indicate(ks.b["L0"], color=WARN, scale_factor=1.06), run_time=0.6)
        self.at(self.cue("yanlış zamanlayıcı adlarını", 21.5))
        self.play(FadeIn(fx[0]), *[FadeIn(r[:3], shift=RIGHT * 0.05) for r in fx[1:]], run_time=0.5)
        self.at(self.cue("birinci değişiklik adları", 27.1))
        self.play(*[FadeIn(r[3], shift=LEFT * 0.05) for r in fx[1:]], run_time=0.4)
        self.at(self.cue("değerlere dokunmadı", 30.0))
        self.play(FadeIn(vv, shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep19_recap")
