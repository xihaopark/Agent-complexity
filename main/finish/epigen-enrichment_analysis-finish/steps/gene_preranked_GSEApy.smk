configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_preranked_GSEApy"


rule all:
  input:
    "results/finish/gene_preranked_GSEApy.done"


rule run_gene_preranked_GSEApy:
  output:
    "results/finish/gene_preranked_GSEApy.done"
  run:
    run_step(STEP_ID, output[0])
