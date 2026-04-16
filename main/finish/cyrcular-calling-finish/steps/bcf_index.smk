configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bcf_index"


rule all:
  input:
    "results/finish/bcf_index.done"


rule run_bcf_index:
  output:
    "results/finish/bcf_index.done"
  run:
    run_step(STEP_ID, output[0])
