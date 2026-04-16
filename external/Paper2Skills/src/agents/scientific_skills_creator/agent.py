"""
Paper2SkillCreator: read studies from a training directory and build
a git-managed Python skill library in a workspace repository.
"""
import ast
import json as _json
import os
import logging
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Literal, Dict, Any, Optional, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from src.base_agent import (
    BaseAgent,
    ContentFilterError,
    run_with_retry,
    _is_content_filter_error,
    _strip_images_from_messages,
)
from src.state import AgentState
from src.agents.scientific_skills_creator.prompt import (
    SCIENTIFIC_SKILLS_CREATOR_SYSTEM_PROMPT,
    SINGLE_DOC_USER_MESSAGE_TEMPLATE,
)
from src.agents.scientific_skills_creator.tools import get_scientific_skills_creator_tools
from src.execution import ExecutionResults


# ------------------------------------------------------------------ #
# Token-usage tracking helpers
# ------------------------------------------------------------------ #

def _empty_token_usage() -> Dict[str, int]:
    """Return a zeroed token-usage dict."""
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "llm_calls": 0,
    }


def _add_token_usage(accumulator: Dict[str, int], delta: Dict[str, int]) -> None:
    """Add *delta* counts into *accumulator* in place."""
    for key in ("input_tokens", "output_tokens", "total_tokens", "llm_calls"):
        accumulator[key] = accumulator.get(key, 0) + delta.get(key, 0)


