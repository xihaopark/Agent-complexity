"""R-task evaluation environment compatible with aviary Environment + ldp rollout loop."""

from __future__ import annotations

import asyncio
import json
import logging
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from aviary.core import Environment, Messages, Tool, ToolRequestMessage
from aviary.message import Message
from aviary.tools import ToolResponseMessage

logger = logging.getLogger(__name__)


@dataclass
class RTaskEvalState:
    """Mutable state for RTaskEvalEnv."""

    work_dir: Path
    done: bool = False
    truncated: bool = False
    total_reward: float = 0.0
    step_index: int = 0
    actions: list[str] = field(default_factory=list)
    last_tool_output: str = ""


def _list_dir_json(root: Path, max_depth: int = 4) -> dict[str, Any]:
    """Nested dict of files under root (bounded depth)."""

    def walk(p: Path, depth: int) -> dict[str, Any]:
        if depth > max_depth:
            return {"_truncated": True}
        if p.is_file():
            return {"_file": p.name, "_size": p.stat().st_size}
        out: dict[str, Any] = {}
        try:
            for c in sorted(p.iterdir(), key=lambda x: x.name):
                if c.name.startswith("."):
                    continue
                out[c.name] = walk(c, depth + 1) if c.is_dir() else {"_file": c.name}
        except OSError as e:
            return {"_error": str(e)}
        return out

    return walk(root, 0)


