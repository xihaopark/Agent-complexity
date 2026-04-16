configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "spia"


rule all:
  input:
    "results/finish/spia.done"


rule run_spia:
  output:
    "results/finish/spia.done"
  run:
    run_step(STEP_ID, output[0])
