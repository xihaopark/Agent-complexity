configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "build_minimap_index"


rule all:
  input:
    "results/finish/build_minimap_index.done"


rule run_build_minimap_index:
  output:
    "results/finish/build_minimap_index.done"
  run:
    run_step(STEP_ID, output[0])
