import json
from PIL import Image
from photo_organizer.db import init_db, insert_metadata


def test_insert_and_retrieve_metadata(tmp_path):
    img_path = tmp_path / "img.jpg"
    Image.new("RGB", (5, 5)).save(img_path)
    entry = {
        "path": str(img_path),
        "exif": {"key": "value"},
        "faces": [],
    }
    conn = init_db(str(tmp_path / "photo.db"))
    insert_metadata(conn, [entry])
    row = conn.execute(
        "SELECT metadata FROM photos WHERE path=?", (str(img_path),)
    ).fetchone()
    assert row is not None
    meta = json.loads(row[0])
    assert meta == entry


def test_init_db_creates_table(tmp_path):
    db_file = tmp_path / "db.sqlite"
    conn = init_db(str(db_file))
    assert db_file.exists()
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='photos'"
    ).fetchone()
    assert row is not None


def test_insert_metadata_multiple(tmp_path):
    img1 = tmp_path / "a.jpg"
    img2 = tmp_path / "b.jpg"
    Image.new("RGB", (5, 5)).save(img1)
    Image.new("RGB", (5, 5)).save(img2)
    db_file = tmp_path / "db.sqlite"
    conn = init_db(str(db_file))
    entries = [
        {"path": str(img1), "exif": {"n": "1"}, "faces": []},
        {"path": str(img2), "exif": {"n": "2"}, "faces": []},
    ]
    insert_metadata(conn, entries)
    rows = list(conn.execute("SELECT path FROM photos ORDER BY path"))
    assert [r[0] for r in rows] == [str(img1), str(img2)]
