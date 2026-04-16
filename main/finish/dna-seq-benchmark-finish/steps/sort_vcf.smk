configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_vcf"


rule all:
  input:
    "results/finish/sort_vcf.done"


rule run_sort_vcf:
  output:
    "results/finish/sort_vcf.done"
  run:
    run_step(STEP_ID, output[0])
