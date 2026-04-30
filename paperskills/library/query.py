#!/usr/bin/env python3
"""CLI for querying Paper Skills Library.

Usage:
    python paperskills/library/query.py --doi "10.1186/s13059-014-0550-8"
    python paperskills/library/query.py --tool "DESeq2"
    python paperskills/library/query.py --family "rna"
    python paperskills/library/query.py --task "deseq2_lrt_interaction"
    python paperskills/library/query.py --search "shrinkage estimation"
    python paperskills/library/query.py --list-families
    python paperskills/library/query.py --list-tools
"""

import argparse
import json
from pathlib import Path

from indices.library_index import LibraryIndex


def main():
    ap = argparse.ArgumentParser(description="Query Paper Skills Library")
    ap.add_argument("--doi", help="Lookup by DOI (canonical or slug)")
    ap.add_argument("--tool", help="Lookup by tool name")
    ap.add_argument("--family", help="Lookup by technical family (rna, chip, methyl...)")
    ap.add_argument("--task", help="Lookup papers recommended for task_id")
    ap.add_argument("--search", help="Full-text search in SKILL.md content")
    ap.add_argument("--list-families", action="store_true", help="List all families")
    ap.add_argument("--list-tools", action="store_true", help="List all tools")
    ap.add_argument("--json", action="store_true", help="Output as JSON")
    ap.add_argument("--limit", type=int, default=10, help="Limit for search results")
    args = ap.parse_args()

    lib = LibraryIndex().load()

    if args.list_families:
        families = lib.all_families()
        if args.json:
            print(json.dumps({"families": families}, indent=2))
        else:
            print("Available families:")
            for f in families:
                print(f"  - {f}")
        return

    if args.list_tools:
        tools = lib.all_tools()
        if args.json:
            print(json.dumps({"tools": tools}, indent=2))
        else:
            print("Available tools:")
            for t in tools:
                print(f"  - {t}")
        return

    results = []
    if args.doi:
        entry = lib.by_doi(args.doi)
        if entry:
            results.append(entry.to_dict())
        else:
            print(f"No entry found for DOI: {args.doi}")
            return

    elif args.tool:
        entries = lib.by_tool(args.tool, fuzzy=True)
        results = [e.to_dict() for e in entries]

    elif args.family:
        entries = lib.by_family(args.family)
        results = [e.to_dict() for e in entries]

    elif args.task:
        entries = lib.recommended_for_task(args.task)
        results = [e.to_dict() for e in entries]

    elif args.search:
        scored = lib.search(args.search, limit=args.limit)
        results = [{"entry": e.to_dict(), "score": s} for e, s in scored]

    else:
        ap.print_help()
        return

    if args.json:
        print(json.dumps({"results": results}, indent=2, ensure_ascii=False))
    else:
        if not results:
            print("No results found.")
            return
        print(f"\nFound {len(results)} result(s):\n")
        for i, r in enumerate(results, 1):
            if "entry" in r:
                r = r["entry"]  # unwrap search result
            print(f"[{i}] {r.get('tool', 'Unknown')} | {r.get('family', 'unknown')}")
            print(f"    DOI: {r.get('doi', 'N/A')}")
            print(f"    Title: {r.get('title', 'N/A')}")
            print(f"    Year: {r.get('year', 'N/A')}")
            if r.get('tasks_recommended'):
                print(f"    Tasks: {', '.join(r['tasks_recommended'])}")
            print(f"    Path: {r.get('skill_md_path', 'N/A')}")
            print()


if __name__ == "__main__":
    main()
