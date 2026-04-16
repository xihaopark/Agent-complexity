configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "drug_target"


rule all:
  input:
    "results/finish/drug_target.done"


rule run_drug_target:
  output:
    "results/finish/drug_target.done"
  run:
    run_step(STEP_ID, output[0])
