configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "lfc_heatmap"


rule all:
  input:
    "results/finish/lfc_heatmap.done"


rule run_lfc_heatmap:
  output:
    "results/finish/lfc_heatmap.done"
  run:
    run_step(STEP_ID, output[0])
