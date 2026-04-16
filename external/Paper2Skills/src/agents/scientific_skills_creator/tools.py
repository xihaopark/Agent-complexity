"""Tools for Paper2SkillCreator. Agent-specific + imports from src.tool_wrappers."""
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Type, List, Optional

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from src.tool_wrappers.bash_tool import BashInWorkspaceTool
from src.tool_wrappers.file_tools import WriteFileTool, EditFileTool
from src.tool_wrappers.search_tools import GlobInWorkspaceTool, GrepInWorkspaceTool
from src.tool_wrappers.multimodal_tools import ReadImageTool, ReadPdfTool
from src.tool_wrappers.todo_tool import TodoWriteTool


DEFAULT_PROCESSED_STATE = {
    "processed_docs": [],
    "last_updated": None,
    "category_to_docs": {},
}


class ReadProcessedStateInput(BaseModel):
    check_doc: Optional[str] = Field(
        default=None,
        description="If set, return whether this document is already processed and which category.",
    )


class ReadProcessedStateTool(BaseTool):
    name: str = "read_processed_state"
    description: str = (
        "Read the current processed-documents state. "
        "Optionally pass check_doc to see if a specific document is already processed."
    )
    args_schema: Type[BaseModel] = ReadProcessedStateInput
    skills_root: Path = None  # type: ignore[assignment]

    def __init__(self, skills_root: Path, **kwargs):
        super().__init__(**kwargs)
        self.skills_root = Path(skills_root)

    def _run(self, check_doc: Optional[str] = None) -> str:
        state_path = self.skills_root / ".processed.json"
        if not state_path.exists():
            state = dict(DEFAULT_PROCESSED_STATE)
        else:
            try:
                with open(state_path, encoding="utf-8") as f:
                    state = json.load(f)
            except Exception as e:
                return f"Error reading .processed.json: {e}"
        processed = set(state.get("processed_docs") or [])
        cat_docs = state.get("category_to_docs") or {}
        if check_doc:
            doc = str(check_doc).strip()
            if doc in processed:
                for cat, docs in cat_docs.items():
                    if doc in (docs or []):
                        return f"Document '{doc}' is already processed (category: {cat})."
                return f"Document '{doc}' is already processed."
            return f"Document '{doc}' is not yet processed."
        total = len(processed)
        summary = {"total_processed_docs": total, "categories": {}}
        for cat, docs in cat_docs.items():
            summary["categories"][cat] = len(docs or [])
        return json.dumps(summary, indent=2)


class MarkDocsProcessedInput(BaseModel):
    doc_names: List[str] = Field(description="List of document names to mark as processed (delta).")
    category: str = Field(description="Topic name (e.g. causal_inference) to associate.")


