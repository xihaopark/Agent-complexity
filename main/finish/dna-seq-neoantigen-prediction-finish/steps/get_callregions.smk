configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_callregions"


rule all:
  input:
    "results/finish/get_callregions.done"


rule run_get_callregions:
  output:
    "results/finish/get_callregions.done"
  run:
    run_step(STEP_ID, output[0])
