configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "normalization"


rule all:
  input:
    "results/finish/normalization.done"


rule run_normalization:
  output:
    "results/finish/normalization.done"
  run:
    run_step(STEP_ID, output[0])
