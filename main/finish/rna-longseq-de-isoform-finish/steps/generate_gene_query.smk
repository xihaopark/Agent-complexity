configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "generate_gene_query"


rule all:
  input:
    "results/finish/generate_gene_query.done"


rule run_generate_gene_query:
  output:
    "results/finish/generate_gene_query.done"
  run:
    run_step(STEP_ID, output[0])
