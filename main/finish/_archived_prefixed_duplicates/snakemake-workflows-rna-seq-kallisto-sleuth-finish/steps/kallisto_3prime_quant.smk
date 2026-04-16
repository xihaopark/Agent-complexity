configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_3prime_quant"


rule all:
  input:
    "results/finish/kallisto_3prime_quant.done"


rule run_kallisto_3prime_quant:
  output:
    "results/finish/kallisto_3prime_quant.done"
  run:
    run_step(STEP_ID, output[0])
