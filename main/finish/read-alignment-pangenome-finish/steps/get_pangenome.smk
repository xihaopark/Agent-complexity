configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_pangenome"


rule all:
  input:
    "results/finish/get_pangenome.done"


rule run_get_pangenome:
  output:
    "results/finish/get_pangenome.done"
  run:
    run_step(STEP_ID, output[0])
