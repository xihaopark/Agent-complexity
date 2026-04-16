configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_region_file"


rule all:
  input:
    "results/finish/prep_region_file.done"


rule run_prep_region_file:
  output:
    "results/finish/prep_region_file.done"
  run:
    run_step(STEP_ID, output[0])
