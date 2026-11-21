"""Arabic text helpers: normalisation and fuzzy similarity (spelling/dialect tolerant)."""
import re
from rapidfuzz import fuzz

_TASHKEEL = re.compile(r"[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed\u0640]")
_ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
AR = re.compile(r"[\u0600-\u06FF]")
# things speech models invent over music or silence
JUNK = ["اشتركوا في القناة", "ترجمة نانسي قنقر", "شكرا للمشاهدة", "لا تنسوا الاشتراك", "موسيقى", "تصفيق", "subscribe", "thanks for watching", "music", "applause"]


def normalize(s: str) -> str:
    """Remove vowel marks and unify letter variants (أ/إ/آ->ا, ة->ه, ى->ي ...)."""
    s = _TASHKEEL.sub("", _ZERO_WIDTH.sub("", s))
    s = re.sub("[إأآٱ]", "ا", s)
    s = re.sub("[ىیے]", "ي", s)
    s = re.sub("[ةۀ]", "ه", s)
    s = s.replace("ؤ", "و").replace("ئ", "ي")
    s = re.sub("[کگ]", "ك", s)
    return re.sub(r"\s+", " ", _PUNCT.sub(" ", s)).strip().lower()


def phonetic(s: str) -> str:
    """Looser form: letters that dialects and sites swap are merged (ذ/ز/ظ/ض, ث/ت, ص/س, ط/ت, ق/ا)."""
    s = normalize(s)
    s = re.sub("[ذزظض]", "د", s)
    return s.replace("ث", "ت").replace("ص", "س").replace("ط", "ت").replace("ق", "ا")


def similarity(a: str, b: str) -> float:
    """0..1. Also high when one text is contained in the other (a half-line vs a full line)."""
    a, b = phonetic(a), phonetic(b)
    if not a or not b:
        return 0.0
    s = fuzz.ratio(a, b)
    if min(len(a), len(b)) >= 8:
        s = max(s, 0.95 * fuzz.partial_ratio(a, b))
    return s / 100.0


def is_junk(text: str) -> bool:
    n = normalize(text)
    if not n or not AR.search(text):
        return True
    w = n.split()
    if len(w) >= 6 and len(set(w)) <= 2:      # runaway repetition loop
        return True
    return any(normalize(j) == n for j in JUNK)


def lyric_lines(text: str) -> list[str]:
    """Lyrics text (pasted or from a page) -> clean lines."""
    out = []
    for raw in re.split(r"[\r\n]+", text):
        raw = re.sub(r"\s+", " ", re.sub(r"[#*_>`~|\[\]]+", " ", raw)).strip()
        if len(AR.findall(raw)) < 3 or len(raw) > 160 or "http" in raw:
            continue
        parts = [p.strip(" .،؛-") for p in re.split(r"\.{2,}|\s{3,}|\t+", raw)]
        out.extend(p for p in parts if len(AR.findall(p)) >= 3)
    return out
