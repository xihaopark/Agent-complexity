configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "chromosome_size"


rule all:
  input:
    "results/finish/chromosome_size.done"


rule run_chromosome_size:
  output:
    "results/finish/chromosome_size.done"
  run:
    run_step(STEP_ID, output[0])
