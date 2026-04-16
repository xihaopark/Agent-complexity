configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_combined"


rule all:
  input:
    "results/finish/all_combined.done"


rule run_all_combined:
  output:
    "results/finish/all_combined.done"
  run:
    run_step(STEP_ID, output[0])
