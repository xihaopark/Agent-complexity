from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path
from typing import Iterable


_DEFAULT_CONDA_CANDIDATES = (
    "/root/miniconda3/bin/conda",
    "/opt/conda/bin/conda",
    str((Path.home() / "miniconda3" / "bin" / "conda").resolve()),
    str((Path.home() / "mambaforge" / "bin" / "conda").resolve()),
    str((Path.home() / "anaconda3" / "bin" / "conda").resolve()),
)


def _default_runtime_cache_root() -> Path:
    return (Path(__file__).resolve().parents[1] / "data" / "cache" / "runtime").resolve()


def _scoped_cache_root(base_root: Path, scope: str | None) -> Path:
    text = str(scope or "").strip()
    if not text:
        return base_root
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in text).strip("._")
    if not safe:
        return base_root
    return (base_root / safe).resolve()


def _short_tmp_root(cache_root: Path) -> Path:
    digest = hashlib.sha1(str(cache_root).encode("utf-8")).hexdigest()[:12]
    return (cache_root / "tmp" / digest).resolve()


def _unique_candidates(candidates: Iterable[str | os.PathLike[str] | None]) -> list[str]:
    resolved: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate is None:
            continue
        text = os.fspath(candidate).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        resolved.append(text)
    return resolved


def find_conda_bin(explicit: str | None = None) -> str:
    which_conda = shutil.which("conda")
    for candidate in _unique_candidates(
        (
            explicit,
            os.environ.get("CONDA_EXE"),
            which_conda,
            *_DEFAULT_CONDA_CANDIDATES,
        )
    ):
        path = Path(candidate).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    return ""


def build_runtime_env(extra_env: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    if extra_env:
        env.update({key: value for key, value in extra_env.items() if value is not None})

    # Nested Snakemake runs should not inherit the caller's active Python/conda
    # environment, otherwise wrapper jobs can execute against a polluted PATH or
    # stale activation state from the outer workflow runner.
    for key in (
        "CONDA_PREFIX",
        "CONDA_DEFAULT_ENV",
        "CONDA_PROMPT_MODIFIER",
        "CONDA_SHLVL",
        "CONDA_PYTHON_EXE",
        "_CE_CONDA",
        "_CE_M",
        "PYTHONHOME",
        "PYTHONPATH",
        "VIRTUAL_ENV",
    ):
        env.pop(key, None)

    base_cache_root = Path(
        env.get("WORKFLOW_RUNTIME_BASE_CACHE_DIR")
        or env.get("WORKFLOW_RUNTIME_CACHE_DIR")
        or _default_runtime_cache_root()
    ).expanduser().resolve()
    cache_root = _scoped_cache_root(base_cache_root, env.get("WORKFLOW_RUNTIME_CACHE_SCOPE"))
    xdg_cache_home = cache_root / "xdg"
    tmp_dir = _short_tmp_root(cache_root)
    conda_prefix_override = (env.get("RENZO_SNAKEMAKE_CONDA_PREFIX") or env.get("SNAKEMAKE_CONDA_PREFIX") or "").strip()
    snakemake_conda_prefix = (
        Path(conda_prefix_override).expanduser().resolve()
        if conda_prefix_override
        else (base_cache_root / "snakemake" / "conda")
    )
    conda_pkgs_dir = (base_cache_root / "conda" / "pkgs").resolve()
    conda_envs_dir = (base_cache_root / "conda" / "envs").resolve()
    for path in (cache_root, xdg_cache_home, tmp_dir, snakemake_conda_prefix, conda_pkgs_dir, conda_envs_dir):
        path.mkdir(parents=True, exist_ok=True)

    env["WORKFLOW_RUNTIME_BASE_CACHE_DIR"] = str(base_cache_root)
    env["WORKFLOW_RUNTIME_CACHE_DIR"] = str(cache_root)
    env["XDG_CACHE_HOME"] = str(xdg_cache_home)
    env["TMPDIR"] = str(tmp_dir)
    env["SNAKEMAKE_CONDA_PREFIX"] = str(snakemake_conda_prefix)
    env.setdefault("CONDA_PKGS_DIRS", str(conda_pkgs_dir))
    env.setdefault("CONDA_ENVS_PATH", str(conda_envs_dir))
    env.setdefault("RENZO_SHARED_ARTIFACT_CACHE_DIR", str((base_cache_root / "finish-step-artifacts").resolve()))
    env.setdefault("RENZO_RUNTIME_ROOT", str(Path(__file__).resolve().parents[1]))
    env.setdefault("RENZO_NESTED_SNAKEMAKE_SCHEDULER", "greedy")
    env.setdefault("RENZO_NESTED_SNAKEMAKE_RETRIES", "1")
    env.setdefault("RENZO_NESTED_SNAKEMAKE_RETRY_DELAY_SECONDS", "2")

    conda_bin = find_conda_bin(env.get("CONDA_EXE"))
    if conda_bin:
        env["CONDA_EXE"] = conda_bin
        conda_dir = str(Path(conda_bin).resolve().parent)
        path_parts = [part for part in env.get("PATH", "").split(os.pathsep) if part]
        if conda_dir not in path_parts:
            env["PATH"] = os.pathsep.join([conda_dir, *path_parts]) if path_parts else conda_dir

    env.setdefault("WORKFLOW_SNAKEMAKE_ENV", "snakemake")
    return env
