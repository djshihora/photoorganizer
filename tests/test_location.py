from photo_organizer.location import resolve_location, group_by_location


def test_resolve_location_offline():
    loc = resolve_location(40.7128, -74.0060)
    assert loc == {
        "city": "New York",
        "state": "New York",
        "country": "United States",
    }


def test_group_by_location():
    metadata = [
        {
            "path": "a.jpg",
            "city": "New York",
            "state": "New York",
            "country": "United States",
        },
        {
            "path": "b.jpg",
            "city": "New York",
            "state": "New York",
            "country": "United States",
        },
        {
            "path": "c.jpg",
            "city": "San Francisco",
            "state": "California",
            "country": "United States",
        },
    ]
    by_city = group_by_location(metadata, level="city")
    assert set(by_city.keys()) == {"New York", "San Francisco"}
    assert len(by_city["New York"]) == 2
    by_state = group_by_location(metadata, level="state")
    assert set(by_state.keys()) == {"New York", "California"}
    assert len(by_state["California"]) == 1
