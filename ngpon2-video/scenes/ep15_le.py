"""S2·B5 · Laboratuvarda (PLOAM yakalama, altın vektörler, varsayılan anahtarla doğrulama, anahtar türetme, sıra numaraları,
işleme süresi, canlılık, olumsuz durumlar, güç dengeleme, profiller, neden kodları ve OMCI) and Kapanış."""
from ep15_common import *

EXAMPLES = [["Deactivate_ONU-ID · yayın · SeqNo 1", "03ff 05 01 · RC 0000", "eaef6afe6fd5b497"],
            ["Disable_Serial_Number · 0x0F · SeqNo 2", "03ff 06 02 · 0f", "33adf1f7c67f2f7b"],
            ["Request_Registration · ONU 0x13 · SeqNo 4", "0013 09 04", "0293c646da331d7f"]]
POINTS = [("PLOAM: sabit 48 B · bant içi; AMCC'de yalnızca 2 ↑ mesaj\nçerçeve başına 1 yayın + ONU başına 1 tek alıcılı · kuyruk 8 · 750 µs", "§11.1"),
          ("sıra numarası: ↓ 1'den başlar, 0'ı atlar\n↑ yalnızca yansıtır · 0 = sırasız", "§11.2.3"),
          ("MIC: Cdir + 40 B → 64 bit\nyayın ve aktivasyon: herkesin bildiği anahtar 0x55 × 16", "§15.6 · §15.3.3"),
          ("iki değişiklik: dolguda iki neden kodu\nBurst_Profile: en son gelen kazanır", "Amd.1 · Amd.2"),
          ("OMCC: Port-ID = Alloc-ID = ONU-ID\n4 B kendi MIC'i · varsayılan anahtarı yok", "§6.1.4.3 · §15.7")]


def two_line_chip(top, bot, color, w=1.05, h=0.7):
    r = RoundedRectangle(corner_radius=0.05, width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.22)
    g = VGroup(HX(top, 14, TXT, BOLD), T(bot, 14, color, BOLD)).arrange(DOWN, buff=0.08).move_to(r)
    return VGroup(r, g)


