configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "has_header"


rule all:
  input:
    "results/finish/has_header.done"


rule run_has_header:
  output:
    "results/finish/has_header.done"
  run:
    run_step(STEP_ID, output[0])
