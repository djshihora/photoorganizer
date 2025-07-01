"""Scanning utilities for photo organizer."""
from __future__ import annotations

import os
from typing import Dict, Iterable, List
from PIL import Image, ExifTags


def _extract_exif(image: Image.Image) -> Dict[str, str]:
    """Extract EXIF data from PIL image."""
    exif_data = {}
    info = image.getexif()
    for tag_id, value in info.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        exif_data[str(tag)] = str(value)
    return exif_data


def scan_folder(folder: str) -> List[Dict[str, str]]:
    """Scan folder for images and return metadata list."""
    supported = {".jpg", ".jpeg", ".png"}
    metadata = []
    for root, _, files in os.walk(folder):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in supported:
                path = os.path.join(root, name)
                try:
                    with Image.open(path) as img:
                        exif = _extract_exif(img)
                except Exception:
                    exif = {}
                entry = {
                    "path": path,
                    "exif": exif,
                }
                metadata.append(entry)
    return metadata

__all__ = ["scan_folder"]
