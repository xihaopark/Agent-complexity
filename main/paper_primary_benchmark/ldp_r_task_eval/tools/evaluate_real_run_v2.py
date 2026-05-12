#!/usr/bin/env python3
"""V2 lenient evaluator for ldp R-task runs.

Inspired by BixBench, this scorer grades each expected file on a tiered ladder
(byte-identical → normalized text/JSON → canonical tabular form → tabular
tolerance → RDS semantic → process credit) and adds trajectory-level process
signals. See ``EVALUATION_V2.md`` for the full rubric.

Notable differences from V1 (``evaluate_real_run.py``, untouched):

* Output is per-file scores in ``[0, 1]`` plus four process booleans; an
  ``overall_score`` combines them as ``0.3 * mean(process) + 0.7 * mean(files)``.
* Verdicts: ``pass``, ``partial_pass``, ``partial_fail``, ``fail``, ``error``.
* ``--legacy`` replays the V1 verdict logic so runs can be compared
  apples-to-apples.
* JSON output always carries both ``verdict`` and ``verdict_legacy`` so
  downstream tools can migrate incrementally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from evaluators import (
    extract_process_signals,
    load_table,
    normalized_text_equal,
    tabular_tolerance_score,
)
from evaluators.tabular import canonical_tsv

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evaluate_real_run as _v1  # noqa: E402 -- sibling module, reused for legacy verdicts

_HERE = Path(__file__).resolve().parent
_LDP = _HERE.parent
_RUNS = _LDP / "runs"
_GT = _LDP / "tasks" / "real_ground_truth"
_REG = _LDP / "r_tasks" / "registry.real.json"
_DEFAULT_RDS_HELPER = _HERE / "evaluators" / "rds_sidecar.R"

EVALUATOR_VERSION = "v2.1"

_PROCESS_WEIGHT = 0.3
_FILE_WEIGHT = 0.7
_TEXT_EXT = {".txt", ".tsv", ".csv", ".json", ".md", ".log", ".bed", ".bedgraph", ".gff", ".gtf", ".vcf"}
_RDS_EXT = {".rds", ".RDS"}
# V2.1: remove the hard 0.5 floor that discarded continuous cell-match signal.
# Below this floor the file still earns credit, anchored at _PROCESS_CREDIT.
_PROCESS_CREDIT = 0.25
_MAX_TOLERANCE_SCORE = 0.99

_VERDICT_PASS = 0.90
_VERDICT_PARTIAL_PASS = 0.60
_VERDICT_PARTIAL_FAIL = 0.30


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class FileScore:
    filename: str
    expected_path: str
    got_path: str
    strategy_used: str = "missing"
    strategy_score: float = 0.0
    bytes_identical: bool = False
    size_agent: int | None = None
    size_ref: int | None = None
    notes: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "expected_path": self.expected_path,
            "got_path": self.got_path,
            "strategy_used": self.strategy_used,
            "strategy_score": round(self.strategy_score, 4),
            "bytes_identical": self.bytes_identical,
            "size_agent": self.size_agent,
            "size_ref": self.size_ref,
            "notes": self.notes,
            "details": self.details,
        }


def _clip(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, val))


def _rds_to_tsv(rds_path: Path, out_path: Path, helper: Path, timeout: int = 60) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["Rscript", "--vanilla", str(helper), str(rds_path), str(out_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        diag = (proc.stderr or "").strip().splitlines()[-1] if proc.stderr else ""
        if out_path.exists() and out_path.stat().st_size > 0:
            return True, diag or "ok"
        return False, diag or "empty_output"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except FileNotFoundError:
        return False, "rscript_missing"
    except Exception as e:  # pragma: no cover
        return False, f"exception:{e}"


def _score_tabular(df_a, df_b, rtol: float, atol: float) -> tuple[float, dict]:
    """Return (tolerance_score_in_0_to_1, diagnostic_dict).

    V2.1 ladder (no hard floor): we combine ``effective_fraction`` (a penalised
    multiset match) with ``cell_match_fraction`` (pure cell agreement under
    numeric tolerance) and map linearly to ``[0, 0.99]``. A separate
    ``_score_file`` step still anchors any present file at ``_PROCESS_CREDIT``.
    """
    stats = tabular_tolerance_score(df_a, df_b, rtol=rtol, atol=atol)
    eff = float(stats.get("effective_fraction", 0.0))
    cell_frac = float(stats.get("cell_match_fraction", 0.0))
    # Blend: effective_fraction captures shape+content; cell_match_fraction is
    # a schema-aligned sanity check. Take max to reward either signal.
    blended = max(eff, 0.85 * cell_frac)
    if blended >= 0.999:
        score = _MAX_TOLERANCE_SCORE
    else:
        score = _clip(blended, 0.0, _MAX_TOLERANCE_SCORE - 0.01)
    return score, stats


def _score_file(
    filename: str,
    agent_path: Path,
    ref_path: Path,
    *,
    rds_helper: Path,
    rtol: float,
    atol: float,
    scratch_dir: Path,
) -> FileScore:
    fs = FileScore(
        filename=filename,
        expected_path=str(ref_path),
        got_path=str(agent_path),
    )
    ref_exists = ref_path.is_file()
    agent_exists = agent_path.is_file()
    if not ref_exists:
        fs.strategy_used = "missing_reference"
        fs.notes.append("reference file not found")
        return fs
    fs.size_ref = ref_path.stat().st_size
    if not agent_exists:
        fs.strategy_used = "missing"
        return fs
    fs.size_agent = agent_path.stat().st_size

    try:
        if fs.size_agent == fs.size_ref and _sha256(agent_path) == _sha256(ref_path):
            fs.bytes_identical = True
            fs.strategy_used = "byte_identical"
            fs.strategy_score = 1.0
            return fs
    except Exception as e:
        fs.notes.append(f"sha256_failed:{e}")

    ext = agent_path.suffix.lower()
    is_text_like = ext in _TEXT_EXT or ext == ""
    best_score = 0.0
    best_strategy = "fail"
    best_details: dict = {}

    if is_text_like:
        equal, reason = normalized_text_equal(agent_path, ref_path)
        if equal:
            fs.strategy_used = reason
            fs.strategy_score = 1.0
            return fs
        df_a = load_table(agent_path)
        df_b = load_table(ref_path)
        if df_a is not None and df_b is not None:
            try:
                if canonical_tsv(df_a) == canonical_tsv(df_b):
                    fs.strategy_used = "normalized_table_equal"
                    fs.strategy_score = 1.0
                    return fs
            except Exception as e:
                fs.notes.append(f"canonical_tsv_failed:{e}")
            score, stats = _score_tabular(df_a, df_b, rtol, atol)
            best_details["tabular"] = stats
            if score > best_score:
                best_score = score
                best_strategy = "tabular_tolerance"
        # V2.1: anchor any present file at _PROCESS_CREDIT, but keep any tabular
        # gains above the floor so 60-80% matches keep their information.
        if agent_path.stat().st_size > 0 and best_score < _PROCESS_CREDIT:
            best_score = _PROCESS_CREDIT
            if best_strategy == "fail":
                best_strategy = "process_credit"

    elif ext in _RDS_EXT:
        scratch_dir.mkdir(parents=True, exist_ok=True)
        agent_tsv = scratch_dir / (filename.replace("/", "_") + ".agent.tsv")
        ref_tsv = scratch_dir / (filename.replace("/", "_") + ".ref.tsv")
        ok_a, diag_a = _rds_to_tsv(agent_path, agent_tsv, rds_helper)
        ok_b, diag_b = _rds_to_tsv(ref_path, ref_tsv, rds_helper)
        best_details["rds_diag"] = {"agent": diag_a, "ref": diag_b, "ok_agent": ok_a, "ok_ref": ok_b}
        if ok_a and ok_b:
            df_a = load_table(agent_tsv)
            df_b = load_table(ref_tsv)
            if df_a is not None and df_b is not None:
                try:
                    if canonical_tsv(df_a) == canonical_tsv(df_b):
                        fs.strategy_used = "rds_normalized_equal"
                        fs.strategy_score = 1.0
                        return fs
                except Exception as e:
                    fs.notes.append(f"canonical_tsv_failed:{e}")
                score, stats = _score_tabular(df_a, df_b, rtol, atol)
                best_details["tabular"] = stats
                if score > best_score:
                    best_score = score
                    best_strategy = "rds_semantic"
        if best_score < _PROCESS_CREDIT and agent_path.stat().st_size > 0:
            best_score = _PROCESS_CREDIT
            if best_strategy == "fail":
                best_strategy = "process_credit"

    else:
        if agent_path.stat().st_size > 0:
            best_score = _PROCESS_CREDIT
            best_strategy = "process_credit"

    fs.strategy_used = best_strategy
    fs.strategy_score = best_score
    fs.details = best_details
    return fs


def _verdict_from_score(score: float) -> str:
    if score >= _VERDICT_PASS:
        return "pass"
    if score >= _VERDICT_PARTIAL_PASS:
        return "partial_pass"
    if score >= _VERDICT_PARTIAL_FAIL:
        return "partial_fail"
    return "fail"


def _legacy_verdict(run_dir: Path, registry: dict) -> dict:
    """Delegate to the untouched V1 evaluator for an apples-to-apples verdict."""
    try:
        return _v1.evaluate_run_dir(run_dir, registry)
    except Exception as e:  # pragma: no cover -- defensive
        return {"verdict": "fail", "error": f"legacy_failed:{e}"}


def evaluate_run_dir(
    run_dir: Path,
    registry: dict,
    *,
    rds_helper: Path,
    rtol: float,
    atol: float,
    scratch_root: Path,
    legacy: bool = False,
) -> dict:
    meta_path = run_dir / "metadata.json"
    if not meta_path.is_file():
        return {
            "run_dir": str(run_dir),
            "task_id": None,
            "error": "no_metadata",
            "overall_score": 0.0,
            "verdict": "error",
            "verdict_legacy": "fail",
            "process_signals": {},
            "per_file": [],
        }
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    task_id = meta.get("task_id")
    entry = next((t for t in registry.get("tasks", []) if t["id"] == task_id), None)
    expected = (entry.get("evaluation", {}).get("expected_files", []) if entry else [])
    gt_dir = _GT / (task_id or "") / "reference_output"

    workspace = run_dir / "workspace"
    if workspace.is_dir():
        output_dir = workspace / "output"
    else:
        output_dir = Path(meta.get("work_dir", run_dir)) / "output"

    scratch_dir = scratch_root / run_dir.name
    file_scores: list[FileScore] = []
    for rel in expected:
        fs = _score_file(
            rel,
            output_dir / rel,
            gt_dir / rel,
            rds_helper=rds_helper,
            rtol=rtol,
            atol=atol,
            scratch_dir=scratch_dir,
        )
        file_scores.append(fs)

    file_scores_mean = (
        sum(fs.strategy_score for fs in file_scores) / len(file_scores) if file_scores else 0.0
    )
    process = extract_process_signals(run_dir, output_dir)
    process_mean = process["mean"]

    if file_scores:
        overall = _PROCESS_WEIGHT * process_mean + _FILE_WEIGHT * file_scores_mean
    else:
        overall = process_mean

    trajectory_errored = process.get("trajectory_errored", False)
    no_outputs = process["signals"]["outputs_dir_nonempty_and_valid"] == 0.0
    if trajectory_errored and no_outputs:
        verdict = "error"
    else:
        verdict = _verdict_from_score(overall)

    legacy_out = _legacy_verdict(run_dir, registry)
    verdict_legacy = legacy_out.get("verdict", "fail")
    if legacy:
        verdict = verdict_legacy

    return {
        "run_dir": str(run_dir),
        "task_id": task_id,
        "batch_run_id": meta.get("batch_run_id"),
        "model": (meta.get("agent") or {}).get("llm_model"),
        "skill": meta.get("skill"),
        "n_expected": len(expected),
        "n_files_scored": len(file_scores),
        "overall_score": round(overall, 4),
        "verdict": verdict,
        "verdict_legacy": verdict_legacy,
        "process_signals": process["signals"],
        "process_mean": round(process_mean, 4),
        "process_counts": process["counts"],
        "file_scores_mean": round(file_scores_mean, 4),
        "per_file": [fs.to_dict() for fs in file_scores],
    }


def evaluate_batch(
    batch_run_id: str,
    registry: dict,
    *,
    rds_helper: Path,
    rtol: float,
    atol: float,
    legacy: bool,
    scratch_root: Path,
) -> dict:
    batch_root = _RUNS / f"batch_{batch_run_id}"
    if not batch_root.is_dir():
        raise FileNotFoundError(f"batch directory not found: {batch_root}")
    per_task = []
    for child in sorted(batch_root.iterdir()):
        if child.is_dir():
            per_task.append(
                evaluate_run_dir(
                    child,
                    registry,
                    rds_helper=rds_helper,
                    rtol=rtol,
                    atol=atol,
                    scratch_root=scratch_root,
                    legacy=legacy,
                )
            )

    counts_v2 = {"pass": 0, "partial_pass": 0, "partial_fail": 0, "fail": 0, "error": 0}
    counts_v1 = {"pass": 0, "partial": 0, "fail": 0}
    scores = []
    for r in per_task:
        v = r.get("verdict", "fail")
        counts_v2[v] = counts_v2.get(v, 0) + 1
        vl = r.get("verdict_legacy", "fail")
        counts_v1[vl] = counts_v1.get(vl, 0) + 1
        scores.append(r.get("overall_score", 0.0))

    return {
        "batch_run_id": batch_run_id,
        "batch_root": str(batch_root),
        "evaluator_version": EVALUATOR_VERSION,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rtol": rtol,
        "atol": atol,
        "legacy_active": legacy,
        "n_tasks": len(per_task),
        "mean_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
        "verdict_counts": counts_v2,
        "verdict_counts_legacy": counts_v1,
        "tasks": {r.get("task_id") or f"unknown_{i}": r for i, r in enumerate(per_task)},
        "results": per_task,
    }


def _render_markdown(summary: dict) -> str:
    lines = [
        f"# Evaluation V2 · batch `{summary['batch_run_id']}`",
        "",
        f"evaluator_version: `{summary['evaluator_version']}` · "
        f"ts: `{summary['ts']}` · n_tasks: {summary['n_tasks']} · "
        f"rtol={summary['rtol']} atol={summary['atol']}",
        "",
        f"**Mean overall score:** {summary['mean_score']:.3f}",
        "",
        "**Verdict counts (V2):** "
        + ", ".join(f"{k}={v}" for k, v in summary["verdict_counts"].items()),
        "",
        "**Verdict counts (legacy V1):** "
        + ", ".join(f"{k}={v}" for k, v in summary["verdict_counts_legacy"].items()),
        "",
        "| task | verdict | verdict (V1) | overall | process_mean | files_mean | n_expected | strategies |",
        "|------|---------|--------------|---------|--------------|------------|------------|------------|",
    ]
    for r in summary["results"]:
        strategies = ",".join(sorted({fs["strategy_used"] for fs in r.get("per_file", [])}))
        lines.append(
            f"| `{r.get('task_id')}` | **{r.get('verdict')}** | {r.get('verdict_legacy')} | "
            f"{r.get('overall_score', 0.0):.3f} | {r.get('process_mean', 0.0):.2f} | "
            f"{r.get('file_scores_mean', 0.0):.3f} | {r.get('n_expected', 0)} | {strategies} |"
        )
    lines.append("")
    lines.append("## Per-file detail")
    lines.append("")
    for r in summary["results"]:
        lines.append(f"### `{r.get('task_id')}`")
        lines.append("")
        lines.append("| file | strategy | score | bytes_eq | size_a | size_r |")
        lines.append("|------|----------|-------|----------|--------|--------|")
        for fs in r.get("per_file", []):
            lines.append(
                f"| `{fs['filename']}` | {fs['strategy_used']} | {fs['strategy_score']:.3f} | "
                f"{fs['bytes_identical']} | {fs['size_agent']} | {fs['size_ref']} |"
            )
        lines.append("")
    return "\n".join(lines)


def _flatten_per_file(summary: dict) -> list[dict]:
    rows = []
    for r in summary["results"]:
        for fs in r.get("per_file", []):
            rows.append({
                "batch_run_id": summary["batch_run_id"],
                "task_id": r.get("task_id"),
                **fs,
            })
    return rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Lenient BixBench-style evaluator for ldp R-task runs (V2).",
    )
    p.add_argument("--batch-run-id", action="append", help="batch id (repeatable)")
    p.add_argument("--all", action="store_true", help="evaluate every runs/batch_*")
    p.add_argument("--registry", default=str(_REG))
    p.add_argument("--output", default=None, help="directory for json/md outputs")
    p.add_argument("--per-file-json", default=None,
                   help="if set, also dump a flat per-file JSON array at this path")
    p.add_argument("--rds-helper", default=str(_DEFAULT_RDS_HELPER),
                   help="Rscript sidecar to dump .rds files to TSV")
    p.add_argument("--rtol", type=float, default=1e-3)
    p.add_argument("--atol", type=float, default=1e-5)
    p.add_argument("--legacy", action="store_true",
                   help="emit V1 verdicts as the primary verdict")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    rds_helper = Path(args.rds_helper)

    targets: list[str] = []
    if args.all:
        for d in sorted(_RUNS.glob("batch_*")):
            if d.is_dir():
                targets.append(d.name.removeprefix("batch_"))
    if args.batch_run_id:
        for b in args.batch_run_id:
            if b not in targets:
                targets.append(b)
    if not targets:
        p.error("pass --batch-run-id or --all")

    out_dir = Path(args.output) if args.output else (_LDP / "runs" / "_evaluations")
    out_dir.mkdir(parents=True, exist_ok=True)
    scratch_root = Path(out_dir) / "_rds_scratch"
    scratch_root.mkdir(parents=True, exist_ok=True)

    all_flat: list[dict] = []
    for bid in targets:
        t0 = time.time()
        try:
            summary = evaluate_batch(
                bid,
                registry,
                rds_helper=rds_helper,
                rtol=args.rtol,
                atol=args.atol,
                legacy=args.legacy,
                scratch_root=scratch_root,
            )
        except FileNotFoundError as e:
            print(f"skip {bid}: {e}", file=sys.stderr)
            continue
        (out_dir / f"{bid}.v2.json").write_text(json.dumps(summary, indent=2, default=str))
        (out_dir / f"{bid}.v2.md").write_text(_render_markdown(summary))
        if not args.quiet:
            print(_render_markdown(summary))
        all_flat.extend(_flatten_per_file(summary))
        if not args.quiet:
            print(f"# {bid}: {time.time() - t0:.1f}s", file=sys.stderr)

    if args.per_file_json:
        Path(args.per_file_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.per_file_json).write_text(json.dumps(all_flat, indent=2, default=str))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
