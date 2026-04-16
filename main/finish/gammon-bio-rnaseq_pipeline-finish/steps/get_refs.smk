configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_refs"


rule all:
  input:
    "results/finish/get_refs.done"


rule run_get_refs:
  output:
    "results/finish/get_refs.done"
  run:
    run_step(STEP_ID, output[0])
