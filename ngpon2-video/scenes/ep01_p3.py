"""B01 · Perde 3 — G.989 ailesi ve PMD↔TC sınırı."""
from kit import *
from scipy.special import erfc
from scipy.stats import binom

HDR3 = "BÖLÜM 1 · PERDE 3 — G.989 ailesi ve PMD↔TC sınırı"
MAN3 = "build/v4/ep01_p3/audio_proc/manifest.json"
FAM = [("G.989", "tanımlar · kısaltmalar · kurallar", "#475569"), ("G.989.1", "genel gereksinimler", "#64748B"),
       ("G.989.2", "PMD — fiziksel ortama bağımlı katman", ACC), ("G.989.3", "TC — iletim yakınsama katmanı", "#A78BFA"),
       ("G.988", "OMCI — ONU yönetim ve kontrol arayüzü", GOLD)]


def block(i, w=6.6, h=0.78):
    name, desc, c = FAM[i]
    r = RoundedRectangle(corner_radius=0.12, width=w - 0.35 * i * (i == 0), height=h, stroke_color=c, stroke_width=3,
                         fill_color=c, fill_opacity=0.16)
    t = VGroup(T(name, 24, TXT, BOLD), T(desc, 17, TXT)).arrange(RIGHT, buff=0.35).move_to(r)
    if t.width > w - 0.4:
        t.scale_to_fit_width(w - 0.4)
    return VGroup(r, t)


def stack():
    blocks = VGroup(*[block(i) for i in range(5)]).arrange(UP, buff=0.12).move_to([-3.0, -0.75, 0])
    return blocks


class P3A(Act):
    HDR, MANIFEST, FIRST = HDR3, MAN3, True

    def construct(self):
        self.beat("r1")
        tc = self.title_card("PERDE 3", "G.989 ailesi ve PMD↔TC sınırı")
        self.at(self.cues[2] - 0.2)
        self.to_header(tc)
        h = self.show_heading("Beş tavsiye, tek sistem")
        st = stack()
        ground = Line([-6.6, st.get_bottom()[1] - 0.12, 0], [0.6, st.get_bottom()[1] - 0.12, 0], color=MUTED, stroke_width=3)
        self.at(self.cues[4] - 0.2)
        self.play(Create(ground), run_time=0.6)
        self.end(pad=0.05)
        side = VGroup()

        def side_list(items, color):
            g = VGroup(*[VGroup(Dot(radius=0.05, color=color), T(s, 20, TXT)).arrange(RIGHT, buff=0.18) for s in items])
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.9, -0.4, 0]).align_to([1.2, 0, 0], LEFT)

        for bid, i, items in [("r2", 0, ["tanımlar ve kısaltmalar", "kanal çifti, spektral sapma,\nayar süresi… resmi tanımları", "ailenin sözlüğü"]),
                              ("r3", 1, ["taşınacak servisler", "hedef kapasite", "eski sistemlerle birlikte çalışma", "sorular burada sorulur"]),
                              ("r4", 2, ["dalga boyları · güçler", "sönüm oranları", "alıcı hassasiyetleri", "ayar süreleri", "girişim toleransları"])]:
            self.beat(bid)
            new = side_list(items, FAM[i][2])
            cap = T(FAM[i][0], 30, FAM[i][2], BOLD).next_to(new, UP, buff=0.35, aligned_edge=LEFT)
            anims = [FadeIn(st[i], shift=DOWN * 0.3)]
            if len(side):
                anims.append(FadeOut(side))
            self.play(*anims, run_time=0.7)
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in new], lag_ratio=0.25), run_time=1.4)
            side = VGroup(cap, new)
            if bid == "r4":
                self.play(st[2][0].animate.set_fill(ACC, opacity=0.35), Indicate(st[2], color=ACC, scale_factor=1.03), run_time=0.8)
            self.end(pad=0.05)
        self.play(FadeOut(side), run_time=0.3)
        self.save_timeline("ep01_p3A")


