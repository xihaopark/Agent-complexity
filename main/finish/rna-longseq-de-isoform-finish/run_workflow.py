from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["sample_qa_plot", "total_sample_qa_plot", "alignment_qa", "alignment_qa_report", "bam_stats", "download_ncbi_genome", "download_ncbi_annotation", "download_ensembl_genome", "download_ensembl_annotation", "get_genome", "get_annotation", "standardize_gff", "genome_to_transcriptome", "correct_transcriptome", "filter_reads", "build_minimap_index", "map_reads", "sam_to_bam", "bam_sort", "bam_index", "count_reads", "merge_read_counts", "transcriptid_to_gene", "deseq2_init", "deseq2", "pca", "reads_manifest", "gff_to_gtf", "bam_to_bed", "concatenate_beds", "build_flair_genome_index", "flair_align", "flair_correct", "flair_collapse", "flair_quantify", "flair_diffexp", "flair_plot_isoforms", "iso_analysis_report", "get_indexed_protein_db", "generate_gene_query", "lambda_gene_annotation", "get_protein_names", "all"]


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
