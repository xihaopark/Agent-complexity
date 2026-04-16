configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2e_cache_seurat"


rule all:
  input:
    "results/finish/ont_2e_cache_seurat.done"


rule run_ont_2e_cache_seurat:
  output:
    "results/finish/ont_2e_cache_seurat.done"
  run:
    run_step(STEP_ID, output[0])
