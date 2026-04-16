configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ens_gene_to_go"


rule all:
  input:
    "results/finish/ens_gene_to_go.done"


rule run_ens_gene_to_go:
  output:
    "results/finish/ens_gene_to_go.done"
  run:
    run_step(STEP_ID, output[0])
