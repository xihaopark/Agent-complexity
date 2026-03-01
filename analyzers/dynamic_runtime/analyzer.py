from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from analyzers.utils import to_artifact_ref, write_json
from common.events import ArtifactRef, MetricRecord


DYNAMIC_CODES = [
    "B1",
    "B2",
    "B3",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "D1",
    "D2",
    "D3",
    "D4",
    "D5",
    "E1",
    "E2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
]


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _bootstrap_ci(values: list[float], n_bootstrap: int = 500) -> tuple[float | None, float | None]:
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], values[0]
    rng = np.random.default_rng(42)
    arr = np.array(values)
    samples = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, len(arr), len(arr))
        samples.append(float(np.mean(arr[idx])))
    return float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))


def _load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    events.sort(key=lambda x: x.get("timestamp", ""))
    return events


def _run_metrics(events: list[dict[str, Any]], run_stats: dict[str, float] | None = None) -> dict[str, float]:
    run_stats = run_stats or {}
    if not events:
        return {code: 0.0 for code in DYNAMIC_CODES}

    timestamps = [_parse_ts(evt["timestamp"]) for evt in events if evt.get("timestamp")]
    if timestamps:
        duration_s = max((max(timestamps) - min(timestamps)).total_seconds(), 1e-3)
    else:
        duration_s = 1.0

    call_start = [e for e in events if e.get("event_type") == "call_start"]
    call_end = [e for e in events if e.get("event_type") == "call_end"]
    call_error = [e for e in events if e.get("event_type") == "call_error"]
    summaries = [e for e in events if e.get("event_type") == "runtime_summary"]

    llm_end = [e for e in call_end if e.get("payload", {}).get("kind") == "llm_call"]
    tool_end = [e for e in call_end if e.get("payload", {}).get("kind") == "tool_call"]
    message_end = [e for e in call_end if e.get("payload", {}).get("kind") == "message_call"]
    retry_end = [e for e in call_end if e.get("payload", {}).get("kind") == "retry_call"]

    usage_total = 0
    prompt_token_estimates: list[float] = []
    template_hashes: list[str] = []
    for evt in llm_end:
        payload = evt.get("payload", {})
        usage = payload.get("usage", {}) or {}
        if isinstance(usage, dict):
            if "total_tokens" in usage:
                usage_total += float(usage.get("total_tokens", 0))
            else:
                usage_total += float(usage.get("prompt_tokens", usage.get("input_tokens", 0)))
                usage_total += float(usage.get("completion_tokens", usage.get("output_tokens", 0)))
        prompt_chars = float(payload.get("prompt_chars", 0))
        prompt_token_estimates.append(prompt_chars / 4.0 if prompt_chars else 0.0)
        template = payload.get("template_hash")
        if isinstance(template, str) and template:
            template_hashes.append(template)

    message_bytes = 0.0
    message_fingerprints: list[str] = []
    for evt in message_end:
        payload = evt.get("payload", {})
        message_bytes += float(payload.get("bytes_in", 0)) + float(payload.get("bytes_out", 0))
        fp = f"{payload.get('target','')}:{payload.get('bytes_in',0)}:{payload.get('bytes_out',0)}"
        message_fingerprints.append(fp)
    unique_messages = len(set(message_fingerprints))
    redundancy = (1 - unique_messages / len(message_fingerprints)) if message_fingerprints else 0.0

    thread_peak = 0.0
    process_peak = 0.0
    async_peak = 0.0
    if summaries:
        payload = summaries[-1].get("payload", {})
        thread_peak = float(payload.get("thread_peak", 0))
        process_peak = float(payload.get("process_peak", 0))
        async_peak = float(payload.get("async_peak", 0))

    actors = {evt.get("actor") for evt in events if evt.get("phase") == "message_call"}
    actors.discard(None)

    total_errors = len(call_error)
    total_calls = max(1, len(call_end) + len(call_error))
    error_amplification = total_errors / total_calls

    expected_phases = {"llm_call", "tool_call", "message_call", "runtime"}
    seen_phases = {str(evt.get("phase")) for evt in events}
    observability_score = len(expected_phases & seen_phases) / len(expected_phases)

    run_metrics = {
        "B1": thread_peak,
        "B2": process_peak,
        "B3": async_peak,
        "C1": float(len(actors)),
        "C2": float(len(message_end) / duration_s),
        "C3": float(message_bytes / duration_s),
        "C4": float(len(message_end)),
        "C5": float(redundancy),
        "C6": float(error_amplification),
        "D1": float(len(llm_end)),
        "D2": float(usage_total),
        "D3": float(np.mean(prompt_token_estimates)) if prompt_token_estimates else 0.0,
        "D4": float(len(set(template_hashes))),
        "D5": float(len(tool_end) / max(1, len(call_end))),
        "E1": float(len([e for e in events if e.get("event_type") == "state_write"])),
        "E2": float(len(retry_end)),
        "F3": float(run_stats.get("cpu_peak_pct", 0.0)),
        "F4": float(run_stats.get("memory_peak_mb", 0.0)),
        "F5": float(duration_s),
        "F6": float(run_stats.get("reproducibility_flag", 1.0)),
        "F7": float(observability_score),
    }
    return run_metrics


