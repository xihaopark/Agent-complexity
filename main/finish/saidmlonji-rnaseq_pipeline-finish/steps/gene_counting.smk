configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_counting"


rule all:
  input:
    "results/finish/gene_counting.done"


rule run_gene_counting:
  output:
    "results/finish/gene_counting.done"
  run:
    run_step(STEP_ID, output[0])
