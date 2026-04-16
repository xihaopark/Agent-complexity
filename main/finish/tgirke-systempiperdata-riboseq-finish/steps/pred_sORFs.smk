configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pred_sORFs"


rule all:
  input:
    "results/finish/pred_sORFs.done"


rule run_pred_sORFs:
  output:
    "results/finish/pred_sORFs.done"
  run:
    run_step(STEP_ID, output[0])
