configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "check_te_file"


rule all:
  input:
    "results/finish/check_te_file.done"


rule run_check_te_file:
  output:
    "results/finish/check_te_file.done"
  run:
    run_step(STEP_ID, output[0])
