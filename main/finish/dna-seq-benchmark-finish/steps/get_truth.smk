configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_truth"


rule all:
  input:
    "results/finish/get_truth.done"


rule run_get_truth:
  output:
    "results/finish/get_truth.done"
  run:
    run_step(STEP_ID, output[0])
