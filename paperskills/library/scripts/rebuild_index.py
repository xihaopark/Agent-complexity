#!/usr/bin/env python3
"""Rebuild master_index.json from library directories.

Usage:
    python paperskills/library/scripts/rebuild_index.py
"""

import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from indices.library_index import LibraryIndex, PaperEntry


def slug_to_canonical(slug: str) -> str:
    """Convert directory slug to canonical DOI."""
    # Try pattern: 10.1186_s13059-014-0550-8 -> 10.1186/s13059-014-0550-8
    m = re.match(r"^(10\.\d+)_([^_]+)_(.+)$", slug)
    if m:
        a, b, c = m.groups()
        return f"{a}/{b}/{c.replace('_', '-')}"
    # Fallback: just replace underscores
    return slug.replace("_", "/")


def extract_year_from_doi(doi: str) -> int:
    """Try to extract year from DOI patterns."""
    # Pattern like s13059-014-0550 -> 2014
    m = re.search(r"-(\d{4})-", doi)
    if m:
        year = int(m.group(1))
        if 2000 <= year <= 2030:
            return year
    return 0


def scan_library(library_root: Path) -> list[PaperEntry]:
    """Scan all categories and build entries."""
    entries = []
    
    for category in ["methods", "workflows", "references"]:
        cat_dir = library_root / category
        if not cat_dir.exists():
            continue
        
        for item in cat_dir.iterdir():
            if not item.is_dir():
                continue
            
            slug = item.name
            doi = slug_to_canonical(slug)
            skill_md_path = item / "SKILL.md"
            
            if not skill_md_path.exists():
                continue
            
            # Parse SKILL.md for title/tool
            skill_content = skill_md_path.read_text(encoding="utf-8")
            title = ""
            tool = ""
            
            # Extract title from first # heading
            m = re.search(r"^#\s+(.+)$", skill_content, re.MULTILINE)
            if m:
                title = m.group(1).strip()
            
            # Extract tool from ## Method section or metadata
            m = re.search(r"## Method\s*\n+([^#]+)", skill_content, re.DOTALL)
            if m:
                method_text = m.group(1)
                # Try to find tool name in first sentence
                sentences = method_text.split(".")
                if sentences:
                    first = sentences[0]
                    # Look for capitalized tool names
                    tool_match = re.search(r"([A-Z][a-zA-Z0-9_-]{2,})", first)
                    if tool_match:
                        tool = tool_match.group(1)
            
            # If no tool in content, use title as fallback
            if not tool and title:
                # Remove common suffixes/prefixes
                clean = re.sub(r"^(A|An|The)\s+", "", title, flags=re.IGNORECASE)
                clean = re.sub(r"\s+(method|tool|package|software).*$", "", clean, flags=re.IGNORECASE)
                tool = clean[:30]
            
            entry = PaperEntry(
                doi=doi,
                doi_slug=slug,
                title=title or slug,
                authors=[],  # Would need external lookup
                year=extract_year_from_doi(doi),
                tool=tool or "Unknown",
                family="",  # Would need inference
                kind=category[:-1] if category.endswith("s") else category,  # method/workflow/reference
                source="imported" if category == "methods" else "workflow_corpus",
                skill_md_path=f"paperskills/library/{category}/{slug}/SKILL.md",
                pdf_path=str(item / "paper.pdf") if (item / "paper.pdf").exists() else "",
                brat_annotated=(item / "annotations").exists(),
                tasks_recommended=[],
                skill_md_content=skill_content[:5000],  # Cache for search
            )
            entries.append(entry)
    
    return entries


def main():
    library_root = Path(__file__).resolve().parents[2]
    indices_dir = library_root / "indices"
    
    print(f"Scanning library at: {library_root}")
    entries = scan_library(library_root)
    print(f"Found {len(entries)} entries")
    
    # Build and save
    lib = LibraryIndex(library_root)
    for e in entries:
        lib.add(e)
    
    lib.save()
    print(f"✓ Saved master_index.json with {len(lib.entries)} entries")
    
    # Also save by-family and by-tool lookups
    by_family = {}
    by_tool = {}
    for doi, e in lib.entries.items():
        if e.family:
            by_family.setdefault(e.family, []).append(doi)
        if e.tool:
            by_tool.setdefault(e.tool.lower(), []).append(doi)
    
    with open(indices_dir / "by_family.json", "w") as f:
        json.dump(by_family, f, indent=2)
    
    with open(indices_dir / "by_tool.json", "w") as f:
        json.dump(by_tool, f, indent=2)
    
    print(f"  - by_family.json: {len(by_family)} families")
    print(f"  - by_tool.json: {len(by_tool)} tools")


if __name__ == "__main__":
    main()
