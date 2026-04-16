configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_list_export"


rule all:
  input:
    "results/finish/gene_list_export.done"


rule run_gene_list_export:
  output:
    "results/finish/gene_list_export.done"
  run:
    run_step(STEP_ID, output[0])
