configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "stratify_truth"


rule all:
  input:
    "results/finish/stratify_truth.done"


rule run_stratify_truth:
  output:
    "results/finish/stratify_truth.done"
  run:
    run_step(STEP_ID, output[0])
