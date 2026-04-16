configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "preprocess"


rule all:
  input:
    "results/finish/preprocess.done"


rule run_preprocess:
  output:
    "results/finish/preprocess.done"
  run:
    run_step(STEP_ID, output[0])
