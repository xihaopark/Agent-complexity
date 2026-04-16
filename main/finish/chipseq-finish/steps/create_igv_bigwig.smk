configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_igv_bigwig"


rule all:
  input:
    "results/finish/create_igv_bigwig.done"


rule run_create_igv_bigwig:
  output:
    "results/finish/create_igv_bigwig.done"
  run:
    run_step(STEP_ID, output[0])
