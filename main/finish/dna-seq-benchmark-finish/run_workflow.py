from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["eval", "norm_vcf", "index_vcf", "index_bcf", "sort_vcf", "get_reads", "get_archive", "get_truth", "rename_truth_contigs", "merge_truthsets", "normalize_truth", "get_confidence_bed", "get_liftover_track", "get_target_bed", "postprocess_target_bed", "get_reference", "get_liftover_chain", "samtools_faidx", "bwa_index", "bwa_mem", "mark_duplicates", "samtools_index", "mosdepth", "stratify_regions", "get_reference_dict", "merge_callsets", "liftover_callset", "rename_contigs", "add_format_field", "remove_non_pass", "intersect_calls_with_target_regions", "restrict_to_reference_contigs", "normalize_calls", "stratify_truth", "stratify_results", "index_stratified_truth", "stat_truth", "generate_sdf", "benchmark_variants_germline", "benchmark_variants_somatic", "extract_fp_fn", "extract_fp_fn_tp", "reformat_fp_fn_tp_tables", "calc_precision_recall", "collect_stratifications", "collect_precision_recall", "report_precision_recall", "collect_fp_fn", "collect_stratifications_fp_fn", "collect_fp_fn_benchmark", "filter_shared_fn", "filter_unique", "write_shared_fn_vcf", "write_unique_fn_vcf", "write_unique_fp_vcf", "report_fp_fn", "report_fp_fn_callset", "get_downsampled_vep_cache", "get_vep_cache", "get_vep_plugins", "download_revel", "process_revel_scores", "tabix_revel_scores", "annotate_shared_fn", "annotate_unique_fp_fn", "vembrane_table_shared_fn", "vembrane_table_unique_fp_fn", "all"]


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
