#!/usr/bin/env python3
"""Resolve DOIs via Unpaywall and download open-access PDFs when available."""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_LIT = Path(__file__).resolve().parents[1]
_MAP = _LIT / "workflow_literature_map.json"
_PDF = _LIT / "pdfs"
_UNPAYWALL = "https://api.unpaywall.org/v2"


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


_SSL_CTX = _ssl_context()


def _doi_to_filename(doi: str) -> str:
    return re.sub(r"[^\w.+-]+", "_", doi) + ".pdf"


def fetch_unpaywall(doi: str, email: str) -> dict:
    url = f"{_UNPAYWALL}/{urllib.parse.quote(doi)}?email={urllib.parse.quote(email)}"
    req = urllib.request.Request(url, headers={"User-Agent": f"Paper2Skills/1.0 (mailto:{email})"})
    with urllib.request.urlopen(req, timeout=60, context=_SSL_CTX) as r:
        return json.loads(r.read().decode())


def _download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Paper2Skills/1.0"})
    with urllib.request.urlopen(req, timeout=120, context=_SSL_CTX) as r, dest.open("wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)


def main() -> None:
    p = argparse.ArgumentParser(description="Download OA PDFs for DOIs in workflow_literature_map.json")
    p.add_argument("--all", action="store_true", help="All unique DOIs in the map")
    p.add_argument("--workflow-id", action="append", help="Restrict to one workflow_id (repeatable)")
    p.add_argument(
        "--metadata-only",
        action="store_true",
        help="Print OA status and URLs only; do not download PDFs",
    )
    p.add_argument(
        "--email",
        default=os.environ.get("UNPAYWALL_EMAIL"),
        help="Email for Unpaywall (or set UNPAYWALL_EMAIL)",
    )
    args = p.parse_args()

    data = json.loads(_MAP.read_text(encoding="utf-8"))
    workflows = data.get("workflows", [])
    if args.workflow_id:
        allow = set(args.workflow_id)
        workflows = [w for w in workflows if w.get("workflow_id") in allow]

    dois: set[str] = set()
    for w in workflows:
        for c in w.get("citations", []):
            d = c.get("doi")
            if d:
                dois.add(d)

    email = args.email
    if not email and not args.metadata_only:
        print("ERROR: set --email or UNPAYWALL_EMAIL for Unpaywall API.", file=sys.stderr)
        sys.exit(1)

    _PDF.mkdir(parents=True, exist_ok=True)
    ok_dl = 0
    missing = 0
    for doi in sorted(dois):
        if args.metadata_only:
            print(doi, "(metadata-only; skipping API)")
            continue
        assert email
        try:
            info = fetch_unpaywall(doi, email)
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, doi, file=sys.stderr)
            time.sleep(1.0)
            continue
        except Exception as e:
            print("ERROR", doi, e, file=sys.stderr)
            continue

        best = info.get("best_oa_location") or {}
        pdf_url = best.get("url_for_pdf") or (info.get("oa_locations") or [{}])[0].get("url_for_pdf")
        title = info.get("title", "")
        is_oa = info.get("is_oa", False)
        print(f"{doi} | is_oa={is_oa} | {title[:60]}...")
        if not pdf_url:
            print("  no PDF URL in Unpaywall")
            missing += 1
            time.sleep(0.35)
            continue
        out = _PDF / _doi_to_filename(doi)
        if out.is_file() and out.stat().st_size > 1000:
            print("  exists:", out)
            ok_dl += 1
            continue
        try:
            _download(pdf_url, out)
            print("  ->", out)
            ok_dl += 1
        except Exception as e:
            print("  download failed:", e, file=sys.stderr)
            missing += 1
        time.sleep(0.35)

    if not args.metadata_only:
        print(f"Done. Downloaded or cached: {ok_dl}; no PDF URL or failed: {missing}")


if __name__ == "__main__":
    main()
