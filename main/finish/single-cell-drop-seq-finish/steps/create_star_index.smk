configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_star_index"


rule all:
  input:
    "results/finish/create_star_index.done"


rule run_create_star_index:
  output:
    "results/finish/create_star_index.done"
  run:
    run_step(STEP_ID, output[0])
