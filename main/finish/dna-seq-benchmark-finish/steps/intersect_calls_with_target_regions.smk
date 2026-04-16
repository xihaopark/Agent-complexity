configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "intersect_calls_with_target_regions"


rule all:
  input:
    "results/finish/intersect_calls_with_target_regions.done"


rule run_intersect_calls_with_target_regions:
  output:
    "results/finish/intersect_calls_with_target_regions.done"
  run:
    run_step(STEP_ID, output[0])
