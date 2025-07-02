from photo_organizer.cluster import cluster_faces


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
