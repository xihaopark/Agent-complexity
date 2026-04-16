from pathlib import Path
import shlex
import subprocess
import sys
import os


def _runtime_helper():
  root = os.environ.get("RENZO_RUNTIME_ROOT", "").strip()
  if root:
    path = (Path(root) / "app" / "finish_step_runtime.py").resolve()
    if path.exists():
      return path
  candidate = (Path(".").resolve().parent / "Renzo_DA_Agent" / "app" / "finish_step_runtime.py").resolve()
  return candidate if candidate.exists() else None


def run_step(step_id, output_path):
  helper = _runtime_helper()
  if helper is None:
    raise RuntimeError("finish_step_runtime.py not found")
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
