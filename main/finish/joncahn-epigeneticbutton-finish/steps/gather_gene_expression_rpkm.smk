configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gather_gene_expression_rpkm"


rule all:
  input:
    "results/finish/gather_gene_expression_rpkm.done"


rule run_gather_gene_expression_rpkm:
  output:
    "results/finish/gather_gene_expression_rpkm.done"
  run:
    run_step(STEP_ID, output[0])
