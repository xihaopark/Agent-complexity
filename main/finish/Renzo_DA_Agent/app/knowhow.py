"""knowhow — Domain knowledge loader for Renzo agent.

Loads markdown documents from files or strings and makes their content
available as LLM context for the planner and coder nodes.

Usage:
    loader = KnowHowLoader()
    loader.add_from_file("path/to/skill.md")
    loader.add_from_string("# My Guide\n\nStep 1: ...", name="My Guide")

    # Get concatenated context for LLM prompts (truncated to max_chars)
    context = loader.get_context(max_chars=4000)

    # Get individual documents
    docs = loader.documents
"""
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
FINISH_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class KnowHowDocument:
    """A single know-how document."""
    id: str
    name: str
    description: str
    content: str
    source: str = ""  # file path or "inline"
    metadata: Dict = field(default_factory=dict)


@dataclass
class WorkflowSkillSpec:
    """Structured orchestration metadata extracted from a workflow step skill."""

    workflow_id: str
    workflow_name: str
    step_id: str
    step_name: str
    upstream_requirements: List[str] = field(default_factory=list)
    downstream_handoff: List[str] = field(default_factory=list)
    step_file: str = ""
    config_file: str = ""
    shared_environment: str = ""
    completion_artifacts: List[str] = field(default_factory=list)
    representative_outputs: List[str] = field(default_factory=list)
    execution_targets: List[str] = field(default_factory=list)
    guardrails: List[str] = field(default_factory=list)
    source_path: str = ""
    name: str = ""
    description: str = ""


class KnowHowLoader:
    """Loads and manages domain knowledge documents for the agent."""

    def __init__(self):
        self.documents: List[KnowHowDocument] = []
        self._doc_index: Dict[str, KnowHowDocument] = {}

    def add_from_file(self, file_path: str, name: Optional[str] = None,
                      description: Optional[str] = None) -> str:
        """Load a know-how document from a markdown file.

        Args:
            file_path: Path to the .md or .txt file.
            name: Optional display name. Derived from filename if not given.
            description: Optional description. Auto-generated if not given.

        Returns:
            The document ID.
        """
        path = Path(file_path)
        if not path.is_file():
            logger.warning("Know-how file not found: %s", file_path)
            return ""

        content = path.read_text(encoding="utf-8")
        skill_meta = _extract_skill_frontmatter(content) if path.stem.upper() == "SKILL" else {}

        doc_id = (
            skill_meta.get("name")
            or (path.parent.name if path.stem.upper() == "SKILL" else path.stem)
        ).lower().replace(" ", "_").replace("-", "_")

        if name is None:
            if skill_meta.get("name"):
                name = skill_meta["name"]
            elif path.stem.upper() == "SKILL":
                name = path.parent.name.replace("_", " ").replace("-", " ").title()
            else:
                name = path.stem.replace("_", " ").replace("-", " ").title()

        if description is None:
            if skill_meta.get("description"):
                description = skill_meta["description"]
            else:
                for line in content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and line != "---":
                        description = line[:200]
                        break
            if not description:
                description = f"Know-how document: {name}"

        doc = KnowHowDocument(
            id=doc_id,
            name=name,
            description=description,
            content=content,
            source=str(path.resolve()),
        )
        self._add_doc(doc)
        logger.info("Loaded know-how: '%s' (%d chars) from %s", name, len(content), file_path)
        return doc_id

    def add_from_string(self, content: str, name: Optional[str] = None,
                        description: Optional[str] = None) -> str:
        """Add a know-how document from a string.

        Args:
            content: The markdown content.
            name: Optional display name.
            description: Optional description.

        Returns:
            The document ID.
        """
        if name is None:
            # Try to extract title from first H1
            for line in content.split("\n"):
                if line.startswith("# "):
                    name = line[2:].strip()
                    break
            if not name:
                name = f"Document {len(self.documents) + 1}"

        doc_id = name.lower().replace(" ", "_").replace("-", "_")[:64]

        if description is None:
            description = f"Know-how document: {name}"

        doc = KnowHowDocument(
            id=doc_id,
            name=name,
            description=description,
            content=content,
            source="inline",
        )
        self._add_doc(doc)
        logger.info("Added know-how: '%s' (%d chars)", name, len(content))
        return doc_id

    def _add_doc(self, doc: KnowHowDocument) -> None:
        """Add a document, replacing any existing one with the same ID."""
        if doc.id in self._doc_index:
            # Replace existing
            self.documents = [d for d in self.documents if d.id != doc.id]
        self.documents.append(doc)
        self._doc_index[doc.id] = doc

    def get_context(self, max_chars: int = 8000) -> str:
        """Get concatenated know-how content for LLM prompts.

        Documents are concatenated with headers. Content is truncated
        to max_chars to fit within LLM context limits.
        """
        if not self.documents:
            return ""

        parts = []
        total = 0
        for doc in self.documents:
            header = f"\n--- {doc.name} ---\n"
            if total + len(header) + len(doc.content) > max_chars:
                # Truncate this document to fit
                remaining = max_chars - total - len(header) - 50  # buffer
                if remaining > 200:
                    parts.append(header)
                    parts.append(doc.content[:remaining] + "\n... [truncated]")
                break
            parts.append(header)
            parts.append(doc.content)
            total += len(header) + len(doc.content)

        return "\n".join(parts)

    def get_document(self, doc_id: str) -> Optional[KnowHowDocument]:
        """Get a specific document by ID."""
        return self._doc_index.get(doc_id)

    def list_documents(self) -> List[Dict]:
        """List all loaded documents (summary only)."""
        return [
            {
                "id": doc.id,
                "name": doc.name,
                "description": doc.description,
                "source": doc.source,
                "chars": len(doc.content),
            }
            for doc in self.documents
        ]

    def clear(self) -> None:
        """Remove all documents."""
        self.documents.clear()
        self._doc_index.clear()


