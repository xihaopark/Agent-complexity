configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_downsampled_vep_cache"


rule all:
  input:
    "results/finish/get_downsampled_vep_cache.done"


rule run_get_downsampled_vep_cache:
  output:
    "results/finish/get_downsampled_vep_cache.done"
  run:
    run_step(STEP_ID, output[0])
