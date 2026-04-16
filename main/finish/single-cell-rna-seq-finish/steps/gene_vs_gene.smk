configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_vs_gene"


rule all:
  input:
    "results/finish/gene_vs_gene.done"


rule run_gene_vs_gene:
  output:
    "results/finish/gene_vs_gene.done"
  run:
    run_step(STEP_ID, output[0])
