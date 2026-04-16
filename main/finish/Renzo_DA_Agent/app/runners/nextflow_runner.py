"""Nextflow runner - execute Nextflow workflow steps."""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from renzo.app.runners.base import BaseRunner, RunResult


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _tail(text: str, limit: int = 4000) -> str:
    return (text or "")[-limit:]


class NextflowRunner(BaseRunner):
    """Runner for Nextflow workflows."""

    def __init__(self, nextflow_cmd: str = "nextflow"):
        self.nextflow_cmd = nextflow_cmd
        self.last_install_diagnostics: Dict[str, Any] = {}

    def _runtime_cache_dir(self) -> Path:
        root = os.environ.get("WORKFLOW_RUNTIME_CACHE_DIR")
        if root:
            return Path(root).resolve()
        return (Path.home() / ".cache" / "renzo" / "runtime").resolve()

    def _diagnostic(
        self,
        code: str,
        message: str,
        hint: str,
        *,
        returncode: int | None = None,
        stdout: str = "",
        stderr: str = "",
        command: str = "",
        version: str = "",
        installed_path: str = "",
    ) -> Dict[str, Any]:
        return {
            "component": "nextflow_runner",
            "code": code,
            "message": message,
            "hint": hint,
            "returncode": returncode,
            "stdout_tail": _tail(stdout),
            "stderr_tail": _tail(stderr),
            "command": command,
            "version": version,
            "installed_path": installed_path,
        }

    def check_available(self) -> bool:
        """Check if nextflow is installed."""
        if shutil.which(self.nextflow_cmd) is not None:
            return True
        # Handle command path persisted from runtime install.
        if Path(self.nextflow_cmd).is_file():
            return True
        return False

    def install_if_missing(self) -> bool:
        """Install Nextflow on-demand with pinned version and cached location."""
        if self.check_available():
            self.last_install_diagnostics = self._diagnostic(
                "already_available",
                "Nextflow is already available.",
                "No action required.",
                installed_path=str(shutil.which(self.nextflow_cmd) or self.nextflow_cmd),
            )
            return True

        if not _truthy(os.environ.get("WORKFLOW_RUNTIME_INSTALL", "1")):
            self.last_install_diagnostics = self._diagnostic(
                "runtime_install_disabled",
                "Nextflow is missing and runtime installation is disabled.",
                "Set WORKFLOW_RUNTIME_INSTALL=1 or preinstall nextflow in the runtime image.",
            )
            return False

        version = os.environ.get("NEXTFLOW_VERSION", "24.10.5")
        cache_dir = self._runtime_cache_dir()
        bin_dir = cache_dir / "bin"
        nxf_home = cache_dir / "nextflow-home"
        bin_dir.mkdir(parents=True, exist_ok=True)
        nxf_home.mkdir(parents=True, exist_ok=True)
        installed_path = bin_dir / "nextflow"

        command = (
            "set -euo pipefail; "
            f"mkdir -p {shlex.quote(str(bin_dir))} {shlex.quote(str(nxf_home))}; "
            f"cd {shlex.quote(str(cache_dir))}; "
            f"export NXF_HOME={shlex.quote(str(nxf_home))}; "
            f"export NXF_VER={shlex.quote(version)}; "
            "curl -fsSL https://get.nextflow.io | bash; "
            f"mv -f nextflow {shlex.quote(str(installed_path))}; "
            f"chmod +x {shlex.quote(str(installed_path))}"
        )

        try:
            result = subprocess.run(
                ["bash", "-lc", command],
                capture_output=True,
                text=True,
                timeout=600,
            )
        except subprocess.TimeoutExpired as exc:
            self.last_install_diagnostics = self._diagnostic(
                "install_timeout",
                "Installing Nextflow timed out.",
                "Check outbound access to get.nextflow.io and retry.",
                returncode=-1,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                command=command,
                version=version,
            )
            return False
        except Exception as exc:
            self.last_install_diagnostics = self._diagnostic(
                "install_exception",
                f"Installing Nextflow failed: {exc}",
                "Verify runtime permissions and retry.",
                returncode=-1,
                command=command,
                version=version,
            )
            return False

        if result.returncode == 0 and installed_path.exists():
            self.nextflow_cmd = str(installed_path)
            self.last_install_diagnostics = self._diagnostic(
                "installed",
                "Installed Nextflow successfully.",
                "Proceed with workflow execution.",
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                command=command,
                version=version,
                installed_path=str(installed_path),
            )
            return True

        self.last_install_diagnostics = self._diagnostic(
            "install_failed",
            "Failed to install Nextflow.",
            "Inspect stderr_tail and confirm Java/curl/network availability.",
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            command=command,
            version=version,
        )
        return False

    def list_targets(self, workflow_dir: Path) -> List[str]:
        """List available workflows/entries in the workflow directory."""
        nf_files = list(workflow_dir.glob("*.nf"))
        return [f.name for f in nf_files]

    def run_step(
        self,
        workflow_dir: Path,
        work_dir: Path,
        targets: Optional[List[str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> RunResult:
        """Execute Nextflow pipeline."""
        params = dict(params or {})
        timeout = timeout or 3600
        work_dir = Path(work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)

        entry = self._find_entry(workflow_dir, targets)
        if not entry:
            return RunResult(
                status="error",
                error=f"No .nf entry point found in {workflow_dir}",
                returncode=-1,
            )

        cmd = [
            self.nextflow_cmd,
            "run",
            str(entry),
            "-work-dir", str(work_dir / "work"),
            "-ansi-log", "false",
        ]

        profile = params.pop("profile", None)
        if profile:
            cmd.extend(["-profile", profile])
        if params.pop("resume", False):
            cmd.append("-resume")
        cmd.extend(["--outdir", str(work_dir / "output")])

        for key, val in params.items():
            cmd.extend([f"--{key}", str(val)])

        try:
            result = subprocess.run(
                cmd,
                cwd=str(workflow_dir),
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**dict(os.environ), "NXF_ANSI_LOG": "false"},
            )
        except subprocess.TimeoutExpired as exc:
            return RunResult(
                status="timeout",
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                returncode=-1,
                error="Execution timed out",
            )
        except Exception as exc:
            return RunResult(
                status="error",
                error=str(exc),
                returncode=-1,
            )

        artifacts = self._collect_artifacts(work_dir)
        status = "success" if result.returncode == 0 else "error"
        return RunResult(
            status=status,
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            artifacts=artifacts,
            error=None if result.returncode == 0 else _tail(result.stderr, 500),
        )

    def _find_entry(self, workflow_dir: Path, targets: Optional[List[str]]) -> Optional[Path]:
        """Find Nextflow entry point."""
        if targets:
            for target in targets:
                candidate = workflow_dir / target
                if candidate.exists():
                    return candidate

        for name in ("main.nf", "workflow.nf"):
            candidate = workflow_dir / name
            if candidate.exists():
                return candidate

        nf_files = list(workflow_dir.glob("*.nf"))
        if nf_files:
            return nf_files[0]
        return None

    def _collect_artifacts(self, work_dir: Path, max_files: int = 100) -> List[str]:
        """Collect output artifacts from work directory."""
        artifacts: List[str] = []
        output_dir = work_dir / "output"
        if output_dir.exists():
            for path in output_dir.rglob("*"):
                if path.is_file():
                    artifacts.append(str(path))
                    if len(artifacts) >= max_files:
                        break
        return artifacts
