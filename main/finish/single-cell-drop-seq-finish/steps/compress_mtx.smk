configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "compress_mtx"


rule all:
  input:
    "results/finish/compress_mtx.done"


rule run_compress_mtx:
  output:
    "results/finish/compress_mtx.done"
  run:
    run_step(STEP_ID, output[0])
