configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "star_index"


rule all:
  input:
    "results/finish/star_index.done"


rule run_star_index:
  output:
    "results/finish/star_index.done"
  run:
    run_step(STEP_ID, output[0])
