configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_gsize"


rule all:
  input:
    "results/finish/get_gsize.done"


rule run_get_gsize:
  output:
    "results/finish/get_gsize.done"
  run:
    run_step(STEP_ID, output[0])
