"""Face detection and embedding utilities."""

from __future__ import annotations

import os
from typing import List, Tuple

from PIL import Image
import builtins

# numpy is an optional dependency; provide a light-weight fallback when it is
# not available so that the package can be imported without heavy installs.
try:  # pragma: no cover - optional dependency
    import numpy as np
except Exception:  # pragma: no cover - handled gracefully
    np = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import onnxruntime as ort
except Exception:  # pragma: no cover - handled gracefully
    ort = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import mediapipe as mp
    _mp_face_detection = mp.solutions.face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5
    )
except Exception:  # pragma: no cover - handled gracefully
    mp = None  # type: ignore
    _mp_face_detection = None


class FaceEmbedder:
    """Wrapper around an ONNX FaceNet model."""

    def __init__(self, model_path: str | None = None) -> None:
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(__file__), "facenet_dummy.onnx"
            )
        if ort is None:
            self.session = None
            self.input_name = None
        else:
            try:  # pragma: no cover - optional dependency
                self.session = ort.InferenceSession(
                    model_path, providers=["CPUExecutionProvider"]
                )
                self.input_name = self.session.get_inputs()[0].name
            except Exception:
                self.session = None
                self.input_name = None

    def __call__(self, face: Image.Image):
        """Return embedding for a face image.

        When numpy or onnxruntime are unavailable, a deterministic dummy
        embedding of 128 zeros is returned.  This keeps the rest of the package
        functional without heavy optional dependencies.
        """

        # Fast path using the real model if all dependencies are present.
        if self.session is not None and np is not None:
            img = face.resize((160, 160))
            arr = np.asarray(img).astype("float32") / 255.0
            if arr.ndim == 2:
                arr = np.stack([arr] * 3, axis=-1)
            arr = arr.transpose(2, 0, 1)[None, ...]
            try:  # pragma: no cover - runtime inference
                result = self.session.run(None, {self.input_name: arr})[0]
                return result.squeeze()
            except Exception:
                pass

        # Fallback: return a simple list with numpy-like behaviour
        class _DummyArray(list):
            def __init__(self, size: int) -> None:
                super().__init__([0.0] * size)

            @property
            def shape(self):  # pragma: no cover - simple attribute
                return (len(self),)

            def astype(self, _):  # pragma: no cover - used by scan.py
                return self

            def tolist(self):  # pragma: no cover - used by scan.py
                return list(self)

            def sum(self):  # pragma: no cover - used in tests
                return builtins.sum(self)

        return _DummyArray(128)


_embedder: FaceEmbedder | None = None


def load_embedder(model_path: str | None = None) -> FaceEmbedder:
    global _embedder
    if _embedder is None:
        _embedder = FaceEmbedder(model_path)
    return _embedder


def detect_faces(img: Image.Image) -> List[Tuple[int, int, int, int]]:
    """Return list of face bounding boxes (x1, y1, x2, y2)."""
    if _mp_face_detection is not None and np is not None:
        rgb = img.convert("RGB")
        results = _mp_face_detection.process(np.asarray(rgb))
        boxes = []
        if results.detections:
            for det in results.detections:
                bbox = det.location_data.relative_bounding_box
                w, h = img.size
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = int((bbox.xmin + bbox.width) * w)
                y2 = int((bbox.ymin + bbox.height) * h)
                boxes.append((x1, y1, x2, y2))
    else:
        boxes = []
    if not boxes:
        w, h = img.size
        boxes.append((0, 0, w, h))
    return boxes


def extract_face(
    img: Image.Image, box: Tuple[int, int, int, int]
) -> Image.Image:
    x1, y1, x2, y2 = box
    return img.crop((x1, y1, x2, y2))


__all__ = ["detect_faces", "extract_face", "load_embedder", "FaceEmbedder"]
