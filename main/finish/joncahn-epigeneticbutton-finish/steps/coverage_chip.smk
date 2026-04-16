configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "coverage_chip"


rule all:
  input:
    "results/finish/coverage_chip.done"


rule run_coverage_chip:
  output:
    "results/finish/coverage_chip.done"
  run:
    run_step(STEP_ID, output[0])
