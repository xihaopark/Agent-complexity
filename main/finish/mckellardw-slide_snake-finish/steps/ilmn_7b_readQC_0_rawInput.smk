configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_0_rawInput"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_0_rawInput.done"


rule run_ilmn_7b_readQC_0_rawInput:
  output:
    "results/finish/ilmn_7b_readQC_0_rawInput.done"
  run:
    run_step(STEP_ID, output[0])
