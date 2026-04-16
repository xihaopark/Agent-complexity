configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiBamSummary"


rule all:
  input:
    "results/finish/multiBamSummary.done"


rule run_multiBamSummary:
  output:
    "results/finish/multiBamSummary.done"
  run:
    run_step(STEP_ID, output[0])
