configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "making_pseudo_replicates"


rule all:
  input:
    "results/finish/making_pseudo_replicates.done"


rule run_making_pseudo_replicates:
  output:
    "results/finish/making_pseudo_replicates.done"
  run:
    run_step(STEP_ID, output[0])
