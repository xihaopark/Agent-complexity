configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_sra"


rule all:
  input:
    "results/finish/get_sra.done"


rule run_get_sra:
  output:
    "results/finish/get_sra.done"
  run:
    run_step(STEP_ID, output[0])
