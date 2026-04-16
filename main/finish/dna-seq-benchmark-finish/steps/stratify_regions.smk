configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "stratify_regions"


rule all:
  input:
    "results/finish/stratify_regions.done"


rule run_stratify_regions:
  output:
    "results/finish/stratify_regions.done"
  run:
    run_step(STEP_ID, output[0])