class E15LabA(Act15):
    HDR, MANIFEST, FIRST = H15["L"], M15("lab"), True

    def construct(self):
        # g1 — bench: analyzer on a splitter (both directions), OLT and ONU emulators, power meter, wavemeter; method vs criteria
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "PLOAM yakalama ve bütünlük doğrulama")
        self.at(self.cue("Düzenek", 1.1))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Düzenek")
        y = 1.0
        eo = emu_icon(2.0, 1.35, "OLT emülatörü").move_to([-5.15, y, 0])
        sp = VGroup(splitter(0.38), T("ayırıcı", 15, FEED, BOLD)).arrange(DOWN, buff=0.1).move_to([-2.6, y - 0.12, 0])
        eu = emu_icon(2.0, 1.35, "ONU emülatörü").move_to([0.15, y, 0])
        pa = pa_icon(2.0, 1.35, "Protokol analizörü · ↓ ↑").move_to([-2.6, -1.1, 0])
        pm = inst("PM", "Güç ölçer", 1.75, 1.2, "dBm").move_to([3.15, 1.45, 0])
        wm = inst("PM", "Dalga boyu ölçer", 1.75, 1.2, "λ", None, GOLD).move_to([3.15, -0.6, 0])
        f1 = Line(eo[0].get_right(), sp[0].get_left(), color=FEED, stroke_width=3)
        f2 = Line(sp[0].get_right(), eu[0].get_left(), color=FEED, stroke_width=3)
        f3 = DashedLine(sp[0].get_bottom(), pa[0].get_top(), color=FEED, stroke_width=2.5, dash_length=0.1)
        f4 = VGroup(Line(eu[0].get_right(), pm[0].get_left(), color=FEED, stroke_width=2.5), Line(eu[0].get_right(), wm[0].get_left(), color=FEED, stroke_width=2.5))
        bt = VGroup(tag("yöntem: yalnızca altın vektörler · Ek IV", GOLD, 16), interp("yorum"), T("diğer testler: mühendislik pratiği", 17, TXT, BOLD),
                    tag("ölçütler: standarttan", GOOD, 16)).arrange(RIGHT, buff=0.22)
        fit(bt, 12.8).move_to([0, -2.75, 0])
        self.at(self.cue("dinleyen bir protokol", 4.6))
        self.play(self.set_src("G.989.3 Ek IV · §11 · tezgâh: yorum"), FadeIn(sp), FadeIn(pa, shift=UP * 0.1), Create(f3), run_time=0.7)
        self.at(self.cue("bir OLT emülatörü", 6.6))
        self.play(FadeIn(eo, shift=RIGHT * 0.1), Create(f1), run_time=0.5)
        self.at(self.cue("bir ONU emülatörü", 8.2))
        self.play(FadeIn(eu, shift=LEFT * 0.1), Create(f2), run_time=0.5)
        self.at(self.cue("bir güç ölçer", 9.9))
        self.play(FadeIn(pm, shift=LEFT * 0.1), Create(f4[0]), run_time=0.5)
        self.at(self.cue("bir dalga boyu ölçer", 11.5))
        self.play(FadeIn(wm, shift=LEFT * 0.1), Create(f4[1]), run_time=0.5)
        self.at(self.cue("altın vektörler için", 14.0))
        self.play(FadeIn(bt[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("mühendislik pratiğidir", 18.7))
        self.play(FadeIn(bt[1:3], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ölçütleri ise", 22.4))
        self.play(FadeIn(bt[3], shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g2 — TEST 1: find the PLOAMd partition (P from HLend), slice 48 × P; per-frame limits; ONU-ID checks
        self.beat("g2")
        self.clear(h)
        self.play(FadeOut(h), run_time=0.3)
        h = step_head(self, 1, "PLOAM bölmesini bulmak")
        ds = strip([FS_(1.0, "HLend"), FS_(1.9, "BWmap · 8N B", BWC), FS_(3.3, "PLOAMd · 48 × P B", PLDC, 0.3), (4.8, "FS yükü", PAYC, 0.12),
                    FS_(0.8, "BIP", BIPC, 0.4)], -6.0, 1.45, 0.55, 15)
        hp = apanel(2.7, 1.45, "HLend · örnek", ACC).move_to([-5.0, -1.35, 0])
        hr = VGroup(kv("N", "6", kw=0.8), kv("P", "3", kw=0.8)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(hp[0]).shift(DOWN * 0.18)
        hr[1][1].set_color(PLDC)
        ha = CurvedArrow(ds[0].get_bottom(), hp[0].get_top() + RIGHT * 0.3, angle=0.4, color=ACC, stroke_width=2, tip_length=0.1)
        chips = VGroup(two_line_chip("0x3FF", "yayın", BCC), two_line_chip("0x013", "tek alıcılı", UCC), two_line_chip("0x007", "tek alıcılı", UCC)).arrange(RIGHT, buff=0.06)
        chips.next_to(ds[2], DOWN, buff=0.75)
        zl = zoom_lines(ds[2], chips)
        cb = brace_lbl(chips, "3 × 48 B · ONU-ID'ye göre ayır", PLDC, DOWN, 15)
        cks = VGroup(chk("≤ 1 yayın / çerçeve", True, 17), chk("ONU başına ≤ 1 tek alıcılı / çerçeve", True, 17), chk("ONU-ID'nin üst 6 biti = 0", True, 17),
                     chk("0x3FD (1021) · 0x3FE (1022) hiç yok", True, 17)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cks.move_to([3.6, -0.75, 0])
        self.play(self.set_src("G.989.3 §8.1.1.1 · §11.1.2 · §11.2.1"), FadeIn(ds), run_time=0.6)
        self.at(self.cue("PLOAM sayısını okuyun", 2.7))
        self.play(Create(ha), FadeIn(hp), FadeIn(hr), run_time=0.7)
        self.at(self.cue("kırk sekiz çarpı P", 7.0))
        self.play(Create(zl), LaggedStart(*[FadeIn(c, shift=DOWN * 0.05) for c in chips], lag_ratio=0.2), FadeIn(cb), run_time=0.9)
        self.at(self.cue("en çok bir yayın", 11.5))
        self.play(FadeIn(cks[0], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("her ONU için en çok", 14.5))
        self.play(FadeIn(cks[1], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("üstteki altı biti", 18.6))
        self.play(FadeIn(cks[2], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("bin yirmi bir ve", 22.5))
        self.play(FadeIn(cks[3], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g3 — TEST 2: golden vectors IV.9 (46 39 …) and IV.10 (Cdir 0x02); a flipped direction byte must change everything
        self.beat("g3")
        self.clear(h)
        h = step_head(self, 2, "Altın vektörler — Ek IV.9 · IV.10", h)
        p = apanel(12.4, 2.25, "Ek IV.9 · ↓ Assign_Alloc-ID · ONU 0x13 · PLOAM_IK (Ek IV.8)", GOLD).move_to([0, 0.95, 0])
        rows = VGroup(kv("Cdir", "01", kw=2.6), kv("oktet 1–9", "00 13 0a 03 04 45 01 00 00", kw=2.6), kv("oktet 10–40", "31 × 00", kw=2.6),
                      kv("MIC · Ek IV.9", "46 39 87 56 28 08 14 e6", kw=2.6)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.move_to(p[0]).shift(DOWN * 0.18).align_to(p[0], LEFT).shift(RIGHT * 0.4)
        rows[3][1].set_color(MICC)
        g46 = SurroundingRectangle(rows[3][1][0:2], color=GOLD, buff=0.05, stroke_width=3)
        g39 = SurroundingRectangle(rows[3][1][2:4], color=GOLD, buff=0.05, stroke_width=3)
        cond = VGroup(tag("hesap", GOLD, 14), T("tutması için: kapsam = 0x0000 ve dolgu = 0", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        cond.next_to(p[0], DOWN, buff=0.15).align_to(p[0], RIGHT)
        iv10 = VGroup(tag("Ek IV.10", GOLD, 15), T("↑ Sleep_Request · Cdir = 0x02 →", 17, TXT, BOLD), HX("fe af 8d 09 20 8f 0d 9b", 18, MICC, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.18)
        iv10.move_to([0, -1.05, 0])
        flip = VGroup(T("IV.9 gövdesi, Cdir bilerek 0x02 →", 17, TXT, BOLD), HX("22 9a 69 aa 5b 6e 50 54", 18, WARN, BOLD), tag("hesap", GOLD, 14))
        flip.arrange(RIGHT, buff=0.18).move_to([0, -1.95, 0])
        rej = VGroup(T("kod tamamen değişir →", 17, TXT, BOLD), T("çözücü mesajı reddetmeli", 17, WARN, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.15).move_to([0, -2.7, 0])
        self.play(self.set_src("G.989.3 Ek IV.9 · Ek IV.10 · (15-7) · hesap"), FadeIn(p), run_time=0.4)
        self.at(self.cue("dokuzuncu örneğinin kodu", 2.4))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.05) for r in rows], lag_ratio=0.15), run_time=0.9)
        self.at(self.cue("dört altı", 5.7))
        self.play(Create(g46), run_time=0.4)
        self.at(self.cue("üç dokuz", 8.1))
        self.play(Create(g39), run_time=0.4)
        self.at(self.cue("kapsam alanı ve dolgu", 10.5))
        self.play(FadeIn(cond, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Onuncu örnek", 15.2))
        self.play(FadeIn(iv10, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("yön baytını bilerek", 18.7))
        self.play(FadeIn(flip[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("kod tamamen değişmeli", 21.8))
        self.play(FadeIn(flip[1:], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("reddetmelidir", 23.7))
        self.play(FadeIn(rej, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g4 — TEST 3: verify broadcasts without secrets: key 16 × 0x55, Cdir 1, octets 1–40; coverage; our computed examples (not golden)
        self.beat("g4")
        self.clear(h)
        h = step_head(self, 3, "Yayınları sır bilmeden doğrulamak", h)
        f = eqline(("MIC = AES-CMAC(", TXT, True), ("55 × 16,", DKC, True), ("01", GOLD, True), ("|", TXT, True), ("oktet 1–40,", CNC, True), ("64)", TXT, True), size=24, buff=0.2)
        f.move_to([0, 1.55, 0])
        cov = VGroup(tag("profiller", FAM["prof"], 16), tag("Assign_ONU-ID", FAM["kim"], 16), tag("Disable_Serial_Number", FAM["dis"], 16),
                     tag("her zaman varsayılan anahtarlı tek alıcılılar", DKC, 16)).arrange(RIGHT, buff=0.18)
        fit(cov, 12.6).move_to([0, 0.6, 0])
        tb = mtable(["mesaj", "oktet 1–4 · içerik", "MIC · varsayılan anahtar"], EXAMPLES, [5.0, 3.4, 3.6], size=17, hsize=15, row_h=0.5, mono=(1, 2))
        tb.move_to([0, -1.25, 0])
        for r in tb[1:]:
            r[3].set_color(MICC)
        nt = tag("hesap — altın vektör değil", WARN, 16).next_to(tb, UP, buff=0.12).align_to(tb, RIGHT)
        self.play(self.set_src("G.989.3 §15.3.3 · (15-7) · örnekler: hesap (Python cryptography AES-CMAC)"), FadeIn(f[0]), FadeIn(f[-1]), run_time=0.4)
        self.at(self.cue("on altı kez beş beş", 4.0))
        self.play(FadeIn(f[1], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("yön baytı bir", 6.3))
        self.play(FadeIn(f[2], shift=UP * 0.05), FadeIn(f[3]), run_time=0.35)
        self.at(self.cue("girdi ilk kırk bayt", 7.5))
        self.play(FadeIn(f[4], shift=UP * 0.05), run_time=0.35)
        for k, (key, d) in enumerate((("profilleri", 9.4), ("kimlik atamayı", 10.4), ("seri numarası engellemeyi", 11.7), ("her zaman varsayılan anahtarlı", 15.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(cov[k], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("Kendi hesapladığımız örnekler", 19.2))
        self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in tb[1:]], lag_ratio=0.2), run_time=0.9)
        self.at(self.cue("altın vektör değildirler", 22.4))
        self.play(FadeIn(nt, scale=0.9), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep15_labA")


class E15LabB(Act15):
    HDR, MANIFEST, PREV_BADGE = H15["L"], M15("lab"), "lab"

    def construct(self):
        # g5 — TEST 4: unicast needs the ONU's key; with registration-based keys an analyzer that saw the activation can derive it (our inference)
        self.beat("g5")
        h = step_head(self, 4, "Tek alıcılılar: ONU'nun anahtarı")
        y = 0.9
        y = 1.25
        bx = [("Registration_ID", "Registration · 5–40", GOLD), ("MSK", "(15-2)", DKC), ("SK", "(15-3)", ACC), ("PLOAM_IK", "(15-5)", SKC)]
        bs = VGroup(*[sbox(a, b, c, 2.7, 0.85, 19, 15) for a, b, c in bx]).arrange(RIGHT, buff=0.5).move_to([0, y, 0])
        fm = VGroup(HX("MSK = AES-CMAC(0x55 × 16, Registration_ID, 128)", 16, DKC, BOLD), HX("SK = AES-CMAC(MSK, SN | PON-TAG | “SessionK”, 128)", 16, ACC, BOLD),
                    HX("PLOAM_IK = AES-CMAC(SK, “PLOAMIntegrtyKey”, 128)", 16, SKC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, -1.45, 0])
        ar = VGroup(*[arrow(bs[i].get_right(), bs[i + 1].get_left(), MUTED, 2.2, 0.1) for i in range(3)])
        ins = VGroup(tile("SN · Serial_Number_ONU 5–12", FAM["kim"], 3.6, 0.48, 15, 0.15), tile("PON-TAG · Burst_Profile 26–33", FAM["prof"], 3.6, 0.48, 15, 0.15))
        ins.arrange(RIGHT, buff=0.3).move_to([bs[2].get_x() - 0.6, 0.0, 0])
        ia = VGroup(*[arrow(i.get_top(), bs[2].get_bottom() + RIGHT * (0.5 * k - 0.25), FAM["kim"] if k == 0 else FAM["prof"], 2, 0.1) for k, i in enumerate(ins)])
        inf = tag("çıkarım · (15-2) (15-3) (15-5)", GOLD, 16).next_to(bs, UP, buff=0.3)
        reg = T("anahtarlar kayıt tabanlıysa:", 17, TXT, BOLD).next_to(inf, LEFT, buff=0.3)
        no = VGroup(T("diğer iki kimlik doğrulama yöntemi (OMCI tabanlı · IEEE 802.1X):", 17, TXT, BOLD), T("türetilemez", 17, WARN, BOLD), ok_x(False, 18)).arrange(RIGHT, buff=0.15)
        fit(no, 12.6).move_to([0, -2.75, 0])
        self.play(self.set_src("G.989.3 §15.3.3 · (15-2) · (15-3) · (15-5) · çıkarım"), run_time=0.2)
        self.at(self.cue("Bizim çıkarımımız", 5.0))
        self.play(FadeIn(inf, shift=DOWN * 0.05), run_time=0.4)
        self.at(self.cue("kayıt tabanlıysa", 6.6))
        self.play(FadeIn(reg), FadeIn(bs[0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("baştan görmüş bir analizör", 9.0))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(ar[k]), FadeIn(bs[k + 1], shift=RIGHT * 0.05), FadeIn(fm[k])) for k in range(3)], lag_ratio=0.5), run_time=1.5)
        self.at(self.cue("kayıt kimliği,", 13.5))
        self.play(Indicate(bs[0], color=GOLD, scale_factor=1.05), run_time=0.6)
        self.at(self.cue("PON etiketi yeter", 16.0))
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.05) for i in ins], lag_ratio=0.3), *[GrowArrow(a) for a in ia], run_time=0.8)
        self.at(self.cue("Diğer iki kimlik doğrulama", 19.3))
        self.play(FadeIn(no, shift=UP * 0.05), run_time=0.5)
        self.end(pad=0.05)

        # g6 — TEST 5: sequence numbers: broadcast +1, 255 → 1, never 0 (except Calibration_Request); per-ONU flow from 1; echo; keep-alive 0
        self.beat("g6")
        self.clear(h)
        h = step_head(self, 5, "Sıra numaraları", h)
        pl = apanel(6.3, 3.0, "↓ yayın akışı · yakalama", BCC).move_to([-3.3, 0.45, 0])
        caps = [("System_Profile", "253", True), ("Channel_Profile", "254", True), ("Burst_Profile", "255", True), ("Channel_Profile", "1", True),
                ("Calibration_Request", "0", None)]
        cr = VGroup()
        for n, v, ok in caps:
            a = T(n, 16, TXT, SEMIBOLD)
            b = HX(v, 18, GOLD if ok else WARN, BOLD)
            c = ok_x(True, 17) if ok else tag("istisna", WARN, 14)
            row = VGroup(a, b, c)
            cr.add(row)
        cr.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(pl[0]).shift(DOWN * 0.2).align_to(pl[0], LEFT).shift(RIGHT * 0.3)
        for row in cr:
            row[1].move_to([pl[0].get_left()[0] + 3.6, row[0].get_y(), 0])
            row[2].move_to([pl[0].get_left()[0] + 4.55, row[0].get_y(), 0], aligned_edge=LEFT)
        wr = T("255 → 1 · 0 yok", 15, GOLD, BOLD).next_to(pl[0], DOWN, buff=0.1).align_to(pl[0], RIGHT)
        pr = apanel(5.8, 3.0, "ONU 0x13 · tek alıcılı akış", UCC).move_to([3.45, 0.45, 0])
        rr = VGroup(VGroup(T("Assign_ONU-ID", 16, TXT, SEMIBOLD), T("→", 16, MUTED, BOLD), HX("1, 2, 3 …", 17, UCC, BOLD)).arrange(RIGHT, buff=0.15),
                    VGroup(T("kanal devri · Complete_u", 16, TXT, SEMIBOLD), T("→", 16, MUTED, BOLD), HX("1, 2 …", 17, UCC, BOLD)).arrange(RIGHT, buff=0.15),
                    chk("cevap SeqNo = ↓ SeqNo", True, 16), chk("canlılık onayı SeqNo = 0", True, 16)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rr.move_to(pr[0]).shift(DOWN * 0.2)
        self.play(self.set_src("G.989.3 §11.2.3 · Tablo 11-14 · Tablo 11-28"), FadeIn(pl), run_time=0.4)
        self.at(self.cue("her mesajda bir artmalı", 2.5))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.05) for r in cr[:3]], lag_ratio=0.2), run_time=0.8)
        self.at(self.cue("iki yüz elli beşten bire", 5.5))
        self.play(FadeIn(cr[3], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("sıfır görünmemelidir", 8.3))
        self.play(FadeIn(wr), run_time=0.4)
        self.at(self.cue("kalibrasyon isteğidir", 10.1))
        self.play(FadeIn(cr[4], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("ONU başına akış", 12.9))
        self.play(FadeIn(pr), FadeIn(rr[0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("kanal devri tamamlandıktan", 16.5))
        self.play(FadeIn(rr[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("yansıtmalı", 20.4))
        self.play(FadeIn(rr[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("sıfır taşımalıdır", 23.8))
        self.play(FadeIn(rr[3], shift=RIGHT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g7 — TEST 6: processing time: directed message in DS frame N, a PLOAMu grant every frame → answer by US frame N+6; 8 back-to-back ≤ 6 apart
        self.beat("g7")
        self.clear(h)
        h = step_head(self, 6, "İşleme süresi", h)
        n, w, x0 = 13, 0.9, -5.6
        dsc, _ = frame_cells(n, x0, w, 1.3, 0.5, TW_DS)
        usc, ulb = frame_cells(n, x0, w, 0.45, 0.5, TW_US, nlabels(n), 14)
        rl = VGroup(T("↓", 20, TW_DS, BOLD).next_to(dsc, LEFT, buff=0.15), T("↑", 20, TW_US, BOLD).next_to(usc, LEFT, buff=0.15))
        m = mbox("mesaj", UCC, 0.8, 0.34, 14).move_to(dsc[0])
        gp = VGroup(*[Rectangle(width=0.16, height=0.36, stroke_width=0, fill_color=PLDC, fill_opacity=0.8).move_to(c).align_to(c, LEFT).shift(RIGHT * 0.06) for c in usc])
        gpl = T("her ↑ çerçevede PLOAMu tahsisi", 15, PLDC, BOLD).next_to(usc, DOWN, buff=0.38).align_to(usc, LEFT)
        rp = mbox("cevap", GOOD, 0.72, 0.34, 14).move_to(usc[6]).shift(RIGHT * 0.08)
        ca = CurvedArrow(m.get_bottom(), rp.get_top(), angle=0.3, color=GOOD, stroke_width=2, tip_length=0.1)
        ok = VGroup(T("en geç N+6", 17, GOOD, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.12).next_to(dsc[8], UP, buff=0.12)
        ax, X = frame_axis(48, -5.6, 6.1, -1.9, labels=False)
        axl = VGroup(T("0", 14, MUTED, BOLD).next_to([X(0), -1.9, 0], DOWN, buff=0.1), T("48 çerçeve", 14, MUTED, BOLD).next_to([X(48), -1.9, 0], DOWN, buff=0.1))
        tl = T("8 mesaj art arda →", 16, TXT, BOLD).next_to(ax, UP, buff=0.45).align_to(ax, LEFT)
        rm = VGroup(*[Triangle(color=GOOD, fill_color=GOOD, fill_opacity=0.9).scale(0.09).rotate(PI).move_to([X(6 * (k + 1)), -1.68, 0]) for k in range(8)])
        sp = VGroup(*[BraceBetweenPoints([X(6 * k), -2.15, 0], [X(6 * (k + 1)), -2.15, 0], DOWN, color=GOOD) for k in range(1, 3)])
        spl = T("cevaplar arası ≤ 6 çerçeve", 16, GOOD, BOLD).next_to(sp, DOWN, buff=0.06)
        self.play(self.set_src("G.989.3 §11.1.2 · yöntem: yorum"), FadeIn(dsc), FadeIn(usc), FadeIn(ulb), FadeIn(rl), run_time=0.5)
        self.at(self.cue("N numaralı çerçevede yönlendirilmiş", 2.3))
        self.play(FadeIn(m, shift=DOWN * 0.06), run_time=0.4)
        self.at(self.cue("her çerçevede PLOAM tahsisi", 8.2))
        self.play(LaggedStart(*[FadeIn(g) for g in gp], lag_ratio=0.05), FadeIn(gpl), run_time=0.8)
        self.at(self.cue("N artı altıncı", 12.0))
        self.play(Create(ca), FadeIn(rp, shift=UP * 0.05), FadeIn(ok), run_time=0.7)
        self.at(self.cue("sekiz mesajı art arda", 17.2))
        self.play(FadeIn(ax), FadeIn(axl), FadeIn(tl), LaggedStart(*[FadeIn(r, shift=DOWN * 0.05) for r in rm], lag_ratio=0.1), run_time=1.0)
        self.at(self.cue("en çok altı çerçeve", 20.3))
        self.play(FadeIn(sp), FadeIn(spl), run_time=0.5)
        self.end(pad=0.05)

        # g8 — TEST 7: keep-alive: empty queue → Ack SeqNo 0, code 1; while processing → code 2; Ind MSB = 1 while messages are pending
        self.beat("g8")
        self.clear(h)
        h = step_head(self, 7, "Canlılık", h)
        p1 = apanel(5.8, 1.9, "kuyruk boş · PLOAMu verildi", ACC).move_to([-3.25, 1.0, 0])
        r1 = VGroup(kv("SeqNo", "0x00", kw=1.8), kv("Completion", "0x01 · mesaj yok", kw=1.8)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(p1[0]).shift(DOWN * 0.18)
        p2 = apanel(5.8, 1.9, "mesaj işlenirken · PLOAMu verildi", GOLD).move_to([3.25, 1.0, 0])
        r2 = VGroup(kv("tür", "0x09 · Acknowledgement", kw=1.8), kv("Completion", "0x02 · meşgul", kw=1.8)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(p2[0]).shift(DOWN * 0.18)
        r1[1][1].set_color(ACC)
        r2[1][1].set_color(GOLD)
        uh = fields(USHDR, 7.0, 0.55, 16, 14, unit=" bit").move_to([-1.0, -1.35, 0])
        uhl = T("↑ FS başlığı", 15, MUTED, BOLD).next_to(uh, UP, buff=0.12).align_to(uh, LEFT)
        ir = uh[1][0]
        ib = Rectangle(width=ir.width / 9, height=ir.height, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.85).align_to(ir, LEFT).align_to(ir, UP)
        ibl = VGroup(T("Ind'in en anlamlı biti", 17, TXT, BOLD), T("= 1 · bekleyen mesaj var", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        ibl.move_to([ib.get_x() - 0.3, -2.65, 0], aligned_edge=LEFT)
        iba = arrow(ib.get_bottom() + DOWN * 0.03, [ib.get_x(), ibl.get_top()[1] + 0.05, 0], GOLD, 2, 0.1)
        self.play(self.set_src("G.989.3 §11.1.3 · Tablo 11-28 · §8.1.2.1"), run_time=0.2)
        self.at(self.cue("Kuyruk boşken", 1.9))
        self.play(FadeIn(p1), run_time=0.4)
        self.at(self.cue("sıra numarası sıfır ve kodu bir", 4.9))
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.05) for r in r1], lag_ratio=0.3), run_time=0.7)
        self.at(self.cue("bir mesaj işlenirken", 9.6))
        self.play(FadeIn(p2), FadeIn(r2[0], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("kodu iki olan", 12.6))
        self.play(FadeIn(r2[1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("gösterge alanının en anlamlı", 15.5))
        self.play(FadeIn(uhl), FadeIn(uh), run_time=0.5)
        self.play(FadeIn(ib), run_time=0.3)
        self.at(self.cue("bekleyen mesaj varken", 21.1))
        self.play(FadeIn(ibl, shift=LEFT * 0.05), GrowArrow(iba), run_time=0.5)
        self.end(pad=0.05)
        self.save_timeline("ep15_labB")


class E15LabC(Act15):
    HDR, MANIFEST, PREV_BADGE = H15["L"], M15("lab"), "lab"

    def construct(self):
        # g9 — TEST 8: negative cases: unknown type → Ack 0x03; broadcast → silence; flipped MIC bit → no Ack, counter +1; US ×3 → LOPCi
        self.beat("g9")
        h = step_head(self, 8, "Olumsuz durumlar")
        tb = mtable(["uyaran", "beklenen"], [["ONU-ID'sine bilinmeyen tür", "Ack · kod 0x03"], ["aynı tür · yayın (0x3FF)", "sessizlik"],
                                            ["MIC'te tek bit çevrik", "onay yok · PLOAM MIC hata sayacı +1"], ["↑ aynı hata art arda 3 kez", "OLT: LOPCi ilan eder"]],
                    [5.2, 5.9], size=18, hsize=16, row_h=0.62).move_to([-0.7, 0.35, 0])
        cols = [ACC, MUTED, MICC, WARN]
        for r, c in zip(tb[1:], cols):
            r[2].set_color(c)
        lp = sbox("LOPCi", "PLOAM kanalı kaybı", WARN, 2.4, 0.9, 20, 14).move_to([5.3, -2.35, 0])
        cnt = VGroup(T("PLOAM MIC hataları:", 16, MUTED, BOLD), HX("n → n+1", 18, MICC, BOLD)).arrange(RIGHT, buff=0.15).move_to([-2.3, -2.35, 0])
        self.play(self.set_src("G.989.3 §11.2.2 · §11.1.3 · Tablo 14-1 · Tablo 14-2"), FadeIn(tb[0]), run_time=0.3)
        steps = [("bilinmeyen bir tür gönderin", 2.8, 1), ("kodu üç olan", 6.7, 2), ("Aynı türü yayınla", 9.2, 1), ("sessizlik", 11.5, 2),
                 ("tek bir biti çevirin", 12.4, 1), ("onay gelmemeli", 15.6, 2)]
        for key, d, part in steps:
            self.at(self.cue(key, d))
            k = 1 + [s[0] for s in steps].index(key) // 2
            if part == 1:
                self.play(FadeIn(tb[k][0]), FadeIn(tb[k][1], shift=RIGHT * 0.05), run_time=0.35)
            else:
                self.play(FadeIn(tb[k][2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("hatası sayacı artmalıdır", 16.9))
        self.play(FadeIn(cnt, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("art arda üç kez", 19.7))
        self.play(FadeIn(tb[4][0]), FadeIn(tb[4][1], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("PLOAM kanalı kaybını", 24.1))
        self.play(FadeIn(tb[4][2], shift=RIGHT * 0.05), FadeIn(lp, scale=0.9), run_time=0.5)
        self.end(pad=0.05)

        # g10 — TEST 9: power levelling: power meter on the ONU, OLT RSSI log; decrease → one 3 dB step (or next level); Ack attenuation = measured; limit → code 4, no change
        self.beat("g10")
        self.clear(h)
        h = step_head(self, 9, "Güç dengeleme", h)
        onu = onu_box("ONU", ONUC, 1.2, 0.55, 17).move_to([-5.4, 1.2, 0])
        pm = inst("PM", "Güç ölçer · ONU çıkışı", 1.7, 1.15, "dBm").move_to([-3.2, 1.2, 0])
        olt = VGroup(sbox("OLT", "RSSI okuması", OLTC, 2.2, 0.75, 18, 14)).move_to([-4.3, -0.7, 0])
        l1 = Line(onu.get_right(), pm[0].get_left(), color=FEED, stroke_width=2.5)
        l2 = arrow(onu.get_bottom(), olt.get_top() + LEFT * 0.4, FEED, 2, 0.1)
        x0, x1 = -1.2, 6.2
        yax, Y = v_axis(-7, 1, -2.6, 1.6, x0, [0, -3, -6], labels=[0, -3, -6], size=15, fmt=lambda v: tr(v))
        yl = T("dB", 15, MUTED).next_to(yax, UP, buff=0.08)
        xa = Line([x0, -2.6, 0], [x1, -2.6, 0], color=MUTED, stroke_width=2)
        xl = T("zaman →", 15, MUTED).next_to(xa, DOWN, buff=0.08).align_to(xa, RIGHT)
        tA, tB, tC = x0 + 1.6, x0 + 4.4, x1
        s1 = Line([x0, Y(0), 0], [tA, Y(0), 0], color=PWC, stroke_width=4)
        s2 = VGroup(Line([tA, Y(0), 0], [tA, Y(-3), 0], color=PWC, stroke_width=4), Line([tA, Y(-3), 0], [tB, Y(-3), 0], color=PWC, stroke_width=4))
        s3 = Line([tB, Y(-3), 0], [tC, Y(-3), 0], color=PWC, stroke_width=4)
        c1 = VGroup(DashedLine([tA, Y(0.6), 0], [tA, Y(-3.5), 0], color=GOLD, stroke_width=1.6, dash_length=0.08), T("“azalt”", 15, GOLD, BOLD).move_to([tA, Y(0.85), 0]))
        st = VGroup(T("−3 dB · bir adım", 16, PWC, BOLD), T("ya da desteklenen", 14, MUTED, BOLD), T("bir sonraki düzey", 14, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        st.move_to([tA + 0.25, Y(-1.5), 0], aligned_edge=LEFT)
        ak = VGroup(T("Ack OK · zayıflatma", 15, TXT, BOLD), HX("0001", 16, PWC, BOLD), T("= ölçülen düşüş", 15, GOOD, BOLD), ok_x(True, 16)).arrange(RIGHT, buff=0.12)
        ak.move_to([(tA + tC) / 2 + 0.3, Y(-4.6), 0])
        c2 = VGroup(DashedLine([tB, Y(0.6), 0], [tB, Y(-3.5), 0], color=WARN, stroke_width=1.6, dash_length=0.08), T("sınır isteği", 15, WARN, BOLD).move_to([tB, Y(0.85), 0]))
        lim = VGroup(T("kod 0x04 · güç değişmez", 15, WARN, BOLD)).next_to([(tB + tC) / 2, Y(-3), 0], UP, buff=0.12)
        self.play(self.set_src("G.989.3 Tablo 11-21 · §12.1.6.2 · Tablo 14-2 (ALRFi) · yöntem: yorum"), run_time=0.2)
        self.at(self.cue("ONU çıkışına güç ölçeri", 2.5))
        self.play(FadeIn(onu), FadeIn(pm), Create(l1), run_time=0.5)
        self.at(self.cue("alınan güç okumasını", 5.0))
        self.play(GrowArrow(l2), FadeIn(olt), run_time=0.5)
        self.play(FadeIn(yax), FadeIn(yl), Create(xa), FadeIn(xl), Create(s1), run_time=0.6)
        self.at(self.cue("Gücü azalt komutu", 8.5))
        self.play(FadeIn(c1), Create(s2), run_time=0.7)
        self.at(self.cue("üç desibellik bir adım", 10.0))
        self.play(FadeIn(st[0]), run_time=0.3)
        self.at(self.cue("desteklenen bir sonraki", 12.0))
        self.play(FadeIn(st[1:]), run_time=0.3)
        self.at(self.cue("zayıflatma baytı ölçtüğünüz", 16.5))
        self.play(FadeIn(ak, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("Sınırdaki bir istekte", 21.3))
        self.play(FadeIn(c2), Create(s3), run_time=0.6)
        self.at(self.cue("güç değişmemelidir", 24.6))
        self.play(FadeIn(lim, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g11 — TEST 10: profiles vs optics (wavemeter, gated scope); the Amd.2 rule: broadcast → new-version unicast → broadcast; latest wins
        self.beat("g11")
        self.clear(h)
        h = step_head(self, 10, "Profiller ve optik", h)
        f1 = VGroup(mtile(0x18, "Channel_Profile · frekanslar", "prof", 3.95, 0.42, 15), T("→", 20, MUTED, BOLD)).arrange(RIGHT, buff=0.15).move_to([-4.0, 1.35, 0])
        wm = inst("PM", "Dalga boyu ölçer", 1.6, 1.1, "λ", None, GOLD).next_to(f1, RIGHT, buff=0.2)
        f2 = VGroup(mtile(0x01, "Burst_Profile · önsöz, sınırlayıcı", "prof", 3.95, 0.42, 15), T("→", 20, MUTED, BOLD)).arrange(RIGHT, buff=0.15).move_to([-4.0, -0.45, 0])
        osc = inst("OSC", "Kapılı osiloskop", 1.6, 1.1).next_to(f2, RIGHT, buff=0.2)
        rx = 3.85
        rt = T("yeni kural · Amd.2", 18, GOLD, BOLD).move_to([rx, 1.75, 0])
        seq = VGroup(mbox("yayın · v1", BCC, 1.45, 0.42, 15), mbox("ONU 7 · v2", UCC, 1.45, 0.42, 15), mbox("yayın · v3", BCC, 1.45, 0.42, 15)).arrange(DOWN, buff=0.35)
        seq.move_to([rx - 0.9, 0.0, 0])
        sar = VGroup(*[arrow(seq[i].get_bottom(), seq[i + 1].get_top(), MUTED, 1.8, 0.09) for i in range(2)])
        use = VGroup(*[T(f"ONU 7 kullanır: {s}", 15, GOOD, BOLD).next_to(seq[i], RIGHT, buff=0.3) for i, s in enumerate(("v1", "v2", "v3"))])
        idx = T("aynı indeks k", 15, MUTED, BOLD).next_to(seq, UP, buff=0.15)
        res = VGroup(T("ONU her seferinde en son geleni kullanmalı", 17, TXT, BOLD), ok_x(True, 18)).arrange(RIGHT, buff=0.15).move_to([0, -2.55, 0])
        self.play(self.set_src("G.989.3 Tablo 11-18 · Tablo 11-4 · §11.3.3.1 (Amd.2) · yöntem: yorum"), run_time=0.2)
        self.at(self.cue("dalga boyu ölçerle", 2.7))
        self.play(FadeIn(f1, shift=RIGHT * 0.05), FadeIn(wm), run_time=0.6)
        self.at(self.cue("kapılı bir osiloskopla", 7.0))
        self.play(FadeIn(f2, shift=RIGHT * 0.05), FadeIn(osc), run_time=0.6)
        self.at(self.cue("yeni kuralı sınayın", 12.0))
        self.play(FadeIn(rt), FadeIn(idx), run_time=0.4)
        self.at(self.cue("önce yayın", 14.2))
        self.play(FadeIn(seq[0], shift=DOWN * 0.05), FadeIn(use[0]), run_time=0.4)
        self.at(self.cue("yeni sürümlü tek alıcılı", 16.5))
        self.play(GrowArrow(sar[0]), FadeIn(seq[1], shift=DOWN * 0.05), FadeIn(use[1]), use[0].animate.set_opacity(0.35), run_time=0.5)
        self.at(self.cue("sonra yine yayın", 20.0))
        self.play(GrowArrow(sar[1]), FadeIn(seq[2], shift=DOWN * 0.05), FadeIn(use[2]), use[1].animate.set_opacity(0.35), run_time=0.5)
        self.at(self.cue("en son geleni kullanmalıdır", 22.2))
        self.play(FadeIn(res, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # g12 — TEST 11: Reason Codes ≠ 0 (aware ONU logs, legacy ONU behaves as with 0); OMCI filter Port-ID = ONU-ID, 48-byte baseline, MIC
        self.beat("g12")
        self.clear(h)
        h = step_head(self, 11, "Neden kodları ve OMCI", h)
        ms = VGroup(VGroup(mtile(0x05, "Deactivate_ONU-ID", "dis", 3.0, 0.4, 15), tag("RC ≠ 0", GOLD, 15)).arrange(RIGHT, buff=0.15),
                    VGroup(mtile(0x06, "Disable_Serial_Number", "dis", 3.0, 0.4, 15), tag("RC ≠ 0", GOLD, 15)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ms.move_to([-3.6, 1.2, 0])
        o1 = VGroup(onu_box("haberdar ONU", ONUC, 2.1, 0.5, 15), T("→ değeri kaydeder", 16, GOOD, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        o2 = VGroup(onu_box("eski ONU", MUTED, 2.1, 0.5, 15), T("→ 0x0000'daki gibi davranır", 16, GOOD, BOLD), ok_x(True, 17)).arrange(RIGHT, buff=0.15)
        oo = VGroup(o1, o2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, 1.2, 0])
        fl = VGroup(T("süzgeç:", 17, MUTED, BOLD), HX("XGEM Port-ID = ONU-ID", 20, PIDC, BOLD)).arrange(RIGHT, buff=0.2).move_to([-3.4, -1.2, 0])
        p = apanel(5.4, 2.0, "OMCC · temel OMCI", OMC).move_to([3.4, -1.45, 0])
        rows = VGroup(kv("PLI", "48 → 56 B", kw=2.0), kv("MIC · OMCI_IK", "doğrula ✓", kw=2.0)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(p[0]).shift(DOWN * 0.18)
        fa = arrow(fl.get_right() + RIGHT * 0.1, p[0].get_left(), PIDC, 2, 0.1)
        self.play(self.set_src("G.989.3 Tablo 11-8 · Tablo 11-9 · §6.1.4.3 · §15.7 · yöntem: yorum"), run_time=0.2)
        self.at(self.cue("neden kodlu bir devre dışı", 4.0))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.05) for m in ms], lag_ratio=0.3), run_time=0.7)
        self.at(self.cue("haberdar ONU kaydetmeli", 9.4))
        self.play(FadeIn(o1, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("eski ONU sıfırdaki", 11.4))
        self.play(FadeIn(o2, shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("port kimliği ONU kimliğine", 15.0))
        self.play(FadeIn(fl, shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("kırk sekiz bayt olmalı", 19.7))
        self.play(GrowArrow(fa), FadeIn(p), FadeIn(rows[0], shift=RIGHT * 0.05), run_time=0.6)
        self.at(self.cue("kodları da doğrulanmalıdır", 23.4))
        self.play(FadeIn(rows[1], shift=RIGHT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        self.note11("g13", [("1", "Varsayılan anahtarla doğrulama: en ucuz, en güçlü test",
                             "her yayında çalıştırın · tek bir uyuşmazlık = uygulama hatası", "varsayılan anahtarla doğrulama"),
                            ("2", "Aktivasyon kaydı, anahtar demektir",
                             "kaydeden analizör o ağın anahtarlarını türetebilir\nbu kayıtları test ortamı dışında saklamayın", "aktivasyonu kaydeden")], badge="lab")
        self.save_timeline("ep15_labC")


class E15End(Act15):
    HDR, MANIFEST, FIRST = H15["E"], M15("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölümün özeti")
        self.at(self.cue("Bir:", 1.2))
        self.to_header(tc)
        self.set_badge("ozet")
        rows = VGroup()
        for i, (s, c) in enumerate(POINTS):
            n = T(f"{i + 1}", 30, ACC, BOLD)
            t = fit(T(s, 20, TXT, line_spacing=0.85), 9.4)
            ch = tag(c, GOLD, 16)
            rows.add(VGroup(n, t, ch))
        for r, y in zip(rows, np.linspace(1.85, -2.45, 5)):
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([5.65, y, 0])
        for k, (key, d) in enumerate((("sabit kırk sekiz", 2.0), ("sıra numaraları aşağı", 20.9))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.05)
        self.beat("h2")
        for k, (key, d) in zip((2, 3, 4), (("bütünlük kodu", 0.3), ("iki değişiklik dolguya", 11.8), ("ONU kimliğiyle aynı numaralı", 19.9))):
            self.at(self.cue(key, d))
            self.play(FadeIn(rows[k][:2], shift=RIGHT * 0.2), FadeIn(rows[k][2], shift=LEFT * 0.1), run_time=0.6)
        self.end(pad=0.15)

        self.beat("h3")
        self.clear()
        ttl = T("Kendini test et", 40, TXT, BOLD).move_to(UP * 2.3)
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.6, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("Yakalanan bir yayın\nChannel_Profile'ın MIC'i:\nhangi anahtar, hangi baytlar,\nkaç bit?", CH[0]),
            ("Boştaki ONU'ya N. çerçevede\nyönlendirilmiş mesaj: cevap\nen geç ne zaman, hangi SeqNo?\nİşlerken tahsis gelirse?", CH[1]),
            ("Zayıflatması sıfır olan\nbir ONU'ya “gücü artır”\nkomutu gelirse\nne olur?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: bir sonraki bölümün başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        for k, (key, d) in enumerate((("Birinci soru", 1.3), ("İkinci soru", 13.0), ("Üçüncü soru", 29.0))):
            self.at(self.cue(key, d))
            self.play(FadeIn(qs[k], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında", 37.2))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        # h4 — next episode: Uyanış (S2·B6): O1 → O5 with the named messages and timers
        self.beat("h4")
        self.clear()
        self.drop_badge()
        e6 = SERIES["season2"]["episodes"][5]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Sezon 2 · Bölüm {e6['n']} · {e6['title']}", 50, TXT, BOLD), T(e6["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        fit(nxt[1], 12.6)
        y = -1.45
        sts = VGroup(*[sbox(s, None, STATE, 1.35, 0.62, 20) for s in ("O1", "O2-3", "O4", "O5")]).arrange(RIGHT, buff=2.35).move_to([0, y, 0])
        ms_ = ["Serial_Number_ONU", "Assign_ONU-ID", "Ranging_Time"]
        tr_ = VGroup(*[VGroup(arrow(sts[i].get_right(), sts[i + 1].get_left(), GOLD, 2.2, 0.1), T(m, 14, GOLD, BOLD)) for i, m in enumerate(ms_)])
        for t in tr_:
            t[1].next_to(t[0], UP, buff=0.08)
            fit(t[1], 2.1)
        tm = tag("zamanlayıcılar · TO1 · TO2 …", MUTED, 15).next_to(sts, DOWN, buff=0.3)
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.2)
        self.at(self.cue("ONU aktivasyonu", 2.1))
        self.play(FadeIn(nxt[2]), run_time=0.5)
        self.at(self.cue("adlarını koyduğumuz seri numarası", 5.5))
        self.play(LaggedStart(*[FadeIn(s) for s in sts], lag_ratio=0.15), run_time=0.7)
        self.at(self.cue("kimlik atama ve eşitleme", 9.3))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(t[0]), FadeIn(t[1])) for t in tr_], lag_ratio=0.3), run_time=1.0)
        self.at(self.cue("zamanlayıcılarıyla birlikte", 16.2))
        self.play(FadeIn(tm, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.6)
        self.play(FadeOut(nxt), FadeOut(VGroup(sts, tr_, tm)), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T(f"LAMBDA · Sezon 2 · Bölüm {EP15['n']} · {EP15['title']}", 30, TXT, BOLD),
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
        self.save_timeline("ep15_end")
