configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_databases"


rule all:
  input:
    "results/finish/prepare_databases.done"


rule run_prepare_databases:
  output:
    "results/finish/prepare_databases.done"
  run:
    run_step(STEP_ID, output[0])
