configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_vcf"


rule all:
  input:
    "results/finish/create_vcf.done"


rule run_create_vcf:
  output:
    "results/finish/create_vcf.done"
  run:
    run_step(STEP_ID, output[0])
