configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_known_variants"


rule all:
  input:
    "results/finish/get_known_variants.done"


rule run_get_known_variants:
  output:
    "results/finish/get_known_variants.done"
  run:
    run_step(STEP_ID, output[0])
