configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "uropa_gencode"


rule all:
  input:
    "results/finish/uropa_gencode.done"


rule run_uropa_gencode:
  output:
    "results/finish/uropa_gencode.done"
  run:
    run_step(STEP_ID, output[0])
