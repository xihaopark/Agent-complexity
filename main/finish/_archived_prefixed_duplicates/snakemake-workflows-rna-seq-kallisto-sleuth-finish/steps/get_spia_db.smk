configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_spia_db"


rule all:
  input:
    "results/finish/get_spia_db.done"


rule run_get_spia_db:
  output:
    "results/finish/get_spia_db.done"
  run:
    run_step(STEP_ID, output[0])
