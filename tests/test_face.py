import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image
from photo_organizer.face import detect_faces, extract_face, load_embedder


def test_detect_and_embed():
    img_path = Path(__file__).with_name('data').joinpath('lena.jpg')
    img = Image.open(img_path)
    boxes = detect_faces(img)
    assert boxes, 'no face detected'
    face_img = extract_face(img, boxes[0])
    embedder = load_embedder()
    emb = embedder(face_img)
    assert emb.shape[0] == 128
