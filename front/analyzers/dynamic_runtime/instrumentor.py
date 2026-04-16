from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import libcst as cst

RUNTIME_HOOK_FILENAME = "agentic_runtime_hooks.py"
IMPORT_LINE = "from agentic_runtime_hooks import ac_track_call\n"

EXCLUDE_PARTS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache"}


def _call_name(node: cst.BaseExpression) -> str:
    if isinstance(node, cst.Name):
        return node.value
    if isinstance(node, cst.Attribute):
        return f"{_call_name(node.value)}.{node.attr.value}"
    return "unknown"


def _classify(call_name: str) -> str | None:
    lowered = call_name.lower()
    if any(k in lowered for k in ("openai", "anthropic", "chat.completions", "responses.create", "messages.create")):
        return "llm_call"
    if any(k in lowered for k in ("subprocess", "os.system", "requests.", "httpx.", "tool", "invoke", "execute")):
        return "tool_call"
    if any(k in lowered for k in ("send", "publish", "emit", "receive", "recv", "message")):
        return "message_call"
    if any(k in lowered for k in ("retry", "rollback", "compensate")):
        return "retry_call"
    return None


class CallInstrumentationTransformer(cst.CSTTransformer):
    def __init__(self) -> None:
        self.touched = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        name = _call_name(updated_node.func)
        kind = _classify(name)
        if not kind:
            return updated_node
        self.touched = True
        args = [
            cst.Arg(value=cst.SimpleString(f"'{kind}'")),
            cst.Arg(value=cst.SimpleString(f"'{name}'")),
            cst.Arg(value=updated_node.func),
        ]
        args.extend(updated_node.args)
        return cst.Call(func=cst.Name("ac_track_call"), args=args)


def _is_docstring_stmt(stmt: cst.CSTNode) -> bool:
    if not isinstance(stmt, cst.SimpleStatementLine):
        return False
    if len(stmt.body) != 1:
        return False
    expr = stmt.body[0]
    if not isinstance(expr, cst.Expr):
        return False
    return isinstance(expr.value, cst.SimpleString)


def _is_future_import(stmt: cst.CSTNode) -> bool:
    if not isinstance(stmt, cst.SimpleStatementLine):
        return False
    for item in stmt.body:
        if isinstance(item, cst.ImportFrom) and isinstance(item.module, cst.Name):
            if item.module.value == "__future__":
                return True
    return False


def _inject_import(module: cst.Module) -> cst.Module:
    if "agentic_runtime_hooks" in module.code:
        return module
    body = list(module.body)
    idx = 0
    if idx < len(body) and _is_docstring_stmt(body[idx]):
        idx += 1
    while idx < len(body) and _is_future_import(body[idx]):
        idx += 1
    body.insert(idx, cst.parse_statement(IMPORT_LINE))
    return module.with_changes(body=body)


@dataclass
class InstrumentationResult:
    files_total: int
    files_touched: int

    @property
    def coverage(self) -> float:
        if self.files_total == 0:
            return 0.0
        return self.files_touched / self.files_total


def _discover_python_files(repo_path: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_path.rglob("*.py"):
        if any(part in EXCLUDE_PARTS for part in path.parts):
            continue
        if path.name == RUNTIME_HOOK_FILENAME:
            continue
        files.append(path)
    return files


def _runtime_hook_source() -> str:
    source = Path(__file__).with_name("runtime_hooks.py").read_text(encoding="utf-8")
    return source


def instrument_python_repo(repo_path: Path) -> InstrumentationResult:
    files = _discover_python_files(repo_path)
    touched = 0

    hooks_path = repo_path / RUNTIME_HOOK_FILENAME
    hooks_path.write_text(_runtime_hook_source(), encoding="utf-8")

    for path in files:
        source = path.read_text(encoding="utf-8", errors="ignore")
        try:
            module = cst.parse_module(source)
        except Exception:
            continue
        transformer = CallInstrumentationTransformer()
        updated = module.visit(transformer)
        if not transformer.touched:
            continue
        updated = _inject_import(updated)
        new_source = updated.code
        path.write_text(new_source, encoding="utf-8")
        touched += 1

    return InstrumentationResult(files_total=len(files), files_touched=touched)
