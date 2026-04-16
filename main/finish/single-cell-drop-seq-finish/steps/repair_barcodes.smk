configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "repair_barcodes"


rule all:
  input:
    "results/finish/repair_barcodes.done"


rule run_repair_barcodes:
  output:
    "results/finish/repair_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
