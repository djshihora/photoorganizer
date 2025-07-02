from PIL import Image
from photo_organizer.scan import scan_folder, find_images, _extract_exif


def test_scan_folder(tmp_path):
    img_path = tmp_path / "image.jpg"
    Image.new("RGB", (10, 10)).save(img_path)

    metadata = scan_folder(str(tmp_path))
    assert len(metadata) == 1
    assert metadata[0]["path"] == str(img_path)
    assert isinstance(metadata[0]["exif"], dict)
    assert "faces" in metadata[0]
    assert isinstance(metadata[0]["faces"], list)


def test_extract_exif_invalid_gps():
    class DummyImg:
        def getexif(self):
            return {
                "GPSInfo": {
                    "GPSLatitude": ("a", "b", "c"),
                    "GPSLatitudeRef": "N",
                    "GPSLongitude": ("d", "e", "f"),
                    "GPSLongitudeRef": "E",
                }
            }

    exif = _extract_exif(DummyImg())
    assert "gps" not in exif


def test_find_images_custom_extensions(tmp_path):
    (tmp_path / "a.TIFF").write_text("x")
    (tmp_path / "b.jpeg").write_text("x")
    (tmp_path / "c.txt").write_text("x")

    paths = set(find_images(str(tmp_path), extensions=["tiff", ".JPEG"]))
    expected = {str(tmp_path / "a.TIFF"), str(tmp_path / "b.jpeg")}
    assert paths == expected

    none_found = find_images(str(tmp_path), extensions=[".gif"])
    assert none_found == []
