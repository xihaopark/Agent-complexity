configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extend_barcode_top"


rule all:
  input:
    "results/finish/extend_barcode_top.done"


rule run_extend_barcode_top:
  output:
    "results/finish/extend_barcode_top.done"
  run:
    run_step(STEP_ID, output[0])
