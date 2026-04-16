configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "lambda_gene_annotation"


rule all:
  input:
    "results/finish/lambda_gene_annotation.done"


rule run_lambda_gene_annotation:
  output:
    "results/finish/lambda_gene_annotation.done"
  run:
    run_step(STEP_ID, output[0])
