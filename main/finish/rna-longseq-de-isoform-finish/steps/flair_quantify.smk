configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "flair_quantify"


rule all:
  input:
    "results/finish/flair_quantify.done"


rule run_flair_quantify:
  output:
    "results/finish/flair_quantify.done"
  run:
    run_step(STEP_ID, output[0])
