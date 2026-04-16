configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_geneid2name"


rule all:
  input:
    "results/finish/get_geneid2name.done"


rule run_get_geneid2name:
  output:
    "results/finish/get_geneid2name.done"
  run:
    run_step(STEP_ID, output[0])
