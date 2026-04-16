configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "deseq2_analysis"


rule all:
  input:
    "results/finish/deseq2_analysis.done"


rule run_deseq2_analysis:
  output:
    "results/finish/deseq2_analysis.done"
  run:
    run_step(STEP_ID, output[0])
