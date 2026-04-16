configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cellranger_multi_files_gene_expression_global"


rule all:
  input:
    "results/finish/cellranger_multi_files_gene_expression_global.done"


rule run_cellranger_multi_files_gene_expression_global:
  output:
    "results/finish/cellranger_multi_files_gene_expression_global.done"
  run:
    run_step(STEP_ID, output[0])