def analyze_dynamic_runs(
    event_files: dict[str, Path],
    run_stats: dict[str, dict[str, float]],
    artifact_dir: Path,
) -> tuple[list[MetricRecord], list[ArtifactRef], float]:
    metrics: list[MetricRecord] = []
    artifacts: list[ArtifactRef] = []
    run_metric_map: dict[str, dict[str, float]] = {}

    for run_id, path in event_files.items():
        events = _load_events(path)
        run_values = _run_metrics(events, run_stats.get(run_id, {}))
        run_metric_map[run_id] = run_values
        for code, value in run_values.items():
            metrics.append(
                MetricRecord(
                    metric_code=code,
                    scope="run",
                    run_id=run_id,
                    raw_value=float(value),
                    agg_type="raw",
                    evidence_ref=str(path),
                )
            )

    if run_metric_map:
        for code in DYNAMIC_CODES:
            values = [run_metric_map[r][code] for r in run_metric_map]
            ci_low, ci_high = _bootstrap_ci(values)
            metrics.append(
                MetricRecord(
                    metric_code=code,
                    scope="system",
                    raw_value=float(np.mean(values)),
                    agg_type="summary",
                    ci_low=ci_low,
                    ci_high=ci_high,
                    value_json={
                        "mean": float(np.mean(values)),
                        "p50": float(np.percentile(values, 50)),
                        "p95": float(np.percentile(values, 95)),
                        "count": len(values),
                    },
                )
            )

    obs_values = [run_metric_map[r]["F7"] for r in run_metric_map] if run_metric_map else [0.0]
    observability_coverage = float(np.mean(obs_values))

    summary_path = artifact_dir / "dynamic_metrics_summary.json"
    parquet_path = artifact_dir / "dynamic_metrics.parquet"
    jsonl_path = artifact_dir / "dynamic_metrics.jsonl"

    summary_data = {
        "runs": run_metric_map,
        "observability_coverage": observability_coverage,
    }
    write_json(summary_path, summary_data)
    artifacts.append(to_artifact_ref(summary_path, "dynamic_summary"))

    rows = []
    for metric in metrics:
        rows.append(
            {
                "metric_code": metric.metric_code,
                "scope": metric.scope,
                "run_id": metric.run_id,
                "raw_value": metric.raw_value,
                "agg_type": metric.agg_type,
                "ci_low": metric.ci_low,
                "ci_high": metric.ci_high,
                "value_json": json.dumps(metric.value_json, ensure_ascii=False),
                "evidence_ref": metric.evidence_ref,
            }
        )
    df = pd.DataFrame(rows)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(parquet_path, index=False)
    df.to_json(jsonl_path, orient="records", lines=True, force_ascii=False)
    artifacts.append(to_artifact_ref(parquet_path, "metrics_parquet"))
    artifacts.append(to_artifact_ref(jsonl_path, "metrics_jsonl"))

    return metrics, artifacts, observability_coverage
