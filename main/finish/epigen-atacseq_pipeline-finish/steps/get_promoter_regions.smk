configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_promoter_regions"


rule all:
  input:
    "results/finish/get_promoter_regions.done"


rule run_get_promoter_regions:
  output:
    "results/finish/get_promoter_regions.done"
  run:
    run_step(STEP_ID, output[0])
