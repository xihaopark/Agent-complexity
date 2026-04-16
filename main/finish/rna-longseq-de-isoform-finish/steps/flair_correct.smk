configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "flair_correct"


rule all:
  input:
    "results/finish/flair_correct.done"


rule run_flair_correct:
  output:
    "results/finish/flair_correct.done"
  run:
    run_step(STEP_ID, output[0])
