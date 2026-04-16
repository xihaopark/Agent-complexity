configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "convert_long_to_mtx"


rule all:
  input:
    "results/finish/convert_long_to_mtx.done"


rule run_convert_long_to_mtx:
  output:
    "results/finish/convert_long_to_mtx.done"
  run:
    run_step(STEP_ID, output[0])
