configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "check_read_type"


rule all:
  input:
    "results/finish/check_read_type.done"


rule run_check_read_type:
  output:
    "results/finish/check_read_type.done"
  run:
    run_step(STEP_ID, output[0])
