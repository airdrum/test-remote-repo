"""S2·B7 · Perde 1 (profiller ve kalibrasyon — G.989.3 §17.1, §17.2, Tablo 17-1/17-2, §11.2.6.4, Ek E) and
Perde 2 (devir — §17.3, Şekil 17-1, Tablo 17-3 … 17-9, Tablo 12-1/12-3/12-4 O5.2/O8/O9, Amd.2)."""
from ep17_common import *


# ================================ PERDE 1 ======================================
class E17P1A(Act17):
    HDR, MANIFEST, FIRST = H17[1], M17("p1"), True

    def construct(self):
        # b1 — §17: four procedures; edition note: §17 + Annexes F, H, X unchanged since 2021; amendments touch only O5, O8, O9 tables
        self.beat("b1")
        tc = self.title_card("PERDE 1", "Profiller ve kalibrasyon")
        self.at(self.cue("On yedinci madde", 3.0))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("§17 — dört işlevin yordamı")
        fn = VGroup(*[sbox(a, b, c, 2.95, 0.95, 20, 15) for a, b, c in (("profil duyurusu", "§17.1", GOLD), ("ONU kalibrasyonu", "§17.2", ACC),
                                                                         ("kanal devri", "§17.3", TGTC), ("kanal kilitleme", "§17.4", "#60A5FA"))])
        fn.arrange(RIGHT, buff=0.18).move_to([0, 1.35, 0])
        rows = mtable(["blok", "2021 → Amd.1 (2023)", "Amd.1 → Amd.2 (2025)"],
                      [["§17 · Tablo 17-1 … 17-9", "değişiklik yok", "değişiklik yok"], ["Ek F · ayar dizileri", "değişiklik yok", "değişiklik yok"],
                       ["Ek H · bağlama", "değişiklik yok", "değişiklik yok"], ["Ek X · klonlu CT", "değişiklik yok", "değişiklik yok"]],
                      [3.9, 3.1, 3.1], size=17, hsize=15, row_h=0.44).move_to([-1.0, -0.75, 0])
        for r in rows[1:]:
            for c in r[2:]:
                c.set_color(GOOD)
        amd = VGroup(T("değişikliklerin dokunduğu yer:", 17, MUTED, BOLD),
                     VGroup(tile("O5", OPC, 0.8, 0.42, 16, 0.2), tag("Amd.1 · TO6", AMDC, 15)).arrange(RIGHT, buff=0.1),
                     VGroup(tile("O8", TUC, 0.8, 0.42, 16, 0.2), tile("O9", TUC, 0.8, 0.42, 16, 0.2), tag("Amd.2 · O8.2 kararı", AMDC, 15)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.35)
        fit(amd, 12.6).move_to([0, -2.95, 0])
        self.play(self.set_src("G.989.3 §17 · Ek F · Ek H · Ek X · kelime farkı 2021 → Amd.2"), run_time=0.3)
        self.at(self.cue("dört işlevin", 4.0))
        self.play(FadeIn(fn[0], shift=UP * 0.06), run_time=0.4)
        for k, (key, d) in enumerate((("ONU kalibrasyonu", 8.2), ("dalga boyu kanalı devri", 9.7), ("ve kanal kilitleme", 11.5))):
            self.at(self.cue(key, d))
            self.play(FadeIn(fn[k + 1], shift=UP * 0.06), run_time=0.4)
        self.at(self.cue("Önce bir sürüm notu", 13.3))
        self.play(FadeIn(rows[0]), run_time=0.4)
        self.at(self.cue("on yedinci madde ve F", 15.0))
        self.play(FadeIn(rows[1][:2], shift=RIGHT * 0.06), FadeIn(rows[2][:2], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("H ve X ekleri", 16.8))
        self.play(FadeIn(rows[3][:2], shift=RIGHT * 0.06), FadeIn(rows[4][:2], shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("tek sözcük değişmedi", 19.5))
        self.play(*[FadeIn(r[2:], shift=LEFT * 0.05) for r in rows[1:]], run_time=0.6)
        self.at(self.cue("İki değişikliğin", 22.0))
        self.play(FadeIn(amd[0]), FadeIn(amd[1], shift=UP * 0.06), run_time=0.5)
        self.at(self.cue("O8 ve O9'un", 26.5))
        self.play(FadeIn(amd[2], shift=UP * 0.06), run_time=0.4)
        self.end(pad=0.05)

        # b2 + b3 — §17.1 profile announcement: 1 System + ≤ 8 Channel + ≤ 64 Burst, broadcast, unacknowledged; TminProfile 1–5 s;
        #          our arithmetic: ≤ 73 messages ≥ 9.1 ms; ONU side TProfileDwell ≥ 10 s = 2 × 5 s
        self.beat("b2")
        self.clear()
        h = self.show_heading("§17.1 — profil duyurusu", h)
        x0 = -3.3
        lbl = VGroup(*[VGroup(T(a, 18, GOLD, BOLD), T(b, 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
                       for a, b in (("System_Profile", "tek mesaj"), ("Channel_Profile", "kanal çifti başına 1"), ("Burst_Profile", "haritaların andığı her profil"))])
        for l, y in zip(lbl, (1.75, 1.0, -0.05)):
            l.move_to([-6.4, y, 0], aligned_edge=LEFT)
        sp = mbox("SP", GOLD, 0.62, 0.42, 15, 0.35).move_to([x0 + 0.31, 1.75, 0])
        cp = VGroup(*[mbox(f"CP{i + 1}", GOLD, 0.62, 0.42, 14, 0.25) for i in range(8)]).arrange(RIGHT, buff=0.06).move_to([x0, 1.0, 0], aligned_edge=LEFT)
        bp = VGroup()
        for c in range(8):
            col = VGroup(*[Rectangle(width=0.5, height=0.11, stroke_width=0, fill_color=GOLD, fill_opacity=0.5 if c == 0 else 0.3) for _ in range(8)]).arrange(DOWN, buff=0.025)
            bp.add(col)
        bp.arrange(RIGHT, buff=0.18).move_to([x0, -0.05, 0], aligned_edge=LEFT)
        c8 = T("≤ 8", 20, GOLD, BOLD).next_to(cp, RIGHT, buff=0.2)
        b8 = brace_lbl(bp[0], "kanal başına ≤ 8", GOLD, DOWN, 15)
        b64 = T("toplam ≤ 64", 20, GOLD, BOLD).next_to(bp, DOWN, buff=0.1).align_to(bp, RIGHT)
        bc = VGroup(T("her ↓ kanalda", 17, TXT, BOLD), tag("yayın", BCC, 15), tag("onaysız", MUTED, 15)).arrange(RIGHT, buff=0.15).next_to(h, RIGHT, buff=0.4)
        ax, X = lin_axis(0, 10, -6.0, 5.6, -2.55, list(range(0, 11)), size=14, fmt=lambda v: f"{v:g}")
        axu = T("s", 14, MUTED).next_to(ax, RIGHT, buff=0.12).shift(DOWN * 0.15)
        sets5 = VGroup(*[Rectangle(width=X(0.3) - X(0), height=0.3, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([X(t) + (X(0.3) - X(0)) / 2, -2.25, 0]) for t in (0, 5, 10)])
        sets1 = VGroup(*[Rectangle(width=0.05, height=0.18, stroke_width=0, fill_color=GOLD, fill_opacity=0.6).move_to([X(t), -2.2, 0]) for t in range(1, 10)])
        tp = VGroup(T("tam küme · TminProfile", 16, GOLD, BOLD), T("1 s … 5 s", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([X(2.5), -1.75, 0])
        self.play(self.set_src("G.989.3 §17.1 · §17.1.2 · §11.3.3"), run_time=0.3)
        self.at(self.cue("her aşağı yön kanalında", 1.3))
        self.play(FadeIn(bc, shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("bir sistem profili", 6.1))
        self.play(FadeIn(lbl[0]), FadeIn(sp, shift=RIGHT * 0.06), run_time=0.4)
        self.at(self.cue("konuşlu her kanal çifti", 7.7))
        self.play(FadeIn(lbl[1]), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.05) for c in cp], lag_ratio=0.1), run_time=0.9)
        self.at(self.cue("en çok sekiz;", 11.7))
        self.play(FadeIn(c8, scale=0.8), run_time=0.3)
        self.at(self.cue("haritaların andığı", 12.8))
        self.play(FadeIn(lbl[2]), FadeIn(bp[0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("kanal başına en çok sekiz", 17.4))
        self.play(FadeIn(b8), run_time=0.4)
        self.at(self.cue("toplam altmış dört", 19.6))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.05) for c in bp[1:]], lag_ratio=0.08), FadeIn(b64), run_time=0.8)
        self.at(self.cue("Tam küme bir ile beş", 21.2))
        self.play(Create(ax), FadeIn(axu), run_time=0.5)
        self.play(FadeIn(sets5), FadeIn(sets1), FadeIn(tp), run_time=0.6)
        self.end(pad=0.05)

        self.beat("b3")
        calc = VGroup(VGroup(T("1 + 8 + 64 =", 26, TXT, BOLD), T("73", 30, GOLD, BOLD)).arrange(RIGHT, buff=0.18),
                      VGroup(T("yayın mesajı · ≤ 1 / çerçeve", 18, MUTED, BOLD), T("≥ 73 × 125 µs = 9,1 ms", 22, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        calc.move_to([5.0, 0.55, 0])
        ht = interp("hesap", GOLD, 15).next_to(calc, UP, buff=0.12).align_to(calc, LEFT)
        dw = Rectangle(width=X(10) - X(0), height=0.3, stroke_color=O1C, stroke_width=1.6, fill_color=O1C, fill_opacity=0.3).move_to([(X(0) + X(10)) / 2, -1.3, 0])
        dwl = T("O1.2 · TProfileDwell ≥ 10 s", 16, TXT, BOLD).move_to(dw)
        two = T("= 2 × en uzun periyot (5 s)", 17, O1C, BOLD).next_to(dw, UP, buff=0.1).align_to(dw, RIGHT)
        self.play(FadeOut(tp), run_time=0.3)
        self.at(self.cue("en çok yetmiş üç", 1.6))
        self.play(FadeIn(ht), FadeIn(calc[0], shift=LEFT * 0.06), Indicate(VGroup(sp, cp, bp), color=GOLD, scale_factor=1.02), run_time=0.8)
        self.at(self.cue("Çerçeve başına en çok bir", 5.0))
        self.play(FadeIn(calc[1], shift=LEFT * 0.06), run_time=0.5)
        self.at(self.cue("ONU tarafındaki karşılık", 11.5))
        self.play(GrowFromEdge(dw, LEFT), FadeIn(dwl), run_time=0.8)
        self.at(self.cue("en uzun periyodun", 17.9))
        self.play(FadeIn(two, shift=DOWN * 0.05), Indicate(sets5[1], color=GOLD, scale_factor=1.4), run_time=0.6)
        self.end(pad=0.05)

        # b4 — System_Profile (Table 17-1 / 11-17): channel count, US spacing (1 GHz, ONU Tx scaling factor), MSE, FSR, band; two rule fields
        self.beat("b4")
        self.clear()
        h = self.show_heading("Sistem profili — Tablo 17-1", h)
        spec = [("bant", 1, "#94A3B8", "9"), ("kanal sayısı", 1.2, GOLD, "10"), ("↑ aralık", 1.2, ACC, "11"), ("MSE", 1.0, "#60A5FA", "12"),
                ("FSR", 1.6, "#A78BFA", "13–14"), ("doğruluk · AMCC", 1.8, GOOD, "15"), ("gevşek sınır", 1.4, PINK, "16")]
        om = octets(spec, 12.4, 0.62, 17, 14).move_to([0, 1.25, 0])
        oml = T("System_Profile · oktet", 15, MUTED, BOLD).next_to(om, UP, buff=0.12).align_to(om, LEFT)
        notes = {
            1: VGroup(T("kanal sayısı", 17, GOLD, BOLD), T("kaç Channel_Profile beklenir", 16, TXT, BOLD)),
            2: VGroup(T("↑ kanal aralığı · 1 GHz birim", 17, ACC, BOLD), T("ONU vericisi için ölçek çarpanı", 16, TXT, BOLD)),
            3: VGroup(T("en büyük spektral sapma · 1 GHz", 17, "#60A5FA", BOLD)),
            4: VGroup(T("serbest spektral aralık · 0,1 GHz", 17, "#A78BFA", BOLD), T("↑ bant · G.989.2 Tablo 9-1", 16, TXT, BOLD)),
        }
        col = VGroup(*[VGroup(*notes[k]).arrange(DOWN, aligned_edge=LEFT, buff=0.06) for k in (1, 2, 3, 4)]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        col.move_to([-6.3, -1.1, 0], aligned_edge=LEFT)
        rl = VGroup(T("iki kural alanı", 19, GOOD, BOLD),
                    VGroup(T("BB", 18, GOOD, BOLD), T("bant içi aktivasyon için en düşük doğruluk", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15),
                    VGroup(T("", 1), T("01 kalibre değil · 10 gevşek · 11 yeterli", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.0),
                    VGroup(T("A", 18, GOOD, BOLD), T("AMCC aktivasyon için var / yok", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rl[2].align_to(rl[1][1], LEFT)
        rbox = SurroundingRectangle(rl, color=GOOD, buff=0.2, corner_radius=0.12, stroke_width=1.8)
        VGroup(rl, rbox).move_to([3.6, -1.25, 0])
        self.play(self.set_src("G.989.3 Tablo 17-1 · Tablo 11-17"), FadeIn(oml), FadeIn(om[0], shift=DOWN * 0.05), run_time=0.5)
        self.at(self.cue("kanal sayısı", 2.5))
        self.play(FadeIn(om[1], shift=DOWN * 0.05), FadeIn(col[0]), run_time=0.4)
        self.at(self.cue("bir gigahertzlik birimle", 3.6))
        self.play(FadeIn(om[2], shift=DOWN * 0.05), FadeIn(col[1][0]), run_time=0.4)
        self.at(self.cue("ölçek çarpanıdır", 8.8))
        self.play(FadeIn(col[1][1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("en büyük spektral sapma", 11.4))
        self.play(FadeIn(om[3], shift=DOWN * 0.05), FadeIn(col[2]), run_time=0.4)
        self.at(self.cue("serbest spektral aralık", 13.4))
        self.play(FadeIn(om[4], shift=DOWN * 0.05), FadeIn(col[3][0]), run_time=0.4)
        self.at(self.cue("yukarı yön bandı", 15.5))
        self.play(Indicate(om[0], color=TXT, scale_factor=1.1), FadeIn(col[3][1]), run_time=0.5)
        self.at(self.cue("Ve iki kural alanı", 17.1))
        self.play(FadeIn(om[5:], shift=DOWN * 0.05), Create(rbox), FadeIn(rl[0]), run_time=0.5)
        self.at(self.cue("en düşük kalibrasyon doğruluğu", 19.8))
        self.play(FadeIn(rl[1:3], shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("ve AMCC bayrağı", 23.4))
        self.play(FadeIn(rl[3], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p1A")


class E17P1B(Act17):
    HDR, MANIFEST, FIRST = H17[1], M17("p1"), True
    PREV_BADGE = "std"

    def construct(self):
        # b5 — Channel_Profile = the handover checklist (Table 17-2 / 11-18) → the NACK / ROLLBACK code each element feeds (our reading);
        #      default response channel; 4-bit versions
        self.beat("b5")
        h = self.show_heading("Kanal profili — devrin kontrol listesi")
        data = [("yönetim etiketi · PON-ID", "7–10", "DS_ALBL · US_ALBL", "yönetim etiketi"), ("boş göstergeleri D / U", "5", "DS_VOID · US_VOID", "boş göstergeleri"),
                ("↓ frekans ofseti · 0,1 GHz", "11", "DS_TUNR", "aşağı yön frekans ofseti"), ("↓ hız · hat kodu", "12", "DS_LNRT · DS_LNCD", "hızı ve hat kodu"),
                ("bölümleme indeksi", "13", "DS_PART", "bölümleme indeksi"), ("↑ frekans", "24–27", "US_TUNR", "yukarı yön frekansı"),
                ("bağlantı tipi · ↑ hız", "28 · 29", "US_LKTP · US_LNRT", "bağlantı tipi ve hızı")]
        tb = mtable(["öğe (Tablo 17-2)", "oktet", "beslediği kod"], [[a, b, c] for a, b, c, _ in data], [4.3, 1.3, 3.6], size=17, hsize=15, row_h=0.45, mono=(2,))
        tb.move_to([-6.45, 0.55, 0], aligned_edge=LEFT).set_y(0.45)
        for r in tb[1:]:
            r[3].set_color(WARN)
            r[3].set_opacity(0)
        tb[0][3].set_opacity(0)
        rd = interp("bizim okumamız", GOLD, 15).next_to(tb, DOWN, buff=0.12).align_to(tb, RIGHT)
        xr = 4.75
        dsl = tile("↓ λ · bu kanal", TGTC, 2.2, 0.5, 16, 0.2).move_to([xr, 1.6, 0])
        onu = onu_box("ONU", ONUC, 1.2, 0.55, 16).move_to([xr, 0.55, 0])
        usl = tile("↑ kanal · UWLCH", TGTC, 2.2, 0.5, 16, 0.2).move_to([xr, -0.5, 0])
        a1 = arrow(dsl.get_bottom(), onu.get_top(), TGTC, 2.2, 0.12)
        a2 = arrow(onu.get_bottom(), usl.get_top(), TGTC, 2.2, 0.12)
        drl = VGroup(T("varsayılan yanıt kanalı", 17, TXT, BOLD), T("oktet 14–17", 15, MUTED, BOLD)).arrange(DOWN, buff=0.05).next_to(usl, DOWN, buff=0.15)
        ver = VGroup(T("her profilde sürüm:", 17, TXT, BOLD), bitbox([(c, GOLD) for c in "VVVV"], 0.36, 0.4, 16), T("4 bit", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        ver.move_to([0, -3.0, 0])
        vrule = T("güncelleme yalnızca sürümden anlaşılmalı", 17, GOLD, BOLD).next_to(ver, RIGHT, buff=0.35)
        VGroup(ver, vrule).move_to([0, -3.0, 0])
        self.play(self.set_src("G.989.3 Tablo 17-2 · Tablo 11-18 · Tablo 17-3/17-4 · §17.1.2"), FadeIn(tb[0][:3]), run_time=0.5)
        for k, (_, _, _, key) in enumerate(data):
            self.at(self.cue(key, 3.7 + 1.5 * k))
            self.play(FadeIn(tb[k + 1][:3], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("Bizim okumamızla", 15.1))
        self.play(tb[0][3].animate.set_opacity(1), FadeIn(rd), run_time=0.4)
        self.at(self.cue("bir hata kodunu besler", 18.2))
        self.play(LaggedStart(*[r[3].animate.set_opacity(1) for r in tb[1:]], lag_ratio=0.12), run_time=1.0)
        self.at(self.cue("varsayılan yanıt kanalı", 20.9))
        self.play(FadeIn(dsl), FadeIn(onu), GrowArrow(a1), run_time=0.5)
        self.at(self.cue("hangi yukarı yön kanalında", 25.6))
        self.play(GrowArrow(a2), FadeIn(usl), FadeIn(drl), run_time=0.6)
        self.at(self.cue("dört bitlik bir sürümü", 30.8))
        self.play(FadeIn(ver, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("yalnızca sürümden", 35.0))
        self.play(FadeIn(vrule, shift=LEFT * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # b6 — §17.2 calibration: definition; calibration record (channel parameters ↔ internal tuning values); DS loop by the ONU alone
        #      (O1, O8, own discretion); US loop needs the OLT (O2-3 SN state, O9, OLT guidance)
        self.beat("b6")
        self.clear()
        h = self.show_heading("§17.2 — ONU kalibrasyonu", h)
        df = VGroup(T("ONU,", 22, TXT, BOLD), T("söylendiğinde belirli kanallara doğru ayarlanabilmeli", 22, ACC, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, 1.8, 0])
        fit(df, 12.6)
        lc = VGroup(*[tag(s, GOLD, 16) for s in ("↓ kanal · frekans", "↑ kanal · frekans")]).arrange(DOWN, buff=0.18).move_to([-4.2, 0.45, 0])
        rc = VGroup(*[tag(s, ACC, 16) for s in ("Rx ayar değerleri", "Tx ayar değerleri")]).arrange(DOWN, buff=0.18).move_to([4.2, 0.45, 0])
        rec = sbox("kalibrasyon kaydı", "eşleme", GOLD, 2.8, 0.95, 21, 16).move_to([0, 0.45, 0])
        la = VGroup(arrow(lc.get_right() + RIGHT * 0.1, rec.get_left(), MUTED, 2, 0.1), arrow(rec.get_right(), rc.get_left() + LEFT * 0.1, MUTED, 2, 0.1))
        lcl = T("kanal parametreleri", 15, GOLD, BOLD).next_to(lc, UP, buff=0.1)
        rcl = T("ONU'nun iç ayar değerleri", 15, ACC, BOLD).next_to(rc, UP, buff=0.1)

        def loop_panel(title, sub, states, who, color, x):
            r = RoundedRectangle(corner_radius=0.16, width=6.3, height=1.95, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([x, -2.0, 0])
            t = T(title, 19, color, BOLD).move_to(r.get_corner(UL) + [0.25, -0.3, 0], aligned_edge=LEFT)
            st = VGroup(*[tile(s, c, 0.95, 0.42, 16, 0.2) for s, c in states]).arrange(RIGHT, buff=0.12)
            st.next_to(t, DOWN, buff=0.22).align_to(t, LEFT)
            w = fit(T(who, 16, TXT, BOLD), 6.3 - 0.55 - st.width - 0.3).next_to(st, RIGHT, buff=0.3)
            s_ = fit(T(sub, 15, MUTED, BOLD), 5.8).next_to(st, DOWN, buff=0.18).align_to(t, LEFT)
            return VGroup(r, t, st, w, s_)
        dsp = loop_panel("↓ döngü", "alıcı aralığını tara · senkron · Channel_Profile oku · kaydet", (("O1", O1C), ("O8", TUC)), "ONU tek başına · kendi takdiriyle", ACC, -3.3)
        usp = loop_panel("↑ döngü", "en iyi çaba → OLT'den geri bildirim gelene kadar", (("O2-3", SNC), ("O9", TUC)), "OLT zorunlu · OLT rehberliğinde", GOLD, 3.3)
        self.play(self.set_src("G.989.3 §17.2 · §17.2.1 · §17.2.2"), run_time=0.3)
        self.at(self.cue("söylendiğinde belirli", 2.4))
        self.play(FadeIn(df, shift=UP * 0.06), run_time=0.6)
        self.at(self.cue("Yolu bir kalibrasyon kaydıdır", 7.2))
        self.play(FadeIn(rec, scale=0.9), run_time=0.5)
        self.at(self.cue("kanal parametreleri ile", 9.7))
        self.play(FadeIn(lc), FadeIn(lcl), GrowArrow(la[0]), run_time=0.5)
        self.at(self.cue("iç ayar değerleri", 12.0))
        self.play(GrowArrow(la[1]), FadeIn(rc), FadeIn(rcl), run_time=0.5)
        self.at(self.cue("Aşağı yön döngüsünü", 15.4))
        self.play(FadeIn(dsp[:2]), FadeIn(dsp[4]), run_time=0.5)
        self.at(self.cue("O1'de ve O8'de", 19.1))
        self.play(FadeIn(dsp[2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("kendi takdiriyle", 20.4))
        self.play(FadeIn(dsp[3], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("Yukarı yön döngüsü", 21.8))
        self.play(FadeIn(usp[:2]), FadeIn(usp[4]), run_time=0.5)
        self.at(self.cue("seri numarası durumunda", 26.2))
        self.play(FadeIn(usp[2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("OLT'nin rehberliğinde", 29.0))
        self.play(FadeIn(usp[3], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # b7 — accuracy classes: 8-octet calibration record status in Serial_Number_ONU / Tuning_Response; 2 bits per US channel (16);
        #      00 unannounced · 01 uncalibrated · 10 loose · 11 sufficient; loose bound at run time (0 → MSE); sufficient: no number
        self.beat("b7")
        self.clear()
        h = self.show_heading("Doğruluk sınıfları — kalibrasyon durumu", h)
        vals = [3, 3, 2, 3, 1, 2, 3, 0, 0, 3, 2, 1, 3, 3, 0, 0]  # UWLCH 0 … 15
        octs_ = VGroup()
        for o in range(8):
            hi, lo = vals[2 * o + 1], vals[2 * o]
            bits = "00" + format(hi, "02b") + "00" + format(lo, "02b")
            spec = [(b, MUTED if i in (0, 1, 4, 5) else ACCC[hi if i < 4 else lo]) for i, b in enumerate(bits)]
            bb = bitbox(spec, 0.172, 0.42, 14)
            for i in (0, 1, 4, 5):
                bb[i][0].set_fill(opacity=0.04)
            ids = VGroup(T(str(2 * o + 1), 14, MUTED, BOLD).next_to(bb[0:4], DOWN, buff=0.06), T(str(2 * o), 14, MUTED, BOLD).next_to(bb[4:8], DOWN, buff=0.06))
            octs_.add(VGroup(bb, ids))
        octs_.arrange(RIGHT, buff=0.14).move_to([0, 1.2, 0])
        onum = VGroup(*[T(f"oktet {o + 1}", 14, MUTED, BOLD).next_to(octs_[o][0], UP, buff=0.08) for o in range(8)])
        src = VGroup(tag("Serial_Number_ONU · 27–34", SNC, 15), tag("Tuning_Response · 23–30", ACC, 15)).arrange(RIGHT, buff=0.2).next_to(onum, UP, buff=0.15)
        uwl = T("altında: UWLCH 0 … 15 · çift kimlik düşük yarıda", 15, MUTED, BOLD).next_to(octs_, DOWN, buff=0.12)
        leg = VGroup(*[VGroup(bitbox([(c, ACCC[a]) for c in format(a, "02b")], 0.32, 0.4, 16), T(ACCN[a], 18, ACCC[a], BOLD)).arrange(RIGHT, buff=0.2)
                       for a in range(4)]).arrange(RIGHT, buff=0.5)
        fit(leg, 12.6).move_to([0, -0.75, 0])
        lb = VGroup(T("gevşek sınırı:", 18, GOLD, BOLD), T("System_Profile oktet 16 · 1 GHz · çalışma anında", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        lb0 = VGroup(HX("0x00", 18, GOLD, BOLD), T("→ en büyük spektral sapma (MSE)", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        sf = VGroup(T("yeterli:", 18, GOOD, BOLD), T("sayısal tanım yok", 18, WARN, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.2)
        low = VGroup(lb, lb0, sf).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.3, 0])
        self.play(self.set_src("G.989.3 §11.2.6.4 · §17.2.2 · Tablo 11-17 (oktet 16) · Tablo 12-3"), run_time=0.3)
        self.at(self.cue("seri numarası mesajında", 2.0))
        self.play(FadeIn(src[0], shift=DOWN * 0.05), run_time=0.4)
        self.at(self.cue("ayar yanıtında", 4.5))
        self.play(FadeIn(src[1], shift=DOWN * 0.05), run_time=0.4)
        self.at(self.cue("sekiz baytlık", 5.5))
        self.play(LaggedStart(*[FadeIn(o[0], shift=UP * 0.05) for o in octs_], lag_ratio=0.08), FadeIn(onum), run_time=1.0)
        self.at(self.cue("on altı yukarı yön", 9.4))
        self.play(LaggedStart(*[FadeIn(o[1]) for o in octs_], lag_ratio=0.06), FadeIn(uwl), run_time=0.8)
        for a, (key, d) in enumerate((("Sıfır,", 13.8), ("bir,", 15.9), ("iki,", 17.8), ("üç,", 18.7))):
            self.at(self.cue(key, d))
            self.play(FadeIn(leg[a], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Gevşeğin sınırını", 19.6))
        self.play(FadeIn(lb, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("sıfır yazılırsa", 23.5))
        self.play(FadeIn(lb0, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("Yeterli ise", 27.8))
        self.play(FadeIn(sf, shift=UP * 0.05), Indicate(leg[3], color=WARN, scale_factor=1.06), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p1B")


class E17P1C(Act17):
    HDR, MANIFEST, FIRST = H17[1], M17("p1"), True
    PREV_BADGE = "std"

    def construct(self):
        # b8 — the deliberate gap (System_Profile octet 16 text); ONU below threshold ignores in-band SN grants; no AMCC → silent
        self.beat("b8")
        self.set_badge("neden")
        h = self.show_heading("Bilinçli bir boşluk")
        qt = self.quote("G.989.3 Tablo 11-17 · oktet 16",
                        "\"it is not for standards to determine how loose the ONU wavelength calibration can be\n to avoid interference with other channels. This is conveyed to the ONU by the OLT.\"",
                        "Kalibrasyonun ne kadar gevşek olabileceğine standartlar karar vermez; bunu ONU'ya OLT söyler.", 12.0)
        qt.move_to([0, 1.0, 0])
        dq = sbox("doğruluk ≥ BB eşiği?", None, GOLD, 3.0, 0.7, 19).move_to([-3.6, -1.55, 0])
        yes = VGroup(arrow(dq.get_right() + UP * 0.12, [-0.6, -1.05, 0], GOOD, 2.2, 0.12), tag("bant içi SN tahsisleri", GOOD, 16).move_to([1.15, -1.05, 0]))
        no = VGroup(arrow(dq.get_right() + DOWN * 0.12, [-0.6, -2.1, 0], WARN, 2.2, 0.12),
                    VGroup(tag("bant içini yok say", WARN, 16), T("→", 18, MUTED, BOLD), tag("AMCC varsa: AMCC", GOLD, 16), tag("yoksa: sus", WARN, 16)).arrange(RIGHT, buff=0.12))
        no[1].move_to([-0.5, -2.1, 0], aligned_edge=LEFT)
        yl = T("evet", 15, GOOD, BOLD).next_to(yes[0], UP, buff=0.02)
        nl = T("hayır", 15, WARN, BOLD).next_to(no[0], DOWN, buff=0.02)
        self.play(self.set_src("G.989.3 Tablo 11-17 · §6.1.4.2 · Tablo 12-1 (O2-3)"), run_time=0.3)
        self.at(self.cue("Metne göre", 2.2))
        self.play(FadeIn(qt[0]), FadeIn(qt[1], shift=UP * 0.05), run_time=0.7)
        self.at(self.cue("standartlar karar vermez", 9.0))
        self.play(FadeIn(qt[2], shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("Eşiği karşılamayan ONU", 14.2))
        self.play(FadeIn(dq), GrowArrow(yes[0]), FadeIn(yes[1]), FadeIn(yl), run_time=0.6)
        self.play(GrowArrow(no[0]), FadeIn(nl), FadeIn(no[1][0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("AMCC sunulmuyorsa", 20.9))
        self.play(FadeIn(no[1][1:], shift=RIGHT * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # b9 — the AMCC route: Channel_Profile octet 18 I/A; ONU sends via AMCC; OLT: Calibration_Request (0x13) or activate here and postpone;
        #      in handover only in the target's Expecting state; gap: TWDM AMCC rate/framing not specified (Annex E: FFS)
        self.beat("b9")
        h = self.reset("AMCC yolu", "std")
        o18 = VGroup(T("Channel_Profile · oktet 18", 16, MUTED, BOLD), bitbox([(c, MUTED) for c in "000000"] + [("I", GOOD), ("A", GOLD)], 0.36, 0.42, 16)).arrange(RIGHT, buff=0.25)
        o18.move_to([-2.6, 1.85, 0])
        for i in range(6):
            o18[1][i][0].set_fill(opacity=0.04)
        o18l = VGroup(T("I · bant içi SN tahsisi sunuluyor", 15, GOOD, BOLD), T("A · AMCC SN tahsisi sunuluyor", 15, GOLD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        o18l.next_to(o18, RIGHT, buff=0.35)
        xo, xu, top, bot = -5.0, -1.4, 1.0, -3.2
        lo = lifeline("OLT CT", xo, top, bot, OLTC, 1.4, 0.48, 16)
        lu = lifeline("ONU", xu, top, bot, ONUC, 1.2, 0.48, 16)
        g1 = msg3(xo, xu, 0.2, "AMCC SN tahsisi · Alloc-ID 1021", GOLD, size=14)
        r1 = msg3(xu, xo, -0.55, "Serial_Number_ONU · AMCC", GOLD, size=14)
        alt = VGroup(msg3(xo, xu, -1.4, "Calibration_Request · hangi çift", ACC, size=14),
                     T("ya da", 15, MUTED, BOLD).move_to([(xo + xu) / 2, -1.85, 0]),
                     msg3(xo, xu, -2.55, "Assign_ONU-ID · burada ranging", SNC, size=14))
        pp = VGroup(T("öteki kanalların kalibrasyonu", 16, TXT, BOLD), T("→ o kanala devre kadar ertelenir", 16, SNC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        pp.move_to([-1.15, -2.55, 0], aligned_edge=LEFT)
        hv = VGroup(T("devirde:", 17, TGTC, BOLD), T("AMCC yönlendirilmiş", 16, TXT, BOLD), T("PLOAM tahsisi yalnızca", 16, TXT, BOLD),
                    VGroup(T("hedefin", 16, TXT, BOLD), ostate(2, 2.1, 0.7, 17, 14)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        hv.move_to([4.7, -0.2, 0])
        gap = VGroup(T("TWDM AMCC hızı · çerçevesi", 16, TXT, BOLD), T("standartta yok · Ek E: ileride", 16, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        gapb = SurroundingRectangle(gap, color=WARN, buff=0.15, corner_radius=0.1, stroke_width=1.6)
        VGroup(gap, gapb).move_to([4.95, -2.4, 0])
        self.play(self.set_src("G.989.3 Tablo 11-18 (oktet 18) · Tablo 11-2 · Tablo 12-1/12-3 · §6.1.4.2 · Ek E"), run_time=0.3)
        self.at(self.cue("Kanal profilinin iki biti", 0.8))
        self.play(FadeIn(o18, shift=DOWN * 0.05), run_time=0.5)
        self.at(self.cue("bant içi ve AMCC", 3.0))
        self.play(FadeIn(o18l, shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("ONU AMCC ile gönderir", 8.0))
        self.play(FadeIn(lo), FadeIn(lu), GrowArrow(g1[0]), FadeIn(g1[1]), run_time=0.6)
        self.play(GrowArrow(r1[0]), FadeIn(r1[1]), run_time=0.5)
        self.at(self.cue("kalibrasyon isteğiyle", 9.9))
        self.play(GrowArrow(alt[0][0]), FadeIn(alt[0][1]), run_time=0.5)
        self.at(self.cue("ya da ONU'yu bu kanalda", 16.7))
        self.play(FadeIn(alt[1]), GrowArrow(alt[2][0]), FadeIn(alt[2][1]), run_time=0.6)
        self.at(self.cue("o kanala devre kadar", 22.4))
        self.play(FadeIn(pp, shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("Devirde aynı yol", 24.8))
        self.play(FadeIn(hv, shift=LEFT * 0.05), run_time=0.6)
        self.at(self.cue("Bir boşluk", 30.1))
        self.play(FadeIn(gap), Create(gapb), run_time=0.5)
        self.end(pad=0.05)

        # b10 — PMD bridge S1·B7: OOC mask must be met wherever the Tx is tuned within its MSE (G.989.2 §9.3.9); our reading:
        #       outside its excursion an ONU is not covered → in-band talk reserved for calibrated ONUs
        self.beat("b10")
        h, chp = self.pmd_reset("PMD Köprüsü — OOC maskesi", s1chip(7))
        ax, X = lin_axis(-60, 60, -6.0, 6.0, -1.6, [-50, -25, 0, 25, 50], size=14, fmt=lambda v: f"{v:+g}".replace("+0", "0").replace("-", "−"))
        axl = T("GHz · kanal merkezine göre (50 GHz aralık örneği)", 14, MUTED, BOLD).next_to(ax, DOWN, buff=0.35)
        chn = Rectangle(width=X(25) - X(-25), height=2.6, stroke_width=0, fill_color=TGTC, fill_opacity=0.08).move_to([X(0), -0.3, 0])
        mse = DashedVMobject(Rectangle(width=X(12.5) - X(-12.5), height=2.6, stroke_color=GOLD, stroke_width=2), num_dashes=40).move_to([X(0), -0.3, 0])
        msel = T("MSE ± 12,5 GHz", 16, GOLD, BOLD).next_to(mse, UP, buff=0.08)
        lob = lobe(X, 6.0, -1.6, 2.0, 2.6, ONUC, 0.3)
        mask = VGroup(Line([X(-60), -0.85, 0], [X(-25), -0.85, 0], color=WARN, stroke_width=3), Line([X(25), -0.85, 0], [X(60), -0.85, 0], color=WARN, stroke_width=3))
        mkl = T("kanal dışı maske (OOC)", 16, WARN, BOLD).next_to(mask[0], UP, buff=0.08)
        rule = VGroup(T("G.989.2 §9.3.9:", 18, GOLD, BOLD), T("MSE içinde nereye ayarlanırsa ayarlansın → maskeye uy", 18, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        rule.move_to([0, 2.05, 0])
        fit(rule, 12.6)
        out = lobe(X, 30.0, -1.6, 2.0, 2.6, WARN, 0.3)
        outl = VGroup(T("sapmasının dışında:", 16, WARN, BOLD), T("güvence yok", 16, WARN, BOLD)).arrange(DOWN, buff=0.04).next_to([X(30), 0.45, 0], UP, buff=0.05)
        yr = VGroup(interp("yorum", GOLD, 15), T("bant içi konuşma → kalibre ONU'lar", 18, GOOD, BOLD)).arrange(RIGHT, buff=0.2).move_to([-3.6, 1.4, 0])
        self.play(self.set_src("S1·B7 · G.989.2 §9.3.9 · §11.1.5.2.4 · Tablo 11-6"), run_time=0.3)
        self.at(self.cue("kanal dışı güç maskesi", 2.5))
        self.play(Create(ax), FadeIn(axl), FadeIn(chn), Create(mask), FadeIn(mkl), run_time=0.8)
        self.at(self.cue("verici,", 7.9))
        self.play(Create(mse), FadeIn(msel), FadeIn(lob), run_time=0.6)
        self.at(self.cue("nereye ayarlanırsa", 10.0))
        self.play(FadeIn(rule, shift=DOWN * 0.05), run_time=0.5)
        self.play(lob.animate.shift(LEFT * (X(12) - X(0))), run_time=1.0)
        self.play(lob.animate.shift(RIGHT * (X(6) - X(0))), run_time=0.6)
        self.at(self.cue("sapmasının dışındaki", 16.9))
        self.play(FadeIn(out), FadeIn(outl), run_time=0.6)
        self.at(self.cue("bant içi konuşma", 21.9))
        self.play(FadeIn(yr, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # b11 — engineer note; b12 — bridge
        self.note11("b11", [("1", "Kalibrasyon durumunu her SN mesajında ve ayar yanıtında kaydedin",
                             "16 kanal × 2 bit · bir ONU'nun nereye gidebileceğinin en ucuz özeti", "kalibrasyon durumunu"),
                            ("2", "OLT'nin \"yeterli\" tanımını üreticiden yazılı isteyin",
                             "bant içi ile AMCC arasındaki sınır bu tanıma bağlı", "OLT'nizin yeterli")])
        self.bridge_beat("b12", "ONU nereye gidebileceğini biliyor.\nŞimdi onu taşıyalım.")
        self.save_timeline("ep17_p1C")


# ================================ PERDE 2 ======================================
XK, XH, XO, XN = -4.9, -1.9, 1.1, -6.7          # lanes: source CT · target CT · ONU · step numbers
LK, LH = (XK, XH), (XH, XO)                    # label segments
SX = (2.95, 4.45, 5.95)                         # state tiles (right panel)
ONUS = {"O5.1": OPC, "O5.2": OPC, "O8.1": TUC, "O8.2": TUC, "O9": TUC}


class Chart(Act17):
    """Shared chrome of the 11-step chart: three lanes on the left, current-state tiles on the right."""

    def chart(self):
        ln = self.lanes((XK, XH, XO), 2.2, -3.4, ("Kaynak CT · λ1", "Hedef CT · λ3", "ONU"), (SRCC, TGTC, ONUC), 1.75)
        labs = VGroup(*[T(s, 14, MUTED, BOLD).move_to([x, 2.5, 0]) for s, x in zip(("Kaynak", "Hedef", "ONU"), SX)])
        self.st = [None, None, None]
        return ln, labs

    def stile(self, i, name, color):
        return tile(name, color, 1.42, 0.42, 15, 0.22).move_to([SX[i], 2.08, 0])

    def set_states(self, changes, rt=0.4):
        """changes = {lane index: (name, colour)} → swap the state tiles."""
        anims = []
        for i, (n, c) in changes.items():
            new = self.stile(i, n, c)
            anims.append(FadeIn(new, shift=DOWN * 0.08) if self.st[i] is None else FadeTransform(self.st[i], new))
            self.st[i] = new
        self.play(*anims, run_time=rt)

    def ost(self, k):
        return OST[k][0], OST[k][2]


class E17P2A(Chart):
    HDR, MANIFEST, FIRST = H17[2], M17("p2"), True

    def construct(self):
        # c1 — planned handover between two TWDM channels: use cases; three players; an 11-step causal sequence
        self.beat("c1")
        tc = self.title_card("PERDE 2", "Devir")
        self.at(self.cue("Planlı devir", 1.4))
        self.to_header(tc)
        self.set_badge("std")
        h = self.show_heading("§17.3 — planlı devir")
        uc = VGroup(*[tag(s, GOLD, 17) for s in ("aktivasyon", "yük dengeleme", "güç tasarrufu", "kademeli büyüme", "başıboş ONU")]).arrange(RIGHT, buff=0.22).move_to([0, 1.75, 0])
        src = sbox("Kaynak CT", "λ1 · ONU'yu barındırır", SRCC, 2.8, 0.95, 21, 15).move_to([-4.0, 0.15, 0])
        tgt = sbox("Hedef CT", "λ3", TGTC, 2.8, 0.95, 21, 15).move_to([4.0, 0.15, 0])
        onu = onu_box("ONU", ONUC, 1.4, 0.65, 19).move_to([0, -0.95, 0])
        la = DashedLine(src.get_bottom(), onu.get_left(), color=SRCC, stroke_width=2.2)
        lb = DashedLine(onu.get_right(), tgt.get_bottom(), color=TGTC, stroke_width=2.2)
        mv = CurvedArrow(src.get_right() + RIGHT * 0.1, tgt.get_left() + LEFT * 0.1, angle=-0.35, color=GOLD, stroke_width=2.2, tip_length=0.12)
        st = VGroup(*[self.num(k + 1, 0, 0, GOLD, 0.24) for k in range(11)]).arrange(RIGHT, buff=0.22).move_to([0, -2.45, 0])
        stl = T("nedensel dizi · Şekil 17-1", 16, MUTED, BOLD).next_to(st, DOWN, buff=0.15)
        self.play(self.set_src("G.989.3 §17.3 · §17.3.1 · Şekil 17-1"), run_time=0.3)
        for k, (key, d) in enumerate((("aktivasyonda", 4.8), ("yük dengelemede", 6.0), ("güç tasarrufunda", 7.3), ("kademeli büyümede", 8.8), ("başıboş bir ONU", 10.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(uc[k], shift=UP * 0.06), run_time=0.35)
        self.at(self.cue("ONU'yu barındıran", 14.4))
        self.play(FadeIn(src, shift=RIGHT * 0.06), run_time=0.45)
        self.at(self.cue("hedef,", 18.3))
        self.play(FadeIn(tgt, shift=LEFT * 0.06), run_time=0.35)
        self.at(self.cue("ve ONU.", 18.8))
        self.play(FadeIn(onu, shift=UP * 0.06), Create(la), Create(lb), Create(mv), run_time=0.6)
        self.at(self.cue("on bir adımlık", 20.5))
        self.play(LaggedStart(*[FadeIn(s, scale=0.7) for s in st], lag_ratio=0.07), FadeIn(stl), run_time=1.0)
        self.end(pad=0.05)

        # c2 + c3 — steps 1–6 as a three-lane chart; ICTP commit; Ttarget / Tsource; Tuning_Control fields; ACK or NACK; source keeps granting
        self.beat("c2")
        ln, labs = self.chart()
        h = self.reset("§17.3.1 — adım 1–6", None, 0.5, extra=[FadeIn(ln), FadeIn(labs)])
        Y = {1: 1.35, 2: 0.7, 3: 0.05, 4: -0.65, 5: -1.35, 6: -2.55}
        nm = {k: self.num(k, XN, y) for k, y in Y.items()}
        d1 = VGroup(DoubleArrow([XK, Y[1], 0], [XO, Y[1], 0], buff=0.05, color=OPC, stroke_width=2.4, tip_length=0.14, max_tip_length_to_length_ratio=0.1),
                    tf("çalışma · veri", 15, OPC, BOLD).next_to([(XK + XH) / 2, Y[1], 0], UP, buff=0.07))
        ic = ictp_bar(XK, XH, Y[2], "ICTP · ayar-çıkış ⇄ ayar-giriş")
        g3 = msg3(XH, XO, Y[3], "düzenli PLOAM tahsisleri", TGTC, LH, 14, dashed=True)
        tt = tag("Ttarget ▶", TMRC, 14).move_to([XH - 0.75, Y[3] - 0.05, 0])
        ts = tag("Tsource ▶", TMRC, 14).move_to([XK - 0.85, Y[4] - 0.35, 0])
        tcm = msg3(XK, XO, Y[4], "Tuning_Control · Request", GOLD, LK, 15)
        self.at(self.cue("Bir:", 0.0))
        self.play(FadeIn(nm[1], scale=0.8), FadeIn(d1), run_time=0.4)
        self.set_states({0: self.ost(3), 1: self.ost(1), 2: ("O5.1", OPC)})
        self.play(self.set_src("G.989.3 §17.3.1 · Şekil 17-1 · Tablo 17-5 · Ek F.1.1"), run_time=0.3)
        self.at(self.cue("İki:", 2.4))
        self.play(FadeIn(nm[2], scale=0.8), FadeIn(ic[0]), run_time=0.4)
        self.at(self.cue("ICTP işlemi", 2.7))
        self.play(FadeIn(ic[1]), run_time=0.4)
        self.at(self.cue("kaynak ayar-çıkış", 6.0))
        self.set_states({0: self.ost(4)})
        self.at(self.cue("hedef ayar-giriş", 7.6))
        self.set_states({1: self.ost(2)})
        self.at(self.cue("Üç:", 12.2))
        self.play(FadeIn(nm[3], scale=0.8), run_time=0.3)
        self.at(self.cue("düzenli PLOAM tahsisleri", 14.0))
        self.play(*grow_msg(g3), run_time=0.6)
        self.at(self.cue("hedef bekleme zamanlayıcısını", 19.0))
        self.play(FadeIn(tt, scale=0.9), run_time=0.4)
        self.at(self.cue("Dört:", 22.6))
        self.play(FadeIn(nm[4], scale=0.8), run_time=0.3)
        self.at(self.cue("kaynak bekleme zamanlayıcısını", 23.6))
        self.play(FadeIn(ts, scale=0.9), run_time=0.4)
        self.at(self.cue("ayar denetimi mesajını", 26.8))
        self.play(GrowArrow(tcm[0]), FadeIn(tcm[1]), run_time=0.6)
        self.end(pad=0.05)

        self.beat("c3")
        p = apanel(4.65, 3.1, "↓ Tuning_Control 0x15 · Request", GOLD).move_to([4.55, -0.15, 0])
        rows = [("işlem kodu", "0x00 · Request"), ("hedef ↓ PON-ID", "oktet 9–12"), ("hedef ↑ PON-ID", "oktet 13–16"),
                ("planlı SFC", "6–7 · 16 bit"), ("R · geri dönüş", "oktet 8"), ("kalibrasyon biti", "oktet 17")]
        kvs = VGroup(*[kv(a, b, 15, 16, MUTED, TXT, 2.15) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        kvs.move_to(p[0]).shift(DOWN * 0.2).align_to(p[0], LEFT).shift(RIGHT * 0.22)
        kvs[3][1].set_color(GOLD)
        a5 = msg3(XO, XK, Y[5], "Tuning_Response · ACK", ACKC, LK, 15)
        n5 = msg3(XO, XK, Y[5] - 0.6, "ya da NACK · SFC çok yakın", NACKC, LK, 14, dashed=True)
        g6 = msg3(XK, XO, Y[6], "tahsisler sürer", SRCC, LK, 15, dashed=True)
        rb = tag("geri dönüş bunun için", RBC, 14).next_to([XH + 1.5, Y[6], 0], DOWN, buff=0.12)
        self.play(FadeIn(p), FadeIn(kvs[0]), run_time=0.4)
        for k, (key, d) in enumerate((("PON kimlikleri", 2.5), ("PON kimlikleri", 3.2), ("planlı süper çerçeve", 4.1), ("geri dönüş desteği", 7.1), ("kalibrasyon biti", 9.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(kvs[k + 1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("Beş:", 11.4))
        self.play(FadeIn(nm[5], scale=0.8), run_time=0.3)
        self.at(self.cue("ONU onaylar", 11.7))
        self.play(GrowArrow(a5[0]), FadeIn(a5[1]), run_time=0.5)
        self.set_states({2: ("O5.2", OPC)})
        self.at(self.cue("olumsuz cevap verir", 14.2))
        self.play(GrowArrow(n5[0][1]), Create(n5[0][0]), FadeIn(n5[1]), run_time=0.5)
        self.at(self.cue("planlı değer çok yakınsa", 16.4))
        self.play(Indicate(kvs[3], color=WARN, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("Altı:", 19.2))
        self.play(FadeIn(nm[6], scale=0.8), run_time=0.3)
        self.set_states({0: self.ost(5)})
        self.at(self.cue("tahsis vermeyi sürdürebilir", 23.4))
        self.play(Create(g6[0][0]), GrowArrow(g6[0][1]), FadeIn(g6[1]), run_time=0.6)
        self.at(self.cue("geri dönüşü mümkün", 25.9))
        self.play(FadeIn(rb, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # c4 + c5 — steps 7–11: SFC match (16 LSB of the local SFC copy), Complete_u or ROLLBACK, Request_Registration, Complete_d,
        #           ICTP confHandover; PON-TAG change → keys re-derived; source releases; operation; tuning messages use the default key
        self.beat("c4")
        rows_old = [m for m in self.mobjects if m not in (self.hdr, self.badge, h, ln, labs, *[s for s in self.st if s is not None], self.src)]
        nh = self.heading("§17.3.1 — adım 7–11")
        fit(nh, 10.0).next_to(self.hdr, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(*[FadeOut(m) for m in rows_old], FadeTransform(h, nh), run_time=0.5)
        h = nh
        Y = {7: 1.35, 8: 0.6, "8b": 0.0, 9: -0.7, "9b": -1.25, "9c": -1.85, 10: -2.45, 11: -3.05}
        nm = {k: self.num(k, XN, Y[k]) for k in (7, 8, 9, 10, 11)}
        sfl = VGroup(DashedLine([XK - 0.3, Y[7], 0], [XO + 0.3, Y[7], 0], color=GOLD, stroke_width=2.4, dash_length=0.12),
                     tf("planlı SFC = yerel SFC'nin 16 LSB'si", 15, GOLD, BOLD).next_to([(XK + XH) / 2, Y[7], 0], UP, buff=0.07))
        pf = VGroup(T("PSBd · SFC · 51 bit", 15, MUTED, BOLD), fields([("", 35, "#475569"), ("16 LSB", 16, GOLD)], 4.3, 0.45, 15, 14, True, unit=" bit"))
        pf.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.55, 0.95, 0])
        peq = VGroup(T("=", 18, GOLD, BOLD), T("planlı değer → ayar başlar", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.12).next_to(pf, DOWN, buff=0.35).align_to(pf, RIGHT)
        cu = msg3(XO, XH, Y[8], "Tuning_Resp. · Complete_u", CMPC, LH, 15)
        rbk = msg3(XO, XK, Y["8b"], "ya da ROLLBACK · R = 1", RBC, LK, 14, dashed=True)
        rr = msg3(XH, XO, Y[9], "Request_Registration", TGTC, LH, 15)
        rr.add(tag("isteğe bağlı", TGTC, 14).move_to([XH - 1.0, Y[9], 0]))
        cd = msg3(XH, XO, Y["9b"], "Tuning_Control · Complete_d", TGTC, LH, 15)
        ic2 = ictp_bar(XK, XH, Y["9c"], "ICTP · devri onayla")
        self.at(self.cue("Yedi:", 0.0))
        self.play(FadeIn(nm[7], scale=0.8), run_time=0.3)
        self.at(self.cue("PSBd'den kopyalanan", 1.5))
        self.play(FadeIn(pf, shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("en düşük on altı bitine", 4.5))
        self.play(Create(sfl[0]), FadeIn(sfl[1]), FadeIn(peq, shift=LEFT * 0.05), run_time=0.6)
        self.at(self.cue("ONU ayara başlar", 7.0))
        self.set_states({2: ("O8.1", TUC)})
        self.at(self.cue("Sekiz:", 8.8))
        self.play(FadeIn(nm[8], scale=0.8), run_time=0.3)
        self.at(self.cue("yeni kanalda senkron", 9.3))
        self.set_states({2: ("O8.2", TUC)})
        self.at(self.cue("ayar tamamlandı yanıtıyla", 13.0))
        self.play(GrowArrow(cu[0]), FadeIn(cu[1]), run_time=0.5)
        self.set_states({2: ("O9", TUC)})
        self.at(self.cue("ayar başarısızsa", 16.0))
        self.play(Create(rbk[0][0]), GrowArrow(rbk[0][1]), FadeIn(rbk[1]), run_time=0.6)
        self.at(self.cue("Dokuz:", 23.3))
        self.play(FadeIn(nm[9], scale=0.8), run_time=0.3)
        self.at(self.cue("kayıt isteğiyle", 25.0))
        self.play(GrowArrow(rr[0]), FadeIn(rr[1:]), run_time=0.5)
        self.at(self.cue("ayar denetiminin tamamlandı", 27.6))
        self.play(GrowArrow(cd[0]), FadeIn(cd[1]), run_time=0.5)
        self.set_states({1: self.ost(3), 2: ("O5.1", OPC)})
        self.at(self.cue("ICTP ile devri", 31.5))
        self.play(FadeIn(ic2[0]), FadeIn(ic2[1]), run_time=0.5)
        self.end(pad=0.05)

        self.beat("c5")
        kp = apanel(4.65, 2.15, "PON-TAG değişti →", PINK).move_to([4.55, -1.15, 0])
        ks = VGroup(*[tag(s, PINK, 15) for s in ("SK", "OMCI_IK", "PLOAM_IK", "KEK")]).arrange(RIGHT, buff=0.12)
        kl = T("yeniden türetilir", 16, PINK, BOLD)
        kg = VGroup(ks, kl).arrange(DOWN, buff=0.15).move_to(kp[0]).shift(DOWN * 0.15)
        fit(kg, 4.3)
        g10 = msg3(XK, XO, Y[10], "tahsisler kesilir", SRCC, LK, 15, dashed=True)
        g10 = VGroup(g10[0], VGroup(g10[1], T("yapılar bırakılır", 14, SRCC, BOLD).next_to([(XK + XH) / 2, Y[10], 0], DOWN, buff=0.08)))
        x10 = xmark(Square(0.3).move_to([(XH + XO) / 2, Y[10], 0]), WARN, 3.5, 0.0)
        op = VGroup(DoubleArrow([XH, Y[11], 0], [XO, Y[11], 0], buff=0.05, color=OPC, stroke_width=2.6, tip_length=0.14, max_tip_length_to_length_ratio=0.12),
                    tf("çalışma · veri", 15, OPC, BOLD).next_to([(XH + XO) / 2, Y[11], 0], UP, buff=0.07))
        dk = VGroup(T("ayar mesajları:", 16, TXT, BOLD), keychip(True, 15)).arrange(RIGHT, buff=0.15).move_to([4.55, -2.75, 0])
        yr = VGroup(interp("yorum", GOLD, 14), T("etiket değişse de doğrulanır", 15, GOLD, BOLD)).arrange(RIGHT, buff=0.12).next_to(dk, DOWN, buff=0.15)
        VGroup(dk, yr).move_to([4.6, -2.95, 0])
        self.play(FadeOut(VGroup(pf, peq)), run_time=0.3)
        self.at(self.cue("Burst profilindeki PON etiketi", 0.2))
        self.play(FadeIn(kp), run_time=0.4)
        self.at(self.cue("anahtarlarını yeniden türetir", 5.5))
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.05) for k in ks], lag_ratio=0.15), FadeIn(kl), run_time=0.7)
        self.at(self.cue("On:", 8.0))
        self.play(FadeIn(nm[10], scale=0.8), run_time=0.3)
        self.at(self.cue("kaynak tahsisleri keser", 8.2))
        self.play(Create(g10[0][0]), GrowArrow(g10[0][1]), FadeIn(g10[1]), run_time=0.5)
        self.play(Create(x10), run_time=0.3)
        self.at(self.cue("yapılarını bırakır", 11.0))
        self.set_states({0: self.ost(1)})
        self.at(self.cue("On bir:", 12.8))
        self.play(FadeIn(nm[11], scale=0.8), run_time=0.3)
        self.at(self.cue("hedef ve ONU çalışmaya", 13.4))
        self.play(GrowFromCenter(op[0]), FadeIn(op[1]), run_time=0.5)
        self.at(self.cue("varsayılan anahtarla", 17.5))
        self.play(FadeOut(VGroup(kp, kg)), FadeIn(dk, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("etiket değişse de", 22.0))
        self.play(FadeIn(yr, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p2A")


def timer(s, kind="▶", color=TMRC, size=15):
    """Timer chip: 'TO4 ▶' (start), 'TO6 ■' (stop)."""
    return tag(f"{s} {kind}", WARN if kind == "■" else color, size)


def trow(items, buff=0.14):
    """Row of mobjects/strings (strings → T 16 bold)."""
    return VGroup(*[T(i, 16, TXT, BOLD) if isinstance(i, str) else i for i in items]).arrange(RIGHT, buff=buff)


class E17P2B(Act17):
    HDR, MANIFEST, FIRST = H17[2], M17("p2"), True
    PREV_BADGE = "std"

    def sm(self):
        sm = OnuSM()
        e = sm.main_edges()
        return sm, e

    def construct(self):
        # c6 — ONU view (Tables 12-1/12-4): O5.2 keeps data but starts no new fragmentation (idle XGEM fill); SFC match: Rx(+Tx) →
        #      stop TO6, start TO4, Discard I → O8.1; Tx only → DS not interrupted, start TO5 → O9
        self.beat("c6")
        h = self.show_heading("ONU'nun gözünden — O5.2 · O8 · O9")
        sm, e = self.sm()
        dsy = T("DSYNC", 14, TUC, BOLD).next_to(e["o82"][0], UP, buff=0.05)
        self.play(FadeIn(sm.boxes("O5.1", "O5.2")), FadeIn(sm.fr["O5"]), FadeIn(e["tune"]), self.set_src("G.989.3 Tablo 12-1 · Tablo 12-4 · Amd.1 · Amd.2"), run_time=0.6)
        pt = VGroup(T("O5.2 · bekleyen", 20, OPC, BOLD), T("veri sürer", 17, TXT, BOLD)).arrange(RIGHT, buff=0.3).move_to([-6.4, 1.85, 0], aligned_edge=LEFT)
        bs = strip([(0.3, "H", SAC, 0.55), (1.0, "SDU sonu", SAC, 0.14), (0.3, "H", SAC, 0.55), (1.5, "tam SDU", SAC, 0.14), (2.0, "boş XGEM", IDC, 0.12)], -6.4, 1.0, 0.55, 15)
        b1 = brace_lbl(bs[:2], "parçalanmakta olanı bitir", SAC, DOWN, 14)
        b3 = brace_lbl(bs[4], "sığmayan yer", IDC, DOWN, 14)
        nf = VGroup(T("yeni SDU parçalanmaz", 16, WARN, BOLD), ok_x(False, 16)).arrange(RIGHT, buff=0.1).move_to([-3.6, -0.15, 0])
        sh = T("Sayaç eşleşince:", 18, GOLD, BOLD).move_to([-6.4, -0.85, 0], aligned_edge=LEFT)
        ra = VGroup(tag("↓ (+↑) ayar", TUC, 15), timer("TO6", "■"), timer("TO4"), tag("Discard I · burst profilleri", WARN, 15), T("→ O8.1", 16, TUC, BOLD))
        VGroup(*ra[:3]).arrange(RIGHT, buff=0.1)
        VGroup(*ra[3:]).arrange(RIGHT, buff=0.12).next_to(ra[0], DOWN, buff=0.14).align_to(ra[1], LEFT)
        rb_ = VGroup(tag("yalnız ↑ ayar", TUC, 15), T("↓ kesilmez", 16, GOOD, BOLD), timer("TO5"), T("→ O9", 16, TUC, BOLD)).arrange(RIGHT, buff=0.12)
        rows = VGroup(ra, rb_).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-6.4, -1.95, 0], aligned_edge=LEFT)
        self.at(self.cue("O5.2'de veri sürer", 1.4))
        self.play(Indicate(sm.b["O5.2"], color=OPC, scale_factor=1.08), FadeIn(pt), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.05) for b in bs[:4]], lag_ratio=0.15), FadeIn(b1), run_time=0.8)
        self.at(self.cue("parçalamaya başlamaz", 5.5))
        self.play(FadeIn(nf, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("boş XGEM çerçeveleriyle", 8.8))
        self.play(FadeIn(bs[4], shift=RIGHT * 0.05), FadeIn(b3), run_time=0.5)
        self.at(self.cue("Sayaç eşleşince", 11.7))
        self.play(FadeIn(sh), FadeIn(e["sfcl"]), run_time=0.4)
        self.at(self.cue("TO6 durur", 13.6))
        self.play(FadeIn(ra[0]), FadeIn(ra[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("TO4 başlar", 15.8))
        self.play(FadeIn(ra[2], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("burst profilleri atılır", 16.8))
        self.play(FadeIn(ra[3], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("O8.1'e girer", 18.8))
        self.play(FadeIn(ra[4]), GrowArrow(e["sfcrx"][0]), FadeIn(sm.b["O8.1"]), run_time=0.5)
        self.at(self.cue("Yalnızca verici", 20.5))
        self.play(FadeIn(rb_[0]), FadeIn(rb_[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("TO5 başlar", 24.6))
        self.play(FadeIn(rb_[2], shift=LEFT * 0.05), run_time=0.3)
        self.at(self.cue("doğrudan O9", 26.2))
        self.play(FadeIn(rb_[3]), GrowArrow(e["sfctx"][0]), FadeIn(sm.b["O9"]), run_time=0.5)
        self.end(pad=0.05)

        # c7 — O8.2 (Amd.2): collect the new channel's profiles; partition, US link type and US rate match → ok to work: stop TO4,
        #      start TO5 → O9; else Discard I → O8.1; calibration no longer checked here
        self.beat("c7")
        left = VGroup(pt, bs, b1, b3, nf, sh, rows)
        p2 = VGroup(T("O8.2 · profil öğrenme", 20, TUC, BOLD), tag("Amd.2 · 2025", AMDC, 15)).arrange(RIGHT, buff=0.25).move_to([-6.4, 1.85, 0], aligned_edge=LEFT)
        cl = VGroup(chk("kanal bölümlemesi uyuşuyor"), chk("↑ bağlantı tipi uyuşuyor"), chk("↑ hat hızı uyuşuyor")).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cl.move_to([-6.3, 0.55, 0], aligned_edge=LEFT)
        okr = VGroup(tag("çalışmaya uygun", GOOD, 15), timer("TO4", "■"), timer("TO5"), T("→ O9", 16, TUC, BOLD)).arrange(RIGHT, buff=0.12).move_to([-6.4, -0.75, 0], aligned_edge=LEFT)
        nor = VGroup(tag("uygun değil", WARN, 15), tag("Discard I", WARN, 15), T("→ O8.1", 16, TUC, BOLD)).arrange(RIGHT, buff=0.12).move_to([-6.4, -1.45, 0], aligned_edge=LEFT)
        cal = VGroup(T("kalibrasyon doğruluğu", 16, MUTED, BOLD), T("artık burada denetlenmez", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([-6.3, -2.35, 0], aligned_edge=LEFT)
        st_ = strike(cal[0], WARN, 2.5)
        self.at(self.cue("Senkron gelince", 0.0))
        self.play(FadeOut(left), GrowArrow(e["o82"][0]), FadeIn(dsy), FadeIn(sm.b["O8.2"]), FadeIn(sm.fr["O8"]), run_time=0.6)
        self.play(FadeIn(p2[0]), run_time=0.3)
        self.at(self.cue("profillerini toplar", 2.5))
        self.play(Indicate(sm.b["O8.2"], color=TUC, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("İki bin yirmi beş", 4.9))
        self.play(FadeIn(p2[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("bölümleme,", 9.5))
        self.play(FadeIn(cl[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("yukarı yön bağlantı tipi", 10.4))
        self.play(FadeIn(cl[1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("ve hızı uyuşuyorsa", 12.3))
        self.play(FadeIn(cl[2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("çalışmaya uygundur", 14.4))
        self.play(FadeIn(okr[0]), run_time=0.3)
        self.at(self.cue("TO4 durur", 16.2))
        self.play(FadeIn(okr[1:3], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("ONU O9'a geçer", 18.0))
        self.play(FadeIn(okr[3]), GrowArrow(e["o89"][0]), run_time=0.4)
        self.at(self.cue("Uymuyorsa", 19.2))
        self.play(FadeIn(nor, shift=RIGHT * 0.05), Indicate(sm.b["O8.1"], color=WARN, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("Kalibrasyon artık", 23.4))
        self.play(FadeIn(cal), run_time=0.4)
        self.play(Create(st_), run_time=0.3)
        self.end(pad=0.05)

        # c8 — O9: Complete_u on every directed PLOAM grant of the target until feedback or TO5; uncalibrated → wait for an AMCC grant;
        #      TO5 initial value depends on it; feedback = Complete_d or Request_Registration / Assign_Alloc-ID / Key_Control / Sleep_Allow;
        #      stop TO5, start TO6 → O5
        self.beat("c8")
        p3 = T("O9 · ↑ ayar", 20, TUC, BOLD).move_to([-6.4, 1.85, 0], aligned_edge=LEFT)
        r1 = VGroup(T("her yönlendirilmiş PLOAM tahsisine →", 16, TXT, BOLD), mbox("Complete_u", CMPC, None, 0.36, 15)).arrange(RIGHT, buff=0.15)
        r2 = T("dönüş gelene ya da TO5 dolana kadar", 16, MUTED, BOLD)
        r3 = VGroup(T("bant içi kalibre değil →", 16, TXT, BOLD), tag("AMCC yönlendirilmiş tahsis bekle", GOLD, 15)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        r4 = VGroup(T("TO5 başlangıç değeri buna bağlı ·", 16, TXT, BOLD), T("değer yok", 16, WARN, BOLD)).arrange(RIGHT, buff=0.12)
        r5h = T("dönüş (↑ ayar onayı):", 16, GOOD, BOLD)
        r5 = VGroup(*[mbox(s, c, None, 0.38, 15) for s, c in (("Complete_d", TGTC), ("Request_Registration", SNC), ("Assign_Alloc-ID", SNC),
                                                             ("Key_Control", PINK), ("Sleep_Allow", "#C084FC"))])
        r5a = VGroup(*r5[:2]).arrange(RIGHT, buff=0.1)
        r5b = VGroup(*r5[2:]).arrange(RIGHT, buff=0.1)
        r6 = VGroup(timer("TO5", "■"), timer("TO6"), T("→ O5", 17, OPC, BOLD)).arrange(RIGHT, buff=0.12)
        col = VGroup(r1, r2, r3, r4, r5h, r5a, r5b, r6).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        fit(col, 5.4).move_to([-6.35, -0.7, 0], aligned_edge=LEFT)
        self.play(FadeOut(VGroup(p2, cl, okr, nor, cal, st_)), FadeIn(p3), Indicate(sm.b["O9"], color=TUC, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("her yönlendirilmiş PLOAM", 1.5))
        self.play(FadeIn(r1, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("dönüş gelene", 6.8))
        self.play(FadeIn(r2), run_time=0.4)
        self.at(self.cue("Bant içi için kalibre", 9.8))
        self.play(FadeIn(r3, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("başlangıç değeri", 16.5))
        self.play(FadeIn(r4, shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Dönüş,", 19.1))
        self.play(FadeIn(r5h), run_time=0.3)
        for k, (key, d) in enumerate((("tamamlandı biçimidir", 20.5), ("kayıt isteği", 23.2), ("tahsis kimliği atama", 24.8), ("anahtar denetimi", 26.5), ("uyku izni", 28.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(r5[k], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Sonra TO5 durur", 29.2))
        self.play(FadeIn(r6[0]), run_time=0.3)
        self.at(self.cue("TO6 başlar", 30.6))
        self.play(FadeIn(r6[1]), run_time=0.3)
        self.at(self.cue("ONU O5'e döner", 31.5))
        self.play(FadeIn(r6[2]), GrowArrow(e["o95"][0]), Indicate(sm.b["O5.1"], color=OPC, scale_factor=1.08), run_time=0.6)
        self.end(pad=0.05)

        # c9 — Scheduled SFC = 16 LSBs of the SFC; our arithmetic: wraps every 65 536 frames = 8.192 s → a farther target is ambiguous;
        #      no lower bound written, but the ONU's answer may take 6 frames
        self.beat("c9")
        h = self.reset("Planlı SFC — 16 bitlik bir ufuk", rt=0.5)
        sfc = fields([("süper çerçeve sayacı · üst 35 bit", 35, "#475569"), ("planlı SFC", 16, GOLD)], 11.6, 0.55, 17, 14, True, unit=" bit").move_to([0, 1.55, 0])
        sfl = T("PSBd · SFC · 51 bit", 15, MUTED, BOLD).next_to(sfc, UP, buff=0.1).align_to(sfc, LEFT)
        c0 = np.array([-4.4, -1.4, 0])
        R = 1.45
        ring = Circle(radius=R, stroke_color=GOLD, stroke_width=3).move_to(c0)
        tk = VGroup(*[Line(c0 + R * 0.86 * np.array([np.cos(a), np.sin(a), 0]), c0 + R * np.array([np.cos(a), np.sin(a), 0]), color=GOLD, stroke_width=1.5)
                      for a in np.linspace(0, TAU, 16, endpoint=False)])
        z = T("16 bit · 0 … 65 535", 14, GOLD, BOLD).next_to(ring, DOWN, buff=0.12)
        now = Dot(c0 + R * UP, radius=0.09, color=TXT)
        nl = T("şimdi", 15, TXT, BOLD).next_to(now, UP, buff=0.1)
        ang = -PI * 0.55
        tgt = Dot(c0 + R * np.array([np.cos(PI / 2 + ang), np.sin(PI / 2 + ang), 0]), radius=0.09, color=GOLD)
        tl = T("planlı", 15, GOLD, BOLD).next_to(tgt, RIGHT, buff=0.32)
        arc = Arc(radius=R + 0.18, start_angle=PI / 2, angle=ang, arc_center=c0, color=GOLD, stroke_width=4)
        wrap = VGroup(T("65 536 çerçeve", 20, GOLD, BOLD), T("= 8,192 s", 22, GOLD, BOLD), interp("hesap", GOLD, 14)).arrange(DOWN, buff=0.08).move_to(c0)
        amb = VGroup(T("daha uzak hedef", 16, WARN, BOLD), T("aynı 16 bit → belirsiz", 16, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(ring, RIGHT, buff=0.35).shift(UP * 0.6)
        ax = Line([1.5, -1.55, 0], [6.6, -1.55, 0], color=MUTED, stroke_width=2)
        m0 = tmark(1.7, -1.85, -0.7, "Tuning_Control", GOLD, 14)
        m1 = tmark(6.3, -1.85, -0.7, "planlı SFC", GOLD, 14)
        zone = Rectangle(width=1.5, height=0.4, stroke_width=0, fill_color=WARN, fill_opacity=0.25).move_to([2.45, -1.55, 0])
        zl = VGroup(T("≤ 6 çerçeve · 750 µs", 15, WARN, BOLD), T("ONU cevabı", 15, WARN, BOLD)).arrange(DOWN, buff=0.04).next_to(zone, DOWN, buff=0.12)
        lb = VGroup(T("alt sınır:", 16, TXT, BOLD), T("yazılı değil", 16, WARN, BOLD)).arrange(RIGHT, buff=0.12).move_to([5.0, -2.35, 0])
        lead = T("öncülük süresi", 15, MUTED, BOLD).move_to([4.6, -1.3, 0])
        self.play(self.set_src("G.989.3 §17.3.1 · Tablo 11-16 · §11.1.2 · PSBd SFC (§10)"), run_time=0.3)
        self.at(self.cue("en düşük on altı bitidir", 3.5))
        self.play(FadeIn(sfl), FadeIn(sfc[0]), run_time=0.4)
        self.play(FadeIn(sfc[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("altmış beş bin", 5.8))
        self.play(Create(ring), FadeIn(tk), FadeIn(z), FadeIn(now), FadeIn(nl), run_time=0.7)
        self.play(FadeIn(tgt), FadeIn(tl), Create(arc), run_time=0.5)
        self.play(FadeIn(wrap[0]), run_time=0.3)
        self.at(self.cue("sekiz virgül bir", 10.9))
        mv = Dot(c0 + R * UP, radius=0.07, color=ACC)
        self.play(FadeIn(wrap[1:]), MoveAlongPath(mv, Arc(radius=R, start_angle=PI / 2, angle=-TAU, arc_center=c0)), run_time=1.6)
        self.remove(mv)
        self.at(self.cue("daha uzak bir hedef", 14.8))
        self.play(FadeIn(amb, shift=LEFT * 0.05), Indicate(tgt, color=WARN, scale_factor=1.6), run_time=0.6)
        self.at(self.cue("Alt sınır yazılı", 17.5))
        self.play(Create(ax), FadeIn(m0), FadeIn(m1), FadeIn(lead), FadeIn(lb), run_time=0.6)
        self.at(self.cue("altı çerçeve sürebilir", 20.0))
        self.play(FadeIn(zone), FadeIn(zl, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep17_p2B")


class E17P2C(Act17):
    HDR, MANIFEST, FIRST = H17[2], M17("p2"), True
    PREV_BADGE = "std"

    def bm_row(self, table, label, color, y, value=None, idx=True):
        bm = bitmap16(table, value, 0.58, 0.48, 15, idx)
        lab = VGroup(T(label, 17, color, BOLD), T("oktet 6–7", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=RIGHT, buff=0.04)
        g = VGroup(lab, bm).arrange(RIGHT, buff=0.3)
        g.move_to([0.0, y, 0])
        return g

    def code_rows(self, items, x, y, dy=0.42, size=14, w=None):
        g = VGroup()
        for k, (b, grp, code, cond) in enumerate(items):
            c = code_chip(b, code, grp, size, w=2.05)
            t = T(cond, 15, TXT, BOLD).next_to(c, RIGHT, buff=0.15)
            r = VGroup(c, t)
            r.move_to([x, y - k * dy, 0], aligned_edge=LEFT)
            g.add(r)
        return g

    def construct(self):
        # c10 — NACK: Tuning_Response opcode 0x01; 16-bit condition map; 14 conditions in three groups (INT 1 · DS 6 · US 7)
        self.beat("c10")
        h = self.show_heading("Olumsuz cevap — Tablo 17-3")
        op = VGroup(T("↑ Tuning_Response 0x1A · oktet 5", 16, MUTED, BOLD), HX("0x01", 18, NACKC, BOLD), T("NACK · ayardan önce", 17, NACKC, BOLD)).arrange(RIGHT, buff=0.2)
        op.move_to([0, 2.05, 0])
        row = self.bm_row(NACK, "NACK", NACKC, 1.05)
        cells = row[1][0]
        br = VGroup(brace_lbl(cells[15], "INT", GRC["INT"], DOWN, 14), brace_lbl(cells[9:15], "DS · 6", GRC["DS"], DOWN, 15),
                    brace_lbl(cells[2:9], "US · 7", GRC["US"], DOWN, 15), brace_lbl(cells[0:2], "ayrılmış", MUTED, DOWN, 14))
        ints = self.code_rows(NACK[:1], -6.45, -0.45)
        dss = self.code_rows(NACK[1:7], -6.45, -0.95)
        uss = self.code_rows(NACK[7:], 0.35, -0.45)
        cnt = T("14 koşul · 3 grup", 18, GOLD, BOLD).next_to(row, RIGHT, buff=0.2).shift(UP * 0.55)
        self.play(self.set_src("G.989.3 §17.3.2 · Tablo 17-3 · Tuning_Response (Tablo 11-30)"), run_time=0.3)
        self.at(self.cue("işlem kodu birdir", 1.2))
        self.play(FadeIn(op, shift=DOWN * 0.05), run_time=0.5)
        self.at(self.cue("on altı bitlik", 4.1))
        self.play(FadeIn(row[0]), LaggedStart(*[FadeIn(c) for c in row[1][0]], lag_ratio=0.04), FadeIn(row[1][1]), run_time=0.9)
        self.at(self.cue("on dört koşul", 8.1))
        self.play(FadeIn(br[1:]), FadeIn(br[0]), run_time=0.5)
        self.at(self.cue("İç grupta tek kod", 10.0))
        self.play(Indicate(cells[15], color=GRC["INT"], scale_factor=1.3), run_time=0.4)
        self.at(self.cue("ONU planlı çerçevede", 11.6))
        self.play(FadeIn(ints, shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Aşağı yönde altı", 14.4))
        self.play(Indicate(VGroup(*cells[9:15]), color=GRC["DS"], scale_factor=1.05), run_time=0.4)
        for k, (key, d) in enumerate((("yönetim etiketi", 15.9), ("boş tanım,", 17.3), ("bölüm,", 18.2), ("alıcı ayar aralığı", 18.7), ("hız ve hat kodu.", 20.3))):
            self.at(self.cue(key, d))
            sel = dss[k:k + 1] if k < 4 else dss[4:6]
            self.play(FadeIn(sel, shift=RIGHT * 0.05), run_time=0.25)
        self.at(self.cue("Yukarı yönde yedi", 21.7))
        self.play(Indicate(VGroup(*cells[2:9]), color=GRC["US"], scale_factor=1.05), run_time=0.4)
        for k, (key, d) in enumerate((("etiket,", 23.3), ("boş tanım,", 23.9), ("verici aralığı", 24.7), ("kalibrasyon,", 26.0), ("bağlantı tipi", 27.1), ("hız ve hat kodu", 28.3))):
            self.at(self.cue_n(key, 2, d) if key in ("boş tanım,", "hız ve hat kodu") else self.cue(key, d))
            sel = uss[k:k + 1] if k < 5 else uss[5:7]
            self.play(FadeIn(sel, shift=RIGHT * 0.05), run_time=0.25)
        self.end(pad=0.05)

        # c11 — US_CLBR suppressed by the calibration flag; US_LNCD tests a field no profile carries (our reading); codes OR: 0x0210
        self.beat("c11")
        lists = VGroup(ints, dss, uss)
        d1 = VGroup(code_chip(0x0400, "US_CLBR", "US", 15), T("hedefteki doğruluk < bant içi eşiği → konur", 16, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        d1b = VGroup(T("ama Tuning_Control kalibrasyon biti = 1 →", 16, TXT, BOLD), tag("bastırılır", GOOD, 15),
                     T("ONU gereken kalibrasyonla ayar yapar", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.15)
        d2 = VGroup(code_chip(0x2000, "US_LNCD", "US", 15), T("hiçbir profil mesajında ↑ hat kodu alanı yok", 16, TXT, BOLD), interp("bizim okumamız", GOLD, 14)).arrange(RIGHT, buff=0.2)
        blk = VGroup(d1, d1b, d2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        fit(blk, 12.6).move_to([0, -0.85, 0])
        cmb = VGroup(HX("0x0210", 22, GOLD, BOLD), T("=", 20, TXT, BOLD), code_chip(0x0200, "US_TUNR", "US", 15), T("+", 20, TXT, BOLD),
                     code_chip(0x0010, "DS_TUNR", "DS", 15), T("→ alıcı ve verici aralığı birden", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        fit(cmb, 12.6).move_to([0, -2.65, 0])
        self.play(FadeOut(lists), run_time=0.4)
        self.at(self.cue("Kalibrasyon kodu", 1.0))
        self.play(FadeIn(d1, shift=UP * 0.05), Indicate(cells[5], color=GOLD, scale_factor=1.3), run_time=0.6)
        self.at(self.cue("kalibrasyon biti birse", 7.5))
        self.play(FadeIn(d1b[:2], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("gereken kalibrasyonla", 12.5))
        self.play(FadeIn(d1b[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("yukarı yön hat kodu koşulu", 15.2))
        self.play(FadeIn(d2[0]), Indicate(cells[2], color=GOLD, scale_factor=1.3), run_time=0.5)
        self.at(self.cue("hiçbir profil mesajında", 18.9))
        self.play(FadeIn(d2[1:], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("Kodlar birleşebilir", 22.9))
        self.play(*set_bits(row[1], 0x0210, NACK), run_time=0.6)
        self.at(self.cue("sıfır iki bir sıfır", 24.6))
        self.play(FadeIn(cmb[:5], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("alıcı ve verici aralığı", 27.9))
        self.play(FadeIn(cmb[5], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # c12 — ROLLBACK (opcode 0x04, after tuning): 9 conditions (COM 1 · DS 2 · US 6); same bit, different meaning (0x0004, 0x0010)
        self.beat("c12")
        h = self.reset("Geri dönüş — Tablo 17-4", rt=0.5)
        r1 = self.bm_row(NACK, "NACK · 0x01", NACKC, 1.75, None, True)
        r2 = self.bm_row(RBK, "ROLLBACK · 0x04", RBC, 0.75, None, False)
        r2[1].align_to(r1[1], LEFT)
        r2[0].align_to(r1[0], RIGHT)
        coms = self.code_rows(RBK[:3], -6.45, -0.25)
        uss2 = self.code_rows(RBK[3:], 0.35, -0.25)
        bk = [SurroundingRectangle(VGroup(r1[1][0][15 - b], r2[1][0][15 - b]), color=GOLD, buff=0.06, stroke_width=3) for b in (2, 4)]
        cmp = VGroup(
            VGroup(HX("0x0004", 18, GOLD, BOLD), T("NACK →", 16, NACKC, BOLD), code_chip(0x0004, "DS_VOID", "DS", 15), T("boş ↓ tanım", 16, TXT, BOLD),
                   T("· ROLLBACK →", 16, RBC, BOLD), code_chip(0x0004, "DS_LKTP", "DS", 15), T("bağlantı tipi", 16, TXT, BOLD)).arrange(RIGHT, buff=0.14),
            VGroup(HX("0x0010", 18, GOLD, BOLD), T("NACK →", 16, NACKC, BOLD), code_chip(0x0010, "DS_TUNR", "DS", 15), T("alıcı aralığı", 16, TXT, BOLD),
                   T("· ROLLBACK →", 16, RBC, BOLD), code_chip(0x0010, "US_VOID", "US", 15), T("boş ↑ tanım", 16, TXT, BOLD)).arrange(RIGHT, buff=0.14)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(cmp, 12.8).move_to([0, -1.25, 0])
        rule = VGroup(T("çözerken:", 18, TXT, BOLD), T("önce oktet 5 · işlem kodu", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.7, 0])
        self.play(FadeIn(r1), self.set_src("G.989.3 §17.3.2 · Tablo 17-4 · Tablo 17-3"), run_time=0.4)
        self.at(self.cue("işlem kodu dört", 0.9))
        self.play(FadeIn(r2[0]), LaggedStart(*[FadeIn(c) for c in r2[1][0]], lag_ratio=0.04), run_time=0.8)
        self.at(self.cue("Hedef aşağı yönde senkron", 4.7))
        self.play(FadeIn(coms[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("PSBd'sindeki etiket", 8.5))
        self.play(FadeIn(coms[1:], shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("kanal profili ONU ile", 13.0))
        self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.05) for u in uss2], lag_ratio=0.12), run_time=0.9)
        self.at(self.cue("Aynı bit iki tabloda", 16.1))
        self.play(FadeOut(coms), FadeOut(uss2), Create(bk[0]), Create(bk[1]), run_time=0.6)
        self.at(self.cue("Değeri dört olan bit", 19.6))
        self.play(FadeIn(cmp[0][:5], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("geri dönüşte bağlantı tipidir", 24.0))
        self.play(FadeIn(cmp[0][5:], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("on altı olan bit", 26.5))
        self.play(FadeIn(cmp[1][:5], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("boş yukarı yön tanımıdır", 29.5))
        self.play(FadeIn(cmp[1][5:], shift=RIGHT * 0.05), FadeIn(rule, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # c13 — OLT wavelength handover state machine (Tables 17-5 … 17-9): five states, the normal path, failures, alerts, custody
        self.beat("c13")
        h = self.reset("OLT devir makinesi — Tablo 17-5 … 17-9", rt=0.5)
        sm = OltSM(dy=-0.1)
        e12 = sm.edge(1, "T", 2, "L", "ayar-giriş\nTtarget ▶", TGTC, 0.3, 0.0, LEFT, 0.1, 15)
        e23 = sm.edge(2, "R", 3, "L", "Complete_u", TGTC, 0.12, 0.12, UP, 0.06, 15)
        e34 = sm.edge(3, "R", 4, "T", "ayar-çıkış\nTsource ▶", SRCC, 0.0, 0.3, RIGHT, 0.1, 15)
        e45 = sm.edge(4, "B", 5, "R", "ACK", SRCC, 0.0, 0.0, DOWN + RIGHT * 0.4, 0.05, 15)
        e51 = sm.edge(5, "L", 1, "B", "ICTP onayı", SRCC, 0.0, 0.0, DOWN + LEFT * 0.4, 0.05, 15)
        f43 = sm.edge(4, "L", 3, "B", "NACK", NACKC, 0.12, 0.45, DOWN, 0.08, 15)
        f53 = sm.edge(5, "T", 3, "B", "ROLLBACK", RBC, 0.4, -0.45, LEFT, 0.1, 15)
        f21 = sm.edge(2, "B", 1, "R", "iptal", NACKC, 0.0, 0.12, RIGHT, 0.08, 15)
        lh = tag("hedef CT", TGTC, 15).move_to([-4.6, 1.3, 0])
        lk = tag("kaynak CT", SRCC, 15).move_to([5.0, 1.0, 0])
        ab = VGroup(T("kaynak → hedefe", 16, NACKC, BOLD), tag("ICTP iptal", NACKC, 15)).arrange(RIGHT, buff=0.12).move_to([0.0, 0.25, 0])
        al = VGroup(T("zamanlayıcı doldu →", 16, TXT, BOLD), tag("ICTP uyarısı", ICTC, 15), T("· yayın · bütün kanallar", 16, ICTC, BOLD)).arrange(RIGHT, buff=0.12)
        al.move_to([3.4, -3.15, 0])
        cus = VGroup(T("hata →", 17, TXT, BOLD), tag("velayet: kaynak", HOC, 16), T("çünkü onunla çalıştığı bilinir", 16, MUTED, BOLD)).arrange(RIGHT, buff=0.12)
        cus.move_to([-3.4, -3.15, 0])
        fit(VGroup(al, cus), 13.4)
        self.play(self.set_src("G.989.3 §17.3.3 · Tablo 17-5 … 17-9 · Ek F"), run_time=0.3)
        self.at(self.cue("habersiz,", 2.6))
        for k, (key, d) in enumerate((("habersiz,", 2.6), ("bekleme,", 3.4), ("barındırma,", 4.0), ("yönlendirme ve", 5.0), ("ve uğurlama", 5.8))):
            self.at(self.cue(key, d))
            self.play(FadeIn(sm.b[k + 1], scale=0.9), run_time=0.3)
        self.at(self.cue("Hedef ayar-girişle", 7.0))
        self.play(FadeIn(lh), *grow_msg(e12), run_time=0.6)
        self.at(self.cue("tamamlandı yanıtıyla barındırmaya", 9.4))
        self.play(*grow_msg(e23), run_time=0.5)
        self.at(self.cue("kaynak ayar-çıkışla", 12.3))
        self.play(FadeIn(lk), *grow_msg(e34), run_time=0.6)
        self.at(self.cue("onayla uğurlamaya", 15.2))
        self.play(*grow_msg(e45), run_time=0.5)
        self.at(self.cue("ICTP onayıyla", 16.7))
        self.play(*grow_msg(e51), run_time=0.5)
        self.at(self.cue("Olumsuz cevapta", 19.2))
        self.play(*grow_msg(f43), run_time=0.5)
        self.at(self.cue("ve geri dönüşte", 20.6))
        self.play(*grow_msg(f53), run_time=0.5)
        self.at(self.cue("hedefe iptal yollar", 24.0))
        self.play(FadeIn(ab, shift=UP * 0.05), *grow_msg(f21), run_time=0.6)
        self.at(self.cue("bir zamanlayıcı dolarsa", 26.1))
        self.play(FadeIn(al, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("velayeti kaynaktadır", 32.5))
        self.play(FadeIn(cus[:2], shift=UP * 0.05), Indicate(sm.b[3], color=HOC, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("çünkü onunla", 35.6))
        self.play(FadeIn(cus[2], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # c14 — PMD bridge S1·B10: life of an ONU, step 10 = handover at an SFC; TO4, TO5, Ttarget, Tsource: no values; Tsource > Ttarget;
        #       our inference: Ttarget starts before the tuning request → must also cover the Scheduled SFC lead time
        self.beat("c14")
        h, chp = self.pmd_reset("PMD Köprüsü — devrin zamanlayıcıları", s1chip(10))
        LIFE = ["güç", "kanal arama", "↓ senkron", "profiller", "SN", "↑ λ düzelt", "ranging", "doğrulama", "çalışma", "güç dengeleme",
                "kanal devri", "λ kilitleme", "koruma", "izleme", "arızalar", "ayrılış"]
        row = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.06, width=0.7, height=0.45, stroke_color=MUTED, stroke_width=1.6, fill_color=PANEL, fill_opacity=1),
                              T(str(i), 16, MUTED, BOLD)) for i in range(16)]).arrange(RIGHT, buff=0.08).move_to([0, 1.75, 0])
        for c in row:
            c[1].move_to(c[0])
        rl = T("S1·B10 · bir ONU'nun hayatı", 15, S1C, BOLD).next_to(row, UP, buff=0.08).align_to(row, LEFT)
        z10 = VGroup(tile("10 · " + LIFE[10], GOLD, 2.3, 0.5, 17, 0.2), T("anı: süper çerçeve sayacı", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, 0.95, 0])
        za = DashedLine(row[10].get_bottom(), z10[0].get_top(), color=GOLD, stroke_width=1.5)
        tms = VGroup(*[VGroup(tag(n, TMRC, 16), T(w, 14, MUTED, BOLD)).arrange(DOWN, buff=0.06) for n, w in
                       (("TO4", "ONU · O8"), ("TO5", "ONU · O9"), ("Ttarget", "hedef CT"), ("Tsource", "kaynak CT"))]).arrange(RIGHT, buff=0.55).move_to([-2.2, 0.0, 0])
        nv = VGroup(T("değer:", 17, TXT, BOLD), T("yok · yok · yok · yok", 17, WARN, BOLD)).arrange(RIGHT, buff=0.15).next_to(tms, RIGHT, buff=0.5)
        rule = VGroup(T("tek kural:", 17, TXT, BOLD), T("Tsource > Ttarget", 19, GOLD, BOLD), T("Tablo 17-6", 14, MUTED, BOLD)).arrange(RIGHT, buff=0.15).next_to(nv, DOWN, buff=0.18).align_to(nv, LEFT)
        y = -1.95
        x = {"in": -5.6, "tc": -3.4, "sfc": 0.6, "cu": 3.6}
        tl_ = Line([-6.2, y, 0], [6.4, y, 0], color=MUTED, stroke_width=2)
        mk = VGroup(tmark(x["in"], y - 0.15, y + 0.4, "ICTP ayar-giriş", TGTC, 14), tmark(x["tc"], y - 0.15, y + 0.4, "Tuning_Control", GOLD, 14),
                    tmark(x["sfc"], y - 0.15, y + 0.4, "planlı SFC", GOLD, 14), tmark(x["cu"], y - 0.15, y + 0.4, "Complete_u", CMPC, 14))
        ld = brace_lbl(Line([x["tc"], y, 0], [x["sfc"], y, 0]), "öncülük süresi", GOLD, DOWN, 14)
        tt = Rectangle(width=x["cu"] + 0.9 - x["in"], height=0.22, stroke_width=0, fill_color=TGTC, fill_opacity=0.55).move_to([(x["in"] + x["cu"] + 0.9) / 2, y - 0.95, 0])
        ttl = T("Ttarget", 14, TGTC, BOLD).next_to(tt, LEFT, buff=0.1)
        ts = Rectangle(width=x["cu"] + 2.2 - x["tc"], height=0.22, stroke_width=0, fill_color=SRCC, fill_opacity=0.55).move_to([(x["tc"] + x["cu"] + 2.2) / 2, y - 1.3, 0])
        tsl = T("Tsource", 14, SRCC, BOLD).next_to(ts, LEFT, buff=0.1)
        inf = VGroup(interp("çıkarım", GOLD, 14), T("Ttarget öncülüğü de kapsamalı", 15, GOLD, BOLD)).arrange(RIGHT, buff=0.12).next_to(rule, DOWN, buff=0.2).align_to(rule, LEFT)
        self.play(self.set_src("S1·B10 · G.989.3 Tablo 12-2 · Tablo 17-6 · Ek F"), run_time=0.3)
        self.at(self.cue("onuncu adımı devirdi", 3.5))
        self.play(FadeIn(rl), LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in row], lag_ratio=0.03), run_time=0.8)
        self.play(row[10][0].animate.set_stroke(GOLD), row[10][1].animate.set_color(GOLD), Create(za), FadeIn(z10[0]), run_time=0.5)
        self.at(self.cue("süper çerçeve sayacı belirliyordu", 8.0))
        self.play(FadeIn(z10[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("zamanlayıcılarına bakın", 11.3))
        self.play(FadeIn(tms[0]), run_time=0.3)
        self.at(self.cue("TO5 ve OLT'deki", 14.9))
        self.play(LaggedStart(*[FadeIn(t) for t in tms[1:]], lag_ratio=0.2), run_time=0.7)
        self.at(self.cue("değeri yoktur", 19.0))
        self.play(FadeIn(nv, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("tek kural", 20.8))
        self.play(FadeIn(rule, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Bizim çıkarımımız", 25.3))
        self.play(Create(tl_), FadeIn(mk), run_time=0.6)
        self.at(self.cue("ayar isteğinden önce", 27.8))
        self.play(GrowFromEdge(tt, LEFT), FadeIn(ttl), run_time=0.6)
        self.play(GrowFromEdge(ts, LEFT), FadeIn(tsl), run_time=0.5)
        self.at(self.cue("öncülük süresini", 31.5))
        self.play(FadeIn(ld), FadeIn(inf, shift=DOWN * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # c15 — engineer note; c16 — bridge
        self.note11("c15", [("1", "Ayar yanıtını çözerken önce işlem kodunu okuyun",
                             "aynı bit NACK ile ROLLBACK'te farklı koşuldur · oktet 5, sonra oktet 6–7", "işlem kodunu okuyun"),
                            ("2", "OLT makinesini Tablo 17-9'a göre kodlayın",
                             "iptal mesajının tetikleyicisi ve yönü metinde üç farklı biçimde anlatılır", "on yedi tire dokuz")])
        self.bridge_beat("c16", "Devir mesaj mesaj belli.\nPeki ne kadar sürer?")
        self.save_timeline("ep17_p2C")
