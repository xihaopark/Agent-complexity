configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ucsc_hub"


rule all:
  input:
    "results/finish/ucsc_hub.done"


rule run_ucsc_hub:
  output:
    "results/finish/ucsc_hub.done"
  run:
    run_step(STEP_ID, output[0])
