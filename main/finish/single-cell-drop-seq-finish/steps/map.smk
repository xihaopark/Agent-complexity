configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map"


rule all:
  input:
    "results/finish/map.done"


rule run_map:
  output:
    "results/finish/map.done"
  run:
    run_step(STEP_ID, output[0])
