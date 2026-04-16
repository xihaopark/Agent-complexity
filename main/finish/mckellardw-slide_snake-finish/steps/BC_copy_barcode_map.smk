configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "BC_copy_barcode_map"


rule all:
  input:
    "results/finish/BC_copy_barcode_map.done"


rule run_BC_copy_barcode_map:
  output:
    "results/finish/BC_copy_barcode_map.done"
  run:
    run_step(STEP_ID, output[0])
