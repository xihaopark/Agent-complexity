configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "index_bcf"


rule all:
  input:
    "results/finish/index_bcf.done"


rule run_index_bcf:
  output:
    "results/finish/index_bcf.done"
  run:
    run_step(STEP_ID, output[0])
