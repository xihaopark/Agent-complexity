configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bcftools_concat"


rule all:
  input:
    "results/finish/bcftools_concat.done"


rule run_bcftools_concat:
  output:
    "results/finish/bcftools_concat.done"
  run:
    run_step(STEP_ID, output[0])
