configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3a_cache_h5ad_STAR"


rule all:
  input:
    "results/finish/ilmn_3a_cache_h5ad_STAR.done"


rule run_ilmn_3a_cache_h5ad_STAR:
  output:
    "results/finish/ilmn_3a_cache_h5ad_STAR.done"
  run:
    run_step(STEP_ID, output[0])