class P3B(Act):
    HDR, MANIFEST = HDR3, MAN3

    def construct(self):
        h = self.heading("Beş tavsiye, tek sistem")
        st = stack()
        st[2][0].set_fill(ACC, opacity=0.35)
        ground = Line([-6.6, st.get_bottom()[1] - 0.12, 0], [0.6, st.get_bottom()[1] - 0.12, 0], color=MUTED, stroke_width=3)
        self.add(h, st[:3], ground)
        self.beat("r5")
        items = ["çerçeve yapısı", "ONU aktivasyonu", "bant genişliği tahsisi", "kanal yönetimi", "güvenlik ve koruma"]
        lst = VGroup(*[VGroup(Dot(radius=0.05, color=FAM[3][2]), T(s, 20, TXT)).arrange(RIGHT, buff=0.18) for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lst.move_to([2.8, 0.1, 0]).align_to([1.2, 0, 0], LEFT)
        cap = T("G.989.3", 30, FAM[3][2], BOLD).next_to(lst, UP, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(st[3], shift=DOWN * 0.3), FadeIn(cap), run_time=0.7)
        self.at(self.cues[2] - 0.2)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in lst], lag_ratio=0.35), run_time=2.6)
        base = VGroup(T("G.987.3 (XG-PON TC)", 20, MUTED, BOLD), T("→ G.989.3", 20, FAM[3][2], BOLD), T("+ NG-PON2'ye özgü değişiklikler", 18, FAM[3][2])
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(lst, DOWN, buff=0.45).align_to(lst, LEFT)
        self.at(self.cues[7])
        self.play(FadeIn(base, shift=UP * 0.15), self.set_src("G.989.2 Özet"), run_time=0.8)
        self.end(pad=0.05)

        self.beat("r6")
        lst2 = VGroup(*[VGroup(Dot(radius=0.05, color=GOLD), T(s, 20, TXT)).arrange(RIGHT, buff=0.18) for s in ["ONU yönetim ve kontrol arayüzü", "servislerin ONU'da yapılandırılması"]]
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(lst).align_to(lst, LEFT).align_to(lst, UP)
        cap2 = T("G.988", 30, GOLD, BOLD).move_to(cap).align_to(cap, LEFT)
        self.play(FadeIn(st[4], shift=DOWN * 0.3), FadeOut(lst), FadeOut(base), FadeTransform(cap, cap2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in lst2], lag_ratio=0.3), run_time=1.0)
        self.end(pad=0.05)

        # r7 — §9.1 layered structure
        self.beat("r7")
        self.play(*[FadeOut(m) for m in (st, ground, cap2, lst2)], run_time=0.5)
        q = self.quote("G.989.2 §9.1", "“…the data plane and the auxiliary management and control plane are mounted on top of\nthe common physical medium, represented by the NG-PON2 ODN.”",
                       "Veri düzlemi + yardımcı yönetim/kontrol düzlemi → ortak ODN'in üzerinde").scale(0.85).to_edge(UP, buff=1.55)
        self.play(FadeIn(q, shift=UP * 0.15), self.set_src("G.989.2 §9.1"), run_time=0.8)
        slab = RoundedRectangle(corner_radius=0.1, width=9.0, height=0.7, stroke_color=MUTED, stroke_width=2.5, fill_color="#1F2937", fill_opacity=1).move_to(DOWN * 2.3)
        slab_t = T("NG-PON2 ODN — ortak fiziksel ortam", 22, TXT, BOLD).move_to(slab)
        dp = RoundedRectangle(corner_radius=0.1, width=5.0, height=1.0, stroke_color=CH[1], stroke_width=2.5, fill_color=CH[1], fill_opacity=0.15).move_to(DOWN * 1.2 + LEFT * 2.0)
        mp = RoundedRectangle(corner_radius=0.1, width=3.6, height=1.0, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.15).move_to(DOWN * 1.2 + RIGHT * 2.7)
        dpt = T("veri düzlemi", 22, CH[1], BOLD).move_to(dp)
        mpt = T("yönetim/kontrol düzlemi", 20, GOLD, BOLD).move_to(mp)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(slab), FadeIn(slab_t), run_time=0.6)
        self.play(FadeIn(dp, shift=DOWN * 0.2), FadeIn(dpt), FadeIn(mp, shift=DOWN * 0.2), FadeIn(mpt), run_time=0.9)
        self.end(pad=0.05)

        # r8 — focus to TC bridge
        self.beat("r8")
        self.clear()
        st2 = stack()
        st2[2][0].set_fill(ACC, opacity=0.35)
        st2.move_to(ORIGIN + DOWN * 0.3)
        self.play(FadeIn(st2), run_time=0.6)
        yb = (st2[2].get_top()[1] + st2[3].get_bottom()[1]) / 2
        border = DashedLine([st2.get_left()[0] - 0.3, yb, 0], [st2.get_right()[0] + 0.3, yb, 0], color=GOLD, stroke_width=4, dash_length=0.12)
        self.at(self.cues[2] - 0.2)
        self.play(Create(border), st2[0].animate.set_opacity(0.3), st2[1].animate.set_opacity(0.3), st2[4].animate.set_opacity(0.3), run_time=0.9)
        self.at(self.cues[3])
        self.set_badge("tc")
        self.play(Flash(border.get_center(), color=GOLD, flash_radius=0.6, line_length=0.3), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep01_p3B")


class P3C(Act):
    HDR, MANIFEST, PREV_BADGE = HDR3, MAN3, "tc"

    def construct(self):
        self.beat("r9")
        h = self.show_heading("TC katmanının üç alt katmanı")
        names = [("Servis uyarlama", "XGEM kapsülleme · bölme · şifreleme (isteğe bağlı)", CH[1]),
                 ("Çerçeveleme", "PON yönetimi için başlık alanları", CH[0]),
                 ("PHY uyarlama", "FEC · karıştırma · senkronizasyon bloğu (PSB)", GOLD)]
        boxes = VGroup()
        for i, (n, d, c) in enumerate(names):
            r = RoundedRectangle(corner_radius=0.12, width=5.0, height=1.0, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.14)
            boxes.add(VGroup(r, T(n, 24, TXT, BOLD).move_to(r)))
        pmd = RoundedRectangle(corner_radius=0.12, width=5.0, height=1.0, stroke_color=ACC, stroke_width=3, fill_color=ACC, fill_opacity=0.3)
        pmd = VGroup(pmd, T("PMD — ışık", 24, TXT, BOLD).move_to(pmd))
        col = VGroup(*boxes, pmd).arrange(DOWN, buff=0.38).move_to([-3.6, -0.6, 0])
        arrows = VGroup(*[Arrow(col[i].get_bottom(), col[i + 1].get_top(), buff=0.04, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        descs = VGroup(*[T(d, 19, c).next_to(boxes[i], RIGHT, buff=0.45) for i, (n, d, c) in enumerate(names)])
        sdu = VGroup(T("SDU: kullanıcı verisi + OMCI", 18, MUTED)).next_to(col, UP, buff=0.2)
        self.play(FadeIn(sdu), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in col], lag_ratio=0.15), Create(arrows),
                  self.set_src("G.989.3 §6.1.2–6.1.3"), run_time=1.6)
        self.at(self.cues[1])
        self.play(Indicate(boxes[0], color=CH[1], scale_factor=1.04), FadeIn(descs[0], shift=RIGHT * 0.15), run_time=0.9)
        self.end(pad=0.05)

        self.beat("r10")
        self.play(Indicate(boxes[1], color=CH[0], scale_factor=1.04), FadeIn(descs[1], shift=RIGHT * 0.15), run_time=0.9)
        self.at(self.cues[2])
        self.play(Indicate(boxes[2], color=GOLD, scale_factor=1.04), FadeIn(descs[2], shift=RIGHT * 0.15), run_time=0.9)
        self.end(pad=0.05)

        # r11 — the PMD/TC interface: continuous frames down, timed bursts up
        self.beat("r11")
        self.clear(h)
        h = self.show_heading("Sınır: PMD ile TC'nin el sıkıştığı yer", h)
        x0, x1 = -6.0, 6.0
        yd, yu = 0.8, -1.6
        ds = VGroup(*[Rectangle(width=(x1 - x0) / 5 - 0.04, height=0.55, stroke_width=0, fill_color=WHITE, fill_opacity=0.8 - 0.25 * (i % 2))
                      .move_to([x0 + (i + 0.5) * (x1 - x0) / 5, yd, 0]) for i in range(5)])
        dsl = T("↓  sürekli bit akışı · 125 µs'lik PHY çerçeveleri", 22, WHITE, BOLD).next_to(ds, UP, buff=0.2).align_to(ds, LEFT)
        ticks = VGroup(*[T("125 µs", 15, MUTED).next_to(ds[i], DOWN, buff=0.08) for i in range(5)])
        rng = np.random.default_rng(4)
        us, x = VGroup(), x0
        for k in range(7):
            w = rng.uniform(0.6, 1.4)
            us.add(Rectangle(width=w, height=0.55, stroke_width=0, fill_color=CH[k % 4], fill_opacity=0.9).move_to([x + w / 2, yu, 0]))
            x += w + rng.uniform(0.15, 0.45)
        usl = T("↑  hassas zamanlanmış burst dizisi", 22, GOLD, BOLD).next_to(us, UP, buff=0.2).align_to(ds, LEFT)
        self.at(self.cues[1])
        self.play(FadeIn(dsl), LaggedStart(*[GrowFromEdge(r, LEFT) for r in ds], lag_ratio=0.2), FadeIn(ticks), self.set_src("G.989.3 §6.1.2"), run_time=1.8)
        self.at(self.cues[3])
        self.play(FadeIn(usl), LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in us], lag_ratio=0.2), run_time=1.8)
        self.end(pad=0.05)

        # r12 — downstream PHY frame anatomy
        self.beat("r12")
        self.clear(h)
        h = self.show_heading("Aşağı yön PHY çerçevesi (9,95328 Gbit/s)", h)
        bar = Rectangle(width=12.0, height=0.8, stroke_color=WHITE, stroke_width=2, fill_color=WHITE, fill_opacity=0.12).move_to(UP * 0.9)
        psb = Rectangle(width=0.5, height=0.8, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).align_to(bar, LEFT).align_to(bar, UP)
        bl = T("125 µs = 155 520 bayt   (2,48832 Gbit/s'de 38 880 bayt)", 22, TXT, BOLD).next_to(bar, UP, buff=0.2)
        pl = T("PHY yükü: FS çerçevesi — karıştırılmış, FEC ile korunur", 19, MUTED).move_to(bar).shift(RIGHT * 0.3)
        self.play(FadeIn(bar), FadeIn(bl), FadeIn(pl), run_time=0.8)
        self.at(self.cues[2])
        self.play(FadeIn(psb), run_time=0.4)
        fields = VGroup(*[RoundedRectangle(corner_radius=0.08, width=3.6, height=1.1, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.12) for _ in range(3)]
                        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.3)
        ft = VGroup(VGroup(T("PSync · 8 B", 20, GOLD, BOLD), T("0xC5E51840 FD59BB49", 16, TXT)),
                    VGroup(T("SFC + HEC · 8 B", 20, GOLD, BOLD), T("51-bit süper çerçeve sayacı", 16, TXT)),
                    VGroup(T("OC · 8 B", 20, GOLD, BOLD), T("işletim kontrol yapısı", 16, TXT)))
        for f, t in zip(fields, ft):
            t.arrange(DOWN, buff=0.1).move_to(f)
        zl = VGroup(DashedLine(psb.get_corner(DL), fields.get_corner(UL), color=GOLD, stroke_width=1.5),
                    DashedLine(psb.get_corner(DR), fields.get_corner(UR), color=GOLD, stroke_width=1.5))
        pt = T("PSBd = 24 bayt", 20, GOLD, BOLD).next_to(fields, DOWN, buff=0.2)
        self.at(self.cues[3])
        self.play(Create(zl), LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.2), FadeIn(ft), FadeIn(pt), self.set_src("G.989.3 §10.1.1"), run_time=1.4)
        self.at(self.cues[5])
        self.play(Indicate(VGroup(fields[0], ft[0]), color=WHITE, scale_factor=1.06), run_time=0.9)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep01_p3C")


