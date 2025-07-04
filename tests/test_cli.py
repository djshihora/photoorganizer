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
