from photo_organizer.events import group_by_event, name_event, rename_event


def test_group_by_event_assigns_ids_and_groups():
    metadata = [
        {
            "path": "a.jpg",
            "exif": {"timestamp": "2023:01:01 10:00:00"},
            "faces": [],
            "category": "other",
        },
        {
            "path": "b.jpg",
            "exif": {"timestamp": "2023:01:01 12:00:00"},
            "faces": [],
            "category": "other",
        },
        {
            "path": "c.jpg",
            "exif": {"timestamp": "2023:01:02 00:00:00"},
            "faces": [],
            "category": "other",
        },
    ]

    events = group_by_event(metadata, gap_hours=6)
    assert set(events.keys()) == {0, 1}
    assert [e["event_id"] for e in events[0]] == [0, 0]
    assert [e["event_id"] for e in events[1]] == [1]


def test_name_and_rename_event():
    metadata = [
        {
            "path": "a.jpg",
            "exif": {"timestamp": "2023:01:01 10:00:00"},
            "faces": [],
            "category": "other",
        }
    ]
    events = group_by_event(metadata)
    name_event(events, 0, "Birthday")
    assert events[0][0]["event_name"] == "Birthday"
    rename_event(events, 0, "Party")
    assert events[0][0]["event_name"] == "Party"
