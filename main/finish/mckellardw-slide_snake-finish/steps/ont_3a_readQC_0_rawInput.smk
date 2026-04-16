configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_0_rawInput"


rule all:
  input:
    "results/finish/ont_3a_readQC_0_rawInput.done"


rule run_ont_3a_readQC_0_rawInput:
  output:
    "results/finish/ont_3a_readQC_0_rawInput.done"
  run:
    run_step(STEP_ID, output[0])
