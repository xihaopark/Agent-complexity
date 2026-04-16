configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mark_dup"


rule all:
  input:
    "results/finish/mark_dup.done"


rule run_mark_dup:
  output:
    "results/finish/mark_dup.done"
  run:
    run_step(STEP_ID, output[0])
