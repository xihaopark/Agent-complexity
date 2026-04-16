configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2b_txome_cache_seurat_minimap2"


rule all:
  input:
    "results/finish/ont_2b_txome_cache_seurat_minimap2.done"


rule run_ont_2b_txome_cache_seurat_minimap2:
  output:
    "results/finish/ont_2b_txome_cache_seurat_minimap2.done"
  run:
    run_step(STEP_ID, output[0])
