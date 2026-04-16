from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["link_bam", "samtools_index_external", "link_bam_bai_external", "sambamba_flagstat", "bamCoverage", "bamCoverage_filtered", "plotCoverage", "multiBamSummary", "plotCorrelation_pearson", "plotCorrelation_spearman", "plotPCA", "estimate_read_filtering", "computeGCBias", "bamPE_fragment_size", "bamcoverage_short_cleaned", "multiQC", "filterFragments", "filterCoveragePerScaffolds", "callOpenChromatin", "tempChromSizes", "HMMRATAC_peaks", "namesort_bams", "Genrich_peaks", "plotFingerprint", "plotFingerprint_allelic", "MACS2_peak_qc", "CSAW", "calc_matrix_log2r_CSAW", "plot_heatmap_log2r_CSAW", "calc_matrix_cov_CSAW", "plot_heatmap_cov_CSAW", "CSAW_report", "get_nearest_transcript", "get_nearest_gene", "split_sampleSheet", "filter_gtf", "gtf_to_files", "annotation_bed2fasta", "all"]


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
