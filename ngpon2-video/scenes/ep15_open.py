"""S2·B5 — 'Bu bölümde' opening + 'Önceki bölümde' recap with the answers to the S2·B4 quiz."""
from ep15_common import *

AGENDA = ["PLOAM kanalı: taşıma, sınırlar, cevap", "Mesaj biçimi ve bütünlük kodu", "Katalog: 20 ↓ · 8 ↑ mesaj",
          "OMCC ve metindeki çelişkiler", "Laboratuvarda: yakala, çöz, doğrula"]
PX, PY = 3.4, -0.45
CX = PX + 0.2


class Ep15Open(Act15):
    MANIFEST, FIRST = M15("open"), True

    def construct(self):
        # o1 — title, agenda, cover; three management channels between OLT CT and ONU
        self.beat("o1")
        tag_ = T(f"SEZON 2 · BÖLÜM {EP15['n']} · {tr_upper(EP15['title'])}", 20, ACC, BOLD).to_corner(UL, buff=0.45)
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
        num = T(f"{EP15['n']:02d}", 110, ACC, BOLD)
        sub = fit(T(EP15["sub"], 22, TXT, SEMIBOLD), 6.0)
        refs = fit(T(EP15["refs"], 16, MUTED, MEDIUM), 6.0)
        cover = VGroup(num, sub, refs).arrange(DOWN, buff=0.25).move_to([CX, PY + 1.05, 0])
        self.play(FadeIn(num, scale=0.9), FadeIn(sub, shift=UP * 0.15), FadeIn(s2), run_time=0.5)
        self.play(FadeIn(refs), items.animate.set_opacity(0.4), run_time=0.3)
        olt = sbox("OLT CT", None, OLTC, 1.15, 1.75, 17).move_to([CX - 2.55, PY - 1.85, 0])
        onu = sbox("ONU", None, ONUC, 1.15, 1.75, 17).move_to([CX + 2.55, PY - 1.85, 0])
        ys = [PY - 1.3, PY - 1.88, PY - 2.46]
        names = [("gömülü OAM · bit alanları", MUTED), ("PLOAM · 48 B mesajlar", PLC), ("OMCC · OMCI", OMC)]
        lanes = VGroup()
        for y, (s, c) in zip(ys, names):
            ln = DoubleArrow([CX - 1.95, y - 0.1, 0], [CX + 1.95, y - 0.1, 0], buff=0, color=c, stroke_width=2.5, tip_length=0.12)
            lanes.add(VGroup(ln, T(s, 15, c, BOLD).move_to([CX, y + 0.1, 0])))
        self.at(self.cue("Gömülü alanlara", 3.4))
        self.play(FadeIn(olt), FadeIn(onu), FadeIn(lanes[0]), run_time=0.6)
        self.at(self.cue("kırk sekiz baytlık mesajlarla", 7.8))
        self.play(GrowFromCenter(lanes[1][0]), FadeIn(lanes[1][1]), run_time=0.6)
        self.at(self.cue("PLOAM.", 10.9))
        self.play(Indicate(lanes[1][1], color=PLC), run_time=0.5)
        self.at(self.cue("OMCC'de yolculuk", 15.2))
        self.play(GrowFromCenter(lanes[2][0]), FadeIn(lanes[2][1]), run_time=0.6)
        self.at(self.cue("bayt bayt", 18.5))
        self.play(lanes[0].animate.set_opacity(0.35), Indicate(VGroup(lanes[1], lanes[2]), color=ACC, scale_factor=1.04), run_time=0.7)
        self.end(pad=0.05)
        self.items, self.cur = items, VGroup(s2, cover, olt, onu, lanes)

        # o2 — PLOAM channel teaser: two transports, per-frame limits, queue of 8, 750 µs, silence
        self.beat("o2")
        tr_ = VGroup(tag("bant içi", PLC, 17), tag("AMCC · yalnızca ↑", PTPC, 17)).arrange(RIGHT, buff=0.3).move_to([CX, PY + 2.15, 0])
        fr = Rectangle(width=4.6, height=0.62, stroke_color=TW_DS, stroke_width=1.6, fill_color=TW_DS, fill_opacity=0.06).move_to([CX, PY + 1.05, 0])
        chips = VGroup(mbox("yayın ×1", BCC, 1.3), mbox("ONU 3", UCC, 0.95), mbox("ONU 7", UCC, 0.95), mbox("ONU 9", UCC, 0.95)).arrange(RIGHT, buff=0.12).move_to(fr)
        frl = T("bir 125 µs çerçeve", 15, MUTED, BOLD).next_to(fr, DOWN, buff=0.08)
        q8 = VGroup(queue(8, CNC, 8, 0.2, 0.4), T("ONU kuyruğu · 8 mesaj", 15, CNC, BOLD)).arrange(RIGHT, buff=0.25).move_to([CX, PY - 0.25, 0])
        t750 = pill("750 µs = 6 × 125 µs", GOLD, 20).move_to([CX, PY - 1.2, 0])
        sil = VGroup(T("sessizlik", 18, TXT, BOLD), T("= ?", 20, WARN, BOLD)).arrange(RIGHT, buff=0.15).move_to([CX, PY - 2.15, 0])
        self.focus(0, VGroup(tr_, fr, chips, frl, q8, t750, sil))
        self.at(self.cue("iki taşıma seçeneği", 1.5))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.08) for t in tr_], lag_ratio=0.3), run_time=0.6)
        self.at(self.cue("çerçeve başına mesaj sınırları", 3.2))
        self.play(FadeIn(fr), FadeIn(frl), LaggedStart(*[FadeIn(c, shift=DOWN * 0.06) for c in chips], lag_ratio=0.15), run_time=0.8)
        self.at(self.cue("sekiz mesajlık kuyruk", 5.8))
        self.play(FadeIn(q8, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("yedi yüz elli", 7.7))
        self.play(FadeIn(t750, scale=0.9), run_time=0.5)
        self.at(self.cue("sessizliğin", 11.3))
        self.play(FadeIn(sil, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.05)

        # o3 — the 48 bytes, SeqNo and MIC, the public key, the misspelled label
        self.beat("o3")
        bar = p48(6.0, 0.5, 15, 14, octs=False).move_to([CX, PY + 1.65, 0])
        bl = T("kırk sekiz bayt", 15, MUTED, BOLD).next_to(bar, DOWN, buff=0.3)
        gs = VGroup(glow(bar[2][0], SQC, 0.04), glow(bar[4][0], MICC, 0.04))
        key = VGroup(T("anahtar:", 16, MUTED, BOLD), HX("0x55 × 16", 22, DKC, BOLD), T("herkes bilir", 16, DKC, BOLD)).arrange(RIGHT, buff=0.2).move_to([CX, PY - 0.25, 0])
        lab = HX("PLOAMIntegrtyKey", 26, TXT, BOLD).move_to([CX, PY - 1.45, 0])
        gap = (lab[10].get_right() + lab[11].get_left()) / 2
        car = VGroup(T("^", 22, WARN, BOLD).move_to([gap[0], lab.get_bottom()[1] - 0.2, 0]),
                     T("“i” eksik", 16, WARN, BOLD).move_to([gap[0], lab.get_bottom()[1] - 0.55, 0]))
        self.focus(1, VGroup(bar, bl, gs, key, lab, car))
        self.at(self.cue("kırk sekiz baytın yerleşimi", 1.9))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in bar], lag_ratio=0.15), FadeIn(bl), run_time=0.8)
        self.at(self.cue("sıra numaraları ve", 4.2))
        self.play(Create(gs[0]), run_time=0.4)
        self.play(Create(gs[1]), run_time=0.4)
        self.at(self.cue("Herkesin bildiği bir anahtar", 7.0))
        self.play(FadeIn(key, shift=UP * 0.08), run_time=0.5)
        self.at(self.cue("bir harfi eksik", 9.6))
        self.play(FadeIn(lab), run_time=0.4)
        self.play(FadeIn(car, shift=UP * 0.08), run_time=0.4)
        self.end(pad=0.05)

        # o4 — catalogue: 20 down, 8 up, nine families, the season-1 optical tables
        self.beat("o4")
        cnt = VGroup(pill("↓ 20 tür", TXT, 22), pill("↑ 8 tür", TXT, 22)).arrange(RIGHT, buff=0.4).move_to([CX, PY + 2.05, 0])
        fams = [("Profiller", "prof"), ("Kimlikler", "kim"), ("Devre dışı", "dis"), ("Anahtarlar", "key"), ("Uyku", "pm"),
                ("Ayar", "tun"), ("Koruma", "prot"), ("Güç seviyesi", "pwr"), ("Hız", "rate")]
        ft = VGroup(*[tile(s, FAM[f], 1.85, 0.48, 16, 0.18) for s, f in fams])
        for i, t in enumerate(ft):
            t.move_to([CX - 2.0 + 2.0 * (i % 3), PY + 0.95 - 0.66 * (i // 3), 0])
        s1 = pill("S1 · G.989.2 optik tabloları", S1C, 17).move_to([CX, PY - 1.95, 0])
        s1a = VGroup(*[Line([s1.get_x() + dx, s1.get_top()[1] + 0.05, 0], [s1.get_x() + dx * 1.6, PY - 1.0, 0], color=S1C, stroke_width=1.5)
                       for dx in (-1.2, 0, 1.2)])
        self.focus(2, VGroup(cnt, ft, s1, s1a))
        self.at(self.cue("aşağı yönde yirmi", 1.5))
        self.play(FadeIn(cnt[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("yukarı yönde sekiz", 3.0))
        self.play(FadeIn(cnt[1], shift=UP * 0.08), run_time=0.4)
        keys = ["Profiller", "kimlikler", "devre dışı", "anahtarlar", "uyku", "ayar", "koruma", "güç seviyesi", "ve hız"]
        defs = [5.2, 6.0, 6.9, 8.6, 9.5, 9.9, 10.4, 11.0, 12.0]
        for k, (key, d) in enumerate(zip(keys, defs)):
            self.at(self.cue(key, d))
            self.play(FadeIn(ft[k], shift=UP * 0.06), run_time=0.3)
        self.at(self.cue("optik tablolarına", 13.5))
        self.play(FadeIn(s1, shift=UP * 0.08), *[Create(a) for a in s1a], run_time=0.6)
        self.end(pad=0.05)

        # o5 — OMCC teaser: OMCI inside XGEM, its own 4-byte MIC, G.988, conflicts
        self.beat("o5")
        st = strip([(1.2, "XGEM başlığı · 8 B", SAC, 0.55), (3.6, "OMCI mesajı · 48 B", OMC, 0.2), (0.8, "MIC 4 B", MICC, 0.45)], CX - 2.8, PY + 1.6, 0.6, 14)
        pid = T("Port-ID = ONU-ID", 16, PIDC, BOLD).next_to(st[0], UP, buff=0.12)
        mg = glow(st[2], MICC, 0.04)
        dc = doc_card("G.988", ["OMCI'ın anlamı"], GOLD, 2.4, 1.2, 19, 15).move_to([CX - 1.4, PY - 0.35, 0])
        dl = T("burada anlatılmaz", 15, MUTED, BOLD).next_to(dc, RIGHT, buff=0.3)
        cf = VGroup(*[tag("çelişki", WARN, 16) for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to([CX, PY - 2.0, 0])
        self.focus(3, VGroup(st, pid, mg, dc, dl, cf))
        self.at(self.cue("XGEM içinde", 1.0))
        self.play(FadeIn(st[:2], shift=RIGHT * 0.08), FadeIn(pid), run_time=0.6)
        self.at(self.cue("kendi bütünlük kodu", 4.0))
        self.play(FadeIn(st[2]), Create(mg), run_time=0.5)
        self.at(self.cue("G.988'e bırakılanlar", 5.7))
        self.play(FadeIn(dc, shift=UP * 0.08), FadeIn(dl), run_time=0.5)
        self.at(self.cue("çelişkiler", 8.5))
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cf], lag_ratio=0.2), run_time=0.6)
        self.end(pad=0.05)

        # o6 — lab: analyzer + OLT and ONU emulators; capture, MIC without secrets, golden vectors, SeqNo, keep-alive
        self.beat("o6")
        pa = pa_icon(1.85, 1.3, "Analizör").move_to([CX - 2.1, PY + 1.35, 0])
        e1 = emu_icon(1.85, 1.3, "OLT emülatörü").move_to([CX, PY + 1.35, 0])
        e2 = emu_icon(1.85, 1.3, "ONU emülatörü").move_to([CX + 2.1, PY + 1.35, 0])
        ts = VGroup(tag("yakala · çöz", GOOD, 16), tag("yayın MIC'i · sır yok", DKC, 16), tag("altın vektörler", GOLD, 16),
                    tag("sıra numaraları", SQC, 16), tag("canlılık onayı", ACC, 16))
        ts[:2].arrange(RIGHT, buff=0.2).move_to([CX, PY - 0.55, 0])
        ts[2:].arrange(RIGHT, buff=0.2).move_to([CX, PY - 1.45, 0])
        self.focus(4, VGroup(pa, e1, e2, ts))
        self.play(FadeIn(pa, shift=UP * 0.1), FadeIn(e1, shift=UP * 0.1), FadeIn(e2, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("yakalayıp çözeceğiz", 1.5))
        self.play(FadeIn(ts[0], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("sır bilmeden", 5.5))
        self.play(FadeIn(ts[1], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("altın vektörlerle", 9.0))
        self.play(FadeIn(ts[2], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("sıra numaralarıyla", 10.7))
        self.play(FadeIn(ts[3], shift=UP * 0.08), run_time=0.4)
        self.at(self.cue("canlılık onaylarıyla", 12.3))
        self.play(FadeIn(ts[4], shift=UP * 0.08), run_time=0.4)
        self.end(pad=0.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.wait(0.3)
        self.save_timeline("ep15_open")

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


class Ep15Recap(Act15):
    HDR, MANIFEST, FIRST = f"SEZON 2 · BÖLÜM {K15} · ÖNCEKİ BÖLÜMDE", M15("recap"), True

    def qhead(self, n, text, color):
        g = VGroup(T(f"Soru {n}", 24, color, BOLD), T(text, 25, TXT, SEMIBOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(g, 12.6)
        return g.to_edge(LEFT, buff=0.8).set_y(2.2)

    def construct(self):
        # a1 — BE gets nothing while an NA Alloc-ID is unsaturated: strict hierarchy; BE guaranteed part may be zero
        self.beat("a1")
        tc = self.title_card("ÖNCEKİ BÖLÜMDE", "Sezon 2 · Bölüm 4 · Paylaşım")
        self.at(self.cue("Birinci soru", 1.9))
        self.to_header(tc)
        self.set_badge("ozet")
        q1 = self.qhead(1, "En iyi çaba T-CONT'u hiç pay alamıyor, güvencesiz T-CONT hâlâ doymamış: OLT bozuk mu?", CH[0])
        x0, W = -5.0, 5.6
        levels = [("1 · sabit", FXC, 1.0), ("2 · güvenceli", ASC, 1.0), ("3 · güvencesiz", NAC, 0.62), ("4 · en iyi çaba", BEC, 0.0)]
        rows = VGroup()
        for i, (s, c, f) in enumerate(levels):
            y = 0.75 - 0.62 * i
            lb = T(s, 17, c, BOLD).move_to([x0 - 0.15, y, 0], aligned_edge=RIGHT)
            fr = Rectangle(width=W, height=0.4, stroke_color=c, stroke_width=1.6).move_to([x0 + W / 2 + 0.05, y, 0])
            fl = Rectangle(width=max(W * f, 0.02), height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.5 if f else 0).move_to([x0 + 0.05 + max(W * f, 0.02) / 2, y, 0])
            rows.add(VGroup(lb, fr, fl))
        rows.shift(RIGHT * 0.9)
        nas = T("doymamış", 15, NAC, BOLD).next_to(rows[2][2], RIGHT, buff=0.15)
        be0 = T("pay = 0", 16, BEC, BOLD).next_to(rows[3][1].get_left(), RIGHT, buff=0.2)
        cap = T("kapasite bitti", 15, WARN, BOLD).next_to(rows[2][1], RIGHT, buff=0.2)
        ans = VGroup(T("Hayır.", 30, GOOD, BOLD), T("katı öncelik sırası", 18, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 0.6, 0])
        rule = VGroup(T("en iyi çaba ek payı ←", 17, BEC, BOLD), T("bütün güvencesiz Alloc-ID'ler doyunca", 17, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rule.move_to([0.0, -2.0, 0]).align_to(rows, LEFT)
        inv = VGroup(HX("χAB = BE ⇒ RM > RF + RA ≥ 0", 19, TXT, BOLD), T("garantili pay sıfır olabilir", 17, GOOD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        inv.move_to([3.6, -2.0, 0])
        self.play(FadeIn(q1, shift=RIGHT * 0.2), self.set_src("G.989.3 §7.3.3 · §7.3.5 · (7-2)"), run_time=0.6)
        self.at(self.cue("en iyi çaba T-CONT'u hiç", 3.1))
        self.play(FadeIn(rows[3][:2]), FadeIn(be0), run_time=0.5)
        self.at(self.cue("güvencesiz bir T-CONT", 6.3))
        self.play(FadeIn(rows[2][:2]), GrowFromEdge(rows[2][2], LEFT), FadeIn(nas), run_time=0.6)
        self.at(self.cue("Hayır.", 10.0))
        self.play(FadeIn(ans[0], scale=0.9), run_time=0.4)
        self.at(self.cue("katı bir sıra izler", 11.0))
        self.play(FadeIn(ans[1]), run_time=0.4)
        for k, (key, d) in enumerate((("sabit,", 14.0), ("güvenceli,", 14.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2]), GrowFromEdge(rows[k][2], LEFT), run_time=0.35)
        self.at(self.cue("güvencesiz,", 15.4))
        self.play(Indicate(rows[2][0], color=NAC), FadeIn(cap), run_time=0.5)
        self.at(self.cue("en son en iyi çaba", 16.3))
        self.play(Indicate(rows[3][0], color=BEC), run_time=0.5)
        self.at(self.cue("En iyi çaba ek payı", 17.9))
        self.play(FadeIn(rule[0], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("doyunca gelir", 22.0))
        self.play(FadeIn(rule[1], shift=RIGHT * 0.08), run_time=0.4)
        self.at(self.cue("garantili pay sıfır", 26.0))
        self.play(FadeIn(inv[0], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("tasarımın kendisidir", 31.3))
        self.play(FadeIn(inv[1], shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.1)

        # a2 — the time quantum: 125 µs / 9720; 4 B or 16 B; 32 or 128 bit per frame → 256 kbit/s or 1,024 Mbit/s; 16 B minimum
        self.beat("a2")
        self.clear()
        q2 = self.qhead(2, "Bir zaman kuantumu kaç bayt, çerçeve başına kaç bit/s eder; en küçük yük tahsisi ne?", CH[1])
        fr = VGroup(*[Rectangle(width=0.2, height=0.42, stroke_color=TIMC, stroke_width=1, fill_color=TIMC, fill_opacity=0.08 + 0.06 * (i % 2)) for i in range(40)]).arrange(RIGHT, buff=0)
        fr.move_to([-1.6, 0.85, 0])
        frb = brace_lbl(fr, "125 µs = 9720 kuantum", TIMC, UP, 16)
        one = Rectangle(width=0.2, height=0.42, stroke_width=0, fill_color=GOLD, fill_opacity=0.8).move_to(fr[0])
        onel = T("1 kuantum = 12,86 ns", 16, GOLD, BOLD).next_to(fr, RIGHT, buff=0.3)
        tb = mtable(["↑ hız", "1 kuantum", "bit / çerçeve", "× 8000 çerçeve/s", "en küçük yük"],
                    [["2,5G", "4 B", "32 bit", "256 kbit/s", "16 B · GrantSize 4"], ["10G", "16 B", "128 bit", "1,024 Mbit/s", "16 B · GrantSize 1"]],
                    [1.4, 1.7, 2.0, 2.7, 3.3], size=18, hsize=16, row_h=0.52).move_to([0, -0.85, 0])
        nt = VGroup(tag("2,5G · GrantSize 1", BWC, 16), T("= yalnızca DBRu", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.55, 0])
        cols = lambda k: [r[k + 1] for r in tb[1:]]
        self.play(FadeIn(q2, shift=RIGHT * 0.2), self.set_src("G.989.3 §8.1.1.2.3–4 · hesap"), run_time=0.6)
        self.at(self.cue("zaman kuantumu", 1.0))
        self.play(LaggedStart(*[FadeIn(c) for c in fr], lag_ratio=0.02), run_time=0.8)
        self.at(self.cue("dokuz bin yedi yüz", 2.4))
        self.play(FadeIn(frb), FadeIn(one), FadeIn(onel, shift=LEFT * 0.06), run_time=0.6)
        self.at(self.cue("iki buçuk gigabitte dört", 7.6))
        self.play(FadeIn(tb[0]), *[FadeIn(r[0]) for r in tb[1:]], FadeIn(tb[1][1]), FadeIn(tb[1][2]), run_time=0.5)
        self.at(self.cue("on gigabitte on altı", 9.7))
        self.play(FadeIn(tb[2][1]), FadeIn(tb[2][2]), run_time=0.4)
        self.at(self.cue("Çerçeve başına otuz iki", 11.9))
        self.play(*[FadeIn(m, shift=UP * 0.05) for m in cols(2)], run_time=0.4)
        self.at(self.cue("saniyede sekiz bin", 16.1))
        self.play(*[FadeIn(m, shift=UP * 0.05) for m in cols(3)], run_time=0.4)
        self.at(self.cue("En küçük yük tahsisi", 24.3))
        self.play(*[FadeIn(m, shift=UP * 0.05) for m in cols(4)], run_time=0.4)
        self.at(self.cue("tek kuantumluk tahsis", 28.6))
        self.play(FadeIn(nt, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.1)

        # a3 — Annex J only: idle-ONU-support allocation → one Acknowledgement, code 0x06, Busy Alloc-ID (0xC0 = all)
        self.beat("a3")
        self.clear()
        q3 = self.qhead(3, "Yalnızca Ek J varsa: boştaki ONU, T-CONT'unun tahsislerini nasıl geri ister?", CH[3])
        conds = VGroup(*[chk(s, True, 17) for s in ("O5 durumunda", "T-CONT'una yönlendirilmiş tahsis yok", "trafiği var",
                                                     "zaman aşımı içinde başka çekişmeli tahsise cevap vermedi")]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        conds.move_to([-3.6, 0.35, 0])
        cl = T("uygun ONU", 16, MUTED, BOLD).next_to(conds, UP, buff=0.15).align_to(conds, LEFT)
        ca = tile("boştaki ONU desteği · işlev 0x03", GOLD, 4.2, 0.5, 16, 0.18).move_to([-3.5, -1.55, 0])
        p = apanel(5.6, 2.6, "Acknowledgement · tek PLOAM", ACC).move_to([3.4, 0.45, 0])
        rows = VGroup(kv("Completion", "0x06", kw=2.1), kv("anlamı", "istenmemiş trafik", kw=2.1), kv("Busy Alloc-ID", "oktet 8–9", kw=2.1),
                      kv("oktet 8 = 0xC0", "hepsi", kw=2.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rows.move_to(p[0]).shift(DOWN * 0.2)
        rows[0][1].set_color(GOLD)
        rows[3][1].set_color(GOOD)
        ar = arrow(ca.get_right(), p[0].get_left() + DOWN * 0.6, ACC, 2.2, 0.12)
        back = VGroup(T("OLT", 18, OLTC, BOLD), T("→ tahsisleri geri verir", 18, GOOD, BOLD)).arrange(RIGHT, buff=0.15).move_to([3.4, -1.6, 0])
        self.play(FadeIn(q3, shift=RIGHT * 0.2), self.set_src("G.989.3 Ek J · Tablo J.1 · Tablo J.3"), run_time=0.6)
        self.at(self.cue("O5'teki", 2.8))
        self.play(FadeIn(cl), FadeIn(conds[0], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("T-CONT'una yönlendirilmiş", 3.5))
        self.play(FadeIn(conds[1], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("trafiği olan", 7.2))
        self.play(FadeIn(conds[2], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("zaman aşımı içinde", 9.0))
        self.play(FadeIn(conds[3], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("boştaki ONU desteği", 14.1))
        self.play(FadeIn(ca, shift=UP * 0.08), run_time=0.4)
        self.play(GrowArrow(ar), FadeIn(p), run_time=0.5)
        self.at(self.cue("tamamlama kodu altı", 18.9))
        self.play(FadeIn(rows[0], shift=RIGHT * 0.06), run_time=0.35)
        self.at(self.cue("istenmemiş trafik", 20.6))
        self.play(FadeIn(rows[1], shift=RIGHT * 0.06), run_time=0.35)
        self.at(self.cue("meşgul tahsis kimliği", 23.0))
        self.play(FadeIn(rows[2], shift=RIGHT * 0.06), run_time=0.35)
        self.at(self.cue("ce sıfır ise hepsi", 25.1))
        self.play(FadeIn(rows[3], shift=RIGHT * 0.06), run_time=0.35)
        self.at(self.cue("OLT tahsisleri geri verir", 28.3))
        self.play(FadeIn(back, shift=UP * 0.08), run_time=0.5)
        self.end(pad=0.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.save_timeline("ep15_recap")
