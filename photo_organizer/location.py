"""Location utilities using geopy with offline fallback."""

from __future__ import annotations

from typing import Iterable, List, Dict

try:
    from geopy.geocoders import Nominatim
except Exception:  # pragma: no cover - geopy not installed
    Nominatim = None  # type: ignore

# Simple offline coordinate mapping for tests and offline use
OFFLINE_LOCATIONS: Dict[tuple[float, float], Dict[str, str]] = {
    (40.7128, -74.0060): {
        "city": "New York",
        "state": "New York",
        "country": "United States",
    },
    (37.7749, -122.4194): {
        "city": "San Francisco",
        "state": "California",
        "country": "United States",
    },
}


def _offline_lookup(lat: float, lon: float) -> Dict[str, str]:
    key = (round(lat, 4), round(lon, 4))
    return OFFLINE_LOCATIONS.get(key, {})


def resolve_location(lat: float, lon: float) -> Dict[str, str]:
    """Resolve *lat* and *lon* to a city/state/country dictionary."""
    if Nominatim is not None:
        try:
            geolocator = Nominatim(user_agent="photo_organizer")
            location = geolocator.reverse((lat, lon), language="en", timeout=5)
            if location and "address" in location.raw:
                addr = location.raw["address"]
                return {
                    "city": addr.get("city")
                    or addr.get("town")
                    or addr.get("village"),
                    "state": addr.get("state"),
                    "country": addr.get("country"),
                }
        except Exception:
            pass
    return _offline_lookup(lat, lon)


def group_by_location(
    metadata: Iterable[Dict[str, str]], level: str = "city"
) -> Dict[str, List[Dict[str, str]]]:
    """Group metadata entries by a location level."""
    groups: Dict[str, List[Dict[str, str]]] = {}
    for entry in metadata:
        key = entry.get(level)
        if key:
            groups.setdefault(key, []).append(entry)
    return groups


__all__ = ["resolve_location", "group_by_location"]
