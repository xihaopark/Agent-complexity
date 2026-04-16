configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "stratify_results"


rule all:
  input:
    "results/finish/stratify_results.done"


rule run_stratify_results:
  output:
    "results/finish/stratify_results.done"
  run:
    run_step(STEP_ID, output[0])
