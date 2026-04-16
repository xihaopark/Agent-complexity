"""Bash-in-workspace tool (local only)."""
from __future__ import annotations

import logging
import re
import subprocess
from pathlib import Path
from typing import Optional, Type

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)

_PATH_TRAVERSAL_RE = re.compile(r"(?:^|[\s;|&\"'])\.\.(?:[/\s;|&\"']|$)")


class BashInWorkspaceInput(BaseModel):
    command: str = Field(
        description="Bash command to run in the workspace. Paths relative to workspace. No '..'."
    )


class BashInWorkspaceTool(BaseTool):
    name: str = "bash_in_workspace"
    description: str = (
        "Run a bash command in the workspace. Use for: ls, cat, head, mkdir -p, grep, mv, cp, git. "
        "For writing files prefer write_file. Paths must be relative; no '..'."
    )
    args_schema: Type[BaseModel] = BashInWorkspaceInput
    data_root: Optional[Path] = None
    timeout_seconds: int = 60

    def __init__(
        self,
        data_root: Optional[Path] = None,
        timeout_seconds: int = 60,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve() if data_root else None
        self.timeout_seconds = timeout_seconds

    def _run(self, command: str) -> str:
        if _PATH_TRAVERSAL_RE.search(command):
            return f"$ {command}\n\nError: '..' path traversal not allowed."
        cwd = str(self.data_root) if self.data_root else "."
        if self.data_root and not self.data_root.exists():
            return f"$ {command}\n\nError: workspace does not exist: {self.data_root}"
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            out = (result.stdout or "").strip()
            err = (result.stderr or "").strip()
            lines = [f"$ {command}"]
            if out:
                lines.append(f"stdout:\n{out}")
            if err:
                lines.append(f"stderr:\n{err}")
            lines.append(f"returncode: {result.returncode}")
            return "\n\n".join(lines)
        except subprocess.TimeoutExpired:
            return f"$ {command}\n\nError: command timed out."
        except Exception as e:
            return f"$ {command}\n\nError: {e}"
