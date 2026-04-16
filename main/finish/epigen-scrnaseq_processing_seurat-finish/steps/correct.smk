configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "correct"


rule all:
  input:
    "results/finish/correct.done"


rule run_correct:
  output:
    "results/finish/correct.done"
  run:
    run_step(STEP_ID, output[0])
