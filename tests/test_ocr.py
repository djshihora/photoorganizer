from PIL import Image
from photo_organizer.scan import scan_folder


def test_ocr_text_extraction(monkeypatch, tmp_path):
    img_path = tmp_path / "doc.jpg"
    Image.new("RGB", (10, 10)).save(img_path)

    monkeypatch.setattr(
        "photo_organizer.scan.classify_image", lambda img: "document"
    )
    monkeypatch.setattr(
        "photo_organizer.scan.extract_text", lambda img: "hello"
    )

    meta = scan_folder(str(tmp_path))
    assert meta[0]["ocr_text"] == "hello"
