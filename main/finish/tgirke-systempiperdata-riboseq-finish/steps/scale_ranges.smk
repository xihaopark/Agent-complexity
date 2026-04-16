configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "scale_ranges"


rule all:
  input:
    "results/finish/scale_ranges.done"


rule run_scale_ranges:
  output:
    "results/finish/scale_ranges.done"
  run:
    run_step(STEP_ID, output[0])
