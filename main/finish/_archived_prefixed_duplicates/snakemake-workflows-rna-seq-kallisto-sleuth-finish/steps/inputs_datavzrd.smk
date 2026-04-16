configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "inputs_datavzrd"


rule all:
  input:
    "results/finish/inputs_datavzrd.done"


rule run_inputs_datavzrd:
  output:
    "results/finish/inputs_datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
