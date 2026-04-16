configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extend_barcode_whitelist"


rule all:
  input:
    "results/finish/extend_barcode_whitelist.done"


rule run_extend_barcode_whitelist:
  output:
    "results/finish/extend_barcode_whitelist.done"
  run:
    run_step(STEP_ID, output[0])
