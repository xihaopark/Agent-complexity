configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_bt2_indices"


rule all:
  input:
    "results/finish/make_bt2_indices.done"


rule run_make_bt2_indices:
  output:
    "results/finish/make_bt2_indices.done"
  run:
    run_step(STEP_ID, output[0])
