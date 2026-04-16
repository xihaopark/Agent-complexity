configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "datavzrd"


rule all:
  input:
    "results/finish/datavzrd.done"


rule run_datavzrd:
  output:
    "results/finish/datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
