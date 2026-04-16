configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "salmon_index"


rule all:
  input:
    "results/finish/salmon_index.done"


rule run_salmon_index:
  output:
    "results/finish/salmon_index.done"
  run:
    run_step(STEP_ID, output[0])
