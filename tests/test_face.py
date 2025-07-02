from PIL import Image
from photo_organizer.face import (
    detect_faces,
    extract_face,
    load_embedder,
    FaceEmbedder,
)
import onnxruntime as ort


def test_detect_and_embed():
    # Create a simple blank image instead of loading one from disk
    img = Image.new("RGB", (10, 10))
    boxes = detect_faces(img)
    assert boxes, "no face detected"
    face_img = extract_face(img, boxes[0])
    embedder = load_embedder()
    emb = embedder(face_img)
    assert emb.shape[0] == 128


def test_face_embedder_failure(monkeypatch):
    def raise_session(*args, **kwargs):
        raise RuntimeError("fail")

    monkeypatch.setattr(ort, "InferenceSession", raise_session)

    img = Image.new("RGB", (10, 10))
    embedder = FaceEmbedder("bad.onnx")
    emb = embedder(img)
    assert emb.shape == (128,)
    assert emb.sum() == 0
