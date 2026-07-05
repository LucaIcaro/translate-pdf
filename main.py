import argparse
import sys
from pathlib import Path

from src.extract import extract_all_content
from src.transliterate import transliterate_text
from src.generate import generate_pdf
from src.fonts import font_available


def main():
    parser = argparse.ArgumentParser(
        description="Transliterate Devanagari PDF text to IAST (Latin script)"
    )
    parser.add_argument("-i", "--input", required=True, help="Input PDF path")
    parser.add_argument("-o", "--output", default="output.pdf", help="Output PDF path")
    parser.add_argument(
        "-t", "--translate", action="store_true",
        help="Enable translation pass (uses stub; requires future LLM agent)",
    )
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not font_available():
        print(
            "Error: DejaVu Sans font not found.\n"
            "Install it with: sudo apt install fonts-dejavu-core",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Extracting text from {args.input}...")
    page_contents = extract_all_content(args.input)
    print(f"  Found {len(page_contents)} pages")

    total_spans = sum(len(pc.text_spans) for pc in page_contents)
    print(f"  Found {total_spans} text spans")

    print("Transliterating Devanagari to IAST...")
    transliterated = []
    for pc in page_contents:
        spans_for_page = []
        for span in pc.text_spans:
            iast = transliterate_text(span.text)
            spans_for_page.append((span.text, iast))
        transliterated.append(spans_for_page)

    changed = sum(1 for row in transliterated for orig, new in row if orig != new)
    print(f"  Transliterated {changed} spans")

    if args.translate:
        from src.translate import DummyTranslator
        translator = DummyTranslator()
        print("Translation pass (stub): LLM translation not yet implemented.")

    print(f"Generating output PDF: {args.output}...")
    generate_pdf(args.input, args.output, page_contents, transliterated)
    print("Done!")


if __name__ == "__main__":
    main()
