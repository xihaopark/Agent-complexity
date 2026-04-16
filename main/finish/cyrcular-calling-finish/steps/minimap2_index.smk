configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "minimap2_index"


rule all:
  input:
    "results/finish/minimap2_index.done"


rule run_minimap2_index:
  output:
    "results/finish/minimap2_index.done"
  run:
    run_step(STEP_ID, output[0])
