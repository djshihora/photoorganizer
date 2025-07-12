"""Event grouping utilities for photo organizer."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Any


def group_by_event(
    metadata: Iterable[Dict[str, Any]], gap_hours: int = 6
) -> Dict[int, List[Dict[str, Any]]]:
    """Group metadata entries into events separated by *gap_hours*.

    Each entry must have ``entry["exif"]["timestamp"]`` in the format
    ``YYYY:MM:DD HH:MM:SS``. Entries are sorted by this timestamp and a new
    event is started whenever the time gap between consecutive photos exceeds
    ``gap_hours``. The ``event_id`` field is added to each entry. The returned
    dictionary maps event IDs to the corresponding list of entries.
    """
    items: List[tuple[datetime, Dict[str, Any]]] = []
    for entry in metadata:
        ts_str = entry.get("exif", {}).get("timestamp")
        if ts_str is None:
            continue
        try:
            dt = datetime.strptime(ts_str, "%Y:%m:%d %H:%M:%S")
        except Exception:
            continue
        items.append((dt, entry))

    items.sort(key=lambda x: x[0])

    events: Dict[int, List[Dict[str, Any]]] = {}
    last_dt: datetime | None = None
    event_id = 0
    for dt, entry in items:
        if last_dt is None or dt - last_dt > timedelta(hours=gap_hours):
            event_id = len(events)
            events[event_id] = []
        entry["event_id"] = event_id
        events[event_id].append(entry)
        last_dt = dt

    return events


def name_event(event_map: Dict[int, List[Dict[str, Any]]], event_id: int, name: str) -> None:
    """Assign a human-friendly *name* to an event."""
    for entry in event_map.get(event_id, []):
        entry["event_name"] = name


def rename_event(
    event_map: Dict[int, List[Dict[str, Any]]], event_id: int, new_name: str
) -> None:
    """Change the human-friendly name for an event."""
    name_event(event_map, event_id, new_name)


__all__ = ["group_by_event", "name_event", "rename_event"]
