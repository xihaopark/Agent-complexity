configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bwa_index"


rule all:
  input:
    "results/finish/bwa_index.done"


rule run_bwa_index:
  output:
    "results/finish/bwa_index.done"
  run:
    run_step(STEP_ID, output[0])
