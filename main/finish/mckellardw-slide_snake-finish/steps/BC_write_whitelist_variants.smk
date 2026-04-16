configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "BC_write_whitelist_variants"


rule all:
  input:
    "results/finish/BC_write_whitelist_variants.done"


rule run_BC_write_whitelist_variants:
  output:
    "results/finish/BC_write_whitelist_variants.done"
  run:
    run_step(STEP_ID, output[0])
