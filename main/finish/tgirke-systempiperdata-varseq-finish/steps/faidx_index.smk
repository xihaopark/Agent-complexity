configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "faidx_index"


rule all:
  input:
    "results/finish/faidx_index.done"


rule run_faidx_index:
  output:
    "results/finish/faidx_index.done"
  run:
    run_step(STEP_ID, output[0])
