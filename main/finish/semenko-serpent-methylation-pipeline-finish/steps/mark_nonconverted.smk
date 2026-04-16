configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mark_nonconverted"


rule all:
  input:
    "results/finish/mark_nonconverted.done"


rule run_mark_nonconverted:
  output:
    "results/finish/mark_nonconverted.done"
  run:
    run_step(STEP_ID, output[0])
