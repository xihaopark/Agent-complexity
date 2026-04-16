configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "correlation"


rule all:
  input:
    "results/finish/correlation.done"


rule run_correlation:
  output:
    "results/finish/correlation.done"
  run:
    run_step(STEP_ID, output[0])
