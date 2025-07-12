"""CLI entry point for photo organizer."""

from __future__ import annotations

import argparse

from photo_organizer.scan import scan_folder
from photo_organizer.cluster import cluster_faces
from photo_organizer.db import init_db, insert_metadata
from photo_organizer.picker import pick_folder
from photo_organizer.location import group_by_location
from photo_organizer.events import group_by_event
import json


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Photo Organizer CLI")
    parser.add_argument("folder", nargs="?", help="Folder to scan for photos")
    parser.add_argument(
        "--db", default="photo.db", help="SQLite database path"
    )
    parser.add_argument(
        "--group-by",
        choices=["city", "state", "country"],
        help="Group results by location level",
    )
    parser.add_argument(
        "--group-events",
        nargs="?",
        const=6,
        default=None,
        type=int,
        metavar="HOURS",
        help="Group photos into events separated by HOURS gap (default: 6)",
    )

    ns = parser.parse_args(args)

    folder = ns.folder or pick_folder()
    print(f"Scanning {folder}...")
    metadata = scan_folder(folder)
    # ensure every entry contains a category so downstream steps
    # like database insertion and tests can rely on this key
    for entry in metadata:
        entry.setdefault("category", "other")
    cluster_faces(metadata)
    if ns.group_events is not None:
        event_groups = group_by_event(metadata, gap_hours=ns.group_events)
        print(json.dumps(event_groups))
    elif ns.group_by:
        groups = group_by_location(metadata, level=ns.group_by)
        print(json.dumps(groups))
    else:
        print(json.dumps(metadata))
    conn = init_db(ns.db)
    insert_metadata(conn, metadata)
    print(f"Inserted {len(metadata)} records into {ns.db}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
