from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["bam_index", "tabix_known_variants", "get_genome", "genome_faidx", "genome_dict", "get_known_variants", "remove_iupac_codes", "bwa_index", "get_pangenome", "get_sra", "fastp_pipe", "fastp_se", "fastp_pe", "merge_trimmed_fastqs", "map_reads_bwa", "count_sample_kmers", "create_reference_paths", "map_reads_vg", "reheader_mapped_reads", "fix_mate", "add_read_group", "sort_alignments", "annotate_umis", "mark_duplicates", "calc_consensus_reads", "map_consensus_reads", "merge_consensus_reads", "sort_consensus_reads", "recalibrate_base_qualities", "apply_bqsr", "assign_primers", "filter_primerless_reads", "trim_primers", "map_primers", "filter_unmapped_primers", "primer_to_bed", "build_primer_regions", "all"]


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
