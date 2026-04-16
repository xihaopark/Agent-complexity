configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bwa_meth_index"


rule all:
  input:
    "results/finish/bwa_meth_index.done"


rule run_bwa_meth_index:
  output:
    "results/finish/bwa_meth_index.done"
  run:
    run_step(STEP_ID, output[0])
