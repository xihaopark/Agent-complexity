configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_index"


rule all:
  input:
    "results/finish/make_index.done"


rule run_make_index:
  output:
    "results/finish/make_index.done"
  run:
    run_step(STEP_ID, output[0])
