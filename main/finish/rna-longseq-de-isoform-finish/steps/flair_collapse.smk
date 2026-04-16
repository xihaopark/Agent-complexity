configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "flair_collapse"


rule all:
  input:
    "results/finish/flair_collapse.done"


rule run_flair_collapse:
  output:
    "results/finish/flair_collapse.done"
  run:
    run_step(STEP_ID, output[0])
