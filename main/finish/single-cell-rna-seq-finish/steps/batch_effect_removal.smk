configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "batch_effect_removal"


rule all:
  input:
    "results/finish/batch_effect_removal.done"


rule run_batch_effect_removal:
  output:
    "results/finish/batch_effect_removal.done"
  run:
    run_step(STEP_ID, output[0])
