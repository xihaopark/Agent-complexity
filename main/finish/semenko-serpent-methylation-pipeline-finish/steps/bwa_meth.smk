configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bwa_meth"


rule all:
  input:
    "results/finish/bwa_meth.done"


rule run_bwa_meth:
  output:
    "results/finish/bwa_meth.done"
  run:
    run_step(STEP_ID, output[0])