class P3D(Act):
    HDR, MANIFEST, PREV_BADGE = HDR3, MAN3, "tc"

    def construct(self):
        self.beat("r12a")
        h = self.show_heading("Bir Ethernet çerçevesinin yolculuğu")
        eth = Rectangle(width=6.0, height=0.7, stroke_width=0, fill_color=CH[1], fill_opacity=0.85).move_to([0.5, 1.5, 0])
        et = T("Ethernet çerçevesi · 1500 B", 20, BG, BOLD).move_to(eth)
        self.at(self.cues[1])
        self.play(GrowFromEdge(eth, LEFT), FadeIn(et), run_time=0.8)
        hdr = Rectangle(width=0.8, height=0.7, stroke_width=0, fill_color=CH[0], fill_opacity=0.95).next_to(eth, LEFT, buff=0)
        ht = T("8 B", 16, WHITE, BOLD).move_to(hdr)
        hl = T("XGEM başlığı → XGEM Port-ID (akış kimliği)", 19, CH[0], BOLD).next_to(VGroup(hdr, eth), DOWN, buff=0.2).align_to(hdr, LEFT)
        self.at(self.cues[3] - 0.2)
        self.play(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(ht), run_time=0.6)
        self.at(self.cues[4])
        self.play(FadeIn(hl), self.set_src("G.989.3 §9.1 — XGEM başlığı 8 bayt"), run_time=0.6)
        self.end(pad=0.05)

        self.beat("r12b")
        xg = VGroup(hdr, ht, eth, et)
        self.play(FadeOut(hl), xg.animate.scale(0.5).move_to([-3.6, 1.5, 0]), run_time=0.6)
        fs = RoundedRectangle(corner_radius=0.08, width=7.2, height=0.9, stroke_color=MUTED, stroke_width=2).move_to([1.6, 1.5, 0])
        fsh = Rectangle(width=0.9, height=0.9, stroke_width=0, fill_color=MUTED, fill_opacity=0.5).move_to(fs).align_to(fs, LEFT)
        fst = T("FS başlığı", 14, TXT).move_to(fsh)
        fsl = T("çerçeveleme alt katmanı çerçevesi", 18, MUTED).next_to(fs, UP, buff=0.1)
        self.play(Create(fs), FadeIn(fsh), FadeIn(fst), FadeIn(fsl), run_time=0.7)
        self.play(xg.animate.scale(0.9).move_to(fs.get_center() + RIGHT * 0.4), run_time=0.7)
        self.at(self.cues[1])
        cws = VGroup()
        for i in range(3):
            d = Rectangle(width=2.7, height=0.7, stroke_width=0, fill_color=WHITE, fill_opacity=0.75)
            p = Rectangle(width=0.4, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).next_to(d, RIGHT, buff=0)
            cws.add(VGroup(d, p, T("216 B veri", 16, BG, BOLD).move_to(d), T("32", 14, BG, BOLD).move_to(p)))
        cws.arrange(RIGHT, buff=0.12).move_to(DOWN * 0.4)
        cwl = T("RS(248,216) kod sözcükleri: 216 B veri + 32 B eşlik", 20, GOLD, BOLD).next_to(cws, DOWN, buff=0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cws], lag_ratio=0.2), run_time=1.2)
        self.at(self.cues[2])
        self.play(FadeIn(cwl), *[Indicate(c[1], color=GOLD, scale_factor=1.2) for c in cws], run_time=1.0)
        self.end(pad=0.05)

        self.beat("r12c")
        eff = VGroup(Rectangle(width=10.0 * 216 / 248, height=0.6, stroke_width=0, fill_color=CH[1], fill_opacity=0.85),
                     Rectangle(width=10.0 * 32 / 248, height=0.6, stroke_width=0, fill_color=GOLD, fill_opacity=0.95))
        eff[1].next_to(eff[0], RIGHT, buff=0)
        eff.move_to(DOWN * 2.3)
        el = VGroup(T("≈ 8,67 Gbit/s veri  (216/248 = %87,1)", 20, CH[1], BOLD).next_to(eff[0], UP, buff=0.1).align_to(eff, LEFT),
                    T("%12,9 FEC", 18, GOLD, BOLD).next_to(eff[1], UP, buff=0.1))
        self.at(self.cues[1] - 0.2)
        self.play(GrowFromEdge(eff[0], LEFT), GrowFromEdge(eff[1], LEFT), FadeIn(el), run_time=1.0)
        fec = pill("FEC desteği zorunlu · ↓ statik açık/kapalı · ↑ OLT dinamik kontrol", ACC, 19).to_edge(DOWN, buff=0.35)
        self.at(self.cues[3])
        self.play(FadeOut(VGroup(cwl)), FadeIn(fec, shift=UP * 0.1), self.set_src("G.989.3 §10.1.3, Ek B"), run_time=0.7)
        self.end(pad=0.1)

        # r13 — PMD as a meaning-agnostic converter
        self.beat("r13")
        self.clear(h)
        h = self.show_heading("PMD için bitlerin anlamı yoktur", h)
        bits_in = T("…0110 1001 1100…", 26, TXT, BOLD).move_to([-5.0, 0.2, 0])
        eo = box(1.7, 1.2, "E/O\nlazer", ACC, 20).move_to([-2.4, 0.2, 0])
        oe = box(1.7, 1.2, "O/E\nfotodiyot", ACC, 20).move_to([2.4, 0.2, 0])
        bits_out = T("…0110 1001 1100…", 26, TXT, BOLD).move_to([5.0, 0.2, 0])
        rng = np.random.default_rng(9)
        light = VMobject(color=WHITE, stroke_width=3).set_points_as_corners(nrz(rng.integers(0, 2, 22), -1.4, 0.13, -0.1, 0.5))
        a1 = Arrow(bits_in.get_right(), eo.get_left(), buff=0.1, color=MUTED, stroke_width=3)
        a2 = Arrow(oe.get_right(), bits_out.get_left(), buff=0.1, color=MUTED, stroke_width=3)
        ber = pill("koşul: BER ≤ referans seviyesi", GOLD, 20).move_to(DOWN * 1.6)
        self.at(self.cues[1])
        self.play(FadeIn(bits_in), GrowArrow(a1), FadeIn(eo), run_time=0.8)
        self.at(self.cues[4])
        self.play(Create(light), FadeIn(oe), GrowArrow(a2), FadeIn(bits_out), run_time=1.6)
        self.at(self.cues[6])
        self.play(FadeIn(ber, shift=UP * 0.15), run_time=0.6)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep01_p3D")


