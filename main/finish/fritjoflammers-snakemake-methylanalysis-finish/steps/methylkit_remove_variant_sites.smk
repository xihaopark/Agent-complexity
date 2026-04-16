configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_remove_variant_sites"


rule all:
  input:
    "results/finish/methylkit_remove_variant_sites.done"


rule run_methylkit_remove_variant_sites:
  output:
    "results/finish/methylkit_remove_variant_sites.done"
  run:
    run_step(STEP_ID, output[0])
