"""Extract skill-unique tokens from a skill markdown blob.

V3 insight layer uses these tokens to detect whether the agent actually
attended to the injected skill — we scan the run's trajectory for any
tool-call argument that mentions a token.

Heuristic (deterministic, stdlib-only):

* Function-like identifiers written with an opening paren, e.g.
  ``DESeqDataSetFromMatrix(``, ``methRead(``, ``saveRDS(``.
* Backtick-quoted code spans, e.g. ``padj`` or ``methylRawList``.
* Numeric thresholds with the form ``padj < 0.05``,
  ``log2FoldChange >= 2``, ``rtol=1e-3``.
* A small stop-list of generic R/bioinformatics words
  (``function``, ``TRUE``, ``data``, ...) is removed.

All tokens are lower-cased for matching; the unique list is returned in
stable sort order.
"""

from __future__ import annotations

import re
from pathlib import Path


_FUNC_CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_.]{2,})\(")
_BACKTICK_RE = re.compile(r"`([^`\n]{2,80})`")
_THRESHOLD_RE = re.compile(
    r"\b([A-Za-z_][A-Za-z0-9_.]{2,})\s*(?:<=|>=|<|>|==|=|!=)\s*([+-]?\d+\.?\d*(?:[eE][+-]?\d+)?)"
)
_LIBRARY_RE = re.compile(r"\blibrary\(([A-Za-z0-9_.]+)\)")
_PACKAGE_DOUBLE_COLON_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9.]{2,})::([A-Za-z_][A-Za-z0-9_.]+)")

_STOP = {
    "true", "false", "null", "none", "na", "nan", "inf",
    "function", "return", "data", "list", "vector", "matrix",
    "character", "numeric", "integer", "logical", "factor", "array",
    "rows", "cols", "columns", "names", "files", "file", "path", "paths",
    "if", "else", "for", "while", "do", "by", "via", "use", "used", "using",
    "the", "and", "or", "not", "with", "without", "from", "to", "of",
    "cat", "print", "paste", "sprintf", "length", "dim", "nrow", "ncol",
    "head", "tail", "sort", "order", "table", "setwd", "getwd",
    "read.table", "write.table", "read.csv", "write.csv",
    "c", "t", "f",
    "bash", "sh", "zsh", "python", "r",  # shell words
    "example", "note", "notes",
    "etc", "e.g", "i.e",
}


def _ok_token(tok: str) -> bool:
    raw = tok.strip().strip("()`*,;: ")
    t = raw.lower()
    if not t or len(t) < 3:
        return False
    if t in _STOP:
        return False
    if t.replace(".", "").replace("_", "").isdigit():
        return False
    if any(ch.isspace() for ch in t):
        return False
    if raw.isalpha() and raw.islower() and len(raw) < 8 and "_" not in raw and "." not in raw:
        return False
    return True


def extract_tokens_from_skill_text(text: str) -> list[str]:
    """Pull distinctive tokens from a skill markdown blob."""
    if not text:
        return []
    out: set[str] = set()
    for m in _FUNC_CALL_RE.finditer(text):
        out.add(m.group(1))
    for m in _BACKTICK_RE.finditer(text):
        frag = m.group(1).strip()
        if _ok_token(frag) and len(frag) <= 64:
            out.add(frag)
        inner = _FUNC_CALL_RE.search(frag)
        if inner:
            out.add(inner.group(1))
    for m in _THRESHOLD_RE.finditer(text):
        lhs = m.group(1)
        rhs = m.group(2)
        if _ok_token(lhs):
            out.add(lhs)
        triple = f"{lhs} {m.group(0).strip()[len(lhs):].strip()}"
        tight = f"{lhs}{rhs}"
        if len(triple) <= 40:
            out.add(triple)
        out.add(tight)
    for m in _LIBRARY_RE.finditer(text):
        out.add(m.group(1))
    for m in _PACKAGE_DOUBLE_COLON_RE.finditer(text):
        out.add(m.group(1))
        out.add(m.group(2))
        out.add(f"{m.group(1)}::{m.group(2)}")

    cleaned = {t.strip() for t in out}
    final = sorted({t for t in cleaned if _ok_token(t)})
    return final


