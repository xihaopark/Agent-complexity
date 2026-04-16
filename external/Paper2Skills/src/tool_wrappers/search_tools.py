"""Glob and grep tools (local workspace only)."""
from __future__ import annotations

import fnmatch
import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Type

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)

_MAX_GLOB_RESULTS = 100
_MAX_GREP_MATCHES = 200
_EXCLUDE_DIRS = (".git", "__pycache__", "node_modules", ".tox", ".mypy_cache", ".venv", "venv")


def _validate_subpath(rel: str) -> tuple[bool, str, str]:
    rel = rel.strip().strip("/")
    if not rel:
        return True, "", ""
    if ".." in Path(rel).parts:
        return False, f"Error: '..' not allowed in path: {rel}", ""
    return True, "", rel


def _parse_grep_output(
    stdout: str, search_root: Path, data_root: Path, limit: int
) -> List[tuple[str, int, str]]:
    matches: List[tuple[str, int, str]] = []
    if not stdout:
        return matches
    for line in stdout.splitlines():
        if not line.strip():
            continue
        first_colon = line.find(":")
        if first_colon == -1:
            continue
        second_colon = line.find(":", first_colon + 1)
        if second_colon == -1:
            continue
        fpath_raw = line[:first_colon]
        lineno_str = line[first_colon + 1 : second_colon]
        content = line[second_colon + 1 :].rstrip()
        try:
            lineno = int(lineno_str)
        except ValueError:
            continue
        abs_path = (search_root / fpath_raw).resolve()
        try:
            rel = str(abs_path.relative_to(data_root.resolve()))
        except ValueError:
            rel = fpath_raw.lstrip("./")
        matches.append((rel, lineno, content))
        if len(matches) >= limit:
            break
    return matches


class GlobInput(BaseModel):
    pattern: str = Field(description="Glob pattern, e.g. '**/*.py', '*.md'.")
    path: str = Field(default="", description="Sub-directory to search in (empty = whole workspace).")