class MarkDocsProcessedTool(BaseTool):
    name: str = "mark_docs_processed"
    description: str = (
        "Delta update: add document name(s) to .processed.json under the given category. "
        "Also regenerates CATEGORIES.md."
    )
    args_schema: Type[BaseModel] = MarkDocsProcessedInput
    skills_root: Path = None  # type: ignore[assignment]

    def __init__(self, skills_root: Path, **kwargs):
        super().__init__(**kwargs)
        self.skills_root = Path(skills_root)

    def _run(self, doc_names: List[str], category: str) -> str:
        state_path = self.skills_root / ".processed.json"
        state = dict(DEFAULT_PROCESSED_STATE)
        if state_path.exists():
            try:
                with open(state_path, encoding="utf-8") as f:
                    state = json.load(f)
            except Exception as e:
                return f"Error reading .processed.json: {e}"
        seen = set(state.get("processed_docs") or [])
        for d in doc_names:
            d = str(d).strip()
            if d and d not in seen:
                state.setdefault("processed_docs", []).append(d)
                seen.add(d)
        cat = category.strip()
        state.setdefault("category_to_docs", {})
        if cat not in state["category_to_docs"]:
            state["category_to_docs"][cat] = []
        for d in doc_names:
            d = str(d).strip()
            if d and d not in state["category_to_docs"][cat]:
                state["category_to_docs"][cat].append(d)
        state["last_updated"] = datetime.utcnow().isoformat() + "Z"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        lines = [
            "# Skill topics\n",
            "| Topic | Modules | Source documents |",
            "|-------|---------|-----------------|",
        ]
        for td in sorted(self.skills_root.iterdir()):
            if not td.is_dir() or td.name.startswith("."):
                continue
            modules = sorted(f.stem for f in td.glob("*.py") if not f.name.startswith("_"))
            if not modules and (td / "core.py").exists():
                modules = ["core"]
            if not modules and not (td / "__init__.py").exists():
                continue
            mod_str = ", ".join(modules[:8])
            if len(modules) > 8:
                mod_str += f" … +{len(modules) - 8}"
            doc_list = state["category_to_docs"].get(td.name, [])
            doc_str = ", ".join(doc_list[:10]) + (" …" if len(doc_list) > 10 else "")
            lines.append(f"| {td.name} | {mod_str} | {doc_str} |")
        (self.skills_root / "CATEGORIES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return f"Marked {len(doc_names)} document(s) as processed for category '{cat}'. Updated .processed.json and CATEGORIES.md."


class RunTestsInput(BaseModel):
    skill_module: str = Field(
        description="Topic directory name under the skills root (e.g. 'causal_inference'). Tests at <topic>/tests/."
    )
    extra_args: Optional[str] = Field(default=None, description="Optional extra pytest arguments.")


class RunTestsTool(BaseTool):
    name: str = "run_tests"
    description: str = (
        "Run pytest on a topic's test suite. Provide the skill_module name (topic directory)."
    )
    args_schema: Type[BaseModel] = RunTestsInput
    data_root: Path = None  # type: ignore[assignment]
    skills_root: Path = None  # type: ignore[assignment]
    timeout_seconds: int = 120

    def __init__(self, data_root: Path, skills_root: Path, timeout_seconds: int = 120, **kwargs):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve()
        self.skills_root = Path(skills_root).resolve()
        self.timeout_seconds = timeout_seconds

    def _run(self, skill_module: str, extra_args: Optional[str] = None) -> str:
        skill_module = skill_module.strip().strip("/")
        if ".." in skill_module or "/" in skill_module:
            return f"Error: skill_module must be a simple directory name, got '{skill_module}'."
        test_dir = self.skills_root / skill_module / "tests"
        if not test_dir.exists():
            return f"Error: test directory not found: {skill_module}/tests/. Create tests first."
        rel_test_path = f"{self.skills_root.name}/{skill_module}/tests/"
        cmd = f"python -m pytest {rel_test_path} -v --tb=short --no-header"
        if extra_args:
            cmd += f" {extra_args}"
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(self.data_root),
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            out = (result.stdout or "").strip()
            err = (result.stderr or "").strip()
            lines = [f"$ {cmd}"]
            if out:
                lines.append(out)
            if err:
                err_lines = [ln for ln in err.splitlines() if not ln.strip().startswith("PytestUnraisable")]
                filtered_err = "\n".join(err_lines).strip()
                if filtered_err:
                    lines.append(f"stderr:\n{filtered_err}")
            if result.returncode == 0:
                lines.append("\n✓ All tests passed.")
            else:
                lines.append(f"\n✗ Tests failed (exit code {result.returncode}).")
            return "\n".join(lines)
        except subprocess.TimeoutExpired:
            return f"$ {cmd}\n\nError: tests timed out after {self.timeout_seconds}s."
        except Exception as e:
            return f"$ {cmd}\n\nError: {e}"


def get_scientific_skills_creator_tools(data_root: Path, skills_root: Path) -> List[BaseTool]:
    return [
        WriteFileTool(data_root=data_root),
        EditFileTool(data_root=data_root),
        GlobInWorkspaceTool(data_root=data_root),
        GrepInWorkspaceTool(data_root=data_root),
        BashInWorkspaceTool(data_root=data_root),
        ReadProcessedStateTool(skills_root=skills_root),
        MarkDocsProcessedTool(skills_root=skills_root),
        RunTestsTool(data_root=data_root, skills_root=skills_root),
        ReadImageTool(data_root=data_root),
        ReadPdfTool(data_root=data_root),
        TodoWriteTool(data_root=data_root),
    ]