class P3E(Act):
    HDR, MANIFEST, PREV_BADGE = HDR3, MAN3, "tc"

    def construct(self):
        self.beat("r14")
        h = self.show_heading("BER referansı ve FEC")
        tb = table(["Hat hızı", "BER referansı", "FEC kodu", "Kaynak"],
                   [["2,48832 Gbit/s", "10⁻⁴", "RS(248,232)", "Tablo 11-4, 11-6"], ["9,95328 Gbit/s", "10⁻³", "RS(248,216)", "Tablo 11-5, 11-7"]],
                   [3.0, 2.6, 2.8, 3.4], size=22, hsize=18, row_h=0.62).move_to(UP * 0.6)
        self.at(self.cues[2] - 0.2)
        self.play(FadeIn(tb[0]), run_time=0.5)
        self.at(self.cues[5])
        self.play(FadeIn(tb[2], shift=UP * 0.1), run_time=0.6)
        self.at(self.cues[6])
        self.play(FadeIn(tb[1], shift=UP * 0.1), self.set_src("G.989.2 Tablo 11-4…11-7 · G.989.3 §10.1.3"), run_time=0.6)
        self.end(pad=0.05)

        # r15 — waterfall: pre-FEC vs post-FEC
        self.beat("r15")
        self.play(tb.animate.scale(0.7).to_corner(UR, buff=0.4).shift(DOWN * 0.7), run_time=0.6)
        ax = Axes(x_range=[0, 8, 1], y_range=[-14, -1, 1], x_length=7.0, y_length=4.4,
                  axis_config={"color": MUTED, "include_tip": False, "include_ticks": False}).move_to([-2.2, -1.0, 0])
        SUP = {-12: "10⁻¹²", -9: "10⁻⁹", -6: "10⁻⁶", -3: "10⁻³"}
        ylab = VGroup(*[T(SUP[v], 15, MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (-12, -9, -6, -3)])
        xl = T("alınan güç →  (göreli dB)", 16, MUTED).next_to(ax, DOWN, buff=0.15).align_to(ax, RIGHT)
        yl = T("BER (log)", 16, MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        q_of = lambda p: 10 ** ((p - 4.0) / 10) * 3.09  # Q ∝ optical power (thermal-noise limited); x=4 → BER 1e-3
        raw = lambda p: 0.5 * erfc(q_of(p) / np.sqrt(2))

        def post(p):
            ps = 1 - (1 - raw(p)) ** 8
            n, t = 248, 16
            pf = binom.sf(t, n, ps)
            return max(pf * (t + 1) / n * ps / max(ps, 1e-30) * 0.5 + 1e-16, 1e-16)
        xs = np.linspace(0, 8, 160)
        rc = VMobject(color=WARN, stroke_width=3.5).set_points_smoothly([ax.c2p(x, np.clip(np.log10(raw(x)), -14, -1)) for x in xs])
        pc = VMobject(color=GOOD, stroke_width=3.5).set_points_smoothly([ax.c2p(x, np.clip(np.log10(post(x)), -14, -1)) for x in xs if np.log10(post(x)) > -14.2])
        ref = DashedLine(ax.c2p(0, -3), ax.c2p(8, -3), color=GOLD, stroke_width=2.5)
        rl = T("referans: 10⁻³ (FEC öncesi)", 16, GOLD, BOLD).next_to(ax.c2p(8, -3), UL, buff=0.05)
        lg = VGroup(T("— ham (FEC öncesi)", 17, WARN, BOLD), T("— FEC sonrası", 17, GOOD, BOLD), T("temsili eğriler", 14, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lg.next_to(ax, RIGHT, buff=0.3).shift(DOWN * 0.6)
        self.play(Create(ax), FadeIn(ylab), FadeIn(xl), FadeIn(yl), run_time=0.7)
        self.play(Create(rc), FadeIn(lg[0]), FadeIn(lg[2]), run_time=1.2)
        self.play(Create(ref), FadeIn(rl), run_time=0.6)
        self.at(self.cues[4] - 0.2)
        self.play(Create(pc), FadeIn(lg[1]), run_time=1.4)
        vline = DashedLine(ax.c2p(4, -3), ax.c2p(4, np.log10(post(4))), color=WHITE, stroke_width=2)
        vt = T("≈ 10⁻¹²" if np.log10(post(4)) < -11 else "≈ 10⁻¹¹", 18, GOOD, BOLD).next_to(ax.c2p(4, np.log10(post(4))), RIGHT, buff=0.1)
        self.at(self.cues[9])
        self.play(Create(vline), FadeIn(vt), run_time=0.8)
        self.end(pad=0.05)

        # r16 — what you measure without FEC
        self.beat("r16")
        x12 = next(x for x in np.linspace(4, 8, 400) if raw(x) < 1e-12)
        p12 = Dot(ax.c2p(x12, -12), color=WARN, radius=0.08)
        gap = DoubleArrow(ax.c2p(4, -12.6), ax.c2p(x12, -12.6), buff=0, color=WHITE, stroke_width=2.5, tip_length=0.15)
        gt = T(f"≈ {x12 - 4:.1f} dB fark (temsili)", 17, WHITE, BOLD).next_to(gap, DOWN, buff=0.08)
        self.at(self.cues[2])
        self.play(FadeIn(p12, scale=1.5), Create(gap), FadeIn(gt), run_time=1.0)
        warn = pill("FEC'siz 10⁻¹² ≠ G.989.2 hassasiyeti", WARN, 19).move_to([4.4, -2.5, 0])
        self.at(self.cues[4] - 0.2)
        self.play(FadeIn(warn, shift=UP * 0.15), run_time=0.6)
        nxt = T("→ Bölüm 5: Ayarlanabilir Kulak", 20, ACC, BOLD).next_to(warn, DOWN, buff=0.25)
        self.at(self.cues[5])
        self.play(FadeIn(nxt), run_time=0.5)
        self.end(pad=0.1)
        self.clear()
        self.save_timeline("ep01_p3E")


class P3F(Act):
    HDR, MANIFEST, PREV_BADGE = HDR3, MAN3, "tc"

    def construct(self):
        self.beat("r17")
        h = self.show_heading("Üç yönetim kanalı")
        chans = VGroup(card("Gömülü OAM", "çerçeve başlık alanları\nburst zamanlama · bant tahsisi", None, CH[1], w=4.0, h=2.0, tsize=24, bsize=18),
                       card("PLOAM", "mesaj tabanlı kanal\nkanal ayarı · güç seviyesi", None, CH[0], w=4.0, h=2.0, tsize=24, bsize=18),
                       card("OMCC", "OMCI mesajları\nservis katmanlarının yönetimi", None, GOLD, w=4.0, h=2.0, tsize=24, bsize=18)
                       ).arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        tgt1 = RoundedRectangle(corner_radius=0.12, width=8.3, height=0.7, stroke_color=ACC, stroke_width=2.5, fill_color=ACC, fill_opacity=0.15)
        tgt1 = VGroup(tgt1, T("PMD + TC katmanlarının yönetimi", 20, ACC, BOLD).move_to(tgt1)).next_to(chans[:2], DOWN, buff=0.6)
        tgt2 = RoundedRectangle(corner_radius=0.12, width=4.0, height=0.7, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.15)
        tgt2 = VGroup(tgt2, T("üst katmanlar (servis)", 20, GOLD, BOLD).move_to(tgt2)).next_to(chans[2], DOWN, buff=0.6)
        ar = VGroup(*[Arrow(c.get_bottom(), [c.get_x(), (tgt1 if i < 2 else tgt2).get_top()[1], 0], buff=0.05, color=MUTED, stroke_width=3) for i, c in enumerate(chans)])
        self.at(self.cues[2] - 0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chans], lag_ratio=0.35), self.set_src("G.989.3 §6.1.4"), run_time=2.0)
        self.at(self.cues[4])
        self.play(Create(ar[:2]), FadeIn(tgt1), run_time=0.8)
        self.play(Create(ar[2]), FadeIn(tgt2), run_time=0.6)
        self.end(pad=0.05)

        # r18 — AMCC for uncalibrated ONU discovery
        self.beat("r18")
        self.clear(h)
        h = self.show_heading("Kalibre olmamış ONU ve AMCC", h)
        ax = Line([-5.5, -0.3, 0], [3.5, -0.3, 0], color=MUTED, stroke_width=2)
        xs = [-4.4, -2.4, -0.4, 1.6]
        chs = VGroup(*[FunctionGraph(lambda x, c=c: -0.3 + 1.6 * np.exp(-((x - c) / 0.18) ** 2), x_range=[c - 0.7, c + 0.7], color=CH[i], stroke_width=3.5)
                       for i, c in enumerate(xs)])
        cl = VGroup(*[T(f"λ{i + 1}′", 18, CH[i]).next_to([c, -0.3, 0], DOWN, buff=0.12) for i, c in enumerate(xs)])
        cap = T("çalışan yukarı yön kanalları", 18, MUTED).next_to(ax, UP, buff=1.9).align_to(ax, LEFT)
        self.play(Create(ax), LaggedStart(*[Create(c) for c in chs], lag_ratio=0.15), FadeIn(cl), FadeIn(cap), run_time=1.2)
        pos = ValueTracker(-1.5)
        rogue = always_redraw(lambda: FunctionGraph(lambda x: -0.3 + 1.3 * np.exp(-((x - pos.get_value()) / 0.22) ** 2),
                                                    x_range=[pos.get_value() - 0.8, pos.get_value() + 0.8], color=WARN, stroke_width=4))
        rl = T("kalibre olmamış ONU: dalga boyu belirsiz", 19, WARN, BOLD).move_to([-2.9, 2.05, 0])
        self.at(self.cues[1])
        self.add(rogue)
        self.play(FadeIn(rl), pos.animate.set_value(-2.1), run_time=1.0)
        self.play(pos.animate.set_value(-0.9), run_time=1.2, rate_func=there_and_back)
        self.at(self.cues[2])
        self.play(Flash([-2.4, 0.9, 0], color=WARN, flash_radius=0.35), chs[1].animate.set_stroke(opacity=0.4), run_time=0.8)
        olt = box(1.6, 1.0, "OLT CT", "#3B4A75", 18).move_to([5.6, 1.2, 0])
        amcc = DashedLine([-0.9, 1.7, 0], olt.get_left(), color=GOLD, stroke_width=3, dash_length=0.1)
        at = T("AMCC: düşük hızlı yardımcı kanal\nSerial_Number_ONU mesajı", 17, GOLD, BOLD).move_to([4.6, 0.35, 0])
        self.at(self.cues[4])
        self.play(FadeIn(olt), Create(amcc), FadeIn(at), self.set_src("G.989.3 §6.1.4.2"), run_time=1.2)
        self.at(self.cues[6])
        nx = T("→ Bölüm 7 ve 8", 20, ACC, BOLD).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(nx), run_time=0.5)
        self.end(pad=0.1)
        rogue.clear_updaters()

        # r18a — ONU state machine teaser
        self.beat("r18a")
        self.clear(h)
        h = self.show_heading("ONU durum makinesi (G.989.3 §12.1)", h)
        states = [("O1", "Başlangıç"), ("O2-3", "Seri numarası"), ("O4", "Ranging"), ("O5", "Çalışma")]
        nodes = VGroup(*[VGroup(Circle(radius=0.62, color=ACC, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                                T(a, 22, ACC, BOLD), T(b, 14, TXT)) for a, b in states])
        for n in nodes:
            n[1].move_to(n[0]).shift(UP * 0.12); n[2].next_to(n[1], DOWN, buff=0.04)
        nodes.arrange(RIGHT, buff=1.0).move_to(UP * 0.5)
        arr = VGroup(*[Arrow(nodes[i][0].get_right(), nodes[i + 1][0].get_left(), buff=0.05, color=MUTED, stroke_width=3) for i in range(3)])
        tun = VGroup(*[VGroup(Circle(radius=0.62, color=GOLD, stroke_width=3, fill_color=PANEL, fill_opacity=1), T(a, 22, GOLD, BOLD), T(b, 13, TXT))
                       for a, b in [("O8", "↓ ayar"), ("O9", "↑ ayar")]])
        for n in tun:
            n[1].move_to(n[0]).shift(UP * 0.12); n[2].next_to(n[1], DOWN, buff=0.04)
        tun.arrange(RIGHT, buff=1.2).next_to(nodes[3], DOWN, buff=1.0).shift(LEFT * 1.0)
        loop = VGroup(CurvedArrow(nodes[3][0].get_bottom() + LEFT * 0.2, tun[0][0].get_top(), angle=-0.6, color=GOLD, stroke_width=3),
                      Arrow(tun[0][0].get_right(), tun[1][0].get_left(), buff=0.05, color=GOLD, stroke_width=3),
                      CurvedArrow(tun[1][0].get_top(), nodes[3][0].get_bottom() + RIGHT * 0.2, angle=-0.6, color=GOLD, stroke_width=3))
        other = T("(ayrıca O6 kesintili LODS,\nO7 acil durdurma)", 16, MUTED).move_to([-4.2, -1.7, 0])
        self.at(self.cues[2] - 0.2)
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes], lag_ratio=0.25), Create(arr), self.set_src("G.989.3 §12.1"), run_time=1.8)
        self.at(self.cues[5])
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in tun], lag_ratio=0.3), Create(loop), FadeIn(other), run_time=1.6)
        nx = pill("kanal değişimi = O8/O9 → ayar süresi ölçümü (Bölüm 7)", GOLD, 18).next_to(tun, DOWN, buff=0.35)
        self.at(self.cues[8])
        self.play(FadeIn(nx), run_time=0.6)
        self.end(pad=0.1)

        self.engineer_note("r19", [("1", "Her parametrenin üç bağlamı vardır",
                                    "Hangi BER referansı? Hangi hat hızı? FEC varsayımı ne?", 1),
                                   ("2", "En sık hata",
                                    "Farklı referanslara göre verilmiş datasheet değerlerini\nyan yana karşılaştırmak.", 4)])
        self.beat("r20")
        self.clear()
        self.drop_badge()
        b = self.bridge("Sıradaki", "G.989.2'nin referans mimarisinde hangi kutular var,\nve ölçümü tam olarak nerede yapıyoruz?")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.9)
        self.end(pad=0.4)
        self.play(FadeOut(b), run_time=0.5)
        self.save_timeline("ep01_p3F")
