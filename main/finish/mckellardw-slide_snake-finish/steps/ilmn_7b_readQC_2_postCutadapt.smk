configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_2_postCutadapt"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_2_postCutadapt.done"


rule run_ilmn_7b_readQC_2_postCutadapt:
  output:
    "results/finish/ilmn_7b_readQC_2_postCutadapt.done"
  run:
    run_step(STEP_ID, output[0])
