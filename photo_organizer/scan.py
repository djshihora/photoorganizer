"""Scanning utilities for photo organizer."""

from __future__ import annotations

import os
from fractions import Fraction
from typing import Dict, Iterable, List, Tuple
from PIL import Image, ExifTags
from .face import detect_faces, extract_face, load_embedder
from .classifier import classify_image
from .ocr import extract_text
from .location import resolve_location


def _gps_to_decimal(
    coords: Tuple[Fraction, Fraction, Fraction], ref: str
) -> float | None:
    """Convert GPS coordinates to decimal degrees."""
    try:
        d, m, s = [float(x) for x in coords]
        result = d + m / 60 + s / 3600
        if ref in {"S", "W"}:
            result = -result
        return result
    except Exception:
        return None


def _extract_exif(image: Image.Image) -> Dict[str, str]:
    """Extract timestamp, GPS, and camera metadata from PIL image."""
    exif_data: Dict[str, str] = {}
    info = image.getexif()

    gps_raw = None
    for tag_id, value in info.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        if (
            tag in {"DateTimeOriginal", "DateTime"}
            and "timestamp" not in exif_data
        ):
            exif_data["timestamp"] = str(value)
        elif tag == "Make":
            exif_data["camera_make"] = str(value)
        elif tag == "Model":
            exif_data["camera_model"] = str(value)
        elif tag == "GPSInfo":
            gps_raw = value

    if gps_raw:
        gps_parsed = {
            ExifTags.GPSTAGS.get(k, k): v for k, v in gps_raw.items()
        }
        lat = _gps_to_decimal(
            gps_parsed.get("GPSLatitude"), gps_parsed.get("GPSLatitudeRef")
        )
        lon = _gps_to_decimal(
            gps_parsed.get("GPSLongitude"), gps_parsed.get("GPSLongitudeRef")
        )
        if lat is not None and lon is not None:
            exif_data["gps"] = f"{lat},{lon}"

    if "camera_make" in exif_data or "camera_model" in exif_data:
        make = exif_data.get("camera_make", "").strip()
        model = exif_data.get("camera_model", "").strip()
        camera = " ".join(x for x in [make, model] if x)
        exif_data["camera"] = camera

    return exif_data


def find_images(
    folder: str, extensions: Iterable[str] | None = None
) -> List[str]:
    """Recursively collect image file paths within *folder*."""
    if extensions is None:
        extensions = {".jpg", ".jpeg", ".png"}
    else:
        extensions = {
            e.lower() if e.startswith(".") else f".{e.lower()}"
            for e in extensions
        }

    paths: List[str] = []
    for root, _, files in os.walk(folder):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in extensions:
                paths.append(os.path.join(root, name))
    return paths


def scan_folder(folder: str) -> List[Dict[str, str]]:
    """Scan folder for images and return metadata list."""
    metadata: List[Dict[str, str]] = []
    embedder = load_embedder()
    for path in find_images(folder):
        faces_info = []
        category = "other"
        text = ""
        try:
            with Image.open(path) as img:
                exif = _extract_exif(img)
                location_info = {}
                if "gps" in exif:
                    try:
                        lat_str, lon_str = exif["gps"].split(",")
                        location_info = resolve_location(
                            float(lat_str), float(lon_str)
                        )
                    except Exception:
                        location_info = {}
                category = classify_image(img)
                if category in {"document", "id"}:
                    text = extract_text(img)
                boxes = detect_faces(img)
                for box in boxes:
                    face_img = extract_face(img, box)
                    embedding = embedder(face_img).astype(float).tolist()
                    faces_info.append(
                        {"box": list(box), "embedding": embedding}
                    )
        except Exception:
            exif = {}
            location_info = {}
        entry = {
            "path": path,
            "exif": exif,
            "faces": faces_info,
            "category": category,
            "ocr_text": text,
        }
        entry.update(location_info)
        metadata.append(entry)
    return metadata


__all__ = ["scan_folder", "find_images"]
