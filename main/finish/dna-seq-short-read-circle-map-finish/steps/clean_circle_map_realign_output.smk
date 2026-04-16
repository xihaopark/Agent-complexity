configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "clean_circle_map_realign_output"


rule all:
  input:
    "results/finish/clean_circle_map_realign_output.done"


rule run_clean_circle_map_realign_output:
  output:
    "results/finish/clean_circle_map_realign_output.done"
  run:
    run_step(STEP_ID, output[0])
