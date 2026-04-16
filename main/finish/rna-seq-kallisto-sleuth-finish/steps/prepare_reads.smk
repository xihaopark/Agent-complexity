configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_reads"


rule all:
  input:
    "results/finish/prepare_reads.done"


rule run_prepare_reads:
  output:
    "results/finish/prepare_reads.done"
  run:
    run_step(STEP_ID, output[0])
