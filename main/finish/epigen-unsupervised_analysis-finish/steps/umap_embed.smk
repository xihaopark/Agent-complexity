configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "umap_embed"


rule all:
  input:
    "results/finish/umap_embed.done"


rule run_umap_embed:
  output:
    "results/finish/umap_embed.done"
  run:
    run_step(STEP_ID, output[0])
