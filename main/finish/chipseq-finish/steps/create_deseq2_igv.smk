configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_deseq2_igv"


rule all:
  input:
    "results/finish/create_deseq2_igv.done"


rule run_create_deseq2_igv:
  output:
    "results/finish/create_deseq2_igv.done"
  run:
    run_step(STEP_ID, output[0])
