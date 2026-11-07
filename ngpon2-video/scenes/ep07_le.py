"""B07 · Laboratuvarda (ayarı ölçmek) ve Kapanış."""
from ep07_common import *


class E7LabA(Act7):
    HDR, MANIFEST, FIRST = H7["L"], M7("lab"), True

    def construct(self):
        self.beat("g1")
        tc = self.title_card("LABORATUVARDA", "Ayarı ölçmek")
        self.at(self.q("üç açıdan ölçeceğiz", 3))
        self.to_header(tc)
        self.set_badge("lab")
        h = self.show_heading("Zaman + dalga boyu birlikte")
        tiles = VGroup(
            card("Ayar süresi", "komut → ilk\ngeçerli burst", None, GOOD, w=3.9, h=1.6, tsize=23, bsize=18),
            card("Burst içi kayma", "ısıl cırlama", None, TUNE, w=3.9, h=1.6, tsize=23, bsize=18),
            card("Kanal dışı güç", "ayar sırasında\nkomşuya sızıntı", None, LEAK, w=3.9, h=1.6, tsize=23, bsize=18)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.35)
        cap = T("zamanda ve dalga boyunda aynı anda görebilen düzenek", 20, ACC, BOLD).move_to([0, -1.6, 0])
        self.at(self.q("ayar süresi,", 6.3))
        self.play(FadeIn(tiles[0], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("burst içi dalga boyu kayması,", 7.5))
        self.play(FadeIn(tiles[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ve ayar sırasındaki kanal dışı güç.", 9.2))
        self.play(FadeIn(tiles[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("zamanda ve dalga boyunda aynı anda", 14))
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g1a")
        self.clear(h)
        h = self.show_heading("Düzenek: ONU → kuplör → iki kol", h)
        onu = sbox("ayarlı ONU", "OLT öykünücüsü", TUNE, 2.4, 1.0, 19, 14).move_to([-4.6, 0.9, 0])
        cpl = splitter(0.5).move_to([-1.6, 0.9, 0])
        cplt = T("kuplör", 14, MUTED).next_to(cpl, DOWN, buff=0.1)
        wm = sbox("dalga boyu\nölçer", "süzgeç-PD", LOCK, 2.5, 1.0, 17, 13).move_to([2.0, 2.0, 0])
        pm = sbox("güç ölçer", None, ACC, 2.0, 0.85, 18).move_to([1.6, -0.2, 0])
        osa = sbox("OSA", None, GOLD, 1.5, 0.85, 18).move_to([4.2, -0.2, 0])
        links = VGroup(Line(onu.get_right(), cpl.get_left(), color=FEED, stroke_width=2.5),
                       Line(cpl.get_right(), wm.get_left(), color=FEED, stroke_width=2.5),
                       Line(cpl.get_right(), pm.get_left(), color=FEED, stroke_width=2.5),
                       Line(pm.get_right(), osa.get_left(), color=FEED, stroke_width=2.5))
        cap = T("dalga boyu + güç, zamanla birlikte", 19, ACC, BOLD).move_to([0, -1.9, 0])
        self.play(FadeIn(onu), run_time=0.4)
        self.at(self.q("bir OLT öykünücüsüyle sürülür", 3))
        self.play(FadeIn(cpl), FadeIn(cplt), Create(links[0]), run_time=0.5)
        self.at(self.q("hızlı bir dalga boyu ölçere", 9))
        self.play(FadeIn(wm), Create(links[1]), run_time=0.6)
        self.at(self.q("optik spektrum çözümleyiciye", 16.9))
        self.play(FadeIn(pm), FadeIn(osa), Create(links[2]), Create(links[3]), run_time=0.7)
        self.at(self.q("gücü zamanla birlikte izleriz", 21.58))
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g2")
        self.clear(h)
        h = self.show_heading("Ölçüm 1: ayar süresi (TC katmanı)", h)
        yb = 0.3
        tl = Line([-5.6, yb, 0], [5.6, yb, 0], color=MUTED, stroke_width=2)
        segs = VGroup()
        xs = [-4.4, -1.6, 1.8, 4.6]
        names = [("hazırlık", GOLD), ("fiziksel ayar", TUNE), ("yeniden senkron", ACC)]
        for i, (nm, c) in enumerate(names):
            r = Rectangle(width=xs[i + 1] - xs[i] - 0.1, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.5).move_to([(xs[i] + xs[i + 1]) / 2, yb + 0.35, 0])
            segs.add(VGroup(r, T(nm, 15, BG, BOLD).move_to(r)))
        m1 = VGroup(Line([xs[0], yb - 0.35, 0], [xs[0], yb + 0.9, 0], color=GOLD, stroke_width=3), T("ayar komutu", 16, GOLD, BOLD).next_to([xs[0], yb - 0.35, 0], DOWN, buff=0.12))
        m2 = VGroup(Line([xs[3], yb - 0.35, 0], [xs[3], yb + 0.9, 0], color=GOOD, stroke_width=3), T("hedef kanalda ilk geçerli burst", 16, GOOD, BOLD).next_to([xs[3], yb - 0.35, 0], DOWN, buff=0.12))
        br = BraceBetweenPoints([xs[0], yb + 1.0, 0], [xs[3], yb + 1.0, 0], UP, color=TXT)
        brt = T("TC katmanı ayar süresi", 20, TXT, BOLD).next_to(br, UP, buff=0.08)
        self.play(Create(tl), FadeIn(m1), run_time=0.6)
        self.at(self.q("komutun verildiği an,", 8.66))
        self.play(FadeIn(m2), run_time=0.5)
        self.at(self.q("TC katmanı ayar süresidir;", 17))
        self.play(FadeIn(br), FadeIn(brt), run_time=0.5)
        self.at(self.q("fiziksel ayar ve yeniden senkronun toplamı", 19.51))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.05) for s in segs], lag_ratio=0.2), run_time=0.9)
        self.end(pad=0.05)

        self.beat("g2a")
        self.clear(h)
        h = self.show_heading("Fiziksel süre ayrı — ve genelde kısa", h)
        yb = 0.3
        tl = Line([-5.6, yb, 0], [5.6, yb, 0], color=MUTED, stroke_width=2)
        xs = [-4.4, -1.6, 4.6]
        phys = Rectangle(width=xs[1] - xs[0], height=0.6, stroke_width=0, fill_color=TUNE, fill_opacity=0.55).move_to([(xs[0] + xs[1]) / 2, yb + 0.35, 0])
        rest = Rectangle(width=xs[2] - xs[1], height=0.6, stroke_width=0, fill_color=ACC, fill_opacity=0.45).move_to([(xs[1] + xs[2]) / 2, yb + 0.35, 0])
        pl = T("fiziksel ayar\n(lazer oturur)", 15, BG, BOLD, line_spacing=0.85).move_to(phys)
        rl = T("yeniden senkron + hazırlık", 16, BG, BOLD).move_to(rest)
        wm = T("dalga boyu ölçer: MSE penceresine oturma anı", 17, TUNE, BOLD).next_to([xs[1], yb + 0.65, 0], UP, buff=0.2)
        tip = Line([xs[1], yb, 0], [xs[1], yb + 0.65, 0], color=TUNE, stroke_width=3)
        cap = T("asıl önemli olan: sistemin gördüğü TC süresi (daha uzun)", 19, GOLD, BOLD).move_to([0, -2.2, 0])
        self.play(Create(tl), FadeIn(phys), FadeIn(pl), run_time=0.6)
        self.at(self.q("spektral sapma penceresi içine oturduğu", 7.49))
        self.play(Create(tip), FadeIn(wm), run_time=0.6)
        self.at(self.q("yeniden senkron ve hazırlığın payıdır;", 14.3))
        self.play(FadeIn(rest), FadeIn(rl), run_time=0.6)
        self.at(self.q("asıl önemli olan odur.", 20.7))
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep07_labA")


class E7LabB(Act7):
    HDR, MANIFEST, PREV_BADGE = H7["L"], M7("lab"), "lab"

    def construct(self):
        self.beat("g3")
        self.set_badge("lab")
        h = self.show_heading("Ölçüm 2: burst içi dalga boyu kayması")
        env, edges, xe = burst_env(-5.0, -2.4, -1.0, BURST, widths={"g0": 0.6, "on": 0.6, "pre": 1.4, "dlm": 0.5, "pay": 4.2, "off": 0.6, "g1": 0.6})
        axl = Line([-5.0, -2.4, 0], [xe + 0.1, -2.4, 0], color=MUTED, stroke_width=2)
        envlab = T("güç", 14, MUTED).next_to(env, LEFT, buff=0.1).set_y(-1.7)
        # wavelength drift over the payload (chirp)
        px0, px1 = edges["on"][0], edges["off"][1]
        drift = VMobject(stroke_color=TUNE, stroke_width=3.5).set_points_smoothly(
            [[px0, 0.4, 0], [px0 + 0.6, 0.45, 0], [(px0 + px1) / 2, 0.9, 0], [px1 - 0.4, 1.6, 0], [px1, 1.75, 0]])
        dlab = T("dalga boyu (ısıl cırlama)", 16, TUNE, BOLD).next_to(drift, UP, buff=0.05).set_x(-1.0)
        d0 = DashedLine([px0, 0.4, 0], [6.0, 0.4, 0], color=MUTED, stroke_width=1.5)
        d1 = DashedLine([px1, 1.75, 0], [6.0, 1.75, 0], color=MUTED, stroke_width=1.5)
        dlt = VGroup(DoubleArrow([5.7, 0.4, 0], [5.7, 1.75, 0], buff=0, color=GOLD, stroke_width=2.5, tip_length=0.12), T("Δλ", 18, GOLD, BOLD).next_to([5.7, 1.1, 0], LEFT, buff=0.1))
        cap = T("tek burst'e kapıla → baş ile son arasındaki Δλ", 18, TUNE, BOLD).move_to([-0.5, -3.3, 0])
        self.play(Create(axl), FadeIn(env, shift=UP * 0.1), FadeIn(envlab), run_time=0.8)
        self.at(self.q("lazeri ısıtır ve dalga boyunu burst boyunca kaydırır", 12.52))
        self.play(Create(drift), FadeIn(dlab), run_time=0.9)
        self.at(self.q("Buna ısıl cırlama deriz.", 17.64))
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.at(self.q("başı ile sonu arasındaki dalga boyu farkını", 24.25))
        self.play(Create(d0), Create(d1), GrowFromCenter(dlt[0]), FadeIn(dlt[1]), run_time=0.7)
        self.end(pad=0.05)

        self.beat("g3a")
        self.clear(h)
        h = self.show_heading("Neden önemli?", h)
        axg, X = lin_axis(-120, 120, -5.5, 2.5, -0.6, [-100, -50, 0, 50, 100], size=13, fmt=lambda v: ("C" if v == 0 else tr(v)), unit="GHz")
        win = Rectangle(width=X(25) - X(-25), height=2.0, stroke_color=GOOD, stroke_width=2, fill_color=GOOD, fill_opacity=0.12).move_to([X(0), 0.4, 0])
        wint = T("MSE penceresi", 15, GOOD, BOLD).next_to(win, UP, buff=0.08)
        start = glow_dot(ACC, 0.06, 3).move_to([X(0), -0.1, 0])
        startl = T("burst başı", 14, ACC, BOLD).next_to(start, DOWN, buff=0.1)
        endd = glow_dot(WARN, 0.06, 3).move_to([X(45), 0.5, 0])
        arr = arrow([X(5), 0.1, 0], [X(42), 0.45, 0], TUNE, 3)
        endl = T("burst sonu → pencereden taşar / komşuya sızar", 16, WARN, BOLD).move_to([X(40), 1.5, 0])
        tail = T("en uzun izin verilen burst'te ölç = en kötü durum", 18, GOLD, BOLD).move_to([-0.5, -2.4, 0])
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(win), FadeIn(wint), FadeIn(start), FadeIn(startl), run_time=0.8)
        self.at(self.q("spektral sapma penceresinden taşabilir,", 8.05))
        self.play(GrowArrow(arr), FadeIn(endd), FadeIn(endl), run_time=0.7)
        self.at(self.q("en uzun izin verilen burst", 18.56))
        self.play(FadeIn(tail, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.05)

        self.beat("g4")
        self.clear(h)
        self.set_badge("fiz")
        h = self.show_heading("Ölçüm 3: ayar sırasında kanal dışı güç", h)
        axg, X = lin_axis(-250, 250, -5.6, 3.4, -1.2, [-200, -100, 0, 100, 200], size=12, fmt=lambda v: ("C" if v == 0 else tr(v)), unit="GHz")
        src = lobe(X, 0, -1.2, 1.3, 14, BURST, op=0.3)
        sweep = arrow([X(-10), 0.3, 0], [X(140), 0.3, 0], TUNE, 3)
        nb = Rectangle(width=X(120) - X(80), height=1.6, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.1).move_to([X(100), -0.4, 0])
        nbt = VGroup(T("komşu kanal", 14, WARN, BOLD), T("dar süzgeç + PM", 13, MUTED)).arrange(DOWN, buff=0.04).next_to(nb, UP, buff=0.1)
        cmp = VGroup(T("karşılaştır:", 18, TXT, BOLD), T("durağan maske DEĞİL → D eki ayar gevşemesi", 19, GOLD, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -2.5, 0])
        self.play(Create(axg[0]), FadeIn(axg[1:]), FadeIn(src), run_time=0.7)
        self.at(self.q("bir komşu kanalın bandına düşen gücü,", 7.14))
        self.play(GrowArrow(sweep), FadeIn(nb), FadeIn(nbt), run_time=0.7)
        self.at(self.q("D ekindeki ayar gevşemesiyle", 18.07))
        self.play(FadeIn(cmp, shift=UP * 0.1), self.set_src("G.989.2 Ek D (ayar gevşemesi)"), run_time=0.6)
        self.end(pad=0.05)

        self.beat("g4a")
        self.clear(h)
        self.set_badge("lab")
        h = self.show_heading("Süre boyutu: komşuya nezaket", h)
        c1 = card("Sınıf 1 · hızlı", "ayar penceresi KISA\n→ komşu kısa rahatsız", None, GOOD, w=5.2, h=1.8, tsize=23, bsize=19).move_to([-3.2, 0.6, 0])
        c2 = card("Sınıf 2 · yavaş", "ayar penceresi UZUN\n→ komşu uzun rahatsız", None, GOLD, w=5.2, h=1.8, tsize=23, bsize=19).move_to([3.2, 0.6, 0])
        tail = T("hızlı ayar = yalnızca verimlilik değil, komşuya nezaket", 20, ACC, BOLD).move_to([0, -2.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("hızlı ayar yalnızca verimlilik değil,", 11.07))
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at(self.q("hem daha çabuk hem daha kibar", 18.05))
        self.play(FadeIn(tail, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep07_labB")


class E7LabC(Act7):
    HDR, MANIFEST, PREV_BADGE = H7["L"], M7("lab"), "lab"

    def construct(self):
        self.beat("g5")
        self.set_badge("lab")
        h = self.show_heading("Üç ölçüm = vericinin olgunluğu")
        tiles = VGroup(
            card("Ayar süresi", "ne kadar hızlı", None, GOOD, w=3.9, h=1.7, tsize=23, bsize=18),
            card("Burst içi kayma", "ne kadar küçük", None, TUNE, w=3.9, h=1.7, tsize=23, bsize=18),
            card("Ayar sızıntısı", "ne kadar sınırlı", None, LEAK, w=3.9, h=1.7, tsize=23, bsize=18)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.8)
        concl = T("üçü ne kadar iyiyse, o kadar güvenle renk değiştirir", 20, GOLD, BOLD).move_to([0, -1.6, 0])
        self.at(self.q("ayarlanabilir bir vericinin olgunluğunu", 2))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.2), run_time=0.9)
        self.at(self.q("güvenle renk değiştirebilir.", 13.78))
        self.play(FadeIn(concl, shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.1)

        self.note5("g6", [("1", "Ayar süresini yeniden senkrona kadar ölçün", "Lazerin oturduğu ana kadar değil; sistemin gördüğü süre budur.", "Bir:"),
                          ("2", "Burst içi kaymayı en uzun burst'te, tek burst'e kapılı ölçün", "Ortalama alan bir alet cırlama hakkında dürüst değildir.", "İki:")])

        self.beat("g7")
        self.clear()
        self.drop_badge()
        fwd = VGroup(T("ONU tarafını tamamladık", 30, ACC, BOLD),
                     T("Bugüne kadar: vericisi · alıcısı · burst modu · ayarı", 23, TXT, BOLD),
                     T("Bölüm 8: ağacın tepesine — OLT", 24, BURST, BOLD),
                     T("onlarca ONU'nun patlamalarını dinleyen,\nayırt eden ve dengeleyen tarafa", 21, MUTED, BOLD, line_spacing=0.9)).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeIn(fwd[0], shift=UP * 0.1), run_time=0.6)
        self.at(self.q("vericisi,", 3.17))
        self.play(FadeIn(fwd[1], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("OLT'ye çıkıyoruz;", 9.09))
        self.play(FadeIn(fwd[2], shift=UP * 0.1), run_time=0.5)
        self.at(self.q("ayırt eden ve dengeleyen tarafa", 13.75))
        self.play(FadeIn(fwd[3], shift=UP * 0.1), run_time=0.5)
        self.end(pad=0.3)
        self.play(FadeOut(fwd), FadeOut(self.hdr), run_time=0.6)
        self.save_timeline("ep07_labC")


class E7End(Act7):
    HDR, MANIFEST, FIRST = H7["E"], M7("end"), True

    def construct(self):
        self.beat("h1")
        tc = self.title_card("KAPANIŞ", "Bölüm 7'nin özeti")
        self.at(1.4)
        self.to_header(tc)
        self.set_badge("ozet")
        pts = ["ONU hem vericisini hem alıcısını dalga boyunda ayarlar; Tablo 9-2: 3 sınıf + 2 kısıtlı tür, teknoloji dayatılmaz",
               "Durağan: kanal dışı güç yoğunluğu maskesi; ayar sırasında D ekinde sınırlı gevşeme (lazer spektrumda yürür)",
               "Kalibrasyon = iç ayar ↔ dalga boyu; ↓ otonom, ↑ OLT geri beslemesiyle; dithering ile güncel tutulur",
               "Kanal yönetimi profil duyurusuyla (1–5 s); devir = zamanlı SFC + ayar denetimi/yanıtı + güvenli geri alma",
               "Her devir, yeni bir dalga boyu kadar yeni bir kriptografik bağlamdır"]
        items = VGroup(*[VGroup(T(f"{i + 1}", 30, ACC, BOLD), T(s, 19, TXT)).arrange(RIGHT, buff=0.35) for i, s in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        for it in items:
            fit(it, 13.2)
        self.at(self.cue("Bir:", 1.9))
        self.play(FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at(self.cue("İki:", 18.4))
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
        qs = VGroup(*[card(f"Soru {i + 1}", q, None, c, w=4.1, h=2.7, tsize=24, bsize=17) for i, (q, c) in enumerate([
            ("OLT burst alıcısı, her yeni\nONU'nun burst'üne güçte ve\nfazda ne kadar hızlı\nkilitlenmeli — hangi ek tanımlar?", CH[0]),
            ("Burst modu bir alıcının göz\naçıklığını ölçmek, neden\nsürekli mod ölçümünden\nfarklıdır?", CH[1]),
            ("Güç dengeleme neden gereklidir?\nFarklı uzaklıktaki iki ONU'nun\ngücü OLT'de neden\nsorun olur?", CH[3])])]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)
        ans = T("Cevaplar: Bölüm 8'in başında", 22, MUTED).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(ttl), run_time=0.5)
        self.at(self.cue("Birinci soru:", 1.7))
        self.play(FadeIn(qs[0], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("burst modu bir alıcının göz açıklığını", 13.77))
        self.play(FadeIn(qs[1], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("güç dengeleme neden gereklidir;", 22.89))
        self.play(FadeIn(qs[2], shift=UP * 0.2), run_time=0.6)
        self.at(self.cue("bir sonraki bölümün başında.", 31.13))
        self.play(FadeIn(ans), run_time=0.5)
        self.end(pad=0.1)

        self.beat("h4")
        self.clear()
        self.drop_badge()
        e8 = SERIES["episodes"][7]
        nxt = VGroup(T("SONRAKİ BÖLÜM", 22, ACC, BOLD), T(f"Bölüm {e8['n']} · {e8['title']}", 50, TXT, BOLD), T(e8["sub"], 24, MUTED)).arrange(DOWN, buff=0.25).move_to(UP * 1.4)
        for m in nxt:
            fit(m, 12.5)
        self.at(self.q("Kalabalığı Dinlemek.", 1.4))
        self.play(FadeIn(nxt[0]), Write(nxt[1]), run_time=1.1)
        self.play(FadeIn(nxt[2]), run_time=0.5)
        topics = VGroup(*[pill(s, c, 18) for s, c in [("OLT burst alıcısı", ACC), ("etkinleştirme + mesafe ölçümü", GOLD), ("güç dengeleme", GOOD)]]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.4)
        fit(topics, 13.0)
        self.at(self.q("OLT burst alıcısı,", 4.12))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in topics], lag_ratio=0.15), run_time=0.9)
        self.at(self.q("Görüşmek üzere.", 15))
        bye = T("Görüşmek üzere.", 26, TXT, BOLD).move_to(DOWN * 1.7)
        self.play(FadeIn(bye), run_time=0.5)
        self.end(pad=0.5)
        self.play(FadeOut(nxt), FadeOut(topics), FadeOut(bye), FadeOut(self.hdr), run_time=0.7)
        cr = VGroup(T("LAMBDA · Bölüm 7 · Renk Değiştiren Lazer", 30, TXT, BOLD),
                    T("Senaryo, animasyon ve görseller: Claude (Anthropic)", 22, TXT),
                    T("Seslendirme: XTTS-v2 · Damien Black", 22, ACC, BOLD),
                    T("Intro müziği: Google Lyria", 22, TXT),
                    T("Kaynaklar: ITU-T G.989.2 (2019)/Cor.1 (2019)/Amd.1 (2020) · ITU-T G.989.3 (2021)/Amd.2 (2025)", 18, MUTED)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(cr), run_time=1.0)
        self.wait(0.5)
        self.save_timeline("ep07_end")
