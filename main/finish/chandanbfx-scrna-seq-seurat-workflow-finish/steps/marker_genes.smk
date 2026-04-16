configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "marker_genes"


rule all:
  input:
    "results/finish/marker_genes.done"


rule run_marker_genes:
  output:
    "results/finish/marker_genes.done"
  run:
    run_step(STEP_ID, output[0])
