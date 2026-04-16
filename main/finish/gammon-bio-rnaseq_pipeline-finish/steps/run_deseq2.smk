configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "run_deseq2"


rule all:
  input:
    "results/finish/run_deseq2.done"


rule run_run_deseq2:
  output:
    "results/finish/run_deseq2.done"
  run:
    run_step(STEP_ID, output[0])
