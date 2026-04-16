"""Workflow executor: run Nextflow and Snakemake pipelines."""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from renzo.app.runtime_env import build_runtime_env, find_conda_bin
from renzo.app.workflows.models import WorkflowRunStatus


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _tail(text: str, limit: int = 4000) -> str:
    return (text or "")[-limit:]


class WorkflowExecutor:
    """Execute Nextflow and Snakemake workflows via subprocess."""

    def __init__(self, nextflow_cmd: str = "nextflow", snakemake_cmd: str = "snakemake"):
        self.nextflow_cmd = nextflow_cmd
        self.snakemake_cmd = snakemake_cmd

    def _runtime_cache_dir(self) -> Path:
        root = os.environ.get("WORKFLOW_RUNTIME_CACHE_DIR")
        if root:
            return Path(root).resolve()
        return (Path.home() / ".cache" / "renzo" / "runtime").resolve()

    def _build_error(
        self,
        code: str,
        message: str,
        hint: str,
        *,
        component: str = "workflow_executor",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return {
            "code": code,
            "message": message,
            "hint": hint,
            "component": component,
            "details": details or {},
        }

    def _command_available(self, command: str) -> bool:
        if shutil.which(command):
            return True
        return Path(command).is_file()

    def _shared_conda_env(self, params: Optional[Dict[str, Any]] = None) -> str:
        params = params or {}
        return str(params.get("shared_conda_env") or os.environ.get("WORKFLOW_SNAKEMAKE_ENV", "snakemake")).strip()

    def _shared_conda_cmd(self, params: Optional[Dict[str, Any]] = None) -> list[str] | None:
        conda_bin = find_conda_bin()
        env_name = self._shared_conda_env(params)
        if conda_bin and env_name:
            return [conda_bin, "run", "-n", env_name, "python", "-m", "snakemake"]
        return None

    def _snakemake_available(self, params: Optional[Dict[str, Any]] = None) -> bool:
        shared_cmd = self._shared_conda_cmd(params)
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
        return self._command_available(self.snakemake_cmd)

    def _docker_socket_status(self) -> Dict[str, Any]:
        sock = Path("/var/run/docker.sock")
        return {
            "path": str(sock),
            "exists": sock.exists(),
            "readable": os.access(sock, os.R_OK),
            "writable": os.access(sock, os.W_OK),
        }

    def get_runtime_status(self, profile: str = "docker") -> Dict[str, Any]:
        """Expose runtime readiness details for operators and `/api/ready`."""
        runtime_install = _truthy(os.environ.get("WORKFLOW_RUNTIME_INSTALL", "1"))
        nextflow_version = os.environ.get("NEXTFLOW_VERSION", "24.10.5")
        snakemake_version = os.environ.get("SNAKEMAKE_VERSION", "8.30.0")
        docker_socket = self._docker_socket_status()

        checks = {
            "runtime_install_enabled": runtime_install,
            "nextflow": {
                "command": self.nextflow_cmd,
                "available": self._command_available(self.nextflow_cmd),
                "target_version": nextflow_version,
            },
            "snakemake": {
                "command": self._shared_conda_env() or self.snakemake_cmd,
                "available": self._snakemake_available(),
                "target_version": snakemake_version,
            },
            "docker_cli": {
                "command": "docker",
                "available": self._command_available("docker"),
            },
            "docker_socket": docker_socket,
            "profile": profile,
        }

        # If runtime installation is enabled, missing engines are acceptable at startup.
        engines_ready = bool(
            checks["nextflow"]["available"]
            or checks["snakemake"]["available"]
            or runtime_install
        )
        ready = engines_ready
        if profile == "docker":
            ready = (
                ready
                and checks["docker_cli"]["available"]
                and docker_socket["exists"]
                and (docker_socket["readable"] or docker_socket["writable"])
            )

        return {
            "status": "ready" if ready else "degraded",
            "ready": ready,
            "checks": checks,
        }

    def _install_nextflow(self) -> Dict[str, Any]:
        version = os.environ.get("NEXTFLOW_VERSION", "24.10.5")
        cache_dir = self._runtime_cache_dir()
        bin_dir = cache_dir / "bin"
        nxf_home = cache_dir / "nextflow-home"
        installed_path = bin_dir / "nextflow"
        bin_dir.mkdir(parents=True, exist_ok=True)
        nxf_home.mkdir(parents=True, exist_ok=True)

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
            return {
                "ok": False,
                "returncode": -1,
                "stdout_tail": _tail(exc.stdout or ""),
                "stderr_tail": _tail(exc.stderr or ""),
                "message": "Installing Nextflow timed out.",
                "hint": "Check outbound access to get.nextflow.io and retry.",
                "command": command,
            }
        except Exception as exc:
            return {
                "ok": False,
                "returncode": -1,
                "stdout_tail": "",
                "stderr_tail": "",
                "message": f"Installing Nextflow failed: {exc}",
                "hint": "Verify runtime permissions and retry.",
                "command": command,
            }

        if result.returncode == 0 and installed_path.exists():
            self.nextflow_cmd = str(installed_path)
            return {
                "ok": True,
                "returncode": 0,
                "stdout_tail": _tail(result.stdout),
                "stderr_tail": _tail(result.stderr),
                "installed_path": str(installed_path),
                "command": command,
            }
        return {
            "ok": False,
            "returncode": result.returncode,
            "stdout_tail": _tail(result.stdout),
            "stderr_tail": _tail(result.stderr),
            "message": "Installing Nextflow failed.",
            "hint": "Inspect stderr_tail and ensure Java/curl/network are available.",
            "command": command,
        }

    def _install_snakemake(self) -> Dict[str, Any]:
        version = os.environ.get("SNAKEMAKE_VERSION", "8.30.0")
        command = (
            f"{shlex.quote(sys.executable)} -m pip install --no-cache-dir "
            f"{shlex.quote(f'snakemake=={version}')}"
        )
        try:
            result = subprocess.run(
                ["bash", "-lc", command],
                capture_output=True,
                text=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "ok": False,
                "returncode": -1,
                "stdout_tail": _tail(exc.stdout or ""),
                "stderr_tail": _tail(exc.stderr or ""),
                "message": "Installing Snakemake timed out.",
                "hint": "Check package index/network availability and retry.",
                "command": command,
            }
        except Exception as exc:
            return {
                "ok": False,
                "returncode": -1,
                "stdout_tail": "",
                "stderr_tail": "",
                "message": f"Installing Snakemake failed: {exc}",
                "hint": "Verify runtime permissions and retry.",
                "command": command,
            }

        if result.returncode == 0 and shutil.which("snakemake"):
            self.snakemake_cmd = "snakemake"
            return {
                "ok": True,
                "returncode": 0,
                "stdout_tail": _tail(result.stdout),
                "stderr_tail": _tail(result.stderr),
                "installed_path": str(shutil.which("snakemake")),
                "command": command,
            }
        return {
            "ok": False,
            "returncode": result.returncode,
            "stdout_tail": _tail(result.stdout),
            "stderr_tail": _tail(result.stderr),
            "message": "Installing Snakemake failed.",
            "hint": "Inspect stderr_tail and ensure pip/network are available.",
            "command": command,
        }

    def _ensure_runtime(self, engine: str, profile: str = "docker") -> Optional[Dict[str, Any]]:
        runtime_install = _truthy(os.environ.get("WORKFLOW_RUNTIME_INSTALL", "1"))
        status = self.get_runtime_status(profile=profile)
        checks = status["checks"]

        if engine == "nextflow" and not checks["nextflow"]["available"]:
            if runtime_install:
                install_info = self._install_nextflow()
                if not install_info.get("ok"):
                    return self._build_error(
                        "nextflow_install_failed",
                        install_info.get("message", "Failed to install Nextflow."),
                        install_info.get("hint", "Inspect install diagnostics and retry."),
                        details=install_info,
                    )
            if not self._command_available(self.nextflow_cmd):
                return self._build_error(
                    "nextflow_missing",
                    "Nextflow is not available.",
                    "Set WORKFLOW_RUNTIME_INSTALL=1 or preinstall nextflow in the runtime image.",
                    details={"command": self.nextflow_cmd},
                )

        if engine == "snakemake" and not checks["snakemake"]["available"]:
            if runtime_install:
                install_info = self._install_snakemake()
                if not install_info.get("ok"):
                    return self._build_error(
                        "snakemake_install_failed",
                        install_info.get("message", "Failed to install Snakemake."),
                        install_info.get("hint", "Inspect install diagnostics and retry."),
                        details=install_info,
                    )
            if not self._snakemake_available():
                return self._build_error(
                    "snakemake_missing",
                    "Snakemake is not available.",
                    "Set WORKFLOW_RUNTIME_INSTALL=1 or preinstall snakemake in the runtime image.",
                    details={"command": self._shared_conda_env() or self.snakemake_cmd},
                )

        if profile == "docker":
            docker_cli = self._command_available("docker")
            docker_socket = self._docker_socket_status()
            if not docker_cli:
                return self._build_error(
                    "docker_cli_missing",
                    "Docker CLI is not available inside backend runtime.",
                    "Install docker CLI in the image or switch profile away from docker.",
                    details={"command": "docker"},
                )
            if not docker_socket["exists"]:
                return self._build_error(
                    "docker_socket_missing",
                    "Docker socket is not mounted in backend container.",
                    "Mount /var/run/docker.sock:/var/run/docker.sock in docker-compose.",
                    details=docker_socket,
                )
            if not (docker_socket["readable"] or docker_socket["writable"]):
                return self._build_error(
                    "docker_socket_unusable",
                    "Docker socket exists but is not readable/writable by backend process.",
                    "Adjust permissions or run backend with sufficient privileges.",
                    details=docker_socket,
                )

        return None

    def _ensure_workflow_dir(self, workflow_path: str, work_dir: Path) -> Path:
        """
        If workflow_path is a .crate.zip, extract to work_dir/workflow and return that path.
        Otherwise return the resolved workflow directory.
        """
        path = Path(workflow_path)
        if not path.exists():
            raise FileNotFoundError(f"Workflow path does not exist: {workflow_path}")
        if path.suffix == ".zip" and ".crate" in path.stem:
            extract_to = work_dir / "workflow"
            extract_to.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(path, "r") as archive:
                archive.extractall(extract_to)
            entries = list(extract_to.iterdir())
            if len(entries) == 1 and entries[0].is_dir() and (entries[0] / "ro-crate-metadata.json").exists():
                return entries[0]
            if (extract_to / "ro-crate-metadata.json").exists():
                return extract_to
            return extract_to
        return path.resolve()

    def run_nextflow(
        self,
        workflow_path: str,
        work_dir: Path,
        params: Optional[Dict[str, Any]] = None,
        profile: str = "docker",
        input_path: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> WorkflowRunStatus:
        """
        Run Nextflow pipeline.
        workflow_path: path to workflow dir or .crate.zip
        work_dir: working directory for execution (outputs, work, etc.)
        params: optional dict of --param_name value
        profile: docker or singularity
        input_path: path to input file or directory (maps to --input)
        """
        preflight_error = self._ensure_runtime(engine="nextflow", profile=profile)
        if preflight_error:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                error=preflight_error["message"],
                error_detail=preflight_error,
            )

        params = params or {}
        work_dir = Path(work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)

        wf_dir = self._ensure_workflow_dir(workflow_path, work_dir)
        entry = "main.nf"
        entry_path = wf_dir / entry
        if not entry_path.exists():
            for candidate in ("main.nf", "workflow.nf", "nextflow.config"):
                if (wf_dir / candidate).exists():
                    entry = candidate
                    break
            else:
                nf_files = list(wf_dir.glob("*.nf"))
                if nf_files:
                    entry = nf_files[0].name
                else:
                    return WorkflowRunStatus(
                        run_id="",
                        workflow_id="",
                        status="failed",
                        error=f"No .nf entry point found in {wf_dir}",
                        error_detail=self._build_error(
                            "nextflow_entry_missing",
                            "No Nextflow entry point was found.",
                            "Provide main.nf/workflow.nf or specify a valid .nf entry.",
                            details={"workflow_dir": str(wf_dir)},
                        ),
                    )

        cmd = [
            self.nextflow_cmd,
            "run",
            str(wf_dir / entry),
            "-work-dir", str(work_dir / "work"),
            "-outdir", str(work_dir / "output"),
            "-profile", profile,
            "-ansi-log", "false",
        ]
        if input_path:
            cmd.extend(["--input", input_path])
        for key, val in params.items():
            if key.startswith("--"):
                cmd.append(key)
            else:
                cmd.append(f"--{key}")
            cmd.append(str(val))

        start_ts = datetime.utcnow().isoformat() + "Z"
        try:
            result = subprocess.run(
                cmd,
                cwd=str(work_dir),
                capture_output=True,
                text=True,
                timeout=timeout or 3600,
                env={**dict(os.environ), "NXF_ANSI_LOG": "false"},
            )
        except subprocess.TimeoutExpired as exc:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                returncode=-1,
                work_dir=str(work_dir),
                start_ts=start_ts,
                end_ts=datetime.utcnow().isoformat() + "Z",
                error="Execution timed out",
                error_detail=self._build_error(
                    "workflow_timeout",
                    "Nextflow execution timed out.",
                    "Increase timeout or optimize workflow workload.",
                    details={"timeout_seconds": timeout or 3600},
                ),
            )
        except Exception as exc:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                work_dir=str(work_dir),
                start_ts=start_ts,
                end_ts=datetime.utcnow().isoformat() + "Z",
                error=str(exc),
                error_detail=self._build_error(
                    "workflow_executor_exception",
                    "Unexpected exception during Nextflow execution.",
                    "Inspect backend logs for stack trace details.",
                    details={"exception": str(exc)},
                ),
            )

        end_ts = datetime.utcnow().isoformat() + "Z"
        status = "success" if result.returncode == 0 else "failed"
        output_paths = []
        out_dir = work_dir / "output"
        if out_dir.exists():
            output_paths = [str(path) for path in out_dir.rglob("*") if path.is_file()]

        error_detail = {}
        if result.returncode != 0:
            error_detail = self._build_error(
                "workflow_nonzero_exit",
                "Nextflow exited with a non-zero status.",
                "Inspect stderr_tail for failure reason and retry with corrected inputs/params.",
                details={
                    "returncode": result.returncode,
                    "stderr_tail": _tail(result.stderr or ""),
                    "stdout_tail": _tail(result.stdout or ""),
                    "command": cmd,
                },
            )

        return WorkflowRunStatus(
            run_id="",
            workflow_id="",
            status=status,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            returncode=result.returncode,
            output_paths=output_paths[:100],
            work_dir=str(work_dir),
            start_ts=start_ts,
            end_ts=end_ts,
            error=None if result.returncode == 0 else (result.stderr or "Non-zero exit"),
            error_detail=error_detail,
        )

    def run_snakemake(
        self,
        workflow_path: str,
        work_dir: Path,
        params: Optional[Dict[str, Any]] = None,
        use_singularity: bool = False,
        config: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> WorkflowRunStatus:
        """
        Run Snakemake pipeline.
        workflow_path: path to workflow dir or .crate.zip
        work_dir: working directory
        params: optional CLI args (e.g. target rules)
        use_singularity: use --use-singularity
        config: optional config dict (written to config.yaml)
        """
        profile = "singularity" if use_singularity else "docker"
        preflight_error = self._ensure_runtime(engine="snakemake", profile=profile)
        if preflight_error:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                error=preflight_error["message"],
                error_detail=preflight_error,
            )

        params = params or {}
        config = config or {}
        work_dir = Path(work_dir)
        work_dir.mkdir(parents=True, exist_ok=True)

        wf_dir = self._ensure_workflow_dir(workflow_path, work_dir)
        snakefile = None
        for name in ("Snakefile", "snakefile", "workflow/Snakefile"):
            candidate = wf_dir / name
            if candidate.exists():
                snakefile = candidate
                break
        if not snakefile:
            candidates = list(wf_dir.rglob("*.smk")) + list(wf_dir.rglob("Snakefile*"))
            if candidates:
                snakefile = candidates[0]
        if not snakefile:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                error=f"No Snakefile found in {wf_dir}",
                error_detail=self._build_error(
                    "snakemake_entry_missing",
                    "No Snakemake entry point was found.",
                    "Provide Snakefile/snakefile or *.smk entry.",
                    details={"workflow_dir": str(wf_dir)},
                ),
            )

        config_path = work_dir / "config.yaml"
        if config:
            try:
                import yaml

                with open(config_path, "w", encoding="utf-8") as file:
                    yaml.safe_dump(config, file)
            except Exception:
                config_path = None

        cmd = [
            *(self._shared_conda_cmd(params) or [self.snakemake_cmd]),
            "-s", str(snakefile),
            "--directory", str(work_dir),
            "-j", "1",
            "--printshellcmds",
        ]
        if use_singularity:
            cmd.append("--use-singularity")
        if config_path and config_path.exists():
            cmd.extend(["--configfile", str(config_path)])
        for key, val in params.items():
            if key == "targets":
                for target in (val if isinstance(val, (list, tuple)) else [val]):
                    cmd.append(str(target))
            else:
                cmd.extend([f"--{key}", str(val)])

        start_ts = datetime.utcnow().isoformat() + "Z"
        try:
            result = subprocess.run(
                cmd,
                cwd=str(work_dir),
                capture_output=True,
                text=True,
                timeout=timeout or 3600,
                env=build_runtime_env(),
            )
        except subprocess.TimeoutExpired as exc:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                returncode=-1,
                work_dir=str(work_dir),
                start_ts=start_ts,
                end_ts=datetime.utcnow().isoformat() + "Z",
                error="Execution timed out",
                error_detail=self._build_error(
                    "workflow_timeout",
                    "Snakemake execution timed out.",
                    "Increase timeout or optimize workflow workload.",
                    details={"timeout_seconds": timeout or 3600},
                ),
            )
        except Exception as exc:
            return WorkflowRunStatus(
                run_id="",
                workflow_id="",
                status="failed",
                work_dir=str(work_dir),
                start_ts=start_ts,
                end_ts=datetime.utcnow().isoformat() + "Z",
                error=str(exc),
                error_detail=self._build_error(
                    "workflow_executor_exception",
                    "Unexpected exception during Snakemake execution.",
                    "Inspect backend logs for stack trace details.",
                    details={"exception": str(exc)},
                ),
            )

        end_ts = datetime.utcnow().isoformat() + "Z"
        status = "success" if result.returncode == 0 else "failed"
        output_paths = []
        for path in work_dir.rglob("*"):
            if path.is_file() and not any(token in str(path) for token in (".snakemake", "config.yaml")):
                output_paths.append(str(path))
        output_paths = output_paths[:100]

        error_detail = {}
        if result.returncode != 0:
            error_detail = self._build_error(
                "workflow_nonzero_exit",
                "Snakemake exited with a non-zero status.",
                "Inspect stderr_tail for failure reason and retry with corrected inputs/params.",
                details={
                    "returncode": result.returncode,
                    "stderr_tail": _tail(result.stderr or ""),
                    "stdout_tail": _tail(result.stdout or ""),
                    "command": cmd,
                },
            )

        return WorkflowRunStatus(
            run_id="",
            workflow_id="",
            status=status,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            returncode=result.returncode,
            output_paths=output_paths,
            work_dir=str(work_dir),
            start_ts=start_ts,
            end_ts=end_ts,
            error=None if result.returncode == 0 else (result.stderr or "Non-zero exit"),
            error_detail=error_detail,
        )
