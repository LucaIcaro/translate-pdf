import fitz

from .extract import PageContent
from .fonts import load_font


_MIN_FONT_SIZE = 4
_MAX_SCALE_TRIES = 20


def _fit_font_size(
    font: fitz.Font,
    text: str,
    box_width: float,
    max_size: float,
    min_size: float = _MIN_FONT_SIZE,
) -> float:
    if not text or box_width <= 0:
        return min_size

    lo, hi = min_size, max(max_size, min_size)
    best = min_size

    for _ in range(_MAX_SCALE_TRIES):
        mid = (lo + hi) / 2.0
        w = font.text_length(text, fontsize=mid)
        if w <= box_width:
            best = mid
            lo = mid
        else:
            hi = mid
        if hi - lo < 0.1:
            break

    return best


def generate_pdf(
    input_pdf: str,
    output_pdf: str,
    page_contents: list[PageContent],
    transliterated_spans: list[list[tuple[str, str]]],
) -> None:
    doc = fitz.open(input_pdf)
    font_obj = load_font()

    for page_idx, page in enumerate(doc):
        if page_idx >= len(page_contents):
            continue
        content = page_contents[page_idx]
        spans_for_page = (
            transliterated_spans[page_idx]
            if page_idx < len(transliterated_spans)
            else []
        )

        dirties: list[tuple] = []
        for span_idx, span in enumerate(content.text_spans):
            if span_idx >= len(spans_for_page):
                continue
            _, iast_text = spans_for_page[span_idx]
            if iast_text == span.text:
                continue
            dirties.append((span, iast_text))

        if not dirties:
            continue

        redact_rects = fitz.Rect()
        for span, _ in dirties:
            page.add_redact_annot(fitz.Rect(span.bbox), fill=(1, 1, 1))
            redact_rects = redact_rects | fitz.Rect(span.bbox)

        page.apply_redactions()

        page.insert_font(fontname="F0", fontbuffer=font_obj.buffer)

        for span, iast_text in dirties:
            bbox = fitz.Rect(span.bbox)
            fit_size = _fit_font_size(
                font_obj, iast_text, bbox.width, span.font_size
            )
            page.insert_text(
                fitz.Point(span.origin[0], span.origin[1]),
                iast_text,
                fontname="F0",
                fontsize=fit_size,
                color=(0, 0, 0),
            )

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
