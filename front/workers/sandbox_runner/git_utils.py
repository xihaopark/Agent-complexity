from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _auth_repo_url(repo_url: str, token: str | None) -> str:
    if not token:
        return repo_url
    if repo_url.startswith("https://github.com/"):
        return repo_url.replace("https://", f"https://{token}@")
    return repo_url


def clone_repository(repo_url: str, git_ref: str, destination: Path, token: str | None = None) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    auth_url = _auth_repo_url(repo_url, token)
    subprocess.run(
        ["git", "clone", "--depth", "1", auth_url, str(destination)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "fetch", "--depth", "1", "origin", git_ref],
        check=False,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "checkout", git_ref],
        check=True,
        capture_output=True,
        text=True,
    )


def get_commit_sha(repo_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()
