#!/usr/bin/env python3
"""
Build real R-centric tasks from workflow_candidates source code (V2).

This version enforces two new rules from COORDINATION_PLAN_V2:
  1. Every task comes from a paper-covered pipeline (i.e. the workflow_id
     appears in experiments/skills/manifest.json::by_workflow_id).
  2. Every task produces data-only deliverables (CSV/TSV/TXT/JSON). Tasks
     whose source script also writes a figure (svg/pdf/png) are rebuilt
     with the image calls stripped from a temp copy of the script. Pure
     image-only tasks are dropped.

For snakemake@-style scripts (which cannot be executed standalone),
`_cmd_*` emits a tiny wrapper R script that:
  - defines an S4 SnakemakeMock class with slots input/output/params/
    wildcards/config/threads/log/scriptdir,
  - instantiates `snakemake` with the task-specific values,
  - optionally pre-computes upstream artifacts (e.g. running methRead +
    unite to synthesize a methylBase object),
  - `source()`s the patched copy of the original script.

All ground-truth outputs are produced by actually running the real
source code; nothing is fabricated.

Run:
  python3 tools/build_real_r_tasks.py --all --force
  python3 tools/build_real_r_tasks.py --task star_deseq2_init
  python3 tools/build_real_r_tasks.py --list
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

_HERE = Path(__file__).resolve().parent
_LDP = _HERE.parent
_PB = _LDP.parent
_MAIN = _PB.parent
_REPO = _MAIN.parent
_WFC = _MAIN / "finish" / "workflow_candidates"
_REAL_ROOT = _LDP / "tasks" / "real"
_GT_ROOT = _LDP / "tasks" / "real_ground_truth"


# --------------------------------------------------------------------------- #
# TaskSpec                                                                    #
# --------------------------------------------------------------------------- #


@dataclass
class TaskSpec:
    task_id: str
    workflow_id: str
    family: str
    stage: str
    difficulty: int
    r_script_src: Path
    description: str
    analyst_objective: str
    generate_inputs: Callable[[Path, random.Random], None]
    run_cmd: Callable[[Path, Path], list[str]]
    success_glob: str
    eval_files: list[str]
    wrapper_kind: str = "commandArgs"  # "commandArgs" | "snakemake"
    paper_covered: bool = True
    # Optional hook to edit the copied reference script before execution
    # (e.g. strip svg/ggsave calls). Receives the path of the copy.
    patch_source: Optional[Callable[[Path], None]] = None


# --------------------------------------------------------------------------- #
# akinyi_deseq2 (commandArgs, data-only, paper-covered) — kept from V1        #
# --------------------------------------------------------------------------- #


def _gen_akinyi_deseq2(workdir: Path, rng: random.Random) -> None:
    """Generate a featureCounts-style input for DESeq2 DE analysis."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    n_genes = 600
    n_ercc = 30
    sample_names = [f"sample_{i}" for i in range(6)]
    header = [
        "Geneid", "Chr", "Start", "End", "Strand", "Length", *sample_names,
    ]
    lines = ["\t".join(header)]
    for g in range(n_genes):
        gid = f"GENE_{g:04d}"
        base = rng.randint(50, 2000)
        row_counts = []
        de_up = (g % 30 == 0)
        de_down = (g % 47 == 0)
        for i, _ in enumerate(sample_names):
            cond_b = i >= 3
            if cond_b and de_up:
                c = int(base * rng.uniform(5, 9))
            elif cond_b and de_down:
                c = int(base * rng.uniform(0.05, 0.2))
            else:
                c = int(base * rng.uniform(0.85, 1.15))
            row_counts.append(str(max(c, 0)))
        lines.append(
            "\t".join([gid, "chr1", str(1000 + g), str(1500 + g), "+", "500", *row_counts])
        )
    for k in range(n_ercc):
        gid = f"ERCC-{k:04d}"
        row_counts = [str(rng.randint(10, 100)) for _ in sample_names]
        lines.append(
            "\t".join([gid, "chr_ERCC", "1", "100", "+", "100", *row_counts])
        )
    (inp / "featureCounts_output.txt").write_text("\n".join(lines) + "\n")


def _cmd_akinyi(workdir: Path, gtdir: Path) -> list[str]:
    return [
        "Rscript",
        str(gtdir / "reference" / "script.R"),
        str(workdir / "input" / "featureCounts_output.txt"),
        str(gtdir / "reference_output" / "deseq2_up.txt"),
        str(gtdir / "reference_output" / "deseq2_down.txt"),
    ]


# --------------------------------------------------------------------------- #
# Snakemake wrapper helper                                                    #
# --------------------------------------------------------------------------- #


class _RVec:
    """Marker wrapper telling `_r_quote` to emit ``c(...)`` instead of ``list(...)``.

    Use this for params that Snakemake normally passes as an R character vector
    (e.g. ``desired_cols``, ``unwanted_categorical``).
    """

    __slots__ = ("items",)

    def __init__(self, items):
        self.items = list(items)


def _r_quote(value) -> str:
    """Render a Python value as an R literal.

    Supports: str, bool, int, float, None, list, tuple, dict, `_RVec` (nested).
    """
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, _RVec):
        if not value.items:
            return "character(0)"
        body = ", ".join(_r_quote(v) for v in value.items)
        return f"c({body})"
    if isinstance(value, (list, tuple)):
        body = ", ".join(_r_quote(v) for v in value)
        return f"list({body})"
    if isinstance(value, dict):
        parts = []
        for k, v in value.items():
            parts.append(f'`{k}` = {_r_quote(v)}')
        return f"list({', '.join(parts)})"
    raise TypeError(f"Unsupported R-literal type: {type(value)}")


_SNAKEMAKE_MOCK_PREAMBLE = r"""
# --- SnakemakeMock preamble ---------------------------------------------------
# Minimal S4 stand-in for Snakemake's `snakemake` object so we can `source()`
# a Snakemake-authored R script outside any Snakemake context.
suppressPackageStartupMessages({
  if (!isClass("SnakemakeMock")) {
    setClass(
      "SnakemakeMock",
      representation(
        input = "list", output = "list", params = "list",
        wildcards = "list", config = "list", threads = "numeric",
        log = "list", scriptdir = "character", rule = "character",
        resources = "list"
      ),
      prototype(
        input = list(), output = list(), params = list(),
        wildcards = list(), config = list(), threads = 1,
        log = list(), scriptdir = ".", rule = "mock_rule",
        resources = list()
      )
    )
  }
})
"""


def _emit_snakemake_wrapper(
    wrapper_path: Path,
    *,
    script_to_source: Path,
    inputs: dict,
    outputs: dict,
    params: dict,
    config: dict,
    wildcards: dict,
    threads: int,
    log_path: str,
    scriptdir: str,
    pre_source_r: str = "",
    post_source_r: str = "",
) -> None:
    """Write an R wrapper that fakes the snakemake object and sources the script.

    `pre_source_r` is injected between the snakemake object creation and the
    source() call (useful for function-stubbing like `svg <- function(...) NULL`
    or for creating upstream input artifacts in-process).
    """
    lines: list[str] = []
    lines.append(_SNAKEMAKE_MOCK_PREAMBLE)
    lines.append(f'SCRIPT_TO_SOURCE <- {_r_quote(str(script_to_source))}')
    lines.append(f'LOG_PATH <- {_r_quote(log_path)}')
    lines.append(
        "snakemake <- new(\n"
        "  \"SnakemakeMock\",\n"
        f"  input = {_r_quote(inputs)},\n"
        f"  output = {_r_quote(outputs)},\n"
        f"  params = {_r_quote(params)},\n"
        f"  wildcards = {_r_quote(wildcards)},\n"
        f"  config = {_r_quote(config)},\n"
        f"  threads = {threads},\n"
        "  log = list(LOG_PATH),\n"
        f"  scriptdir = {_r_quote(scriptdir)}\n"
        ")\n"
    )
    if pre_source_r:
        lines.append("# --- pre-source hook --------------------------------------------------------")
        lines.append(pre_source_r)
    lines.append("# --- source original script ------------------------------------------------")
    lines.append("source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)")
    if post_source_r:
        lines.append("# --- post-source hook -------------------------------------------------------")
        lines.append(post_source_r)
    wrapper_path.write_text("\n".join(lines) + "\n")


# --------------------------------------------------------------------------- #
# rna-seq-star-deseq2-finish — deseq2-init.R                                  #
# --------------------------------------------------------------------------- #


_STAR_SAMPLES = [
    ("A1", "treated"),
    ("A2", "treated"),
    ("A3", "treated"),
    ("B1", "untreated"),
    ("B2", "untreated"),
    ("B3", "untreated"),
]


def _star_deseq2_write_counts_and_samples(workdir: Path, rng: random.Random) -> None:
    """Shared helper: generate counts TSV + samples TSV for star-deseq2 tasks."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    n_genes = 500
    sample_names = [s[0] for s in _STAR_SAMPLES]
    header = ["gene", *sample_names]
    lines = ["\t".join(header)]
    for g in range(n_genes):
        gid = f"ENSG{g:08d}"
        base = rng.randint(80, 2400)
        row = []
        de_up = g % 25 == 0
        de_down = g % 41 == 0
        for name, cond in _STAR_SAMPLES:
            treated = cond == "treated"
            if treated and de_up:
                c = int(base * rng.uniform(4.0, 7.0))
            elif treated and de_down:
                c = int(base * rng.uniform(0.07, 0.25))
            else:
                c = int(base * rng.uniform(0.9, 1.1))
            row.append(str(max(c, 0)))
        lines.append("\t".join([gid, *row]))
    (inp / "counts.tsv").write_text("\n".join(lines) + "\n")

    sam_lines = ["sample_name\tcondition"]
    for name, cond in _STAR_SAMPLES:
        sam_lines.append(f"{name}\t{cond}")
    (inp / "samples.tsv").write_text("\n".join(sam_lines) + "\n")


def _gen_star_deseq2_init(workdir: Path, rng: random.Random) -> None:
    _star_deseq2_write_counts_and_samples(workdir, rng)


def _cmd_star_deseq2_init(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    counts_path = workdir / "input" / "counts.tsv"
    samples_path = workdir / "input" / "samples.tsv"
    out_rds = gtdir / "reference_output" / "dds.rds"
    out_tsv = gtdir / "reference_output" / "normalized_counts.tsv"
    log_path = gtdir / "reference" / "run.R.log"

    config = {
        "samples": str(samples_path),
        "diffexp": {
            "variables_of_interest": {
                "condition": {"base_level": "untreated"},
            },
            "batch_effects": [""],
            "model": "~condition",
        },
    }

    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"counts": str(counts_path)},
        outputs=[str(out_rds), str(out_tsv)],
        params={},
        config=config,
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# rna-seq-star-deseq2-finish — deseq2.R (contrast)                            #
# --------------------------------------------------------------------------- #


def _gen_star_deseq2_contrast(workdir: Path, rng: random.Random) -> None:
    """Generate counts/samples + run deseq2-init to produce dds.rds as input."""
    _star_deseq2_write_counts_and_samples(workdir, rng)
    # Pre-compute dds.rds via a self-contained R pre-step so the task is isolated.
    prep = workdir / "input" / "_prep_dds.R"
    counts_path = workdir / "input" / "counts.tsv"
    samples_path = workdir / "input" / "samples.tsv"
    dds_rds = workdir / "input" / "dds.rds"
    init_script = _WFC / "snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2-init.R"
    log_path = workdir / "input" / "_prep_dds.log"
    _emit_snakemake_wrapper(
        prep,
        script_to_source=init_script,
        inputs={"counts": str(counts_path)},
        outputs=[str(dds_rds), str(workdir / "input" / "_prep_normalized_counts.tsv")],
        params={},
        config={
            "samples": str(samples_path),
            "diffexp": {
                "variables_of_interest": {
                    "condition": {"base_level": "untreated"},
                },
                "batch_effects": [""],
                "model": "~condition",
            },
        },
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(workdir / "input"),
    )
    env = os.environ.copy()
    proc = subprocess.run(
        ["Rscript", str(prep)],
        capture_output=True, text=True, env=env,
    )
    if proc.returncode != 0 or not dds_rds.exists():
        raise RuntimeError(
            "deseq2-init pre-step failed for star_deseq2_contrast:\n"
            + (proc.stderr or "")[-4000:]
        )


def _patch_strip_svg(script_path: Path) -> None:
    """Strip svg/plotMA/dev.off lines from the star-deseq2 deseq2.R copy."""
    text = script_path.read_text()
    text = re.sub(r'^\s*svg\([^)]*\).*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*plotMA\([^\n]*\).*$\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*dev\.off\(\).*$\n?', '', text, flags=re.MULTILINE)
    script_path.write_text(text)


def _cmd_star_deseq2_contrast(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    dds_rds = workdir / "input" / "dds.rds"
    out_tsv = gtdir / "reference_output" / "contrast_results.tsv"
    out_svg = gtdir / "reference_output" / "_ma_plot.svg"  # should NOT be created
    log_path = gtdir / "reference" / "run.R.log"

    config = {
        "diffexp": {
            "contrasts": {
                "treated-vs-untreated": {
                    "variable_of_interest": "condition",
                    "level_of_interest": "treated",
                }
            },
            "variables_of_interest": {
                "condition": {"base_level": "untreated"},
            },
        },
    }
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=[str(dds_rds)],
        outputs={
            "table": str(out_tsv),
            "ma_plot": str(out_svg),
        },
        params={},
        config=config,
        wildcards={"contrast": "treated-vs-untreated"},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# cellranger-multi-finish — create_cellranger_multi_config_csv.R              #
# --------------------------------------------------------------------------- #


def _gen_cellranger_multi_config(workdir: Path, rng: random.Random) -> None:
    """Synthesize a pool sheet + feature reference + dummy fastq paths."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)

    # Pool sheet: one pool, one gene-expression library with 2 lanes.
    pool_lines = [
        "id\tsample\tfeature_types\tlane_number\tphysical_library_id\tsubsample_rate\tchemistry",
        "POOL1\tSAMPLE1\tGene Expression\t1\tPL_GEX\t\tauto",
        "POOL1\tSAMPLE1\tGene Expression\t2\tPL_GEX\t\tauto",
    ]
    (inp / "pool_sheet.tsv").write_text("\n".join(pool_lines) + "\n")

    # Feature reference CSV (required when Antigen Capture present — not used
    # here, but the script's read_csv only runs conditionally, so we just
    # create an empty placeholder).
    (inp / "feature_reference.csv").write_text("id,mhc_allele\n")

    # Create a dummy fastq R1 file under the expected layout so that
    # normalizePath(dirname(filename)) doesn't warn; the script only consumes
    # directory paths, it never opens the fastq.
    fq_dir = workdir / "results" / "input" / "POOL1_Gene_Expression"
    fq_dir.mkdir(parents=True, exist_ok=True)
    for lane in (1, 2):
        fq = fq_dir / f"POOL1_S1_L00{lane}_R1_001.fastq.gz"
        fq.write_bytes(b"")


