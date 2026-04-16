configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pred_ORF"


rule all:
  input:
    "results/finish/pred_ORF.done"


rule run_pred_ORF:
  output:
    "results/finish/pred_ORF.done"
  run:
    run_step(STEP_ID, output[0])
