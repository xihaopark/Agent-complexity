configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "run_edgeR"


rule all:
  input:
    "results/finish/run_edgeR.done"


rule run_run_edgeR:
  output:
    "results/finish/run_edgeR.done"
  run:
    run_step(STEP_ID, output[0])
