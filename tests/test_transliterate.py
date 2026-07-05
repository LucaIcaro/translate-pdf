import sys
sys.path.insert(0, "/home/luca/translate-pdf")

from src.transliterate import transliterate_text, has_devanagari


def test_has_devanagari():
    assert has_devanagari("संस्कृतम्") is True
    assert has_devanagari("English text") is False
    assert has_devanagari("मिश्रित text") is True
    assert has_devanagari("") is False


def test_transliterate_simple():
    result = transliterate_text("संस्कृतम्")
    assert "saṃskṛtam" in result


def test_transliterate_common_words():
    cases = [
        ("नमः", "namaḥ"),
        ("शिव", "śiva"),
        ("राम", "rāma"),
        ("कृष्ण", "kṛṣṇa"),
        ("धर्म", "dharma"),
    ]
    for dev, expected in cases:
        result = transliterate_text(dev)
        assert result.lower() == expected.lower(), f"{dev} → {result}, expected {expected}"


def test_non_devanagari_passthrough():
    text = "Verse 1.2.3"
    assert transliterate_text(text) == text


def test_mixed_content():
    result = transliterate_text("श्लोक १")
    assert "śloka" in result.lower()
    assert "1" in result or "१" in result


def test_empty_string():
    assert transliterate_text("") == ""
