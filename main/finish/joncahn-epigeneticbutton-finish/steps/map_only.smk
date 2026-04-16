configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map_only"


rule all:
  input:
    "results/finish/map_only.done"


rule run_map_only:
  output:
    "results/finish/map_only.done"
  run:
    run_step(STEP_ID, output[0])
