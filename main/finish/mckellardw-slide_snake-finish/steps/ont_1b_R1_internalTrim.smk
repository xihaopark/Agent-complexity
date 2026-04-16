configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1b_R1_internalTrim"


rule all:
  input:
    "results/finish/ont_1b_R1_internalTrim.done"


rule run_ont_1b_R1_internalTrim:
  output:
    "results/finish/ont_1b_R1_internalTrim.done"
  run:
    run_step(STEP_ID, output[0])
