configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "coverage_upstream_downstream"


rule all:
  input:
    "results/finish/coverage_upstream_downstream.done"


rule run_coverage_upstream_downstream:
  output:
    "results/finish/coverage_upstream_downstream.done"
  run:
    run_step(STEP_ID, output[0])
