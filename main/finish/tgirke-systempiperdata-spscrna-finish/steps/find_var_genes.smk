configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "find_var_genes"


rule all:
  input:
    "results/finish/find_var_genes.done"


rule run_find_var_genes:
  output:
    "results/finish/find_var_genes.done"
  run:
    run_step(STEP_ID, output[0])
