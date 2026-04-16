configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bismark_map_se"


rule all:
  input:
    "results/finish/bismark_map_se.done"


rule run_bismark_map_se:
  output:
    "results/finish/bismark_map_se.done"
  run:
    run_step(STEP_ID, output[0])
