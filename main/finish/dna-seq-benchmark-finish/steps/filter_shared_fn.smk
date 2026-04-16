configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_shared_fn"


rule all:
  input:
    "results/finish/filter_shared_fn.done"


rule run_filter_shared_fn:
  output:
    "results/finish/filter_shared_fn.done"
  run:
    run_step(STEP_ID, output[0])
