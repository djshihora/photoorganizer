from photo_organizer.cluster import cluster_faces, group_by_face


def test_cluster_faces_assigns_ids():
    meta = [
        {
            "path": "a.jpg",
            "exif": {},
            "faces": [
                {"embedding": [0.0] * 128},
                {"embedding": [0.0] * 128},
            ],
        },
        {
            "path": "b.jpg",
            "exif": {},
            "faces": [
                {"embedding": [1.0] * 128},
            ],
        },
    ]
    result = cluster_faces(meta, eps=1.0, min_samples=1)
    for entry in result:
        for face in entry["faces"]:
            assert "cluster_id" in face
            assert isinstance(face["cluster_id"], int)


def test_group_by_face_groups_entries():
    metadata = [
        {
            "path": "a.jpg",
            "faces": [
                {"cluster_id": 0},
                {"cluster_id": 1},
            ],
        },
        {
            "path": "b.jpg",
            "faces": [
                {"cluster_id": 1},
            ],
        },
    ]
    groups = group_by_face(metadata)
    assert set(groups.keys()) == {0, 1}
    assert groups[0] == [metadata[0]]
    assert groups[1] == [metadata[0], metadata[1]]


def test_group_by_face_empty():
    assert group_by_face([]) == {}
