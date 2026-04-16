configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_transcript_info"


rule all:
  input:
    "results/finish/get_transcript_info.done"


rule run_get_transcript_info:
  output:
    "results/finish/get_transcript_info.done"
  run:
    run_step(STEP_ID, output[0])
