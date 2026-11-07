"""Turkish read-aloud spellings for acronyms (applied only to the text sent to TTS; subtitles keep the original)."""
import re
LEX = [
    ("ITU-T", "ay ti yu ti"),
    ("NG-PON2", "en ci pon iki"), ("XGS-PON", "eks ci es pon"), ("XG-PON1", "eks ci pon bir"), ("XG-PON", "eks ci pon"), ("G-PON", "ci pon"), ("GPON", "ci pon"),
    (r"G\.989\.(\d)", lambda m: "ci dokuz sekiz dokuz nokta " + ["sıfır", "bir", "iki", "üç"][int(m.group(1))]),
    (r"G\.987\.3", "ci dokuz sekiz yedi nokta üç"), (r"G\.988", "ci dokuz sekiz sekiz"), (r"G\.989", "ci dokuz sekiz dokuz"),
    (r"\bAWG\b", "ey dabılyu ci"), (r"\bPLC\b", "pi el si"), (r"\bFBT\b", "ef bi ti"), (r"\bORL\b", "o ar el"), (r"\bOTDR\b", "o ti di ar"),
    (r"G\.652", "ci altı beş iki"), (r"L\.313", "el üç yüz on üç"), (r"\bDD20\b", "di di yirmi"), (r"\bDD40\b", "di di kırk"),
    (r"\bT eqd\b", "te e kü de"), (r"\bL min\b", "el min"), (r"\bD maks\b", "de maks"), (r"Ranging_Time", "renging taym"),
    ("PtP WDM", "pi tu pi dabılyu di em"), ("TWDM", "ti dabılyu di em"),
    ("WM'nin", "dabılyu em'in"), ("WM", "dabılyu em"),
    ("OMCI'yi", "o em si ay'ı"), ("OMCI", "o em si ay"), ("OMCC", "o em si si"), ("AMCC", "ey em si si"),
    ("PLOAM", "pi el o ey em"), ("OAM", "o ey em"), ("XGEM", "eks ci em"),
    ("OLT", "o el ti"), ("ONU", "o en yu"), ("ODN", "o di en"), ("PMD", "pi em di"), ("FEC", "fek"),
    ("NRZ", "en ar zi"), ("OSA'ya", "o es ey'e"), ("OSA", "o es ey"), ("DCA", "di si ey"), ("BERT", "bört"), ("VOA", "vi o ey"),
    ("SDH", "es di eyç"), (r"STM-(\d+)", lambda m: "es ti em " + {"64": "altmış dört", "16": "on altı"}[m.group(1)]),
    (r"\bRS\b", "ar es"), (r"\bRF\b", "ar ef"), (r"\bdBm\b", "de be em"), (r"\bTC\b", "ti si"),
    (r"\bCG\b", "si ci"), (r"\bCP\b", "si pi"),
    ("S bölü R", "es bölü ar"), ("R bölü S", "ar bölü es"),
    (r"\bS, ağa", "Es, ağa"), (r"\bR, ağdan", "Ar, ağdan"),
    (r"\bN1\b", "en bir"), (r"\bN2\b", "en iki"), (r"\bE1\b", "e bir"), (r"\bE2\b", "e iki"),
    (r"Stratum-(\d)", lambda m: "stratum " + ["sıfır", "bir", "iki", "üç", "dört"][int(m.group(1))]),
    (r"Tablo 11-5", "tablo on bir tire beş"), (r"Tablo 11-8", "tablo on bir tire sekiz"), (r"Şekil 11-4", "şekil on bir tire dört"),
    (r"\bO8\b", "o sekiz"), (r"\bO9\b", "o dokuz"),
    (r"\bCEx\b", "si i eks"), (r"8B10B", "sekiz bi on bi"), (r"\bMAC\b", "mek"), (r"\bDC\b", "di si"), (r"\bEML\b", "i em el"),
    (r"\bDFB\b", "di ef bi"), (r"\bTV\b", "ti vi"), (r"\bL bandı", "el bandı"), (r"\bC bandı", "si bandı"), (r"\bU bandı", "yu bandı"),
    (r"G\.694\.1", "ci altı dokuz dört nokta bir"), (r"G\.698\.3", "ci altı dokuz sekiz nokta üç"),
    (r"G\.Sup39", "ci ek otuz dokuz"), (r"G\.984\.2", "ci dokuz sekiz dört nokta iki"), (r"G\.783", "ci yedi sekiz üç"), (r"G\.825", "ci sekiz iki beş"),
    (r"G\.957", "ci dokuz beş yedi"), (r"G\.959\.1", "ci dokuz beş dokuz nokta bir"), (r"G\.987\.3", "ci dokuz sekiz yedi nokta üç"),
    (r"\bAPD", "a pe de"), (r"\bPIN\b", "pin"), (r"\bLODS", "lods"), (r"\bPSync", "pi sink"), (r"\bPSBd", "pi es bi di"), (r"\bHEC", "hek"),
    (r"BIP-32", "bip otuz iki"), (r"\bTO(\d)\b", lambda m: "te o " + ["sıfır","bir","iki","üç","dört","beş","altı"][int(m.group(1))]),
    (r"\bSMSR", "es em es ar"), (r"\bWNE\b", "dabılyu en i"), (r"\bEDC\b", "i di si"), (r"\bDCA'", "di si ey'"), (r"\bTOL\b", "tol"),
    (r"\bXGEM", "eks ci em"), (r"\bBCH\b", "bi si eyç"), (r"\bXOR", "eks or"), (r"\bOTN\b", "o ti en"), (r"\bQAM\b", "kuam"),
    (r"PON-ID", "pon ay di"), (r"\bDFB\b", "di ef bi"), (r"\bOMCI\b", "o em si ay"),
    # XTTS reads bare variable letters badly ("X bölü S" came out as "işitsel"): spell them out
    (r"\bX/S\b", "iks bölü es"), (r"\bX\b", "iks"), (r"\bS\b", "es"), (r"\bburst", "börst"),
]

def speak(text):
    for pat, rep in LEX:
        text = re.sub(pat, rep, text)
    return text

if __name__ == "__main__":
    import json, sys
    for b in json.load(open(sys.argv[1]))["beats"]:
        print(b["id"], speak(b["text"]))
