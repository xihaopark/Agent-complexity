configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "index_vcf"


rule all:
  input:
    "results/finish/index_vcf.done"


rule run_index_vcf:
  output:
    "results/finish/index_vcf.done"
  run:
    run_step(STEP_ID, output[0])