def find_skill_files(base_dir: Optional[str] = None) -> List[str]:
    """Find SKILL.md files in standard project skill directories.

    Searches parent directories for .trae/skills first, then .cursor/skills.
    """
    if base_dir is None:
        cwd = Path(os.getcwd()).resolve()
        candidates = []
        for root in [cwd, *cwd.parents]:
            candidates.append(root / ".trae" / "skills")
            candidates.append(root / ".cursor" / "skills")
    else:
        candidates = [Path(base_dir)]

    skill_files = []
    seen = set()
    for skills_dir in candidates:
        if skills_dir.is_dir():
            for skill_md in sorted(skills_dir.rglob("SKILL.md")):
                resolved = str(skill_md.resolve())
                if resolved in seen:
                    continue
                seen.add(resolved)
                skill_files.append(resolved)

    return skill_files


def _strip_frontmatter_value(value: str) -> str:
    return value.strip().strip("'").strip('"')


def _extract_skill_frontmatter(content: str) -> Dict[str, Any]:
    if not content.startswith("---\n"):
        return {}

    _, _, remainder = content.partition("---\n")
    frontmatter, separator, _ = remainder.partition("\n---")
    if not separator:
        return {}

    meta: Dict[str, Any] = {}
    current_block: Optional[str] = None
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if raw_line.startswith((" ", "\t")):
            if current_block == "metadata" and ":" in line:
                key, value = line.split(":", 1)
                meta.setdefault("metadata", {})[key.strip()] = _strip_frontmatter_value(value)
            continue
        if ":" not in line:
            current_block = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = _strip_frontmatter_value(value)
        if key == "metadata":
            meta.setdefault("metadata", {})
            current_block = "metadata"
            continue
        current_block = None
        if value:
            meta[key] = value
    return meta


def _extract_section(content: str, title: str) -> str:
    pattern = rf"^##\s+{re.escape(title)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, content, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_backtick_items(text: str) -> List[str]:
    items = [item.strip() for item in re.findall(r"`([^`]+)`", text or "") if item.strip()]
    if items:
        return items
    value = (text or "").strip().lower()
    if value in {"none", "n/a", "na"}:
        return []
    return []


