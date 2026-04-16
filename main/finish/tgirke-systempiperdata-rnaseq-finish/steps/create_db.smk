configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_db"


rule all:
  input:
    "results/finish/create_db.done"


rule run_create_db:
  output:
    "results/finish/create_db.done"
  run:
    run_step(STEP_ID, output[0])
