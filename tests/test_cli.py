from PIL import Image
import json
from cli import main
from photo_organizer.db import init_db

ALLOWED = {"selfie", "document", "screenshot", "nature", "other"}


def test_cli_main(tmp_path):
    img = Image.new("RGB", (5, 5))
    img_path = tmp_path / "img.jpg"
    img.save(img_path)
    db_path = tmp_path / "photo.db"
    ret = main([str(tmp_path), "--db", str(db_path)])
    assert ret == 0
    conn = init_db(str(db_path))
    row = conn.execute("SELECT metadata FROM photos").fetchone()
    assert row is not None
    meta = json.loads(row[0])
    assert meta["faces"]
    assert "cluster_id" in meta["faces"][0]
    assert "category" in meta
    assert isinstance(meta["category"], str)
    assert meta["category"] in ALLOWED


def test_cli_default_json_output(tmp_path, capsys):
    img = Image.new("RGB", (5, 5))
    img_path = tmp_path / "img.jpg"
    img.save(img_path)
    db_path = tmp_path / "photo.db"

    ret = main([str(tmp_path), "--db", str(db_path)])
    assert ret == 0
    out = capsys.readouterr().out
    json_line = [
        line
        for line in out.splitlines()
        if line.startswith("[") or line.startswith("{")
    ][0]
    data = json.loads(json_line)
    assert isinstance(data, list)
    assert data[0]["path"].endswith("img.jpg")


def test_cli_group_by(monkeypatch, tmp_path, capsys):
    img = Image.new("RGB", (5, 5))
    img_path = tmp_path / "img.jpg"
    img.save(img_path)
    db_path = tmp_path / "photo.db"

    monkeypatch.setattr(
        "photo_organizer.scan._extract_exif", lambda img: {"gps": "0,0"}
    )
    monkeypatch.setattr(
        "photo_organizer.scan.resolve_location",
        lambda lat, lon: {
            "city": "TestCity",
            "state": "TestState",
            "country": "TestCountry",
        },
    )

    ret = main([str(tmp_path), "--db", str(db_path), "--group-by", "city"])
    assert ret == 0
    out = capsys.readouterr().out
    json_line = [line for line in out.splitlines() if line.startswith("{")][0]
    groups = json.loads(json_line)
    assert "TestCity" in groups
    assert groups["TestCity"][0]["city"] == "TestCity"


def test_cli_group_events(monkeypatch, tmp_path, capsys):
    img1 = tmp_path / "a.jpg"
    img2 = tmp_path / "b.jpg"
    Image.new("RGB", (5, 5)).save(img1)
    Image.new("RGB", (5, 5)).save(img2)
    db_path = tmp_path / "photo.db"

    timestamps = ["2023:01:01 10:00:00", "2023:01:02 00:00:00"]

    def fake_exif(img):
        return {"timestamp": timestamps.pop(0)}

    monkeypatch.setattr("photo_organizer.scan._extract_exif", fake_exif)

    ret = main([str(tmp_path), "--db", str(db_path), "--group-events"])
    assert ret == 0
    out = capsys.readouterr().out
    json_line = [line for line in out.splitlines() if line.startswith("{")][0]
    groups = json.loads(json_line)
    assert set(groups.keys()) == {"0", "1"}

    conn = init_db(str(db_path))
    rows = conn.execute("SELECT metadata FROM photos").fetchall()
    event_ids = {json.loads(r[0])["event_id"] for r in rows}
    assert event_ids == {0, 1}
