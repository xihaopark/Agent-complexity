"""Snakemake runner - execute Snakemake workflow steps."""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from renzo.app.runners.base import BaseRunner, RunResult
from renzo.app.runtime_env import build_runtime_env, find_conda_bin
from renzo.app.workflow_failures import classify_workflow_failure


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _tail(text: str, limit: int = 4000) -> str:
    return (text or "")[-limit:]


class SnakemakeRunner(BaseRunner):
    """Runner for Snakemake workflows."""

    def __init__(self, snakemake_cmd: str = "snakemake"):
        self.snakemake_cmd = snakemake_cmd
        self.last_install_diagnostics: Dict[str, Any] = {}

    def _shared_conda_env(self, params: Optional[Dict[str, Any]] = None) -> str:
        params = params or {}
        return str(params.get("shared_conda_env") or os.environ.get("WORKFLOW_SNAKEMAKE_ENV", "snakemake")).strip()

    def _shared_conda_cmd(self, params: Optional[Dict[str, Any]] = None) -> List[str] | None:
        conda_bin = find_conda_bin()
        env_name = self._shared_conda_env(params)
        if conda_bin and env_name:
            return [conda_bin, "run", "-n", env_name, "python", "-m", "snakemake"]
        return None

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
            "component": "snakemake_runner",
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
        """Check if snakemake is installed."""
        shared_cmd = self._shared_conda_cmd()
        if shared_cmd is not None:
            try:
                result = subprocess.run(
                    [*shared_cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    env=build_runtime_env(),
                )
                if result.returncode == 0:
                    return True
            except Exception:
                pass
        if shutil.which(self.snakemake_cmd) is not None:
            return True
        if Path(self.snakemake_cmd).is_file():
            return True
        return False

    def install_if_missing(self) -> bool:
        """Install Snakemake on-demand with pinned version."""
        if self.check_available():
            self.last_install_diagnostics = self._diagnostic(
                "already_available",
                "Snakemake is already available.",
                "No action required.",
                installed_path=self._shared_conda_env() or str(shutil.which(self.snakemake_cmd) or self.snakemake_cmd),
            )
            return True

        shared_env = self._shared_conda_env()
        if shared_env:
            self.last_install_diagnostics = self._diagnostic(
                "shared_env_missing",
                f"Shared Snakemake environment '{shared_env}' is not available.",
                f"Create it with conda create -c conda-forge -c bioconda -c nodefaults --name {shared_env} snakemake snakedeploy",
                installed_path=shared_env,
            )
            return False

        if not _truthy(os.environ.get("WORKFLOW_RUNTIME_INSTALL", "1")):
            self.last_install_diagnostics = self._diagnostic(
                "runtime_install_disabled",
                "Snakemake is missing and runtime installation is disabled.",
                "Set WORKFLOW_RUNTIME_INSTALL=1 or preinstall snakemake in the runtime image.",
            )
            return False

        version = os.environ.get("SNAKEMAKE_VERSION", "8.30.0")
        command = (
            f"{shlex.quote(sys.executable)} -m pip install "
            f"--no-cache-dir {shlex.quote(f'snakemake=={version}')}"
        )

        try:
            result = subprocess.run(
                ["bash", "-lc", command],
                capture_output=True,
                text=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired as exc:
            self.last_install_diagnostics = self._diagnostic(
                "install_timeout",
                "Installing Snakemake timed out.",
                "Check Python package index/network access and retry.",
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
                f"Installing Snakemake failed: {exc}",
                "Verify runtime permissions and retry.",
                returncode=-1,
                command=command,
                version=version,
            )
            return False

        installed_path = shutil.which("snakemake") or self.snakemake_cmd
        if result.returncode == 0 and shutil.which("snakemake"):
            self.snakemake_cmd = "snakemake"
            self.last_install_diagnostics = self._diagnostic(
                "installed",
                "Installed Snakemake successfully.",
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
            "Failed to install Snakemake.",
            "Inspect stderr_tail and confirm pip/network availability.",
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            command=command,
            version=version,
            installed_path=str(installed_path),
        )
        return False

    def list_targets(self, workflow_dir: Path) -> List[str]:
        """List available rules in the Snakefile."""
        snakefile = self._find_snakefile(workflow_dir)
        if not snakefile:
            return []
        try:
            shared_cmd = self._shared_conda_cmd()
            base_cmd = shared_cmd if shared_cmd is not None else [self.snakemake_cmd]
            result = subprocess.run(
                [*base_cmd, "-s", str(snakefile), "--list-target-rules"],
                cwd=str(workflow_dir),
                capture_output=True,
                text=True,
                timeout=30,
                env=build_runtime_env(),
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except Exception:
            pass
        return []

    def run_step(
        self,
        workflow_dir: Path,
        work_dir: Path,
        targets: Optional[List[str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> RunResult:
        """Execute Snakemake targets."""
        params = params or {}
        timeout = timeout or 3600
        work_dir = Path(work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)

        snakefile_param = params.get("snakefile")
        snakefile = (workflow_dir / snakefile_param).resolve() if snakefile_param else self._find_snakefile(workflow_dir)
        if not snakefile:
            return RunResult(
                status="error",
                error=f"No Snakefile found in {workflow_dir}",
                returncode=-1,
            )

        configfile_param = params.get("configfile")
        run_directory_param = params.get("run_directory")
        use_conda = bool(params.get("use_conda", False))
        cores = str(params.get("cores", 1))
        shared_cmd = self._shared_conda_cmd(params)
        cmd = [*(shared_cmd if shared_cmd is not None else [sys.executable, "-m", "snakemake"]), "-s", str(snakefile)]
        execution_cwd = workflow_dir
        if run_directory_param == "work_dir":
            cmd.extend(["--directory", str(work_dir)])
            execution_cwd = work_dir
        elif run_directory_param:
            run_directory = (workflow_dir / run_directory_param).resolve()
            run_directory.mkdir(parents=True, exist_ok=True)
            cmd.extend(["--directory", str(run_directory)])
            execution_cwd = run_directory
        cmd.extend(["--cores", cores, "--printshellcmds"])
        if configfile_param:
            cmd.extend(["--configfile", str((workflow_dir / configfile_param).resolve())])
        if use_conda:
            cmd.append("--use-conda")
        extra_args = params.get("extra_args", [])
        if isinstance(extra_args, list):
            cmd.extend(str(arg) for arg in extra_args)
        elif extra_args:
            cmd.extend(str(extra_args).split())
        config_items = params.get("config_items", {})
        cmd = [
            *cmd,
        ]
        normalized_targets = [str(target) for target in (targets or []) if str(target).strip()]
        if normalized_targets and normalized_targets != ["all"]:
            cmd.extend(normalized_targets)
        for key, val in config_items.items():
            cmd.extend(["--config", f"{key}={val}"])

        try:
            result = subprocess.run(
                cmd,
                cwd=str(execution_cwd),
                capture_output=True,
                text=True,
                timeout=timeout,
                env=build_runtime_env(),
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

        artifact_root = execution_cwd if execution_cwd.exists() else work_dir
        artifacts = self._collect_artifacts(artifact_root)
        status = "success" if result.returncode == 0 else "error"
        metadata: Dict[str, Any] = {}
        if result.returncode != 0:
            metadata["failure"] = classify_workflow_failure(
                result.stdout,
                result.stderr,
                work_dir=execution_cwd,
            )
        return RunResult(
            status=status,
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            artifacts=artifacts,
            error=None if result.returncode == 0 else _tail(result.stderr, 500),
            metadata=metadata,
        )

    def _find_snakefile(self, workflow_dir: Path) -> Optional[Path]:
        """Find Snakefile in workflow directory."""
        for name in ("Snakefile", "snakefile", "workflow/Snakefile"):
            path = workflow_dir / name
            if path.exists():
                return path
        smk_files = list(workflow_dir.rglob("*.smk"))
        if smk_files:
            return smk_files[0]
        return None

    def _collect_artifacts(self, work_dir: Path, max_files: int = 100) -> List[str]:
        """Collect output artifacts from work directory."""
        artifacts: List[str] = []
        for path in work_dir.rglob("*"):
            if path.is_file() and ".snakemake" not in str(path):
                artifacts.append(str(path))
                if len(artifacts) >= max_files:
                    break
        return artifacts
