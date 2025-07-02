"""OCR utilities for document images."""

from __future__ import annotations

from PIL import Image

try:  # pragma: no cover - optional dependency
    import pytesseract
except Exception:  # pragma: no cover - handled gracefully
    pytesseract = None  # type: ignore


def extract_text(img: Image.Image) -> str:
    """Return text from *img* using Tesseract if available."""
    if pytesseract is None:
        return ""
    try:  # pragma: no cover - runtime OCR
        return pytesseract.image_to_string(img)
    except Exception:
        return ""


__all__ = ["extract_text"]
