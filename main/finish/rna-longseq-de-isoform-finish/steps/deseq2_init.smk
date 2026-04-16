configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "deseq2_init"


rule all:
  input:
    "results/finish/deseq2_init.done"


rule run_deseq2_init:
  output:
    "results/finish/deseq2_init.done"
  run:
    run_step(STEP_ID, output[0])
