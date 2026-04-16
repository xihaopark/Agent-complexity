configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2d_ultra_add_corrected_barcodes"


rule all:
  input:
    "results/finish/ont_2d_ultra_add_corrected_barcodes.done"


rule run_ont_2d_ultra_add_corrected_barcodes:
  output:
    "results/finish/ont_2d_ultra_add_corrected_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
