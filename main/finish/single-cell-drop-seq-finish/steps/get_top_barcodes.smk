configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_top_barcodes"


rule all:
  input:
    "results/finish/get_top_barcodes.done"


rule run_get_top_barcodes:
  output:
    "results/finish/get_top_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