def extract_tokens_from_skill_md(path: Path) -> list[str]:
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    return extract_tokens_from_skill_text(text)


# ---------------------------------------------------------------------------
# Builder: assemble skill_tokens_v3.json from the three live manifests.
# ---------------------------------------------------------------------------


def build_skill_tokens_v3(
    registry_path: Path,
    paper_manifest: Path,
    pipeline_manifest: Path,
    llm_plan_manifest: Path,
) -> dict:
    """Return ``{ task_id: { arm: [tokens] } }`` for the four known arms.

    The ``none`` arm is always empty: the batch runner injects the
    ``_NO_SKILL_MARKER`` sentinel, i.e. no real skill tokens to attribute.
    """
    import json

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    paper = json.loads(paper_manifest.read_text(encoding="utf-8")) if paper_manifest.is_file() else {}
    pipe = json.loads(pipeline_manifest.read_text(encoding="utf-8")) if pipeline_manifest.is_file() else {}
    plan = json.loads(llm_plan_manifest.read_text(encoding="utf-8")) if llm_plan_manifest.is_file() else {}

    paper_by_task = paper.get("by_task_id", {}) if isinstance(paper, dict) else {}
    pipe_by_wf = pipe.get("by_workflow_id", {}) if isinstance(pipe, dict) else {}
    plan_by_task = plan.get("by_task_id", {}) if isinstance(plan, dict) else {}

    out: dict[str, dict[str, list[str]]] = {}
    for entry in registry.get("tasks", []):
        tid = entry["id"]
        wfid = entry.get("pipeline_workflow_id") or ""
        arms: dict[str, list[str]] = {"none": []}

        paper_entry = paper_by_task.get(tid) or {}
        paper_text = paper_entry.get("skill_md_inline") or ""
        arms["paper"] = extract_tokens_from_skill_text(paper_text)

        pipe_entry = pipe_by_wf.get(wfid) or {}
        pipe_text = pipe_entry.get("skill_md_inline") or ""
        arms["pipeline"] = extract_tokens_from_skill_text(pipe_text)

        plan_entry = plan_by_task.get(tid) or {}
        plan_text = plan_entry.get("skill_md_inline") or ""
        arms["llm_plan"] = extract_tokens_from_skill_text(plan_text)

        out[tid] = arms
    return out


def _main(argv: list[str] | None = None) -> int:
    import argparse
    import json

    here = Path(__file__).resolve().parent
    default_out = here / "skill_tokens_v3.json"
    repo_root = here.parents[4]  # .../Paper2Skills-main
    exp = repo_root / "main" / "paper_primary_benchmark" / "experiments"
    default_registry = here.parents[1] / "r_tasks" / "registry.real.json"

    p = argparse.ArgumentParser(description="Build skill_tokens_v3.json from the three live skill manifests.")
    p.add_argument("--registry", default=str(default_registry))
    p.add_argument("--paper-manifest", default=str(exp / "skills" / "manifest.json"))
    p.add_argument("--pipeline-manifest", default=str(exp / "skills_pipeline" / "manifest.json"))
    p.add_argument("--llm-plan-manifest", default=str(exp / "skills_llm_plan" / "manifest.json"))
    p.add_argument("--out", default=str(default_out))
    args = p.parse_args(argv)

    mapping = build_skill_tokens_v3(
        Path(args.registry),
        Path(args.paper_manifest),
        Path(args.pipeline_manifest),
        Path(args.llm_plan_manifest),
    )
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(mapping, indent=2, sort_keys=True))
    print(f"wrote {args.out}: {len(mapping)} task entries", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
