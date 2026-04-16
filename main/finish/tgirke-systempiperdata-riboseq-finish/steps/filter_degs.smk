configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_degs"


rule all:
  input:
    "results/finish/filter_degs.done"


rule run_filter_degs:
  output:
    "results/finish/filter_degs.done"
  run:
    run_step(STEP_ID, output[0])
