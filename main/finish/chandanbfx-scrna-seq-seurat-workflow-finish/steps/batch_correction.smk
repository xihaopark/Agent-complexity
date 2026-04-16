configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "batch_correction"


rule all:
  input:
    "results/finish/batch_correction.done"


rule run_batch_correction:
  output:
    "results/finish/batch_correction.done"
  run:
    run_step(STEP_ID, output[0])
