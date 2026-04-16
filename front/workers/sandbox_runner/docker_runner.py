from __future__ import annotations

import json
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from common.settings import get_settings

settings = get_settings()


@dataclass
class RunResult:
    run_id: str
    exit_code: int
    duration_sec: float
    stdout: str
    stderr: str
    cpu_peak_pct: float
    memory_peak_mb: float
    event_file: Path


class DockerSandboxRunner:
    def __init__(self) -> None:
        self.image = settings.docker_image
        self.network = settings.docker_network
        self.cpus = settings.standard_cpus
        self.memory_mb = settings.standard_memory_mb
        self.pids_limit = settings.standard_pids_limit

    def _sample_stats(self, container_name: str, stop_flag: threading.Event, sink: dict[str, float]) -> None:
        cpu_peak = 0.0
        mem_peak = 0.0
        while not stop_flag.is_set():
            try:
                cmd = [
                    "docker",
                    "stats",
                    container_name,
                    "--no-stream",
                    "--format",
                    "{{json .}}",
                ]
                out = subprocess.run(cmd, capture_output=True, text=True, check=False)
                raw = out.stdout.strip()
                if raw:
                    data = json.loads(raw)
                    cpu_raw = str(data.get("CPUPerc", "0")).replace("%", "")
                    mem_raw = str(data.get("MemUsage", "0MiB / 0MiB")).split("/")[0].strip()
                    try:
                        cpu_peak = max(cpu_peak, float(cpu_raw))
                    except ValueError:
                        pass
                    if mem_raw.lower().endswith("mib"):
                        mem_peak = max(mem_peak, float(mem_raw[:-3]))
                    elif mem_raw.lower().endswith("gib"):
                        mem_peak = max(mem_peak, float(mem_raw[:-3]) * 1024.0)
            except Exception:
                pass
            time.sleep(1.0)
        sink["cpu_peak_pct"] = cpu_peak
        sink["memory_peak_mb"] = mem_peak

    def run(
        self,
        repo_path: Path,
        output_path: Path,
        run_id: str,
        job_id: str,
        setup_commands: list[str],
        entry_command: str,
        timeout_sec: int,
        env_allowlist: list[str] | None = None,
    ) -> RunResult:
        output_path.mkdir(parents=True, exist_ok=True)
        event_file = output_path / f"events_{run_id}.jsonl"
        stdout_file = output_path / f"stdout_{run_id}.log"
        stderr_file = output_path / f"stderr_{run_id}.log"
        container_name = f"aca-{run_id}-{uuid4().hex[:8]}"
        env_allowlist = env_allowlist or []

        env_flags = [
            "-e",
            f"AGENTIC_EVENT_LOG=/output/{event_file.name}",
            "-e",
            f"AGENTIC_JOB_ID={job_id}",
            "-e",
            f"AGENTIC_RUN_ID={run_id}",
        ]
        for key in env_allowlist:
            if key in settings.model_fields:
                continue
            env_flags.extend(["-e", f"{key}"])

        command_parts = ["set -e", "cd /workspace"]
        command_parts.extend(setup_commands)
        command_parts.append(entry_command)
        bash_cmd = " && ".join(command_parts)

        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "--network",
            self.network,
            "--cpus",
            str(self.cpus),
            "--memory",
            f"{self.memory_mb}m",
            "--pids-limit",
            str(self.pids_limit),
            "--user",
            "1000:1000",
            "-v",
            f"{repo_path.resolve()}:/workspace:ro",
            "-v",
            f"{output_path.resolve()}:/output",
            "-w",
            "/workspace",
        ]
        docker_cmd.extend(env_flags)
        docker_cmd.extend([self.image, "bash", "-lc", bash_cmd])

        start = time.perf_counter()
        stats: dict[str, float] = {}
        stop_flag = threading.Event()
        stats_thread = threading.Thread(
            target=self._sample_stats, args=(container_name, stop_flag, stats), daemon=True
        )

        proc = subprocess.Popen(docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stats_thread.start()
        try:
            stdout, stderr = proc.communicate(timeout=timeout_sec)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            exit_code = 124
        finally:
            stop_flag.set()
            stats_thread.join(timeout=2.0)
            subprocess.run(["docker", "rm", "-f", container_name], check=False, capture_output=True)

        duration_sec = time.perf_counter() - start
        stdout_file.write_text(stdout or "", encoding="utf-8", errors="ignore")
        stderr_file.write_text(stderr or "", encoding="utf-8", errors="ignore")

        return RunResult(
            run_id=run_id,
            exit_code=exit_code,
            duration_sec=duration_sec,
            stdout=stdout or "",
            stderr=stderr or "",
            cpu_peak_pct=float(stats.get("cpu_peak_pct", 0.0)),
            memory_peak_mb=float(stats.get("memory_peak_mb", 0.0)),
            event_file=event_file,
        )
