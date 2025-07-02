"""Image classification utilities for photo organizer."""

from __future__ import annotations

from typing import List
from PIL import Image

# Attempt to import torch and torchvision. If unavailable, we fall back to a
# dummy classifier so that the rest of the package remains functional even
# without the heavy ML dependencies.
try:  # pragma: no cover - optional dependency
    import torch
    from torchvision import transforms
    from torchvision.models import (
        mobilenet_v2,
        MobileNet_V2_Weights,
    )
except Exception:  # pragma: no cover - handled gracefully
    torch = None  # type: ignore
    MobileNet_V2_Weights = None  # type: ignore
    transforms = None  # type: ignore

_classifier = None
_transform = None


def load_classifier() -> None:
    """Load a pretrained MobileNet model if available."""
    global _classifier, _transform
    if _classifier is not None:
        return None

    if torch is None or MobileNet_V2_Weights is None:
        _classifier = None
        _transform = None
        return None

    try:  # pragma: no cover - relies on torch/torchvision
        weights = MobileNet_V2_Weights.DEFAULT
        model = mobilenet_v2(weights=weights)
        model.eval()
        _transform = weights.transforms()
        _classifier = model
    except Exception:  # pragma: no cover - any failure results in dummy mode
        _classifier = None
        _transform = None


_CATEGORY_KEYWORDS = {
    "selfie": ["person", "face", "portrait"],
    "document": ["document", "binder", "envelope", "notebook"],
    "screenshot": ["screen", "monitor", "web site", "website", "webpage"],
    "nature": [
        "tree",
        "flower",
        "mountain",
        "valley",
        "lake",
        "ocean",
        "sea",
        "forest",
    ],
}


def _map_label_to_category(label: str) -> str:
    label = label.lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in label:
                return category
    return "other"


def classify_image(img: Image.Image) -> str:
    """Return a coarse image category for *img*."""
    if _classifier is None:
        load_classifier()

    if _classifier is not None and transforms is not None and torch is not None:
        try:  # pragma: no cover - runtime inference
            tensor = _transform(img).unsqueeze(0)
            with torch.no_grad():
                logits = _classifier(tensor)
            idx = int(logits.argmax(1).item())
            label = MobileNet_V2_Weights.DEFAULT.meta["categories"][idx]
            return _map_label_to_category(label)
        except Exception:
            pass

    # Fallback heuristic: if the image is mostly green, consider it nature.
    try:
        small = img.convert("RGB").resize((32, 32))
        data = list(small.getdata())
        greens = sum(p[1] for p in data)
        reds = sum(p[0] for p in data)
        blues = sum(p[2] for p in data)
        if greens > reds and greens > blues:
            return "nature"
    except Exception:
        pass

    return "other"


__all__ = ["load_classifier", "classify_image"]
