configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "concat_variants"


rule all:
  input:
    "results/finish/concat_variants.done"


rule run_concat_variants:
  output:
    "results/finish/concat_variants.done"
  run:
    run_step(STEP_ID, output[0])
