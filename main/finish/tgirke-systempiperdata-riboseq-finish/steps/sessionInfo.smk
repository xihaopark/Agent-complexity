configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sessionInfo"


rule all:
  input:
    "results/finish/sessionInfo.done"


rule run_sessionInfo:
  output:
    "results/finish/sessionInfo.done"
  run:
    run_step(STEP_ID, output[0])
