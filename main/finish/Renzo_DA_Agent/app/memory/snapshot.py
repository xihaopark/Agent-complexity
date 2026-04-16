from __future__ import annotations

import json
import os
from typing import Any, Dict


def save_snapshot(state: Dict[str, Any], snapshot_dir: str, version: int) -> str:
    os.makedirs(snapshot_dir, exist_ok=True)
    path = os.path.join(snapshot_dir, f"state_{version}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
    return path


def load_snapshot(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
