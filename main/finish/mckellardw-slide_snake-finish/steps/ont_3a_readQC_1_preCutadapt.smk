configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_1_preCutadapt"


rule all:
  input:
    "results/finish/ont_3a_readQC_1_preCutadapt.done"


rule run_ont_3a_readQC_1_preCutadapt:
  output:
    "results/finish/ont_3a_readQC_1_preCutadapt.done"
  run:
    run_step(STEP_ID, output[0])
