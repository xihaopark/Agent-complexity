configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filterFragments"


rule all:
  input:
    "results/finish/filterFragments.done"


rule run_filterFragments:
  output:
    "results/finish/filterFragments.done"
  run:
    run_step(STEP_ID, output[0])
