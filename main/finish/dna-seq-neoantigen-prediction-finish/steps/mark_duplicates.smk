configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mark_duplicates"


rule all:
  input:
    "results/finish/mark_duplicates.done"


rule run_mark_duplicates:
  output:
    "results/finish/mark_duplicates.done"
  run:
    run_step(STEP_ID, output[0])
