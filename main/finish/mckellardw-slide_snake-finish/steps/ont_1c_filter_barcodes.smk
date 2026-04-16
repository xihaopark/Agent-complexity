configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1c_filter_barcodes"


rule all:
  input:
    "results/finish/ont_1c_filter_barcodes.done"


rule run_ont_1c_filter_barcodes:
  output:
    "results/finish/ont_1c_filter_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
