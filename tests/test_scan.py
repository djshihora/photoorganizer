import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from photo_organizer.scan import scan_folder
from PIL import Image


def test_scan_folder(tmp_path):
    img_path = tmp_path / "image.jpg"
    Image.new("RGB", (10, 10)).save(img_path)

    metadata = scan_folder(str(tmp_path))
    assert len(metadata) == 1
    assert metadata[0]["path"] == str(img_path)
    assert isinstance(metadata[0]["exif"], dict)
