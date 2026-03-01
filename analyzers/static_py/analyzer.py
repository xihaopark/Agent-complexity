from __future__ import annotations

import ast
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from analyzers.utils import to_artifact_ref, write_json
from common.events import ArtifactRef, MetricRecord

try:
    from radon.complexity import cc_visit  # type: ignore
    from radon.metrics import h_visit  # type: ignore
except Exception:  # pragma: no cover
    cc_visit = None
    h_visit = None


EXCLUDE_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache"}


def _module_name(root: Path, file_path: Path) -> str:
    relative = file_path.relative_to(root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else "root"


def _discover_python_files(repo_path: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_path.rglob("*.py"):
        if any(part in EXCLUDE_PARTS for part in path.parts):
            continue
        files.append(path)
    return files


def _is_test_file(path: Path) -> bool:
    lower_parts = [p.lower() for p in path.parts]
    return "tests" in lower_parts or path.name.lower().startswith("test_")


def _safe_parse(source: str, path: Path) -> ast.AST | None:
    try:
        return ast.parse(source, filename=str(path))
    except SyntaxError:
        return None


def _full_call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _full_call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


class FunctionCallCollector(ast.NodeVisitor):
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.current_fn: list[str] = []
        self.edges: list[tuple[str, str]] = []
        self.functions: list[str] = []
        self.unresolved_calls = 0

    def _fn_id(self, name: str) -> str:
        return f"{self.module_name}:{name}"

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        fn_id = self._fn_id(node.name)
        self.functions.append(fn_id)
        self.current_fn.append(fn_id)
        self.generic_visit(node)
        self.current_fn.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        fn_id = self._fn_id(node.name)
        self.functions.append(fn_id)
        self.current_fn.append(fn_id)
        self.generic_visit(node)
        self.current_fn.pop()

    def visit_Call(self, node: ast.Call) -> Any:
        if self.current_fn:
            called = _full_call_name(node.func)
            if called:
                self.edges.append((self.current_fn[-1], called))
            else:
                self.unresolved_calls += 1
        self.generic_visit(node)


class ComplexityCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.function_count = 0
        self.class_method_count = 0
        self.try_count = 0
        self.bare_except_count = 0
        self.max_try_depth = 0
        self.except_types: set[str] = set()
        self.current_try_depth = 0
        self.if_count = 0
        self.getenv_count = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.function_count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.function_count += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.class_method_count += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> Any:
        self.if_count += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> Any:
        self.try_count += 1
        self.current_try_depth += 1
        self.max_try_depth = max(self.max_try_depth, self.current_try_depth)
        for handler in node.handlers:
            if handler.type is None:
                self.bare_except_count += 1
            else:
                exc_name = _full_call_name(handler.type) or ast.unparse(handler.type)
                self.except_types.add(exc_name)
        self.generic_visit(node)
        self.current_try_depth -= 1

    def visit_Call(self, node: ast.Call) -> Any:
        fn_name = _full_call_name(node.func)
        if fn_name and ("getenv" in fn_name or "os.environ" in fn_name):
            self.getenv_count += 1
        self.generic_visit(node)


def _radon_metrics(source: str) -> tuple[list[float], list[float], list[float]]:
    cc_values: list[float] = []
    volumes: list[float] = []
    difficulties: list[float] = []
    if cc_visit is not None:
        try:
            cc_values = [float(block.complexity) for block in cc_visit(source)]
        except Exception:
            cc_values = []
    if h_visit is not None:
        try:
            result = h_visit(source)
            total = getattr(result, "total", None)
            volume = getattr(total, "volume", None)
            difficulty = getattr(total, "difficulty", None)
            if volume is not None:
                volumes.append(float(volume))
            if difficulty is not None:
                difficulties.append(float(difficulty))
        except Exception:
            pass
    return cc_values, volumes, difficulties


def _metric(code: str, value: float | None, evidence: str, extra: dict[str, Any] | None = None) -> MetricRecord:
    return MetricRecord(
        metric_code=code,
        scope="system",
        raw_value=value,
        value_json=extra or {},
        agg_type="raw",
        evidence_ref=evidence,
    )


def analyze_python_repo(repo_path: Path, artifact_dir: Path) -> tuple[list[MetricRecord], list[ArtifactRef]]:
    py_files = _discover_python_files(repo_path)
    dep_graph = nx.DiGraph()
    call_graph = nx.DiGraph()
    collector = ComplexityCollector()
    imports_counter: Counter[str] = Counter()

    cc_all: list[float] = []
    halstead_volume_all: list[float] = []
    halstead_difficulty_all: list[float] = []
    unresolved_calls = 0
    total_calls = 0

    module_names = {}
    for path in py_files:
        module_names[path] = _module_name(repo_path, path)
        dep_graph.add_node(module_names[path])

    for path in py_files:
        module = module_names[path]
        source = path.read_text(encoding="utf-8", errors="ignore")
        tree = _safe_parse(source, path)
        if tree is None:
            continue
        collector.visit(tree)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dep_graph.add_edge(module, alias.name.split(".")[0])
                    imports_counter[alias.name.split(".")[0]] += 1
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dep_graph.add_edge(module, node.module.split(".")[0])
                    imports_counter[node.module.split(".")[0]] += 1

        call_collector = FunctionCallCollector(module)
        call_collector.visit(tree)
        unresolved_calls += call_collector.unresolved_calls
        total_calls += len(call_collector.edges) + call_collector.unresolved_calls
        for fn in call_collector.functions:
            call_graph.add_node(fn)
        for src, dst in call_collector.edges:
            call_graph.add_edge(src, dst)

        cc_values, volumes, difficulties = _radon_metrics(source)
        cc_all.extend(cc_values)
        halstead_volume_all.extend(volumes)
        halstead_difficulty_all.extend(difficulties)

    test_files = [f for f in py_files if _is_test_file(f)]
    effective_modules = [m for p, m in module_names.items() if not _is_test_file(p)]

    dep_nodes = dep_graph.number_of_nodes()
    dep_edges = dep_graph.number_of_edges()
    dep_density = float(nx.density(dep_graph)) if dep_nodes > 1 else 0.0
    scc = list(nx.strongly_connected_components(dep_graph))
    scc_count = len([comp for comp in scc if len(comp) > 1])
    largest_scc_ratio = (max((len(comp) for comp in scc), default=0) / dep_nodes) if dep_nodes else 0.0

    call_nodes = call_graph.number_of_nodes()
    call_edges = call_graph.number_of_edges()
    unresolved_ratio = (unresolved_calls / total_calls) if total_calls else 0.0
    weak_components = nx.number_weakly_connected_components(call_graph) if call_nodes else 0
    call_cyclomatic = (call_edges - call_nodes + weak_components) if call_nodes else 0.0

    modularity_score = 0.0
    if dep_graph.number_of_edges() > 0 and dep_graph.number_of_nodes() > 1:
        undirected = dep_graph.to_undirected()
        communities = list(nx.algorithms.community.greedy_modularity_communities(undirected))
        if communities:
            modularity_score = float(nx.algorithms.community.modularity(undirected, communities))

    cc_mean = float(np.mean(cc_all)) if cc_all else 0.0
    cc_p90 = float(np.percentile(cc_all, 90)) if cc_all else 0.0
    cc_p99 = float(np.percentile(cc_all, 99)) if cc_all else 0.0
    cc_high_ratio = (sum(1 for v in cc_all if v > 10) / len(cc_all)) if cc_all else 0.0

    hv_mean = float(np.mean(halstead_volume_all)) if halstead_volume_all else 0.0
    hv_p95 = float(np.percentile(halstead_volume_all, 95)) if halstead_volume_all else 0.0
    hd_mean = float(np.mean(halstead_difficulty_all)) if halstead_difficulty_all else 0.0

    ci_exists = (repo_path / ".github" / "workflows").exists()
    test_ratio = (len(test_files) / len(py_files)) if py_files else 0.0
    observability_hits = 0
    for p in py_files:
        content = p.read_text(encoding="utf-8", errors="ignore")
        if "opentelemetry" in content or "trace_id" in content or "logging." in content:
            observability_hits += 1
    observability_ratio = (observability_hits / len(py_files)) if py_files else 0.0

    evidence_path = artifact_dir / "static_python_summary.json"
    dep_path = artifact_dir / "dependency_graph.json"
    call_path = artifact_dir / "call_graph.json"

    write_json(
        evidence_path,
        {
            "python_files": len(py_files),
            "effective_modules": len(effective_modules),
            "imports_top10": imports_counter.most_common(10),
            "scc_count": scc_count,
            "largest_scc_ratio": largest_scc_ratio,
            "unresolved_call_ratio": unresolved_ratio,
            "cc_count": len(cc_all),
            "halstead_count": len(halstead_volume_all),
        },
    )
    write_json(
        dep_path,
        {"nodes": list(dep_graph.nodes()), "edges": [[s, t] for s, t in dep_graph.edges()]},
    )
    write_json(
        call_path,
        {"nodes": list(call_graph.nodes()), "edges": [[s, t] for s, t in call_graph.edges()]},
    )

    metrics: list[MetricRecord] = [
        _metric("A1", float(len(effective_modules)), str(evidence_path)),
        _metric("A2", float(collector.function_count + collector.class_method_count), str(evidence_path)),
        _metric("A3", float(dep_edges), str(dep_path), {"nodes": dep_nodes, "density": dep_density}),
        _metric("A4", float(scc_count), str(dep_path), {"largest_scc_ratio": largest_scc_ratio}),
        _metric(
            "A5",
            float(call_edges),
            str(call_path),
            {"nodes": call_nodes, "unresolved_call_ratio": unresolved_ratio},
        ),
        _metric("A6", float(call_cyclomatic), str(call_path), {"weak_components": weak_components}),
        _metric("A7", float(modularity_score), str(dep_path)),
        _metric(
            "A8",
            cc_mean,
            str(evidence_path),
            {"p90": cc_p90, "p99": cc_p99, "high_complexity_ratio": cc_high_ratio},
        ),
        _metric(
            "A9",
            hv_mean,
            str(evidence_path),
            {"volume_p95": hv_p95, "difficulty_mean": hd_mean},
        ),
        _metric(
            "A10",
            float(collector.try_count),
            str(evidence_path),
            {
                "max_try_depth": collector.max_try_depth,
                "except_type_count": len(collector.except_types),
                "bare_except_ratio": (
                    collector.bare_except_count / collector.try_count if collector.try_count else 0.0
                ),
            },
        ),
        _metric(
            "A11",
            float(collector.if_count),
            str(evidence_path),
            {"getenv_count": collector.getenv_count},
        ),
        _metric("F1", test_ratio, str(evidence_path), {"test_files": len(test_files), "ci_exists": ci_exists}),
        _metric("F2", observability_ratio, str(evidence_path), {"files_with_observability": observability_hits}),
    ]

    artifacts = [
        to_artifact_ref(evidence_path, "static_python_summary"),
        to_artifact_ref(dep_path, "dependency_graph"),
        to_artifact_ref(call_path, "call_graph"),
    ]
    return metrics, artifacts
