from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["fastp_se", "fastp_pe", "max_read_length", "get_aligned_pos", "get_selected_transcripts_aligned_read_bins", "get_selected_transcripts_sample_QC_histogram", "get_sample_QC_histogram", "get_transcriptome", "get_annotation", "get_transcript_info", "get_pfam", "convert_pfam", "calculate_cpat_hexamers", "calculate_cpat_logit_model", "get_spia_db", "cds_polyA_T_removal", "get_main_transcripts_fasta", "kallisto_long_index", "kallisto_long_bus", "bustools_sort", "bustools_count", "kallisto_long_quant_tcc", "kallisto_index", "kallisto_quant", "bwa_index", "bwa_mem", "get_only_main_transcript_reads_closest_to_3_prime", "get_main_transcript_fastq", "kallisto_3prime_index", "kallisto_3prime_quant", "kallisto_samtools_sort", "kallisto_samtools_index", "compose_sample_sheet", "sleuth_init", "sleuth_diffexp", "ihw_fdr_control", "plot_bootstrap", "prepare_pca", "plot_pca", "plot_diffexp_pval_hist", "logcount_matrix", "tpm_matrix", "plot_diffexp_heatmap", "plot_group_density", "plot_scatter", "plot_fragment_length_dist", "plot_vars", "vega_volcano_plot", "init_isoform_switch", "calculate_protein_domains", "calculate_coding_potential", "annotate_isoform_switch", "spia", "fgsea", "fgsea_plot_gene_sets", "ens_gene_to_go", "download_go_obo", "goatools_go_enrichment", "postprocess_go_enrichment", "postprocess_diffexp", "postprocess_tpm_matrix", "plot_enrichment_scatter", "plot_pathway_scatter", "spia_datavzrd", "diffexp_datavzrd", "go_enrichment_datavzrd", "meta_compare_datavzrd", "inputs_datavzrd", "bam_paired_to_fastq", "bam_single_to_fastq", "meta_compare_diffexp", "meta_compare_enrichment", "meta_compare_pathways", "all"]


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
