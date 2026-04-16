configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_ORA_GSEApy"


rule all:
  input:
    "results/finish/gene_ORA_GSEApy.done"


rule run_gene_ORA_GSEApy:
  output:
    "results/finish/gene_ORA_GSEApy.done"
  run:
    run_step(STEP_ID, output[0])
