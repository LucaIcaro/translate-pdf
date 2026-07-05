# translate-pdf

Transliterate Devanagari (Sanskrit/Hindi) text in PDF files to IAST (International Alphabet of Sanskrit Transliteration) while preserving the original layout — including images, text positions, and font sizes.

## How it works

```
Input PDF (Devanagari)
        │
        ▼
┌─────────────────┐
│  1. Extract      │  PyMuPDF reads each page and extracts text spans
│                  │  with their bounding boxes, origin points, and font sizes.
│                  │  Image positions are also recorded (preserved as-is).
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Transliterate │  indic-transliteration converts Devanagari Unicode
│                    │  text to IAST (e.g., "संस्कृतम्" → "saṃskṛtam").
│                    │  Non-Devanagari text (numbers, English) passes through.
└────────┬──────────┘
         │
         ▼
┌─────────────────┐
│  3. Generate     │  For each page:
│                  │    a. Add white redaction annotations over original text
│                  │    b. Apply redactions (removes Devanagari text)
│                  │    c. Insert IAST text at the same baseline position
│                  │    d. If IAST text is wider than the original box,
│                  │       font size is reduced proportionally to fit
│                  │
│                  │  Images are left untouched — they remain exactly
│                  │  as in the original PDF.
└────────┬────────┘
         │
         ▼
Output PDF (IAST transliteration, same layout)
```

## Requirements

- Python 3.10+
- DejaVu Sans font (usually pre-installed; on Debian/Ubuntu: `fonts-dejavu-core`)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python setup_font.py   # verifies DejaVu Sans is available
```

## Usage

```bash
python main.py -i input.pdf -o output.pdf
```

### Options

| Flag | Description |
|------|-------------|
| `-i`, `--input` | Path to input PDF (required) |
| `-o`, `--output` | Path for output PDF (default: `output.pdf`) |
| `-t`, `--translate` | Enable translation pass (stub; for future LLM agent) |

## Project structure

```
translate-pdf/
├── main.py              # CLI entry point
├── requirements.txt
├── setup_font.py        # Verifies system font
├── src/
│   ├── extract.py       # PDF text/image extraction
│   ├── transliterate.py # Devanagari → IAST conversion
│   ├── fonts.py         # Font loading (DejaVu Sans)
│   ├── generate.py      # Output PDF generation with redaction + overlay
│   └── translate.py     # Translation stub (ABC + DummyTranslator)
└── tests/
    └── test_transliterate.py
```

## Translation (future)

A separate agent will add page-by-page LLM translation. The `src/translate.py` module provides a `Translator` ABC and a `DummyTranslator` placeholder. To integrate:

1. Implement `Translator.translate(text: str) -> TranslationResult`
2. Pass it to the pipeline in `main.py` when `--translate` is used

The `TranslationResult` dataclass contains `text` (original), `iast` (transliteration), and `translation` (English, optional).
