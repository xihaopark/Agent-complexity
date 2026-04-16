configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "coverage_combined"


rule all:
  input:
    "results/finish/coverage_combined.done"


rule run_coverage_combined:
  output:
    "results/finish/coverage_combined.done"
  run:
    run_step(STEP_ID, output[0])
