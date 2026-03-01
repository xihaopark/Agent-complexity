from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import markdown

from analyzers.utils import to_artifact_ref, write_json
from common.events import ArtifactRef, MetricRecord


STATIC_CODES = {f"A{i}" for i in range(1, 12)} | {"F1", "F2"}
DYNAMIC_CODES = {f"B{i}" for i in range(1, 4)} | {f"C{i}" for i in range(1, 7)} | {f"D{i}" for i in range(1, 6)} | {f"E{i}" for i in range(1, 3)} | {"F3", "F4", "F5", "F6", "F7"}


METRIC_DESCRIPTION = {
    "A1": "模块/包数量",
    "A2": "函数/方法规模",
    "A3": "依赖图规模",
    "A4": "依赖环与强连通",
    "A5": "调用图规模",
    "A6": "调用图复杂度",
    "A7": "模块化聚类质量",
    "A8": "圈复杂度统计",
    "A9": "Halstead 体积/难度",
    "A10": "异常处理结构复杂度",
    "A11": "配置/策略分支复杂度",
    "B1": "线程峰值",
    "B2": "进程峰值",
    "B3": "async 并发度",
    "C1": "运行态 agent 数量",
    "C2": "消息频率",
    "C3": "通信带宽",
    "C4": "协调回合数",
    "C5": "协作冗余率",
    "C6": "错误放大系数",
    "D1": "LLM 调用次数",
    "D2": "Token 总用量",
    "D3": "Prompt 长度分布",
    "D4": "Prompt 模板多样性",
    "D5": "工具调用密度",
    "E1": "状态规模近似",
    "E2": "重试/回滚复杂度",
    "F1": "静态可测试性",
    "F2": "静态可观测性",
    "F3": "CPU 峰值",
    "F4": "内存峰值",
    "F5": "端到端时延",
    "F6": "运行时可测试性",
    "F7": "运行时可观测性",
}


def _normalize(value: float) -> float:
    if value <= 0:
        return 0.0
    return min(1.0, math.log1p(value) / math.log(101))


def maybe_compute_composite(metrics: list[MetricRecord], enabled: bool) -> tuple[list[MetricRecord], float | None]:
    if not enabled:
        return metrics, None
    summary = [m for m in metrics if m.scope == "system" and m.raw_value is not None]
    if not summary:
        return metrics, None
    scores = [_normalize(float(m.raw_value)) for m in summary]
    composite = 100.0 * sum(scores) / len(scores)
    metrics.append(
        MetricRecord(
            metric_code="S",
            scope="system",
            raw_value=composite,
            agg_type="summary",
            value_json={"enabled": True},
        )
    )
    return metrics, composite


def _markdown_table(metrics: list[MetricRecord]) -> str:
    lines = [
        "| Code | Metric | Scope | Value | CI | Evidence |",
        "|---|---|---|---:|---|---|",
    ]
    for m in metrics:
        value = "" if m.raw_value is None else f"{m.raw_value:.4f}"
        ci = ""
        if m.ci_low is not None and m.ci_high is not None:
            ci = f"[{m.ci_low:.4f}, {m.ci_high:.4f}]"
        lines.append(
            f"| {m.metric_code} | {METRIC_DESCRIPTION.get(m.metric_code, '-')}"
            f" | {m.scope} | {value} | {ci} | {m.evidence_ref or '-'} |"
        )
    return "\n".join(lines)


def generate_report(
    analysis_id: str,
    job_meta: dict[str, Any],
    metrics: list[MetricRecord],
    artifact_dir: Path,
    composite_enabled: bool = False,
) -> tuple[list[MetricRecord], list[ArtifactRef]]:
    metrics, composite_score = maybe_compute_composite(metrics, composite_enabled)
    static_metrics = [m for m in metrics if m.metric_code in STATIC_CODES and m.scope == "system"]
    dynamic_metrics = [m for m in metrics if m.metric_code in DYNAMIC_CODES and m.scope == "system"]
    run_metrics = [m for m in metrics if m.scope == "run"]

    sections = [
        "# Agentic Complexity Report",
        "",
        "## 1. 项目元数据",
        f"- Analysis ID: `{analysis_id}`",
        f"- Repo: `{job_meta.get('repo_url')}`",
        f"- Git Ref: `{job_meta.get('git_ref')}`",
        f"- Run Profile: `{job_meta.get('run_profile')}`",
        f"- Repeats: `{job_meta.get('repeats')}`",
        f"- Timeout(sec): `{job_meta.get('timeout_sec')}`",
        f"- Observability Coverage: `{job_meta.get('observability_coverage', 0):.4f}`",
        f"- Composite Score Enabled: `{composite_enabled}`",
        f"- Composite Score: `{composite_score if composite_score is not None else 'disabled'}`",
        "",
        "## 2. 静态指标 (A/F)",
        _markdown_table(static_metrics),
        "",
        "## 3. 动态指标 (B/C/D/E/F)",
        _markdown_table(dynamic_metrics),
        "",
        "## 4. 运行级指标明细",
        _markdown_table(run_metrics[:200]),
        "",
        "## 5. 结论与热点",
        "- 本报告默认输出指标明细，不做默认综合排名。",
        "- 建议优先关注高值指标对应模块与阶段，并结合 evidence_ref 复核。",
    ]

    report_md = "\n".join(sections).strip() + "\n"
    report_html = markdown.markdown(report_md, extensions=["tables"])

    md_path = artifact_dir / "report.md"
    html_path = artifact_dir / "report.html"
    metrics_json_path = artifact_dir / "metrics.json"
    metrics_parquet_path = artifact_dir / "metrics.parquet"

    md_path.write_text(report_md, encoding="utf-8")
    html_path.write_text(report_html, encoding="utf-8")
    write_json(metrics_json_path, [m.model_dump() for m in metrics])

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
                "evidence_ref": metric.evidence_ref,
                "value_json": json.dumps(metric.value_json, ensure_ascii=False),
            }
        )
    import pandas as pd

    pd.DataFrame(rows).to_parquet(metrics_parquet_path, index=False)

    artifacts = [
        to_artifact_ref(md_path, "report_markdown"),
        to_artifact_ref(html_path, "report_html"),
        to_artifact_ref(metrics_json_path, "metrics_json"),
        to_artifact_ref(metrics_parquet_path, "metrics_parquet"),
    ]
    return metrics, artifacts
