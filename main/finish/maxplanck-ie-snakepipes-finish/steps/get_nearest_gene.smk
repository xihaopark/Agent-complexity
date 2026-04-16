configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_nearest_gene"


rule all:
  input:
    "results/finish/get_nearest_gene.done"


rule run_get_nearest_gene:
  output:
    "results/finish/get_nearest_gene.done"
  run:
    run_step(STEP_ID, output[0])
