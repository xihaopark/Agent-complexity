from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from typing import Dict


class LocalSandbox:
    def run_code(self, code: str, working_dir: str) -> Dict:
        os.makedirs(working_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=working_dir) as fh:
            fh.write(code)
            script_path = fh.name

        cmd = ["python3", os.path.basename(script_path)]
        try:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False,
            )
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
        """Execute R code via Rscript in a local environment."""
        os.makedirs(working_dir, exist_ok=True)

        # Check that Rscript is available
        if not shutil.which("Rscript"):
            return {
                "status": "error",
                "stdout": "",
                "stderr": "Rscript not found. Please install R (r-base) to run R code.",
                "returncode": -1,
            }

        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, dir=working_dir) as fh:
            fh.write(code)
            script_path = fh.name

        cmd = ["Rscript", os.path.basename(script_path)]
        try:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False,
                timeout=600,  # R scripts can be slow (package loading, etc.)
            )
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

        cmd = ["python3", "-m", "pip", "install"] + packages
        try:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False,
            )
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
        """Install R packages via install.packages()."""
        if not packages:
            return {"status": "skipped"}

        if not shutil.which("Rscript"):
            return {
                "status": "error",
                "stdout": "",
                "stderr": "Rscript not found.",
                "returncode": -1,
            }

        pkg_str = ", ".join(f'"{p}"' for p in packages)
        r_code = f'install.packages(c({pkg_str}), repos="https://cloud.r-project.org", quiet=TRUE)'
        cmd = ["Rscript", "-e", r_code]
        try:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False,
                timeout=600,
            )
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
