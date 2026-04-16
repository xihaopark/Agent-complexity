configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_2_symbol"


rule all:
  input:
    "results/finish/gene_2_symbol.done"


rule run_gene_2_symbol:
  output:
    "results/finish/gene_2_symbol.done"
  run:
    run_step(STEP_ID, output[0])
