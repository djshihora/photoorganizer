"""Face clustering utilities."""

from __future__ import annotations

from typing import List, Dict, Any, Iterable

import numpy as np
from sklearn.cluster import DBSCAN


def cluster_faces(
    metadata: List[Dict[str, Any]],
    eps: float = 0.5,
    min_samples: int = 3,
) -> List[Dict[str, Any]]:
    """Assign cluster labels to faces across *metadata*.

    This iterates over all face embeddings, performs DBSCAN clustering,
    and sets ``face["cluster_id"]`` for each face dictionary. The function
    returns the input list for convenience.
    """
    embeddings: List[List[float]] = []
    faces: List[Dict[str, Any]] = []
    for entry in metadata:
        for face in entry.get("faces", []):
            if "embedding" in face:
                embeddings.append(face["embedding"])
                faces.append(face)

    if embeddings:
        arr = np.array(embeddings)
        labels = DBSCAN(eps=eps, min_samples=min_samples).fit(arr).labels_
        for face, label in zip(faces, labels):
            face["cluster_id"] = int(label)
    return metadata


def group_by_face(
    metadata: Iterable[Dict[str, Any]]
) -> Dict[int, List[Dict[str, Any]]]:
    """Group metadata entries by face ``cluster_id``.

    Each entry may be included in multiple groups if it contains faces from
    different clusters. Entries without any faces labeled with a cluster ID are
    ignored.
    """

    groups: Dict[int, List[Dict[str, Any]]] = {}
    for entry in metadata:
        seen: set[int] = set()
        for face in entry.get("faces", []):
            cid = face.get("cluster_id")
            if isinstance(cid, int) and cid not in seen:
                groups.setdefault(cid, []).append(entry)
                seen.add(cid)
    return groups


__all__ = ["cluster_faces", "group_by_face"]
