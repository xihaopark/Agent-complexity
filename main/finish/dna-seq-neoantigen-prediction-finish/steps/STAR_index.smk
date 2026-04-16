configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "STAR_index"


rule all:
  input:
    "results/finish/STAR_index.done"


rule run_STAR_index:
  output:
    "results/finish/STAR_index.done"
  run:
    run_step(STEP_ID, output[0])