def _extract_scalar_from_bullet(section: str, label: str) -> str:
    pattern = rf"^- {re.escape(label)}:\s*(.+)$"
    match = re.search(pattern, section, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_plain_bullets(section: str) -> List[str]:
    items: List[str] = []
    for line in (section or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            value = stripped[2:].strip()
            if value:
                items.append(value)
    return items


def parse_workflow_skill_file(file_path: str) -> Optional[WorkflowSkillSpec]:
    path = Path(file_path)
    if not path.is_file():
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None

    meta = _extract_skill_frontmatter(content)
    metadata = meta.get("metadata") if isinstance(meta.get("metadata"), dict) else {}
    workflow_id = str(metadata.get("workflow_id") or "").strip()
    step_id = str(metadata.get("step_id") or "").strip()
    if not workflow_id or not step_id:
        return None

    orchestration = _extract_section(content, "Orchestration")
    guardrails = _extract_section(content, "Guardrails")
    return WorkflowSkillSpec(
        workflow_id=workflow_id,
        workflow_name=str(metadata.get("workflow_name") or "").strip(),
        step_id=step_id,
        step_name=str(metadata.get("step_name") or meta.get("name") or step_id).strip(),
        upstream_requirements=_extract_backtick_items(
            _extract_scalar_from_bullet(orchestration, "Upstream requirements")
        ),
        downstream_handoff=_extract_backtick_items(
            _extract_scalar_from_bullet(orchestration, "Downstream handoff")
        ),
        step_file=_extract_scalar_from_bullet(orchestration, "Step file").strip("`"),
        config_file=_extract_scalar_from_bullet(orchestration, "Config file").strip("`"),
        shared_environment=_extract_scalar_from_bullet(orchestration, "Shared environment").strip("`"),
        completion_artifacts=_extract_backtick_items(
            _extract_scalar_from_bullet(orchestration, "Completion artifacts")
        ),
        representative_outputs=_extract_backtick_items(
            _extract_scalar_from_bullet(orchestration, "Representative outputs")
        ),
        execution_targets=_extract_backtick_items(
            _extract_scalar_from_bullet(orchestration, "Execution targets")
        ),
        guardrails=_extract_plain_bullets(guardrails),
        source_path=str(path.resolve()),
        name=str(meta.get("name") or path.parent.name).strip(),
        description=str(meta.get("description") or "").strip(),
    )


def _workflow_finish_dir(workflow_id: str) -> Optional[Path]:
    candidates = [FINISH_ROOT / workflow_id]
    if not workflow_id.endswith("-finish"):
        candidates.append(FINISH_ROOT / f"{workflow_id}-finish")
    for path in candidates:
        if path.is_dir():
            return path.resolve()
    return None


def _workflow_valid_step_ids(workflow_id: str) -> set[str]:
    finish_dir = _workflow_finish_dir(workflow_id)
    if finish_dir is None:
        return set()
    valid: set[str] = set()
    config_path = finish_dir / "config_basic" / "config.yaml"
    if config_path.is_file():
        try:
            import yaml as _yaml

            data = _yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            steps = data.get("steps")
            if isinstance(steps, dict):
                valid.update(str(key).strip() for key in steps.keys() if str(key).strip())
        except Exception:
            logger.debug("Failed to read workflow config for skill filtering: %s", config_path, exc_info=True)
    steps_dir = finish_dir / "steps"
    if steps_dir.is_dir():
        for step_file in steps_dir.glob("*.smk"):
            if step_file.name == "common.smk":
                continue
            valid.add(step_file.stem)
    return valid


def _is_valid_finish_skill_spec(spec: WorkflowSkillSpec) -> bool:
    finish_dir = _workflow_finish_dir(spec.workflow_id)
    if finish_dir is None:
        return False
    valid_step_ids = _workflow_valid_step_ids(spec.workflow_id)
    if spec.step_id not in valid_step_ids:
        return False
    if spec.step_file:
        normalized = spec.step_file.strip().replace("\\", "/").lstrip("./")
        expected = f"finish/{finish_dir.name}/steps/{spec.step_id}.smk"
        if normalized != expected:
            return False
        if not (FINISH_ROOT.parent / normalized).is_file():
            return False
    return True


def find_workflow_skill_specs(
    workflow_id: str,
    base_dir: Optional[str] = None,
) -> List[WorkflowSkillSpec]:
    specs: List[WorkflowSkillSpec] = []
    for skill_path in find_skill_files(base_dir=base_dir):
        spec = parse_workflow_skill_file(skill_path)
        if spec and spec.workflow_id == workflow_id and _is_valid_finish_skill_spec(spec):
            specs.append(spec)
    return sorted(
        specs,
        key=lambda item: (
            item.step_id,
        ),
    )
