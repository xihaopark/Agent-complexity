configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "norm_vcf"


rule all:
  input:
    "results/finish/norm_vcf.done"


rule run_norm_vcf:
  output:
    "results/finish/norm_vcf.done"
  run:
    run_step(STEP_ID, output[0])
