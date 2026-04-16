configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_nearest_transcript"


rule all:
  input:
    "results/finish/get_nearest_transcript.done"


rule run_get_nearest_transcript:
  output:
    "results/finish/get_nearest_transcript.done"
  run:
    run_step(STEP_ID, output[0])
