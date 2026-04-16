configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_2_postCutadapt"


rule all:
  input:
    "results/finish/ont_3a_readQC_2_postCutadapt.done"


rule run_ont_3a_readQC_2_postCutadapt:
  output:
    "results/finish/ont_3a_readQC_2_postCutadapt.done"
  run:
    run_step(STEP_ID, output[0])
