"""S2·B9 · Perde 3 (sayaçlar — G.989.3 §14.1, Tablo 14-1, G.989.2 Ek II) and Perde 4 (kusurlar ve son nefes — §14.2.1–14.2.3,
Tablo 14-2 / 14-3, Tablo 13-1, Tablo 16-7, §8.1.2.1.2, Tablo 18-3, G.989.2 Tablo III.2 / Ek II / Ek D)."""
from ep19_common import *

PMH = ["sayaç", "M/O", "ONU", "OLT · ONU_i", "OLT · toplam"]
PMW = [5.0, 0.9, 2.3, 2.2, 2.2]


def pmtable(rows, row_h=0.42, size=16, hsize=15, widths=None):
    """Table 14-1 extract: Evet / Hayır / N/A coloured, M in the accent colour."""
    tb = mtable(PMH, rows, widths or PMW, size=size, hsize=hsize, row_h=row_h)
    for r in tb[1:]:
        r[2].set_color(MANC if r[2].text == "M" else MUTED)
        for c in r[3:]:
            t = c.text
            c.set_color(GOOD if t.startswith("Evet") else WARN if t.startswith("Hayır") else MUTED)
    return tb


def frames_bursts(n, x0, cw, y, marks, h=0.42, size=15):
    """Frame cells with one scheduled burst each; marks[k] in {'ok','miss','none'} → green burst, red ✗, nothing."""
    cells = VGroup()
    for k in range(n):
        r = Rectangle(width=cw, height=h, stroke_color=LINE, stroke_width=1.4, fill_color=PANEL, fill_opacity=1).move_to([x0 + cw * (k + 0.5), y, 0])
        m = marks[k] if k < len(marks) else "none"
        if m == "ok":
            g = Rectangle(width=cw * 0.45, height=h * 0.6, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(r)
        elif m == "miss":
            g = T("✗", size + 3, WARN, BOLD).move_to(r)
        else:
            g = VGroup()
        cells.add(VGroup(r, g))
    return cells


# ================================ PERDE 3 ======================================
class E19P3A(Act19):
    HDR, MANIFEST, FIRST = H19[3], M19("p3"), True

    def construct(self):
        # d1 — §14.1 scope: mechanisms to detect link failure and monitor link health; the functions that use the information (threshold alerts,
        #      alarms, …) largely out of scope; optical power monitoring → G.988; ONU counters reach the OLT via OMCI
        self.beat("d1")
        tc = self.title_card("PERDE 3", "Sayaçlar")
        h = self.heading("§14.1 — başarım izleme: kapsam")
        self.at(self.cue("On dördüncü madde", 1.5))
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        cin = frame_box("kapsamda", GOOD, 5.9, 2.0, 18).move_to([-3.25, 0.9, 0])
        ci = VGroup(*[ok_line(s, True, 17) for s in ("bağlantı arızasını saptama", "bağlantıların sağlığını izleme")]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ci.move_to(cin[0]).shift(DOWN * 0.15)
        cout = frame_box("büyük ölçüde kapsam dışı", WARN, 5.9, 2.0, 18).move_to([3.25, 0.9, 0])
        co = VGroup(*[ok_line(s, False, 16) for s in ("bilgiyi kullanan işlevler: istasyon yönetimi,\nbant tahsisi, provizyon", "eşik aşım uyarıları · alarmlar · koruma anahtarlama")])
        co.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fit(co, 5.4).move_to(cout[0]).shift(DOWN * 0.15)
        g988 = VGroup(T("optik güç izleme", 17, TXT, BOLD), T("→", 18, MUTED, BOLD), tag("G.988 (2022)", OMC, 16)).arrange(RIGHT, buff=0.15).move_to([-3.25, -1.55, 0])
        on = onu_box("ONU", ONUC, 1.2, 0.5, 16)
        oc = mbox("OMCI", OMC, 1.0, 0.4, 15)
        ol = ct_box("OLT CT", OLTC, 1.3, 0.5, 16)
        fl = VGroup(VGroup(on, T("sayaçlar", 14, ONUC, BOLD).next_to(on, DOWN, buff=0.06)), oc, ol).arrange(RIGHT, buff=0.7).move_to([3.25, -1.55, 0])
        fa = VGroup(arrow(on.get_right(), oc.get_left(), OMC, 2, 0.1), arrow(oc.get_right(), ol.get_left(), OMC, 2, 0.1))
        self.play(self.set_src("G.989.3 §14.1 · Tablo 14-1"), run_time=0.3)
        self.at(self.cue("bağlantı arızasını saptama", 3.0))
        self.play(FadeIn(cin), FadeIn(ci[0], shift=RIGHT * 0.05), run_time=0.45)
        self.play(FadeIn(ci[1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("bu bilgiyi kullanan", 10.3))
        self.play(FadeIn(cout), FadeIn(co[0], shift=RIGHT * 0.05), run_time=0.45)
        self.at(self.cue("eşik uyarılarını ve alarmları", 12.8))
        self.play(FadeIn(co[1], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("Optik güç izleme", 18.1))
        self.play(FadeIn(g988, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ONU'nun sayaçları OLT'ye", 21.4))
        self.play(FadeIn(fl[0]), GrowArrow(fa[0]), FadeIn(oc), GrowArrow(fa[1]), FadeIn(ol), run_time=0.6)
        self.end(pad=0.05)

        # d2 — Table 14-1 read in three columns (each ONU per TWDM channel · OLT CT per ONU · OLT CT aggregate); our count: 111 rows, 37 M, 74 O,
        #      11 groups; all TWDM — not a single PtP WDM counter
        self.beat("d2")
        h = self.reset("Tablo 14-1 — üç sütun, on bir grup", "std", 0.5)
        cols = VGroup(tag("ONU · her TWDM kanalı için", ONUC, 16), tag("OLT CT · her ONU_i için", OLTC, 16), tag("OLT CT · toplam", OLTC, 16)).arrange(RIGHT, buff=0.3)
        cols.move_to([0, 1.95, 0])
        gr = pm_grid(x_lab=-6.35, x0=-3.95, y0=1.3, dy=0.36, cw=0.24, gap=0.04, h=0.27, size=15)
        sm = VGroup(VGroup(pm_cell(True, 0.24, 0.27), T("37 zorunlu (M)", 17, MANC, BOLD)).arrange(RIGHT, buff=0.12),
                    VGroup(pm_cell(False, 0.24, 0.27), T("74 isteğe bağlı (O)", 17, MUTED, BOLD)).arrange(RIGHT, buff=0.12),
                    T("= 111 satır · 11 grup", 17, TXT, BOLD), ytag("bizim saymamız")).arrange(RIGHT, buff=0.35)
        fit(sm, 12.6).move_to([0, -2.85, 0])
        ptp = VGroup(T("hepsi TWDM ·", 17, TXT, BOLD), T("PtP WDM: 0 sayaç", 18, PTPC, BOLD)).arrange(RIGHT, buff=0.12).move_to([3.2, -1.95, 0])
        self.play(self.set_src("G.989.3 Tablo 14-1 (Amd.2 PDF s.147–158) · sayım: bizim"), run_time=0.3)
        self.at(self.cue("her ONU,", 2.0))
        self.play(FadeIn(cols[0], shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("her ONU için", 4.9))
        self.play(FadeIn(cols[1], shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("bütün ONU'ların toplamı", 6.6))
        self.play(FadeIn(cols[2], shift=DOWN * 0.05), run_time=0.3)
        self.at(self.cue("yüz on bir satır vardır", 10.0))
        self.play(LaggedStart(*[FadeIn(r[0]) for r in gr], lag_ratio=0.05), LaggedStart(*[FadeIn(r[1], shift=RIGHT * 0.05) for r in gr], lag_ratio=0.08),
                  LaggedStart(*[FadeIn(r[2]) for r in gr], lag_ratio=0.05), run_time=1.2)
        self.at(self.cue("otuz yedisi zorunlu", 12.6))
        self.play(FadeIn(sm[0], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("yetmiş dördü isteğe bağlı", 14.3))
        self.play(FadeIn(sm[1], shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("on bir grupta", 16.5))
        self.play(FadeIn(sm[2:], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("noktadan noktaya WDM için", 19.3))
        self.play(FadeIn(ptp, shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # d3 — PHY group: six mandatory rows (FEC corrected bytes / codewords, uncorrectable, total; BIP-32 protected words, BIP-32 errors), Note 1
        #      (BIP-32 gives a BER estimate only when FEC is off); three optional (PSBd HEC, FS header HEC, unknown profile)
        self.beat("d3")
        h = self.reset("Fiziksel katman grubu — 6 M · 3 O", "std", 0.5)
        rows = [["FEC ile düzeltilen baytlar", "M", "Evet · tüm akış", "Evet, ↑ FEC açıksa", "N/A"],
                ["FEC ile düzeltilen kod sözcükleri", "M", "Evet", "Evet, ↑ FEC açıksa", "N/A"],
                ["düzeltilemeyen kod sözcükleri", "M", "Evet", "Evet, ↑ FEC açıksa", "Evet"],
                ["toplam FEC kod sözcükleri", "M", "Evet", "Evet, ↑ FEC açıksa", "Evet"],
                ["BIP-32 korumalı sözcükler (4 B)", "M", "Evet", "Evet", "Evet"],
                ["BIP-32 hata sayısı · Not 1", "M", "Evet", "Evet", "Evet"],
                ["PSBd HEC hataları", "O", "Evet", "N/A", "N/A"],
                ["FS başlık HEC hataları", "O", "Evet", "Evet", "N/A"],
                ["bilinmeyen profil sayısı", "O", "Evet", "N/A", "N/A"]]
        tb = pmtable(rows, 0.41, 16, 15).move_to([0, 0.05, 0])
        n1 = VGroup(T("Not 1:", 16, GOLD, BOLD), T("BIP-32, yalnızca FEC kapalıyken hata oranı tahmini verir", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -2.6, 0])
        hl = SurroundingRectangle(tb[6], color=GOLD, buff=0.02, stroke_width=2)
        self.play(FadeIn(tb[0]), self.set_src("G.989.3 Tablo 14-1 · PHY PM · Not 1"), run_time=0.4)
        for idx, key, d in (((1,), "FEC ile düzeltilen baytlar", 3.8), ((2,), "düzeltilen,", 6.1), ((3, 4), "düzeltilemeyen ve toplam", 7.0),
                            ((5, 6), "BIP-32 ile korunan", 10.4)):
            self.at(self.cue(key, d))
            self.play(*[FadeIn(tb[i], shift=RIGHT * 0.05) for i in idx], run_time=0.35)
        self.at(self.cue("ancak FEC kapalıyken", 16.1))
        self.play(Create(hl), FadeIn(n1, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("İsteğe bağlı üçü", 19.9))
        self.play(FadeOut(hl), run_time=0.3)
        self.at(self.cue("PSBd ve çerçeve başlığı", 21.4))
        self.play(FadeIn(tb[7], shift=RIGHT * 0.05), FadeIn(tb[8], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("bilinmeyen profil", 24.5))
        self.play(FadeIn(tb[9], shift=RIGHT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # d4 — LODS group: seven rows, all mandatory, all ONU-local: total LODS events; restored in the operating / protection / discretionary channel;
        #      reactivations without DS (TO2, or TO3 + TO4); after US handshake failure (TO5) in the pre-configured / discretionary channel
        self.beat("d4")
        root = VGroup(sbox("LODS", "O5 → O6", LDC, 2.0, 0.85, 22, 15), tag("toplam olay", MANC, 15)).arrange(DOWN, buff=0.12).move_to([-4.9, 0.1, 0])
        loc = T("ONU'nun yerel olayı", 16, ONUC, BOLD).next_to(root, DOWN, buff=0.25)
        br = [("işletim kanalında geri geldi", "yeniden ayar yok", GOOD), ("koruma kanalında geri geldi", "WLCP açık", GOOD),
              ("ONU'nun seçtiği kanalda geri geldi", "WLCP kapalı", GOOD), ("↓ gelmeden yeniden aktivasyon", "TO2 · ya da TO3 + TO4", WARN),
              ("TO5 · ↑ el sıkışma başarısız", "önceden yapılandırılmış kanal", WARN),
              ("TO5 · ↑ el sıkışma başarısız", "seçilen kanal", WARN)]
        ys = [1.75, 1.1, 0.45, -0.45, -1.1, -1.75]
        leaves, links = VGroup(), VGroup()
        for (a, b, c), y in zip(br, ys):
            row = VGroup(pm_cell(True, 0.24, 0.3), T(a, 16, TXT, BOLD), T("· " + b, 15, c, BOLD)).arrange(RIGHT, buff=0.15)
            row.move_to([-1.7, y, 0], aligned_edge=LEFT)
            leaves.add(row)
            links.add(Line(root[0].get_right(), row.get_left() + LEFT * 0.08, color=c, stroke_width=1.6, stroke_opacity=0.7))
        rc = pm_cell(True, 0.24, 0.3).next_to(root[1], LEFT, buff=0.12)
        tmr = s2chip(6, 15).move_to([3.6, -2.55, 0])
        cnt = VGroup(T("7 satır · hepsi", 17, TXT, BOLD), T("M", 18, MANC, BOLD)).arrange(RIGHT, buff=0.12).move_to([-4.9, -2.55, 0])
        h = self.reset("Senkron kaybı grubu — 7 M · yalnızca ONU", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 14-1 · LODS PM · zamanlayıcılar: S2·B6")])
        self.at(self.cue("Senkron kaybı grubu yedi", 0.3))
        self.play(FadeIn(root[0], scale=0.95), run_time=0.4)
        self.at(self.cue("hepsi zorunlu", 2.9))
        self.play(FadeIn(cnt, shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("hepsi ONU'nun yerel olayı", 4.0))
        self.play(FadeIn(loc, shift=UP * 0.05), run_time=0.3)
        self.at(self.cue("toplam LODS olayları", 6.2))
        self.play(FadeIn(root[1]), FadeIn(rc), run_time=0.35)
        self.at(self.cue("çalışan kanalda", 8.0))
        self.play(Create(links[0]), FadeIn(leaves[0], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("koruma kanalında ya da", 9.3))
        self.play(*[Create(links[k]) for k in (1, 2)], *[FadeIn(leaves[k], shift=RIGHT * 0.05) for k in (1, 2)], run_time=0.45)
        self.at(self.cue("aşağı yön dönmeden TO2", 14.8))
        self.play(Create(links[3]), FadeIn(leaves[3], shift=RIGHT * 0.05), FadeIn(tmr), run_time=0.45)
        self.at(self.cue("TO5 ile yukarı yön", 21.2))
        self.play(*[Create(links[k]) for k in (4, 5)], *[FadeIn(leaves[k], shift=RIGHT * 0.05) for k in (4, 5)], run_time=0.45)
        self.end(pad=0.05)
        self.save_timeline("ep19_p3A")


class E19P3B(Act19):
    HDR, MANIFEST, PREV_BADGE = H19[3], M19("p3"), "std"

    def construct(self):
        # d5 — XGEM group: four mandatory (Tx and Rx XGEM frames, header HEC errors, key errors); oddity: "Received XGEM frames" is mandatory but only
        #      in the OLT aggregate — "No" in the ONU column; utilisation: two mandatory byte counters, one optional DBA counter
        self.beat("d5")
        h = self.heading19("XGEM ve kullanım grupları")
        rx = [["gönderilen XGEM çerçeveleri", "M", "Evet", "Hayır", "Evet"],
              ["alınan XGEM çerçeveleri", "M", "Hayır", "Hayır", "Evet"],
              ["XGEM başlık HEC hataları", "M", "Evet", "Evet", "Hayır"],
              ["XGEM anahtar hataları", "M", "Evet", "Evet", "N/A"]]
        ru = [["boş olmayan XGEM çerçevelerinde gönderilen baytlar", "M", "Evet", "Evet", "Evet"],
              ["boş olmayan XGEM çerçevelerinde alınan baytlar", "M", "Evet", "Evet", "Evet"],
              ["talep varken garantili bant atanamadı (DBA)", "O", "N/A", "Evet", "Evet"]]
        t1 = pmtable(rx, 0.42, 16, 15).move_to([0, 0.92, 0])
        t2 = pmtable(ru, 0.42, 16, 15).move_to([0, -1.68, 0])
        g1 = T("XGEM · 4 M (+4 O)", 15, MANC, BOLD).next_to(t1, UP, buff=0.08).align_to(t1, LEFT)
        g2 = T("kullanım · 2 M · 1 O", 15, MANC, BOLD).next_to(t2, UP, buff=0.08).align_to(t2, LEFT)
        odd = SurroundingRectangle(t1[2], color=WARN, buff=0.02, stroke_width=2.2)
        oddc = VGroup(SurroundingRectangle(t1[2][3], color=WARN, buff=0.04, stroke_width=2.6), SurroundingRectangle(t1[2][5], color=GOOD, buff=0.04, stroke_width=2.6))
        oddl = T("bir tuhaflık: zorunlu, ama yalnızca OLT toplamında", 15, WARN, BOLD).next_to(t1, DOWN, buff=0.1).align_to(t1, RIGHT)
        self.at(self.cue("XGEM grubunun dört zorunlu", 0.3))
        self.play(FadeIn(g1), FadeIn(t1[0]), self.set_src("G.989.3 Tablo 14-1 · XGEM PM · UTILIZATION PM"), run_time=0.35)
        self.at(self.cue("gönderilen ve alınan", 2.9))
        self.play(FadeIn(t1[1], shift=RIGHT * 0.05), FadeIn(t1[2], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("başlık HEC hataları ve anahtar", 6.0))
        self.play(FadeIn(t1[3], shift=RIGHT * 0.05), FadeIn(t1[4], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("alınan çerçeve sayacı zorunludur", 10.5))
        self.play(Create(odd), run_time=0.4)
        self.at(self.cue("yalnızca OLT toplamında", 13.3))
        self.play(Create(oddc[1]), FadeIn(oddl, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ONU sütununda hayır", 15.6))
        self.play(Create(oddc[0]), run_time=0.35)
        self.at(self.cue("Kullanım grubunun iki zorunlu", 17.8))
        self.play(FadeIn(g2), FadeIn(t2[0]), FadeIn(t2[1], shift=RIGHT * 0.05), FadeIn(t2[2], shift=RIGHT * 0.05), run_time=0.5)
        self.at(self.cue("garantili bant genişliğinin", 25.9))
        self.play(FadeIn(t2[3], shift=RIGHT * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # d6 — PLOAM group: 34 rows, only four mandatory (Ranging_Time count — base for drift estimation; Protection_Control count; Adjust_Tx_Wavelength
        #      count and amplitude); the rest optional per message, incl. Sleep_Allow, Sleep_Request, Power_Consumption_Report; no counter for the
        #      inquiry and the rate messages
        self.beat("d6")
        cw, gp, x0, y0 = 0.3, 0.05, -5.95, 1.85
        cells = VGroup(*[pm_cell(k < 4, cw, 0.36).move_to([x0 + (cw + gp) * k + cw / 2, y0, 0]) for k in range(34)])
        cl = T("34", 16, MUTED, BOLD).next_to(cells, RIGHT, buff=0.15)
        ml = [("Ranging_Time sayısı", "kayma tahmininin temeli"), ("Protection_Control sayısı", ""), ("Adjust_Tx_Wavelength sayısı", "dalga boyu kayma tahmini"),
              ("Adjust_Tx_Wavelength genliği", "mutlak değer tahmincisi")]
        lab = VGroup()
        for k, (a, b) in enumerate(ml):
            g = VGroup(T(a, 16, MANC, BOLD), T(b, 15, MUTED, BOLD) if b else VGroup()).arrange(RIGHT, buff=0.15)
            g.move_to([-4.3, 1.05 - 0.48 * (3 - k), 0], aligned_edge=LEFT)
            ln = VGroup(Line(cells[k].get_bottom(), [cells[k].get_x(), g.get_y(), 0], color=MANC, stroke_width=1.4),
                        Line([cells[k].get_x(), g.get_y(), 0], g.get_left() + LEFT * 0.06, color=MANC, stroke_width=1.4))
            lab.add(VGroup(ln, g))
        op = VGroup(T("isteğe bağlı sayaç var:", 16, MUTED, BOLD),
                    *[mtile(c, n, f, 3.9, 0.4, 15) for c, n, f in ((0x12, "Sleep_Allow ↓", "pm"), (0x10, "Sleep_Request ↑", "pm"), (0x1B, "Power_Consumption_Report ↑", "pm"))])
        op.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.55, -2.1, 0])
        no = VGroup(T("sayaç yok:", 16, WARN, BOLD),
                    *[mtile(c, n, f, 3.9, 0.4, 15) for c, n, f in ((0x1B, "Power_Consumption_Inquire ↓", "pm"), (0x1C, "Rate_Control ↓", "rate"), (0x1C, "Rate_Response ↑", "rate"))])
        no.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, -2.1, 0])
        nx = VGroup(*[T("✗", 20, WARN, BOLD).next_to(t, RIGHT, buff=0.12) for t in no[1:]])
        h = self.reset("PLOAM grubu — 34 satır · 4 M", "std", 0.5, extra=[self.src_in("G.989.3 Tablo 14-1 · PLOAM PM")])
        self.at(self.cue("PLOAM grubu otuz dört", 0.3))
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), FadeIn(cl), run_time=0.8)
        self.at(self.cue("eşitleme gecikmesi mesajlarının", 4.5))
        self.play(FadeIn(lab[0]), run_time=0.4)
        self.at(self.cue("koruma denetimi", 9.8))
        self.play(FadeIn(lab[1]), run_time=0.35)
        self.at(self.cue("dalga boyu ayarı", 12.9))
        self.play(FadeIn(lab[2]), FadeIn(lab[3]), run_time=0.4)
        self.at(self.cue("Geri kalanı mesaj başına", 16.9))
        self.play(FadeIn(op[0]), run_time=0.3)
        self.at(self.cue("uyku izni,", 20.4))
        self.play(FadeIn(op[1], shift=RIGHT * 0.05), run_time=0.3)
        self.at(self.cue("uyku isteği ve güç", 21.2))
        self.play(FadeIn(op[2:], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("Güç sorgusu ve hız", 24.6))
        self.play(FadeIn(no[0]), FadeIn(no[1:], shift=RIGHT * 0.05), FadeIn(nx), run_time=0.5)
        self.end(pad=0.05)

        # d7 — tuning control: 34 rows, 13 mandatory; activation, power levelling, OMCI: all optional; the only mandatory optical row = OLT transmit optical
        #      power level; the only power-management row is optional (time in low-power states); nothing counts forced wake-ups or handshake violations
        self.beat("d7")
        idx = [6, 5, 7, 8, 9, 10]
        full = pm_grid(x_lab=-6.35, x0=-3.6, y0=1.85, dy=0.4, cw=0.24, gap=0.035, h=0.3, size=15)
        rows = VGroup(*[full[i] for i in idx])
        for k, r in enumerate(rows):
            r.set_y(1.85 - 0.4 * k)
        mon = VGroup(T("zorunlu tek optik satır:", 16, MANC, BOLD), T("OLT'nin gönderdiği optik güç düzeyi", 17, TXT, BOLD),
                     T("OLT toplam · S/R-CP, S/R-CG ya da S'/R'", 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        mon.move_to([-3.2, -1.25, 0])
        ene = VGroup(T("güç yönetimine ait tek satır · O:", 16, MUTED, BOLD), T("düşük güç durumlarında geçen süre", 17, TXT, BOLD),
                     T("ONU ✓ · OLT/ONU_i ✓", 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        ene.move_to([3.2, -1.25, 0])
        nono = VGroup(T("satır yok:", 16, WARN, BOLD), *[VGroup(T(s, 16, TXT, BOLD), T("✗", 18, WARN, BOLD)).arrange(RIGHT, buff=0.08)
                                                        for s in ("zorunlu uyandırma (FWI)", "el sıkışma ihlali (Ter_i)", "uyarı zaman aşımı (Talerted)")]).arrange(RIGHT, buff=0.35)
        fit(nono, 12.6).move_to([0, -2.65, 0])
        h = self.reset("Kalan gruplar — ve iki tek satır", "std", 0.5,
                       extra=[self.src_in("G.989.3 Tablo 14-1 · Tuning control PM · Power monitoring · Energy conservation")])
        self.at(self.cue("Ayar denetimi grubu da", 0.3))
        self.play(FadeIn(rows[0]), run_time=0.45)
        self.at(self.cue("on üçü zorunlu", 3.5))
        self.play(Indicate(VGroup(*rows[0][1][:13]), color=MANC, scale_factor=1.04), run_time=0.45)
        self.at(self.cue("aktivasyon,", 4.8))
        self.play(FadeIn(rows[1]), run_time=0.3)
        self.at(self.cue("güç dengeleme ve OMCI", 5.7))
        self.play(FadeIn(rows[2]), FadeIn(rows[3]), run_time=0.35)
        self.at(self.cue("Zorunlu tek optik satır", 10.7))
        self.play(FadeIn(rows[4]), run_time=0.3)
        self.at(self.cue("OLT'nin gönderdiği optik güç", 12.7))
        self.play(FadeIn(mon, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Güç yönetimine ait tek satır", 15.9))
        self.play(FadeIn(rows[5]), FadeIn(ene[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("düşük güç durumlarında geçen", 20.1))
        self.play(FadeIn(ene[1:], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("zorunlu uyandırmaları ya da", 24.9))
        self.play(FadeIn(nono, shift=UP * 0.05), run_time=0.45)
        self.end(pad=0.05)

        # d8 — PMD Köprüsü (S1·B10): G.989.2 Appendix II monitoring table: ONU received-power accuracy ±3 dB (±5 dB below −35 dBm), OLT transmit
        #      power ±2 dB; G.989.3 leaves measurement to G.988 and accuracy to an informative appendix. Our reading: even the one mandatory optical
        #      counter carries a 2 dB uncertainty
        self.beat("d8")
        h, chp = self.pmd_reset2("PMD Köprüsü — izleme doğruluğu", [s1chip(10)])
        ax, X = lin_axis(-6, 6, -2.6, 4.6, -0.95, [-6, -4, -2, 0, 2, 4, 6], size=14, fmt=lambda v: ("+" if v > 0 else "") + tr(v))
        axl = T("dB · hata", 14, MUTED, BOLD).next_to(ax, RIGHT, buff=0.15).shift(UP * 0.12)
        rr = [("ONU alınan güç", "≥ −35 dBm", 3, ONUC, 1.2), ("ONU alınan güç", "< −35 dBm", 5, ONUC, 0.55), ("OLT gönderilen güç", "Tablo 14-1 · M", 2, MANC, -0.1)]
        bars = VGroup()
        for name, sub, e, c, y in rr:
            r = Rectangle(width=X(e) - X(-e), height=0.36, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.3).move_to([X(0), y, 0])
            lb = VGroup(T(name, 16, TXT, BOLD), T(sub, 14, c, BOLD)).arrange(RIGHT, buff=0.12).next_to(r, LEFT, buff=0.2)
            v = T(f"±{e} dB", 16, c, BOLD).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(r, lb, v))
        for b in bars:
            if b[1].get_left()[0] < -6.9:
                b[1].shift(RIGHT * (-6.9 - b[1].get_left()[0]))
        src = VGroup(T("G.989.2 Ek II · Tablo II.1", 15, MUTED, BOLD), tag("bilgilendirici", MUTED, 14)).arrange(RIGHT, buff=0.15).move_to([0, 1.85, 0])
        g9 = VGroup(T("G.989.3:", 16, GOLD, BOLD), T("ölçüm → G.988 · doğruluk → bilgilendirici ek", 16, TXT, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -1.85, 0])
        ip = VGroup(ytag("bizim yorumumuz"), T("zorunlu tek optik sayaç bile ±2 dB belirsizlik taşır", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.55, 0])
        self.play(self.set_src("G.989.2 Ek II Tablo II.1 · G.989.3 §14.1 · Tablo 14-1"), run_time=0.3)
        self.at(self.cue("ikinci ekindeki izleme tablosunu", 2.5))
        self.play(FadeIn(src), Create(ax), FadeIn(axl), run_time=0.5)
        self.at(self.cue("ONU'nun alınan güç doğruluğu", 8.1))
        self.play(GrowFromCenter(bars[0][0]), FadeIn(bars[0][1:]), run_time=0.45)
        self.at(self.cue("eksi otuz beş dBm'in altında", 12.3))
        self.play(GrowFromCenter(bars[1][0]), FadeIn(bars[1][1:]), run_time=0.45)
        self.at(self.cue("OLT'nin gönderdiği güç", 15.1))
        self.play(GrowFromCenter(bars[2][0]), FadeIn(bars[2][1:]), run_time=0.45)
        self.at(self.cue("G.989.3 ölçümü G.988'e", 18.8))
        self.play(FadeIn(g9, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("iki desibellik bir belirsizlik", 25.5))
        self.play(FadeIn(ip, shift=UP * 0.05), Indicate(bars[2][0], color=MANC, scale_factor=1.05), run_time=0.5)
        self.end(pad=0.05)
        self.save_timeline("ep19_p3B")


class E19P3C(Act19):
    HDR, MANIFEST, PREV_BADGE = H19[3], M19("p3"), "pmd"

    def construct(self):
        # d9 — widths and accumulation intervals are not in G.989.3; our numbers at 10G: 5 016 000 FEC codewords/s → 32-bit wrap in 14.3 min; BIP-32
        #      words (FEC off) 13.8 s; non-idle XGEM bytes ≈ 4 s; a 64-bit codeword counter ≈ 1.2 × 10^5 years
        self.beat("d9")
        h = self.reset("Taşma süreleri — 10G ↓", "neden", 0.5)
        tg = self.chips_at([tag("genişlik · aralık: G.989.3'te yok", WARN, 15), ytag("bizim hesabımız")], h)
        x0, x1, ya = -6.0, 6.2, -1.75
        ax, X = log_ax(1, 1e13, x0, x1, ya, [(1, "1 s"), (60, "1 dk"), (3600, "1 sa"), (86400, "1 gün"), (3.156e7, "1 yıl"), (3.156e12, "10⁵ yıl")], 14)
        ys = [1.8, 1.25, 0.7, 0.15, -0.75, -1.3]

        def row(y, v, label, val, color):
            r = Rectangle(width=max(X(v) - x0, 0.05), height=0.26, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.45)
            r.move_to([x0 + (X(v) - x0) / 2, y, 0])
            t = T(label, 15, TXT, BOLD).next_to(r, RIGHT, buff=0.15)
            vv = T(val, 16, color, BOLD).next_to(t, RIGHT, buff=0.15)
            return VGroup(r, t, vv)
        rt = VGroup(T("5 016 000 FEC kod sözcüğü / s", 17, GOLD, BOLD), T("(627 / çerçeve)", 15, MUTED, BOLD)).arrange(RIGHT, buff=0.15)
        r_x = row(ys[0], 3.96, "boş olmayan XGEM baytları · 32 bit", "≈ 4 s", WARN)
        r_b = row(ys[1], 13.8, "BIP-32 sözcükleri · FEC kapalı · 32 bit", "13,8 s", WARN)
        r_f = row(ys[2], 856, "FEC kod sözcükleri · 32 bit", "856 s = 14,3 dk", GOLD)
        r_6 = row(ys[3], 3.79e12, "", "", GOOD)
        r_6.remove(r_6[1], r_6[2])
        r_6[0].set_fill(opacity=0.2)
        r_6l = VGroup(T("FEC kod sözcükleri · 64 bit", 15, TXT, BOLD), T("≈ 1,2 × 10⁵ yıl", 16, GOOD, BOLD)).arrange(RIGHT, buff=0.15)
        r_6l.move_to([x0 + 0.2, ys[3], 0], aligned_edge=LEFT).shift(RIGHT * 1.0)
        rt.move_to([3.0, ys[1] + 0.05, 0])
        self.play(Create(ax), FadeIn(tg, shift=LEFT * 0.05), self.set_src("bizim hesabımız · S2·B2 çerçeve sayıları · Tablo 14-1"), run_time=0.6)
        self.at(self.cue("saniyede beş milyon", 7.5))
        self.play(FadeIn(rt, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("on dört dakikada taşar", 13.5))
        self.play(GrowFromEdge(r_f[0], LEFT), FadeIn(r_f[1:]), run_time=0.5)
        self.at(self.cue("BIP-32 sözcükleri FEC kapalıyken", 16.4))
        self.play(GrowFromEdge(r_b[0], LEFT), FadeIn(r_b[1:]), run_time=0.45)
        self.at(self.cue("yaklaşık dört saniyede", 23.5))
        self.play(GrowFromEdge(r_x[0], LEFT), FadeIn(r_x[1:]), run_time=0.45)
        self.at(self.cue("Altmış dört bitlik", 26.0))
        self.play(GrowFromEdge(r_6[0], LEFT), FadeIn(r_6l, shift=UP * 0.05), run_time=0.7)
        self.end(pad=0.05)

        # d10 — error counters are slow: at BER 10^-12 a 10G line collects 10 bit errors only after 1005 s, at 10^-10 after 10 s; counters that wrap in
        #       seconds and counters that stay zero for hours sit side by side — choose the read interval per counter
        self.beat("d10")
        e12 = row(ys[4], 1005, "10 bit hatası · BER 10⁻¹²", "1005 s", ACC)
        e10 = row(ys[5], 10, "10 bit hatası · BER 10⁻¹⁰", "10 s", ACC)
        e10[1].next_to(e12[0], RIGHT, buff=0.15).set_y(ys[5])
        e10[2].next_to(e10[1], RIGHT, buff=0.15)
        el = T("hata sayaçları: biriktirme süresi", 15, ACC, BOLD).move_to([x0, ys[4] + 0.33, 0], aligned_edge=LEFT)
        sep = DashedLine([x0, ys[4] + 0.52, 0], [x1, ys[4] + 0.52, 0], color=LINE, stroke_width=1.4)
        rd = VGroup(T("okuma aralığı:", 17, TXT, BOLD), T("her sayaç için ayrı", 18, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -2.65, 0])
        self.at(self.cue("Hata sayaçları ise yavaştır", 0.3))
        self.play(Create(sep), FadeIn(el), run_time=0.4)
        self.at(self.cue("On üzeri eksi on ikilik", 2.3))
        self.play(GrowFromEdge(e12[0], LEFT), FadeIn(e12[1]), run_time=0.45)
        self.at(self.cue("bin beş saniyede", 7.3))
        self.play(FadeIn(e12[2], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("on üzeri eksi onda", 11.5))
        self.play(GrowFromEdge(e10[0], LEFT), FadeIn(e10[1:]), run_time=0.45)
        self.at(self.cue("saatlerce sıfır kalan", 17.0))
        self.play(Indicate(VGroup(r_x, r_b), color=WARN, scale_factor=1.03), Indicate(VGroup(e12, e10), color=ACC, scale_factor=1.03), run_time=0.8)
        self.at(self.cue("okuma aralığını her biri", 21.8))
        self.play(FadeIn(rd, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        self.note11("d11", [("1", "Test planınızı 37 zorunlu satıra dayandırın",
                             "Enerji sayacı (düşük güçte geçen süre) da, son nefes sayacı da isteğe bağlıdır.", "test planınızı"),
                            ("2", "Sayaç adlarını metinden değil, tablodan alın",
                             "§17.3.3 bir 'LOPCi sayacının artırılmasından' söz eder; Tablo 14-1'de böyle bir sayaç yoktur.", "İki:")])
        self.bridge_beat("d12", "Sayılar bir eğilim söyler.\nPeki bir şey bozulduğunda, standart neyi kusur sayar?")
        self.save_timeline("ep19_p3C")


# ================================ PERDE 4 ======================================
DEF9 = [("LOBi", "burst kaybı"), ("LOS", "sinyal kaybı"), ("TIWi", "iletim girişimi"), ("SUFi", "başlatma"), ("DFi", "devre dışı bırakma"),
        ("LOPCi", "PLOAM kanalı"), ("LOOCi", "OMCC kanalı"), ("DOTXi", "dalga boyu kayması"), ("ALRFi", "zayıflatma isteği")]


class E19P4A(Act19):
    HDR, MANIFEST, FIRST = H19[4], M19("p4"), True

    def construct(self):
        # e1 — §14.2 purpose: separate mandatory TC-layer actions from those left to the implementer; nine OLT defects, one ONU defect (LODS, S2·B2);
        #      most OLT actions are discretionary: extra soak time, changing the allocation schedule, disabling the ONU, rogue ONU diagnostics
        self.beat("e1")
        tc = self.title_card("PERDE 4", "Kusurlar ve son nefes")
        h = self.heading("§14.2 — kusurlar")
        self.at(self.cue("Madde amacını", 1.7))
        self.to_header_badge(tc, "std", 0.7, [FadeIn(h, shift=RIGHT * 0.2)])
        sp = VGroup(tag("TC katmanında zorunlu eylemler", GOLD, 17), T("|", 20, MUTED, BOLD), tag("uygulayıcıya kalanlar", MUTED, 17)).arrange(RIGHT, buff=0.3).move_to([0, 1.9, 0])
        tiles = VGroup(*[sbox(a, b, DEFC, 2.3, 0.72, 18, 14) for a, b in DEF9])
        VGroup(VGroup(*tiles[:5]).arrange(RIGHT, buff=0.15), VGroup(*tiles[5:]).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.18)
        fit(tiles, 12.4).move_to([0, 0.5, 0])
        tl = T("OLT CT · Tablo 14-2 · 9", 16, OLTC, BOLD).next_to(tiles, UP, buff=0.12).align_to(tiles, LEFT)
        onu = VGroup(T("ONU · Tablo 14-3 · 1:", 16, ONUC, BOLD), sbox("LODS", "↓ senkron kaybı", LDC, 2.3, 0.72, 18, 14), s2chip(2, 15)).arrange(RIGHT, buff=0.25)
        onu.next_to(tiles, DOWN, buff=0.3).align_to(tiles, RIGHT)
        acts = VGroup(T("takdir:", 16, MUTED, BOLD), *[tag(s, MUTED, 15) for s in ("ek bekleme süresi", "tahsis planını değiştirmek", "ONU'yu devre dışı bırakmak", "başıboş ONU tanılaması")])
        acts.arrange(RIGHT, buff=0.15)
        fit(acts, 12.6).move_to([0, -2.6, 0])
        self.play(self.set_src("G.989.3 §14.2 · Tablo 14-2 · Tablo 14-3"), run_time=0.3)
        self.at(self.cue("TC katmanında zorunlu", 4.0))
        self.play(FadeIn(sp[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("uygulayıcıya kalanlardan", 6.7))
        self.play(FadeIn(sp[1:], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("OLT'nin dokuz kusuru", 9.5))
        self.play(FadeIn(tl), LaggedStart(*[FadeIn(t, shift=UP * 0.05) for t in tiles], lag_ratio=0.08), run_time=0.8)
        self.at(self.cue("ONU'nun tek kusuru", 11.3))
        self.play(FadeIn(onu[:2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("ikinci bölümde gördüğümüz", 13.5))
        self.play(FadeIn(onu[2], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("eylemlerin çoğu takdire", 16.1))
        self.play(FadeIn(acts[0]), run_time=0.3)
        for k, (key, d) in enumerate((("ek bekleme süresi", 20.1), ("tahsis planını değiştirmek", 21.6), ("ONU'yu devre dışı", 23.9), ("başıboş ONU tanılaması", 26.2))):
            self.at(self.cue(key, d))
            self.play(FadeIn(acts[k + 1], shift=UP * 0.05), run_time=0.3)
        self.end(pad=0.05)

        # e2 — LOBi: failure to delineate Clob_i consecutive scheduled bursts of ONU_i when not exempt by the power-management machine; threshold
        #      configurable, default 4; for power saving the OLT sets it to the tolerated number; one successful burst clears; report qualified by DG
        self.beat("e2")
        h = self.reset("LOBi — burst kaybı", "std", 0.5)
        n, cw, x0, y = 12, 0.85, -5.3, 1.1
        marks = ["ok", "ok", "ok", "miss", "miss", "miss", "miss", "none", "none", "ok", "none", "none"]
        fr = frames_bursts(n, x0, cw, y, marks)
        fl = T("ONU_i · planlı burst'ler", 15, ONUC, BOLD).next_to(fr, UP, buff=0.12).align_to(fr, LEFT)
        cnt = VGroup(*[T(str(k + 1), 16, WARN, BOLD).next_to(fr[3 + k], DOWN, buff=0.1) for k in range(4)])
        lob = VGroup(Rectangle(width=cw * 2, height=0.42, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.25), T("LOBi", 17, WARN, BOLD))
        lob[1].move_to(lob[0])
        lob.move_to([(fr[7][0].get_x() + fr[8][0].get_x()) / 2, y, 0])
        clr = VGroup(T("tek başarılı burst → temizlenir", 15, GOOD, BOLD)).next_to(fr[9], DOWN, buff=0.12)
        dec = T("4. kaçırmada ilan", 15, WARN, BOLD).next_to(cnt[3], DOWN, buff=0.08)
        r1 = VGroup(T("Clob_i:", 17, TXT, BOLD), T("yapılandırılabilir · varsayılan 4", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        r2 = VGroup(T("güç tasarrufunda:", 17, TXT, BOLD), T("OLT, tolere edilen kayıp sayısına göre ayrıca kurar", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        r3 = VGroup(T("koşul:", 17, TXT, BOLD), T("güç yönetimi makinesi muaf tutmuyorsa", 17, SRW, BOLD)).arrange(RIGHT, buff=0.15)
        r4 = VGroup(T("rapor:", 17, TXT, BOLD), T("alınan son nefes (DG) bildirimleriyle nitelenmeli", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15)
        rr = VGroup(r3, r1, r2, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, -1.1, 0]).align_to([-5.3, 0, 0], LEFT)
        self.play(FadeIn(fl), *[FadeIn(c[0]) for c in fr], self.set_src("G.989.3 Tablo 14-2 · LOBi"), run_time=0.5)
        self.at(self.cue("bir ONU'nun planlanmış", 1.7))
        self.play(LaggedStart(*[FadeIn(fr[k][1]) for k in range(3)], lag_ratio=0.2), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(fr[3 + k][1], scale=1.3), FadeIn(cnt[k])) for k in range(4)], lag_ratio=0.35), run_time=1.0)
        self.play(FadeIn(lob, scale=0.9), FadeIn(dec), run_time=0.35)
        self.at(self.cue("güç yönetimi makinesi onu", 7.8))
        self.play(FadeIn(r3, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Eşik yapılandırılabilir", 11.6))
        self.play(FadeIn(r1[0]), run_time=0.3)
        self.at(self.cue("varsayılanı dörttür", 13.6))
        self.play(FadeIn(r1[1], shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("tolere edilen kayıp sayısına", 15.3))
        self.play(FadeIn(r2, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Tek bir başarılı burst", 21.7))
        self.play(FadeIn(fr[9][1], scale=1.3), FadeIn(clr), lob.animate.set_opacity(0.3), run_time=0.45)
        self.at(self.cue("son nefes bildirimleriyle", 25.2))
        self.play(FadeIn(r4, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # e3 — LOS: the OLT receives no expected upstream transmission for four consecutive frames; one transmission clears. Our calculation: with one
        #      burst per frame both LOS and LOBi = 500 µs; Type B SLOS is 0.5 ms too; but LOBi counts bursts: one burst per 16 frames → 8 ms
        self.beat("e3")
        h = self.reset("LOS ve LOBi — aynı 500 µs?", "std", 0.5)
        ax, X = frame_axis(8, -5.2, 1.2, 1.15, labels=True, size=14)
        fl = T("çerçeve (125 µs)", 14, MUTED, BOLD).next_to(ax, RIGHT, buff=0.15)
        allx = VGroup(*[T("✗", 18, WARN, BOLD).move_to([(X(k) + X(k + 1)) / 2, 1.55, 0]) for k in range(4)])
        alll = T("hiçbir ONU'dan ↑ iletim yok", 15, WARN, BOLD).next_to(allx, UP, buff=0.08)
        los = VGroup(Line([X(4), 1.0, 0], [X(4), 1.9, 0], color=WARN, stroke_width=3), T("LOS", 18, WARN, BOLD))
        los[1].next_to(los[0], RIGHT, buff=0.1).shift(UP * 0.3)
        one = VGroup(Rectangle(width=0.3, height=0.3, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to([(X(6) + X(7)) / 2, 1.55, 0]),
                     T("tek iletim → temizlenir", 15, GOOD, BOLD))
        one[1].next_to(one[0], RIGHT, buff=0.15)
        cmp = VGroup(VGroup(T("LOS", 17, WARN, BOLD), T("= 4 çerçeve = 500 µs", 17, TXT, BOLD)).arrange(RIGHT, buff=0.12),
                     VGroup(T("LOBi", 17, WARN, BOLD), T("= 4 burst · 1 burst/çerçeve → 500 µs", 17, TXT, BOLD)).arrange(RIGHT, buff=0.12),
                     VGroup(T("Tip B SLOS", 17, GOLD, BOLD), T("= 0,5 ms sessizlik · Tablo 18-3", 17, TXT, BOLD)).arrange(RIGHT, buff=0.12))
        cmp.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-3.2, -0.55, 0])
        cy = ytag("bizim hesabımız").next_to(cmp, UP, buff=0.12).align_to(cmp, LEFT)
        bx0, by0, bh = 1.6, -2.75, 0.3
        gp = [(1, 0.5), (2, 1), (4, 2), (8, 4), (16, 8)]
        sc = 0.55
        bars = VGroup()
        for k, (g, ms) in enumerate(gp):
            yy = by0 + (len(gp) - 1 - k) * 0.42
            r = Rectangle(width=ms * sc, height=bh, stroke_color=WARN, stroke_width=1.5, fill_color=WARN, fill_opacity=0.4).move_to([bx0 + ms * sc / 2, yy, 0])
            l = T(f"1/{g}", 15, TXT, BOLD).next_to([bx0, yy, 0], LEFT, buff=0.12)
            v = T(f"{tr(ms)} ms", 15, WARN, BOLD).next_to(r, RIGHT, buff=0.1)
            bars.add(VGroup(r, l, v))
        bt = VGroup(T("LOBi süresi · burst / çerçeve", 15, TXT, BOLD), ytag("bizim hesabımız", size=14)).arrange(RIGHT, buff=0.15).next_to(bars, UP, buff=0.12).align_to(bars, LEFT)
        losl = VGroup(DashedLine([bx0 + 0.5 * sc, by0 - 0.25, 0], [bx0 + 0.5 * sc, by0 + 4 * 0.42 + 0.25, 0], color=GOLD, stroke_width=1.8),
                      T("LOS: hep 0,5 ms", 14, GOLD, BOLD))
        losl[1].next_to(losl[0], DOWN, buff=0.04)
        self.play(Create(ax), FadeIn(fl), self.set_src("G.989.3 Tablo 14-2 · Tablo 18-3 · hesap: bizim"), run_time=0.5)
        self.at(self.cue("yukarı yönde beklediği hiçbir", 2.9))
        self.play(LaggedStart(*[FadeIn(x, scale=1.3) for x in allx], lag_ratio=0.25), FadeIn(alll), run_time=0.8)
        self.play(Create(los[0]), FadeIn(los[1]), run_time=0.35)
        self.at(self.cue("Tek bir iletim temizler", 8.6))
        self.play(FadeIn(one, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Bizim hesabımızla,", 10.6))
        self.play(FadeIn(cy), run_time=0.3)
        self.at(self.cue("çerçeve başına bir burst'le", 12.1))
        self.play(FadeIn(cmp[0], shift=UP * 0.05), FadeIn(cmp[1], shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("B tipi korumanın sessizlik", 18.4))
        self.play(FadeIn(cmp[2], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Ama burst kaybı burst sayar", 23.2))
        self.play(FadeIn(bt), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], LEFT), FadeIn(b[1:])) for b in bars], lag_ratio=0.15), Create(losl[0]), FadeIn(losl[1]), run_time=1.0)
        self.at(self.cue("sekiz milisaniyedir", 29.0))
        self.play(Indicate(bars[4], color=WARN, scale_factor=1.05), run_time=0.5)
        self.end(pad=0.05)

        # e4 — TIWi: drift beyond the outer (TIW) threshold that stays out after three Ranging_Time corrections; cleared below the inner (DOW) threshold;
        #      suggested outer threshold ≈ ±6.4 ns. PMD Köprüsü (S1·B6): that is only 3 % of the 205.8 ns worst-case guard time
        self.beat("e4")
        h = self.reset("TIWi — iletim girişimi uyarısı", "std", 0.5)
        ax0, ax1, yc, sy = -5.4, 2.6, 0.2, 0.021
        Yd = lambda b: yc + b * sy
        axes = VGroup(Line([ax0, Yd(-80), 0], [ax0, Yd(80), 0], color=MUTED, stroke_width=2), Line([ax0, yc, 0], [ax1, yc, 0], color=LINE, stroke_width=1.4))
        axl = T("kayma · bit (10G)", 14, MUTED, BOLD).next_to(axes[0], UP, buff=0.06)
        thr = VGroup()
        for v, c, s in ((64, WARN, "TIW ±64"), (32, GOLD, "DOW ±32")):
            for sg in (1, -1):
                thr.add(DashedLine([ax0, Yd(sg * v), 0], [ax1, Yd(sg * v), 0], color=c, stroke_width=1.6, dash_length=0.08))
            thr.add(T(s, 14, c, BOLD).next_to([ax0, Yd(v), 0], LEFT, buff=0.08))
        ts = np.linspace(0, 1, 40)
        dpts = []
        for t in ts:
            xx = ax0 + 0.2 + t * (ax1 - ax0 - 0.4)
            if t < 0.55:
                b = 10 + 110 * t
            elif t < 0.78:
                b = 70.5 - 2 * (t - 0.55) * 10
            else:
                b = 66 - (t - 0.78) * 230
            dpts.append([xx, Yd(b), 0])
        dr = VMobject(stroke_color=ACC, stroke_width=3).set_points_smoothly(dpts)
        cx = [ax0 + 0.2 + t * (ax1 - ax0 - 0.4) for t in (0.5, 0.6, 0.7)]
        cors = VGroup(*[VGroup(Line([x, Yd(70), 0], [x, Yd(50), 0], color=TMRC, stroke_width=2.2), T(str(k + 1), 15, TMRC, BOLD).move_to([x, Yd(78), 0])) for k, x in enumerate(cx)])
        corl = T("Ranging_Time düzeltmeleri", 14, TMRC, BOLD).next_to(cors, UP, buff=0.06)
        tiw = tag("TIWi", WARN, 16).move_to([ax1 - 0.45, Yd(64) + 0.25, 0])
        clr = VGroup(T("DOW altı → temizlenir", 14, GOOD, BOLD)).move_to([ax1 - 0.6, Yd(-40), 0])
        val = VGroup(T("önerilen (Tablo 13-1):", 15, MUTED, BOLD), T("TIW ±16 / ±64 bit ≈ ±6,4 ns", 16, WARN, BOLD), T("DOW ±8 / ±32 bit ≈ ±3,2 ns", 16, GOLD, BOLD))
        val.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.9, 1.2, 0])
        pmd = VGroup(s1chip(6, 15), T("en kötü koruma süresi", 15, TXT, BOLD)).arrange(DOWN, buff=0.1).move_to([4.9, -0.45, 0])
        gb = Rectangle(width=3.6, height=0.32, stroke_color=PMDC, stroke_width=1.6, fill_color=PMDC, fill_opacity=0.25).move_to([4.9, -1.35, 0])
        gbt = T("205,8 ns", 15, TXT, BOLD).move_to(gb)
        tb = Rectangle(width=3.6 * 6.4 / 205.8, height=0.32, stroke_width=0, fill_color=WARN, fill_opacity=0.9).align_to(gb, LEFT).set_y(-1.75)
        tbt = VGroup(T("6,4 ns ≈ %3", 16, WARN, BOLD), ytag("bizim hesabımız", size=14)).arrange(RIGHT, buff=0.12).next_to(tb, RIGHT, buff=0.1)
        tbt.set_x(gb.get_x() + 0.2)
        self.play(Create(axes), FadeIn(axl), self.set_src("G.989.3 Tablo 14-2 · Tablo 13-1 · G.989.2 Tablo III.2 · oran: bizim"), run_time=0.5)
        self.at(self.cue("zamanlama kayması dış eşiği", 2.0))
        self.play(FadeIn(thr), Create(dr), run_time=1.0)
        self.at(self.cue("üç düzeltmeden sonra", 6.5))
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.05) for c in cors], lag_ratio=0.3), FadeIn(corl), run_time=0.8)
        self.play(FadeIn(tiw, scale=0.9), run_time=0.35)
        self.at(self.cue("iç eşiğin altına inince", 10.9))
        self.play(FadeIn(clr, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("Önerilen dış eşik", 14.3))
        self.play(FadeIn(val, shift=LEFT * 0.05), run_time=0.45)
        self.at(self.cue("PMD Köprüsü:", 20.1))
        self.set_badge("pmd")
        self.play(FadeIn(pmd, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("iki yüz beş virgül sekiz", 26.9))
        self.play(GrowFromEdge(gb, LEFT), FadeIn(gbt), run_time=0.45)
        self.at(self.cue("yalnızca yüzde üçüdür", 30.2))
        self.play(GrowFromEdge(tb, LEFT), FadeIn(tbt), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep19_p4A")


class E19P4B(Act19):
    HDR, MANIFEST, PREV_BADGE = H19[4], M19("p4"), "pmd"

    def construct(self):
        # e5 — SUFi: the OLT sees the serial number but the ONU fails to complete bring-up; the only mandatory action in the table: send Deactivate_ONU-ID.
        #      DFi: a disabled ONU keeps answering allocations; visible only while the OLT keeps granting; its IDs may be blocked from re-allocation
        self.beat("e5")
        h = self.reset("SUFi ve DFi", "std", 0.5)
        L = frame_box("SUFi · başlatma başarısızlığı", DEFC, 6.1, 4.3, 17).move_to([-3.2, -0.4, 0])
        R = frame_box("DFi · devre dışı bırakma başarısızlığı", DEFC, 6.1, 4.3, 17).move_to([3.2, -0.4, 0])
        xo, xn = -5.2, -1.4
        lo = lifeline("OLT CT", xo, 1.05, -2.3, OLTC, 1.2, 0.42, 15)
        ln = lifeline("ONU", xn, 1.05, -2.3, ONUC, 1.0, 0.42, 15)
        sn = msg3(xn, xo, 0.3, "Serial_Number_ONU ↑ ✓", ONUC, None, 14)
        rg = VGroup(T("✗", 18, WARN, BOLD), T("bağlanma dizisi tamamlanmaz", 14, WARN, BOLD)).arrange(RIGHT, buff=0.1).move_to([(xo + xn) / 2, -0.3, 0])
        sf = tag("SUFi", WARN, 15).next_to([xo, -0.75, 0], RIGHT, buff=0.15)
        dc = msg3(xo, xn, -1.45, "Deactivate_ONU-ID ↓", FAM["dis"], None, 14)
        dcl = T("tablodaki tek zorunlu eylem", 14, GOLD, BOLD).next_to(dc, DOWN, buff=0.1)
        xo2, xn2 = 1.2, 5.0
        lo2 = lifeline("OLT CT", xo2, 1.05, -2.3, OLTC, 1.2, 0.42, 15)
        ln2 = lifeline("ONU", xn2, 1.05, -2.3, ONUC, 1.0, 0.42, 15)
        ds = msg3(xo2, xn2, 0.35, "Disable_Serial_Number ↓", FAM["dis"], None, 14)
        gr = msg3(xo2, xn2, -0.35, "tahsis ↓", ACC, None, 14)
        an = msg3(xn2, xo2, -0.85, "burst ↑ (hâlâ!)", WARN, None, 14)
        df = tag("DFi", WARN, 15).next_to([xo2, -1.2, 0], RIGHT, buff=0.15)
        dfl = VGroup(T("yalnızca tahsis sürdükçe görülür", 14, GOLD, BOLD), T("ONU-ID · Alloc-ID'ler bloke edilebilir", 14, MUTED, BOLD)).arrange(DOWN, buff=0.05).move_to([(xo2 + xn2) / 2, -1.8, 0])
        self.play(FadeIn(L), FadeIn(lo), FadeIn(ln), self.set_src("G.989.3 Tablo 14-2 · SUFi · DFi"), run_time=0.5)
        self.at(self.cue("OLT seri numarasını görür", 1.9))
        self.play(*grow_msg(sn), run_time=0.45)
        self.at(self.cue("bağlanma dizisini tamamlayamaz", 4.1))
        self.play(FadeIn(rg), FadeIn(sf, scale=0.9), run_time=0.4)
        self.at(self.cue("kimlik iptali mesajı gönder", 10.6))
        self.play(*grow_msg(dc), FadeIn(dcl, shift=UP * 0.05), run_time=0.45)
        self.at(self.cue("Devre dışı bırakma başarısızlığı", 12.9))
        self.play(FadeIn(R), FadeIn(lo2), FadeIn(ln2), *grow_msg(ds), run_time=0.5)
        self.at(self.cue("tahsislere cevap vermeyi sürdürür", 17.0))
        self.play(*grow_msg(gr), run_time=0.35)
        self.play(*grow_msg(an), FadeIn(df, scale=0.9), run_time=0.4)
        self.at(self.cue("OLT bunu ancak", 20.6))
        self.play(FadeIn(dfl[0], shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("yeniden atanmaktan alıkonabilir", 25.5))
        self.play(FadeIn(dfl[1], shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # e6 — three defects from management: LOPCi (persistent MIC failure or missing acknowledgements, persistent = ≥ 3 consecutive), LOOCi (recognised
        #      by the OMCI engine), DOTXi (count or amplitude of wavelength adjustments above thresholds); their cancellation cells are empty
        self.beat("e6")
        h = self.reset("Yönetimden gelen üç kusur", "std", 0.5)
        rows = [["LOPCi · PLOAM kanalı kaybı", "kalıcı MIC hatası ya da eksik onay · kalıcı = art arda ≥ 3", ""],
                ["LOOCi · OMCC kanalı kaybı", "OMCI motoru tanır (kalıcı ↑ MIC hatası)", ""],
                ["DOTXi · verici dalga boyu kayması", "ayar isteği sayısı ve/veya genliği eşikleri aşar", ""]]
        tb = mtable(["kusur", "saptama", "iptal koşulu"], rows, [3.6, 6.4, 2.6], size=16, hsize=15, row_h=0.62).move_to([0, 0.6, 0])
        for r in tb[1:]:
            r[1].set_color(WARN)
        holes = VGroup()
        for r in tb[1:]:
            x = r[0].get_right()[0] - 1.3
            holes.add(VGroup(DashedVMobject(Rectangle(width=2.3, height=0.46, stroke_color=NOCLR, stroke_width=2), num_dashes=24).move_to([x, r.get_y(), 0]),
                             T("boş", 16, NOCLR, BOLD).move_to([x, r.get_y(), 0])))
        th = VGroup(T("“persistent” =", 16, MUTED, BOLD), T("aynı düzensizlik art arda en az 3 kez", 17, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([0, -1.55, 0])
        nc = VGroup(tag("Amd.2 PDF s.160: hücreler boş", NOCLR, 15), T("standart ne zaman temizleneceklerini söylemez", 18, NOCLR, BOLD)).arrange(RIGHT, buff=0.25)
        fit(nc, 12.6).move_to([0, -2.45, 0])
        self.play(FadeIn(tb[0]), self.set_src("G.989.3 Tablo 14-2 · LOPCi · LOOCi · DOTXi"), run_time=0.4)
        self.at(self.cue("PLOAM kanalı kaybı:", 2.2))
        self.play(FadeIn(tb[1][:2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("kalıcı bütünlük hatası", 3.8))
        self.play(FadeIn(tb[1][2], shift=RIGHT * 0.05), run_time=0.35)
        self.at(self.cue("en az üç kez", 9.5))
        self.play(FadeIn(th, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("OMCC kanalı kaybını", 12.8))
        self.play(FadeIn(tb[2][:3], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("Verici dalga boyu kayması", 15.9))
        self.play(FadeIn(tb[3][:3], shift=RIGHT * 0.05), run_time=0.4)
        self.at(self.cue("iptal koşulu hücreleri boştur", 23.9))
        self.play(LaggedStart(*[Create(hh[0]) for hh in holes], lag_ratio=0.2), *[FadeIn(hh[1]) for hh in holes], run_time=0.7)
        self.at(self.cue("ne zaman temizleneceklerini", 27.5))
        self.play(FadeIn(nc, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # e7 — ALRFi: no change in received power after a Change_Power_Level acknowledged by the ONU. PMD Köprüsü: S1·B8 levels change in 3 dB steps;
        #      S1·B10 Appendix II repeatability ±0.5 dB → our calculation: the step is 6× that → visible as a change; the change threshold is not written
        self.beat("e7")
        h = self.reset("ALRFi — zayıflatma düzeyi isteği", "std", 0.5)
        xo, xn = -5.0, -1.4
        lo = lifeline("OLT CT", xo, 1.8, -0.9, OLTC, 1.2, 0.42, 15)
        ln = lifeline("ONU", xn, 1.8, -0.9, ONUC, 1.0, 0.42, 15)
        cp = msg3(xo, xn, 1.05, "Change_Power_Level ↓", FAM["pwr"], None, 14)
        ak = msg3(xn, xo, 0.4, "Acknowledgement ↑ · OK", GOOD, None, 14)
        rxp = VGroup(T("OLT alınan güç:", 15, TXT, BOLD), T("değişmedi", 16, WARN, BOLD)).arrange(RIGHT, buff=0.12).move_to([(xo + xn) / 2, -0.25, 0])
        al = tag("ALRFi", WARN, 16).next_to(rxp, DOWN, buff=0.15)
        alc = T("değişim saptanınca temizlenir", 14, GOOD, BOLD).next_to(al, DOWN, buff=0.1)
        ch = VGroup(s1chip(8, 15), s1chip(10, 15)).arrange(DOWN, buff=0.1).move_to([3.4, 1.85, 0])
        Y = lambda d: -0.6 + d * 0.42
        ax = Line([1.0, Y(-0.9), 0], [1.0, Y(3.6), 0], color=MUTED, stroke_width=2)
        axl = T("dB", 14, MUTED, BOLD).next_to(ax, UP, buff=0.05)
        b0 = Line([1.0, Y(0), 0], [5.2, Y(0), 0], color=TXT, stroke_width=2.4)
        b3 = Line([1.0, Y(3), 0], [5.2, Y(3), 0], color=FAM["pwr"], stroke_width=2.4)
        rep = Rectangle(width=4.2, height=Y(0.5) - Y(-0.5), stroke_width=0, fill_color=ACC, fill_opacity=0.22).move_to([3.1, Y(0), 0])
        repl = T("tekrarlanabilirlik ±0,5 dB · Ek II", 14, ACC, BOLD).next_to(rep, DOWN, buff=0.06)
        st = VGroup(arrow([4.6, Y(0), 0], [4.6, Y(3), 0], FAM["pwr"], 2.4, 0.14), T("adım 3 dB · §12.1.6", 15, FAM["pwr"], BOLD))
        st[1].next_to(b3, UP, buff=0.06).align_to(b3, LEFT).shift(RIGHT * 0.2)
        six = VGroup(T("3 / 0,5 = 6 ×", 20, GOLD, BOLD), ytag("bizim hesabımız", size=14)).arrange(RIGHT, buff=0.15).move_to([3.2, -2.05, 0])
        thr = VGroup(T("değişim eşiği:", 16, TXT, BOLD), tag("yazılı değil", WARN, 15)).arrange(RIGHT, buff=0.15).move_to([3.2, -2.7, 0])
        self.play(FadeIn(lo), FadeIn(ln), self.set_src("G.989.3 Tablo 14-2 · §12.1.6 · G.989.2 Ek II Tablo II.1 · Ek D"), run_time=0.45)
        self.at(self.cue("ONU'nun onayladığı", 4.5))
        self.play(*grow_msg(cp), run_time=0.4)
        self.play(*grow_msg(ak), run_time=0.4)
        self.at(self.cue("OLT'nin aldığı güç değişmez", 8.8))
        self.play(FadeIn(rxp, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(al, scale=0.9), FadeIn(alc), run_time=0.35)
        self.at(self.cue("PMD Köprüsü.", 11.5))
        self.set_badge("pmd")
        self.play(FadeIn(ch, shift=LEFT * 0.05), run_time=0.35)
        self.at(self.cue("üç desibellik adımlarla", 15.0))
        self.play(Create(ax), FadeIn(axl), Create(b0), Create(b3), GrowArrow(st[0]), FadeIn(st[1]), run_time=0.6)
        self.at(self.cue("tekrarlanabilirliği artı eksi yarım", 22.0))
        self.play(FadeIn(rep), FadeIn(repl), run_time=0.45)
        self.at(self.cue("bunun altı katıdır", 29.3))
        self.play(FadeIn(six, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Değişim eşiği ise", 32.8))
        self.play(FadeIn(thr, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # e8 — defects must know about sleep: in Table 16-7 a missed allocation is a self-transition in LowPowerWatch and Alerted (our reading: that is
        #      the exemption); in AwakeFree one miss throws the OLT to AwakeForced (+SA(OFF)) where LOBi can be declared; but "allocation miss" is
        #      defined nowhere and how Clob_i reaches the ONU is not written
        self.beat("e8")
        h = self.reset("Kusurlar uykuyu bilmeli", "std", 0.5)
        sm = PmSM("L", cx=-2.95, cy=0.3, dx=2.25, dy=1.1, w=3.0, h=0.8, tsize=17, ssize=15)
        lp3 = sm.loop(3, "kaçırma · *", RLC, "B", 14)
        lp4 = sm.loop(4, "kaçırma · *", TNC, "B", 14)
        e21 = sm.edge(2, "L", 1, "R", "kaçırma / SA(OFF)", SAOFF, 0.0, 0.0, UP, 0.08, lshift=UP * 0.42)
        lob = tag("LOBi burada ilan edilebilir", WARN, 15).next_to(sm.b[1], DOWN, buff=0.18)
        ex = VGroup(ytag("bizim okumamız"), T("kendine dönüş = muafiyet", 16, GOLD, BOLD)).arrange(RIGHT, buff=0.15).move_to([-3.0, -2.75, 0])
        row = mtable(["girdi", "(1)", "(2)", "(3)", "(4)"], [["Allocation miss", "*", "→ (1) / SA(OFF)", "*", "*"]], [2.2, 0.55, 1.75, 0.55, 0.55], size=15, hsize=14, row_h=0.42)
        row.move_to([3.85, 1.55, 0])
        rl = T("Tablo 16-7", 14, MUTED, BOLD).next_to(row, UP, buff=0.06).align_to(row, LEFT)
        nd = VGroup(VGroup(T("“Allocation miss”:", 15, TXT, BOLD), T("Tablo 16-6'da yok · tanımsız", 15, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04),
                    VGroup(T("Clob_i ONU'ya nasıl bildirilir?", 15, TXT, BOLD), T("yazılı değil", 15, WARN, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04))
        nd.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.85, -0.7, 0])
        self.play(FadeIn(sm.boxes()), self.set_src("G.989.3 Tablo 16-7 · Tablo 16-5 · Tablo 16-6 · Tablo 14-2"), run_time=0.5)
        self.at(self.cue("Geçiş tablosunda,", 2.8))
        self.play(FadeIn(rl), FadeIn(row), run_time=0.4)
        self.at(self.cue("düşük güç gözetiminde ve uyarılmış", 4.3))
        self.play(Create(lp3[0]), FadeIn(lp3[1]), Create(lp4[0]), FadeIn(lp4[1]), Indicate(VGroup(row[1][4], row[1][5]), color=GOLD), run_time=0.7)
        self.at(self.cue("muafiyet budur", 11.7))
        self.play(FadeIn(ex, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Serbest uyanık durumda ise", 14.3))
        self.play(GrowArrow(e21[0]), FadeIn(e21[1]), Indicate(row[1][3], color=SAOFF), run_time=0.6)
        self.at(self.cue("burst kaybı orada", 20.6))
        self.play(FadeIn(lob, shift=DOWN * 0.05), run_time=0.4)
        self.at(self.cue("kaçırma girdisi hiçbir yerde", 23.7))
        self.play(FadeIn(nd[0], shift=LEFT * 0.05), run_time=0.4)
        self.at(self.cue("eşiğin ONU'ya nasıl", 27.7))
        self.play(FadeIn(nd[1], shift=LEFT * 0.05), run_time=0.4)
        self.end(pad=0.05)
        self.save_timeline("ep19_p4B")


class E19P4C(Act19):
    HDR, MANIFEST, PREV_BADGE = H19[4], M19("p4"), "std"

    def construct(self):
        # e9 — urgent status snapshot (§14.2.3): written to non-volatile memory when the channel to the OLT is compromised: in the dying-gasp sequence and
        #      whenever software switches the transmitter off; ≥ 10 records; format and retrieval not written. Our reading: literally every LowPower
        #      entry qualifies → at a 100 ms cycle, 36 000 writes per hour (example)
        self.beat("e9")
        h = self.heading19("Acil durum anlık görüntüsü — §14.2.3")
        nv = nvm_icon(10, 0, 3.4, 1.6, GOLD, "kalıcı bellek · ≥ 10 kayıt").move_to([-3.6, 0.9, 0])
        sv = VGroup(T("dayanır:", 15, MUTED, BOLD), T("yeniden aktivasyon · sıcak / soğuk açılış · güç kaybı", 15, TXT, BOLD)).arrange(RIGHT, buff=0.12).next_to(nv, DOWN, buff=0.15)
        tr1 = VGroup(T("tetik 1:", 16, GOLD, BOLD), T("son nefes dizisi", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        tr2 = VGroup(T("tetik 2:", 16, GOLD, BOLD), T("yazılım vericiyi her kapattığında", 17, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        trg = VGroup(tr1, tr2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, 1.4, 0])
        ta = VGroup(arrow(tr1.get_left() + LEFT * 0.1, nv[0].get_right() + UP * 0.25, GOLD, 2, 0.1), arrow(tr2.get_left() + LEFT * 0.1, nv[0].get_right() + DOWN * 0.15, GOLD, 2, 0.1))
        wh = VGroup(T("içerik: ONU durumu · kusurlar · arıza koşulları", 16, TXT, BOLD)).move_to([3.0, 0.35, 0])
        miss = VGroup(T("biçim", 16, TXT, BOLD), T("✗", 18, WARN, BOLD), T("okuma yolu", 16, TXT, BOLD), T("✗", 18, WARN, BOLD)).arrange(RIGHT, buff=0.12).move_to([3.0, -0.2, 0])
        ip = VGroup(ytag("bizim okumamız"), T("harfiyen: her düşük güç girişi de bir kayıt", 17, TXT, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -1.55, 0])
        ex = VGroup(ex_tag("örnek"), T("100 ms döngü → 3600 s / 0,1 s =", 17, TXT, BOLD), T("36 000 yazım / saat", 20, WARN, BOLD)).arrange(RIGHT, buff=0.2).move_to([0, -2.4, 0])
        self.at(self.cue("Ölüm sonrası tanı", 0.3))
        self.play(FadeIn(nv, shift=UP * 0.05), self.set_src("G.989.3 §14.2.3 · örnek hesap: bizim"), run_time=0.45)
        self.at(self.cue("durumunu ve kusurlarını kalıcı", 7.0))
        self.play(FadeIn(wh, shift=UP * 0.05), *[nv[1][k].animate.set_fill(opacity=0.55) for k in range(3)], run_time=0.45)
        self.at(self.cue("son nefes dizisinde", 11.9))
        self.play(FadeIn(tr1, shift=LEFT * 0.05), GrowArrow(ta[0]), run_time=0.4)
        self.at(self.cue("yazılımı vericiyi her", 13.6))
        self.play(FadeIn(tr2, shift=LEFT * 0.05), GrowArrow(ta[1]), run_time=0.4)
        self.at(self.cue("En az on kayıt", 16.8))
        self.play(FadeIn(sv, shift=UP * 0.05), Indicate(nv[2], color=GOLD), run_time=0.45)
        self.at(self.cue("biçimi ve okuma yolu", 19.0))
        self.play(FadeIn(miss, shift=UP * 0.05), run_time=0.35)
        self.at(self.cue("her düşük güç girişi", 24.1))
        self.play(FadeIn(ip, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("saatte otuz altı bin", 29.5))
        self.play(FadeIn(ex, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        # e10 — dying gasp step by step: local condition → DG bit (Ind bit 0) in the US FS header + snapshot; not a promise to go silent (revoked if the
        #       condition passes); the OLT may count DG bursts per ONU but does not withdraw allocations on DG alone; on power return Serial_Number_ONU
        #       may carry code 1101 (13): "ONU has lost power"
        self.beat("e10")
        h = self.reset("Son nefes — adım adım", "std", 0.5)
        steps = [("1", "yerel durum saptanır", "tahsislere cevabı engelleyebilecek bir durum", ONUC),
                 ("2", "↑ FS başlığında Ind bit 0 = 1 (DG)", "+ acil durum anlık görüntüsü kaydedilir", GOLD),
                 ("3", "susma sözü değil", "durum geçerse bildirim geri alınır", ACC),
                 ("4", "OLT: ONU başına DG burst sayısı (O)", "yalnızca DG ile tahsisleri geri çekmez", OLTC),
                 ("5", "güç geri gelince", "Serial_Number_ONU · Activation Debug 1101 (13)", GOOD)]
        cards = VGroup()
        for n, a, b, c in steps:
            num = VGroup(Circle(radius=0.22, stroke_color=c, stroke_width=2.2, fill_color=PANEL, fill_opacity=1), T(n, 18, c, BOLD))
            num[1].move_to(num[0])
            g = VGroup(T(a, 17, TXT, BOLD), T(b, 15, MUTED, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            cards.add(VGroup(num, g.next_to(num, RIGHT, buff=0.22)))
        for k, cc in enumerate(cards):
            cc.move_to([-6.2, 1.85 - 0.95 * k, 0], aligned_edge=LEFT)
        ars = VGroup(*[arrow(cards[k][0].get_bottom(), cards[k + 1][0].get_top(), MUTED, 1.8, 0.08) for k in range(4)])
        hd = fields([("ONU-ID", 10, ACC), ("Ind", 9, GOLD), ("HEC", 13, HECC)], 5.4, 0.5, 16, 14, show_w=True, unit=" bit").move_to([3.7, 1.25, 0])
        hdl = T("↑ FS başlığı", 15, TXT, BOLD).next_to(hd, UP, buff=0.12).align_to(hd, LEFT)
        ib = VGroup(*[Rectangle(width=0.26, height=0.34, stroke_color=GOLD, stroke_width=1.2, fill_color=GOLD if k == 8 else BG, fill_opacity=0.9 if k == 8 else 0.4) for k in range(9)]).arrange(RIGHT, buff=0.03)
        ib.next_to(hd[1][0], DOWN, buff=0.75)
        ibl = T("bit 0 · DG", 15, GOLD, BOLD).next_to(ib[8], RIGHT, buff=0.12)
        zl = zoom_lines(hd[1][0], ib, GOLD)
        lost = VGroup(HX("1101", 20, GOOD, BOLD), T("“ONU has lost power”", 16, TXT, BOLD), s2chip(6, 14)).arrange(RIGHT, buff=0.2).move_to([3.6, -1.95, 0])
        self.play(self.set_src("G.989.3 §8.1.2.1.2 · §14.2.3 · Tablo 14-1 · Tablo 14-2 · Activation Debug (S2·B6)"), run_time=0.3)
        self.at(self.cue("tahsislere cevap vermesini", 2.0))
        self.play(FadeIn(cards[0], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("son nefes bitini kurar", 9.5))
        self.play(GrowArrow(ars[0]), FadeIn(cards[1], shift=UP * 0.05), FadeIn(hd), FadeIn(hdl), run_time=0.5)
        self.play(Create(zl), FadeIn(ib), FadeIn(ibl), run_time=0.4)
        self.at(self.cue("Bu bir susma sözü", 13.9))
        self.play(GrowArrow(ars[1]), FadeIn(cards[2], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("OLT bu burst'leri", 19.0))
        self.play(GrowArrow(ars[2]), FadeIn(cards[3], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("Güç geri gelince", 26.1))
        self.play(GrowArrow(ars[3]), FadeIn(cards[4], shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("güç kesildi", 31.4))
        self.play(FadeIn(lost, shift=UP * 0.05), run_time=0.35)
        self.end(pad=0.05)

        # e11 — PMD Köprüsü (S1·B10): DG helps tell fibre problems from premises problems; G.989.2 defines neither LOS nor DG; Type B QLOS also takes DG
        #       into account, but the exclusion rules it refers to ("as specified in G.989.3") are written in no clause
        self.beat("e11")
        h, chp = self.pmd_reset2("PMD Köprüsü — son nefes", [s1chip(10)])
        o1 = odn(x_olt=-5.9, y=0.95, n=3, x_sp=-4.3, x_onu=-2.6, dy=0.55, olt_label="OLT", onu_w=0.9, size=14)
        cut = xmark(Square(0.2).move_to(o1["feeder"].get_center()), WARN, 3, 0.0)
        c1 = VGroup(T("fiber kesik:", 15, WARN, BOLD), T("çok ONU · LOBi / LOS · DG yok", 15, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(o1["all"], DOWN, buff=0.2)
        o2 = odn(x_olt=0.4, y=0.95, n=3, x_sp=2.0, x_onu=3.7, dy=0.55, olt_label="OLT", onu_w=0.9, size=14)
        dg = VGroup(T("DG", 15, GOLD, BOLD)).next_to(o2["onus"][1], RIGHT, buff=0.12)
        pw = T("güç ✗", 15, WARN, BOLD).next_to(dg, RIGHT, buff=0.1)
        c2 = VGroup(T("abone tarafı:", 15, GOLD, BOLD), T("tek ONU · önce DG burst'leri", 15, TXT, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(o2["all"], DOWN, buff=0.2)
        nog = VGroup(T("G.989.2:", 17, GOLD, BOLD), T("LOS tanımı", 16, TXT, BOLD), T("✗", 18, WARN, BOLD), T("son nefes tanımı", 16, TXT, BOLD), T("✗", 18, WARN, BOLD)).arrange(RIGHT, buff=0.15)
        nog.move_to([0, -1.25, 0])
        ql = VGroup(T("Tip B · QLOS:", 16, GOLD, BOLD), T("dört çerçeve sessizlik + LOBi; ONU sayısı, güç yönetimi ve DG'ye göre dışlama", 15, TXT, BOLD)).arrange(RIGHT, buff=0.15)
        fit(ql, 12.6).move_to([0, -1.95, 0])
        rf = VGroup(T("“as specified in [ITU-T G.989.3]”", 16, MUTED, BOLD), T("→", 18, MUTED, BOLD), tag("hiçbir maddede yok", WARN, 15)).arrange(RIGHT, buff=0.2).move_to([0, -2.65, 0])
        self.play(FadeIn(o1["all"]), self.set_src("G.989.3 §8.1.2.1.2 · Tablo 18-3 · G.989.2 (LOS / DG tanımı yok) · S1·B10"), run_time=0.5)
        self.at(self.cue("fiber sorunlarını abone", 1.8))
        self.play(Create(cut), FadeIn(c1, shift=UP * 0.05), run_time=0.45)
        self.play(FadeIn(o2["all"]), FadeIn(dg), FadeIn(pw), FadeIn(c2, shift=UP * 0.05), run_time=0.5)
        self.at(self.cue("arıza vakası olarak", 9.5))
        self.play(Indicate(chp[0], color=S1C, scale_factor=1.1), run_time=0.45)
        self.at(self.cue("ne sinyal kaybının ne de", 13.3))
        self.play(FadeIn(nog, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("nitelikli sinyal kaybı da", 18.8))
        self.play(FadeIn(ql, shift=UP * 0.05), run_time=0.4)
        self.at(self.cue("dışlama kuralları ise", 24.7))
        self.play(FadeIn(rf, shift=UP * 0.05), run_time=0.4)
        self.end(pad=0.05)

        self.note11("e12", [("1", "ONU'ları uyutuyorsanız LOBi eşiğini tahsis aralığıyla birlikte ayarlayın",
                             "Dörtlük varsayılan, seyrek tahsisli bir ONU'da milisaniyeler sürer (bizim hesabımız: 1/16 → 8 ms).", "burst kaybı eşiğini"),
                            ("2", "Temizlenme koşulu olmayan üç kusur için kendi kuralınızı yazın",
                             "Yoksa bir kez ilan edilen LOPCi, yönetim sisteminde süresiz açık kalabilir.", "İki:")])
        self.bridge_beat("e13", "Enerji ve sağlık tanımlandı.\nŞimdi laboratuvarda ölçelim.")
        self.save_timeline("ep19_p4C")
