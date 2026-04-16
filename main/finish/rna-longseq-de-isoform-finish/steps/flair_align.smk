configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "flair_align"


rule all:
  input:
    "results/finish/flair_align.done"


rule run_flair_align:
  output:
    "results/finish/flair_align.done"
  run:
    run_step(STEP_ID, output[0])
