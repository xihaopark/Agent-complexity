configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2d_ultra_cache_h5ad"


rule all:
  input:
    "results/finish/ont_2d_ultra_cache_h5ad.done"


rule run_ont_2d_ultra_cache_h5ad:
  output:
    "results/finish/ont_2d_ultra_cache_h5ad.done"
  run:
    run_step(STEP_ID, output[0])
