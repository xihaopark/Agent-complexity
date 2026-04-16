"""Todo-list tool for task planning (local workspace)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Type

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

_TODO_FILENAME = ".todos.json"


class TodoItem(BaseModel):
    id: str = Field(description="Short unique identifier.")
    content: str = Field(description="What needs to be done.")
    status: str = Field(default="pending", description="pending | in_progress | completed.")


class TodoWriteInput(BaseModel):
    todos: List[TodoItem] = Field(
        description="Full updated todo list (replaces previous). Each item: id, content, status."
    )


class TodoWriteTool(BaseTool):
    name: str = "todo_write"
    description: str = (
        "Create or update a task plan. Send the FULL list each time (replaces previous). "
        "Each item: id, content, status (pending | in_progress | completed)."
    )
    args_schema: Type[BaseModel] = TodoWriteInput
    data_root: Optional[Path] = None  # type: ignore[assignment]

    def __init__(self, data_root: Path, **kwargs):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve()

    @property
    def _todo_path(self) -> Path:
        return self.data_root / _TODO_FILENAME

    def _read_todos(self) -> List[dict]:
        if not self._todo_path.exists():
            return []
        try:
            data = json.loads(self._todo_path.read_text(encoding="utf-8"))
            return data.get("todos", [])
        except Exception:
            return []

    def _write_todos(self, todos: List[dict]) -> None:
        self._todo_path.parent.mkdir(parents=True, exist_ok=True)
        self._todo_path.write_text(
            json.dumps({"todos": todos}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _run(self, todos: List[dict]) -> str:
        normalised = []
        for item in todos:
            if isinstance(item, TodoItem):
                normalised.append(item.model_dump())
            elif isinstance(item, dict):
                normalised.append(item)
            else:
                normalised.append(dict(item))
        valid_statuses = {"pending", "in_progress", "completed"}
        for item in normalised:
            st = item.get("status", "pending")
            if st not in valid_statuses:
                return f"Error: invalid status '{st}'. Must be one of: {', '.join(sorted(valid_statuses))}."
        ids = [item.get("id", "") for item in normalised]
        if len(ids) != len(set(ids)):
            dupes = [x for x in ids if ids.count(x) > 1]
            return f"Error: duplicate todo IDs: {set(dupes)}."
        in_progress = [t for t in normalised if t.get("status") == "in_progress"]
        warning = ""
        if len(in_progress) > 1:
            warning = "\n⚠ Warning: multiple items in_progress — ideally only one."
        self._write_todos(normalised)
        counts = {"pending": 0, "in_progress": 0, "completed": 0}
        for item in normalised:
            st = item.get("status", "pending")
            counts[st] = counts.get(st, 0) + 1
        lines = [f"Todo list updated — {len(normalised)} item(s):"]
        for item in normalised:
            marker = {"pending": "○", "in_progress": "▶", "completed": "✓"}.get(item["status"], "?")
            lines.append(f"  {marker} [{item['id']}] {item['content']}")
        lines.append(f"\nSummary: {counts['completed']} done, {counts['in_progress']} in progress, {counts['pending']} pending.")
        if warning:
            lines.append(warning)
        return "\n".join(lines)
