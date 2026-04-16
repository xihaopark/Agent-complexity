configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quantification"


rule all:
  input:
    "results/finish/quantification.done"


rule run_quantification:
  output:
    "results/finish/quantification.done"
  run:
    run_step(STEP_ID, output[0])
