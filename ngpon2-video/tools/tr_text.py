"""Turkish text preparation for XTTS (it normalises far less than Gemini): numbers/units → words, ≤200-char chunks."""
import re

_ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
_BIG = [(10 ** 12, "trilyon"), (10 ** 9, "milyar"), (10 ** 6, "milyon"), (1000, "bin")]


def int_tr(n: int) -> str:
    if n == 0:
        return "sıfır"
    if n < 0:
        return "eksi " + int_tr(-n)
    out = []
    for v, name in _BIG:
        if n >= v:
            q, n = divmod(n, v)
            out.append(name if (v == 1000 and q == 1) else f"{int_tr(q)} {name}")
    if n >= 100:
        q, n = divmod(n, 100)
        out.append("yüz" if q == 1 else f"{_ONES[q]} yüz")
    if n >= 10:
        out.append(_TENS[n // 10]); n %= 10
    if n:
        out.append(_ONES[n])
    return " ".join(out)


def num_tr(s: str) -> str:
    """'12,5' → 'on iki virgül beş'; '1.244.160' → integer with Turkish thousands dots; leading zeros kept digit-wise."""
    s = s.replace(".", "") if re.fullmatch(r"\d{1,3}(\.\d{3})+", s) else s
    if "," in s:
        a, b = s.split(",", 1)
        frac = " ".join(int_tr(int(c)) for c in b) if b.startswith("0") else int_tr(int(b))
        return f"{int_tr(int(a))} virgül {frac}"
    return int_tr(int(s))


UNITS = [("THz", "terahertz"), ("GHz", "gigahertz"), ("MHz", "megahertz"), ("kHz", "kilohertz"), ("Gbit/s", "gigabit bölü saniye"),
         ("µs", "mikrosaniye"), ("ns", "nanosaniye"), ("ps", "pikosaniye"), ("nm", "nanometre"), ("km", "kilometre"), ("dBm", "de be em"), ("dB", "desibel")]


def normalize_tr(text: str) -> str:
    t = re.sub(r"%\s?(\d+(?:,\d+)?)", lambda m: "yüzde " + num_tr(m.group(1)), text)
    t = re.sub(r"[−–-](?=\d)", "eksi ", t)
    t = re.sub(r"\+(?=\d)", "artı ", t)
    for u, w in UNITS:
        t = re.sub(rf"(?<=\d)\s?{re.escape(u)}\b", " " + w, t)
    t = re.sub(r"(?<=[A-Za-zÇĞİÖŞÜçğıöşü])(?=\d)", " ", t)  # PON2 → PON 2 → "PON iki"
    t = re.sub(r"\d{1,3}(?:\.\d{3})+|\d+(?:,\d+)?", lambda m: num_tr(m.group(0)), t)
    return re.sub(r"\s+", " ", t).strip()


def split_tr(text: str, limit: int = 200):
    """Sentences, then clause boundaries, then words — every chunk ≤ limit characters."""
    chunks = []
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if len(sent) <= limit:
            chunks.append(sent); continue
        parts, cur = re.split(r"(?<=[;:,])\s+", sent), ""
        for p in parts:
            if len(p) > limit:
                for w in p.split():
                    cur = (cur + " " + w).strip() if len(cur) + len(w) + 1 <= limit else (chunks.append(cur) or w)
            elif len(cur) + len(p) + 1 <= limit:
                cur = (cur + " " + p).strip()
            else:
                chunks.append(cur); cur = p
        if cur:
            chunks.append(cur)
    chunks = [c for c in chunks if c]
    # XTTS invents syllables on very short inputs ("PMD Köprüsü." came out as "PMD Köprüsü dondu"):
    # pack short neighbouring chunks together, up to the limit, so no chunk is shorter than MIN_CHUNK when avoidable.
    packed = []
    for c in chunks:
        if packed and (len(packed[-1]) < MIN_CHUNK or len(c) < MIN_CHUNK) and len(packed[-1]) + 1 + len(c) <= limit:
            packed[-1] = packed[-1] + " " + c
        else:
            packed.append(c)
    return packed


MIN_CHUNK = 80


if __name__ == "__main__":
    print(normalize_tr("6 GHz bandında %40 artış; 0,17 nm ve +11 dBm, −28 dBm, 1.244.160 bit, 125 µs."))
    print(split_tr("a" * 150 + ", " + "b" * 120 + ". Kısa cümle."))
