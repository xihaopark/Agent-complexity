from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = ["bcf_index", "bam_index", "tabix_known_variants", "gzip_fastq", "tsv_to_excel", "get_sra", "cutadapt_pipe", "cutadapt_pe", "cutadapt_se", "merge_fastqs", "get_genome", "get_cdna", "kallisto_index", "get_annotation", "STAR_index", "split_annotation", "genome_faidx", "genome_dict", "get_callregions", "get_known_variants", "remove_iupac_codes", "bwa_index", "download_HLALA_graph", "index_HLALA", "get_vep_cache", "get_vep_plugins", "make_sampleheader", "map_reads", "mark_duplicates", "recalibrate_base_qualities", "apply_bqsr", "strelka_somatic", "strelka_germline", "vcf_to_bcf", "concat_somatic", "get_tumor_from_somatic", "reheader_germline", "concat_variants", "preprocess_variants", "norm_vcf", "freebayes", "scatter_candidates", "render_scenario", "varlociraptor_preprocess", "varlociraptor_call", "sort_calls", "bcftools_concat", "annotate_variants", "annotate_strelka_variants", "filter_by_annotation", "filter_odds", "gather_calls", "control_fdr", "merge_calls", "change_samplenames", "reheader_varlociraptor", "microphaser_somatic", "microphaser_germline", "concat_proteome", "build_germline_proteome", "microphaser_filter", "concat_tsvs", "HLA_LA", "parse_HLA_LA", "razers3", "bam2fq", "OptiType", "parse_Optitype", "netMHCpan", "netMHCIIpan", "parse_mhc_out", "mhc_csv_table", "add_RNA_info", "kallisto_quant", "STAR_align", "arriba", "estimate_tmb", "vg2svg", "all"]


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
