configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiqc_cutadapt_barcodes"


rule all:
  input:
    "results/finish/multiqc_cutadapt_barcodes.done"


rule run_multiqc_cutadapt_barcodes:
  output:
    "results/finish/multiqc_cutadapt_barcodes.done"
  run:
    run_step(STEP_ID, output[0])
