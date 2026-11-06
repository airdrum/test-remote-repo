"""B03 · Perde 5 (kanal profilleri), Laboratuvarda, Kapanış."""
from ep03_common import *

PROF = "#A78BFA"
OCT = [("1–2", "ONU-ID 0x03FF", "h"), ("3", "tip 0x18", "h"), ("4", "SeqNo", "h"), ("5", "CCCC 0TDU", "c"), ("6", "sürüm VVVV", "c"),
       ("7–10", "PON-ID", "c"), ("11", "↓ frekans kayması", "d"), ("12", "↓ hız 00SE LLLL", "d"), ("13", "kanal bölümü", "d"),
       ("14–17", "varsayılan yanıt kanalı", "d"), ("18", "SN grant tipi", "d"), ("19–22", "AMCC penceresi", "d"), ("23", "UWLCH ID", "u"),
       ("24–27", "↑ frekans", "u"), ("28", "bağlantı tipi 00AB", "u"), ("29", "↑ hız 00HL", "u"), ("30", "varsayılan zayıflatma", "u"),
       ("31", "yanıt eşiği", "u"), ("32", "klon yapılandırma", "x"), ("33–40", "dolgu", "x"), ("41–48", "MIC", "x")]
GC = {"h": MUTED, "c": GOLD, "d": TW_DS, "u": TW_US, "x": MUTED}


def octet_map():
    cells = VGroup()
    for o, name, g in OCT:
        r = RoundedRectangle(corner_radius=0.06, width=3.05, height=0.42, stroke_color=GC[g], stroke_width=2, fill_color=PANEL, fill_opacity=1)
        t = VGroup(T(o, 13, GC[g], BOLD), T(name, 13, TXT)).arrange(RIGHT, buff=0.15)
        t.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.12)
        cells.add(VGroup(r, t))
    cols = [cells[i:i + 7] for i in range(0, 21, 7)]
    for c in cols:
        VGroup(*c).arrange(DOWN, buff=0.08)
    VGroup(*[VGroup(*c) for c in cols]).arrange(RIGHT, buff=0.2, aligned_edge=UP)
    return cells


