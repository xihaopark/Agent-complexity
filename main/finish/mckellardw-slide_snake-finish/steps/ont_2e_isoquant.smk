configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2e_isoquant"


rule all:
  input:
    "results/finish/ont_2e_isoquant.done"


rule run_ont_2e_isoquant:
  output:
    "results/finish/ont_2e_isoquant.done"
  run:
    run_step(STEP_ID, output[0])
