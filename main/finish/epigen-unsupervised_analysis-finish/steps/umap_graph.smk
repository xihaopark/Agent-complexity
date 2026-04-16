configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "umap_graph"


rule all:
  input:
    "results/finish/umap_graph.done"


rule run_umap_graph:
  output:
    "results/finish/umap_graph.done"
  run:
    run_step(STEP_ID, output[0])
