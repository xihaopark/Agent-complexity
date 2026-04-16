configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tabix_known_variants"


rule all:
  input:
    "results/finish/tabix_known_variants.done"


rule run_tabix_known_variants:
  output:
    "results/finish/tabix_known_variants.done"
  run:
    run_step(STEP_ID, output[0])
