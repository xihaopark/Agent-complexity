configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "norm_edgeR"


rule all:
  input:
    "results/finish/norm_edgeR.done"


rule run_norm_edgeR:
  output:
    "results/finish/norm_edgeR.done"
  run:
    run_step(STEP_ID, output[0])
