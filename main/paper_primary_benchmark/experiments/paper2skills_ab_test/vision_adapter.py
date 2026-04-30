#!/usr/bin/env python3
"""OpenRouter-backed vision adapter for Paper2Skills.

Simplified stand-in for ``external/Paper2Skills/run_skill_creator.py``: renders
PDF pages as images with PyMuPDF, sends them to an OpenRouter vision model in a
single multi-image chat completion, and writes a SKILL.md whose sections mirror
what the full LangGraph pipeline aims to produce (Method / Parameters /
Commands / Notes). No git branch / Python-module / test generation — that is
explicitly what the full Paper2Skills tool adds on top.

Usage::

    python vision_adapter.py --pdf path/to.pdf \\
        --out-dir experiments/paper2skills_ab_test/vision_out/<doi-safe> \\
        [--pages 8] [--dpi 130] [--model openrouter/openai/gpt-4o]
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
from pathlib import Path

import fitz  # PyMuPDF
from openai import OpenAI


SYSTEM_PROMPT = """You are Paper2Skill. Read the provided scientific paper \
pages (as images) and distil them into a SKILL.md that another LLM agent will \
consume when asked to run the paper's analysis in R. Focus on the Methods / \
Algorithm / Implementation sections. Keep claims grounded in what the images \
actually show; if a detail is not visible, say so instead of inventing it.

Respond with ONLY markdown using EXACTLY these sections and headings:

## Method
1-3 paragraphs describing the statistical / computational method, including \
the core model / algorithm and any mathematical assumptions a user must know.

## Parameters
Bulleted list of the tunable parameters or arguments (name, default if known, \
meaning). Include defaults only if the paper states them.

## Commands / Code Snippets
Any code the paper shows — R, shell, Python — copied verbatim inside fenced \
code blocks with the correct language tag. If none are visible on the \
provided pages, write `(No code snippets visible on provided pages.)`.

## Notes for R-analysis agent
Pragmatic bullets: which R package / function implements the method, key \
pitfalls, required input shape, and anything the agent should double-check \
before reporting results.
"""


def render_pages(pdf_path: Path, n_pages: int, dpi: int) -> list[bytes]:
    doc = fitz.open(pdf_path)
    pages: list[bytes] = []
    max_i = min(len(doc), n_pages)
    mat = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    for i in range(max_i):
        pix = doc[i].get_pixmap(matrix=mat, alpha=False)
        pages.append(pix.tobytes("png"))
    doc.close()
    return pages


def build_messages(pdf_name: str, page_pngs: list[bytes]) -> list[dict]:
    content: list[dict] = [
        {
            "type": "text",
            "text": (
                f"Paper file: {pdf_name}\n"
                f"Pages attached: {len(page_pngs)} (rendered from the start "
                "of the PDF). Extract the requested sections."
            ),
        }
    ]
    for png in page_pngs:
        b64 = base64.b64encode(png).decode("ascii")
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{b64}",
                    "detail": "high",
                },
            }
        )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]


def call_openrouter(messages: list[dict], model: str, api_key: str) -> dict:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/paper2skills-ab-test",
            "X-Title": "Paper2Skills A/B adapter",
        },
    )
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=2500,
    )
    usage = getattr(resp, "usage", None)
    return {
        "text": resp.choices[0].message.content or "",
        "usage": {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
            "completion_tokens": (
                getattr(usage, "completion_tokens", 0) if usage else 0
            ),
            "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
        },
        "model": getattr(resp, "model", model),
    }


def load_openrouter_key(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env:
        return env
    key_file = Path(__file__).resolve().parents[4] / "openrouterkey.txt"
    if key_file.is_file():
        for line in key_file.read_text().splitlines():
            line = line.strip()
            if line:
                return line
    raise SystemExit(
        "No OpenRouter key found (env OPENROUTER_API_KEY, --api-key, or "
        f"{key_file})."
    )


def main() -> None:
    p = argparse.ArgumentParser(description="OpenRouter vision adapter")
    p.add_argument("--pdf", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--pages", type=int, default=8)
    p.add_argument("--dpi", type=int, default=130)
    p.add_argument(
        "--model",
        default="openrouter/openai/gpt-4o",
        help="OpenRouter model id; vision-capable model required.",
    )
    p.add_argument("--api-key", default=None)
    args = p.parse_args()

    if not args.pdf.is_file():
        print(f"ERROR: PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    api_key = load_openrouter_key(args.api_key)

    # OpenRouter's OpenAI-compat endpoint wants "openai/gpt-4o" style; strip
    # the optional ``openrouter/`` prefix if present.
    model = args.model
    if model.startswith("openrouter/"):
        model = model.split("openrouter/", 1)[1]

    t0 = time.time()
    pngs = render_pages(args.pdf, args.pages, args.dpi)
    t_render = time.time() - t0

    messages = build_messages(args.pdf.name, pngs)

    t1 = time.time()
    result = call_openrouter(messages, model=model, api_key=api_key)
    t_llm = time.time() - t1

    body = result["text"].strip() or "(Empty response from model.)"
    doi_safe = args.pdf.stem
    skill_name = "paper-" + doi_safe.replace(".", "-").replace("_", "-")
    frontmatter = (
        f"---\n"
        f"name: {skill_name}\n"
        f"description: >-\n"
        f"  Vision-adapter skill extracted from {args.pdf.name} via "
        f"{model}\n"
        f"source_pdf: {args.pdf.name}\n"
        f"pages_processed: {len(pngs)}\n"
        f"generator: paper2skills_ab_test/vision_adapter.py\n"
        f"---\n\n"
    )
    skill_md = frontmatter + body + "\n"
    (args.out_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    manifest = {
        "pdf": str(args.pdf),
        "out_dir": str(args.out_dir),
        "pages_processed": len(pngs),
        "dpi": args.dpi,
        "model": model,
        "render_seconds": round(t_render, 2),
        "llm_seconds": round(t_llm, 2),
        "total_seconds": round(time.time() - t0, 2),
        "usage": result["usage"],
    }
    (args.out_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
