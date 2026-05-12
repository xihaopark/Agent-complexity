#!/usr/bin/env python3
"""Import external papers into Paper Skills Library with deduplication.

Usage:
    # Dry-run to preview what would be imported
    python paperskills/library/scripts/import_external_papers.py \\
        --source-dir /path/to/bio_papers --dry-run

    # Actual import
    python paperskills/library/scripts/import_external_papers.py \\
        --source-dir /path/to/bio_papers --output-dir paperskills/library/methods

    # Import as workflows category (not methods)
    python paperskills/library/scripts/import_external_papers.py \\
        --source-dir /path/to/workflow_papers --category workflows

Requirements for source directory:
    - PDF files named with DOI or PMID (e.g., "10.1186_s13059-014-0550-8.pdf")
    - Or: subdirectories with metadata.json containing "doi" field
"""

import argparse
import json
import re
import shutil
from pathlib import Path
from collections import defaultdict
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from indices.library_index import LibraryIndex


def extract_doi_from_filename(filename: str) -> str | None:
    """Try to extract DOI from filename like '10.1186_s13059-014-0550-8.pdf'"""
    # Pattern: 10.XXXX_something_something.pdf
    m = re.match(r"(10\.\d+)_([^_]+)_(.+)\.pdf$", filename, re.IGNORECASE)
    if m:
        a, b, c = m.groups()
        return f"{a}/{b}/{c.replace('_', '-')}"
    # Pattern: PMIDXXXXXX.pdf - not a DOI
    if re.match(r"PMID\d+\.pdf$", filename, re.IGNORECASE):
        return None
    return None


def scan_source_directory(src_dir: Path) -> list[dict]:
    """Scan source directory for papers."""
    papers = []
    
    for item in src_dir.iterdir():
        if item.is_file() and item.suffix.lower() == '.pdf':
            doi = extract_doi_from_filename(item.name)
            papers.append({
                "path": str(item),
                "filename": item.name,
                "doi": doi,
                "doi_slug": doi.replace("/", "_").replace("-", "_") if doi else None,
                "type": "pdf"
            })
        elif item.is_dir() and (item / "metadata.json").exists():
            meta = json.loads((item / "metadata.json").read_text())
            papers.append({
                "path": str(item),
                "filename": item.name,
                "doi": meta.get("doi"),
                "doi_slug": meta.get("doi", "").replace("/", "_").replace("-", "_") if meta.get("doi") else item.name,
                "type": "directory",
                "metadata": meta
            })
    
    return papers


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source-dir", required=True, type=Path, help="Directory containing external papers")
    ap.add_argument("--output-dir", type=Path, default=Path("paperskills/library/methods"), help="Target directory in library")
    ap.add_argument("--category", default="methods", choices=["methods", "workflows", "references"], help="Library category")
    ap.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    ap.add_argument("--auto-skill", action="store_true", help="Attempt auto-extract SKILL.md (requires LLM/parsing)")
    args = ap.parse_args()

    if not args.source_dir.exists():
        print(f"Error: Source directory not found: {args.source_dir}")
        sys.exit(1)

    # Load existing library
    lib = LibraryIndex().load()
    existing_dois = set(lib.entries.keys())
    
    # Scan source
    papers = scan_source_directory(args.source_dir)
    print(f"Scanned {args.source_dir}: found {len(papers)} item(s)")
    
    # Categorize
    to_import = []
    duplicates = []
    no_id = []
    
    for p in papers:
        doi = p.get("doi")
        if not doi:
            no_id.append(p)
            continue
        
        canonical = lib._canonical_doi(doi)
        if canonical in existing_dois:
            duplicates.append((p, canonical))
        else:
            to_import.append(p)
    
    # Report
    print(f"\n=== Analysis ===")
    print(f"  New papers to import: {len(to_import)}")
    print(f"  Duplicates (skipped): {len(duplicates)}")
    print(f"  Without DOI (need manual): {len(no_id)}")
    
    if duplicates:
        print(f"\n--- Duplicates (already in library) ---")
        for p, canonical in duplicates[:5]:
            existing = lib.by_doi(canonical)
            print(f"  SKIP: {p['filename']}")
            print(f"        Already exists as: {existing.tool if existing else 'unknown'} ({canonical})")
        if len(duplicates) > 5:
            print(f"        ... and {len(duplicates)-5} more")
    
    if no_id:
        print(f"\n--- Items without identifiable DOI ---")
        for p in no_id[:5]:
            print(f"  MANUAL: {p['filename']} - need DOI metadata")
        if len(no_id) > 5:
            print(f"          ... and {len(no_id)-5} more")
    
    if to_import:
        print(f"\n--- Ready to import ---")
        for p in to_import:
            print(f"  IMPORT: {p['filename']}")
            print(f"          DOI: {p['doi']}")
    
    if args.dry_run:
        print(f"\n[DRY RUN] No changes made. Remove --dry-run to execute.")
        return
    
    if not to_import:
        print(f"\nNo new papers to import.")
        return
    
    # Execute import
    target_dir = args.output_dir / args.category
    target_dir.mkdir(parents=True, exist_ok=True)
    
    imported = 0
    for p in to_import:
        slug = p["doi_slug"]
        item_path = Path(p["path"])
        dest_dir = target_dir / slug
        
        if p["type"] == "pdf":
            # Create directory, copy PDF
            dest_dir.mkdir(exist_ok=True)
            shutil.copy2(item_path, dest_dir / "paper.pdf")
            # Create placeholder SKILL.md
            skill_md = f"""# {p['doi']}

## Source
- DOI: {p['doi']}
- Imported from: {p['filename']}
- Date: 2026-05-01

## Method
(TODO: Extract method summary from PDF or abstract)

## Commands / Code Snippets
(TODO: Add code snippets if applicable)

## Notes for R-analysis agent
(TODO: Add agent guidance)
"""
            (dest_dir / "SKILL.md").write_text(skill_md)
            
        elif p["type"] == "directory":
            # Copy entire directory
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(item_path, dest_dir)
        
        imported += 1
        print(f"  Created: {dest_dir}")
    
    print(f"\n✓ Imported {imported} paper(s) to {target_dir}")
    print(f"\nNext steps:")
    print(f"  1. Edit imported SKILL.md files to add method summaries")
    print(f"  2. Run: python paperskills/library/scripts/rebuild_index.py")
    print(f"  3. Commit changes to git")


if __name__ == "__main__":
    main()
