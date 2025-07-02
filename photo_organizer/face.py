"""Face detection and embedding utilities."""
from __future__ import annotations

import os
from typing import List, Tuple

import numpy as np
import onnxruntime as ort
from PIL import Image
import mediapipe as mp


# Initialize MediaPipe face detector
_mp_face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)


class FaceEmbedder:
    """Wrapper around an ONNX FaceNet model."""

    def __init__(self, model_path: str | None = None) -> None:
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "facenet_dummy.onnx")
        try:
            self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
            self.input_name = self.session.get_inputs()[0].name
        except Exception:
            self.session = None
            self.input_name = None

    def __call__(self, face: Image.Image) -> np.ndarray:
        """Return embedding for a face image."""
        img = face.resize((160, 160))
        arr = np.asarray(img).astype("float32") / 255.0
        if arr.ndim == 2:
            arr = np.stack([arr] * 3, axis=-1)
        arr = arr.transpose(2, 0, 1)[None, ...]
        if self.session is None:
            return np.zeros(128, dtype=np.float32)
        result = self.session.run(None, {self.input_name: arr})[0]
        return result.squeeze()


_embedder: FaceEmbedder | None = None

def load_embedder(model_path: str | None = None) -> FaceEmbedder:
    global _embedder
    if _embedder is None:
        _embedder = FaceEmbedder(model_path)
    return _embedder


def detect_faces(img: Image.Image) -> List[Tuple[int, int, int, int]]:
    """Return list of face bounding boxes (x1, y1, x2, y2)."""
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
    if not boxes:
        w, h = img.size
        boxes.append((0, 0, w, h))
    return boxes


def extract_face(img: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
    x1, y1, x2, y2 = box
    return img.crop((x1, y1, x2, y2))


__all__ = ["detect_faces", "extract_face", "load_embedder", "FaceEmbedder"]
