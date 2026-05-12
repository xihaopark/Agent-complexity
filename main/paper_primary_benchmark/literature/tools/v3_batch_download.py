#!/usr/bin/env python3
"""Batch DOI downloader for V3 paper coverage expansion.

For each target DOI:
- query Unpaywall
- try best_oa_location.url_for_pdf, then iterate all oa_locations
- if Unpaywall has a bioRxiv preprint host (host_type=repository, url contains biorxiv), prefer it if the primary fails
- skip files that already exist with size > 1000 bytes (idempotent)
- write a per-DOI log line to literature/_v3_download_log.json
"""

from __future__ import annotations

import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import certifi

_LIT = Path(__file__).resolve().parents[1]
_PDF = _LIT / "pdfs"
_LOG = _LIT / "_v3_download_log.json"
_UNPAYWALL = "https://api.unpaywall.org/v2"
EMAIL = "paper2skills@protonmail.com"

_SSL_CTX = ssl.create_default_context(cafile=certifi.where())


def _doi_safe(doi: str) -> str:
    return re.sub(r"[^\w.+-]+", "_", doi)


def _fetch_unpaywall(doi: str) -> dict:
    url = f"{_UNPAYWALL}/{urllib.parse.quote(doi)}?email={urllib.parse.quote(EMAIL)}"
    req = urllib.request.Request(url, headers={"User-Agent": f"Paper2Skills/1.0 (mailto:{EMAIL})"})
    with urllib.request.urlopen(req, timeout=60, context=_SSL_CTX) as r:
        return json.loads(r.read().decode())


def _download(url: str, dest: Path) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/pdf,text/html;q=0.2,*/*;q=0.1",
        },
    )
    tmp = dest.with_suffix(".part")
    with urllib.request.urlopen(req, timeout=120, context=_SSL_CTX) as r, tmp.open("wb") as f:
        n = 0
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)
            n += len(chunk)
    head = tmp.open("rb").read(8)
    if not head.startswith(b"%PDF"):
        tmp.unlink(missing_ok=True)
        return (n, "not-a-pdf")
    tmp.rename(dest)
    return (n, "pdf")


def _iter_pdf_urls(info: dict) -> list[dict]:
    out = []
    best = info.get("best_oa_location") or {}
    if best.get("url_for_pdf"):
        out.append({"url": best["url_for_pdf"], "host_type": best.get("host_type"), "source": "best_oa"})
    for loc in info.get("oa_locations") or []:
        u = loc.get("url_for_pdf")
        if not u:
            continue
        entry = {"url": u, "host_type": loc.get("host_type"), "source": "oa_locations"}
        if entry not in out:
            out.append(entry)
    return out


def _europepmc_lookup(doi: str) -> list[dict]:
    """Return PDF URL candidates derived from Europe PMC for a DOI."""
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
        f"query=DOI:{urllib.parse.quote(doi)}&format=json&resultType=core"
    )
    out: list[dict] = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Paper2Skills/1.0"})
        with urllib.request.urlopen(req, timeout=45, context=_SSL_CTX) as r:
            data = json.loads(r.read().decode())
    except Exception:
        return out
    hits = (data.get("resultList") or {}).get("result") or []
    for h in hits:
        pmcid = h.get("pmcid")
        ftul = (h.get("fullTextUrlList") or {}).get("fullTextUrl") or []
        for ft in ftul:
            if (ft.get("documentStyle") or "").lower() == "pdf" and ft.get("availability", "").lower() != "subscription":
                out.append(
                    {"url": ft.get("url"), "host_type": "europepmc-ftul", "source": "europepmc-ftul"}
                )
        if pmcid:
            out.append(
                {
                    "url": f"https://europepmc.org/articles/{pmcid}?pdf=render",
                    "host_type": "europepmc",
                    "source": "europepmc-articles",
                }
            )
        break
    return [o for o in out if o.get("url")]


def attempt(doi: str) -> dict:
    safe = _doi_safe(doi)
    out_pdf = _PDF / (safe + ".pdf")
    rec: dict = {"doi": doi, "doi_safe": safe, "already_present": False, "attempts": [], "final": None}
    if out_pdf.is_file() and out_pdf.stat().st_size > 1000:
        rec["already_present"] = True
        rec["final"] = {"ok": True, "size": out_pdf.stat().st_size, "reason": "cached"}
        return rec

    try:
        info = _fetch_unpaywall(doi)
    except urllib.error.HTTPError as e:
        rec["final"] = {"ok": False, "reason": f"unpaywall HTTP {e.code}"}
        return rec
    except Exception as e:
        rec["final"] = {"ok": False, "reason": f"unpaywall error {e}"}
        return rec

    rec["is_oa"] = info.get("is_oa", False)
    rec["title"] = (info.get("title") or "")[:120]
    urls = _iter_pdf_urls(info)
    urls.extend(_europepmc_lookup(doi))
    seen = set()
    deduped = []
    for u in urls:
        if u["url"] in seen:
            continue
        seen.add(u["url"])
        deduped.append(u)
    urls = deduped
    if not urls:
        rec["final"] = {"ok": False, "reason": "no OA PDF URL in Unpaywall or Europe PMC"}
        return rec

    tried = 0
    for cand in urls:
        if tried >= 6:
            break
        tried += 1
        try:
            n, kind = _download(cand["url"], out_pdf)
            if kind != "pdf":
                rec["attempts"].append({"url": cand["url"], "ok": False, "reason": f"{kind} ({n})"})
                continue
            if n < 10000:
                out_pdf.unlink(missing_ok=True)
                rec["attempts"].append({"url": cand["url"], "ok": False, "reason": f"too small ({n})"})
                continue
            rec["attempts"].append({"url": cand["url"], "ok": True, "size": n, "host_type": cand["host_type"]})
            rec["final"] = {"ok": True, "size": n, "host_type": cand["host_type"]}
            return rec
        except urllib.error.HTTPError as e:
            rec["attempts"].append({"url": cand["url"], "ok": False, "reason": f"HTTP {e.code}"})
        except Exception as e:
            rec["attempts"].append({"url": cand["url"], "ok": False, "reason": str(e)[:120]})
        time.sleep(0.3)

    rec["final"] = {"ok": False, "reason": "all OA URLs failed"}
    return rec


def main() -> None:
    dois = sys.argv[1:]
    if not dois:
        print("Usage: v3_batch_download.py DOI1 DOI2 ...", file=sys.stderr)
        sys.exit(1)

    _PDF.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    ok = 0
    for d in dois:
        rec = attempt(d)
        records.append(rec)
        tag = "OK" if (rec.get("final") or {}).get("ok") else "FAIL"
        reason = (rec.get("final") or {}).get("reason", "")
        print(f"[{tag}] {d} -- {reason}")
        if (rec.get("final") or {}).get("ok"):
            ok += 1
        time.sleep(0.4)

    prior: list = []
    if _LOG.is_file():
        try:
            prior = json.loads(_LOG.read_text(encoding="utf-8"))
        except Exception:
            prior = []
    prior.extend(records)
    _LOG.write_text(json.dumps(prior, indent=2), encoding="utf-8")
    print(f"\nTotal attempts: {len(records)}; successful: {ok}; log: {_LOG}")


if __name__ == "__main__":
    main()
