from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["get_genome", "genome_faidx", "minimap2_index", "download_regulatory_annotation", "download_repeatmasker_annotation", "download_gene_annotation", "minimap2_bam", "merge_fastqs", "samtools_index", "samtools_faidx", "bcf_index", "bcftools_concat", "bcftools_sort", "varlociraptor_call", "varlociraptor_alignment_properties", "varlociraptor_preprocess", "scatter_candidates", "sort_bnd_bcfs", "circle_bnds", "cyrcular_generate_tables", "cyrcular_annotate_graph", "reheader_filtered_bcf", "sort_bcf_header", "get_bcf_header", "extract_vcf_header_lines_for_bcftools_annotate", "filter_overview_table", "filter_varlociraptor", "circle_coverage_plot", "circle_graph_plots", "render_datavzrd_config", "copy_qc_plots_for_datavzrd", "copy_graph_plots_for_datavzrd", "datavzrd_circle_calls", "all"]


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
