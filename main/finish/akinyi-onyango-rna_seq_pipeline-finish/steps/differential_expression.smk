configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "differential_expression"


rule all:
  input:
    "results/finish/differential_expression.done"


rule run_differential_expression:
  output:
    "results/finish/differential_expression.done"
  run:
    run_step(STEP_ID, output[0])
