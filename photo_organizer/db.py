"""SQLite database utilities for photo organizer."""

from __future__ import annotations

import sqlite3
import json
from typing import Dict, Iterable

SCHEMA = """
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    metadata TEXT
);
"""


def init_db(path: str = "photo.db") -> sqlite3.Connection:
    """Initialize and return a database connection."""
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def insert_metadata(
    conn: sqlite3.Connection, metadata: Iterable[Dict[str, str]]
) -> None:
    """Insert scanned metadata into the database."""
    with conn:
        for entry in metadata:
            conn.execute(
                "INSERT OR REPLACE INTO photos(path, metadata) VALUES (?, ?)",
                (entry["path"], json.dumps(entry["exif"])),
            )


__all__ = ["init_db", "insert_metadata"]
