configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quantify"


rule all:
  input:
    "results/finish/quantify.done"


rule run_quantify:
  output:
    "results/finish/quantify.done"
  run:
    run_step(STEP_ID, output[0])
