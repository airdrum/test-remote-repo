"""Turkish read-aloud spellings for acronyms (applied only to the text sent to TTS; subtitles keep the original)."""
import re
LEX = [
    ("ITU-T", "ay ti yu ti"),
    ("NG-PON2", "en ci pon iki"), ("XGS-PON", "eks ci es pon"), ("XG-PON", "eks ci pon"), ("GPON", "ci pon"),
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
]

def speak(text):
    for pat, rep in LEX:
        text = re.sub(pat, rep, text)
    return text

if __name__ == "__main__":
    import json, sys
    for b in json.load(open(sys.argv[1]))["beats"]:
        print(b["id"], speak(b["text"]))
