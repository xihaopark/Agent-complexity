configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "index_HLALA"


rule all:
  input:
    "results/finish/index_HLALA.done"


rule run_index_HLALA:
  output:
    "results/finish/index_HLALA.done"
  run:
    run_step(STEP_ID, output[0])
