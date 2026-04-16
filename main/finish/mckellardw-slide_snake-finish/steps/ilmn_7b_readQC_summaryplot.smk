configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_summaryplot"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_summaryplot.done"


rule run_ilmn_7b_readQC_summaryplot:
  output:
    "results/finish/ilmn_7b_readQC_summaryplot.done"
  run:
    run_step(STEP_ID, output[0])
