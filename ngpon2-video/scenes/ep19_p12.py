"""S2·B9 · Perde 1 (uyanık ve uykulu — G.989.3 §16 giriş, §16.1.1–16.1.4, Tablo 16-1 … 16-7, Şekil 16-1/16-2, Tablo 11-2/11-13/11-29,
§8.1.1.2.5, G.989.2 WNE-PSD) and Perde 2 (tasarrufun hesabı, kanal seçimi ve PtP hız uyarlama — §16.1.5, §16.2, Tablo 16-8,
Tablo 11-22/11-23/11-31/11-32, Şekil 16-3, G.989.2 Ek A, AMCC)."""
from ep19_common import *


def rule_row(n, title, body, color=GOLD, tsize=19, bsize=15, w=7.0):
    """Numbered rule: coloured number + title + one muted detail line (left-aligned group)."""
    num = T(str(n), 26, color, BOLD)
    g = VGroup(T(title, tsize, TXT, BOLD), T(body, bsize, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    fit(g, w)
    return VGroup(num, g.next_to(num, RIGHT, buff=0.25))


def attr(lines, color=TXT, size=15):
    return VGroup(*[T(s, size, color, BOLD) for s in lines]).arrange(DOWN, buff=0.04)


# ================================ PERDE 1 ======================================
class E19P1A(Act19):
    HDR, MANIFEST, FIRST = H19[1], M19("p1"), True

    def construct(self):
        # b1 — §16 motivation: idle subscriber interface → power down its circuitry, keep detecting activity; scope sentence: design and
        #      operator practice are out of scope; G.989.3 standardizes only the protocol (how the saving is negotiated with the OLT)
        self.beat("b1")
        tc = self.title_card("PERDE 1", "Uyanık ve uykulu")
        h = self.heading("§16 — güç yönetimi: ne standarttır?")
        self.at(self.cue("On altıncı madde", 2.3))
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        onu = RoundedRectangle(corner_radius=0.12, width=2.0, height=2.3, stroke_color=ONUC, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([-4.9, 0.55, 0])
        onl = T("ONU", 20, ONUC, BOLD).next_to(onu, UP, buff=0.1)
        ys = [1.35, 0.82, 0.29, -0.24]
        ports, lamps, lines_, labs = VGroup(), VGroup(), VGroup(), VGroup()
        for k, yy in enumerate(ys):
            p = RoundedRectangle(corner_radius=0.04, width=0.5, height=0.3, stroke_color=TXT, stroke_width=1.6, fill_color=BG, fill_opacity=1).move_to([-3.9, yy, 0])
            ports.add(p)
            lamps.add(glow_dot(GOOD, 0.05, 3).move_to([-4.55, yy, 0]))
            lines_.add(Line(p.get_right(), [-1.9, yy, 0], color=GOOD if k == 0 else FEED, stroke_width=2.5))
            labs.add(T(f"abone arayüzü {k + 1}", 15, MUTED, BOLD).next_to([-1.9, yy, 0], RIGHT, buff=0.12))
        traf = VGroup(*[Dot(radius=0.05, color=GOOD).move_to([-3.2 + 0.4 * i, ys[0], 0]) for i in range(3)])
        off = VGroup(*[VGroup(Circle(radius=0.06, stroke_color="#64748B", stroke_width=1.6, fill_color="#0B1220", fill_opacity=1)).move_to(lamps[k]) for k in (1, 2, 3)])
        eyes = VGroup(*[eye_icon(ACC, 0.12).move_to([-3.25, ys[k], 0]) for k in (1, 2, 3)])
        idl = VGroup(T("boş → devre kapalı", 16, MUTED, BOLD), T("etkinlik algılama açık", 16, ACC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        idl.move_to([1.85, 0.55, 0], aligned_edge=LEFT)
        bx1 = RoundedRectangle(corner_radius=0.14, width=5.8, height=1.35, stroke_color=MUTED, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to([-3.25, -1.95, 0])
        t1 = VGroup(T("ONU tasarımı · abone ve işletme pratiği", 18, TXT, BOLD), tag("kapsam dışı", WARN, 16)).arrange(DOWN, buff=0.15).move_to(bx1)
        bx2 = RoundedRectangle(corner_radius=0.14, width=5.8, height=1.35, stroke_color=GOLD, stroke_width=2.5, fill_color=PANEL, fill_opacity=1).move_to([3.25, -1.95, 0])
        t2 = T("G.989.3: yalnızca protokol", 18, GOLD, BOLD).move_to(bx2.get_top() + DOWN * 0.3)
        ox, nx, my = 1.2, 5.3, -2.3
        oc = ct_box("OLT CT", OLTC, 1.0, 0.4, 15).move_to([ox, my, 0])
        nc = ct_box("ONU", ONUC, 0.9, 0.4, 15).move_to([nx, my, 0])
        m1 = msg3(ox + 0.55, nx - 0.5, my + 0.08, "", GOLD, None, 14, False, True, 2.2)
        m2 = msg3(nx - 0.5, ox + 0.55, my - 0.1, "", SRW, None, 14, False, True, 2.2)
        ml = T("Sleep_Allow ↓ · Sleep_Request ↑ · FWI ↓", 15, TXT, BOLD).move_to([(ox + nx) / 2, my + 0.42, 0])
        fit(ml, 3.4)
        self.play(FadeIn(onu), FadeIn(onl), FadeIn(ports), FadeIn(lamps), *[Create(l) for l in lines_], FadeIn(labs), FadeIn(traf),
                  self.set_src("G.989.3 §16 · §16.1"), run_time=0.7)
        self.at(self.cue("bir abone arayüzü boştaysa", 5.4))
        self.play(*[lines_[k].animate.set_stroke(opacity=0.35) for k in (1, 2, 3)], *[labs[k].animate.set_opacity(0.5) for k in (1, 2, 3)], run_time=0.5)
        self.at(self.cue("etkinliği algılamayı sürdürerek", 10.0))
        self.play(*[Transform(lamps[k], off[i]) for i, k in enumerate((1, 2, 3))], FadeIn(idl[0], shift=LEFT * 0.05), run_time=0.5)
        self.play(FadeIn(eyes, scale=0.8), FadeIn(idl[1], shift=LEFT * 0.05), run_time=0.5)
        self.at(self.cue("Ama hemen bir kapsam", 16.1))
        self.play(FadeIn(bx1), FadeIn(t1[0]), run_time=0.45)
        self.at(self.cue("ONU tasarımının ve işletme", 19.4))
        self.play(FadeIn(t1[1], scale=0.9), run_time=0.35)
        self.at(self.cue("yalnızca protokolü", 23.9))
        self.play(FadeIn(bx2), FadeIn(t2), FadeIn(oc), FadeIn(nc), run_time=0.45)
        self.at(self.cue("tasarrufun OLT ile", 27.6))
        self.play(*grow_msg(m1), *grow_msg(m2), FadeIn(ml), run_time=0.6)
        self.end(pad=0.05)

        # b2 — the only sleep mode left: watchful sleep. Sleep_Request Activity_level 0x00 Awake, 0x03 WSleep, 0x01/0x02 reserved;
        #      doze and cyclic sleep are in none of the three editions; our reading: a trace of XG-PON's wider sleep family
        self.beat("b2")
        h = self.reset("Tek uyku kipi: dikkatli uyku", "std", 0.5)
        mt = VGroup(mtile(0x10, "Sleep_Request ↑", "pm", 3.3, 0.44, 17), T("oktet 5 · Activity_level", 17, MUTED, BOLD)).arrange(RIGHT, buff=0.3)
        mt.move_to([-3.1, 1.75, 0])
        rows = VGroup(code_row("0x00", "Awake · uyanık", SRA, 18, 4.6), code_row("0x01", "ayrılmış", MUTED, 18, 4.6),
                      code_row("0x02", "ayrılmış", MUTED, 18, 4.6), code_row("0x03", "WSleep · dikkatli uyku", SRW, 18, 4.6))
        rows.arrange(DOWN, buff=0.14).move_to([-3.85, -0.1, 0])
        gap = brace_lbl(VGroup(rows[1], rows[2]), "boşluk", MUTED, RIGHT, 16)
        gone = VGroup(*[sbox(a, b, MUTED, 3.2, 0.82, 19, 15) for a, b in (("uyuklama", "doze mode"), ("döngüsel uyku", "cyclic sleep"))]).arrange(DOWN, buff=0.3)
        gone.move_to([3.4, 0.55, 0])
        xs = VGroup(*[xmark(g, WARN, 4, 0.02) for g in gone])
        ed = VGroup(ed_chips(15, MUTED), T("üçünde de yok", 16, WARN, BOLD)).arrange(DOWN, buff=0.12).next_to(gone, DOWN, buff=0.3)
        ip = VGroup(ytag("bizim yorumumuz"), T("boşluk = XG-PON'un (G.987.3) daha geniş uyku ailesinden kalan iz", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2)
        fit(ip, 12.6).move_to([0, -2.75, 0])
        self.play(FadeIn(mt, shift=RIGHT * 0.05), self.set_src("G.989.3 Tablo 11-29 · Tablo 16-3 · 2021 / Amd.1 / Amd.2 tarandı"), run_time=0.45)
        self.at(self.cue("sıfır uyanık", 4.6))
        self.play(FadeIn(rows[0], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("üç dikkatli uyku", 6.6))
        self.play(FadeIn(rows[3], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("bir ve iki ayrılmıştır", 8.8))
        self.play(FadeIn(rows[1:3], shift=RIGHT * 0.05), FadeIn(gap), run_time=0.45)
        self.at(self.cue("Uyuklama ya da döngüsel", 10.7))
        self.play(FadeIn(gone, shift=LEFT * 0.05), run_time=0.45)
        self.play(*[Create(x) for x in xs], run_time=0.4)
        self.at(self.cue("üç baskının hiçbirinde", 13.2))
        self.play(FadeIn(ed, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("bu boşluk", 17.1))
        self.play(FadeIn(ip, shift=UP * 0.05), Indicate(gap, color=GOLD, scale_factor=1.05), run_time=0.6)
        self.end(pad=0.05)

        # b3 — rules (§16.1.1): OMCI discovers and configures (not enabled → Sleep_Allow ignored); two partially aligned machines; PLOAM only on
        #      transitions; a timer starts when the message is actually sent; the ONU sleeps only in O5
        self.beat("b3")
        h = self.reset("Kurallar — §16.1.1", "std", 0.5)
        rr = VGroup(rule_row(1, "OLT, ONU'nun güç yönetimini OMCI ile keşfeder ve yapılandırır", "etkinleştirilmemiş ONU → Sleep_Allow'u yok sayar (Tablo 11-2)"),
                    rule_row(2, "İki taraf, iki durum makinesi — kısmen hizalı", "adım adım eşleşme protokolün hedefi değil (§16.1.3)"),
                    rule_row(3, "PLOAM mesajları yalnızca geçişlerde üretilir", "tam güç ↔ düşük güç alt kümeleri arasında"),
                    rule_row(4, "Zamanlayıcı, mesaj gerçekten gönderilince başlar", "geçiş anı ≠ gönderim anı"),
                    rule_row(5, "ONU yalnızca O5'te uyur", "§16.1.4 · Tablo 12-4: Sleep_Allow O5 ve O9'da işlenir"))
        rr.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-2.45, -0.3, 0])
        for r in rr:
            fit(r, 8.2)
        rr.align_to([-6.4, 0, 0], LEFT)
        y4 = rr[3].get_y()
        tx0, tx1 = 2.6, 6.4
        tl = Line([tx0, y4 - 0.05, 0], [tx1, y4 - 0.05, 0], color=MUTED, stroke_width=2)
        g1 = tmark(tx0 + 0.3, y4 - 0.25, y4 + 0.2, "geçiş", SRW, 14)
        q = Rectangle(width=1.3, height=0.2, stroke_width=0, fill_color=MUTED, fill_opacity=0.5).move_to([tx0 + 0.3 + 0.65, y4 - 0.05, 0])
        ql = T("kuyruk", 14, MUTED, BOLD).next_to(q, DOWN, buff=0.06)
        g2 = tmark(tx0 + 1.6, y4 - 0.25, y4 + 0.2, "gönderim", GOLD, 14, dashed=False)
        tb = tbar(tx0 + 1.6, tx1 - 0.1, y4 - 0.05, "", TMRC, 0.2)
        tbl = T("zamanlayıcı", 14, TMRC, BOLD).next_to(tb, DOWN, buff=0.06)
        sm2 = VGroup(VGroup(*[tile(f"({k})", pcol("L", k), 0.5, 0.36, 14, 0.25) for k in range(1, 5)]).arrange(RIGHT, buff=0.06),
                     VGroup(*[tile(f"({k})", pcol("N", k), 0.5, 0.36, 14, 0.25) for k in range(1, 5)]).arrange(RIGHT, buff=0.06)).arrange(DOWN, buff=0.12)
        sm2.move_to([4.5, rr[1].get_y(), 0])
        sml = VGroup(T("OLT", 14, OLTC, BOLD).next_to(sm2[0], LEFT, buff=0.12), T("ONU", 14, ONUC, BOLD).next_to(sm2[1], LEFT, buff=0.12))
        o5 = sbox("O5", "çalışma", OPC, 1.5, 0.62, 18, 14).move_to([4.5, rr[4].get_y(), 0])
        o5l = T("uyku yalnızca burada", 14, OPC, BOLD).next_to(o5, RIGHT, buff=0.15)
        self.play(self.set_src("G.989.3 §16.1.1 · §16.1.3 · §16.1.4 · Tablo 11-2 · Tablo 12-4"), run_time=0.3)
        self.at(self.cue("ONU'nun güç yönetimini OMCI", 1.1))
        self.play(FadeIn(rr[0][0]), FadeIn(rr[0][1][0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("etkinleştirilmemiş bir ONU", 5.9))
        self.play(FadeIn(rr[0][1][1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("İki taraf birer durum", 10.0))
        self.play(FadeIn(rr[1][0]), FadeIn(rr[1][1][0], shift=RIGHT * 0.05), FadeIn(sm2), FadeIn(sml), run_time=0.45)
        self.at(self.cue("adım adım eşleşme", 15.4))
        self.play(FadeIn(rr[1][1][1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("PLOAM mesajları yalnızca", 18.2))
        self.play(FadeIn(rr[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("ve bir zamanlayıcı", 22.0))
        self.play(FadeIn(rr[3], shift=RIGHT * 0.05), Create(tl), FadeIn(g1), FadeIn(q), FadeIn(ql), run_time=0.45)
        self.at(self.cue("mesaj gerçekten gönderilince", 23.6))
        self.play(FadeIn(g2), GrowFromEdge(tb[0], LEFT), FadeIn(tbl), run_time=0.5)
        self.at(self.cue("ONU yalnızca O5'te", 26.7))
        self.play(FadeIn(rr[4], shift=RIGHT * 0.05), FadeIn(o5), FadeIn(o5l), run_time=0.4)
        self.end(pad=0.05)

        # b4 — Table 16-1: four intervals set by the OLT (Ilowpower max in LowPower, Iaware min in Aware, Irxoff max wake-up wait, Ihold min in
        #      ActiveHeld) and one reported by the ONU (Itransinit, 0 = can answer a grant without delay)
        self.beat("b4")
        h = self.reset("Tablo 16-1 — parametreler", "std", 0.5)
        data = [["Ilowpower", "OLT CT", "düşük güç durumunda en uzun kalış", "125 µs çerçeve", "değer yok"],
                ["Iaware", "OLT CT", "farkında durumunda en kısa kalış", "125 µs çerçeve", "değer yok"],
                ["Irxoff", "OLT CT", "uyandırma kararı → ONU tam çalışır: en uzun bekleme", "125 µs çerçeve", "değer yok"],
                ["Ihold", "OLT CT", "etkin tutulan durumda en kısa kalış", "— yazılmamış", "değer yok"],
                ["Itransinit", "ONU", "uykudan sonra verici + alıcı tam işleve dönüş · 0 = beklemeden", "125 µs çerçeve", "tasarımla bilinir"]]
        tb = mtable(["parametre", "belirleyen", "anlam", "birim", "değer"], data, [2.0, 1.55, 5.35, 2.0, 1.7], size=17, hsize=15, row_h=0.6, mono=(0,))
        tb.move_to([0, 0.25, 0])
        for r in tb[1:]:
            r[1].set_color(TMRC)
            r[2].set_color(ONUC if r[2].text == "ONU" else OLTC)
            r[5].set_color(WARN)
        tb[5][5].set_color(GOLD)
        tb[4][4].set_color(WARN)
        z = SurroundingRectangle(tb[5][3], color=GOLD, buff=0.04, stroke_width=2)
        self.play(self.set_src("G.989.3 Tablo 16-1 · §16.1.2"), run_time=0.3)
        self.at(self.cue("OLT dört aralık belirler", 1.1))
        self.play(FadeIn(tb[0]), run_time=0.4)
        for k, (key, d) in enumerate((("düşük güç durumunda en uzun", 3.2), ("farkında durumunda en kısa", 6.0), ("uyandırma kararından", 8.8),
                                      ("etkin tutulan durumda en kısa", 15.3), ("Beşincisini ONU bildirir", 18.6))):
            self.at(self.cue(key, d))
            self.play(FadeIn(tb[k + 1][0]), FadeIn(tb[k + 1][1:4], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Sıfır,", 25.6))
        self.play(Create(z), run_time=0.4)
        self.end(pad=0.05)

        # b5 — no numeric value for any of them (no default, no bound); unit = 125 µs frames, one has no unit at all; values come via OMCI;
        #      every number in this episode is an example: 1 ms = 8 frames
        self.beat("b5")
        nv = VGroup(tag("varsayılan: yok", WARN, 16), tag("alt / üst sınır: yok", WARN, 16)).arrange(RIGHT, buff=0.2)
        om = VGroup(T("değerler:", 16, MUTED, BOLD), tag("OMCI · G.988 (2022)", OMC, 16)).arrange(RIGHT, buff=0.15)
        ex = VGroup(ex_tag("bu bölümdeki her sayı: örnek", 16), T("1 ms = 8 × 125 µs çerçeve", 18, EXMC, BOLD)).arrange(RIGHT, buff=0.25)
        bot = VGroup(VGroup(nv, om).arrange(RIGHT, buff=0.5), ex).arrange(DOWN, buff=0.22)
        fit(bot, 12.6).move_to([0, -2.45, 0])
        ih = SurroundingRectangle(tb[4][4], color=WARN, buff=0.05, stroke_width=2.5)
        self.play(FadeOut(z), run_time=0.3)
        self.at(self.cue("hiçbirinin sayısal değeri", 3.0))
        self.play(LaggedStart(*[FadeIn(r[5], shift=LEFT * 0.05) for r in tb[1:]], lag_ratio=0.15), run_time=0.7)
        self.at(self.cue("ne varsayılan", 7.2))
        self.play(FadeIn(nv, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Birim yüz yirmi beş", 9.2))
        self.play(*[FadeIn(r[4], shift=LEFT * 0.05) for r in tb[1:]], run_time=0.5)
        self.at(self.cue("birinin birimi hiç", 13.0))
        self.play(Create(ih), Indicate(tb[4][1], color=WARN, scale_factor=1.08), run_time=0.6)
        self.at(self.cue("değerler OMCI ile gelir", 15.8))
        self.play(FadeIn(om, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("her sayı örnektir", 18.1))
        self.play(FadeIn(ex[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("bir milisaniye sekiz", 21.5))
        self.play(FadeIn(ex[1], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)
        self.save_timeline("ep19_p1A")


ONU_ATTR = {1: ["Tx ✓ · Rx ✓", "güç yönetimi geçişi yok"], 2: ["Tx ✓ · Rx ✓", "uyku: ONU'nun yerel kararı"],
            3: ["Tx ✓ · Rx ✓", "her tahsise cevap"], 4: ["Tx ✗ · Rx ara ara bakar", "tahsis ✗ · trafik iletimi ✗"]}


class E19P1B(Act19):
    HDR, MANIFEST, PREV_BADGE = H19[1], M19("p1"), "std"

    def onu_sm(self):
        return PmSM("N", cx=0.0, cy=-0.3, dx=2.9, dy=1.15, w=2.7, h=0.88)

    def construct(self):
        # b6 — ONU states (Table 16-2): ActiveHeld initial (Tx/Rx on, no PM transitions); ActiveFree (sleeping is a local decision); Aware (Tx/Rx on,
        #      answers every grant); LowPower (Tx off, Rx checks only now and then, no grant responses, no forwarding)
        self.beat("b6")
        h = self.heading19("ONU makinesi — dört durum")
        sm = self.onu_sm()
        ats = {}
        for k in range(1, 5):
            c = WARN if k == 4 else TXT
            ats[k] = attr(ONU_ATTR[k], c if k == 4 else MUTED, 15).next_to(sm.b[k], DOWN, buff=0.1)
        ats[1][0].set_color(GOOD)
        ats[2][0].set_color(GOOD)
        ats[3][0].set_color(GOOD)
        ini = VGroup(Dot(radius=0.07, color=TXT).move_to(sm.pt(1, "L") + LEFT * 1.1), arrow(sm.pt(1, "L") + LEFT * 1.05, sm.pt(1, "L"), TXT, 2.2, 0.12))
        inil = T("başlangıç", 15, TXT, BOLD).next_to(ini, UP, buff=0.06)
        zz4 = zz(RLC, 18).next_to(sm.b[4], UR, buff=-0.15)
        self.play(self.set_src("G.989.3 §16.1.3.1 · Tablo 16-2 · Şekil 16-1"), run_time=0.3)
        self.at(self.cue("Etkin tutulan durum başlangıçtır", 2.9))
        self.play(FadeIn(sm.b[1], scale=0.95), FadeIn(ini), FadeIn(inil), run_time=0.5)
        self.at(self.cue("verici ve alıcı açık", 5.7))
        self.play(FadeIn(ats[1], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Etkin serbest durumda", 9.5))
        self.play(FadeIn(sm.b[2], scale=0.95), FadeIn(ats[2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Farkında durumunda verici", 14.0))
        self.play(FadeIn(sm.b[3], scale=0.95), FadeIn(ats[3][0], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("her tahsise cevap verir", 17.6))
        self.play(FadeIn(ats[3][1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Düşük güç durumunda verici", 19.9))
        self.play(FadeIn(sm.b[4], scale=0.95), FadeIn(ats[4][0], shift=UP * 0.05), FadeIn(zz4), run_time=0.5)
        self.at(self.cue("tahsislere cevap vermez", 25.5))
        self.play(FadeIn(ats[4][1], shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # b7 — PMD Köprüsü (S1·B6): a switched-off transmitter is not dark: WNE-PSD ≤ −62.6 dBm/15 GHz; 63 neighbours in a channel ≙ 0.1 dB penalty
        #      (Note 9); no separate optical rule for a sleeping ONU — the same dark rule applies
        self.beat("b7")
        h, chp = self.pmd_reset2("PMD Köprüsü — kapalı verici", [s1chip(6)])
        olt = ct_box("OLT", OLTC, 1.0, 0.45, 15).move_to([-5.8, 0.3, 0])
        sp = splitter(0.3).move_to([-4.3, 0.3, 0])
        fd = Line(olt.get_right(), sp.get_left(), color=FEED, stroke_width=2.5)
        act = onu_box("ONU", ONUC, 1.0, 0.42, 15).move_to([-2.2, 1.45, 0])
        dl1 = Line(sp.get_right(), act.get_left(), color=FEED, stroke_width=2)
        dark = VGroup()
        for i in range(7):
            for j in range(9):
                dark.add(Square(0.16, stroke_color=RLC, stroke_width=1.2, fill_color=RLC, fill_opacity=0.15).move_to([-2.85 + 0.21 * j, 0.6 - 0.21 * i, 0]))
        dark = VGroup(*dark[:63])
        dl2 = Line(sp.get_right(), dark.get_left() + RIGHT * 0.0, color=FEED, stroke_width=2)
        dkl = T("63 komşu · verici kapalı", 15, RLC, BOLD).next_to(dark, DOWN, buff=0.12)
        ul = Line(act.get_left() + LEFT * 0.02, sp.get_right(), color=GOLD, stroke_width=4)
        Y = lambda v: -0.9 + (v + 62.6) / 18.0 * 2.1
        ax = Line([0.9, -1.7, 0], [0.9, 1.8, 0], color=MUTED, stroke_width=2)
        axl = T("dBm / 15 GHz", 15, MUTED, BOLD).next_to(ax, UP, buff=0.08)
        l1 = Line([0.9, Y(-62.6), 0], [6.3, Y(-62.6), 0], color=RLC, stroke_width=3)
        l1t = VGroup(T("−62,6", 18, RLC, BOLD), T("tek karanlık ONU · WNE-PSD üst sınırı", 15, TXT, BOLD)).arrange(RIGHT, buff=0.15).next_to(l1, DOWN, buff=0.08).align_to(l1, LEFT).shift(RIGHT * 0.15)
        l2 = Line([0.9, Y(-44.6), 0], [6.3, Y(-44.6), 0], color=GOLD, stroke_width=3)
        l2t = VGroup(T("≤ −44,6", 18, GOLD, BOLD), T("63 komşunun toplamı", 15, TXT, BOLD), ytag("bizim hesabımız")).arrange(RIGHT, buff=0.15)
        l2t.next_to(l2, UP, buff=0.08).align_to(l2, LEFT).shift(RIGHT * 0.15)
        pen = VGroup(T("≙ 0,1 dB ceza", 20, GOLD, BOLD), T("Not 9 · FEC açık · kanalda 64 ONU", 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        pen.next_to(l2, DOWN, buff=0.35).align_to(l2, LEFT).shift(RIGHT * 0.15)
        same = VGroup(tag("uyuyan ONU için ayrı optik kural: yok", WARN, 16), T("→ aynı karanlık kuralı", 18, TXT, BOLD)).arrange(RIGHT, buff=0.25)
        fit(same, 12.6).move_to([0, -2.85, 0])
        self.play(FadeIn(olt), Create(fd), FadeIn(sp), Create(dl1), FadeIn(act), self.set_src("G.989.2 §11.1.5.2.9 · Tablo 11-6 / 11-7 · Not 9 · bizim hesabımız"), run_time=0.6)
        self.at(self.cue("kapalı verici karanlık değildir", 1.5))
        self.play(Create(dl2), LaggedStart(*[FadeIn(s) for s in dark], lag_ratio=0.01), FadeIn(dkl), Create(ul), run_time=0.9)
        self.at(self.cue("on beş gigahertzde eksi", 8.4))
        self.play(Create(ax), FadeIn(axl), run_time=0.35)
        self.play(Create(l1), FadeIn(l1t, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("altmış üç komşunun", 16.3))
        self.play(*[s.animate.set_fill(opacity=0.45) for s in dark], Create(l2), FadeIn(l2t, shift=UP * 0.05), run_time=0.6)
        self.at(self.cue("sıfır virgül bir desibellik", 19.7))
        self.play(FadeIn(pen, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ayrı bir optik kural", 23.9))
        self.play(FadeIn(same[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("aynı karanlık kuralı", 27.6))
        self.play(FadeIn(same[1], shift=LEFT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # b8 — ONU transitions (Table 16-4): Thold expiry with latched SA(ON) → ActiveFree, no message; LSI → Aware + SR(WSleep); Taware / Tlowpower
        #      timers between Aware and LowPower; SA(OFF), FWI or LWI in either → ActiveHeld + SR(Awake)
        self.beat("b8")
        h = self.reset("ONU geçişleri — Tablo 16-4", "std", 0.5)
        sm = self.onu_sm()
        e12 = sm.edge(1, "B", 2, "T", "Thold doldu\nve SA(ON)", SAON, -0.55, -0.55, LEFT, 0.1)
        nm = T("mesaj yok", 14, MUTED, BOLD).next_to(e12[1], DOWN, buff=0.06)
        e23 = sm.edge(2, "R", 3, "L", "LSI / SR(WSleep)", SRW, 0.0, 0.0, DOWN, 0.08)
        e34 = sm.edge(3, "T", 4, "B", "Taware\ndoldu", TMRC, 0.5, 0.5, RIGHT, 0.1)
        e43 = sm.edge(4, "B", 3, "T", "Tlowpower\ndoldu", TMRC, -0.5, -0.5, LEFT, 0.1)
        e41 = sm.edge(4, "L", 1, "R", "SA(OFF) · FWI · LWI\n/ SR(Awake)", SRA, 0.0, 0.0, UP, 0.08)
        e31 = sm.edge(3, "L", 1, "R", None, SRA, 0.28, -0.3)
        e31l = T("aynı girdiler\n/ SR(Awake)", 14, SRA, BOLD, line_spacing=0.8).next_to(e31[0].point_from_proportion(0.45), DL, buff=0.02)
        ini = VGroup(Dot(radius=0.07, color=TXT).move_to(sm.pt(1, "L") + LEFT * 1.1), arrow(sm.pt(1, "L") + LEFT * 1.05, sm.pt(1, "L"), TXT, 2.2, 0.12))
        self.play(FadeIn(sm.boxes()), FadeIn(ini), self.set_src("G.989.3 Tablo 16-4 · Şekil 16-1 · Tablo 16-3"), run_time=0.6)
        self.at(self.cue("Tutma süresi dolduğunda", 0.8))
        self.play(GrowArrow(e12[0]), FadeIn(e12[1]), run_time=0.5)
        self.at(self.cue("mesajsız", 6.4))
        self.play(FadeIn(nm, shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Yerel uyku göstergesiyle", 7.2))
        self.play(GrowArrow(e23[0]), FadeIn(e23[1]), run_time=0.5)
        self.at(self.cue("Oradan zamanlayıcılarla", 13.2))
        self.play(GrowArrow(e34[0]), FadeIn(e34[1]), run_time=0.45)
        self.play(GrowArrow(e43[0]), FadeIn(e43[1]), run_time=0.45)
        self.at(self.cue("Bu iki durumdayken kapalı izin", 17.3))
        self.play(GrowArrow(e41[0]), GrowArrow(e31[0]), run_time=0.5)
        self.at(self.cue("zorunlu uyandırma biti ya da", 19.9))
        self.play(FadeIn(e41[1], shift=DOWN * 0.05), FadeIn(e31l), run_time=0.45)
        self.at(self.cue("etkin tutulan duruma döner", 25.3))
        self.play(Indicate(sm.b[1], color=GOLD, scale_factor=1.05), run_time=0.5)
        self.end(pad=0.05)

        # b9 — Fig. 16-1 NOTE: yellow (tense) and grey (relaxed) subgraphs; an output only on a transition that crosses the boundary. The contradiction:
        #      Table 16-2 says ActiveHeld entry sends SR(Awake), but ActiveFree → ActiveHeld stays inside yellow and Table 16-4 (normative) has no
        #      output. Our reading: the boundary is "sleep allowed or not"
        self.beat("b9")
        ry = sm.region(True, 0.24, True, 15)
        rg = sm.region(False, 0.24, True, 15)
        e21 = sm.edge(2, "T", 1, "B", "SA(OFF)\nveya FWI", SAOFF, 0.55, 0.55, RIGHT, 0.1)
        outs = VGroup(e23[1], e41[1], e31l)
        q = VGroup(T("Tablo 16-2:", 16, GOLD, BOLD), T("(1)'e girişte SR(Awake)", 16, TXT, BOLD), T("↔", 18, WARN, BOLD),
                   T("Tablo 16-4 (normatif): (2) → (1) çıktısız", 16, TXT, BOLD)).arrange(RIGHT, buff=0.18)
        fit(q, 12.6).move_to([0, -2.6, 0])
        ip = VGroup(ytag("bizim okumamız"), T("sınır = uykuya izin var mı, yok mu", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -3.15, 0])
        self.at(self.cue("durumlar sarı ve gri", 4.2))
        self.play(FadeIn(ry), FadeIn(rg), self.set_src("G.989.3 Şekil 16-1 NOT · Tablo 16-2 · Tablo 16-4"), run_time=0.6)
        self.at(self.cue("sınırı geçen geçişte", 7.4))
        self.play(*[Indicate(o, color=WHITE, scale_factor=1.12) for o in outs], run_time=0.8)
        self.at(self.cue("Durum tablosuna göre", 13.5))
        self.play(FadeIn(q[:2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("etkin serbestten oraya", 20.1))
        self.play(GrowArrow(e21[0]), FadeIn(e21[1]), run_time=0.5)
        self.play(Indicate(e21, color=SAOFF, scale_factor=1.08), run_time=0.5)
        self.at(self.cue("normatif geçiş tablosunda", 24.7))
        self.play(FadeIn(q[2:], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("uykuya izin olup", 29.9))
        self.play(FadeIn(ip, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep19_p1B")


OLT_ATTR = {1: ["her tahsise cevap bekler", "kaçırma → LOBi · girişte SA(OFF)"], 2: ["girişte SA(ON)", "her tahsise cevap bekler"],
            3: ["normal tahsis · ara sıra cevap", "↓ trafik: at ya da tamponla"], 4: ["girişte SA(OFF)", "her tahsiste FWI + PLOAMu"]}


class E19P1C(Act19):
    HDR, MANIFEST, PREV_BADGE = H19[1], M19("p1"), "std"

    def construct(self):
        # b10 — OLT CT states (Table 16-5): AwakeForced initial (expects a reply to every grant, counts missed bursts as a defect, sends SA(OFF) on
        #       entry); AwakeFree sends SA(ON); LowPowerWatch normal allocations, only intermittent replies, DS traffic discarded or buffered; Alerted
        self.beat("b10")
        h = self.heading19("OLT CT makinesi — dört durum")
        sm = PmSM("L", cx=0.0, cy=-0.25, dx=2.9, dy=1.2, w=2.9, h=0.88)
        ats = {k: attr(OLT_ATTR[k], MUTED, 15).next_to(sm.b[k], DOWN, buff=0.1) for k in range(1, 5)}
        ats[1][1].set_color(WARN)
        ats[2][0].set_color(SAON)
        ats[4][0].set_color(SAOFF)
        ats[4][1].set_color(FWIC)
        ini = VGroup(Dot(radius=0.07, color=TXT).move_to(sm.pt(1, "L") + LEFT * 1.0), arrow(sm.pt(1, "L") + LEFT * 0.95, sm.pt(1, "L"), TXT, 2.2, 0.12))
        inil = T("başlangıç", 15, TXT, BOLD).next_to(ini, UP, buff=0.06)
        ry, rg = sm.region(True, 0.22, False), sm.region(False, 0.22, False)
        self.play(self.set_src("G.989.3 §16.1.3.2 · Tablo 16-5 · Şekil 16-2"), run_time=0.3)
        self.at(self.cue("Zorla uyanık durum başlangıçtır", 2.5))
        self.play(FadeIn(sm.b[1], scale=0.95), FadeIn(ini), FadeIn(inil), run_time=0.5)
        self.at(self.cue("her tahsise cevap bekler", 5.2))
        self.play(FadeIn(ats[1][0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("kaçırılan burst'leri kusura", 7.3))
        self.play(FadeIn(ats[1][1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Serbest uyanık durumda", 12.6))
        self.play(FadeIn(sm.b[2], scale=0.95), FadeIn(ats[2], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Düşük güç gözetiminde normal", 15.3))
        self.play(FadeIn(sm.b[3], scale=0.95), FadeIn(ats[3][0], shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("aşağı yön trafiğini atabilir", 21.8))
        self.play(FadeIn(ats[3][1], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Uyarılmış durumda ise", 26.1))
        self.play(FadeIn(sm.b[4], scale=0.95), FadeIn(ats[4], shift=UP * 0.05), run_time=0.5)
        self.play(FadeIn(ry), FadeIn(rg), run_time=0.5)
        self.end(pad=0.05)

        # b11 — the cycle on one time axis: OLT-LWI clears → AwakeFree + SA(ON); ONU after Thold → ActiveFree; activity ends → Aware + SR(WSleep);
        #       OLT → LowPowerWatch, starts the handshake timer Ter_i; ONU alternates Aware / LowPower, answers grants when awake, Ter_i is restarted
        self.beat("b11")
        h = self.reset("Döngü — iki makine, bir zaman ekseni", "std", 0.5)
        yo, yn_ = 0.75, -1.05
        X0, X1 = -5.4, 6.5
        lab = VGroup(side_lbl("OLT CT", yo, OLTC, -6.6, 16), side_lbl("ONU", yn_, ONUC, -6.6, 16))
        o1 = sseg(X0, -3.6, yo, "L", 1, 0.55, 15)
        o2 = sseg(-3.6, -0.15, yo, "L", 2, 0.55, 15)
        o3 = sseg(-0.15, X1, yo, "L", 3, 0.55, 15)
        n1 = sseg(X0, -2.1, yn_, "N", 1, 0.55, 15)
        n2 = sseg(-2.1, -0.45, yn_, "N", 2, 0.55, 15)
        ns = [sseg(-0.45, 0.7, yn_, "N", 3, 0.55, 15), sseg(0.7, 3.0, yn_, "N", 4, 0.55, 15), sseg(3.0, 3.9, yn_, "N", 3, 0.55, 15),
              sseg(3.9, 6.0, yn_, "N", 4, 0.55, 15), sseg(6.0, X1, yn_, "N", 3, 0.55, 15)]
        lwi = VGroup(T("OLT-LWI kalkar", 14, LSC, BOLD)).next_to([-3.6, yo + 0.28, 0], UP, buff=0.06)
        sa = vmsg(-3.6, yo - 0.28, yn_ + 0.28, "SA(ON)", SAON, 15)
        th = tbar(-3.6, -2.1, yn_ - 0.42, "Thold ≥ Ihold", TMRC, 0.14, 14, DOWN)
        lsi = T("LSI", 14, LSC, BOLD).next_to([-0.45, (yo + yn_) / 2, 0], LEFT, buff=0.1)
        sr = vmsg(-0.45, yn_ + 0.28, yo - 0.28, "SR(WSleep)", SRW, 15, RIGHT, 0.06)
        bx = [0.25, 3.45, 6.25]
        bs = VGroup(*[vmsg(x, yn_ + 0.28, yo - 0.28, "", ONUC, 14, sw=2.0) for x in bx])
        bsl = T("burst ↑ (tahsise cevap)", 14, ONUC, BOLD).next_to(bs[1], RIGHT, buff=0.08).shift(DOWN * 0.1)
        ter = VGroup(tbar(-0.15, bx[0], yo + 0.44, "", TMRC, 0.14), tbar(bx[0], bx[1], yo + 0.44, "", TMRC, 0.14), tbar(bx[1], bx[2], yo + 0.44, "", TMRC, 0.14))
        terl = T("Ter_i el sıkışma zamanlayıcısı", 14, TMRC, BOLD).next_to(ter[1], UP, buff=0.06)
        rs = VGroup(*[T("↺", 16, TMRC, BOLD).next_to([x, yo + 0.44, 0], UP, buff=0.02) for x in bx])
        tw = VGroup(tbar(-0.45, 0.7, yn_ - 0.42, "Taware", TMRC, 0.14, 14, DOWN), tbar(0.7, 3.0, yn_ - 0.42, "Tlowpower", TMRC, 0.14, 14, DOWN))
        ex = VGroup(T("Taware ≥ Iaware · Tlowpower ≤ Ilowpower", 15, MUTED, BOLD)).move_to([2.6, -2.35, 0])
        self.play(FadeIn(lab), FadeIn(o1), FadeIn(n1), self.set_src("G.989.3 Tablo 16-4 · Tablo 16-7 · Tablo 16-1 · sıralama: bizim"), run_time=0.5)
        self.at(self.cue("OLT'nin yerel uyanma göstergesi", 1.7))
        self.play(FadeIn(lwi, shift=DOWN * 0.05), run_time=0.35)
        self.play(FadeIn(o2, shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("serbest uyanık olur ve izni", 5.3))
        self.play(GrowArrow(sa[0]), FadeIn(sa[1]), run_time=0.45)
        self.at(self.cue("ONU tutma süresinden sonra", 8.2))
        self.play(GrowFromEdge(th[0], LEFT), FadeIn(th[1]), run_time=0.45)
        self.play(FadeIn(n2, shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("etkinliği bitince dikkatli", 12.0))
        self.play(FadeIn(lsi), FadeIn(ns[0], shift=RIGHT * 0.05), GrowArrow(sr[0]), FadeIn(sr[1]), run_time=0.55)
        self.at(self.cue("OLT düşük güç gözetimine", 15.2))
        self.play(FadeIn(o3, shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("bir el sıkışma zamanlayıcısı", 17.8))
        self.play(GrowFromEdge(ter[0][0], LEFT), FadeIn(terl), run_time=0.45)
        self.at(self.cue("farkında ile düşük güç arasında", 21.2))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.05) for s in ns[1:]], lag_ratio=0.25), FadeIn(tw), run_time=0.9)
        self.play(FadeIn(ex), run_time=0.3)
        self.at(self.cue("her uyanışında tahsislere", 25.7))
        self.play(LaggedStart(*[GrowArrow(b[0]) for b in bs], lag_ratio=0.25), FadeIn(bsl), run_time=0.7)
        self.at(self.cue("zamanlayıcı tazelenir", 28.9))
        self.play(GrowFromEdge(ter[1][0], LEFT), GrowFromEdge(ter[2][0], LEFT), FadeIn(rs), run_time=0.6)
        self.end(pad=0.05)

        # b12 — three exits: (a) ONU traffic → SR(Awake), OLT back to AwakeFree; (b) OLT local reason (e.g. DS traffic) → Alerted: SA(OFF) once,
        #       then FWI in every allocation; (c) ONU silent → Ter_i expires → AwakeForced. Our reading: SA(OFF) is a whisper, FWI a shout
        self.beat("b12")
        h = self.reset("Üç çıkış", "std", 0.5)
        yo, yn_ = 0.75, -0.75
        cs = (-3.85, 0.15, 4.15)
        W = 3.6
        lab = VGroup(side_lbl("OLT", yo, OLTC, -6.6, 16), side_lbl("ONU", yn_, ONUC, -6.6, 16))
        ttl = VGroup(*[tag(s, c, 16).move_to([cx, 1.75, 0]) for s, c, cx in (("a · ONU'da trafik", ONUC, cs[0]), ("b · OLT'de neden", OLTC, cs[1]),
                                                                            ("c · ONU susar", WARN, cs[2]))])
        P = []
        for cx in cs:
            P.append((cx - W / 2, cx + W / 2))
        # (a)
        L, R = P[0]
        a_o = VGroup(sseg(L, L + 1.7, yo, "L", 3, 0.5, 14, short=True), sseg(L + 1.7, R, yo, "L", 2, 0.5, 14))
        a_n = VGroup(sseg(L, L + 1.3, yn_, "N", 4, 0.5, 14, short=True), sseg(L + 1.3, R, yn_, "N", 1, 0.5, 14))
        a_l = T("LWI", 14, LSC, BOLD).next_to([L + 1.3, yn_ - 0.25, 0], DOWN, buff=0.06)
        a_m = vmsg(L + 1.6, yn_ + 0.25, yo - 0.25, "SR(Awake)", SRA, 14, RIGHT, 0.05)
        # (b)
        L, R = P[1]
        b_o = VGroup(sseg(L, L + 0.55, yo, "L", 3, 0.5, 14, short=True), sseg(L + 0.55, L + 2.75, yo, "L", 4, 0.5, 14), sseg(L + 2.75, R, yo, "L", 1, 0.5, 14, short=True))
        b_n = VGroup(sseg(L, L + 1.9, yn_, "N", 4, 0.5, 14), sseg(L + 1.9, L + 2.6, yn_, "N", 4, 0.5, 14, name=False), sseg(L + 2.6, R, yn_, "N", 1, 0.5, 14, short=True))
        b_n[1][0].set_fill(TNC, 0.18)
        b_l = T("OLT-LWI", 14, LSC, BOLD).next_to([L + 0.55, yo + 0.25, 0], UP, buff=0.06)
        b_sa = vmsg(L + 0.6, yo - 0.25, yn_ + 0.25, "", SAOFF, 14, dashed=True)
        b_sal = T("SA(OFF) · bir kez", 14, SAOFF, BOLD).next_to([L + 0.6, -1.25, 0], DOWN, buff=0.04)
        fx = [L + 0.85 + 0.25 * i for i in range(8)]
        b_f = tick_row(fx, yo - 0.33, FWIC, 0.16, 2.6)
        b_fl = T("FWI · her tahsiste", 14, FWIC, BOLD).move_to([np.mean(fx) - 0.1, 0.08, 0])
        chk = VGroup(*[Line([x, yn_ + 0.25, 0], [x, yn_ + 0.4, 0], color=ACC, stroke_width=2.4) for x in (L + 0.35, L + 1.9)])
        chkl = T("alıcı kontrolü", 14, ACC, BOLD).next_to([L + 1.9, yn_ - 0.25, 0], DOWN, buff=0.06)
        b_ti = T("Itransinit", 14, TMRC, BOLD).next_to([L + 2.25, yn_ - 0.25, 0], DOWN, buff=0.3)
        b_m = vmsg(L + 2.7, yn_ + 0.25, yo - 0.25, "SR(Awake)", SRA, 14, RIGHT, 0.05)
        # (c)
        L, R = P[2]
        c_o = VGroup(sseg(L, L + 2.6, yo, "L", 3, 0.5, 14), sseg(L + 2.6, R, yo, "L", 1, 0.5, 14, short=True))
        c_n = VGroup(sseg(L, R, yn_, "N", 4, 0.5, 14))
        c_q = T("sessiz", 15, WARN, BOLD).move_to([L + 2.9, yn_, 0])
        c_t = tbar(L + 0.15, L + 2.6, yo + 0.4, "Ter_i", TMRC, 0.14, 14, UP)
        c_x = T("✗", 18, WARN, BOLD).next_to([L + 2.6, yo + 0.4, 0], RIGHT, buff=0.04)
        c_m = vmsg(L + 2.7, yo - 0.25, yn_ + 0.25, "SA(OFF)", SAOFF, 14, RIGHT, 0.05)
        c_lob = T("→ LOBi sayımı", 14, WARN, BOLD).next_to([R, yn_ - 0.25, 0], DOWN, buff=0.1).align_to([R, 0, 0], RIGHT)
        wh = VGroup(ytag("bizim yorumumuz"), VGroup(T("SA(OFF)", 17, SAOFF, BOLD), T("= fısıltı · uyuyan alıcı kaçırabilir", 17, TXT, BOLD)).arrange(RIGHT, buff=0.12),
                    VGroup(T("FWI", 17, FWIC, BOLD), T("= bağırış · her tahsiste", 17, TXT, BOLD)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.4)
        fit(wh, 12.8).move_to([0, -2.7, 0])
        self.play(FadeIn(lab), FadeIn(ttl[0]), FadeIn(a_o[0]), FadeIn(a_n[0]), self.set_src("G.989.3 Tablo 16-4 · Tablo 16-5 · Tablo 16-7 · §8.1.1.2.5"), run_time=0.5)
        self.at(self.cue("ONU'da trafik başlarsa", 1.4))
        self.play(FadeIn(a_l), FadeIn(a_n[1], shift=RIGHT * 0.05), GrowArrow(a_m[0]), FadeIn(a_m[1]), run_time=0.55)
        self.at(self.cue("OLT serbest uyanığa döner", 4.4))
        self.play(FadeIn(a_o[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("OLT'de ONU'yu uyandırmak", 6.6))
        self.play(FadeIn(ttl[1]), FadeIn(b_o[0]), FadeIn(b_n[0]), FadeIn(chk[0]), run_time=0.45)
        self.at(self.cue("örneğin trafik", 11.2))
        self.play(FadeIn(b_l, shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("OLT uyarılmış duruma geçer", 12.4))
        self.play(FadeIn(b_o[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("izni bir kez kapatır", 14.7))
        self.play(FadeIn(b_sa), FadeIn(b_sal), run_time=0.4)
        self.at(self.cue("her tahsiste zorunlu", 16.5))
        self.play(LaggedStart(*[Create(t) for t in b_f], lag_ratio=0.12), FadeIn(b_fl), run_time=0.7)
        self.play(FadeIn(chk[1]), FadeIn(chkl), FadeIn(b_n[1]), FadeIn(b_ti), run_time=0.4)
        self.play(FadeIn(b_n[2]), GrowArrow(b_m[0]), FadeIn(b_m[1]), FadeIn(b_o[2]), run_time=0.45)
        self.at(self.cue("ONU susarsa", 20.7))
        self.play(FadeIn(ttl[2]), FadeIn(c_o[0]), FadeIn(c_n), FadeIn(c_q), GrowFromEdge(c_t[0], LEFT), FadeIn(c_t[1]), run_time=0.6)
        self.at(self.cue("OLT zorla uyanığa döner", 24.3))
        self.play(FadeIn(c_x), FadeIn(c_o[1], shift=RIGHT * 0.05), GrowArrow(c_m[0]), FadeIn(c_m[1]), FadeIn(c_lob), run_time=0.55)
        self.at(self.cue("kapalı izin bir fısıltıdır", 27.7))
        self.play(FadeIn(wh[0]), FadeIn(wh[1], shift=UP * 0.05), Indicate(b_sa, color=SAOFF, scale_factor=1.1), run_time=0.55)
        self.at(self.cue("bir bağırıştır", 32.4))
        self.play(FadeIn(wh[2], shift=UP * 0.05), Indicate(b_f, color=FWIC, scale_factor=1.15), run_time=0.55)
        self.end(pad=0.05)

        # b13 — managing a sleeping ONU (§16.1.4): in LowPower with Rx off it cannot receive commands, ignores DBRu / PLOAMu; the OLT must allow
        #       extra time beyond the normal 750 µs for a PLOAM reply; recommendation: wake the ONU before management transactions
        self.beat("b13")
        h = self.reset("Uyuyan ONU'yu yönetmek — §16.1.4", "std", 0.5)
        st = pst("N", 4, 2.5, 0.8, 18, 14).move_to([-4.6, 1.25, 0])
        rx = VGroup(rx_icon(False, 0.34), T("alıcı kapalı", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.12).next_to(st, DOWN, buff=0.18)
        ins = VGroup(*[VGroup(mbox(s, c, 2.3, 0.38, 15), T("✗", 18, WARN, BOLD)).arrange(RIGHT, buff=0.15)
                       for s, c in (("PLOAM ↓", PLC), ("OMCI ↓", OMC), ("DBRu · PLOAMu tahsisi", ACC))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ins.move_to([-4.3, -1.1, 0])
        insl = T("komut alamaz · yok sayar", 15, WARN, BOLD).next_to(ins, DOWN, buff=0.15).align_to(ins, LEFT)
        ax, X = frame_axis(14, -0.6, 5.7, 0.55, labels=True, size=14, every=2)
        pl = vmsg(X(0), 1.55, 0.6, "PLOAM ↓", PLC, 14, RIGHT)
        nw = Rectangle(width=X(6) - X(0), height=0.3, stroke_color=GOLD, stroke_width=1.6, fill_color=GOLD, fill_opacity=0.3).move_to([(X(0) + X(6)) / 2, -0.15, 0])
        nwl = T("normal: ≤ 750 µs = 6 çerçeve (§11.1.2)", 15, GOLD, BOLD).next_to(nw, DOWN, buff=0.08).align_to(nw, LEFT)
        xw = DashedVMobject(Rectangle(width=X(14) - X(6), height=0.3, stroke_color=WARN, stroke_width=1.8), num_dashes=24).move_to([(X(6) + X(14)) / 2, -0.15, 0])
        xwl = T("+ ek süre · değeri yazılı değil", 15, WARN, BOLD).next_to(xw, DOWN, buff=0.45).align_to(xw, RIGHT)
        fl = T("çerçeve", 14, MUTED, BOLD).next_to(ax, RIGHT, buff=0.1).shift(DOWN * 0.15)
        rec = VGroup(T("tavsiye:", 17, GOOD, BOLD), mbox("FWI ↓", FWIC, 1.2, 0.4, 15), T("→", 18, MUTED, BOLD), pst("N", 1, 2.3, 0.6, 15, 13), T("→", 18, MUTED, BOLD),
                     mbox("PLOAM · OMCI işlemi", PLC, 2.6, 0.4, 15)).arrange(RIGHT, buff=0.15)
        fit(rec, 7.2).move_to([2.8, -2.35, 0])
        self.play(FadeIn(st), self.set_src("G.989.3 §16.1.4 · §11.1.2"), run_time=0.4)
        self.at(self.cue("alıcısı kapalıyken ONU", 2.9))
        self.play(FadeIn(rx, shift=UP * 0.05), FadeIn(ins[0]), FadeIn(ins[1]), run_time=0.5)
        self.at(self.cue("durum raporu ve PLOAM", 6.0))
        self.play(FadeIn(ins[2]), FadeIn(insl), run_time=0.45)
        self.at(self.cue("normalde yedi yüz elli", 10.3))
        self.play(Create(ax), FadeIn(fl), GrowArrow(pl[0]), FadeIn(pl[1]), run_time=0.5)
        self.play(GrowFromEdge(nw, LEFT), FadeIn(nwl), run_time=0.45)
        self.at(self.cue("ek süre tanımalıdır", 14.5))
        self.play(Create(xw), FadeIn(xwl), run_time=0.5)
        self.at(self.cue("yönetim işleminden önce", 19.2))
        self.play(FadeIn(rec, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # b14 — engineer note: FWI valid only in the first allocation structure of a series; Table 16-5 "normal allocations" vs §7 "allocation
        #       minimization" — our reading: withhold allocations long enough and the 10 s TO6 (restarted by allocations) can expire
        self.note11("b14", [("1", "FWI yalnızca serinin ilk tahsis yapısında geçerlidir",
                             "Sonraki yapılardaki FWI'nin değeri denetlenmez; ONU onu yok sayar (§8.1.1.2.5).", "zorunlu uyandırma biti yalnızca"),
                            ("2", "Normal tahsis mi, en aza indirme mi?",
                             "Tablo 16-5: 'normal tahsis' · §7: 'tahsisi en aza indirme'. Bizim yorumumuz: tahsisleri uzun süre\nkeserseniz, tahsisle yeniden başlayan 10 s'lik TO6 dolabilir.", "İki:")])
        self.bridge_beat("b15", "Uyumanın kuralları belli.\nPeki bu uyku ne kazandırır, ve ne kadar geciktirir?")
        self.save_timeline("ep19_p1C")
