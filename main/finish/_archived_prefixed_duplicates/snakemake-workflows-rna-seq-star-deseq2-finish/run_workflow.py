from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["get_genome", "get_annotation", "genome_faidx", "bwa_index", "star_index", "get_sra", "fastp_se", "fastp_pe", "rseqc_gtf2bed", "rseqc_junction_annotation", "rseqc_junction_saturation", "rseqc_stat", "rseqc_infer", "rseqc_innerdis", "rseqc_readdis", "rseqc_readdup", "rseqc_readgc", "multiqc", "star_align", "count_matrix", "gene_2_symbol", "deseq2_init", "pca", "deseq2", "all"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cores", default="8")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-step")
    parser.add_argument("--to-step")
    return parser.parse_args()


def pick_steps(start: str | None, end: str | None) -> list[str]:
    start_index = STEPS.index(start) if start else 0
    end_index = STEPS.index(end) + 1 if end else len(STEPS)
    if start_index >= end_index:
        raise ValueError("from-step must be earlier than or equal to to-step")
    return STEPS[start_index:end_index]


def main() -> int:
    args = parse_args()
    for step_id in pick_steps(args.from_step, args.to_step):
        command = [
            sys.executable,
            "-m",
            "snakemake",
            "-s",
            f"steps/{step_id}.smk",
            "--configfile",
            "config_basic/config.yaml",
            "--cores",
            args.cores,
        ]
        if args.dry_run:
            command.append("-n")
        print(f"== {step_id} ==")
        print(" ".join(command))
        proc = subprocess.run(command, cwd=ROOT)
        if proc.returncode != 0:
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
