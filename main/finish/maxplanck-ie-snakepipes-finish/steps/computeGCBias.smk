configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "computeGCBias"


rule all:
  input:
    "results/finish/computeGCBias.done"


rule run_computeGCBias:
  output:
    "results/finish/computeGCBias.done"
  run:
    run_step(STEP_ID, output[0])
