configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "alevin_fry_quant"


rule all:
  input:
    "results/finish/alevin_fry_quant.done"


rule run_alevin_fry_quant:
  output:
    "results/finish/alevin_fry_quant.done"
  run:
    run_step(STEP_ID, output[0])
