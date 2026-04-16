configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calculate_cpat_hexamers"


rule all:
  input:
    "results/finish/calculate_cpat_hexamers.done"


rule run_calculate_cpat_hexamers:
  output:
    "results/finish/calculate_cpat_hexamers.done"
  run:
    run_step(STEP_ID, output[0])
