from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["map_only", "coverage_chip", "combined_analysis", "prepare_reference", "check_fasta", "check_gff", "check_gtf", "check_chrom_sizes", "prep_region_file", "check_te_file", "get_fastq_pe", "get_fastq_se", "run_fastqc", "process_fastq_pe", "process_fastq_se", "get_available_bam", "make_bt2_indices", "bowtie2_map_pe", "bowtie2_map_se", "filter_chip_pe", "filter_chip_se", "make_chip_stats_pe", "make_chip_stats_se", "pe_or_se_chip_dispatch", "make_coverage_chip", "make_bigwig_chip", "make_fingerprint_plot", "calling_peaks_macs2_pe", "calling_peaks_macs2_se", "idr_analysis_replicates", "merging_chip_replicates", "making_pseudo_replicates", "create_empty_file", "best_peaks_pseudoreps", "make_peak_stats", "find_motifs_in_file", "perform_pairwise_diff_peaks", "all_chip", "atac_shift_bam", "atac_bam_to_bed", "calling_peaks_atac", "make_coverage_atac", "all_atac", "make_STAR_indices", "STAR_map_pe", "STAR_map_se", "filter_rna_pe", "filter_rna_se", "make_rna_stats_pe", "make_rna_stats_se", "pe_or_se_rna_dispatch", "merging_rna_replicates", "make_rna_stranded_bigwigs", "make_rna_unstranded_bigwigs", "prep_files_for_DEGs", "call_all_DEGs", "gather_gene_expression_rpkm", "plot_expression_levels", "create_GO_database", "perform_GO_on_target_file", "call_rampage_TSS", "all_rna", "make_bismark_indices", "bismark_map_pe", "bismark_map_se", "pe_or_se_mc_dispatch", "make_mc_stats_pe", "make_mc_stats_se", "merging_mc_replicates", "make_mc_bigwig_files", "call_DMRs_pairwise", "all_mc", "download_modkit", "get_dmc_input", "dmc_input_checkpoint", "prepare_modbam_for_pileup", "modkit_pileup_dmc", "copy_bedmethyl_input", "merge_pileup_sources", "modkit_summary_dmc", "make_mc_stats_dmc", "convert_bedmethyl_to_cx_report", "deduplicate_srna_nextflexv3", "make_bt2_indices_for_structural_RNAs", "filter_structural_rna", "dispatch_srna_fastq", "make_bowtie1_indices", "make_bowtie1_indices_large", "shortstack_map", "make_cluster_bedfiles", "make_srna_size_stats", "filter_size_srna_sample", "merging_srna_replicates", "make_srna_stranded_bigwigs", "analyze_all_srna_samples_on_target_file", "prep_files_for_differential_srna_clusters", "call_all_differential_srna_clusters", "all_srna", "has_header", "is_stranded", "prepping_mapping_stats", "plotting_mapping_stats", "prepping_chip_peak_stats", "plotting_peaks_stats_chip_tf", "prepping_srna_sizes_stats", "plotting_srna_sizes_stats", "combine_clusterfiles", "combine_peakfiles", "combine_TSS", "get_annotations_for_bedfile", "plotting_upset_regions", "making_stranded_matrix_on_targetfile", "merging_matrix", "computing_matrix_scales", "plotting_heatmap_on_targetfile", "sort_heatmap", "plotting_sorted_heatmap_on_targetfile", "plotting_profile_on_targetfile", "prep_chromosomes_for_browser", "prep_browser_on_region", "make_single_loci_browser_plot", "merge_region_browser_plots", "summarize_tracks_pca", "plot_PCA_correlation", "all_combined", "all"]


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
