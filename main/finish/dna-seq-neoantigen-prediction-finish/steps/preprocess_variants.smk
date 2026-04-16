configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "preprocess_variants"


rule all:
  input:
    "results/finish/preprocess_variants.done"


rule run_preprocess_variants:
  output:
    "results/finish/preprocess_variants.done"
  run:
    run_step(STEP_ID, output[0])
