configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_3prime_index"


rule all:
  input:
    "results/finish/kallisto_3prime_index.done"


rule run_kallisto_3prime_index:
  output:
    "results/finish/kallisto_3prime_index.done"
  run:
    run_step(STEP_ID, output[0])
