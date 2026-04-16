configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map_primers"


rule all:
  input:
    "results/finish/map_primers.done"


rule run_map_primers:
  output:
    "results/finish/map_primers.done"
  run:
    run_step(STEP_ID, output[0])