class Paper2SkillCreator(BaseAgent):
    """
    Agent that reads biomedical studies and builds a **git-managed** Python
    skill library.

    The workspace is a git repository.  When ``go()`` is called:

    1. A **single feature branch** is created from ``main`` for the entire
       run (e.g. ``skill/run-20260212-143000``).
    2. For each study the agent reads the paper, writes / updates skill
       modules + tests, and **commits** on that branch.
    3. The agent **does not merge** — the caller decides when to merge
       the branch back to ``main``.

    Organisation hierarchy inside the repo::

        <skill_name>/
        ├── <topic>/
        │   ├── __init__.py
        │   ├── <method>.py          # ≤ 80 lines
        │   ├── docs/<method>.md
        │   └── tests/test_<method>.py
        └── ...

    Typical usage::

        agent = Paper2SkillCreator(
            model_name="gpt-5.2", api_type="azure", api_key="...",
        )
        agent.register_workspace(
            workspace_dir="/path/to/skill-repo"
        )
        agent.go(
            "Explore the materials and create skills.",
            skill_name="rwd_skills",
            train_data_dir="/path/to/studies",
        )
    """

    name = "paper2skill_creator"

    def __init__(
        self,
        model_name: str,
        api_type: str,
        api_key: str,
        endpoint: str = None,
        container_id: str = None,
        model_kwargs: Dict[str, Any] = None,
        llm_timeout: Optional[float] = None,
        recursion_limit: Optional[int] = None,
        compact_token_threshold: int = 100000,
        compact_model_name: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            recursion_limit: Max agent steps per paper invocation.
            compact_token_threshold: Token count before compaction kicks in.
            compact_model_name: Cheaper model for compaction.
        """
        super().__init__(
            model_name=model_name,
            api_type=api_type,
            api_key=api_key,
            endpoint=endpoint,
            container_id=container_id,
            model_kwargs=model_kwargs,
            llm_timeout=llm_timeout,
        )
        self.recursion_limit = recursion_limit
        self.compact_token_threshold = compact_token_threshold
        self.compact_model_name = compact_model_name or "gpt-5-mini"
        self.agent_graph = self._create_agent_graph()

        # Set per-run by go(); kept as instance state so _get_tools / prompts
        # can read them during agent invocation.
        self._skill_name: str = "rwd_skills"
        self._branch_name: str = "main"

        # Token usage tracking — reset per generate() call, accumulated by go()
        self._current_token_usage: Dict[str, int] = _empty_token_usage()

    # ------------------------------------------------------------------
    # Workspace registration
    # ------------------------------------------------------------------
    def register_workspace(self, workspace_dir: str = None, **kwargs) -> bool:
        """
        Register a git repository as the skill library workspace.

        The workspace must already be an initialised git repo (``git init``
        or cloned).
        """
        if workspace_dir is None:
            logging.warning("workspace_dir is required.")
            return False
        self.workdir = os.path.abspath(workspace_dir)
        if not os.path.isdir(self.workdir):
            logging.warning(f"workspace_dir does not exist: {self.workdir}")
            return False

        # Verify it's a git repo
        git_dir = os.path.join(self.workdir, ".git")
        if not os.path.isdir(git_dir):
            logging.warning(
                f"workspace_dir is not a git repo (no .git/): {self.workdir}. "
                f"Initialising with 'git init'."
            )
            subprocess.run(
                ["git", "init"], cwd=self.workdir,
                capture_output=True, text=True,
            )

        logging.info(
            f"Paper2SkillCreator workspace registered: repo={self.workdir}"
        )
        return True

    # ------------------------------------------------------------------
    # Resolved paths
    # ------------------------------------------------------------------
    @property
    def _data_root(self) -> Path:
        """Repo root — tools operate here."""
        return Path(self.workdir)

    @property
    def _skills_root(self) -> Path:
        return Path(self.workdir) / self._skill_name

    # ------------------------------------------------------------------
    # Skill package bootstrap
    # ------------------------------------------------------------------
    def _ensure_skill_package(self) -> None:
        """Create the skill package folder + __init__.py if missing."""
        skill_dir = self._skills_root
        skill_dir.mkdir(parents=True, exist_ok=True)
        init_py = skill_dir / "__init__.py"
        if not init_py.exists():
            init_py.write_text(
                f'"""{self._skill_name} — auto-generated skill package."""\n',
                encoding="utf-8",
            )

    # ------------------------------------------------------------------
    # Document loading
    # ------------------------------------------------------------------
    def _load_docs_from_dir(self, train_data_dir: str) -> List[Dict[str, str]]:
        """
        List every top-level item (file or folder) in *train_data_dir*.

        Each item becomes one iteration for the agent.  A folder is treated
        as a single logical document (e.g. a multi-file study).

        Returns a list of dicts::

            {
                "name":  "paper1.pdf",          # item name
                "path":  "data/paper1.pdf",     # relative or absolute path
                "type":  "file",                # "file" | "folder"
            }

        Items are sorted alphabetically.  Hidden items (``.*``) are skipped.
        """
        data_dir = Path(train_data_dir).resolve()
        if not data_dir.is_dir():
            logging.warning(f"train_data_dir does not exist: {data_dir}")
            return []

        docs: List[Dict[str, str]] = []
        for item in sorted(data_dir.iterdir()):
            if item.name.startswith("."):
                continue  # skip hidden files / folders
            # Make path relative to repo root if possible
            try:
                rel = item.relative_to(self._data_root)
                path_str = str(rel)
            except ValueError:
                path_str = str(item)  # absolute if outside repo
            docs.append({
                "name": item.name,
                "path": path_str,
                "type": "folder" if item.is_dir() else "file",
            })
        return docs

    # ------------------------------------------------------------------
    # Existing skills summary
    # ------------------------------------------------------------------
    def _get_existing_skills_summary(self) -> str:
        """
        Build a summary of existing skills organised by topic.

        If a topic has a ``SKILL.md``, its content is used verbatim (it is
        the authoritative index maintained by the agent).  Otherwise a
        summary is built from AST inspection of the Python modules.

        The root ``SKILL.md`` (if present) is included at the top.
        """
        root = self._skills_root
        if not root.exists():
            return "(No existing skills yet.)"

        sections: List[str] = []

        # ── Root SKILL.md ────────────────────────────────────────────
        root_skill = root / "SKILL.md"
        if root_skill.exists():
            try:
                content = root_skill.read_text(encoding="utf-8", errors="replace").strip()
                # Truncate if very long (keep it concise for the LLM)
                if len(content) > 2000:
                    content = content[:2000] + "\n\n… (truncated)"
                sections.append(content)
            except Exception:
                pass

        # ── Per-topic ─────────────────────────────────────────────────
        topic_parts: List[str] = []
        for topic_dir in sorted(root.iterdir()):
            if not topic_dir.is_dir() or topic_dir.name.startswith("."):
                continue

            topic_skill = topic_dir / "SKILL.md"
            if topic_skill.exists():
                # Use SKILL.md as the authoritative index for this topic
                try:
                    skill_text = topic_skill.read_text(
                        encoding="utf-8", errors="replace"
                    ).strip()
                    if len(skill_text) > 1500:
                        skill_text = skill_text[:1500] + "\n… (truncated)"
                    topic_parts.append(
                        f"### {topic_dir.name}/\n\n{skill_text}"
                    )
                    continue  # SKILL.md is sufficient; skip AST scan
                except Exception:
                    pass  # fall through to AST-based summary

            # Fallback: build summary from Python modules
            module_summaries = []
            for py in sorted(topic_dir.glob("*.py")):
                if py.name.startswith("_"):
                    continue
                funcs = self._extract_public_names(py)
                func_str = ", ".join(funcs[:10]) if funcs else "(empty)"
                if len(funcs) > 10:
                    func_str += f" … +{len(funcs) - 10}"
                module_summaries.append(f"  - {py.stem}: {func_str}")

            # Legacy core.py
            if not module_summaries and (topic_dir / "core.py").exists():
                funcs = self._extract_public_names(topic_dir / "core.py")
                func_str = ", ".join(funcs[:10]) if funcs else "(empty)"
                module_summaries.append(f"  - core: {func_str}")

            # Tests
            test_dir = topic_dir / "tests"
            test_count = sum(
                1 for f in test_dir.iterdir()
                if f.name.startswith("test_") and f.suffix == ".py"
            ) if test_dir.is_dir() else 0

            lines = [f"### {topic_dir.name}/ (no SKILL.md yet)"]
            if module_summaries:
                lines.append("Modules:")
                lines.extend(module_summaries)
            else:
                lines.append("Modules: (none yet)")
            lines.append(f"Test files: {test_count}")
            topic_parts.append("\n".join(lines))

        if topic_parts:
            sections.append("\n\n".join(topic_parts))

        return "\n\n".join(sections) if sections else "(No existing skills yet.)"

    @staticmethod
    def _extract_public_names(py_file: Path) -> List[str]:
        """Parse a Python file and return public function/class names."""
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(py_file))
        except (SyntaxError, ValueError):
            return []
        names: List[str] = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    names.append(node.name)
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    names.append(node.name)
        return names

    @staticmethod
    def _extract_md_description(md_path: Path) -> str:
        """Extract ``description`` from YAML frontmatter of a .md file."""
        try:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""
        match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            return ""
        for line in match.group(1).split("\n"):
            if line.startswith("description:"):
                return line.replace("description:", "").strip()
        return ""

    # ------------------------------------------------------------------
    # Tools / graph
    # ------------------------------------------------------------------
    def _get_tools(self):
        return {
            t.name: t
            for t in get_scientific_skills_creator_tools(
                data_root=self._data_root,
                skills_root=self._skills_root,
            )
        }

    def _get_system_prompt(self) -> str:
        return SCIENTIFIC_SKILLS_CREATOR_SYSTEM_PROMPT.format(
            workdir=self.workdir,
            skill_name=self._skill_name,
            branch_name=self._branch_name,
        )

    # ------------------------------------------------------------------
    # Agent node
    # ------------------------------------------------------------------
    def _agent_node(self, state: AgentState, config: RunnableConfig) -> Dict:
        messages = [SystemMessage(content=self._get_system_prompt())] + list(
            state.messages
        )
        messages = self._compact_messages(
            messages,
            token_threshold=self.compact_token_threshold,
            compact_model_name=self.compact_model_name,
        )
        model_kwargs = config.get("configurable", {}).get("model_kwargs", {}) or {}
        llm = self._get_model(
            api=self.api_type,
            model_name=self.model_name,
            api_key=self.api_key,
            endpoint=self.endpoint,
            **{**(self.model_kwargs or {}), **model_kwargs},
        )
        tool_list = list(self._get_tools().values())
        llm_with_tools = llm.bind_tools(tool_list, parallel_tool_calls=False)

        try:
            response = run_with_retry(
                llm_with_tools.invoke, arg=messages, timeout=self.llm_timeout
            )
        except Exception as exc:
            if not _is_content_filter_error(exc):
                raise
            # -- Self-heal: content filter triggered -----------------------
            # The conversation likely contains images (PDF pages) or raw
            # biomedical text that Azure's filter flags as sensitive.
            # Strategy: strip all images, force-compact, and retry once.
            logging.warning(
                "Content filter triggered — stripping images and "
                "compacting conversation for retry."
            )
            sanitized = _strip_images_from_messages(messages)
            sanitized = self._compact_messages(
                sanitized,
                token_threshold=0,  # force compaction regardless of size
                compact_model_name=self.compact_model_name,
            )
            try:
                response = run_with_retry(
                    llm_with_tools.invoke,
                    arg=sanitized,
                    timeout=self.llm_timeout,
                )
            except Exception as inner_exc:
                if _is_content_filter_error(inner_exc):
                    raise ContentFilterError(inner_exc) from inner_exc
                raise

        # -- Track token usage from response metadata --
        usage = getattr(response, "usage_metadata", None) or {}
        if usage:
            inp = usage.get("input_tokens", 0)
            out = usage.get("output_tokens", 0)
            self._current_token_usage["input_tokens"] += inp
            self._current_token_usage["output_tokens"] += out
            self._current_token_usage["total_tokens"] += inp + out
            self._current_token_usage["llm_calls"] += 1

        return {"messages": [response]}

    def _tool_node(self, state: AgentState, config: RunnableConfig) -> Dict:
        last = state.messages[-1]
        if not isinstance(last, AIMessage) or not last.tool_calls:
            return {}
        tool_call = last.tool_calls[0]
        name = tool_call["name"]
        args = tool_call.get("args") or {}
        tool = self._get_tools()[name]
        out = tool._run(**args)
        msg = self._build_tool_message(out, name=name, tool_call_id=tool_call["id"])
        return {"messages": [msg]}

    def _should_continue(self, state: AgentState) -> Literal["tool_node", "end"]:
        if not state.messages:
            return "end"
        last = state.messages[-1]
        if isinstance(last, AIMessage) and last.tool_calls:
            return "tool_node"
        return "end"

    def _create_agent_graph(self):
        wf = StateGraph(AgentState, input=AgentState, output=AgentState)
        wf.add_node("agent_node", self._agent_node)
        wf.add_node("tool_node", self._tool_node)
        wf.add_conditional_edges(
            "agent_node",
            self._should_continue,
            {"tool_node": "tool_node", "end": END},
        )
        wf.add_edge("tool_node", "agent_node")
        wf.set_entry_point("agent_node")
        return wf.compile(debug=False, name=self.name)

    # ------------------------------------------------------------------
    # Git helpers (run before/between agent invocations)
    # ------------------------------------------------------------------
    def _git_ensure_main(self) -> None:
        """Ensure the repo is on main branch."""
        subprocess.run(
            ["git", "checkout", "main"],
            cwd=self.workdir, capture_output=True, text=True,
        )

    def _git_current_branch(self) -> str:
        """Return the current git branch name."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=self.workdir, capture_output=True, text=True,
        )
        return result.stdout.strip()

    def _git_create_branch(self, branch_name: str) -> None:
        """Create and checkout a new branch from the current HEAD."""
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=self.workdir, capture_output=True, text=True,
        )

    def _git_checkout(self, branch_name: str) -> None:
        """Checkout an existing branch."""
        subprocess.run(
            ["git", "checkout", branch_name],
            cwd=self.workdir, capture_output=True, text=True,
        )

    def _git_branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists locally."""
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch_name],
            cwd=self.workdir, capture_output=True, text=True,
        )
        return result.returncode == 0

    # ------------------------------------------------------------------
    # Token usage reporting
    # ------------------------------------------------------------------
    @staticmethod
    def _build_token_usage_report(
        total_token_usage: Dict[str, int],
        per_doc_token_usage: List[Dict[str, Any]],
        run_duration_seconds: float,
        model_name: str,
    ) -> Dict[str, Any]:
        """Build a structured token-usage report for the entire run."""
        completed = [d for d in per_doc_token_usage if d["status"] == "completed"]
        avg_input = (
            total_token_usage["input_tokens"] / len(completed)
            if completed else 0
        )
        avg_output = (
            total_token_usage["output_tokens"] / len(completed)
            if completed else 0
        )
        avg_total = (
            total_token_usage["total_tokens"] / len(completed)
            if completed else 0
        )
        avg_calls = (
            total_token_usage["llm_calls"] / len(completed)
            if completed else 0
        )
        avg_duration = (
            sum(d.get("duration_seconds", 0) for d in completed) / len(completed)
            if completed else 0
        )
        return {
            "model": model_name,
            "run_timestamp": datetime.now().isoformat(),
            "run_duration_seconds": round(run_duration_seconds, 1),
            "docs_total": len(per_doc_token_usage),
            "docs_completed": len(completed),
            "docs_skipped": len(per_doc_token_usage) - len(completed),
            "totals": total_token_usage,
            "averages_per_doc": {
                "input_tokens": round(avg_input),
                "output_tokens": round(avg_output),
                "total_tokens": round(avg_total),
                "llm_calls": round(avg_calls, 1),
                "duration_seconds": round(avg_duration, 1),
            },
            "per_doc": per_doc_token_usage,
        }

    def _save_token_usage_report(self, report: Dict[str, Any]) -> Path:
        """Persist the token-usage report as JSON in the workspace."""
        reports_dir = Path(self.workdir) / ".token_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = reports_dir / f"token_usage_{ts}.json"
        path.write_text(
            _json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return path

    @staticmethod
    def _print_doc_token_summary(
        doc: Dict[str, str], doc_usage: Dict[str, Any]
    ) -> None:
        """Print a single-document token summary line."""
        tokens = doc_usage.get("tokens", {})
        duration = doc_usage.get("duration_seconds", 0)
        status = doc_usage.get("status", "?")
        print(
            f"  ── Tokens for '{doc['name']}': "
            f"input={tokens.get('input_tokens', 0):,}  "
            f"output={tokens.get('output_tokens', 0):,}  "
            f"total={tokens.get('total_tokens', 0):,}  "
            f"calls={tokens.get('llm_calls', 0)}  "
            f"time={duration:.0f}s  "
            f"status={status}"
        )

    @staticmethod
    def _print_run_token_summary(
        report: Dict[str, Any], report_path: Path
    ) -> None:
        """Print a full-run token summary table."""
        totals = report["totals"]
        avgs = report["averages_per_doc"]
        print("\n" + "=" * 80)
        print("TOKEN USAGE SUMMARY")
        print("=" * 80)
        print(f"  Model:              {report['model']}")
        print(f"  Run duration:       {report['run_duration_seconds']:.0f}s")
        print(
            f"  Documents:          {report['docs_completed']} completed, "
            f"{report['docs_skipped']} skipped, "
            f"{report['docs_total']} total"
        )
        print(f"  ─── Totals ───")
        print(f"    Input tokens:     {totals['input_tokens']:,}")
        print(f"    Output tokens:    {totals['output_tokens']:,}")
        print(f"    Total tokens:     {totals['total_tokens']:,}")
        print(f"    LLM calls:        {totals['llm_calls']:,}")
        print(f"  ─── Averages per document ───")
        print(f"    Input tokens:     {avgs['input_tokens']:,}")
        print(f"    Output tokens:    {avgs['output_tokens']:,}")
        print(f"    Total tokens:     {avgs['total_tokens']:,}")
        print(f"    LLM calls:        {avgs['llm_calls']}")
        print(f"    Duration:         {avgs['duration_seconds']:.0f}s")
        print(f"  Report saved to:    {report_path}")
        print("=" * 80 + "\n")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate(self, input_query: str, verbose: bool = True, **kwargs) -> Dict[str, Any]:
        # Reset per-invocation token counter
        self._current_token_usage = _empty_token_usage()

        inputs = {"messages": [("user", input_query)]}
        config = kwargs.get("config") or {}
        config.setdefault(
            "recursion_limit",
            self.recursion_limit if self.recursion_limit is not None else 500,
        )
        result = None
        for stream_mode, chunk in self.agent_graph.stream(
            inputs, stream_mode=["values"], config=config
        ):
            if verbose:
                self._print_stream_chunk(chunk)
            result = chunk

        out = result or {}
        # Attach token usage so callers (go()) can read it
        out["token_usage"] = dict(self._current_token_usage)
        return out

    def go(
        self,
        input_query: str,
        verbose: bool = True,
        skill_name: str = "rwd_skills",
        branch_name: Optional[str] = None,
        train_data_dir: Optional[str] = None,
        **kwargs,
    ) -> ExecutionResults:
        """
        Run the agent on documents from ``train_data_dir``.

        Each top-level item (file or folder) in the directory becomes one
        iteration.  The agent is invoked independently for each document.
        All work happens on a **single branch** — no merging, no per-doc
        branches.

        Args:
            input_query: Fallback query if no training data is found.
            skill_name: Name of the skill package inside the repo (e.g.
                ``"rwd_skills"``). Can be new or existing.
            branch_name: Git branch to work on.  If ``None``, a timestamped
                branch is auto-generated (``skill/run-YYYYMMDD-HHMMSS``).
                If the branch already exists it is checked out; otherwise
                it is created from ``main``.
            train_data_dir: Directory whose top-level items (files and
                folders) are each treated as one document to learn from.
        """
        # -- Set per-run state -----------------------------------------
        self._skill_name = skill_name
        self._ensure_skill_package()

        # -- Resolve branch name ---------------------------------------
        if branch_name is None:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            branch_name = f"skill/run-{ts}"
        self._branch_name = branch_name

        if verbose:
            print("\n" + "=" * 80)
            print("Paper2SkillCreator — git-managed skill library")
            print(f"  repo:          {self.workdir}")
            print(f"  skill_name:    {self._skill_name}")
            print(f"  branch:        {self._branch_name}")
            if train_data_dir:
                print(f"  train data:    {train_data_dir}")
            print("=" * 80 + "\n")

        # -- Create or checkout branch ---------------------------------
        if self._git_branch_exists(self._branch_name):
            self._git_checkout(self._branch_name)
            if verbose:
                print(f"Checked out existing branch: {self._branch_name}\n")
        else:
            self._git_ensure_main()
            self._git_create_branch(self._branch_name)
            if verbose:
                print(f"Created branch from main: {self._branch_name}\n")

        # -- Load documents --------------------------------------------
        docs: List[Dict[str, str]] = []
        if train_data_dir:
            docs = self._load_docs_from_dir(train_data_dir)
            if verbose:
                n_files = sum(1 for d in docs if d["type"] == "file")
                n_folders = sum(1 for d in docs if d["type"] == "folder")
                print(
                    f"Found {len(docs)} document(s) "
                    f"({n_files} files, {n_folders} folders).\n"
                )

        if not docs:
            # Fallback: single generate
            result = self.generate(input_query, verbose=verbose, **kwargs)
            messages = result.get("messages") or []
            fallback_usage = result.get("token_usage", _empty_token_usage())
            if verbose and fallback_usage.get("total_tokens", 0) > 0:
                print(
                    f"  ── Tokens: input={fallback_usage['input_tokens']:,}  "
                    f"output={fallback_usage['output_tokens']:,}  "
                    f"total={fallback_usage['total_tokens']:,}  "
                    f"calls={fallback_usage['llm_calls']}"
                )
            return ExecutionResults(
                sandbox=self.sandbox,
                message_history=self._format_messages(messages),
                code_execution_results=self._format_code_execution_results(
                    result.get("code_execution_results") or []
                ),
                final_response=messages[-1].content if messages else "",
                token_usage={"totals": fallback_usage, "per_doc": []},
            )

        # -- One agent run per document --------------------------------
        all_message_history: List[Dict[str, str]] = []
        all_code_results: list = []
        default_recursion = (
            self.recursion_limit if self.recursion_limit is not None else 50
        )
        config = kwargs.get("config") or {}
        config = {
            **config,
            "recursion_limit": config.get("recursion_limit", default_recursion),
        }

        last_final_content = ""
        skipped_recursion: List[str] = []
        skipped_content_filter: List[str] = []
        processed_count = 0

        # Token usage tracking
        total_token_usage = _empty_token_usage()
        per_doc_token_usage: List[Dict[str, Any]] = []
        run_start_time = datetime.now()

        for i, doc in enumerate(docs):
            if verbose:
                print("\n" + "=" * 80)
                print(
                    f"Document {i + 1}/{len(docs)}: "
                    f"{doc['name']}  ({doc['type']})"
                )
                print("=" * 80 + "\n")

            existing_skills = self._get_existing_skills_summary()
            user_message = SINGLE_DOC_USER_MESSAGE_TEMPLATE.format(
                doc_name=doc["name"],
                doc_path=doc["path"],
                doc_type=doc["type"],
                existing_skills_summary=existing_skills,
                skill_name=self._skill_name,
            )

            doc_start_time = datetime.now()
            doc_usage: Dict[str, Any] = {
                "doc_name": doc["name"],
                "doc_path": doc["path"],
                "doc_type": doc["type"],
                "status": "completed",
            }

            try:
                result = self.generate(
                    user_message,
                    verbose=verbose,
                    config=config,
                    **{k: v for k, v in kwargs.items() if k != "config"},
                )
            except Exception as e:
                err_msg = str(e).lower()
                is_recursion = (
                    "recursion" in err_msg or "recursion_limit" in err_msg
                )
                is_filter = isinstance(e, ContentFilterError) or _is_content_filter_error(e)

                if is_recursion or is_filter:
                    reason = (
                        "content_filter" if is_filter
                        else "recursion_limit"
                    )
                    if is_filter:
                        skipped_content_filter.append(doc["name"])
                    else:
                        skipped_recursion.append(doc["name"])

                    doc_usage["status"] = f"skipped_{reason}"
                    doc_usage["tokens"] = dict(self._current_token_usage)
                    doc_usage["duration_seconds"] = (
                        datetime.now() - doc_start_time
                    ).total_seconds()
                    per_doc_token_usage.append(doc_usage)
                    _add_token_usage(total_token_usage, self._current_token_usage)
                    if verbose:
                        self._print_doc_token_summary(doc, doc_usage)
                        print(
                            f"[Skipped] '{doc['name']}' hit {reason}; "
                            f"continuing.\n"
                        )
                    logging.warning(
                        "Skipping doc '%s' due to %s: %s",
                        doc["name"], reason, e,
                    )
                    # Ensure we're still on the right branch
                    current = self._git_current_branch()
                    if current != self._branch_name:
                        self._git_checkout(self._branch_name)
                    continue
                raise

            # Record token usage for this document
            doc_token = result.get("token_usage", _empty_token_usage())
            doc_usage["tokens"] = doc_token
            doc_usage["duration_seconds"] = (
                datetime.now() - doc_start_time
            ).total_seconds()
            per_doc_token_usage.append(doc_usage)
            _add_token_usage(total_token_usage, doc_token)

            if verbose:
                self._print_doc_token_summary(doc, doc_usage)

            messages = result.get("messages") or []
            all_message_history.extend(self._format_messages(messages))
            all_code_results.extend(result.get("code_execution_results") or [])
            if messages:
                last_final_content = getattr(messages[-1], "content", "") or ""
            processed_count += 1

            # Safety: ensure we're still on the right branch
            current = self._git_current_branch()
            if current != self._branch_name:
                if verbose:
                    print(
                        f"[Warning] Agent switched to branch '{current}'. "
                        f"Switching back to '{self._branch_name}'.\n"
                    )
                self._git_checkout(self._branch_name)

        # -- Build token usage report ----------------------------------
        run_duration = (datetime.now() - run_start_time).total_seconds()
        token_usage_report = self._build_token_usage_report(
            total_token_usage=total_token_usage,
            per_doc_token_usage=per_doc_token_usage,
            run_duration_seconds=run_duration,
            model_name=self.model_name,
        )

        # Save token usage report to workspace
        report_path = self._save_token_usage_report(token_usage_report)

        if verbose:
            self._print_run_token_summary(token_usage_report, report_path)

        final_response = (
            f"Processed {processed_count}/{len(docs)} documents "
            f"on branch '{self._branch_name}'."
        )
        if skipped_recursion:
            final_response += (
                f" Skipped (recursion limit): {skipped_recursion}."
            )
        if skipped_content_filter:
            final_response += (
                f" Skipped (content filter): {skipped_content_filter}."
            )
        if last_final_content:
            final_response += f"\n\nLast run:\n\n{last_final_content}"
        return ExecutionResults(
            sandbox=self.sandbox,
            message_history=all_message_history,
            code_execution_results=self._format_code_execution_results(
                all_code_results
            ),
            final_response=final_response,
            token_usage=token_usage_report,
        )
