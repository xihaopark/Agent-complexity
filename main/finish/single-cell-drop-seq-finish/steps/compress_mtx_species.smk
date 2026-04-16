configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "compress_mtx_species"


rule all:
  input:
    "results/finish/compress_mtx_species.done"


rule run_compress_mtx_species:
  output:
    "results/finish/compress_mtx_species.done"
  run:
    run_step(STEP_ID, output[0])
