configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastqc_barcodes"


rule all:
  input:
    "results/finish/fastqc_barcodes.done"


rule run_fastqc_barcodes:
  output:
    "results/finish/fastqc_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
