configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_vcf"


rule all:
  input:
    "results/finish/filter_vcf.done"


rule run_filter_vcf:
  output:
    "results/finish/filter_vcf.done"
  run:
    run_step(STEP_ID, output[0])
