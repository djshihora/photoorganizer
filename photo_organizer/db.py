"""SQLite database utilities for photo organizer."""

from __future__ import annotations

import sqlite3
import json
from typing import Dict, Iterable, Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    metadata TEXT
);
CREATE TABLE IF NOT EXISTS face_labels (
    cluster_id INTEGER PRIMARY KEY,
    name TEXT
);
"""


def init_db(path: str = "photo.db") -> sqlite3.Connection:
    """Initialize and return a database connection."""
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def insert_metadata(
    conn: sqlite3.Connection, metadata: Iterable[Dict[str, Any]]
) -> None:
    """Insert scanned metadata into the database."""
    with conn:
        for entry in metadata:
            conn.execute(
                "INSERT OR REPLACE INTO photos(path, metadata) VALUES (?, ?)",
                (entry["path"], json.dumps(entry)),
            )


def set_face_label(
    conn: sqlite3.Connection,
    cluster_id: int,
    name: str,
) -> None:
    """Associate a name with a face ``cluster_id`` in the database."""
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO face_labels(cluster_id, name) "
            "VALUES (?, ?)",
            (cluster_id, name),
        )


__all__ = ["init_db", "insert_metadata", "set_face_label"]
