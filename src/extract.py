from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import fitz


@dataclass
class TextSpan:
    text: str
    font: str
    font_size: float
    bbox: Tuple[float, float, float, float]
    origin: Tuple[float, float]


@dataclass
class ImageBlock:
    bbox: Tuple[float, float, float, float]
    image_index: int


@dataclass
class PageContent:
    page_number: int
    text_spans: List[TextSpan] = field(default_factory=list)
    images: List[ImageBlock] = field(default_factory=list)
    page_width: float = 0
    page_height: float = 0


def extract_page_content(page: fitz.Page) -> PageContent:
    content = PageContent(
        page_number=page.number + 1,
        page_width=page.rect.width,
        page_height=page.rect.height,
    )

    text_dict = page.get_text("dict")

    for block in text_dict.get("blocks", []):
        if block.get("type") == 0:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    content.text_spans.append(
                        TextSpan(
                            text=text,
                            font=span.get("font", ""),
                            font_size=span.get("size", 12),
                            bbox=tuple(span.get("bbox", (0, 0, 0, 0))),
                            origin=tuple(span.get("origin", (0, 0))),
                        )
                    )

        elif block.get("type") == 1:
            content.images.append(
                ImageBlock(
                    bbox=tuple(block.get("bbox", (0, 0, 0, 0))),
                    image_index=block.get("number", 0),
                )
            )

    return content


def extract_all_content(pdf_path: str) -> List[PageContent]:
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(extract_page_content(page))
    doc.close()
    return pages
