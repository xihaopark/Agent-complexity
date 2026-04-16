configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_GO_database"


rule all:
  input:
    "results/finish/create_GO_database.done"


rule run_create_GO_database:
  output:
    "results/finish/create_GO_database.done"
  run:
    run_step(STEP_ID, output[0])
