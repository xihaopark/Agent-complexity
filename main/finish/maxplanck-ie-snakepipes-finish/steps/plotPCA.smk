configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotPCA"


rule all:
  input:
    "results/finish/plotPCA.done"


rule run_plotPCA:
  output:
    "results/finish/plotPCA.done"
  run:
    run_step(STEP_ID, output[0])
