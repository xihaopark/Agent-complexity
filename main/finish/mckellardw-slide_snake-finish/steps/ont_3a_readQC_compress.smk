configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_compress"


rule all:
  input:
    "results/finish/ont_3a_readQC_compress.done"


rule run_ont_3a_readQC_compress:
  output:
    "results/finish/ont_3a_readQC_compress.done"
  run:
    run_step(STEP_ID, output[0])
