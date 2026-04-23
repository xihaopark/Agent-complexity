#!/usr/bin/env python3
"""Validate r_tasks registry JSON against on-disk task workspaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_LDP_EVAL = Path(__file__).resolve().parent.parent
_PAPER_PB = _LDP_EVAL.parent
_DEFAULT_REG = _LDP_EVAL / "r_tasks" / "registry.json"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--registry",
        default=str(_DEFAULT_REG),
        help="Path to registry JSON",
    )
    p.add_argument(
        "--kind",
        choices=["auto", "full", "sample50"],
        default="auto",
        help="auto: infer from filename / task count; full: pilot + mixed stubs/ready; "
        "sample50: exactly 50 ready micro-eval tasks",
    )
    args = p.parse_args()

    reg_path = Path(args.registry).resolve()
    if not reg_path.is_file():
        print("ERROR: registry not found:", reg_path, file=sys.stderr)
        sys.exit(1)

    data = json.loads(reg_path.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])
    errs: list[str] = []

    kind = args.kind
    if kind == "auto":
        if "sample_50" in reg_path.name or (
            len(tasks) == 50 and not any(t.get("id") == "pilot_hello" for t in tasks)
        ):
            kind = "sample50"
        else:
            kind = "full"

    if kind == "sample50":
        if len(tasks) != 50:
            errs.append(f"sample50: expected 50 tasks, got {len(tasks)}")
        ready = [t for t in tasks if t.get("status") == "ready"]
        if len(ready) != 50:
            errs.append(f"sample50: expected 50 ready, got {len(ready)}")
        for t in tasks:
            if t.get("status") != "ready":
                errs.append(f"sample50: task {t.get('id')!r} not ready")
            _check_workspace(t, errs, require_micro_eval=True)
    else:
        pilot = [t for t in tasks if t.get("id") == "pilot_hello"]
        if len(pilot) != 1:
            errs.append(f"expected exactly one pilot_hello, got {len(pilot)}")
        stubs = [t for t in tasks if t.get("status") == "stub"]
        ready = [t for t in tasks if t.get("status") == "ready"]
        if len(tasks) != 146:
            errs.append(f"expected 146 tasks total, got {len(tasks)}")
        if len(ready) < 1:
            errs.append("expected at least one ready task (pilot)")
        if len(stubs) + len(ready) != 146:
            errs.append("stub + ready should partition all tasks")
        for t in tasks:
            _check_workspace(t, errs, require_micro_eval=False)

    if errs:
        for e in errs:
            print("ERROR:", e, file=sys.stderr)
        sys.exit(1)

    print(f"OK: {len(tasks)} tasks ({kind})")
    print("   registry:", reg_path)


def _check_workspace(t: dict, errs: list[str], *, require_micro_eval: bool) -> None:
    tid = t.get("id")
    wid = t.get("work_dir")
    if not wid:
        errs.append(f"task {tid!r} missing work_dir")
        return
    root = _PAPER_PB / wid
    if not root.is_dir():
        errs.append(f"missing directory: {root} (id={tid})")
        return
    if not (root / "OBJECTIVE.md").is_file():
        errs.append(f"missing OBJECTIVE.md: {root / 'OBJECTIVE.md'} (id={tid})")
    if tid != "pilot_hello" and not (root / "meta.json").is_file():
        errs.append(f"missing meta.json: {root / 'meta.json'} (id={tid})")
    if t.get("status") == "stub":
        return
    if require_micro_eval:
        v = root / "input" / "values.txt"
        r = root / "evaluation" / "reference_sum.txt"
        if not v.is_file():
            errs.append(f"missing input/values.txt for {tid}")
        if not r.is_file():
            errs.append(f"missing evaluation/reference_sum.txt for {tid}")
        return
    # ready task in full registry: pilot has numbers; sample-prepared have values.txt
    meta_path = root / "meta.json"
    if not meta_path.is_file():
        return
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errs.append(f"invalid meta.json for {tid}")
        return
    if meta.get("sample_50") and meta.get("evaluation_ready"):
        v = root / "input" / "values.txt"
        if not v.is_file():
            errs.append(f"sample_50 ready but missing input/values.txt for {tid}")


if __name__ == "__main__":
    main()
