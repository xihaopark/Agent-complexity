configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "visualize"


rule all:
  input:
    "results/finish/visualize.done"


rule run_visualize:
  output:
    "results/finish/visualize.done"
  run:
    run_step(STEP_ID, output[0])
