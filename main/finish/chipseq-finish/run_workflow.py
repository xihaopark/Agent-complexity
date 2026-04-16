from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["get_genome", "get_annotation", "sra_get_fastq_pe", "sra_get_fastq_se", "gtf2bed", "genome_faidx", "bwa_index", "chromosome_size", "generate_igenomes", "generate_igenomes_blacklist", "bedtools_sort_blacklist", "bedtools_complement_blacklist", "get_gsize", "fastqc", "multiqc", "cutadapt_pe", "cutadapt_se", "bwa_mem", "merge_bams", "mark_merged_duplicates", "samtools_view_filter", "bamtools_filter_json", "samtools_sort", "orphan_remove", "samtools_sort_pe", "merge_se_pe", "samtools_flagstat", "samtools_idxstats", "samtools_stats", "samtools_index", "preseq_lc_extrap", "collect_multiple_metrics", "genomecov", "sort_genomecov", "bedGraphToBigWig", "create_igv_bigwig", "compute_matrix", "plot_profile", "plot_heatmap", "phantompeakqualtools", "phantompeak_correlation", "phantompeak_multiqc", "plot_fingerprint", "macs2_callpeak_broad", "macs2_callpeak_narrow", "peaks_count", "sm_report_peaks_count_plot", "bedtools_intersect", "frip_score", "sm_rep_frip_score", "create_igv_peaks", "homer_annotatepeaks", "plot_macs_qc", "plot_homer_annotatepeaks", "plot_sum_annotatepeaks", "bedtools_merge_broad", "bedtools_merge_narrow", "macs2_merged_expand", "create_consensus_bed", "create_consensus_saf", "plot_peak_intersect", "create_consensus_igv", "homer_consensus_annotatepeaks", "trim_homer_consensus_annotatepeaks", "merge_bool_and_annotatepeaks", "feature_counts", "featurecounts_modified_colnames", "featurecounts_deseq2", "create_deseq2_igv", "all"]


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
