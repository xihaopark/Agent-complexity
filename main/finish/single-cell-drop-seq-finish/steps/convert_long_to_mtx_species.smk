configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "convert_long_to_mtx_species"


rule all:
  input:
    "results/finish/convert_long_to_mtx_species.done"


rule run_convert_long_to_mtx_species:
  output:
    "results/finish/convert_long_to_mtx_species.done"
  run:
    run_step(STEP_ID, output[0])
