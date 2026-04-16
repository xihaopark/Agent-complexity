configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_to_singlets"


rule all:
  input:
    "results/finish/filter_to_singlets.done"


rule run_filter_to_singlets:
  output:
    "results/finish/filter_to_singlets.done"
  run:
    run_step(STEP_ID, output[0])
