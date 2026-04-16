configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_reads"


rule all:
  input:
    "results/finish/get_reads.done"


rule run_get_reads:
  output:
    "results/finish/get_reads.done"
  run:
    run_step(STEP_ID, output[0])
