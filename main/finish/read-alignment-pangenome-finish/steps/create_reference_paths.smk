configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_reference_paths"


rule all:
  input:
    "results/finish/create_reference_paths.done"


rule run_create_reference_paths:
  output:
    "results/finish/create_reference_paths.done"
  run:
    run_step(STEP_ID, output[0])
