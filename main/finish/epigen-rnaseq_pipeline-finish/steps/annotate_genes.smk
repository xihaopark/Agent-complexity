configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_genes"


rule all:
  input:
    "results/finish/annotate_genes.done"


rule run_annotate_genes:
  output:
    "results/finish/annotate_genes.done"
  run:
    run_step(STEP_ID, output[0])
