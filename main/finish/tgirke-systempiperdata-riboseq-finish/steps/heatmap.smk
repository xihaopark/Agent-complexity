configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "heatmap"


rule all:
  input:
    "results/finish/heatmap.done"


rule run_heatmap:
  output:
    "results/finish/heatmap.done"
  run:
    run_step(STEP_ID, output[0])
