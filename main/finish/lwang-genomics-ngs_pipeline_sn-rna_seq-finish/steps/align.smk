configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "align"


rule all:
  input:
    "results/finish/align.done"


rule run_align:
  output:
    "results/finish/align.done"
  run:
    run_step(STEP_ID, output[0])
