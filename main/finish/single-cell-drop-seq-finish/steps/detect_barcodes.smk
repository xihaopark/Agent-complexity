configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "detect_barcodes"


rule all:
  input:
    "results/finish/detect_barcodes.done"


rule run_detect_barcodes:
  output:
    "results/finish/detect_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
