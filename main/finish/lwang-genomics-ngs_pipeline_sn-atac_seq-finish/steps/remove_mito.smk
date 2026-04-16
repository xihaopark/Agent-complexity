configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "remove_mito"


rule all:
  input:
    "results/finish/remove_mito.done"


rule run_remove_mito:
  output:
    "results/finish/remove_mito.done"
  run:
    run_step(STEP_ID, output[0])