def _cmd_cellranger_multi_config(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_csv = gtdir / "reference_output" / "multi_config.csv"
    log_path = gtdir / "reference" / "run.R.log"

    pool_sheet = workdir / "input" / "pool_sheet.tsv"
    feature_reference = workdir / "input" / "feature_reference.csv"
    # The original script matches filenames against the regex
    # `^results/input/{pool_id}_{feature_types}/{pool_id}_.+_R1_001.fastq.gz$`
    # so we must hand it Snakemake-style RELATIVE paths. Rscript runs with
    # cwd=workdir, so `results/input/...` resolves correctly.
    fq_dir_rel = Path("results") / "input" / "POOL1_Gene_Expression"
    fq_files = sorted(
        str(fq_dir_rel / p.name)
        for p in (workdir / fq_dir_rel).glob("*_R1_001.fastq.gz")
    )

    config_sections = {
        "gene-expression": {
            "reference": "refdata-gex-GRCh38-2020-A",
            "expect-cells": "8000",
            "create-bam": "true",
        },
        "vdj": {"reference": ""},
        "feature": {"reference": ""},
        "antigen-specificity": {"control_ids": []},
        "multiplexing": {"activate": False},
    }

    # In real Snakemake invocations, `snakemake@input$fq1` is a character
    # vector; our `_r_quote` turns Python lists into R `list()`, so after
    # constructing the mock we coerce fq1 to a flat character vector (this
    # matches the real Snakemake behaviour and keeps `dirname()` happy).
    pre = "snakemake@input$fq1 <- unlist(snakemake@input$fq1, use.names = FALSE)\n"

    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={
            "pool_sheet": str(pool_sheet),
            "fq1": fq_files,
            "feature_reference": str(feature_reference),
            "multiplexing": "",
        },
        outputs={"multi_config_csv": str(out_csv)},
        params={"multi_config_csv_sections": config_sections},
        config={},
        wildcards={"pool_id": "POOL1"},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        pre_source_r=pre,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# fritjoflammers-snakemake-methylanalysis-finish — methylkit_load.R           #
# --------------------------------------------------------------------------- #


def _gen_methylkit_load(workdir: Path, rng: random.Random) -> None:
    """Synthesize per-sample bismark-coverage files."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    sample_names = ["sampleA", "sampleB", "sampleC"]
    n_sites_per_chr = 120
    chroms = ["chr1", "chr2"]
    for s in sample_names:
        lines = []
        for ch in chroms:
            for i in range(n_sites_per_chr):
                cov = rng.randint(5, 50)
                meth_count = rng.randint(0, cov)
                unmeth = cov - meth_count
                meth_pct = 100.0 * meth_count / cov
                pos = 500 + i * 40
                lines.append(f"{ch}\t{pos}\t{pos}\t{meth_pct:.4f}\t{meth_count}\t{unmeth}")
        (inp / f"{s}.bismark.cov").write_text("\n".join(lines) + "\n")


def _patch_strip_methylkit_load_plots(script_path: Path) -> None:
    """Remove the trailing plot_methylkit_histograms calls so the script is
    purely data-producing (writes only the mk_raw RDS)."""
    text = script_path.read_text()
    text = re.sub(
        r'^\s*plot_methylkit_histograms\([^)]*\).*$\n?',
        '',
        text,
        flags=re.MULTILINE,
    )
    script_path.write_text(text)


def _cmd_methylkit_load(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "mk_raw.rds"
    # `output$plots` is referenced by the source only as `dirname(...)`; we
    # give it a portable relative sentinel path (nothing is actually written
    # because the image calls are stripped by `patch_source`).
    plots_sentinel = Path("output") / "_plots" / ".sentinel"
    log_path = gtdir / "reference" / "run.R.log"

    # methylkit_load.R sources `methylkit_common.R` from `snakemake@scriptdir`;
    # point that at the original workflow scripts dir so we don't vendor extra
    # files into the task.
    src_scripts = _WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts"

    # Pass bismark files as RELATIVE paths (Rscript runs with cwd=workdir),
    # which keeps the resulting RDS byte-portable across workdirs.
    bismark_rel = sorted(
        Path("input") / p.name for p in (workdir / "input").glob("*.bismark.cov")
    )
    sample_names = [p.name.replace(".bismark.cov", "") for p in bismark_rel]

    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=[str(p) for p in bismark_rel],
        outputs={
            "rds": str(out_rds),
            "plots": str(plots_sentinel),
        },
        params={
            "samples": sample_names,
            "min_cov": 4,
            "assembly_name": "mock_v1",
            "calling_tool": "bismark",
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(src_scripts),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# fritjoflammers-snakemake-methylanalysis-finish — methylkit_unite.R          #
# --------------------------------------------------------------------------- #


def _gen_methylkit_unite(workdir: Path, rng: random.Random) -> None:
    """Synthesize per-sample bismark-coverage files and a mk_raw.rds input."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)

    sample_names = ["sampleA", "sampleB", "sampleC", "sampleD"]
    n_sites = 400
    chroms = ["chr1", "chr2", "chr3"]
    # Shared positions so unite() can find overlaps across samples.
    positions: list[tuple[str, int]] = []
    for ch in chroms:
        for i in range(n_sites // len(chroms)):
            positions.append((ch, 1000 + i * 50))

    for s in sample_names:
        lines = []
        for ch, pos in positions:
            cov = rng.randint(6, 60)
            meth_count = rng.randint(0, cov)
            unmeth = cov - meth_count
            meth_pct = 100.0 * meth_count / cov
            # bismark coverage columns: chrom, start, end, meth_pct, meth, unmeth (no header)
            lines.append(
                f"{ch}\t{pos}\t{pos}\t{meth_pct:.4f}\t{meth_count}\t{unmeth}"
            )
        (inp / f"{s}.bismark.cov").write_text("\n".join(lines) + "\n")


def _cmd_methylkit_unite(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "mk_united.rds"
    out_tsv = gtdir / "reference_output" / "unite_stats.tsv"
    # NOTE: db_file is declared with a RELATIVE path so the stats TSV's
    # `db_path` cell (which is `dirname(db_file)`) is portable across
    # workdirs. The Rscript cwd is set to the task workdir.
    db_file = Path("output") / "_unite_db.txt.bgz"
    log_path = gtdir / "reference" / "run.R.log"

    bismark_files = sorted(str(p) for p in (workdir / "input").glob("*.bismark.cov"))
    sample_names = [Path(p).name.replace(".bismark.cov", "") for p in bismark_files]

    pre = f"""
suppressPackageStartupMessages({{
  library(methylKit)
}})
# Upstream synthesis: load the per-sample bismark.cov files into a
# methylRawList via methRead, so the downstream unite() script can
# treat its input as a methylRawList exactly as the pipeline does.
mk_raw <- methylKit::methRead(
  location  = as.list({_r_quote(bismark_files)}),
  sample.id = as.list({_r_quote(sample_names)}),
  assembly  = "mock_v1",
  treatment = as.integer(c({",".join("0" if i < 2 else "1" for i in range(len(sample_names)))})),
  header    = FALSE,
  mincov    = 4,
  pipeline  = "bismarkCoverage"
)
mk_raw_rds <- file.path({_r_quote(str(workdir / "input"))}, "mk_raw.rds")
saveRDS(mk_raw, mk_raw_rds)
# Update snakemake@input[[1]] to point to this freshly-saved RDS.
snakemake@input <- list(mk_raw_rds)
"""

    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=["placeholder"],  # overridden in pre
        outputs={
            "rds": str(out_rds),
            "stats_tsv": str(out_tsv),
            "db_file": str(db_file),
        },
        params={
            "min_per_group": 1,
            "destrand": False,
            "use_db": False,
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        pre_source_r=pre,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# fritjoflammers-snakemake-methylanalysis-finish — methylkit2tibble.R         #
# --------------------------------------------------------------------------- #


def _gen_methylkit_to_tibble(workdir: Path, rng: random.Random) -> None:
    """Synthesize bismark files; the wrapper will run methRead+unite in-proc."""
    _gen_methylkit_unite(workdir, rng)


def _cmd_methylkit_to_tibble(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "df_mku.rds"
    out_tsv = gtdir / "reference_output" / "mean_mcpg.tsv"
    log_path = gtdir / "reference" / "run.R.log"

    bismark_files = sorted(str(p) for p in (workdir / "input").glob("*.bismark.cov"))
    sample_names = [Path(p).name.replace(".bismark.cov", "") for p in bismark_files]

    # methylkit2tibble.R assumes `@dbpath` exists on the input methylBase —
    # only methylBaseDB has that slot. So we run unite(..., save.db=TRUE) to
    # get a methylBaseDB and serialise it for the source script.
    db_dir = workdir / "input" / "mk_db"
    pre = f"""
suppressPackageStartupMessages({{
  library(methylKit)
}})
mk_raw <- methylKit::methRead(
  location  = as.list({_r_quote(bismark_files)}),
  sample.id = as.list({_r_quote(sample_names)}),
  assembly  = "mock_v1",
  treatment = as.integer(c({",".join("0" if i < 2 else "1" for i in range(len(sample_names)))})),
  header    = FALSE,
  mincov    = 4,
  pipeline  = "bismarkCoverage",
  dbtype    = "tabix",
  dbdir     = {_r_quote(str(db_dir))}
)
mk_united <- methylKit::unite(
  mk_raw,
  min.per.group = 1L,
  destrand = FALSE,
  save.db = TRUE,
  dbdir = {_r_quote(str(db_dir))},
  suffix = "unite"
)
mk_rds <- file.path({_r_quote(str(workdir / "input"))}, "mk_united.rds")
saveRDS(mk_united, mk_rds)
snakemake@input$rds <- mk_rds
"""

    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"rds": "placeholder"},
        outputs={"rds": str(out_rds), "stats_tsv": str(out_tsv)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        pre_source_r=pre,
    )
    return ["Rscript", str(wrapper_path)]


# =========================================================================== #
# V3 helpers and task specs                                                    #
# =========================================================================== #


def _patch_redirect_devices(script_path: Path) -> None:
    """Universal patch: redirect pdf/png/svg/jpeg/ggsave to tempfiles so scripts
    that mix data writes with image writes can run without touching real image
    outputs. Inserted as a prelude so that subsequent `library(ggplot2)` doesn't
    mask our override (globalenv wins over attached pkgs in R's search path)."""
    stub = r"""# V3 device-redirect prelude (injected) ----------------------------------------
local({
  .orig_pdf  <- grDevices::pdf
  .orig_png  <- grDevices::png
  .orig_svg  <- grDevices::svg
  .orig_jpeg <- grDevices::jpeg
  assign('pdf',  function(file = NA, ...)     .orig_pdf(file = tempfile(fileext = '.pdf'), ...), envir = globalenv())
  assign('png',  function(filename = NA, ...) .orig_png(filename = tempfile(fileext = '.png'), ...), envir = globalenv())
  assign('svg',  function(filename = NA, ...) .orig_svg(filename = tempfile(fileext = '.svg'), ...), envir = globalenv())
  assign('jpeg', function(filename = NA, ...) .orig_jpeg(filename = tempfile(fileext = '.jpg'), ...), envir = globalenv())
  assign('ggsave', function(filename, ...) invisible(NULL), envir = globalenv())
})
# ------------------------------------------------------------------------------

"""
    text = script_path.read_text()
    script_path.write_text(stub + text)


def _patch_strip_methylkit_plotfn(script_path: Path) -> None:
    """For methylkit_filt_norm.R: drop `plot_methylkit_histograms(...)` calls."""
    text = script_path.read_text()
    text = re.sub(
        r'^\s*plot_methylkit_histograms\([^)]*\).*$\n?',
        '',
        text,
        flags=re.MULTILINE,
    )
    script_path.write_text(text)


# --------------------------------------------------------------------------- #
# snakepipes_merge_fc (commandArgs) — RNA                                     #
# --------------------------------------------------------------------------- #


def _gen_snakepipes_merge_fc(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["sampleA", "sampleB", "sampleC", "sampleD"]
    n_genes = 400
    for s in samples:
        lines = ["\t".join(["Geneid", "Chr", "Start", "End", "Strand", "Length", s + ".bam"])]
        for g in range(n_genes):
            gid = f"GENE_{g:05d}"
            c = rng.randint(0, 2000)
            lines.append("\t".join([gid, "chr1", str(1000 + g * 10),
                                    str(1500 + g * 10), "+", "500", str(c)]))
        (inp / f"{s}.counts.txt").write_text("\n".join(lines) + "\n")


def _cmd_snakepipes_merge_fc(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    out = gtdir / "reference_output" / "merged_counts.tsv"
    inputs = sorted(str(p) for p in (workdir / "input").glob("*.counts.txt"))
    return ["Rscript", str(script), str(out), *inputs]


# --------------------------------------------------------------------------- #
# snakepipes_merge_ct (commandArgs) — RNA                                     #
# --------------------------------------------------------------------------- #


def _gen_snakepipes_merge_ct(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["WT_A", "WT_B", "KO_A", "KO_B"]
    n_tx = 300
    for s in samples:
        lines = ["\t".join(["Name", "Length", "EffectiveLength", "TPM", "NumReads"])]
        for g in range(n_tx):
            name = f"TX_{g:05d}"
            tpm = round(rng.uniform(0.0, 500.0), 4)
            nr = rng.randint(0, 2000)
            lines.append("\t".join([name, "1200", "1000", f"{tpm:.4f}", str(nr)]))
        (inp / f"{s}.quant.sf").write_text("\n".join(lines) + "\n")


def _cmd_snakepipes_merge_ct(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    out = gtdir / "reference_output" / "merged_tpm.tsv"
    inputs = sorted(str(p) for p in (workdir / "input").glob("*.quant.sf"))
    return ["Rscript", str(script), "Name", "TPM", str(out), *inputs]


# --------------------------------------------------------------------------- #
# riya_limma (commandArgs, volcano disabled with "NA" arg) — RNA              #
# --------------------------------------------------------------------------- #


def _gen_riya_limma(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = [f"GSM{i:04d}" for i in range(1, 9)]
    cancer_idx = {0, 1, 2, 3}
    n_genes = 400
    hdr = [""] + samples
    lines = [",".join(hdr)]
    for g in range(n_genes):
        row = [f"PROBE_{g:05d}"]
        de = (g % 18 == 0)
        for i, _ in enumerate(samples):
            base = 8.0 + rng.gauss(0, 0.3)
            if i in cancer_idx and de:
                base += 2.5
            elif i in cancer_idx and g % 29 == 0:
                base -= 2.0
            row.append(f"{base:.4f}")
        lines.append(",".join(row))
    (inp / "exprs.csv").write_text("\n".join(lines) + "\n")

    meta_lines = [",group"]
    for i, s in enumerate(samples):
        g = "cancer" if i in cancer_idx else "normal"
        meta_lines.append(f"{s},{g}")
    (inp / "meta.csv").write_text("\n".join(meta_lines) + "\n")


def _cmd_riya_limma(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    out = gtdir / "reference_output" / "deg_results.csv"
    # Passing only 3 args makes `args[4]` a real character NA, so the script's
    # `if (!is.na(volcano_plot))` short-circuits and no image is emitted.
    return [
        "Rscript", str(script),
        str(workdir / "input" / "exprs.csv"),
        str(workdir / "input" / "meta.csv"),
        str(out),
    ]


# --------------------------------------------------------------------------- #
# chipseq_plot_macs_qc (commandArgs, PDF redirected to tempfile)              #
# --------------------------------------------------------------------------- #


def _gen_chipseq_plot_macs_qc(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["sampleA", "sampleB", "sampleC"]
    for s in samples:
        lines = []
        n_peaks = rng.randint(80, 160)
        for i in range(n_peaks):
            start = rng.randint(1000, 1_000_000)
            end = start + rng.randint(150, 800)
            pileup = round(rng.uniform(5.0, 50.0), 2)
            fold = round(rng.uniform(1.5, 30.0), 2)
            log10p = round(rng.uniform(2.0, 50.0), 2)
            log10q = round(rng.uniform(1.0, log10p), 2)
            summit = rng.randint(0, end - start)
            lines.append("\t".join([
                "chr1", str(start), str(end), f"{s}_peak_{i}",
                str(rng.randint(100, 1000)), ".",
                f"{fold}", f"{log10p}", f"{log10q}", str(summit),
            ]))
        (inp / f"{s}_peaks.narrowPeak").write_text("\n".join(lines) + "\n")


def _cmd_chipseq_plot_macs_qc(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    summary_tsv = gtdir / "reference_output" / "macs_qc_summary.tsv"
    plot_pdf = gtdir / "reference_output" / "_macs_qc.pdf"  # goes to tempfile after patch
    peak_files = sorted(str(p) for p in (workdir / "input").glob("*_peaks.narrowPeak"))
    sample_ids = [Path(p).name.replace("_peaks.narrowPeak", "") for p in peak_files]
    return [
        "Rscript", str(script),
        "--peak_files", ",".join(peak_files),
        "--sample_ids", ",".join(sample_ids),
        "--outdir", str(plot_pdf),
        "--outprefix", str(summary_tsv),
    ]


# --------------------------------------------------------------------------- #
# chipseq_plot_homer_annot (commandArgs, PDF redirected)                      #
# --------------------------------------------------------------------------- #


def _gen_chipseq_plot_homer_annot(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["sampleA", "sampleB", "sampleC"]
    features = ["promoter-TSS", "exon", "intron", "intergenic", "TTS", "3' UTR", "5' UTR"]
    for s in samples:
        lines = ["\t".join([
            "PeakID", "Chr", "Start", "End", "Strand", "Peak Score",
            "Focus Ratio/Region Size", "Annotation", "Detailed Annotation",
            "Distance to TSS", "Nearest PromoterID", "Entrez ID", "Nearest Unigene",
            "Nearest Refseq", "Nearest Ensembl", "Gene Name", "Gene Alias",
            "Gene Description", "Gene Type"
        ])]
        n_peaks = rng.randint(80, 160)
        for i in range(n_peaks):
            ann = rng.choice(features) + " (NM_000{:03d})".format(rng.randint(0, 999))
            dtss = rng.choice([rng.randint(-50000, 50000), ""]) if rng.random() > 0.05 else ""
            prom = f"NM_000{rng.randint(0,9999):04d}" if dtss != "" else ""
            lines.append("\t".join([
                f"{s}_{i}", "chr1", str(1000 + i * 50), str(1500 + i * 50), "+",
                str(rng.randint(10, 500)), "0.5", ann, ann, str(dtss),
                prom, "NA", "NA", "NA", "NA", "GENE_X", "", "", "protein-coding",
            ]))
        (inp / f"{s}_annot.txt").write_text("\n".join(lines) + "\n")


def _cmd_chipseq_plot_homer_annot(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    summary_tsv = gtdir / "reference_output" / "homer_annot_summary.tsv"
    plot_pdf = gtdir / "reference_output" / "_homer_annot.pdf"
    homer_files = sorted(str(p) for p in (workdir / "input").glob("*_annot.txt"))
    sample_ids = [Path(p).name.replace("_annot.txt", "") for p in homer_files]
    return [
        "Rscript", str(script),
        "--homer_files", ",".join(homer_files),
        "--sample_ids", ",".join(sample_ids),
        "--outdir", str(plot_pdf),
        "--outprefix", str(summary_tsv),
    ]


# --------------------------------------------------------------------------- #
# snakepipes_scrna_merge_coutt (commandArgs) — scRNA                          #
# --------------------------------------------------------------------------- #


def _gen_snakepipes_scrna_merge_coutt(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input" / "coutt"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["plate01_libA", "plate01_libB"]
    n_genes = 120
    n_cells = 12
    for s in samples:
        hdr = ["GENEID"] + [f"X{i}" for i in range(1, n_cells + 1)]
        lines = ["\t".join(hdr)]
        for g in range(n_genes):
            gid = f"ENSG{g:08d}"
            row = [gid] + [str(rng.randint(0, 20)) for _ in range(n_cells)]
            lines.append("\t".join(row))
        (inp / f"{s}.corrected.txt").write_text("\n".join(lines) + "\n")


def _cmd_snakepipes_scrna_merge_coutt(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    out = gtdir / "reference_output" / "merged_coutt.tsv"
    cell_names = gtdir / "reference_output" / "merged_coutt.cell_names.tsv"
    return [
        "Rscript", str(script),
        str(workdir / "input" / "coutt"),
        str(out), str(cell_names),
        "FALSE",
    ]


# --------------------------------------------------------------------------- #
# snakepipes_scrna_qc (commandArgs, plot_format omitted -> NULL)              #
# --------------------------------------------------------------------------- #


def _gen_snakepipes_scrna_qc(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input" / "cellsum"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["plate01_libA", "plate01_libB"]
    for s in samples:
        lines = ["\t".join(["sample", "cell_idx", "READS_UNIQFEAT", "UMI"])]
        for c in range(1, 25):
            lines.append("\t".join([s, str(c),
                                    str(rng.randint(1000, 50000)),
                                    str(rng.randint(100, 5000))]))
        (inp / f"{s}.cellsum").write_text("\n".join(lines) + "\n")
        # libsum: V1=sample, V2=metric, V3=reads, V4=pct (no header)
        libsum_lines = []
        for metric in ["total_reads", "mapped_reads", "unique_reads", "deduped_reads"]:
            reads = rng.randint(100_000, 5_000_000)
            pct = round(rng.uniform(0.1, 1.0) * 100, 2)
            libsum_lines.append("\t".join([s, metric, str(reads), f"{pct}"]))
        (inp / f"{s}.libsum").write_text("\n".join(libsum_lines) + "\n")


def _cmd_snakepipes_scrna_qc(workdir: Path, gtdir: Path) -> list[str]:
    script = gtdir / "reference" / "script.R"
    out_prefix = gtdir / "reference_output" / "scqc"
    return [
        "Rscript", str(script),
        str(workdir / "input" / "cellsum"),
        str(out_prefix),
        "FALSE",
        # omit args[4] (cell_names_path) and args[5] (plot_format) so both NULL
    ]


# --------------------------------------------------------------------------- #
# longseq_deseq2_init (snakemake@) — RNA                                      #
# --------------------------------------------------------------------------- #


_LONGSEQ_SAMPLES = [
    ("samp1", "ko"),
    ("samp2", "ko"),
    ("samp3", "ko"),
    ("samp4", "wt"),
    ("samp5", "wt"),
    ("samp6", "wt"),
]


def _longseq_write_counts_and_samples(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    n_genes = 500
    sample_names = [s[0] for s in _LONGSEQ_SAMPLES]
    hdr = ["Reference", *sample_names]
    lines = ["\t".join(hdr)]
    for g in range(n_genes):
        gid = f"TX_{g:05d}"
        base = rng.randint(80, 2400)
        row = []
        de_up = g % 25 == 0
        de_down = g % 41 == 0
        for name, cond in _LONGSEQ_SAMPLES:
            is_ko = cond == "ko"
            if is_ko and de_up:
                c = int(base * rng.uniform(4.0, 7.0))
            elif is_ko and de_down:
                c = int(base * rng.uniform(0.07, 0.25))
            else:
                c = int(base * rng.uniform(0.9, 1.1))
            row.append(str(max(c, 0)))
        lines.append("\t".join([gid, *row]))
    (inp / "all_counts.tsv").write_text("\n".join(lines) + "\n")

    sam_lines = ["sample\tcondition"]
    for name, cond in _LONGSEQ_SAMPLES:
        sam_lines.append(f"{name}\t{cond}")
    (inp / "samples.tsv").write_text("\n".join(sam_lines) + "\n")


def _gen_longseq_deseq2_init(workdir: Path, rng: random.Random) -> None:
    _longseq_write_counts_and_samples(workdir, rng)


def _cmd_longseq_deseq2_init(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "dds.rds"
    out_tsv = gtdir / "reference_output" / "normalized_counts.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    inputs = {
        "all_counts": str(workdir / "input" / "all_counts.tsv"),
        "samples":    str(workdir / "input" / "samples.tsv"),
    }
    config = {
        "deseq2": {
            "design_factors": ["condition"],
            "batch_effect":   [""],
            "fit_type":       "",
            "mincount":       10,
        }
    }
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=inputs,
        outputs=[str(out_rds), str(out_tsv)],
        params={},
        config=config,
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# longseq_deseq2_contrast (snakemake@, strip SVGs + heatmap blocks)           #
# --------------------------------------------------------------------------- #


def _gen_longseq_deseq2_contrast(workdir: Path, rng: random.Random) -> None:
    _longseq_write_counts_and_samples(workdir, rng)
    # Pre-run the init script to produce dds.rds.
    prep = workdir / "input" / "_prep_dds.R"
    dds_rds = workdir / "input" / "dds.rds"
    init_script = _WFC / "snakemake-workflows__rna-longseq-de-isoform/workflow/scripts/deseq2-init.R"
    log_path = workdir / "input" / "_prep_dds.log"
    _emit_snakemake_wrapper(
        prep,
        script_to_source=init_script,
        inputs={
            "all_counts": str(workdir / "input" / "all_counts.tsv"),
            "samples":    str(workdir / "input" / "samples.tsv"),
        },
        outputs=[str(dds_rds), str(workdir / "input" / "_prep_normalized.tsv")],
        params={},
        config={"deseq2": {
            "design_factors": ["condition"], "batch_effect": [""],
            "fit_type": "", "mincount": 10,
        }},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(workdir / "input"),
    )
    env = os.environ.copy()
    proc = subprocess.run(
        ["Rscript", str(prep)], capture_output=True, text=True, env=env,
    )
    if proc.returncode != 0 or not dds_rds.exists():
        raise RuntimeError(
            "deseq2-init pre-step failed for longseq_deseq2_contrast:\n"
            + (proc.stderr or "")[-4000:]
        )


def _cmd_longseq_deseq2_contrast(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    dds_rds = workdir / "input" / "dds.rds"
    out_tsv = gtdir / "reference_output" / "contrast_results.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    sink_dir = gtdir / "reference_output"
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=[str(dds_rds)],
        outputs={
            "table":             str(out_tsv),
            "ma_plot":           str(sink_dir / "_ma.svg"),
            "sample_heatmap":    str(sink_dir / "_sample_heatmap.svg"),
            "count_heatmap":     str(sink_dir / "_count_heatmap.svg"),
            "top_count_heatmap": str(sink_dir / "_top_count_heatmap.svg"),
            "dispersion_plot":   str(sink_dir / "_dispersion.svg"),
        },
        params={
            "factor":          "condition",
            "prop_a":          "ko",
            "prop_b":          "wt",
            "alpha":           0.05,
            "lfc_null":        0.0,
            "alt_hypothesis":  "greaterAbs",
            "colormap":        "Blues",
            "threshold_plot":  50,
        },
        config={"deseq2": {"mincount": 10}},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# spilterlize_filter_features (snakemake@) — RNA/epigenomics                  #
# --------------------------------------------------------------------------- #


def _spilterlize_write_counts(workdir: Path, rng: random.Random,
                              n_genes: int = 400,
                              n_samples: int = 6) -> tuple[list[str], list[str]]:
    """Shared helper: emit `input/counts.csv` + `input/annotation.csv`.
    Counts has a header row with an empty first cell (row-names column) and
    samples thereafter; annotation has `sample_name,group,batch`."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = [f"S{i:02d}" for i in range(1, n_samples + 1)]
    groups = ["A" if i < n_samples // 2 else "B" for i in range(n_samples)]
    batches = [("b1" if i % 2 == 0 else "b2") for i in range(n_samples)]
    # Counts (TSV is fine; `fread` with header=TRUE auto-detects).
    lines = [",".join([""] + samples)]
    for g in range(n_genes):
        gid = f"GENE_{g:05d}"
        row = [gid]
        de_up = g % 25 == 0
        de_down = g % 41 == 0
        for i in range(n_samples):
            base = rng.randint(60, 1500)
            if groups[i] == "B" and de_up:
                c = int(base * rng.uniform(4.0, 7.0))
            elif groups[i] == "B" and de_down:
                c = int(base * rng.uniform(0.07, 0.25))
            else:
                c = int(base * rng.uniform(0.9, 1.1))
            row.append(str(max(c, 0)))
        lines.append(",".join(row))
    (inp / "counts.csv").write_text("\n".join(lines) + "\n")

    # annotation: fread expects first column as row.names for `data.frame(fread(...), row.names=1)`.
    ann_lines = [",".join(["sample_name", "group", "batch"])]
    for s, g, b in zip(samples, groups, batches):
        ann_lines.append(",".join([s, g, b]))
    (inp / "annotation.csv").write_text("\n".join(ann_lines) + "\n")
    return samples, groups


def _gen_spilterlize_filter(workdir: Path, rng: random.Random) -> None:
    _spilterlize_write_counts(workdir, rng)


def _cmd_spilterlize_filter(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_csv = gtdir / "reference_output" / "filtered_counts.csv"
    log_path = gtdir / "reference" / "run.R.log"
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={
            "data":       str(workdir / "input" / "counts.csv"),
            "annotation": str(workdir / "input" / "annotation.csv"),
        },
        outputs={"filtered_counts": str(out_csv)},
        params={"filter_parameters": {
            "group":           "group",
            "min.count":       10,
            "min.total.count": 15,
            "large.n":         10,
            "min.prop":        0.7,
        }},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# spilterlize_norm_voom (snakemake@, PNG redirected)                           #
# --------------------------------------------------------------------------- #


def _gen_spilterlize_voom(workdir: Path, rng: random.Random) -> None:
    # Produce filtered_counts.csv directly (DGEList-friendly) as the voom
    # script only reads that one input.
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = [f"S{i:02d}" for i in range(1, 7)]
    n_genes = 300
    lines = [",".join([""] + samples)]
    for g in range(n_genes):
        gid = f"GENE_{g:05d}"
        row = [gid]
        for i in range(len(samples)):
            base = rng.randint(200, 3000)
            row.append(str(max(int(base * rng.uniform(0.9, 1.1)), 0)))
        lines.append(",".join(row))
    (inp / "filtered_counts.csv").write_text("\n".join(lines) + "\n")


def _cmd_spilterlize_voom(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_csv = gtdir / "reference_output" / "normalized_counts.csv"
    log_path = gtdir / "reference" / "run.R.log"
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"filtered_counts": str(workdir / "input" / "filtered_counts.csv")},
        outputs={
            "normalized_counts": str(out_csv),
            "voom_plot":         str(gtdir / "reference_output" / "_voom.png"),
        },
        params={"split": "all"},
        config={
            "edgeR_parameters": {
                "refColumn":    "NULL",
                "logratioTrim": 0.3,
                "sumTrim":      0.05,
                "doWeighting":  "TRUE",
                "Acutoff":      -1e10,
                "p":            0.75,
            },
            "voom_parameters": {
                "calcNormFactors_method": "TMM",
                "normalize.method":       "none",
                "span":                   0.5,
            },
        },
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# spilterlize_limma_rbe (snakemake@) — RNA/epigenomics integration             #
# --------------------------------------------------------------------------- #


def _gen_spilterlize_rbe(workdir: Path, rng: random.Random) -> None:
    # normalized_data: genes x samples (log CPM-ish). Annotation: sample x cols.
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = [f"S{i:02d}" for i in range(1, 9)]
    groups = ["A"] * 4 + ["B"] * 4
    batches = [("b1" if i % 2 == 0 else "b2") for i in range(len(samples))]
    n_genes = 250
    lines = [",".join([""] + samples)]
    for g in range(n_genes):
        gid = f"GENE_{g:05d}"
        row = [gid]
        for i, s in enumerate(samples):
            base = 8.0 + rng.gauss(0, 0.3)
            if groups[i] == "B":
                base += 0.4
            if batches[i] == "b2":
                base += 0.6
            row.append(f"{base:.4f}")
        lines.append(",".join(row))
    (inp / "normalized.csv").write_text("\n".join(lines) + "\n")
    ann = [",".join(["sample_name", "group", "batch"])]
    for s, g, b in zip(samples, groups, batches):
        ann.append(",".join([s, g, b]))
    (inp / "annotation.csv").write_text("\n".join(ann) + "\n")


def _cmd_spilterlize_rbe(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_csv = gtdir / "reference_output" / "integrated_data.csv"
    log_path = gtdir / "reference" / "run.R.log"
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={
            "normalized_data": str(workdir / "input" / "normalized.csv"),
            "annotation":      str(workdir / "input" / "annotation.csv"),
        },
        outputs={"integrated_data": str(out_csv)},
        params={
            "desired":              _RVec(["group"]),
            "unwanted_categorical": _RVec(["batch"]),
            "unwanted_numerical":   _RVec([]),
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# dea_limma (snakemake@, PDFs redirected)                                     #
# --------------------------------------------------------------------------- #


def _gen_dea_limma(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = [f"S{i:02d}" for i in range(1, 11)]
    groups = ["UT"] * 5 + ["TR"] * 5
    # Count table (tab-sep) — script uses fread, autodetects sep.
    n_genes = 400
    hdr = "\t".join([""] + samples)
    lines = [hdr]
    for g in range(n_genes):
        gid = f"GENE_{g:05d}"
        row = [gid]
        de_up = g % 22 == 0
        for i, s in enumerate(samples):
            base = rng.randint(60, 2000)
            if groups[i] == "TR" and de_up:
                c = int(base * rng.uniform(4.0, 8.0))
            else:
                c = int(base * rng.uniform(0.9, 1.1))
            row.append(str(max(c, 0)))
        lines.append("\t".join(row))
    (inp / "counts.tsv").write_text("\n".join(lines) + "\n")
    # Metadata
    meta = ["\t".join(["sample_name", "treatment"])]
    for s, g in zip(samples, groups):
        meta.append("\t".join([s, g]))
    (inp / "metadata.tsv").write_text("\n".join(meta) + "\n")


def _cmd_dea_limma(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_results = gtdir / "reference_output" / "dea_results.csv"
    out_lmfit = gtdir / "reference_output" / "lmfit.rds"
    out_mm = gtdir / "reference_output" / "model_matrix.csv"
    log_path = gtdir / "reference" / "run.R.log"
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=[
            str(workdir / "input" / "counts.tsv"),
            str(workdir / "input" / "metadata.tsv"),
        ],
        outputs={
            "dea_results":   str(out_results),
            "lmfit_object":  str(out_lmfit),
            "model_matrix":  str(out_mm),
        },
        params={
            "feature_annotation_col": "",
            "reference_levels":       {"treatment": "UT"},
            "formula":                "~ treatment",
            "block_var":              0,
            "comparisons":            "treatment",
            "calcNormFactors_method": "TMM",
            "voom":                   1,
            "eBayes":                 1,
            "limma_trend":            0,
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# msisensor_merge (snakemake@) — variant/MSI                                  #
# --------------------------------------------------------------------------- #


def _gen_msisensor_merge(workdir: Path, rng: random.Random) -> None:
    """Synthesize MSIsensor-style output under results/msi/<sample>/msi_out.txt
    so the regex `results/[^/]+/(?<match>[^/]+)/.+` extracts `sample`."""
    base = workdir / "results" / "msi"
    base.mkdir(parents=True, exist_ok=True)
    samples = ["caseA", "caseB", "caseC"]
    for s in samples:
        d = base / s
        d.mkdir(parents=True, exist_ok=True)
        lines = [
            "Total_Number_of_Sites\tNumber_of_Unstable_Sites\t%",
            f"{rng.randint(100, 500)}\t{rng.randint(0, 40)}\t{rng.uniform(0, 20):.4f}",
        ]
        (d / "msi_out.txt").write_text("\n".join(lines) + "\n")


def _cmd_msisensor_merge(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_tsv = gtdir / "reference_output" / "merged_msi.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    rel_files = sorted(
        str(Path("results") / "msi" / s.name / "msi_out.txt")
        for s in (workdir / "results" / "msi").iterdir()
        if s.is_dir()
    )
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"msi_results": _RVec(rel_files)},
        outputs={"tsv": str(out_tsv)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        pre_source_r=f'setwd({_r_quote(str(workdir))})',
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# methylkit_filt_norm (snakemake@, strip plot calls)                          #
# --------------------------------------------------------------------------- #


def _gen_methylkit_filt_norm(workdir: Path, rng: random.Random) -> None:
    """Create bismark files + produce mk_raw.rds via methRead so the script
    can readRDS it as its single input."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    sample_names = ["sampleA", "sampleB", "sampleC"]
    n_sites_per_chr = 150
    chroms = ["chr1", "chr2"]
    for s in sample_names:
        lines = []
        for ch in chroms:
            for i in range(n_sites_per_chr):
                cov = rng.randint(5, 60)
                meth = rng.randint(0, cov)
                unmeth = cov - meth
                pct = 100.0 * meth / cov
                pos = 500 + i * 40
                lines.append(f"{ch}\t{pos}\t{pos}\t{pct:.4f}\t{meth}\t{unmeth}")
        (inp / f"{s}.bismark.cov").write_text("\n".join(lines) + "\n")


def _cmd_methylkit_filt_norm(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "mk_filt_norm.rds"
    out_tsv = gtdir / "reference_output" / "filt_norm_stats.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    src_scripts = _WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts"

    bismark_rel = sorted(
        Path("input") / p.name for p in (workdir / "input").glob("*.bismark.cov")
    )
    sample_names = [p.name.replace(".bismark.cov", "") for p in bismark_rel]

    pre = f"""
suppressPackageStartupMessages({{
  library(methylKit)
}})
# Upstream: methRead to produce mk_raw, then save to input/mk_raw.rds so the
# filt_norm script's `readRDS(INPUT_FILE)` can consume it.
mk_raw <- methylKit::methRead(
  location  = as.list({_r_quote([str(p) for p in bismark_rel])}),
  sample.id = as.list({_r_quote(sample_names)}),
  assembly  = "mock_v1",
  treatment = as.integer(c({",".join("0" if i < 2 else "1" for i in range(len(sample_names)))})),
  header    = FALSE, mincov = 4, pipeline = "bismarkCoverage"
)
mk_raw_rds <- "input/mk_raw.rds"
saveRDS(mk_raw, mk_raw_rds)
snakemake@input <- list(mk_raw_rds)
"""
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=["placeholder"],
        outputs={
            "rds":         str(out_rds),
            "stats_tsv":   str(out_tsv),
            "plots_filt":  "output/_plots_filt/.sentinel",
            "plots_norm":  "output/_plots_norm/.sentinel",
        },
        params={
            "low_cov_threshold_abs":    3,
            "high_cov_threshold_perc":  99.9,
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(src_scripts),
        pre_source_r=pre,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# methylkit2tibble_split (snakemake@, upstream tibbles RDS)                   #
# --------------------------------------------------------------------------- #


def _gen_methylkit2tibble_split(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    # Two disjoint sample groups to feed the split script.
    for group, samples in (("grp1", ["a1", "a2", "a3"]), ("grp2", ["b1", "b2", "b3"])):
        for s in samples:
            lines = []
            for ch in ("chr1", "chr2"):
                for i in range(150):
                    cov = rng.randint(5, 60)
                    meth = rng.randint(0, cov)
                    pct = 100.0 * meth / cov
                    pos = 500 + i * 40
                    lines.append(f"{ch}\t{pos}\t{pos}\t{pct:.4f}\t{meth}\t{cov - meth}")
            (inp / f"{group}__{s}.bismark.cov").write_text("\n".join(lines) + "\n")


def _cmd_methylkit2tibble_split(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "df_mku_split.rds"
    out_tsv = gtdir / "reference_output" / "mean_mcpg_split.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    src_scripts = _WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts"

    pre = f"""
setwd({_r_quote(str(workdir))})
suppressPackageStartupMessages({{
  library(methylKit); library(tidyverse)
}})
group_to_rds <- list()
for (group in c("grp1","grp2")) {{
  files <- Sys.glob(file.path("input", paste0(group, "__*.bismark.cov")))
  sample_ids <- sub("\\\\.bismark\\\\.cov$", "", basename(files))
  sample_ids <- sub(paste0("^", group, "__"), "", sample_ids)
  mk_raw <- methylKit::methRead(
    location  = as.list(files), sample.id = as.list(sample_ids),
    assembly = "mock_v1",
    treatment = as.integer(seq_along(sample_ids) > length(sample_ids) / 2),
    header = FALSE, mincov = 4, pipeline = "bismarkCoverage"
  )
  mk_u <- methylKit::unite(mk_raw, min.per.group = 1L, destrand = FALSE)
  out <- file.path("input", paste0(group, "_mku.rds"))
  saveRDS(mk_u, out)
  group_to_rds[[group]] <- out
}}
snakemake@input$rds_list <- unlist(group_to_rds, use.names = FALSE)
"""
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"rds_list": ["placeholder"]},
        outputs={"rds": str(out_rds), "stats_tsv": str(out_tsv)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(src_scripts),
        pre_source_r=pre,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# methylkit_remove_snvs (snakemake@, upstream tibble + bed)                   #
# --------------------------------------------------------------------------- #


def _gen_methylkit_remove_snvs(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["a1", "a2", "a3"]
    for s in samples:
        lines = []
        for ch in ("chr1", "chr2"):
            for i in range(150):
                cov = rng.randint(5, 60)
                meth = rng.randint(0, cov)
                pct = 100.0 * meth / cov
                pos = 500 + i * 40
                lines.append(f"{ch}\t{pos}\t{pos}\t{pct:.4f}\t{meth}\t{cov - meth}")
        (inp / f"{s}.bismark.cov").write_text("\n".join(lines) + "\n")
    # Exclusion bed (seqnames start end ref alt score), tab-sep, 0-based starts.
    bed_lines = []
    for _ in range(30):
        ch = rng.choice(["chr1", "chr2"])
        # Pick an overlap position near the grid: start in {500,540,...}
        idx = rng.randint(0, 149)
        start = 499 + idx * 40  # 0-based
        bed_lines.append("\t".join([ch, str(start), str(start + 1),
                                    rng.choice(["A", "C", "G", "T"]),
                                    rng.choice(["A", "C", "G", "T"]),
                                    f"{rng.uniform(0, 1):.2f}"]))
    (inp / "exclusion.bed").write_text("\n".join(bed_lines) + "\n")


def _cmd_methylkit_remove_snvs(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_rds = gtdir / "reference_output" / "df_united_excl.rds"
    out_tsv = gtdir / "reference_output" / "snv_stats.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    src_scripts = _WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts"

    pre = f"""
suppressPackageStartupMessages({{
  library(methylKit); library(tidyverse)
}})
source(file.path({_r_quote(str(src_scripts))}, "methylkit_common.R"))
files <- Sys.glob(file.path("input", "*.bismark.cov"))
sample_ids <- sub("\\\\.bismark\\\\.cov$", "", basename(files))
mk_raw <- methylKit::methRead(
  location = as.list(files), sample.id = as.list(sample_ids),
  assembly = "mock_v1",
  treatment = as.integer(seq_along(sample_ids) > length(sample_ids)/2),
  header = FALSE, mincov = 4, pipeline = "bismarkCoverage",
  dbtype = "tabix", dbdir = "input/mk_db"
)
mk_u <- methylKit::unite(mk_raw, min.per.group = 1L, destrand = FALSE,
                         save.db = TRUE, dbdir = "input/mk_db",
                         suffix = "unite")
df_united <- mku2tibble(mk_u)
saveRDS(df_united, "input/df_united.rds")
snakemake@input$tibble <- "input/df_united.rds"
snakemake@input$exclusion_variants_bedfile <- "input/exclusion.bed"
"""
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"tibble": "placeholder", "exclusion_variants_bedfile": "placeholder"},
        outputs={"tibble": str(out_rds), "stats_tsv": str(out_tsv)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(src_scripts),
        pre_source_r=pre,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# phantompeak_correlation (snakemake@) — ChIP-seq cross-correlation summary   #
# --------------------------------------------------------------------------- #


def _gen_phantompeak(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    # header.csv — the script copies it as the first line, then appends the
    # cross.correlation values.
    (inp / "header.csv").write_text("shift,cross_correlation\n")
    # data .RData with a `crosscorr` list containing `cross.correlation` as a
    # 2-column data.frame (shift, cross-correlation value).
    ks = list(range(-50, 500, 25))
    vals = []
    for k in ks:
        # Bell-ish curve peaked near 150 bp.
        vals.append(round(0.1 + 0.9 * (1.0 / (1.0 + ((k - 150) / 80.0) ** 2)), 6))
    build = workdir / "input" / "_build_rdata.R"
    build.write_text(f"""
shift <- c({",".join(str(k) for k in ks)})
cc    <- c({",".join(str(v) for v in vals)})
crosscorr <- list(`cross.correlation` = data.frame(shift = shift, `cross_correlation` = cc, check.names = FALSE))
save(crosscorr, file = "input/run_spp.RData")
""")
    env = os.environ.copy()
    proc = subprocess.run(
        ["Rscript", str(build)], cwd=workdir, capture_output=True, text=True, env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError("phantompeak prep failed: " + (proc.stderr or "")[-2000:])


def _cmd_phantompeak(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_csv = gtdir / "reference_output" / "crosscorr.csv"
    log_path = gtdir / "reference" / "run.R.log"
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={
            "header": str(workdir / "input" / "header.csv"),
            "data":   str(workdir / "input" / "run_spp.RData"),
        },
        outputs=[str(out_csv)],
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# nearestGene (snakemake@) — ChIP/ATAC annotation                             #
# --------------------------------------------------------------------------- #


def _gen_nearest_gene(workdir: Path, rng: random.Random) -> None:
    """Synthesize a bedtools-closest 24-column output + t2g + gene_symbol."""
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    # 24 columns: V1..V18 = CSAW-like DB result per peak; V19..V24 = nearest gene fields
    # We mirror the nearestGene.R subset: keep V1..V18, V23 (Name/GeneStrand), V24 (Distance)
    lines = []
    n_peaks = 40
    n_genes = 20
    for i in range(n_peaks):
        # CSAW-like: chr start end width strand score nWindows logFCup logFCdown PValue FDR direction rep.test rep.logFC best.logFC best.test best.start Name
        start = 1000 + i * 1000
        end = start + rng.randint(200, 2000)
        width = end - start
        csaw = [
            "chr1", str(start), str(end), str(width), "+",
            f"{rng.uniform(0.1, 3.0):.3f}", str(rng.randint(1, 5)),
            f"{rng.uniform(0.1, 2.0):.3f}", f"{-rng.uniform(0.1, 2.0):.3f}",
            f"{rng.uniform(1e-6, 0.1):.4g}", f"{rng.uniform(1e-5, 0.1):.4g}",
            rng.choice(["up", "down"]), str(rng.randint(0, 5)),
            f"{rng.uniform(-2, 2):.3f}", f"{rng.uniform(-2, 2):.3f}",
            f"{rng.uniform(-10, -1):.3f}", str(rng.randint(0, 1000)),
            f"region_{i}",
        ]
        # nearest-gene: chr, start, end, txid (V22), gene_strand (V23), distance (V24)
        tx = f"tx{(i % n_genes):03d}"
        gene_strand = rng.choice(["+", "-"])
        distance = rng.randint(-50000, 50000)
        near = ["chr1", str(start - 5000), str(end + 5000), tx, gene_strand, str(distance)]
        lines.append("\t".join(csaw + near))
    (inp / "peaks_with_nearest.bed").write_text("\n".join(lines) + "\n")

    # t2g: tx -> gene_id
    t2g = []
    for k in range(n_genes):
        tx = f"tx{k:03d}"
        t2g.append("\t".join([tx, f"GENE_{k:03d}"]))
    (inp / "t2g.tsv").write_text("\n".join(t2g) + "\n")

    # gene_symbol: gene_id -> symbol
    gs = []
    for k in range(n_genes):
        gs.append("\t".join([f"GENE_{k:03d}", f"Sym{k:03d}"]))
    (inp / "gene_symbol.tsv").write_text("\n".join(gs) + "\n")


def _cmd_nearest_gene(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_bed = gtdir / "reference_output" / "annotated.bed"
    log_path = gtdir / "reference" / "run.R.log"
    # params$wdir is where the script tries to write sessionInfo — point it
    # somewhere writable that isn't part of eval_files.
    session_dir = gtdir / "reference_output" / "_session"
    session_dir.mkdir(parents=True, exist_ok=True)
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={
            "bed":         str(workdir / "input" / "peaks_with_nearest.bed"),
            "t2g":         str(workdir / "input" / "t2g.tsv"),
            "gene_symbol": str(workdir / "input" / "gene_symbol.tsv"),
        },
        outputs={"annotated_bed": str(out_bed)},
        params={"pipeline": "chipseq", "wdir": str(session_dir)},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# spilterlize_norm_edgeR (snakemake@) — RNA                                   #
# --------------------------------------------------------------------------- #


def _gen_spilterlize_norm_edger(workdir: Path, rng: random.Random) -> None:
    _gen_spilterlize_voom(workdir, rng)


def _cmd_spilterlize_norm_edger(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    log_path = gtdir / "reference" / "run.R.log"
    # The script writes to `result_path/split/norm<method>.csv`, which is a
    # params value. Point it at reference_output/<split>/ so we can glob the
    # outputs as eval_files.
    result_path = gtdir / "reference_output"
    split = "all"
    (result_path / split).mkdir(parents=True, exist_ok=True)
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"filtered_counts": str(workdir / "input" / "filtered_counts.csv")},
        outputs={},
        params={
            "result_path": str(result_path),
            "split": split,
            "norm_parameters": {
                "method":          _RVec(["TMM"]),
                "refColumn":       "NULL",
                "logratioTrim":    0.3,
                "sumTrim":         0.05,
                "doWeighting":     "TRUE",
                "Acutoff":         -1e10,
                "p":               0.75,
                "quantification":  "CPM",
                "gene.length":     "",
                "log":             "TRUE",
                "prior.count":     3,
            },
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# V3.1: plot_frip_score (snakemake@, emit TSV via post-source)                #
# --------------------------------------------------------------------------- #


def _gen_chipseq_plot_frip(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    pairs = [("sampleA_control", rng.uniform(0.08, 0.35)),
             ("sampleB_control", rng.uniform(0.05, 0.40)),
             ("sampleC_control", rng.uniform(0.10, 0.30)),
             ("sampleD_control", rng.uniform(0.12, 0.32))]
    for name, score in pairs:
        (inp / f"{name}.frip.txt").write_text(f"{name}\t{score:.6f}\n")


def _cmd_chipseq_plot_frip(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_tsv = gtdir / "reference_output" / "frip_scores.tsv"
    png_sink = gtdir / "reference_output" / "_ignored.png"
    log_path = gtdir / "reference" / "run.R.log"
    frip_files = sorted(str(p) for p in (workdir / "input").glob("*.frip.txt"))
    post = f"""
# Emit the tibble `frip_scores` (defined by the sourced script) as TSV.
readr::write_tsv(frip_scores, {_r_quote(str(out_tsv))})
"""
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=list(frip_files),
        outputs={"1": str(png_sink)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        post_source_r=post,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# V3.1: plot_peaks_count_macs2 (snakemake@, emit TSV via post-source)         #
# --------------------------------------------------------------------------- #


def _gen_chipseq_plot_peaks_count(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    pairs = [
        ("sampleA_control", rng.randint(1200, 4200)),
        ("sampleB_control", rng.randint(800, 3800)),
        ("sampleC_control", rng.randint(1500, 5200)),
        ("sampleD_control", rng.randint(900, 4500)),
    ]
    for name, cnt in pairs:
        (inp / f"{name}.peaks_count.txt").write_text(f"{name}\t{cnt}\n")


def _cmd_chipseq_plot_peaks_count(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_tsv = gtdir / "reference_output" / "peaks_count.tsv"
    png_sink = gtdir / "reference_output" / "_ignored.png"
    log_path = gtdir / "reference" / "run.R.log"
    files = sorted(str(p) for p in (workdir / "input").glob("*.peaks_count.txt"))
    post = f"""
readr::write_tsv(counts, {_r_quote(str(out_tsv))})
"""
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs=list(files),
        outputs={"1": str(png_sink)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        post_source_r=post,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# V3.1: plot_annotatepeaks_summary_homer (snakemake@, emit TSV via post-src)  #
# --------------------------------------------------------------------------- #


def _gen_chipseq_plot_annotatepeaks_summary(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["sampleA", "sampleB", "sampleC"]
    cols = ["sample", "exon", "Intergenic", "intron", "promoter-TSS", "TTS"]
    rows = ["\t".join(cols)]
    for s in samples:
        vals = [str(rng.randint(50, 900)) for _ in range(5)]
        rows.append("\t".join([s] + vals))
    (inp / "homer_summary.tsv").write_text("\n".join(rows) + "\n")


def _cmd_chipseq_plot_annotatepeaks_summary(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_tsv = gtdir / "reference_output" / "homer_long.tsv"
    png_sink = gtdir / "reference_output" / "_ignored.png"
    log_path = gtdir / "reference" / "run.R.log"
    post = f"""
readr::write_tsv(homer_data, {_r_quote(str(out_tsv))})
"""
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={"1": str(workdir / "input" / "homer_summary.tsv")},
        outputs={"1": str(png_sink)},
        params={},
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
        post_source_r=post,
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# V3.1: epibtn_gene_expression_rpkm (commandArgs)                             #
# --------------------------------------------------------------------------- #


def _gen_epibtn_rpkm(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    samples = ["WT_1", "WT_2", "WT_3", "KO_1", "KO_2", "KO_3"]
    n_genes = 180
    gene_ids = [f"GENE_{i:05d}" for i in range(n_genes)]
    # genecount: tab-separated, GID header + one column per sample
    lines = ["\t".join(["GID", *samples])]
    for g in gene_ids:
        row = [g] + [str(rng.randint(5, 2000)) for _ in samples]
        lines.append("\t".join(row))
    # sprinkle a couple of "N_" rows that must be filtered
    for nm in ("N_ambiguous", "N_multimapping"):
        lines.append("\t".join([nm] + [str(rng.randint(10, 200)) for _ in samples]))
    (inp / "genecount.tsv").write_text("\n".join(lines) + "\n")

    # targets: Sample + Replicate columns
    tgt = ["\t".join(["Sample", "Replicate"])]
    for s in samples:
        base, rep = s.split("_")
        tgt.append("\t".join([base, s]))
    (inp / "targets.tsv").write_text("\n".join(tgt) + "\n")

    # ref_genes: 6 cols (Chr Start Stop Name Value Strand), no header
    ref = []
    for i, g in enumerate(gene_ids):
        start = 1000 + i * 3000
        stop = start + rng.randint(500, 3500)
        name_attr = f"ID=gene:{g};biotype=protein_coding"
        ref.append("\t".join([
            "chr1", str(start), str(stop), name_attr, ".", "+"
        ]))
    (inp / "ref_genes.bed").write_text("\n".join(ref) + "\n")


def _cmd_epibtn_rpkm(workdir: Path, gtdir: Path) -> list[str]:
    # Script has a hardcoded relative output path:
    #   results/RNA/DEG/genes_rpkm__<analysisname>__<refgenome>.txt
    # We pre-create the dir under gtdir/reference_output and chdir there.
    analysis = "runX"
    refgenome = "mockref"
    out_root = gtdir / "reference_output"
    (out_root / "results" / "RNA" / "DEG").mkdir(parents=True, exist_ok=True)
    script_src = _WFC / "joncahn__epigeneticbutton/workflow/scripts/R_gene_expression_rpkm.R"
    # Write a tiny wrapper that cds into out_root and dispatches with args.
    wrapper = gtdir / "reference" / "wrapper.R"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(
        f"setwd({_r_quote(str(out_root))})\n"
        f"commandArgs <- function(trailingOnly = FALSE) if (trailingOnly) c(\n"
        f"  {_r_quote(str(workdir / 'input' / 'genecount.tsv'))},\n"
        f"  {_r_quote(str(workdir / 'input' / 'targets.tsv'))},\n"
        f"  {_r_quote(analysis)},\n"
        f"  {_r_quote(refgenome)},\n"
        f"  {_r_quote(str(workdir / 'input' / 'ref_genes.bed'))}\n"
        f") else c(\"Rscript\")\n"
        f"source({_r_quote(str(gtdir / 'reference' / 'script.R'))}, echo = FALSE)\n"
    )
    return ["Rscript", str(wrapper)]


# --------------------------------------------------------------------------- #
# V3.1: clean_histoneHMM_result (snakemake@)                                  #
# --------------------------------------------------------------------------- #


def _gen_clean_histoneHMM(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    for s in ("sampleA", "sampleB"):
        lines = ['##gff-version 3']
        n = rng.randint(30, 80)
        for i in range(n):
            start = 1_000 + i * 5_000
            end = start + rng.randint(500, 3_000)
            avg = rng.random()  # 0..1
            lines.append(
                f"chr1\thistoneHMM\tbroadPeak\t{start}\t{end}\t.\t.\t.\t"
                f"ID=peak{i};avg_posterior={avg:.4f}"
            )
        (inp / f"{s}.filtered.histoneHMM-regions.gff").write_text("\n".join(lines) + "\n")


def _cmd_clean_histoneHMM(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    outdir = gtdir / "reference_output"
    outdir.mkdir(parents=True, exist_ok=True)
    log_path = gtdir / "reference" / "run.R.log"
    input_peaks = sorted(
        str(p) for p in (workdir / "input").glob("*.filtered.histoneHMM-regions.gff")
    )
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={},
        outputs={},
        params={
            "outdir": str(outdir),
            "input_peaks": _RVec(input_peaks),
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# V3.2: snakepipes_scrna_report (snakemake@, simple metric-table merge)       #
# --------------------------------------------------------------------------- #


def _gen_snakepipes_scrna_report(workdir: Path, rng: random.Random) -> None:
    inp = workdir / "input"
    inp.mkdir(parents=True, exist_ok=True)
    # Three single-library CSV metric tables (Metric,<col>) with partially
    # overlapping Metric keys (merge by="Metric", all=TRUE).
    metrics_all = [
        "total_reads", "uniquely_mapped", "multi_mapped",
        "unmapped_too_short", "unmapped_other", "ercc_reads",
        "mito_reads", "ribo_reads",
    ]
    for i, lib in enumerate(("libA", "libB", "libC")):
        # Drop one metric per library to ensure an outer-merge picture.
        keep = [m for j, m in enumerate(metrics_all) if j != i]
        rows = []
        for m in keep:
            v = rng.randint(10_000, 5_000_000)
            rows.append(f"{m},{v}")
        (inp / f"{lib}.metrics.csv").write_text("\n".join(rows) + "\n")


def _cmd_snakepipes_scrna_report(workdir: Path, gtdir: Path) -> list[str]:
    wrapper_path = gtdir / "reference" / "wrapper.R"
    out_tsv = gtdir / "reference_output" / "scrna_report.tsv"
    log_path = gtdir / "reference" / "run.R.log"
    libs = ["libA", "libB", "libC"]
    rdir_paths = [str(workdir / "input" / f"{lib}.metrics.csv") for lib in libs]
    _emit_snakemake_wrapper(
        wrapper_path,
        script_to_source=gtdir / "reference" / "script.R",
        inputs={},
        outputs={"report": str(out_tsv)},
        params={
            "wdir":    str(gtdir / "reference_output"),
            "input":   _RVec(rdir_paths),
            "samples": _RVec(libs),
        },
        config={},
        wildcards={},
        threads=1,
        log_path=str(log_path),
        scriptdir=str(gtdir / "reference"),
    )
    return ["Rscript", str(wrapper_path)]


# --------------------------------------------------------------------------- #
# TASKS registry                                                              #
# --------------------------------------------------------------------------- #


TASKS: dict[str, TaskSpec] = {
    "akinyi_deseq2": TaskSpec(
        task_id="akinyi_deseq2",
        workflow_id="akinyi-onyango-rna_seq_pipeline-finish",
        family="rna",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "Akinyi-Onyango__rna_seq_pipeline/scripts/deseq_analysis.r",
        description="DESeq2 differential expression on featureCounts output (Akinyi RNA-seq pipeline).",
        analyst_objective=(
            "You are given a featureCounts-style count matrix in `input/featureCounts_output.txt`.\n"
            "It has columns: Geneid, Chr, Start, End, Strand, Length, followed by 6 sample\n"
            "columns named sample_0..sample_5. The first 3 samples are condition_A and the last\n"
            "3 are condition_B. Rows starting with `ERCC-` must be dropped.\n\n"
            "Run DESeq2 differential expression (`design = ~condition`) and produce two outputs:\n"
            "  - `output/deseq2_up.txt`: genes with log2FoldChange >= 2 (rownames = Geneid)\n"
            "  - `output/deseq2_down.txt`: genes with log2FoldChange <= -2\n"
            "Both must be written with `write.table(..., col.names=TRUE, row.names=TRUE, quote=FALSE)`.\n"
            "Filter out rows where log2FoldChange or padj is NA before the up/down split."
        ),
        generate_inputs=_gen_akinyi_deseq2,
        run_cmd=_cmd_akinyi,
        success_glob="output/deseq2_up.txt",
        eval_files=["deseq2_up.txt", "deseq2_down.txt"],
        wrapper_kind="commandArgs",
        paper_covered=True,
    ),
    "star_deseq2_init": TaskSpec(
        task_id="star_deseq2_init",
        workflow_id="rna-seq-star-deseq2-finish",
        family="rna",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2-init.R",
        description="DESeq2 initialisation + normalised counts (rna-seq-star-deseq2 workflow).",
        analyst_objective=(
            "You are given:\n"
            "  - `input/counts.tsv`: a tab-delimited count matrix with a first column `gene`\n"
            "    followed by one column per sample (A1, A2, A3, B1, B2, B3).\n"
            "  - `input/samples.tsv`: a samples sheet with columns `sample_name` and `condition`\n"
            "    where `A*` rows are `treated` and `B*` rows are `untreated`.\n\n"
            "Using DESeq2, build a DESeqDataSet from the count matrix with `design = ~condition`\n"
            "and the `untreated` level relevelled as the base. Call `DESeq()` on it. Write:\n"
            "  - `output/dds.rds`: the DESeq2 object produced by `saveRDS(dds, ...)`.\n"
            "  - `output/normalized_counts.tsv`: a tab-delimited table with a first column `gene`\n"
            "    and one column per sample of DESeq2 normalised counts, written with\n"
            "    `write.table(..., sep='\\t', row.names=FALSE)`.\n"
            "Drop rows whose total count <= 1 before running DESeq."
        ),
        generate_inputs=_gen_star_deseq2_init,
        run_cmd=_cmd_star_deseq2_init,
        success_glob="output/normalized_counts.tsv",
        eval_files=["normalized_counts.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
    ),
    "star_deseq2_contrast": TaskSpec(
        task_id="star_deseq2_contrast",
        workflow_id="rna-seq-star-deseq2-finish",
        family="rna",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2.R",
        description="DESeq2 contrast + lfcShrink(ashr) table (rna-seq-star-deseq2 workflow, SVG stripped).",
        analyst_objective=(
            "You are given `input/dds.rds`, a pre-built DESeq2 object (design = ~condition)\n"
            "with treated/untreated samples. The base level is `untreated`.\n\n"
            "Using DESeq2, compute results for the contrast `condition treated vs untreated`,\n"
            "apply `lfcShrink(type='ashr')`, sort by padj and write a tab-delimited table to\n"
            "`output/contrast_results.tsv` whose columns are `gene, baseMean, log2FoldChange,\n"
            "lfcSE, pvalue, padj` (as produced by `data.frame(gene=rownames(res), res)` followed\n"
            "by `write.table(..., sep='\\t', row.names=FALSE)`).\n"
            "Do NOT emit any image file — data only."
        ),
        generate_inputs=_gen_star_deseq2_contrast,
        run_cmd=_cmd_star_deseq2_contrast,
        success_glob="output/contrast_results.tsv",
        eval_files=["contrast_results.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
        patch_source=_patch_strip_svg,
    ),
    "methylkit_load": TaskSpec(
        task_id="methylkit_load",
        workflow_id="fritjoflammers-snakemake-methylanalysis-finish",
        family="methylation",
        stage="early",
        difficulty=1,
        r_script_src=_WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_load.R",
        description="methylKit::methRead of per-sample bismark coverage files (plot calls stripped).",
        analyst_objective=(
            "You are given three per-sample bismark coverage files under `input/`:\n"
            "`sampleA.bismark.cov`, `sampleB.bismark.cov`, `sampleC.bismark.cov` — tab-separated\n"
            "without headers, columns `(chrom, start, end, methylation_pct, count_methylated,\n"
            "count_unmethylated)`.\n\n"
            "Load them with `methylKit::methRead(..., pipeline='bismarkCoverage', mincov=4)`\n"
            "using `treatment = c(0, 0, 0)` and assembly `mock_v1`, then save the resulting\n"
            "methylRawList to `output/mk_raw.rds` with `saveRDS`. Use RELATIVE file paths\n"
            "(`input/sampleA.bismark.cov`, ...) so the serialised object is portable. Do not\n"
            "write any plot/PDF/SVG file."
        ),
        generate_inputs=_gen_methylkit_load,
        run_cmd=_cmd_methylkit_load,
        success_glob="output/mk_raw.rds",
        eval_files=["mk_raw.rds"],
        wrapper_kind="snakemake",
        paper_covered=True,
        patch_source=_patch_strip_methylkit_load_plots,
    ),
    "methylkit_unite": TaskSpec(
        task_id="methylkit_unite",
        workflow_id="fritjoflammers-snakemake-methylanalysis-finish",
        family="methylation",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_unite.R",
        description="methylKit::unite of per-sample bismark coverage data into a methylBase + stats TSV.",
        analyst_objective=(
            "You are given four per-sample bismark-style coverage files under `input/`:\n"
            "`sampleA.bismark.cov`, `sampleB.bismark.cov`, `sampleC.bismark.cov`,\n"
            "`sampleD.bismark.cov` — tab-separated without headers, columns\n"
            "`(chrom, start, end, methylation_pct, count_methylated, count_unmethylated)`.\n\n"
            "Load them with `methylKit::methRead(..., pipeline='bismarkCoverage', mincov=4)`,\n"
            "using `treatment = c(0, 0, 1, 1)` and assembly `mock_v1`. Then run\n"
            "`methylKit::unite(mk_raw, min.per.group=1, destrand=FALSE)` and save:\n"
            "  - `output/mk_united.rds`: the united methylBase object (`saveRDS`).\n"
            "  - `output/unite_stats.tsv`: a single-row tab-separated table with columns\n"
            "    `n_samples, n_sites, min_per_group, destrand, use_db, db_path` (`write_tsv`)."
        ),
        generate_inputs=_gen_methylkit_unite,
        run_cmd=_cmd_methylkit_unite,
        success_glob="output/unite_stats.tsv",
        eval_files=["unite_stats.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
    ),
    "methylkit_to_tibble": TaskSpec(
        task_id="methylkit_to_tibble",
        workflow_id="fritjoflammers-snakemake-methylanalysis-finish",
        family="methylation",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit2tibble.R",
        description="Convert a methylBase object to a long tibble + mean mCpG per (sample, chr).",
        analyst_objective=(
            "You are given a methylKit united object at `input/mk_united.rds`. Convert it into\n"
            "a long tibble with columns `(chr, start, end, strand, metric, value, sample)` using\n"
            "`pivot_longer` on the `coverage*`/`numCs*` columns, and save it to\n"
            "`output/df_mku.rds`. Then pivot wide on `metric`, compute `mCpG = numCs / coverage`,\n"
            "group by `(sample, chr)`, and write the mean mCpG table to `output/mean_mcpg.tsv`\n"
            "using `readr::write_tsv` with columns `sample, chr, mean_mCpG`."
        ),
        generate_inputs=_gen_methylkit_to_tibble,
        run_cmd=_cmd_methylkit_to_tibble,
        success_glob="output/mean_mcpg.tsv",
        eval_files=["mean_mcpg.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
    ),
    # =============================================================== V3 =====
    "longseq_deseq2_init": TaskSpec(
        task_id="longseq_deseq2_init",
        workflow_id="snakemake-workflows-rna-longseq-de-isoform",
        family="rna",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "snakemake-workflows__rna-longseq-de-isoform/workflow/scripts/deseq2-init.R",
        description="DESeq2 init for long-read isoform RNA-seq workflow (auto-formula from config).",
        analyst_objective=(
            "You are given `input/all_counts.tsv` (first column `Reference`, one column per\n"
            "sample) and `input/samples.tsv` (first column `sample`, plus `condition`).\n\n"
            "Using DESeq2, build a DESeqDataSet from the counts matrix, use `design = ~condition`,\n"
            "drop rows where total count <= 10, call `DESeq()`, and write\n"
            "  - `output/dds.rds`: the DESeq2 object (saveRDS)\n"
            "  - `output/normalized_counts.tsv`: columns `Reference`, then one per sample,\n"
            "    `write.table(..., sep='\\t', row.names=FALSE)`."
        ),
        generate_inputs=_gen_longseq_deseq2_init,
        run_cmd=_cmd_longseq_deseq2_init,
        success_glob="output/normalized_counts.tsv",
        eval_files=["normalized_counts.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "longseq_deseq2_contrast": TaskSpec(
        task_id="longseq_deseq2_contrast",
        workflow_id="snakemake-workflows-rna-longseq-de-isoform",
        family="rna",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "snakemake-workflows__rna-longseq-de-isoform/workflow/scripts/deseq2.R",
        description="DESeq2 contrast + lfcShrink(ashr) for long-read isoform workflow (SVG/pheatmap stripped).",
        analyst_objective=(
            "You are given `input/dds.rds` (DESeq2 object, design=~condition, base=`wt`).\n"
            "Compute `results(dds, contrast=c('condition','ko','wt'))` with `alpha=0.05`,\n"
            "apply `lfcShrink(type='ashr')`, sort by padj and write a TSV to\n"
            "`output/contrast_results.tsv` with columns `gene, baseMean, log2FoldChange, lfcSE,\n"
            "pvalue, padj` (from `data.frame(gene=rownames(res), res)`).\n"
            "Do not emit any image files — data only."
        ),
        generate_inputs=_gen_longseq_deseq2_contrast,
        run_cmd=_cmd_longseq_deseq2_contrast,
        success_glob="output/contrast_results.tsv",
        eval_files=["contrast_results.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "snakepipes_merge_fc": TaskSpec(
        task_id="snakepipes_merge_fc",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="rna",
        stage="early",
        difficulty=1,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/shared/rscripts/merge_featureCounts.R",
        description="Merge per-sample featureCounts outputs into a single TSV (snakePipes helper).",
        analyst_objective=(
            "You are given four per-sample featureCounts outputs under `input/`:\n"
            "`sampleA.counts.txt`, `sampleB.counts.txt`, `sampleC.counts.txt`,\n"
            "`sampleD.counts.txt` — tab-separated with columns\n"
            "`Geneid, Chr, Start, End, Strand, Length, <sampleBAM>`.\n\n"
            "Merge all four files by `Geneid` (outer join) into a single counts matrix whose\n"
            "rownames are `Geneid` and whose columns are the basenames (with `.counts.txt`\n"
            "stripped) of each input. Save to `output/merged_counts.tsv` using\n"
            "`write.table(..., sep='\\t', quote=F, col.names=NA)`."
        ),
        generate_inputs=_gen_snakepipes_merge_fc,
        run_cmd=_cmd_snakepipes_merge_fc,
        success_glob="output/merged_counts.tsv",
        eval_files=["merged_counts.tsv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
    ),
    "snakepipes_merge_ct": TaskSpec(
        task_id="snakepipes_merge_ct",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="rna",
        stage="early",
        difficulty=1,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/shared/rscripts/merge_count_tables.R",
        description="Merge per-sample Salmon quant.sf TPM columns into a single TSV (snakePipes helper).",
        analyst_objective=(
            "You are given four Salmon quant outputs under `input/`:\n"
            "`WT_A.quant.sf`, `WT_B.quant.sf`, `KO_A.quant.sf`, `KO_B.quant.sf` — tab-separated\n"
            "with columns `Name, Length, EffectiveLength, TPM, NumReads`.\n\n"
            "Merge on `Name` selecting the `TPM` column from each, using the first\n"
            "dot-delimited token of the basename as the sample column name. Save the merged\n"
            "matrix (with `Name` as rownames) to `output/merged_tpm.tsv` using\n"
            "`write.table(..., sep='\\t', quote=F, col.names=NA)`."
        ),
        generate_inputs=_gen_snakepipes_merge_ct,
        run_cmd=_cmd_snakepipes_merge_ct,
        success_glob="output/merged_tpm.tsv",
        eval_files=["merged_tpm.tsv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
    ),
    "riya_limma": TaskSpec(
        task_id="riya_limma",
        workflow_id="RiyaDua-cervical-cancer-snakemake-workflow",
        family="rna",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "RiyaDua__cervical-cancer-snakemake-workflow/scripts/differential_expression.R",
        description="limma topTable DE on pre-normalised expression data (volcano plot skipped via NA).",
        analyst_objective=(
            "You are given `input/exprs.csv` (pre-normalised, row = probe, column = sample)\n"
            "and `input/meta.csv` with a `group` column (`cancer` vs `normal`). Use limma\n"
            "(`lmFit` + `makeContrasts(cancer - normal)` + `eBayes`) to compute the top 250\n"
            "DE probes (`topTable(..., adjust='fdr', number=250)`) and save to\n"
            "`output/deg_results.csv` via `write.csv(...)`. Do NOT produce a volcano plot."
        ),
        generate_inputs=_gen_riya_limma,
        run_cmd=_cmd_riya_limma,
        success_glob="output/deg_results.csv",
        eval_files=["deg_results.csv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
    ),
    "chipseq_plot_macs_qc": TaskSpec(
        task_id="chipseq_plot_macs_qc",
        workflow_id="snakemake-workflows-chipseq-finish",
        family="chipseq",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "snakemake-workflows__chipseq/workflow/scripts/plot_macs_qc.R",
        description="MACS2 peak QC summary statistics (plots redirected to tempfile).",
        analyst_objective=(
            "You are given three narrowPeak files under `input/`: `sampleA_peaks.narrowPeak`,\n"
            "`sampleB_peaks.narrowPeak`, `sampleC_peaks.narrowPeak` (tab-separated, 10-col\n"
            "MACS2 narrowPeak schema).\n\n"
            "For each sample compute summary statistics on `fold`, `-log10(qvalue)`,\n"
            "`-log10(pvalue)` and peak `length`, producing rows of Min/1st Qu/Median/Mean/3rd\n"
            "Qu/Max plus `num_peaks`, `measure`, `sample`. Save the combined table to\n"
            "`output/macs_qc_summary.tsv` via\n"
            "`write.table(summary.dat, sep='\\t', row.names=FALSE, col.names=TRUE, quote=FALSE)`.\n"
            "Do not emit a PDF plot."
        ),
        generate_inputs=_gen_chipseq_plot_macs_qc,
        run_cmd=_cmd_chipseq_plot_macs_qc,
        success_glob="output/macs_qc_summary.tsv",
        eval_files=["macs_qc_summary.tsv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "chipseq_plot_homer_annot": TaskSpec(
        task_id="chipseq_plot_homer_annot",
        workflow_id="snakemake-workflows-chipseq-finish",
        family="chipseq",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "snakemake-workflows__chipseq/workflow/scripts/plot_homer_annotatepeaks.R",
        description="HOMER annotatePeaks feature summary TSV (plots redirected to tempfile).",
        analyst_objective=(
            "You are given three HOMER annotatePeaks outputs under `input/`: `sampleA_annot.txt`,\n"
            "`sampleB_annot.txt`, `sampleC_annot.txt` (tab-separated, HOMER schema). For each\n"
            "sample, aggregate feature counts by the first whitespace token of `Annotation`,\n"
            "then cast to a wide matrix (`sample` x feature). Save to\n"
            "`output/homer_annot_summary.tsv` via `write.table(..., sep='\\t', row.names=F,\n"
            "col.names=T, quote=F)`. Do not emit any PDF plot."
        ),
        generate_inputs=_gen_chipseq_plot_homer_annot,
        run_cmd=_cmd_chipseq_plot_homer_annot,
        success_glob="output/homer_annot_summary.tsv",
        eval_files=["homer_annot_summary.tsv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "snakepipes_scrna_merge_coutt": TaskSpec(
        task_id="snakepipes_scrna_merge_coutt",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="scrna",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/workflows/scRNAseq/scRNAseq_merge_coutt_files2.R",
        description="Merge per-library coutt.corrected.txt tables + cell-name TSV (snakePipes scRNA).",
        analyst_objective=(
            "You are given two per-library single-cell count tables under `input/coutt/`:\n"
            "`plate01_libA.corrected.txt` and `plate01_libB.corrected.txt` (tab-separated\n"
            "with a `GENEID` column followed by per-cell columns `X1`..`Xn`).\n\n"
            "Merge them by `GENEID` (outer join), prefixing each cell column with the library\n"
            "name and substituting `_` for the leading `X`, and write:\n"
            "  - `output/merged_coutt.tsv`: the merged GENEID × cells table (tab-sep,\n"
            "    `write.table(..., sep='\\t', col.names=T, quote=F, row.names=F)`).\n"
            "  - `output/merged_coutt.cell_names.tsv`: a cell manifest with columns\n"
            "    `sample, plate, library, cell_idx, cell_name` (tab-sep)."
        ),
        generate_inputs=_gen_snakepipes_scrna_merge_coutt,
        run_cmd=_cmd_snakepipes_scrna_merge_coutt,
        success_glob="output/merged_coutt.tsv",
        eval_files=["merged_coutt.tsv", "merged_coutt.cell_names.tsv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
    ),
    "snakepipes_scrna_qc": TaskSpec(
        task_id="snakepipes_scrna_qc",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="scrna",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/workflows/scRNAseq/scRNAseq_QC_metrics2.R",
        description="snakePipes scRNA libstats TSVs (plots skipped by omitting plot_format arg).",
        analyst_objective=(
            "You are given per-library `.cellsum` (header: `sample, cell_idx,\n"
            "READS_UNIQFEAT, UMI`) and `.libsum` (no header; 4 cols: sample, metric,\n"
            "reads, pct) files under `input/cellsum/`.\n\n"
            "For every `.libsum`, dcast on `sample × metric` using `value.var='V3'` (→\n"
            "`scqc.libstats_reads.tsv`) and `value.var='V4'` (→ `scqc.libstats_pct.tsv`).\n"
            "Write both with `sep='\\t', row.names=F, quote=F`. Produce NO plot files."
        ),
        generate_inputs=_gen_snakepipes_scrna_qc,
        run_cmd=_cmd_snakepipes_scrna_qc,
        success_glob="output/scqc.libstats_reads.tsv",
        eval_files=["scqc.libstats_reads.tsv", "scqc.libstats_pct.tsv"],
        wrapper_kind="commandArgs",
        paper_covered=False,
    ),
    "spilterlize_filter_features": TaskSpec(
        task_id="spilterlize_filter_features",
        workflow_id="epigen-spilterlize_integrate-finish",
        family="rna",
        stage="early",
        difficulty=2,
        r_script_src=_WFC / "epigen__spilterlize_integrate/workflow/scripts/filter_features.R",
        description="edgeR filterByExpr feature filtering of a counts matrix (epigen spilterlize).",
        analyst_objective=(
            "You are given `input/counts.csv` (first column is the row-name for genes; other\n"
            "columns are samples) and `input/annotation.csv` (first column row-name = sample,\n"
            "columns `group, batch`). Filter features using `edgeR::filterByExpr` with\n"
            "`group = annot$group` and write the filtered matrix to\n"
            "`output/filtered_counts.csv` via `data.table::fwrite(..., row.names=TRUE)`."
        ),
        generate_inputs=_gen_spilterlize_filter,
        run_cmd=_cmd_spilterlize_filter,
        success_glob="output/filtered_counts.csv",
        eval_files=["filtered_counts.csv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "spilterlize_norm_voom": TaskSpec(
        task_id="spilterlize_norm_voom",
        workflow_id="epigen-spilterlize_integrate-finish",
        family="rna",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "epigen__spilterlize_integrate/workflow/scripts/norm_voom.R",
        description="limma::voom normalisation (PNG plot redirected to tempfile).",
        analyst_objective=(
            "You are given `input/filtered_counts.csv` (first column row-name = gene, other\n"
            "columns samples). Run `edgeR::DGEList` → `calcNormFactors(method='TMM')` →\n"
            "`limma::voom(normalize.method='none', span=0.5, plot=TRUE)` and write the\n"
            "resulting `voom_results$E` matrix to `output/normalized_counts.csv` via\n"
            "`data.table::fwrite(..., row.names=TRUE)`. Do not persist any image file."
        ),
        generate_inputs=_gen_spilterlize_voom,
        run_cmd=_cmd_spilterlize_voom,
        success_glob="output/normalized_counts.csv",
        eval_files=["normalized_counts.csv"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "spilterlize_limma_rbe": TaskSpec(
        task_id="spilterlize_limma_rbe",
        workflow_id="epigen-spilterlize_integrate-finish",
        family="rna",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "epigen__spilterlize_integrate/workflow/scripts/limma_removeBatchEffect.R",
        description="limma::removeBatchEffect (batch + design from annotation).",
        analyst_objective=(
            "You are given `input/normalized.csv` (gene × sample log-scale data) and\n"
            "`input/annotation.csv` (sample × `group, batch`). Call\n"
            "`limma::removeBatchEffect(as.matrix(data), batch=annot$batch,\n"
            "design=model.matrix(~group, annot))` and write to\n"
            "`output/integrated_data.csv` via `data.table::fwrite(..., row.names=TRUE)`."
        ),
        generate_inputs=_gen_spilterlize_rbe,
        run_cmd=_cmd_spilterlize_rbe,
        success_glob="output/integrated_data.csv",
        eval_files=["integrated_data.csv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "spilterlize_norm_edger": TaskSpec(
        task_id="spilterlize_norm_edger",
        workflow_id="epigen-spilterlize_integrate-finish",
        family="rna",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "epigen__spilterlize_integrate/workflow/scripts/norm_edgeR.R",
        description="edgeR TMM + logCPM normalisation writing `normTMM.csv` under params$result_path/split.",
        analyst_objective=(
            "You are given `input/filtered_counts.csv` (gene × sample). Run\n"
            "`edgeR::DGEList` → `calcNormFactors(method='TMM')` → `cpm(log=TRUE,\n"
            "prior.count=3)` and save the log-CPM matrix to `output/all/normTMM.csv` via\n"
            "`data.table::fwrite(..., row.names=TRUE)`."
        ),
        generate_inputs=_gen_spilterlize_norm_edger,
        run_cmd=_cmd_spilterlize_norm_edger,
        success_glob="output/all/normTMM.csv",
        eval_files=["all/normTMM.csv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "dea_limma": TaskSpec(
        task_id="dea_limma",
        workflow_id="epigen-dea_limma-finish",
        family="rna",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "epigen__dea_limma/workflow/scripts/limma.R",
        description="limma+voom DE pipeline producing DEA table, lmfit RDS, model matrix (PDFs redirected).",
        analyst_objective=(
            "You are given `input/counts.tsv` (gene × sample) and `input/metadata.tsv`\n"
            "(first column sample_name, plus a `treatment` column with `UT`/`TR`). Run the\n"
            "epigen `dea_limma` pipeline (design=`~treatment`, TMM + voom + eBayes) and write:\n"
            "  - `output/dea_results.csv` with columns `feature, logFC, AveExpr, t, P.Value,\n"
            "    adj.P.Val, B, group` (fwrite).\n"
            "  - `output/lmfit.rds` (fitted limma `lmFit` object, via `saveRDS`).\n"
            "  - `output/model_matrix.csv` (fwrite with row.names=TRUE).\n"
            "Do not persist any image output."
        ),
        generate_inputs=_gen_dea_limma,
        run_cmd=_cmd_dea_limma,
        success_glob="output/dea_results.csv",
        eval_files=["dea_results.csv", "model_matrix.csv"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "msisensor_merge": TaskSpec(
        task_id="msisensor_merge",
        workflow_id="snakemake-workflows-msisensor-pro-finish",
        family="variant",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "snakemake-workflows__microsatellite-instability-detection-with-msisensor-pro/workflow/scripts/merge_msi_results.R",
        description="Merge per-sample MSIsensor-pro outputs into a single summary TSV.",
        analyst_objective=(
            "You are given multiple MSIsensor outputs at\n"
            "`results/msi/<sample>/msi_out.txt` (tab-separated with header:\n"
            "`Total_Number_of_Sites, Number_of_Unstable_Sites, %`). Read all of them, tag\n"
            "each row with a `group` column extracted from the path (second path component\n"
            "after `results/`), rename `Total_Number_of_Sites -> n_all_sites`,\n"
            "`Number_of_Unstable_Sites -> n_unstable_sites`, `% -> msi_score`, and write\n"
            "to `output/merged_msi.tsv` via `readr::write_tsv`."
        ),
        generate_inputs=_gen_msisensor_merge,
        run_cmd=_cmd_msisensor_merge,
        success_glob="output/merged_msi.tsv",
        eval_files=["merged_msi.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "methylkit_filt_norm": TaskSpec(
        task_id="methylkit_filt_norm",
        workflow_id="fritjoflammers-snakemake-methylanalysis-finish",
        family="methylation",
        stage="mid",
        difficulty=2,
        r_script_src=_WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_filt_norm.R",
        description="methylKit filterByCoverage + normalizeCoverage (plot_methylkit_histograms stripped).",
        analyst_objective=(
            "You are given `input/mk_raw.rds` (methylRawList, methylKit). Apply\n"
            "`filterByCoverage(lo.count=3, hi.perc=99.9)` then\n"
            "`normalizeCoverage(method='median')`; save the normalized object to\n"
            "`output/mk_filt_norm.rds` and write a per-sample stats TSV to\n"
            "`output/filt_norm_stats.tsv` (columns `sample, n_CpGs, mean_mCpG,\n"
            "mean_coverage, median_coverage`)."
        ),
        generate_inputs=_gen_methylkit_filt_norm,
        run_cmd=_cmd_methylkit_filt_norm,
        success_glob="output/filt_norm_stats.tsv",
        eval_files=["filt_norm_stats.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
        patch_source=_patch_strip_methylkit_plotfn,
    ),
    "methylkit2tibble_split": TaskSpec(
        task_id="methylkit2tibble_split",
        workflow_id="fritjoflammers-snakemake-methylanalysis-finish",
        family="methylation",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit2tibble_split.R",
        description="Concatenate multiple per-group mku2tibble RDS into a unified tibble + mean-mCpG TSV.",
        analyst_objective=(
            "You are given a list of per-group tibble RDS files in\n"
            "`snakemake@input$rds_list` (each containing a `mku2tibble`-style long-format\n"
            "tibble with columns `chr, start, ..., metric, value, sample`). Concatenate them\n"
            "and save to `output/df_mku_split.rds`. Then pivot wider on `metric`, compute\n"
            "`mCpG = numCs / coverage` (dropping `coverage==0`), group by `(sample, chr)`\n"
            "and write the mean mCpG per group to `output/mean_mcpg_split.tsv` via\n"
            "`readr::write_tsv`."
        ),
        generate_inputs=_gen_methylkit2tibble_split,
        run_cmd=_cmd_methylkit2tibble_split,
        success_glob="output/mean_mcpg_split.tsv",
        eval_files=["mean_mcpg_split.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
    ),
    "methylkit_remove_snvs": TaskSpec(
        task_id="methylkit_remove_snvs",
        workflow_id="fritjoflammers-snakemake-methylanalysis-finish",
        family="methylation",
        stage="late",
        difficulty=3,
        r_script_src=_WFC / "fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_remove_snvs.R",
        description="Anti-join an SNV exclusion bed against a united-tibble; writes stats TSV.",
        analyst_objective=(
            "You are given `input/df_united.rds` (a long-format methylKit tibble) and\n"
            "`input/exclusion.bed` (TSV: seqnames start end ref alt score). Anti-join the\n"
            "tibble against the bed (converting `start` to 1-based by `start + 1`), save the\n"
            "filtered tibble to `output/df_united_excl.rds`, and write a summary TSV at\n"
            "`output/snv_stats.tsv` with columns `dataset, n_sites` and rows `united` /\n"
            "`united_excl`."
        ),
        generate_inputs=_gen_methylkit_remove_snvs,
        run_cmd=_cmd_methylkit_remove_snvs,
        success_glob="output/snv_stats.tsv",
        eval_files=["snv_stats.tsv"],
        wrapper_kind="snakemake",
        paper_covered=True,
    ),
    "phantompeak_correlation": TaskSpec(
        task_id="phantompeak_correlation",
        workflow_id="snakemake-workflows-chipseq-finish",
        family="chipseq",
        stage="late",
        difficulty=1,
        r_script_src=_WFC / "snakemake-workflows__chipseq/workflow/scripts/phantompeak_correlation.R",
        description="Emit SPP-style cross-correlation CSV from a header + RData object.",
        analyst_objective=(
            "You are given `input/header.csv` (single line `shift,cross_correlation`) and\n"
            "`input/run_spp.RData` (contains a `crosscorr` list with data.frame slot\n"
            "`cross.correlation` of shift / correlation values). Copy the header to\n"
            "`output/crosscorr.csv`, then append the `crosscorr$cross.correlation`\n"
            "data.frame values (no header, no rownames, comma-separated)."
        ),
        generate_inputs=_gen_phantompeak,
        run_cmd=_cmd_phantompeak,
        success_glob="output/crosscorr.csv",
        eval_files=["crosscorr.csv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "nearest_gene": TaskSpec(
        task_id="nearest_gene",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="chipseq",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/shared/rscripts/nearestGene.R",
        description="Annotate CSAW differential-region bedtools-closest output with t2g + gene symbols.",
        analyst_objective=(
            "You are given `input/peaks_with_nearest.bed` (24-column bedtools-closest\n"
            "output: 18 CSAW DB columns + 6 nearest-gene columns), `input/t2g.tsv`\n"
            "(txid → gene_id), and `input/gene_symbol.tsv` (gene_id → symbol). For each\n"
            "peak, join GeneID via V22=tx and GeneSymbol via the gene_id, and save a TSV\n"
            "to `output/annotated.bed` with columns\n"
            "`Chromosome, Start, End, Width, Strand, Score, nWindows, logFC.up, logFC.down,\n"
            "PValue, FDR, direction, rep.test, rep.logFC, best.logFC, best.test, best.start,\n"
            "Name, GeneStrand, Distance, GeneID, GeneSymbol` (write.table tab-sep, no row\n"
            "names, no quotes)."
        ),
        generate_inputs=_gen_nearest_gene,
        run_cmd=_cmd_nearest_gene,
        success_glob="output/annotated.bed",
        eval_files=["annotated.bed"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    # =============================================================== V3.1 ===
    "chipseq_plot_frip_score": TaskSpec(
        task_id="chipseq_plot_frip_score",
        workflow_id="snakemake-workflows-chipseq-finish",
        family="chipseq",
        stage="late",
        difficulty=1,
        r_script_src=_WFC / "snakemake-workflows__chipseq/workflow/scripts/plot_frip_score.R",
        description="FRiP per-sample scores tibble (plots redirected, TSV emitted via wrapper).",
        analyst_objective=(
            "You are given four per-sample FRiP files under `input/` (`sampleX_control.frip.txt`),\n"
            "each a single tab-separated line `sample_control\\tfrip`.\n\n"
            "Concatenate them into a single tibble with columns `sample_control, frip`\n"
            "using `tidyverse` conventions (read the tables with `read.table(..., header=F,\n"
            "stringsAsFactors=F)` and `rbind` together). Save the resulting tibble as TSV\n"
            "at `output/frip_scores.tsv` via `readr::write_tsv`."
        ),
        generate_inputs=_gen_chipseq_plot_frip,
        run_cmd=_cmd_chipseq_plot_frip,
        success_glob="output/frip_scores.tsv",
        eval_files=["frip_scores.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "chipseq_plot_peaks_count_macs2": TaskSpec(
        task_id="chipseq_plot_peaks_count_macs2",
        workflow_id="snakemake-workflows-chipseq-finish",
        family="chipseq",
        stage="late",
        difficulty=1,
        r_script_src=_WFC / "snakemake-workflows__chipseq/workflow/scripts/plot_peaks_count_macs2.R",
        description="MACS2 per-sample peak counts tibble (plots redirected, TSV emitted via wrapper).",
        analyst_objective=(
            "You are given four per-sample peak-count files under `input/`\n"
            "(`sampleX_control.peaks_count.txt`), each a single line `sample_control\\tcount`.\n\n"
            "Read them with `read.table(..., header=F, stringsAsFactors=F)`, rbind, and save\n"
            "as a TSV at `output/peaks_count.tsv` with columns `sample_control, count`."
        ),
        generate_inputs=_gen_chipseq_plot_peaks_count,
        run_cmd=_cmd_chipseq_plot_peaks_count,
        success_glob="output/peaks_count.tsv",
        eval_files=["peaks_count.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "chipseq_plot_annotatepeaks_summary_homer": TaskSpec(
        task_id="chipseq_plot_annotatepeaks_summary_homer",
        workflow_id="snakemake-workflows-chipseq-finish",
        family="chipseq",
        stage="late",
        difficulty=1,
        r_script_src=_WFC / "snakemake-workflows__chipseq/workflow/scripts/plot_annotatepeaks_summary_homer.R",
        description="HOMER annotatePeaks summary long-format tibble (plots redirected).",
        analyst_objective=(
            "You are given `input/homer_summary.tsv` (sample × feature wide counts TSV).\n"
            "Pivot it to long format by gathering `exon, Intergenic, intron, promoter-TSS,\n"
            "TTS` into columns `sequence_element, counts` (per `tidyr::gather`-style), and\n"
            "write the resulting tibble to `output/homer_long.tsv` via `readr::write_tsv`."
        ),
        generate_inputs=_gen_chipseq_plot_annotatepeaks_summary,
        run_cmd=_cmd_chipseq_plot_annotatepeaks_summary,
        success_glob="output/homer_long.tsv",
        eval_files=["homer_long.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
    "epibtn_rpkm": TaskSpec(
        task_id="epibtn_rpkm",
        workflow_id="joncahn-epigeneticbutton-finish",
        family="rna",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "joncahn__epigeneticbutton/workflow/scripts/R_gene_expression_rpkm.R",
        description="Per-genotype RPKM table derived from featureCounts (joncahn epigeneticbutton).",
        analyst_objective=(
            "You are given `input/genecount.tsv` (featureCounts-style tab-separated table\n"
            "with a `GID` column plus 6 sample columns; rows with GID matching ^N_ must be\n"
            "dropped), `input/targets.tsv` (columns `Sample, Replicate`), and\n"
            "`input/ref_genes.bed` (headerless 6-col BED: `Chr Start Stop Name Value Strand`,\n"
            "where `Name` contains `ID=gene:<id>;...`).\n\n"
            "For each genotype (unique `Sample`), take the per-replicate columns whose names\n"
            "contain the genotype, compute `avg` across replicates, join with the reference\n"
            "gene table (on parsed `GID`), compute `RPKM = avg * 1000 / (Stop - Start)`, and\n"
            "accumulate into a single table `all_rpkm` with columns `GID, Sample, RPKM`.\n"
            "Write it to `output/results/RNA/DEG/genes_rpkm__runX__mockref.txt` via\n"
            "`write.table(..., sep='\\t', row.names=FALSE, col.names=TRUE, quote=FALSE)`."
        ),
        generate_inputs=_gen_epibtn_rpkm,
        run_cmd=_cmd_epibtn_rpkm,
        success_glob="output/results/RNA/DEG/genes_rpkm__runX__mockref.txt",
        eval_files=["results/RNA/DEG/genes_rpkm__runX__mockref.txt"],
        wrapper_kind="commandArgs",
        paper_covered=False,
    ),
    "snakepipes_scrna_report": TaskSpec(
        task_id="snakepipes_scrna_report",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="scrna",
        stage="late",
        difficulty=1,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/shared/rscripts/scRNAseq_report.R",
        description="Outer-merge per-library scRNA metric CSVs into a unified TSV report.",
        analyst_objective=(
            "You are given three single-library metric CSV files under `input/` named\n"
            "`libA.metrics.csv`, `libB.metrics.csv`, `libC.metrics.csv` (no header; two\n"
            "columns `Metric,<value>`). Each library omits a different Metric row to\n"
            "exercise outer-merge semantics.\n\n"
            "Read each file with `read.table(..., header=FALSE, sep=',', as.is=TRUE)`,\n"
            "rename columns to `Metric, <libID>` and merge them via `Reduce(function(x,y)\n"
            "merge(x,y,all=TRUE,by='Metric',sort=FALSE), ...)`. Write the merged table\n"
            "to `output/scrna_report.tsv` via `write.table(..., row.names=FALSE,\n"
            "quote=FALSE, sep='\\t')`."
        ),
        generate_inputs=_gen_snakepipes_scrna_report,
        run_cmd=_cmd_snakepipes_scrna_report,
        success_glob="output/scrna_report.tsv",
        eval_files=["scrna_report.tsv"],
        wrapper_kind="snakemake",
        paper_covered=False,
    ),
    "clean_histoneHMM": TaskSpec(
        task_id="clean_histoneHMM",
        workflow_id="maxplanck-ie-snakepipes-finish",
        family="chipseq",
        stage="late",
        difficulty=2,
        r_script_src=_WFC / "maxplanck-ie__snakePipes/snakePipes/shared/rscripts/clean_histoneHMM_result.R",
        description="Filter histoneHMM GFF outputs by avg_posterior >= 0.5 and emit GFF3/BED (plots stripped via redirect).",
        analyst_objective=(
            "You are given two histoneHMM filtered-regions GFFs under `input/`\n"
            "(`sampleA.filtered.histoneHMM-regions.gff`, `sampleB.filtered.histoneHMM-regions.gff`),\n"
            "each carrying an `avg_posterior` attribute per feature.\n\n"
            "For each input, read with `rtracklayer::import.gff`, keep features where\n"
            "`avg_posterior >= 0.5`, then:\n"
            "  - write a GFF3 file to `output/<sample>_avgp0.5.gff` via `rtracklayer::export.gff3`.\n"
            "  - set `score <- as.numeric(avg_posterior)` and write a BED file to\n"
            "    `output/<sample>_avgp0.5.bed` via `rtracklayer::export.bed`.\n"
            "Do NOT emit any image output."
        ),
        generate_inputs=_gen_clean_histoneHMM,
        run_cmd=_cmd_clean_histoneHMM,
        success_glob="output/sampleA_avgp0.5.bed",
        eval_files=["sampleA_avgp0.5.bed", "sampleB_avgp0.5.bed"],
        wrapper_kind="snakemake",
        paper_covered=False,
        patch_source=_patch_redirect_devices,
    ),
}


# --------------------------------------------------------------------------- #
# Build driver                                                                #
# --------------------------------------------------------------------------- #


def build_task(spec: TaskSpec, seed: int = 42, force: bool = False) -> dict:
    workdir = _REAL_ROOT / spec.task_id
    gtdir = _GT_ROOT / spec.task_id
    if workdir.exists() and not force:
        return {"task": spec.task_id, "status": "exists", "work_dir": str(workdir)}
    if workdir.exists() and force:
        shutil.rmtree(workdir)
    if gtdir.exists() and force:
        shutil.rmtree(gtdir)
    workdir.mkdir(parents=True)
    gtdir.mkdir(parents=True, exist_ok=True)

    (workdir / "input").mkdir(exist_ok=True)
    (workdir / "output").mkdir(exist_ok=True)
    ref_dir = gtdir / "reference"
    ref_dir.mkdir(exist_ok=True)
    eval_out = gtdir / "reference_output"
    eval_out.mkdir(parents=True, exist_ok=True)

    if not spec.r_script_src.is_file():
        raise FileNotFoundError(f"Missing source R script: {spec.r_script_src}")
    shutil.copy2(spec.r_script_src, ref_dir / "script.R")
    if spec.patch_source is not None:
        spec.patch_source(ref_dir / "script.R")

    rng = random.Random(seed)
    spec.generate_inputs(workdir, rng)

    objective = f"# Real R-task: {spec.task_id}\n\n"
    objective += f"**Pipeline provenance:** `{spec.workflow_id}` (family: `{spec.family}`, "
    objective += f"stage: `{spec.stage}`, difficulty: `{spec.difficulty}`).\n"
    objective += (
        "This workspace is derived from a real R script in the source workflow. The ground-truth\n"
        "reference output used for offline scoring lives outside this workspace and is not\n"
        "accessible to you during execution.\n\n"
    )
    objective += "## Your goal\n\n"
    objective += spec.analyst_objective + "\n\n"
    objective += "## Deliverables\n\n"
    objective += (
        f"- At least `{spec.success_glob}` must exist when you submit.\n"
        f"- Full output set expected: {', '.join(spec.eval_files)} under `output/`.\n\n"
    )
    objective += (
        "When the deliverables are in `output/`, call `submit_done(success=true)` with a short\n"
        "summary of how you solved it.\n"
    )
    (workdir / "OBJECTIVE.md").write_text(objective)

    env = os.environ.copy()
    env.setdefault("R_LIBS_USER", str(Path.home() / "Library/R/x86_64/4.5/library"))
    cmd = spec.run_cmd(workdir, gtdir)
    proc = subprocess.run(
        cmd,
        cwd=workdir,
        capture_output=True,
        text=True,
        env=env,
    )
    (ref_dir / "run.stdout.log").write_text(proc.stdout or "")
    (ref_dir / "run.stderr.log").write_text(proc.stderr or "")
    (ref_dir / "run.cmd.json").write_text(json.dumps(cmd, indent=2))
    if proc.returncode != 0:
        return {
            "task": spec.task_id,
            "status": "reference_failed",
            "returncode": proc.returncode,
            "work_dir": str(workdir),
            "gt_dir": str(gtdir),
            "stderr_tail": (proc.stderr or "").splitlines()[-20:],
        }

    produced = []
    for rel in spec.eval_files:
        p = eval_out / rel
        if p.is_file():
            produced.append(rel)
    missing = [r for r in spec.eval_files if r not in produced]

    meta = {
        "task_id": spec.task_id,
        "kind": "real",
        "workflow_id": spec.workflow_id,
        "family": spec.family,
        "stage": spec.stage,
        "difficulty": spec.difficulty,
        "paper_covered": spec.paper_covered,
        "wrapper_kind": spec.wrapper_kind,
        "description": spec.description,
        "status": "ready" if not missing else "reference_incomplete",
        "r_script_src": str(spec.r_script_src.relative_to(_REPO)) if str(spec.r_script_src).startswith(str(_REPO)) else str(spec.r_script_src),
        "ground_truth_dir": str(gtdir.relative_to(_LDP)),
        "success_glob": spec.success_glob,
        "reference_output_files": produced,
        "missing_reference_files": missing,
        "seed": seed,
    }
    (workdir / "meta.json").write_text(json.dumps(meta, indent=2))
    (gtdir / "meta.json").write_text(json.dumps(meta, indent=2))
    return {
        "task": spec.task_id,
        "status": meta["status"],
        "work_dir": str(workdir),
        "gt_dir": str(gtdir),
        "produced": produced,
        "missing": missing,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Build real R-centric tasks from source workflows")
    p.add_argument("--list", action="store_true", help="List available task specs")
    p.add_argument("--task", action="append", help="Build one task id (repeatable)")
    p.add_argument("--all", action="store_true", help="Build all tasks")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--force", action="store_true", help="Overwrite existing real-task dir")
    args = p.parse_args()

    if args.list:
        for k, v in TASKS.items():
            print(f"{k:32s} workflow={v.workflow_id:55s} family={v.family:11s} wrapper={v.wrapper_kind}")
        return 0

    targets: list[str] = []
    if args.all:
        targets = list(TASKS.keys())
    if args.task:
        targets.extend([t for t in args.task if t not in targets])
    if not targets:
        p.error("pass --list, --task TASK_ID, or --all")

    results = []
    any_fail = False
    for tid in targets:
        if tid not in TASKS:
            print(f"WARN: unknown task {tid}", file=sys.stderr)
            any_fail = True
            continue
        res = build_task(TASKS[tid], seed=args.seed, force=args.force)
        results.append(res)
        print(json.dumps(res, indent=2))
        if res["status"] not in ("ready", "exists"):
            any_fail = True

    summary = _REAL_ROOT / "_build_summary.json"
    _REAL_ROOT.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps({"results": results}, indent=2))
    print(f"\nSummary written to: {summary}")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
