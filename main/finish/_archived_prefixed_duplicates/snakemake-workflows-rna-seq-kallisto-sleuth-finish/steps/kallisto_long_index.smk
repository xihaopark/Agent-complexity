configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_long_index"


rule all:
  input:
    "results/finish/kallisto_long_index.done"


rule run_kallisto_long_index:
  output:
    "results/finish/kallisto_long_index.done"
  run:
    run_step(STEP_ID, output[0])
