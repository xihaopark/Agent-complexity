configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_index"


rule all:
  input:
    "results/finish/kallisto_index.done"


rule run_kallisto_index:
  output:
    "results/finish/kallisto_index.done"
  run:
    run_step(STEP_ID, output[0])
