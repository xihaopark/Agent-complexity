configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_1_preCutadapt"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_1_preCutadapt.done"


rule run_ilmn_7b_readQC_1_preCutadapt:
  output:
    "results/finish/ilmn_7b_readQC_1_preCutadapt.done"
  run:
    run_step(STEP_ID, output[0])
