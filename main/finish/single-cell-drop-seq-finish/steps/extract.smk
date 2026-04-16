configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract"


rule all:
  input:
    "results/finish/extract.done"


rule run_extract:
  output:
    "results/finish/extract.done"
  run:
    run_step(STEP_ID, output[0])
