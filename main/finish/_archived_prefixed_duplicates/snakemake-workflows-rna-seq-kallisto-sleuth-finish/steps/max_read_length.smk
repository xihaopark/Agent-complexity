configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "max_read_length"


rule all:
  input:
    "results/finish/max_read_length.done"


rule run_max_read_length:
  output:
    "results/finish/max_read_length.done"
  run:
    run_step(STEP_ID, output[0])
