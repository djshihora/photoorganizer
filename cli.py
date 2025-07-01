"""CLI entry point for photo organizer."""
from __future__ import annotations

import argparse

from photo_organizer.scan import scan_folder
from photo_organizer.db import init_db, insert_metadata


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Photo Organizer CLI")
    parser.add_argument("folder", help="Folder to scan for photos")
    parser.add_argument("--db", default="photo.db", help="SQLite database path")

    ns = parser.parse_args(args)

    print(f"Scanning {ns.folder}...")
    metadata = scan_folder(ns.folder)
    conn = init_db(ns.db)
    insert_metadata(conn, metadata)
    print(f"Inserted {len(metadata)} records into {ns.db}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
