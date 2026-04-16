configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_quant"


rule all:
  input:
    "results/finish/kallisto_quant.done"


rule run_kallisto_quant:
  output:
    "results/finish/kallisto_quant.done"
  run:
    run_step(STEP_ID, output[0])