class GlobInWorkspaceTool(BaseTool):
    name: str = "glob_files"
    description: str = (
        "Find files matching a glob pattern. Returns paths sorted by mtime (newest first). "
        "Examples: '**/*.py', 'tests/**/*.py'. Use 'path' to limit to a subdirectory."
    )
    args_schema: Type[BaseModel] = GlobInput
    data_root: Optional[Path] = None
    max_results: int = _MAX_GLOB_RESULTS

    def __init__(
        self,
        data_root: Optional[Path] = None,
        max_results: int = _MAX_GLOB_RESULTS,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve() if data_root else None
        self.max_results = max_results

    def _run(self, pattern: str, path: str = "") -> str:
        ok, err, subdir = _validate_subpath(path)
        if not ok:
            return err
        search_root = self.data_root / subdir if subdir else self.data_root
        if not search_root.exists():
            return f"Error: directory does not exist: {path or '.'}"
        try:
            matches = sorted(
                (p for p in search_root.glob(pattern) if p.is_file()),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
        except Exception as e:
            return f"Error running glob: {e}"
        if not matches:
            loc = f" in '{path}'" if path else ""
            return f'No files found matching "{pattern}"{loc}.'
        total = len(matches)
        truncated = total > self.max_results
        shown = matches[: self.max_results]
        rel_paths = []
        for p in shown:
            try:
                rel_paths.append(str(p.relative_to(self.data_root)))
            except ValueError:
                rel_paths.append(str(p))
        loc = f" in '{path}'" if path else ""
        header = f'Found {total} file(s) matching "{pattern}"{loc} (newest first):\n'
        body = "\n".join(rel_paths)
        footer = f"\n... ({total - self.max_results} more)" if truncated else ""
        return header + body + footer


class GrepInput(BaseModel):
    pattern: str = Field(description="Regex pattern to search for.")
    path: str = Field(default="", description="Sub-directory to search in.")
    glob: str = Field(default="", description="Glob to filter files, e.g. '*.py'.")
    limit: int = Field(default=0, description="Max matching lines (0 = internal cap).")


class GrepInWorkspaceTool(BaseTool):
    name: str = "grep_files"
    description: str = (
        "Search file contents by regex. Results grouped by file with line numbers. "
        "Use glob='*.py' to filter. Uses ripgrep when available."
    )
    args_schema: Type[BaseModel] = GrepInput
    data_root: Optional[Path] = None
    max_matches: int = _MAX_GREP_MATCHES

    def __init__(
        self,
        data_root: Optional[Path] = None,
        max_matches: int = _MAX_GREP_MATCHES,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve() if data_root else None
        self.max_matches = max_matches

    def _run(self, pattern: str, path: str = "", glob: str = "", limit: int = 0) -> str:
        ok, err, subdir = _validate_subpath(path)
        if not ok:
            return err
        search_root = self.data_root / subdir if subdir else self.data_root
        if not search_root.exists():
            return f"Error: directory does not exist: {path or '.'}"
        effective_limit = limit if limit > 0 else self.max_matches
        matches = self._try_ripgrep(pattern, search_root, glob, effective_limit)
        if matches is None:
            matches = self._try_git_grep(pattern, search_root, glob, effective_limit)
        if matches is None:
            matches = self._try_system_grep(pattern, search_root, glob, effective_limit)
        if matches is None:
            matches = self._python_grep(pattern, search_root, glob, effective_limit)
        return self._format_results(pattern, path, glob, matches, effective_limit)

    def _try_ripgrep(self, pattern: str, search_root: Path, glob: str, limit: int) -> Optional[List[tuple]]:
        if shutil.which("rg") is None:
            return None
        args = ["rg", "--line-number", "--no-heading", "--with-filename", "--ignore-case", "--regexp", pattern, "--threads", "4"]
        if glob:
            args.extend(["--glob", glob])
        args.append(str(search_root))
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        if result.returncode == 2:
            return None
        return _parse_grep_output(result.stdout, search_root, self.data_root, limit)

    def _try_git_grep(self, pattern: str, search_root: Path, glob: str, limit: int) -> Optional[List[tuple]]:
        git_dir = search_root
        while git_dir != git_dir.parent:
            if (git_dir / ".git").exists():
                break
            git_dir = git_dir.parent
        else:
            return None
        args = ["git", "grep", "--untracked", "-n", "-E", "--ignore-case", pattern]
        if glob:
            args.extend(["--", glob])
        try:
            result = subprocess.run(args, cwd=str(search_root), capture_output=True, text=True, timeout=30)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        if result.returncode not in (0, 1):
            return None
        return _parse_grep_output(result.stdout, search_root, self.data_root, limit)

    def _try_system_grep(self, pattern: str, search_root: Path, glob: str, limit: int) -> Optional[List[tuple]]:
        args = ["grep", "-r", "-n", "-H", "-E", "--ignore-case"]
        for d in _EXCLUDE_DIRS:
            args.append(f"--exclude-dir={d}")
        if glob:
            args.append(f"--include={glob}")
        args.extend([pattern, "."])
        try:
            result = subprocess.run(args, cwd=str(search_root), capture_output=True, text=True, timeout=30)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        if result.returncode not in (0, 1):
            return None
        return _parse_grep_output(result.stdout, search_root, self.data_root, limit)

    def _python_grep(self, pattern: str, search_root: Path, glob_filter: str, limit: int) -> List[tuple]:
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            return [("", 0, f"Error: invalid regex: {e}")]
        matches = []
        glob_pat = glob_filter or "**/*"
        for fpath in search_root.glob(glob_pat):
            if not fpath.is_file():
                continue
            parts = fpath.relative_to(search_root).parts
            if any(p in _EXCLUDE_DIRS or p.startswith(".") for p in parts[:-1]):
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="strict")
            except (UnicodeDecodeError, PermissionError, OSError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if regex.search(line):
                    try:
                        rel = str(fpath.relative_to(self.data_root))
                    except ValueError:
                        rel = str(fpath)
                    matches.append((rel, i, line.rstrip()))
                    if len(matches) >= limit:
                        return matches
        return matches

    def _format_results(
        self,
        pattern: str,
        path: str,
        glob: str,
        matches: List[tuple],
        effective_limit: int,
    ) -> str:
        if not matches:
            loc = f" in '{path}'" if path else ""
            fd = f" (filter: '{glob}')" if glob else ""
            return f'No matches found for "{pattern}"{loc}{fd}.'
        if len(matches) == 1 and matches[0][0] == "" and matches[0][1] == 0:
            return matches[0][2]
        by_file = {}
        for fpath, lineno, line in matches:
            by_file.setdefault(fpath, []).append((lineno, line))
        total = len(matches)
        loc = f" in '{path}'" if path else ""
        fd = f" (filter: '{glob}')" if glob else ""
        parts = [f'Found {total} match(es) for "{pattern}"{loc}{fd}:']
        for fpath in by_file:
            parts.append(f"\nFile: {fpath}")
            for lineno, line in sorted(by_file[fpath], key=lambda x: x[0]):
                parts.append(f"  L{lineno}: {line.strip()}")
        if total >= effective_limit:
            parts.append(f"\n... (capped at {effective_limit})")
        return "\n".join(parts)
