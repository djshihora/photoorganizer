from PIL import Image
import json
from cli import main
from photo_organizer.db import init_db


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
