configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotCoverage"


rule all:
  input:
    "results/finish/plotCoverage.done"


rule run_plotCoverage:
  output:
    "results/finish/plotCoverage.done"
  run:
    run_step(STEP_ID, output[0])
