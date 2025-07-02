import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image  # noqa: E402
from photo_organizer.face import (  # noqa: E402
    detect_faces,
    extract_face,
    load_embedder,
)


def test_detect_and_embed():
    # Create a simple blank image instead of loading one from disk
    img = Image.new("RGB", (10, 10))
    boxes = detect_faces(img)
    assert boxes, "no face detected"
    face_img = extract_face(img, boxes[0])
    embedder = load_embedder()
    emb = embedder(face_img)
    assert emb.shape[0] == 128
