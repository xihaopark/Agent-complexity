configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "macau_run"


rule all:
  input:
    "results/finish/macau_run.done"


rule run_macau_run:
  output:
    "results/finish/macau_run.done"
  run:
    run_step(STEP_ID, output[0])
