configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "STAR_map_se"


rule all:
  input:
    "results/finish/STAR_map_se.done"


rule run_STAR_map_se:
  output:
    "results/finish/STAR_map_se.done"
  run:
    run_step(STEP_ID, output[0])
