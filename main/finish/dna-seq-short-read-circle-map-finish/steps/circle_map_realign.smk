configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "circle_map_realign"


rule all:
  input:
    "results/finish/circle_map_realign.done"


rule run_circle_map_realign:
  output:
    "results/finish/circle_map_realign.done"
  run:
    run_step(STEP_ID, output[0])
