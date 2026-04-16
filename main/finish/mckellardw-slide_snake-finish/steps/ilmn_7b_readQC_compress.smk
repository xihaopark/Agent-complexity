configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_compress"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_compress.done"


rule run_ilmn_7b_readQC_compress:
  output:
    "results/finish/ilmn_7b_readQC_compress.done"
  run:
    run_step(STEP_ID, output[0])
