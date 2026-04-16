from __future__ import annotations

import re
from pathlib import Path

import networkx as nx

from analyzers.utils import to_artifact_ref, write_json
from common.events import ArtifactRef, MetricRecord


EXCLUDE_PARTS = {".git", "node_modules", ".next", "dist", "build"}
IMPORT_RE = re.compile(r"""^\s*import\s+.*?\s+from\s+['"]([^'"]+)['"]""", re.MULTILINE)


def _discover_ts_files(repo_path: Path) -> list[Path]:
    files: list[Path] = []
    for ext in ("*.ts", "*.tsx"):
        for path in repo_path.rglob(ext):
            if any(part in EXCLUDE_PARTS for part in path.parts):
                continue
            files.append(path)
    return files


def _is_test_file(path: Path) -> bool:
    return path.name.endswith(".test.ts") or path.name.endswith(".spec.ts")


def analyze_typescript_repo(repo_path: Path, artifact_dir: Path) -> tuple[list[MetricRecord], list[ArtifactRef]]:
    ts_files = _discover_ts_files(repo_path)
    if not ts_files:
        return [], []

    dep_graph = nx.DiGraph()
    observability_hits = 0
    test_files = [p for p in ts_files if _is_test_file(p)]
    effective_modules = [p for p in ts_files if not _is_test_file(p)]

    for file in ts_files:
        module_name = str(file.relative_to(repo_path))
        dep_graph.add_node(module_name)
        content = file.read_text(encoding="utf-8", errors="ignore")
        for match in IMPORT_RE.findall(content):
            dep_graph.add_edge(module_name, match)
        if "opentelemetry" in content or "console." in content or "trace" in content:
            observability_hits += 1

    dep_nodes = dep_graph.number_of_nodes()
    dep_edges = dep_graph.number_of_edges()
    scc = list(nx.strongly_connected_components(dep_graph))
    scc_count = len([comp for comp in scc if len(comp) > 1])
    largest_scc_ratio = (max((len(comp) for comp in scc), default=0) / dep_nodes) if dep_nodes else 0.0

    modularity = 0.0
    if dep_edges > 0 and dep_nodes > 1:
        undirected = dep_graph.to_undirected()
        communities = list(nx.algorithms.community.greedy_modularity_communities(undirected))
        if communities:
            modularity = float(nx.algorithms.community.modularity(undirected, communities))

    test_ratio = (len(test_files) / len(ts_files)) if ts_files else 0.0
    obs_ratio = (observability_hits / len(ts_files)) if ts_files else 0.0

    evidence_path = artifact_dir / "static_ts_summary.json"
    dep_path = artifact_dir / "dependency_graph_ts.json"
    write_json(
        evidence_path,
        {
            "ts_files": len(ts_files),
            "effective_modules": len(effective_modules),
            "test_files": len(test_files),
            "scc_count": scc_count,
            "largest_scc_ratio": largest_scc_ratio,
        },
    )
    write_json(dep_path, {"nodes": list(dep_graph.nodes()), "edges": [[s, t] for s, t in dep_graph.edges()]})

    metrics: list[MetricRecord] = [
        MetricRecord(
            metric_code="A1",
            scope="system",
            raw_value=float(len(effective_modules)),
            value_json={"language": "typescript"},
            evidence_ref=str(evidence_path),
        ),
        MetricRecord(
            metric_code="A3",
            scope="system",
            raw_value=float(dep_edges),
            value_json={"language": "typescript", "nodes": dep_nodes},
            evidence_ref=str(dep_path),
        ),
        MetricRecord(
            metric_code="A4",
            scope="system",
            raw_value=float(scc_count),
            value_json={"language": "typescript", "largest_scc_ratio": largest_scc_ratio},
            evidence_ref=str(dep_path),
        ),
        MetricRecord(
            metric_code="A7",
            scope="system",
            raw_value=float(modularity),
            value_json={"language": "typescript"},
            evidence_ref=str(dep_path),
        ),
        MetricRecord(
            metric_code="F1",
            scope="system",
            raw_value=float(test_ratio),
            value_json={"language": "typescript", "test_files": len(test_files)},
            evidence_ref=str(evidence_path),
        ),
        MetricRecord(
            metric_code="F2",
            scope="system",
            raw_value=float(obs_ratio),
            value_json={"language": "typescript", "files_with_observability": observability_hits},
            evidence_ref=str(evidence_path),
        ),
    ]
    artifacts = [
        to_artifact_ref(evidence_path, "static_ts_summary"),
        to_artifact_ref(dep_path, "dependency_graph_ts"),
    ]
    return metrics, artifacts
