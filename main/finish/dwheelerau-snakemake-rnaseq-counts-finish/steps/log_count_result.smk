configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "log_count_result"


rule all:
  input:
    "results/finish/log_count_result.done"


rule run_log_count_result:
  output:
    "results/finish/log_count_result.done"
  run:
    run_step(STEP_ID, output[0])
