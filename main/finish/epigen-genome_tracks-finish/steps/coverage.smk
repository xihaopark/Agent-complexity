configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "coverage"


rule all:
  input:
    "results/finish/coverage.done"


rule run_coverage:
  output:
    "results/finish/coverage.done"
  run:
    run_step(STEP_ID, output[0])
