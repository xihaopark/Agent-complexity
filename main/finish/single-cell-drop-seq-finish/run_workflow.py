from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["download_meta", "qc", "filter", "map", "extract", "split_species", "extract_species", "merge", "make_report", "download_annotation", "download_genome", "rename_genome", "merge_genomes", "merge_annotations", "curate_annotation", "create_dict", "reduce_gtf", "create_refFlat", "create_intervals", "get_genomeChrBinNbits", "prep_star_index", "create_star_index", "fastqc_barcodes", "fastqc_reads", "multiqc_fastqc_barcodes", "multiqc_fastqc_reads", "fasta_fastq_adapter", "cutadapt_R1", "cutadapt_R2", "clean_cutadapt", "repair", "detect_barcodes", "plot_adapter_content", "multiqc_cutadapt_barcodes", "multiqc_cutadapt_RNA", "extend_barcode_whitelist", "get_top_barcodes", "get_cell_whitelist", "extend_barcode_top", "repair_barcodes", "STAR_align", "multiqc_star", "pigz_unmapped", "MergeBamAlignment", "TagReadWithGeneExon", "DetectBeadSubstitutionErrors", "bead_errors_metrics", "bam_hist", "plot_yield", "plot_knee_plot", "extract_umi_expression", "extract_reads_expression", "SingleCellRnaSeqMetricsCollector", "plot_rna_metrics", "convert_long_to_mtx", "compress_mtx", "split_bam_species", "extract_all_umi_expression", "plot_barnyard", "extract_umi_expression_species", "extract_reads_expression_species", "convert_long_to_mtx_species", "compress_mtx_species", "SingleCellRnaSeqMetricsCollector_species", "plot_rna_metrics_species", "merge_long", "violine_plots", "summary_stats", "create_publication_text", "all"]


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
