configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bwa_alignment"


rule all:
  input:
    "results/finish/bwa_alignment.done"


rule run_bwa_alignment:
  output:
    "results/finish/bwa_alignment.done"
  run:
    run_step(STEP_ID, output[0])
