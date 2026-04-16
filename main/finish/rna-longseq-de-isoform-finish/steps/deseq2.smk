configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "deseq2"


rule all:
  input:
    "results/finish/deseq2.done"


rule run_deseq2:
  output:
    "results/finish/deseq2.done"
  run:
    run_step(STEP_ID, output[0])
