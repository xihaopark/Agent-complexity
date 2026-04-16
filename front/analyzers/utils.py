from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from common.events import ArtifactRef


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def to_artifact_ref(path: Path, artifact_type: str) -> ArtifactRef:
    return ArtifactRef(
        artifact_type=artifact_type,
        uri=str(path),
        sha256=file_sha256(path) if path.exists() and path.is_file() else None,
        size=path.stat().st_size if path.exists() and path.is_file() else None,
    )
