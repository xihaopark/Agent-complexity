configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_summaryplot"


rule all:
  input:
    "results/finish/ont_3a_readQC_summaryplot.done"


rule run_ont_3a_readQC_summaryplot:
  output:
    "results/finish/ont_3a_readQC_summaryplot.done"
  run:
    run_step(STEP_ID, output[0])
