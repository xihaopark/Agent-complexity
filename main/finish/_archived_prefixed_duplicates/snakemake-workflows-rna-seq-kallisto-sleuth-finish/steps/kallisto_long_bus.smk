configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_long_bus"


rule all:
  input:
    "results/finish/kallisto_long_bus.done"


rule run_kallisto_long_bus:
  output:
    "results/finish/kallisto_long_bus.done"
  run:
    run_step(STEP_ID, output[0])
