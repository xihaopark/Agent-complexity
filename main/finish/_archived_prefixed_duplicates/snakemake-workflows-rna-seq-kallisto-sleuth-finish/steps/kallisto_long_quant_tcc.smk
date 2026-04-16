configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_long_quant_tcc"


rule all:
  input:
    "results/finish/kallisto_long_quant_tcc.done"


rule run_kallisto_long_quant_tcc:
  output:
    "results/finish/kallisto_long_quant_tcc.done"
  run:
    run_step(STEP_ID, output[0])
