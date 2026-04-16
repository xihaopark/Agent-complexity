configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "peak_calling"


rule all:
  input:
    "results/finish/peak_calling.done"


rule run_peak_calling:
  output:
    "results/finish/peak_calling.done"
  run:
    run_step(STEP_ID, output[0])
