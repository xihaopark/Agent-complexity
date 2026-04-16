configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "datavzrd_circle_calls"


rule all:
  input:
    "results/finish/datavzrd_circle_calls.done"


rule run_datavzrd_circle_calls:
  output:
    "results/finish/datavzrd_circle_calls.done"
  run:
    run_step(STEP_ID, output[0])
