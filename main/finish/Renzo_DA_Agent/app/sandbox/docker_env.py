from __future__ import annotations

import json
import os
import subprocess
import tempfile
from typing import Dict


class DockerSandbox:
    def __init__(self, image: str = "python:3.10-slim", r_image: str = "rocker/tidyverse:latest"):
        self.image = image
        self.r_image = r_image

    def run_code(self, code: str, working_dir: str) -> Dict:
        os.makedirs(working_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=working_dir) as fh:
            fh.write(code)
            script_path = fh.name

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{working_dir}:/workspace",
            "-w",
            "/workspace",
            self.image,
            "python",
            os.path.basename(script_path),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            status = "success" if result.returncode == 0 else "error"
            return {
                "status": status,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as exc:
            return {"status": "error", "stdout": "", "stderr": str(exc), "returncode": -1}

    def run_r_code(self, code: str, working_dir: str) -> Dict:
        """Execute R code via Rscript inside a Docker container with R/tidyverse."""
        os.makedirs(working_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, dir=working_dir) as fh:
            fh.write(code)
            script_path = fh.name

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{working_dir}:/workspace",
            "-w",
            "/workspace",
            self.r_image,
            "Rscript",
            os.path.basename(script_path),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=600)
            status = "success" if result.returncode == 0 else "error"
            return {
                "status": status,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "stdout": "",
                "stderr": "R script execution timed out (600s limit).",
                "returncode": -1,
            }
        except Exception as exc:
            return {"status": "error", "stdout": "", "stderr": str(exc), "returncode": -1}

    def install_packages(self, packages: list[str], working_dir: str) -> Dict:
        if not packages:
            return {"status": "skipped"}

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{working_dir}:/workspace",
            "-w",
            "/workspace",
            self.image,
            "pip",
            "install",
        ] + packages

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            status = "success" if result.returncode == 0 else "error"
            return {
                "status": status,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "packages": packages,
            }
        except Exception as exc:
            return {"status": "error", "stdout": "", "stderr": str(exc), "returncode": -1}

    def install_r_packages(self, packages: list[str], working_dir: str) -> Dict:
        """Install R packages inside a Docker container."""
        if not packages:
            return {"status": "skipped"}

        pkg_str = ", ".join(f'"{p}"' for p in packages)
        r_code = f'install.packages(c({pkg_str}), repos="https://cloud.r-project.org", quiet=TRUE)'
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{working_dir}:/workspace",
            "-w",
            "/workspace",
            self.r_image,
            "Rscript",
            "-e",
            r_code,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=600)
            status = "success" if result.returncode == 0 else "error"
            return {
                "status": status,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "packages": packages,
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "stdout": "", "stderr": "R package install timed out.", "returncode": -1}
        except Exception as exc:
            return {"status": "error", "stdout": "", "stderr": str(exc), "returncode": -1}
