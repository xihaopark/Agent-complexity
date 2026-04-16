configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "save_counts"


rule all:
  input:
    "results/finish/save_counts.done"


rule run_save_counts:
  output:
    "results/finish/save_counts.done"
  run:
    run_step(STEP_ID, output[0])
