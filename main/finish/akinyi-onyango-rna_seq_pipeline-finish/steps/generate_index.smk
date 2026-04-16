configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "generate_index"


rule all:
  input:
    "results/finish/generate_index.done"


rule run_generate_index:
  output:
    "results/finish/generate_index.done"
  run:
    run_step(STEP_ID, output[0])
