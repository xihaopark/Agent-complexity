configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "find_markers"


rule all:
  input:
    "results/finish/find_markers.done"


rule run_find_markers:
  output:
    "results/finish/find_markers.done"
  run:
    run_step(STEP_ID, output[0])
