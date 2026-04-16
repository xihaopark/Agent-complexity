configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_3_twiceCutadapt"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_3_twiceCutadapt.done"


rule run_ilmn_7b_readQC_3_twiceCutadapt:
  output:
    "results/finish/ilmn_7b_readQC_3_twiceCutadapt.done"
  run:
    run_step(STEP_ID, output[0])
