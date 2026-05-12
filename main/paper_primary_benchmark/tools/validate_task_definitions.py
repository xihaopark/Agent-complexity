#!/usr/bin/env python3
"""Validate paper_primary_benchmark/task_definitions/*.json against finish/*/manifest.json.

Checks:
- JSON parses; optional JSON Schema if jsonschema is installed.
- manifest_path resolves under --main-root.
- Concatenation of tasks[].step_ids in task order equals manifest steps[].id order (full partition).
- task order fields are 1..N without duplicates.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _schema_validate(doc: dict[str, Any], schema_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema not installed; skipping schema validation (pip install jsonschema)"]
    schema = _load_json(schema_path)
    try:
        jsonschema.validate(instance=doc, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(f"schema: {e.message} at {list(e.path)}")
    return errors


def validate_one(
    main_root: Path,
    task_path: Path,
    schema_path: Path | None,
) -> list[str]:
    errors: list[str] = []
    try:
        doc = _load_json(task_path)
    except Exception as e:
        return [f"{task_path}: invalid JSON: {e}"]

    if schema_path and schema_path.is_file():
        errors.extend(_schema_validate(doc, schema_path))

    wid = doc.get("workflow_id")
    if not wid:
        errors.append("missing workflow_id")
        return errors

    mp = doc.get("manifest_path")
    if not isinstance(mp, str):
        errors.append("manifest_path must be a string")
        return errors

    manifest_path = main_root / mp
    if not manifest_path.is_file():
        errors.append(f"manifest not found: {manifest_path}")
        return errors

    try:
        manifest = _load_json(manifest_path)
    except Exception as e:
        errors.append(f"manifest JSON error: {e}")
        return errors

    expected = [str(s.get("id", "")) for s in manifest.get("steps", []) if s.get("id")]
    tasks = doc.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("tasks must be a non-empty array")
        return errors

    got: list[str] = []
    orders: list[int] = []
    for t in tasks:
        if not isinstance(t, dict):
            errors.append("each task must be an object")
            continue
        sids = t.get("step_ids")
        if not isinstance(sids, list) or not sids:
            errors.append(f"task {t.get('task_id')!r}: step_ids must be non-empty array")
            continue
        for sid in sids:
            got.append(str(sid))
        o = t.get("order")
        if isinstance(o, int):
            orders.append(o)

    if got != expected:
        errors.append(
            "step_ids concatenation != manifest steps order:\n"
            f"  expected ({len(expected)}): {expected[:12]}{'...' if len(expected) > 12 else ''}\n"
            f"  got      ({len(got)}): {got[:12]}{'...' if len(got) > 12 else ''}"
        )

    exp_orders = list(range(1, len(tasks) + 1))
    if sorted(orders) != exp_orders or len(orders) != len(tasks):
        errors.append(f"task order fields should be exactly {exp_orders}, got {sorted(orders)}")

    step_set = set(expected)
    flat = [x for t in tasks if isinstance(t, dict) for x in (t.get("step_ids") or [])]
    if len(flat) != len(set(flat)):
        errors.append("duplicate step_id across tasks")
    if set(flat) != step_set:
        errors.append("step_ids set != manifest step id set")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--main-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent,
        help="Path to main/ (contains finish/ and paper_primary_benchmark/)",
    )
    ap.add_argument(
        "--workflow-id",
        type=str,
        default="",
        help="If set, only validate task_definitions/<id>.json",
    )
    ap.add_argument(
        "--no-schema",
        action="store_true",
        help="Skip JSON Schema validation",
    )
    args = ap.parse_args()
    main_root = args.main_root.resolve()
    td = main_root / "paper_primary_benchmark" / "task_definitions"
    schema_path = td / "schema.json" if not args.no_schema else None

    if args.workflow_id:
        paths = [td / f"{args.workflow_id}.json"]
    else:
        paths = sorted(td.glob("*.json"))
        paths = [p for p in paths if p.name != "schema.json"]

    if not paths:
        print("No task definition files found.", file=sys.stderr)
        return 1

    failed = 0
    for p in paths:
        if not p.is_file():
            print(f"MISSING {p}", file=sys.stderr)
            failed += 1
            continue
        errs = validate_one(main_root, p, schema_path)
        if errs:
            print(f"FAIL {p.name}")
            for e in errs:
                print(f"  {e}")
            failed += 1
        else:
            print(f"OK   {p.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
