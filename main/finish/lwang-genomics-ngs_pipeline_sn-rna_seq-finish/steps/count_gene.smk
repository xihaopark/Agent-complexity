configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "count_gene"


rule all:
  input:
    "results/finish/count_gene.done"


rule run_count_gene:
  output:
    "results/finish/count_gene.done"
  run:
    run_step(STEP_ID, output[0])
