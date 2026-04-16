from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["utils_index_BAM", "BC_copy_barcode_map", "BC_get_simple_whitelist", "BC_write_whitelist_variants", "ilmn_1a_merge_fastqs", "ilmn_1b_cutadapt", "ilmn_1b_cutadapt2", "ilmn_1b_R1_hardTrimming", "ilmn_1b_R1_internalTrimming", "ilmn_1c_fastq_call_bc_from_adapter", "ilmn_1c_filter_barcodes", "ilmn_1c_tsv_bc_correction", "ilmn_1c_summarize_bc_correction", "ilmn_2a_extract_rRNA_fasta", "ilmn_2a_build_rRNA_gtf", "ilmn_2a_build_rRNA_bwa_index", "ilmn_2a_bwa_rRNA_align", "ilmn_2a_bwa_rRNA_get_no_rRNA_list", "ilmn_2a_bwa_rRNA_filter_R1", "ilmn_2a_bwa_rRNA_filter_trimmed_R1", "ilmn_2a_bwa_rRNA_compress_unmapped", "ilmn_2a_bwa_rRNA_filtered_fastqc", "ilmn_2b_ribodetector", "ilmn_2b_ribodetector_get_no_rRNA_list", "ilmn_2b_ribodetector_filter_R1", "ilmn_2b_ribodetector_filter_trimmed_R1", "ilmn_2b_ribodetector_compress_fqs", "ilmn_2c_qualimapQC_rRNA_bwa", "ilmn_2c_qualimap_readqc_summary2csv_rRNA_bwa", "ilmn_2c_qualimap_bamqc_rRNA_bwa", "ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa", "ilmn_3a_STARsolo_firstPass", "ilmn_3a_STARsolo_secondPass", "ilmn_3a_compress_STAR_outs", "ilmn_3a_cache_seurat_STAR", "ilmn_3a_cache_h5ad_STAR", "ilmn_3b_fastqc_unmapped", "ilmn_3c_strand_split_bam", "ilmn_3c_umitools_dedup_fwdBAM", "ilmn_3c_umitools_dedup_revBAM", "ilmn_3c_merge_dedup_bam", "ilmn_3q_qualimapQC_STAR", "ilmn_3q_qualimapQC_dedup_STAR", "ilmn_3q_qualimap_rnaseq_summary2csv_STAR", "ilmn_3q_qualimap_bamqc_STAR_raw", "ilmn_3q_qualimap_bamqc_STAR_dedup", "ilmn_3q_qualimap_bamqc_summary2csv_STAR", "ilmn_3u_filter_noGN", "ilmn_3u_calcHMMbed", "ilmn_3u_filter_out_aTARs", "ilmn_3u_bed_to_gtf", "ilmn_3u_tagReads", "ilmn_3u_sort_index_tagged_bam", "ilmn_3u_extract_HMM_expression", "ilmn_3u_counts_long2mtx", "ilmn_3u_gzip_counts", "ilmn_3u_plot_qc", "ilmn_4a_kbpython_std", "ilmn_4a_kbpython_std_remove_suffix", "ilmn_4a_kbpython_std_compress_outs", "ilmn_4a_cache_seurat_kbpython_std", "ilmn_4a_cache_h5ad_kbpython_std", "ilmn_5a_copy_R2_fq_for_mirge", "ilmn_5a_miRge3_pseudobulk", "ilmn_7a_fastQC_preTrim", "ilmn_7a_fastQC_postTrim", "ilmn_7a_fastQC_twiceTrim", "ilmn_7b_readQC_0_rawInput", "ilmn_7b_readQC_1_preCutadapt", "ilmn_7b_readQC_2_postCutadapt", "ilmn_7b_readQC_3_twiceCutadapt", "ilmn_7b_readQC_3_bam", "ilmn_7b_readQC_downsample", "ilmn_7b_readQC_summaryplot", "ilmn_7b_readQC_compress", "ont_1a_merge_formats", "ont_1a_call_adapter_scan", "ont_1a_readIDs_by_adapter_type", "ont_1a_adapter_scan_summary", "ont_1a_merge_scan_lists", "ont_1a_subset_fastq_by_adapter_type", "ont_1a_compress_merged_fq", "ont_1a_split_fastq_to_R1_R2", "ont_1b_cutadapt", "ont_1b_R1_hardTrimming", "ont_1b_R1_internalTrim", "ont_1b_cutadapt_internalTrimming", "ont_1b_cutadapt_summary", "ont_1c_fastq_call_bc_from_adapter", "ont_1c_filter_barcodes", "ont_1c_tsv_bc_correction", "ont_1c_summarize_bc_correction", "ont_2a_generate_junction_bed", "ont_2a_align_minimap2_genome", "ont_2a_sort_compress_output", "ont_2a_add_corrected_barcodes", "ont_2a_add_umis", "ont_2a_filter_bam_empty_tags", "ont_2a_featureCounts", "ont_2a_add_featureCounts_to_bam", "ont_2a_split_bam_by_strand", "ont_2a_umitools_count", "ont_2a_counts_to_sparse", "ont_2a_cache_h5ad", "ont_2a_cache_seurat", "ont_2b_txome_align_minimap2_transcriptome", "ont_2b_txome_add_corrected_barcodes", "ont_2b_txome_add_umis", "ont_2b_txome_filter_bam_empty_tags", "ont_2b_txome_dedup_by_xb", "ont_2b_txome_sort_by_xb", "ont_2b_txome_oarfish_quant", "ont_2b_txome_compress_oarfish_matrix", "ont_2b_txome_cache_h5ad_minimap2", "ont_2b_txome_cache_seurat_minimap2", "ont_1f_sort_gtf", "ont_2d_ultra_pipeline_genome", "ont_2d_ultra_sort_compress_output", "ont_2d_ultra_add_corrected_barcodes", "ont_2d_ultra_add_umis", "ont_2d_ultra_filter_bam_empty_tags", "ont_2d_ultra_featureCounts", "ont_2d_ultra_add_featureCounts_to_bam", "ont_2d_ultra_umitools_count", "ont_2d_ultra_counts_to_sparse", "ont_2d_ultra_cache_h5ad", "ont_2d_ultra_cache_seurat", "ont_2e_isoquant", "ont_2e_add_isoquant_genes_to_bam", "ont_2e_add_isoquant_transcripts_to_bam", "ont_2e_umitools_count", "ont_2e_counts_to_sparse", "ont_2e_cache_h5ad", "ont_2e_cache_seurat", "ont_3a_readQC_0_rawInput", "ont_3a_readQC_1_preCutadapt", "ont_3a_readQC_2_postCutadapt", "ont_3a_readQC_3_bam", "ont_3a_readQC_downsample", "ont_3a_readQC_summaryplot", "ont_3a_readQC_compress", "ont_3b_qualimap", "ont_3b_qualimap_readqc_summary2csv", "ont_3b_qualimap_bamqc", "ont_3b_qualimap_bamqc_summary2csv", "all"]


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
