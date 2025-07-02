import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json  # noqa: E402
from PIL import Image  # noqa: E402
from photo_organizer.db import init_db, insert_metadata  # noqa: E402


def test_insert_and_retrieve_metadata(tmp_path):
    img_path = tmp_path / "img.jpg"
    Image.new("RGB", (5, 5)).save(img_path)
    entry = {"path": str(img_path), "exif": {"key": "value"}}
    conn = init_db(str(tmp_path / "photo.db"))
    insert_metadata(conn, [entry])
    row = conn.execute(
        "SELECT metadata FROM photos WHERE path=?", (str(img_path),)
    ).fetchone()
    assert row is not None
    meta = json.loads(row[0])
    assert meta == entry["exif"]
