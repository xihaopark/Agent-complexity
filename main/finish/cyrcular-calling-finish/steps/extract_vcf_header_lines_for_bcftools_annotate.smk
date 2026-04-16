configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_vcf_header_lines_for_bcftools_annotate"


rule all:
  input:
    "results/finish/extract_vcf_header_lines_for_bcftools_annotate.done"


rule run_extract_vcf_header_lines_for_bcftools_annotate:
  output:
    "results/finish/extract_vcf_header_lines_for_bcftools_annotate.done"
  run:
    run_step(STEP_ID, output[0])