class RTaskEvalEnv(Environment[RTaskEvalState]):
    """Filesystem + shell + Rscript tools; no Snakemake, no notebook kernel required."""

    state: RTaskEvalState
    tools: list[Tool]

    def __init__(
        self,
        *,
        task_id: str,
        work_dir: str | Path,
        objective_text: str | None = None,
        objective_file: str | Path | None = None,
        success_artifact_glob: str | None = "output/result.txt",
        shell_timeout_s: float = 300.0,
        max_steps_soft_trunc: int | None = None,
    ) -> None:
        self.task_id = task_id
        self._work_dir = Path(work_dir).resolve()
        self._objective_text = objective_text
        self._objective_file = Path(objective_file) if objective_file else None
        self.success_artifact_glob = success_artifact_glob
        self.shell_timeout_s = shell_timeout_s
        self.max_steps_soft_trunc = max_steps_soft_trunc
        self.tools = [
            Tool.from_function(self.run_shell),
            Tool.from_function(self.read_text_file),
            Tool.from_function(self.write_text_file),
            Tool.from_function(self.run_rscript),
            Tool.from_function(self.list_workdir),
            Tool.from_function(self.write_plan),
            Tool.from_function(self.check_progress),
            Tool.from_function(self.submit_done),
        ]

    def _safe_path(self, relative: str) -> Path:
        p = (self.state.work_dir / relative).resolve()
        if not str(p).startswith(str(self.state.work_dir)):
            raise ValueError(f"Path escapes work_dir: {relative}")
        return p

    def _load_objective(self) -> str:
        if self._objective_text:
            return self._objective_text.strip()
        path = self._objective_file or (self._work_dir / "OBJECTIVE.md")
        if path.is_file():
            return path.read_text(encoding="utf-8").strip()
        return (
            f"Complete the analysis in task `{self.task_id}`. "
            "Use tools to inspect files, run R or shell as needed, then call submit_done."
        )

    async def reset(self) -> tuple[Messages, list[Tool]]:
        self._work_dir.mkdir(parents=True, exist_ok=True)
        self.state = RTaskEvalState(work_dir=self._work_dir)
        intro = self._load_objective()
        tree = _list_dir_json(self._work_dir)
        body = (
            f"# Task `{self.task_id}`\n\n{intro}\n\n"
            f"## Workspace (read-only summary)\n```json\n{json.dumps(tree, indent=2)}\n```\n"
        )
        if self.success_artifact_glob:
            body += (
                f"\nSuccess hint: when `{self.success_artifact_glob}` exists under the workspace, "
                "you may call submit_done(success=true).\n"
            )
        obs = cast(Messages, [Message(role="user", content=body)])
        return obs, self.tools

    async def step(
        self, action: ToolRequestMessage
    ) -> tuple[Messages, float, bool, bool]:
        prev = self.state.total_reward
        self.state.step_index += 1
        obs = cast(
            Messages,
            await self.exec_tool_calls(action, concurrency=False, handle_tool_exc=True),
        )
        reward = self.state.total_reward - prev
        if self.max_steps_soft_trunc and self.state.step_index >= self.max_steps_soft_trunc:
            self.state.truncated = True
        trunc = self.state.truncated
        done = self.state.done
        return obs, reward, done, trunc

    # --- tools (sync; exec_tool_calls runs in thread) ---

    def run_shell(self, command: str) -> str:
        """Run a shell command in the task work_dir (bash -lc).

        Args:
            command: Shell command string passed to `bash -lc`.
        """
        self.state.actions.append(f"shell:{command[:200]}")
        try:
            p = subprocess.run(
                ["bash", "-lc", command],
                cwd=self.state.work_dir,
                capture_output=True,
                text=True,
                timeout=self.shell_timeout_s,
            )
            out = f"exit={p.returncode}\nstdout:\n{p.stdout[:24000]}\nstderr:\n{p.stderr[:8000]}"
            self.state.last_tool_output = out[:4000]
            return out
        except subprocess.TimeoutExpired:
            return "ERROR: command timed out"

    def read_text_file(self, relative_path: str) -> str:
        """Read a UTF-8 text file relative to work_dir.

        Args:
            relative_path: Path under the workspace (not absolute).
        """
        path = self._safe_path(relative_path)
        if not path.is_file():
            return f"ERROR: not a file: {relative_path}"
        return path.read_text(encoding="utf-8", errors="replace")[:100_000]

    def write_text_file(self, relative_path: str, content: str) -> str:
        """Write text to a path under work_dir (creates parent dirs).

        Args:
            relative_path: Path under the workspace (not absolute).
            content: Full file body to write as UTF-8 text.
        """
        path = self._safe_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} bytes to {relative_path}"

    def run_rscript(self, code: str) -> str:
        """Run inline R code via Rscript -e (single line safe for agents).

        Args:
            code: R expression passed as the argument to `Rscript -e`.
        """
        self.state.actions.append("rscript:inline")
        # avoid shell injection: pass code as argv to Rscript -e
        try:
            p = subprocess.run(
                ["Rscript", "-e", code],
                cwd=self.state.work_dir,
                capture_output=True,
                text=True,
                timeout=self.shell_timeout_s,
            )
            out = f"exit={p.returncode}\nstdout:\n{p.stdout[:24000]}\nstderr:\n{p.stderr[:8000]}"
            self.state.last_tool_output = out[:4000]
            return out
        except FileNotFoundError:
            return "ERROR: Rscript not found on PATH; install R."
        except subprocess.TimeoutExpired:
            return "ERROR: Rscript timed out"

    def list_workdir(self) -> str:
        """List workspace as JSON (bounded depth).

        Returns:
            JSON string describing files and folders under the task workspace.
        """
        return json.dumps(_list_dir_json(self.state.work_dir), indent=2)

    def write_plan(self, plan: str) -> str:
        """Persist a markdown plan to `workspace/.plan.md` (overwrite on rewrite).

        Use this at the start of a task and whenever the plan needs revision. The
        plan is not shown automatically on later steps; call check_progress to see
        the current plan excerpt alongside deliverable state.

        Args:
            plan: Markdown text describing the step-by-step plan (bullet list).
        """
        self.state.actions.append("write_plan")
        path = self.state.work_dir / ".plan.md"
        path.write_text(plan, encoding="utf-8")
        return f"Wrote plan ({len(plan)} chars) to .plan.md"

    def check_progress(self, note: str) -> str:
        """Log a progress note and return a JSON snapshot of deliverables + plan excerpt.

        Appends `<UTC ISO timestamp> <note>` to `workspace/.progress.log`, then
        returns a JSON string containing:
          - `output_files`: list of {name, size_bytes} under `workspace/output/`.
          - `success_artifact_present`: whether the task's success artifact glob matches.
          - `plan_excerpt`: first 1000 chars of `.plan.md` (or empty if missing).
          - `note_count`: total notes logged so far.

        Args:
            note: Short progress note to append to the log (plain text, one line).
        """
        self.state.actions.append("check_progress")
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        safe_note = note.replace("\n", " ").strip()
        log_path = self.state.work_dir / ".progress.log"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(f"{ts} {safe_note}\n")
        note_count = sum(1 for _ in log_path.read_text(encoding="utf-8").splitlines() if _.strip())

        out_dir = self.state.work_dir / "output"
        output_files: list[dict[str, Any]] = []
        if out_dir.is_dir():
            for p in sorted(out_dir.iterdir(), key=lambda x: x.name):
                if p.is_file():
                    output_files.append({"name": p.name, "size_bytes": p.stat().st_size})

        artifact_present = False
        if self.success_artifact_glob:
            matches = list(self.state.work_dir.glob(self.success_artifact_glob))
            artifact_present = any(m.is_file() for m in matches)

        plan_path = self.state.work_dir / ".plan.md"
        plan_excerpt = ""
        if plan_path.is_file():
            plan_excerpt = plan_path.read_text(encoding="utf-8", errors="replace")[:1000]

        snapshot = {
            "timestamp": ts,
            "output_files": output_files,
            "success_artifact_glob": self.success_artifact_glob,
            "success_artifact_present": artifact_present,
            "plan_excerpt": plan_excerpt,
            "note_count": note_count,
        }
        return json.dumps(snapshot, indent=2)

    def submit_done(self, success: bool, summary: str = "") -> str:
        """End the episode. Set success=true only if criteria met (agent-declared).

        Args:
            success: Whether the agent believes the task objective is satisfied.
            summary: Short optional note for logging.
        """
        self.state.done = True
        bonus = 0.0
        if success and self.success_artifact_glob:
            matches = list(self.state.work_dir.glob(self.success_artifact_glob))
            if matches and any(f.is_file() for f in matches):
                bonus = 1.0
            else:
                summary = (
                    summary
                    + f" [artifact missing: expected file matching {self.success_artifact_glob}]"
                )
        elif success:
            bonus = 0.5
        self.state.total_reward += bonus
        return f"Episode finished. success={success} reward_bonus={bonus}. {summary}"
