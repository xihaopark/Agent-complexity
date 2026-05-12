#!/usr/bin/env python3
"""Summarize CPL-Article BRAT corpus layout (Paper2Skills supplementary context).

Expects ``literature/cpl_corpus/CPL-Article.zip`` or ``--zip PATH``.
Unzips to ``literature/cpl_corpus/_extract/CPL-Article`` by default (see cpl_corpus/.gitignore).
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

_PMID = re.compile(r"^PMID\d+")


def _default_zip() -> Path:
    return Path(__file__).resolve().parents[1] / "cpl_corpus" / "CPL-Article.zip"


def _default_extract_root() -> Path:
    return Path(__file__).resolve().parents[1] / "cpl_corpus" / "_extract"


def ensure_extracted(zip_path: Path, extract_root: Path) -> Path:
    target = extract_root / "CPL-Article"
    if target.is_dir() and any(target.iterdir()):
        return target
    extract_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_root)
    return target


def inventory(corpus_root: Path) -> dict:
    txts = [p for p in corpus_root.rglob("*.txt") if p.name.startswith("PMID")]
    anns = [p for p in corpus_root.rglob("*.ann") if p.name.startswith("PMID")]
    pmids: set[str] = set()
    for p in txts:
        m = _PMID.match(p.name)
        if m:
            pmids.add(m.group(0))

    by_split: dict[str, dict[str, int]] = defaultdict(lambda: {"txt": 0, "ann": 0})
    for p in txts:
        rel = p.relative_to(corpus_root)
        if len(rel.parts) >= 3 and rel.parts[0].startswith("iteration_"):
            key = f"{rel.parts[0]}/{rel.parts[1]}"
            by_split[key]["txt"] += 1
    for p in anns:
        rel = p.relative_to(corpus_root)
        if len(rel.parts) >= 3 and rel.parts[0].startswith("iteration_"):
            key = f"{rel.parts[0]}/{rel.parts[1]}"
            by_split[key]["ann"] += 1

    return {
        "corpus_root": str(corpus_root),
        "unique_pmids": len(pmids),
        "txt_files": len(txts),
        "ann_files": len(anns),
        "splits": dict(sorted(by_split.items())),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", type=Path, default=None, help="Path to CPL-Article.zip")
    ap.add_argument(
        "--extract-root",
        type=Path,
        default=None,
        help="Directory where CPL-Article/ will be extracted",
    )
    ap.add_argument("--json", action="store_true", help="Print machine-readable JSON only")
    args = ap.parse_args()

    zip_path = args.zip or _default_zip()
    extract_root = args.extract_root or _default_extract_root()

    if not zip_path.is_file():
        raise SystemExit(
            f"Missing zip: {zip_path}\n"
            "  Copy CPL-Article.zip into literature/cpl_corpus/ (e.g. from a teammate's Downloads), or run:\n"
            "  curl -fsSL -o literature/cpl_corpus/CPL-Article.zip "
            "'https://zenodo.org/records/18526700/files/CPL-Article.zip?download=1'\n"
            "  (from repo root, adjust path if needed.)"
        )

    root = ensure_extracted(zip_path, extract_root)
    data = inventory(root)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("CPL-Article inventory")
        print("===================")
        print(f"  corpus_root    : {data['corpus_root']}")
        print(f"  unique_pmids   : {data['unique_pmids']}")
        print(f"  .txt files     : {data['txt_files']}")
        print(f"  .ann files     : {data['ann_files']}")
        print("  splits (train/val per iteration):")
        for k, v in data["splits"].items():
            print(f"    {k}: txt={v['txt']} ann={v['ann']}")


if __name__ == "__main__":
    main()
