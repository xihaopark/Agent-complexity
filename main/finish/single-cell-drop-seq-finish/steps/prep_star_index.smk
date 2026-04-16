configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_star_index"


rule all:
  input:
    "results/finish/prep_star_index.done"


rule run_prep_star_index:
  output:
    "results/finish/prep_star_index.done"
  run:
    run_step(STEP_ID, output[0])
