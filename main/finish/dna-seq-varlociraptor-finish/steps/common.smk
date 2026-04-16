from pathlib import Path
import shlex
import subprocess
import sys
import os


def _runtime_helper():
  root = os.environ.get("RENZO_RUNTIME_ROOT", "").strip()
  if not root:
    return None
  path = (Path(root) / "app" / "finish_step_runtime.py").resolve()
  return path if path.exists() else None


def ensure_paths(paths):
  for path in paths:
    resolved = (Path(".") / path).resolve()
    if not resolved.exists():
      raise FileNotFoundError(f"Missing required path: {path}")


def write_stamp(output_path, step_id, command):
  output_path = Path(output_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(f"{step_id}\n{command}\n", encoding="utf-8")


def run_step(step_id, output_path):
  helper = _runtime_helper()
  if helper is not None:
    subprocess.run(
      [
        sys.executable,
        str(helper),
        "--config-file",
        "config_basic/config.yaml",
        "--step-id",
        step_id,
        "--output-path",
        str(output_path),
      ],
      check=True,
    )
    return

  step = config["steps"][step_id]
  ensure_paths(step.get("requires", []))
  command = step.get("command", "").format(source_cores=config.get("source_cores", 8))
  if command:
    command_parts = shlex.split(command)
    if command_parts and command_parts[0] == "snakemake":
      command_parts = [sys.executable, "-m", "snakemake", *command_parts[1:]]
    subprocess.run(command_parts, check=True)
  write_stamp(output_path, step_id, command)
