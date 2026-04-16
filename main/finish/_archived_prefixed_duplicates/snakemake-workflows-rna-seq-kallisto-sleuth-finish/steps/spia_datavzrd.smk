configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "spia_datavzrd"


rule all:
  input:
    "results/finish/spia_datavzrd.done"


rule run_spia_datavzrd:
  output:
    "results/finish/spia_datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
