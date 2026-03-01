from __future__ import annotations

import json
from pathlib import Path

from analyzers.dynamic_runtime.analyzer import analyze_dynamic_runs


def test_dynamic_analyzer_summary(tmp_path: Path) -> None:
    run_file = tmp_path / "events_run_1.jsonl"
    lines = [
        {
            "timestamp": "2026-01-01T00:00:00+00:00",
            "event_type": "call_start",
            "phase": "llm_call",
            "payload": {"kind": "llm_call", "prompt_chars": 100, "template_hash": "abc"},
        },
        {
            "timestamp": "2026-01-01T00:00:01+00:00",
            "event_type": "call_end",
            "phase": "llm_call",
            "payload": {
                "kind": "llm_call",
                "prompt_chars": 100,
                "template_hash": "abc",
                "usage": {"total_tokens": 120},
            },
        },
        {
            "timestamp": "2026-01-01T00:00:02+00:00",
            "event_type": "runtime_summary",
            "phase": "runtime",
            "payload": {"thread_peak": 3, "process_peak": 1, "async_peak": 2},
        },
    ]
    run_file.write_text("\n".join(json.dumps(x) for x in lines), encoding="utf-8")
    metrics, artifacts, obs = analyze_dynamic_runs(
        {"run_1": run_file},
        {"run_1": {"cpu_peak_pct": 50, "memory_peak_mb": 200}},
        tmp_path,
    )
    assert any(m.metric_code == "D1" for m in metrics)
    assert any(a.artifact_type == "dynamic_summary" for a in artifacts)
    assert obs >= 0
