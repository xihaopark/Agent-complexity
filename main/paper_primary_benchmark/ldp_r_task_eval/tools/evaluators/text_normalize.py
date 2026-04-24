"""Tolerant text normalization for the V2 evaluator.

The goal is to declare two text blobs "equal" when they only differ in
cosmetic/whitespace ways (BOM, CRLF, trailing whitespace, trailing blank
lines) or when they are semantically the same JSON document.
"""

from __future__ import annotations

import json
from pathlib import Path

_BOM = "\ufeff"


def normalize_text(text: str) -> str:
    """Strip BOM, unify line endings, drop trailing whitespace/blank lines."""
    if text.startswith(_BOM):
        text = text[len(_BOM):]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def try_json_canonical(text: str) -> str | None:
    """Parse text as JSON and return a deterministic canonical form.

    Returns ``None`` if the text is not a valid JSON document.
    """
    try:
        obj = json.loads(text)
    except Exception:
        return None
    try:
        return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        return None


def normalized_text_equal(agent_path: Path, ref_path: Path) -> tuple[bool, str]:
    """Return (True/False, reason)."""
    try:
        a = agent_path.read_text(encoding="utf-8", errors="replace")
        b = ref_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # pragma: no cover - defensive
        return False, f"read_failed:{e}"

    na = normalize_text(a)
    nb = normalize_text(b)
    if na == nb:
        return True, "normalized_text_equal"

    ja = try_json_canonical(a)
    jb = try_json_canonical(b)
    if ja is not None and jb is not None and ja == jb:
        return True, "normalized_json_equal"

    return False, "not_equal"
