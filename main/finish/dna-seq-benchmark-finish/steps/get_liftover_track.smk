configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_liftover_track"


rule all:
  input:
    "results/finish/get_liftover_track.done"


rule run_get_liftover_track:
  output:
    "results/finish/get_liftover_track.done"
  run:
    run_step(STEP_ID, output[0])
