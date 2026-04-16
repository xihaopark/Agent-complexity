configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "add_read_group"


rule all:
  input:
    "results/finish/add_read_group.done"


rule run_add_read_group:
  output:
    "results/finish/add_read_group.done"
  run:
    run_step(STEP_ID, output[0])
