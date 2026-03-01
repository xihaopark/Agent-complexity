from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class RunSpec:
    setup_commands: list[str] = field(default_factory=list)
    entry_command: str | None = None
    task_inputs: list[dict[str, Any]] = field(default_factory=list)
    env_allowlist: list[str] = field(default_factory=list)
    repeats: int = 10
    timeout_sec: int = 1800

    def to_dict(self) -> dict[str, Any]:
        return {
            "setup_commands": self.setup_commands,
            "entry_command": self.entry_command,
            "task_inputs": self.task_inputs,
            "env_allowlist": self.env_allowlist,
            "repeats": self.repeats,
            "timeout_sec": self.timeout_sec,
        }


def _load_declared_spec(repo_path: Path) -> RunSpec | None:
    spec_path = repo_path / ".agent-complexity.yml"
    if not spec_path.exists():
        return None
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    return RunSpec(
        setup_commands=list(data.get("setup_commands", [])),
        entry_command=data.get("entry_command"),
        task_inputs=list(data.get("task_inputs", [])),
        env_allowlist=list(data.get("env_allowlist", [])),
        repeats=int(data.get("repeats", 10)),
        timeout_sec=int(data.get("timeout_sec", 1800)),
    )


def _detect_from_templates(repo_path: Path) -> RunSpec | None:
    for candidate in ("main.py", "app.py", "run.py"):
        if (repo_path / candidate).exists():
            return RunSpec(setup_commands=["pip install -r requirements.txt || true"], entry_command=f"python {candidate}")
    if (repo_path / "requirements.txt").exists() and (repo_path / "agent.py").exists():
        return RunSpec(setup_commands=["pip install -r requirements.txt || true"], entry_command="python agent.py")
    if (repo_path / "package.json").exists():
        return RunSpec(setup_commands=["npm install"], entry_command="npm run start")
    return None


def _detect_from_pyproject(repo_path: Path) -> RunSpec | None:
    pyproject = repo_path / "pyproject.toml"
    if not pyproject.exists():
        return None
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    if scripts:
        first_script = next(iter(scripts))
        return RunSpec(entry_command=f"python -m {scripts[first_script]}")
    return None


def _detect_from_readme(repo_path: Path) -> RunSpec | None:
    readme_candidates = [repo_path / "README.md", repo_path / "readme.md"]
    cmd_pattern = re.compile(r"^\s*(python\s+[^\n`]+|uv\s+run\s+[^\n`]+|npm\s+run\s+\w+)", re.MULTILINE)
    for readme in readme_candidates:
        if not readme.exists():
            continue
        content = readme.read_text(encoding="utf-8", errors="ignore")
        m = cmd_pattern.search(content)
        if m:
            return RunSpec(entry_command=m.group(1).strip())
    return None


def detect_run_spec(
    repo_path: Path,
    user_spec: dict[str, Any] | None,
    default_repeats: int,
    default_timeout_sec: int,
) -> RunSpec:
    if user_spec and user_spec.get("entry_command"):
        spec = RunSpec(
            setup_commands=list(user_spec.get("setup_commands", [])),
            entry_command=str(user_spec.get("entry_command")),
            task_inputs=list(user_spec.get("task_inputs", [])),
            env_allowlist=list(user_spec.get("env_allowlist", [])),
            repeats=int(user_spec.get("repeats", default_repeats)),
            timeout_sec=int(user_spec.get("timeout_sec", default_timeout_sec)),
        )
        return spec

    spec = _load_declared_spec(repo_path)
    if spec:
        return spec
    spec = _detect_from_templates(repo_path)
    if spec:
        spec.repeats = default_repeats
        spec.timeout_sec = default_timeout_sec
        return spec
    spec = _detect_from_pyproject(repo_path)
    if spec:
        spec.repeats = default_repeats
        spec.timeout_sec = default_timeout_sec
        return spec
    spec = _detect_from_readme(repo_path)
    if spec:
        spec.repeats = default_repeats
        spec.timeout_sec = default_timeout_sec
        return spec

    fallback = RunSpec(
        setup_commands=["pip install -r requirements.txt || true"],
        entry_command="python -c \"print('No entry command detected by analyzer')\"",
        repeats=default_repeats,
        timeout_sec=default_timeout_sec,
    )
    return fallback
