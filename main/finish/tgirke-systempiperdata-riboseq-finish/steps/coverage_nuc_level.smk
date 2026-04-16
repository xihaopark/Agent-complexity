configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "coverage_nuc_level"


rule all:
  input:
    "results/finish/coverage_nuc_level.done"


rule run_coverage_nuc_level:
  output:
    "results/finish/coverage_nuc_level.done"
  run:
    run_step(STEP_ID, output[0])
