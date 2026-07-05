from indic_transliteration import sanscript
import re


_DEVANAGARI_RANGE = re.compile(r"[\u0900-\u097F]")


def has_devanagari(text: str) -> bool:
    return bool(_DEVANAGARI_RANGE.search(text))


def transliterate_text(text: str) -> str:
    if not has_devanagari(text):
        return text
    try:
        return sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception:
        return text
