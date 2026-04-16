"""File writing and editing tools (local workspace only)."""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Optional, Type

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


def _validate_rel_path(rel_path: str) -> tuple[bool, str, str]:
    rel_path = rel_path.strip().strip("/")
    if not rel_path:
        return False, "Error: empty file path.", ""
    if ".." in Path(rel_path).parts:
        return False, f"Error: '..' not allowed in path: {rel_path}", ""
    return True, "", rel_path


def _resolve_local(rel_path: str, data_root: Path) -> tuple[bool, str, Path]:
    ok, err, cleaned = _validate_rel_path(rel_path)
    if not ok:
        return False, err, data_root
    resolved = (data_root / cleaned).resolve()
    try:
        resolved.relative_to(data_root.resolve())
    except ValueError:
        return False, f"Error: path escapes workspace: {rel_path}", data_root
    return True, "", resolved


def _extract_snippet(
    content: str, old_text: str, new_text: str, context_lines: int = 3
) -> str:
    idx = content.find(new_text)
    if idx == -1:
        return ""
    lines = content.splitlines(keepends=True)
    char_count = 0
    start_line = 0
    for i, line in enumerate(lines):
        if char_count + len(line) > idx:
            start_line = i
            break
        char_count += len(line)
    new_line_count = new_text.count("\n") + 1
    end_line = start_line + new_line_count
    snippet_start = max(0, start_line - context_lines)
    snippet_end = min(len(lines), end_line + context_lines)
    snippet_lines = [f"{i + 1:>4}| {lines[i].rstrip()}" for i in range(snippet_start, snippet_end)]
    return f"Showing lines {snippet_start + 1}-{snippet_end} of {len(lines)}:\n" + "\n".join(snippet_lines)


class WriteFileInput(BaseModel):
    file_path: str = Field(description="Path to the file (relative to workspace).")
    content: str = Field(description="The full content to write.")


class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = (
        "Write content to a file in the workspace (create or overwrite). "
        "Parent directories are created automatically. For partial edits, use edit_file."
    )
    args_schema: Type[BaseModel] = WriteFileInput
    data_root: Optional[Path] = None

    def __init__(self, data_root: Optional[Path] = None, **kwargs):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve() if data_root else None

    def _run(self, file_path: str, content: str) -> str:
        ok, err, resolved = _resolve_local(file_path, self.data_root)
        if not ok:
            return err
        is_new = not resolved.exists()
        try:
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(content, encoding="utf-8")
        except Exception as e:
            return f"Error writing {file_path}: {e}"
        n_lines = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
        verb = "Created new file" if is_new else "Overwrote"
        return f"{verb}: {file_path} ({n_lines} lines, {len(content)} chars)."


class EditFileInput(BaseModel):
    file_path: str = Field(description="Path to the file (relative to workspace). Use old_text='' to create.")
    old_text: str = Field(description="Exact text to find and replace. Empty string to create a new file.")
    new_text: str = Field(description="Replacement text or full file content when creating.")
    use_regex: bool = Field(default=False, description="If True, old_text is a regex.")
    replace_all: bool = Field(default=False, description="If True, replace every occurrence.")


class EditFileTool(BaseTool):
    name: str = "edit_file"
    description: str = (
        "Edit a file by replacing text, or create a new file (old_text=''). "
        "By default old_text must match exactly once; set replace_all=True to replace all."
    )
    args_schema: Type[BaseModel] = EditFileInput
    data_root: Optional[Path] = None

    def __init__(self, data_root: Optional[Path] = None, **kwargs):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve() if data_root else None

    def _run(
        self,
        file_path: str,
        old_text: str,
        new_text: str,
        use_regex: bool = False,
        replace_all: bool = False,
    ) -> str:
        return self._run_local(file_path, old_text, new_text, use_regex, replace_all)

    @staticmethod
    def _apply_edit(
        original: Optional[str],
        old_text: str,
        new_text: str,
        use_regex: bool,
        replace_all: bool,
        file_path: str,
        file_exists: bool,
    ) -> tuple[bool, str, str, int]:
        if old_text == "" and not use_regex:
            if not file_exists:
                return True, "", new_text, 0
            return False, f"Error: {file_path} already exists. Use write_file or provide old_text.", "", 0
        if original is None:
            return False, f"Error: file not found: {file_path}. Use old_text='' to create.", "", 0
        original = original.replace("\r\n", "\n")
        if use_regex:
            try:
                pattern = re.compile(old_text, re.DOTALL)
            except re.error as e:
                return False, f"Error: invalid regex: {e}", "", 0
            count = 0 if replace_all else 1
            new_content, n = pattern.subn(new_text, original, count=count)
            if n == 0:
                return False, f"Error: regex pattern not found in {file_path}.", "", 0
            if new_content == original:
                return False, "No changes made (replacement identical).", "", 0
            return True, "", new_content, n
        occurrences = original.count(old_text)
        if occurrences == 0:
            preview = original[:500] + ("…" if len(original) > 500 else "")
            return False, f"Error: old_text not found in {file_path}.\nFile preview:\n{preview}", "", 0
        if occurrences > 1 and not replace_all:
            return False, f"Error: old_text matches {occurrences} locations. Add context or set replace_all=True.", "", 0
        if old_text == new_text:
            return False, "No changes: old_text and new_text are identical.", "", 0
        if replace_all:
            new_content = original.replace(old_text, new_text)
            n = occurrences
        else:
            new_content = original.replace(old_text, new_text, 1)
            n = 1
        return True, "", new_content, n

    def _run_local(
        self,
        file_path: str,
        old_text: str,
        new_text: str,
        use_regex: bool,
        replace_all: bool,
    ) -> str:
        ok, err, resolved = _resolve_local(file_path, self.data_root)
        if not ok:
            return err
        file_exists = resolved.exists()
        original = resolved.read_text(encoding="utf-8") if file_exists else None
        ok, err, new_content, n = self._apply_edit(
            original, old_text, new_text, use_regex, replace_all, file_path, file_exists
        )
        if not ok:
            return err
        try:
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(new_content, encoding="utf-8")
        except Exception as e:
            return f"Error writing {file_path}: {e}"
        if not file_exists:
            return f"Created new file: {file_path} ({new_content.count(chr(10)) + 1} lines)."
        result = f"Edited {file_path}: {n} replacement(s) made."
        snippet = _extract_snippet(new_content, old_text, new_text)
        if snippet:
            result += f"\n{snippet}"
        return result
