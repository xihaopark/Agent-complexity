configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_tsne"


rule all:
  input:
    "results/finish/gene_tsne.done"


rule run_gene_tsne:
  output:
    "results/finish/gene_tsne.done"
  run:
    run_step(STEP_ID, output[0])
