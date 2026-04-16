configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calculate_cpat_logit_model"


rule all:
  input:
    "results/finish/calculate_cpat_logit_model.done"


rule run_calculate_cpat_logit_model:
  output:
    "results/finish/calculate_cpat_logit_model.done"
  run:
    run_step(STEP_ID, output[0])