class E3P5A(Act3):
    HDR, MANIFEST, FIRST = H3[5], M3("p5"), True

    def construct(self):
        self.beat("f1")
        tc = self.title_card("PERDE 5", "Kanal profilleri")
        self.at(self.cue("Yeni açılan", 2))
        self.to_header(tc)
        self.set_badge("tc")
        h = self.show_heading("Profil duyurusu — G.989.3 §17.1")
        q = pill("yeni açılan ONU haritayı bilmez", GOLD, 22).move_to(UP * 1.4)
        tl = Line([-6.0, -0.6, 0], [6.0, -0.6, 0], color=MUTED, stroke_width=2)
        frames = VGroup(*[Rectangle(width=0.95, height=0.5, stroke_color=TW_DS, stroke_width=1.5, fill_color=TW_DS, fill_opacity=0.08).move_to([-5.5 + i * 1.0, -0.3, 0]) for i in range(12)])
        pl = VGroup(*[Rectangle(width=0.32, height=0.26, stroke_width=0, fill_color=PROF, fill_opacity=0.9).move_to([-5.5 + i * 1.0, -0.3, 0]) for i in (0, 4, 8)])
        cap = T("onaysız yayın PLOAM · her ↓ kanalda · periyodik", 20, PROF, BOLD).move_to(DOWN * 1.6)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.at(self.cue("G.989.3'ün", 3))
        self.play(Create(tl), FadeIn(frames), self.set_src("G.989.3 §17.1"), run_time=0.8)
        self.at(self.cue("her aşağı yön", 4))
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pl], lag_ratio=0.3), FadeIn(cap), run_time=0.9)
        self.end(pad=0.05)

        self.beat("f1a")
        self.clear(h)
        cols = [("System_Profile", "× 1", "sistem geneli", GOLD), ("Channel_Profile", "× ≤ 8", "her kanal çifti", PROF), ("Burst_Profile", "× ≤ 8 / kanal  (≤ 64)", "BWmap'in kullandığı", TW_DS)]
        cards = VGroup(*[card(n, f"{c}\n{d}", None, col, w=3.9, h=1.9, tsize=22, bsize=19) for n, c, d, col in cols]).arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        per = T("periyot T_minProfile: 1 … 5 s", 24, GOOD, BOLD).move_to(DOWN * 1.7)
        for i, key in enumerate(["tek bir sistem", "her kanal çifti", "her burst"]):
            self.at(self.cue(key, 1 + 2 * i))
            self.play(FadeIn(cards[i], shift=UP * 0.15), run_time=0.5)
        self.at(self.cue("Bütün set", 6))
        self.play(FadeIn(per), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f2")
        self.clear(h)
        h = self.show_heading("Sistem profili (Tablo 17-1)", h)
        rows = [["kanal sayısı", "farklı profil kimliği olan kanal adedi"], ["↑ kanal aralığı", "tasarım ızgarası — dağıtım değil"], ["MSE", "1 GHz birimi"],
                ["FSR", "döngüsel WM varsa · 0,1 GHz birimi · yoksa 0x0000"], ["↑ bant seçeneği", "geniş · azaltılmış · dar"], ["kalibrasyon doğruluğu", "bant içi aktivasyon için en az"],
                ["gevşek kalibrasyon sınırı", "OLT belirler (WM'ye bağlı)"], ["AMCC kullanım bayrağı", "aktivasyon için AMCC var mı"]]
        tb = table(["Parametre", "Anlamı"], rows, [4.0, 7.2], size=19, hsize=16, row_h=0.47).move_to(DOWN * 0.35)
        self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[1:7]], lag_ratio=0.15), self.set_src("G.989.3 Tablo 17-1"), run_time=1.4)
        self.at(self.cue("Burada önemli", 3))
        self.play(Indicate(tb[2], color=GOLD, scale_factor=1.0), run_time=0.9)
        self.end(pad=0.05)

        self.beat("f2a")
        self.play(FadeIn(tb[7], shift=UP * 0.05), FadeIn(tb[8], shift=UP * 0.05), run_time=0.5)
        hl = SurroundingRectangle(tb[7], color=GOLD, buff=0.03)
        self.play(Create(hl), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f2b")
        self.clear(h)
        h = self.show_heading("Kalibrasyon doğruluğu ve AMCC", h)
        a = card("kalibre ONU", "sistem profilindeki doğruluğu sağlar\n→ bant içi aktivasyon", None, GOOD, w=5.2, h=1.9, tsize=24, bsize=19)
        b = card("yeterince kalibre değil", "→ AMCC üzerinden aktivasyon", None, WARN, w=5.2, h=1.9, tsize=24, bsize=19)
        VGroup(a, b).arrange(RIGHT, buff=0.4).move_to(UP * 0.5)
        o18 = VGroup(T("Channel_Profile · oktet 18 · 0000 00IA", 21, PROF, BOLD), T("I: bant içi SN grant · A: AMCC SN grant sunuluyor mu?", 19, TXT)).arrange(DOWN, buff=0.12).move_to(DOWN * 1.6)
        self.play(FadeIn(a, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Bunu sağlamayan", 2))
        self.play(FadeIn(b, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Kanal profilindeki", 3))
        self.play(FadeIn(o18, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_p5A")


class E3P5B(Act3):
    HDR, MANIFEST, PREV_BADGE = H3[5], M3("p5"), "tc"

    def construct(self):
        self.beat("f3")
        h = self.show_heading("Channel_Profile mesajı — TWDM (Tablo 11-18)")
        om = octet_map().move_to(DOWN * 0.45)
        leg = VGroup(T("■ ortak", 16, GOLD), T("■ ↓ tanımı", 16, TW_DS), T("■ ↑ tanımı", 16, TW_US)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.75)
        self.play(LaggedStart(*[FadeIn(c) for c in om], lag_ratio=0.03), FadeIn(leg), self.set_src("G.989.3 §11.3.3.14"), run_time=1.6)
        self.at(self.cue("Başında", 1))
        self.play(Indicate(om[3], color=GOLD, scale_factor=1.05), run_time=0.8)
        self.at(self.cue("Ardından profil", 3))
        self.play(Indicate(om[4], color=GOLD, scale_factor=1.05), run_time=0.8)
        self.end(pad=0.05)

        self.beat("f3a")
        self.play(*[c.animate.set_opacity(0.25) for i, c in enumerate(om) if OCT[i][2] not in ("d", "u")], run_time=0.5)
        self.play(*[Indicate(om[i], color=TW_DS, scale_factor=1.03) for i in (5, 6, 7)], run_time=0.8)
        self.at(self.cue("Yukarı yön tanımında", 2))
        self.play(*[Indicate(om[i], color=TW_US, scale_factor=1.03) for i in (12, 13)], run_time=0.8)
        self.end(pad=0.05)

        self.beat("f3b")
        self.clear(h)
        h = self.show_heading("İki oktet yakından", h)
        def bits(b, cols):
            cells = VGroup(*[VGroup(Square(0.7, stroke_color=c, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), T(x, 24, c, BOLD)) for x, c in zip(b, cols)])
            for c in cells:
                c[1].move_to(c[0])
            return cells.arrange(RIGHT, buff=0.06)
        o11 = VGroup(T("oktet 11 · ↓ frekans kayması", 20, TW_DS, BOLD), bits("10000000", [WARN] + [MUTED] * 7), T("= bilinmiyor", 20, WARN, BOLD)).arrange(RIGHT, buff=0.35).move_to(UP * 0.9)
        o12 = VGroup(T("oktet 12 · ↓ hız", 20, TW_DS, BOLD), bits("00SELLLL", [MUTED, MUTED, TW_DS, GOLD, ACC, ACC, ACC, ACC]),
                     T("S hız · E FEC · LLLL kod", 18, TXT)).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.8)
        self.play(FadeIn(o11, shift=UP * 0.1), run_time=0.6)
        self.at(self.cue("Aşağı yön hız", 2))
        self.play(FadeIn(o12, shift=UP * 0.1), run_time=0.6)
        self.end(pad=0.05)

        self.beat("f4")
        self.clear(h)
        h = self.show_heading("Örnek: profili okumak", h)
        steps = VGroup(VGroup(T("dinlenen ↓ kanal", 20, MUTED), T("187,7 THz", 30, TW_DS, BOLD)),
                       VGroup(T("PON-ID son 4 bit", 20, MUTED), T("0001 → kanal 2", 30, TW_DS, BOLD)),
                       VGroup(T("↑ frekans alanı", 20, MUTED), T("1 955 000", 30, TW_US, BOLD)),
                       VGroup(T("× 0,1 GHz", 20, MUTED), T("195,5 THz ≈ 1533,47 nm", 30, TW_US, BOLD)))
        for s in steps:
            s.arrange(DOWN, buff=0.1)
        steps.arrange(DOWN, buff=0.35).move_to(DOWN * 0.3)
        keys = ["ONU, yüz", "Çerçevedeki", "Kendi kanalının", "Sıfır virgül bir"]
        for s, key in zip(steps, keys):
            self.at(self.cue(key, 0))
            self.play(FadeIn(s, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f4a")
        self.clear(h)
        h = self.show_heading("Bağlantı tipi ve varsayılan zayıflatma", h)
        c1 = card("oktet 28 · 0000 00AB", "A: A tipi destekli (yükselteçsiz)\nB: B tipi destekli (yükselteçli)", "Bölüm 2, Perde 3", TW_US, w=5.6, h=2.1, tsize=22, bsize=18)
        c2 = card("oktet 30 · 0000 MMMM", "0000: zayıflatma yok\n0001 … 0111: 3 dB adımlar (3 … 21 dB)", "ilk yanıtta ONU gücünü kısar", GOLD, w=5.6, h=2.1, tsize=22, bsize=18)
        VGroup(c1, c2).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Bir de varsayılan", 3))
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.05)

        self.beat("f4b")
        self.clear(h)
        h = self.show_heading("Burst profilleri", h)
        bp = card("Burst_Profile", "önsöz uzunluğu ve deseni · sınırlayıcı · FEC\nBWmap her burst için bir profil seçer", "→ Bölüm 6: ONU vericisi ve burst modu", TW_DS, w=9.0, h=2.2, tsize=26, bsize=20).move_to(DOWN * 0.2)
        self.play(FadeIn(bp, shift=UP * 0.15), run_time=0.7)
        self.end(pad=0.05)

        self.beat("f5")
        self.clear(h)
        h = self.show_heading("↓ / ↑ kanal eşlemesi", h)
        def mapping(x, links, title, color):
            ds = VGroup(*[box(1.0, 0.42, f"↓{i + 1}", TW_DS, 15).move_to([x - 1.3, 1.0 - i * 0.65, 0]) for i in range(4)])
            us = VGroup(*[box(1.0, 0.42, f"↑{i + 1}", TW_US, 15).move_to([x + 1.3, 1.0 - i * 0.65, 0]) for i in range(4)])
            ln = VGroup(*[Line(ds[a].get_right(), us[b].get_left(), color=color, stroke_width=2.5) for a, b in links])
            return VGroup(ds, us, ln, T(title, 20, color, BOLD).next_to(VGroup(ds, us), UP, buff=0.3))
        m1 = mapping(-3.4, [(0, 0), (1, 1), (2, 2), (3, 3)], "sabit 1 : 1", GOOD)
        m2 = mapping(3.4, [(0, 0), (1, 0), (2, 2), (2, 3), (3, 1)], "esnek: çoğa bir · bire çok", GOLD)
        cap = T("varsayılan yanıt kanalı + Tuning_Control mesajı", 20, MUTED).to_edge(DOWN, buff=0.85)
        self.play(FadeIn(m1[0]), FadeIn(m1[1]), FadeIn(m1[3]), Create(m1[2]), run_time=0.9)
        self.at(self.cue("Ama standart", 2))
        self.play(FadeIn(m2[0]), FadeIn(m2[1]), FadeIn(m2[3]), Create(m2[2]), run_time=0.9)
        self.at(self.cue("eşlemeyi", 4))
        self.play(FadeIn(cap), run_time=0.5)
        self.end(pad=0.05)

        self.beat("f5a")
        self.clear(h)
        h = self.show_heading("PtP WDM kanal profili (Tablo 11-19)", h)
        eng = card("engaged bayrağı", "kanal bir ONU ile eşleşti →\nartık başka ONU'lara kapalı", "G.989.3 Tablo 17-2", PTP, w=7.0, h=2.2, tsize=26, bsize=21).move_to(UP * 0.3)
        b9 = T("→ PtP WDM: Bölüm 9", 21, ACC, BOLD).next_to(eng, DOWN, buff=0.5)
        self.play(FadeIn(eng, shift=UP * 0.15), run_time=0.6)
        self.at(self.cue("Noktadan noktaya WDM'i", 3))
        self.play(FadeIn(b9), run_time=0.4)
        self.end(pad=0.05)

        self.engineer_note("f6", [("1", "Fizik ile TC'nin buluştuğu yer", "Ölçülen ≠ duyurulan frekans → kalibrasyon ya da konfigürasyon.", 1),
                                  ("2", "Analizör + OSA", "Profil duyurularını yakalayın, OSA ölçümüyle karşılaştırın.", 2)])
        self.beat("f7")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "Bu haritayı laboratuvarda görelim.")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.7)
        self.end(pad=0.3)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep03_p5B")


class E3LabA(Act3):
    HDR, MANIFEST, FIRST = H3["L"], M3("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Kanal haritası ve yalıtım")
        self.at(self.cue("Bu bölümün", 2))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("İki soru")
        qs = VGroup(card("Kanallar yerinde mi?", "frekans · sapma · güç yoğunluğu", None, TW_DS, w=5.4, h=1.7, tsize=26, bsize=19),
                    card("Komşular ayrık mı?", "WM / CEx yalıtımı · Raman", None, GOLD, w=5.4, h=1.7, tsize=26, bsize=19)).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.2)
        self.play(FadeIn(qs[0], shift=UP * 0.15), run_time=0.5)
        self.at(self.cue("komşu sistemler", 4))
        self.play(FadeIn(qs[1], shift=UP * 0.15), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Kurulum: S/R-CG'de spektrum", h)
        cts = VGroup(*[box(0.9, 0.38, f"CT{i + 1}", CH[i], 13).move_to([-6.0, 1.0 - i * 0.52, 0]) for i in range(4)])
        wm = box(0.7, 2.2, "WM", "#3B4A75", 15).move_to([-4.7, 0.2, 0])
        l1 = VGroup(*[Line(c.get_right(), [wm.get_left()[0], c.get_y(), 0], color=FEED, stroke_width=2) for c in cts])
        cg = DashedLine([-3.9, -1.1, 0], [-3.9, 1.6, 0], color=ACC, stroke_width=2)
        cgt = T("S/R-CG", 15, ACC, BOLD).next_to(cg, UP, buff=0.05)
        cpl = box(1.2, 0.7, "kuplör", MUTED, 15).move_to([-2.8, 0.2, 0])
        f1 = Line(wm.get_right(), cpl.get_left(), color=FEED, stroke_width=3)
        odn = VGroup(Line(cpl.get_right(), [0.4, 0.2, 0], color=FEED, stroke_width=3), box(1.3, 0.6, "ODN", FEED, 15).move_to([1.05, 0.2, 0]),
                     Line([1.7, 0.2, 0], [2.4, 0.2, 0], color=FEED, stroke_width=3), box(1.0, 0.6, "ONU", "#94A3B8", 15).move_to([2.9, 0.2, 0]))
        osa = instrument("OSA", 2.3, 1.7).move_to([4.8, -1.4, 0])
        taps = VGroup(Line(cpl.get_bottom(), [cpl.get_x(), -1.4, 0], color=GOLD, stroke_width=2), Line([cpl.get_x(), -1.4, 0], osa.get_left(), color=GOLD, stroke_width=2))
        tt = T("↓ ve ↑ ayrı kollardan", 16, GOLD, BOLD).next_to(taps[1], UP, buff=0.08)
        self.play(FadeIn(cts), Create(l1), FadeIn(wm), run_time=0.7)
        self.play(Create(cg), FadeIn(cgt), Create(f1), FadeIn(cpl), FadeIn(odn), run_time=0.8)
        self.at(self.cue("Burada bütün", 3))
        self.play(Create(taps), FadeIn(osa), run_time=0.7)
        self.at(self.cue("bir yönlü kuplörle", 4))
        self.play(FadeIn(tt), run_time=0.4)
        self.end(pad=0.05)

        self.beat("g3")
        self.clear(h)
        h = self.show_heading("Çözünürlük bant genişliği düzeltmesi", h)
        lines = VGroup(T("PSD sınırları: dBm / 15 GHz", 26, TXT, BOLD), T("RBW 0,1 nm @ 1598 nm  →  Δf = c · Δλ / λ² ≈ 11,75 GHz", 26, ACC, BOLD),
                       T("düzeltme = 10 · log(15 / 11,75) ≈ + 1,06 dB", 30, GOLD, BOLD)).arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        self.play(FadeIn(lines[0]), run_time=0.5)
        self.at(self.cue("OSA'da", 2))
        self.play(FadeIn(lines[1]), run_time=0.6)
        self.at(self.cue("Okuduğunuz", 4))
        self.play(FadeIn(lines[2]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g4")
        self.clear(h)
        h = self.show_heading("Frekans doğruluğu", h)
        k = 0.016
        b1 = VGroup(T("↓ MSE ± 20 GHz @ 1600 nm", 20, TW_DS, BOLD), Rectangle(width=340 * k, height=0.5, stroke_width=0, fill_color=TW_DS, fill_opacity=0.8), T("± 170 pm", 22, TW_DS, BOLD)).arrange(RIGHT, buff=0.3)
        b2 = VGroup(T("tipik OSA doğruluğu", 20, GOLD, BOLD), Rectangle(width=40 * k, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.8), T("± 10 … 20 pm", 22, GOLD, BOLD)).arrange(RIGHT, buff=0.3)
        VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.4)
        c = T("yeterli — ama referans kaynakla düzenli doğrulayın", 22, GOOD, BOLD).move_to(DOWN * 1.6)
        self.play(FadeIn(b1[0]), GrowFromEdge(b1[1], LEFT), FadeIn(b1[2]), run_time=0.7)
        self.at(self.cue("Tipik bir OSA", 2))
        self.play(FadeIn(b2[0]), GrowFromEdge(b2[1], LEFT), FadeIn(b2[2]), run_time=0.7)
        self.at(self.cue("Ama OSA'yı", 4))
        self.play(FadeIn(c), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g4a")
        self.play(*[FadeOut(m) for m in (b1, b2, c)], run_time=0.4)
        ref = VGroup(box(2.2, 0.7, "referans lazer", GOLD, 16), Arrow(LEFT, RIGHT, color=MUTED), instrument("OSA", 2.0, 1.45), T("eksen doğrulaması", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.3).move_to(UP * 0.7)
        cmp_ = VGroup(T("ölçülen ↓ frekans", 22, TW_DS, BOLD), T("↔", 26, TXT), T("Channel_Profile oktet 11 (duyurulan kayma)", 22, PROF, BOLD)).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.2)
        ct = T("→ OLT'nin kendi bildirdiği değer de test edilir", 19, GOOD, BOLD).next_to(cmp_, DOWN, buff=0.25)
        self.play(FadeIn(ref, shift=UP * 0.1), run_time=0.7)
        self.at(self.cue("Ölçtüğünüz", 2))
        self.play(FadeIn(cmp_), run_time=0.6)
        self.play(FadeIn(ct), run_time=0.4)
        self.end(pad=0.05)

        self.beat("g5")
        self.clear(h)
        h = self.show_heading("Yukarı yön: kanal kanal", h)
        axg, X = nm_axis(1531, 1541, y=-1.6, step=1, label_every=1)
        nms = [thz_to_nm(f) for f in (195.25, 195.2, 195.15, 195.1, 195.05, 195.0, 194.95, 194.9)]
        pk = VGroup(*[Line([X(v), -1.55, 0], [X(v), -0.2, 0], color=TW_US, stroke_width=3).set_opacity(0.25) for v in nms])
        dot = Dot([X(nms[0]), -0.1, 0], color=TW_US, radius=0.09)
        mse = T("50 GHz CS: ± 12,5 GHz ≈ ± 100 pm @ 1536 nm", 22, GOLD, BOLD).move_to(UP * 1.3)
        b7 = T("burst içi λ kayması → Bölüm 7", 19, ACC, BOLD).move_to(UP * 0.6)
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(pk), FadeIn(dot), run_time=0.7)
        for i in range(1, 8):
            self.play(dot.animate.move_to([X(nms[i]), -0.1, 0]), pk[i].animate.set_opacity(1), run_time=0.35)
        self.at(self.cue("Sapma sınırı", 2))
        self.play(FadeIn(mse), run_time=0.5)
        self.at(self.cue("Burst içindeki", 4))
        self.play(FadeIn(b7), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep03_labA")


class E3LabB(Act3):
    HDR, MANIFEST, PREV_BADGE = H3["L"], M3("lab"), "lab"

    def construct(self):
        self.beat("g5a")
        h = self.show_heading("Çoklayıcının karakterizasyonu")
        tls = box(1.9, 0.6, "ayarlanabilir lazer", GOLD, 14).move_to([-5.4, 1.4, 0])
        wm = box(1.0, 0.6, "WM", "#3B4A75", 15).move_to([-3.4, 1.4, 0])
        pm = instrument("PM", 1.6, 1.1).move_to([-1.4, 1.4, 0])
        ln = VGroup(Line(tls.get_right(), wm.get_left(), color=FEED, stroke_width=2.5), Line(wm.get_right(), pm.get_left(), color=FEED, stroke_width=2.5))
        o = np.array([-5.8, -2.3, 0])
        curve = VMobject(color=ACC, stroke_width=3).set_points_smoothly([o + [x, 2.2 * np.exp(-((x - 2.4) / 1.05) ** 4), 0] for x in np.linspace(0, 4.8, 60)])
        axl = Line(o, o + [5.0, 0, 0], color=MUTED, stroke_width=2)
        checks = VGroup(T("✓ (1+X) dB bant genişliği < 2·MTE", 20, TXT), T("✓ merkezden tekdüze azalma", 20, TXT), T("✓ dalgalanma < OLT ölçüm çözünürlüğü", 20, TXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -0.9, 0])
        self.play(FadeIn(tls), FadeIn(wm), FadeIn(pm), Create(ln), run_time=0.8)
        self.play(Create(axl), Create(curve), run_time=0.9)
        for i, key in enumerate(["bir artı X", "eğri kanal", "dalgalanma"]):
            self.at(self.cue(key, 3 + i))
            self.play(FadeIn(checks[i], shift=LEFT * 0.1), run_time=0.4)
        self.end(pad=0.05)

        self.beat("g6")
        self.clear(h)
        h = self.show_heading("Yalıtım ölçümü", h)
        src = box(1.7, 0.6, "kalibre kaynak", GOLD, 14).move_to([-5.2, 0.8, 0])
        wm = box(1.2, 2.4, "WM / CEx", "#3B4A75", 15).move_to([-2.6, 0.2, 0])
        pi_ = Line(src.get_right(), [wm.get_left()[0], 0.8, 0], color=GOLD, stroke_width=3)
        pj = VGroup(Line([wm.get_left()[0], -0.4, 0], [-4.4, -0.4, 0], color=WARN, stroke_width=2), instrument("PM", 1.4, 1.0).move_to([-5.2, -0.6, 0]))
        lbl = VGroup(T("port i", 15, GOLD).next_to(pi_, UP, buff=0.05), T("port j: sızıntı", 15, WARN).next_to(pj[0], DOWN, buff=0.05))
        res = VGroup(T("yalıtım = P_i − P_j", 26, ACC, BOLD), T("geri dönüş kaybı > 50 dB\nyönlülük > 50 dB (Ek VIII örnek)", 18, TXT, line_spacing=0.9),
                     T("CEx: G-PON · XG-PON1 · video\nportları arasında da", 18, GOLD, BOLD, line_spacing=0.9)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, 0.2, 0])
        self.play(FadeIn(src), FadeIn(wm), Create(pi_), run_time=0.7)
        self.play(FadeIn(pj), FadeIn(lbl), FadeIn(res[0]), run_time=0.7)
        self.at(self.cue("Ek sekizdeki", 2))
        self.play(FadeIn(res[1]), run_time=0.5)
        self.at(self.cue("Aynı yöntemle", 3))
        self.play(FadeIn(res[2]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g6a")
        self.clear(h)
        h = self.show_heading("Etkilenmeme testi", h)
        o = np.array([-5.6, -2.0, 0])
        ax = VGroup(Line(o, o + [11.0, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 3.2, 0], color=MUTED, stroke_width=2),
                    T("zaman", 15, MUTED).next_to(o + [11.0, 0, 0], DOWN, buff=0.1), T("eski sistem BER (log)", 15, MUTED).next_to(o + [0, 3.2, 0], UP, buff=0.08))
        rng = np.random.default_rng(3)
        ber = VMobject(color=LEGACY, stroke_width=3).set_points_smoothly([o + [x, 1.0 + 0.08 * rng.standard_normal(), 0] for x in np.linspace(0.1, 10.8, 40)])
        on = VGroup(DashedLine(o + [5.5, 0, 0], o + [5.5, 3.0, 0], color=ACC, stroke_width=2.5), T("NG-PON2 açılır", 17, ACC, BOLD).move_to(o + [5.5, 3.25, 0]))
        ok = T("değişim olmamalı", 22, GOOD, BOLD).move_to(o + [8.3, 2.0, 0])
        self.play(Create(ax), run_time=0.5)
        self.play(Create(ber), run_time=1.6)
        self.at(self.cue("sonra NG-PON2", 2))
        self.play(Create(on[0]), FadeIn(on[1]), run_time=0.5)
        self.at(self.cue("Hata oranında", 3))
        self.play(FadeIn(ok), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g7")
        self.clear(h)
        h = self.show_heading("Raman testi: video CCR", h)
        o = np.array([-5.6, -2.0, 0])
        ax = VGroup(Line(o, o + [10.6, 0, 0], color=MUTED, stroke_width=2), Line(o, o + [0, 3.2, 0], color=MUTED, stroke_width=2),
                    T("RF kanal frekansı", 15, MUTED).next_to(o + [10.6, 0, 0], DOWN, buff=0.1), T("CCR (dB)", 15, MUTED).next_to(o + [0, 3.2, 0], UP, buff=0.08))
        base = Line(o + [0.2, 2.5, 0], o + [10.4, 2.5, 0], color=VIDEO, stroke_width=3)
        deg = [VMobject(color=WARN, stroke_width=2.5).set_points_smoothly([o + [x, 2.5 - n * 0.35 / (1 + (x / 1.6) ** 2), 0] for x in np.linspace(0.2, 10.4, 50)]) for n in (1, 2, 4)]
        lg = VGroup(T("yalnız video", 17, VIDEO, BOLD), T("+ TWDM ↓ kanalları (1 → 4)", 17, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(o + [8.0, 1.2, 0])
        lo = T("alçak frekanslarda bozulma = Raman", 19, WARN, BOLD).move_to(o + [3.2, 0.5, 0])
        self.play(Create(ax), Create(base), FadeIn(lg[0]), run_time=0.8)
        self.at(self.cue("sonra TWDM", 2))
        self.play(LaggedStart(*[Create(d) for d in deg], lag_ratio=0.4), FadeIn(lg[1]), run_time=1.4)
        self.at(self.cue("Düşük frekanslı", 3))
        self.play(FadeIn(lo), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g7a")
        wc = pill("en kötü koşul: her ↓ kanal en büyük başlatma gücünde", WARN, 21).move_to(UP * 1.6)
        self.play(FadeIn(wc, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.cue("Daha düşük güçte", 3))
        self.play(Indicate(deg[-1], color=WARN), run_time=0.8)
        self.end(pad=0.05)

        self.engineer_note("g8", [("1", "Raporunuza yazın", "Frekans doğruluğu ve çözünürlük (RBW) düzeltmesi.", 1),
                                  ("2", "Yalıtımı kenarlarda ölçün", "Kanal merkezinde değil, sapma sınırının iki ucunda.", 2)])
        self.clear()
        self.drop_badge()
        self.save_timeline("ep03_labB")


class E3End(Act3):
    HDR, MANIFEST, FIRST = H3["E"], M3("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 3'ün özeti")
        self.at(1.5)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["TWDM ↓ 1596–1603 nm · ↑ geniş / azaltılmış / dar · PtP: paylaşılan / genişletilmiş",
               "NG-PON2, G-PON · XG-PON1 · RF video · OTDR arasındaki boşluklarda",
               "↓ ızgara 100 GHz sabit · ↑ CS 50…200 GHz · MSE aralıkla ölçeklenir",
               "Raman: video ← modülasyon karışması · ↑ kanallar ← güç tüketimi · Ek VI / IX",
               "Harita ONU'ya System_Profile + Channel_Profile ile duyurulur"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 20, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        self.at(self.cue("Bir:", 1))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 4))
        self.play(FadeIn(items[1], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, key in zip([2, 3, 4], ["Üç:", "Dört:", "Beş:"]):
            self.at(self.cue(key, 0.3))
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("4 kanal · döngüsel değil ·\n100 GHz ↑ ızgara: en küçük\nayar penceresi?", CH[0]),
            ("↑ kanal 195,1 THz:\nChannel_Profile'da\nhangi sayıyla yazılır?", CH[1]),
            ("Raman modülasyon karışması:\naynı yönde mi, karşı\nyönde mi yayılanlar arasında?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 4'ün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, key in enumerate(["Birinci soru", "İkinci soru", "Üçüncü soru"]):
            self.at(self.cue(key, 1 + 4 * k))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("Cevaplar", 12))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T("Bölüm 4 · Kaynak", 54, TXT, BOLD),
                     T("OLT vericisi · sönüm oranı · göz maskesi · SMSR · 125 µs çerçeve", 22, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 0.9)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        eye = VGroup()
        st = lambda u: 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0, 1))
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    lvl = lambda x, a=a, b=b, c=c: a + (b - a) * st((x + 0.25) / 0.5) + (c - b) * st((x - 0.75) / 0.5)
                    pts_ = [[-1.6 + 1.6 * (x + 0.5), -2.4 + 1.2 * lvl(x), 0] for x in np.linspace(-0.5, 1.5, 80)]
                    eye.add(VMobject(stroke_color=TW_DS, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0).set_points_smoothly(pts_))
        self.play(LaggedStart(*[Create(e) for e in eye], lag_ratio=0.1), run_time=1.2)
        self.end(pad=0.6)
        self.play(FadeOut(VGroup(nxt, eye)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 3 · Renk Haritası", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: Google Gemini TTS (3.8 Flash Lite) — ses: Sadaltager", 22, ACC, BOLD),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep03_end")
