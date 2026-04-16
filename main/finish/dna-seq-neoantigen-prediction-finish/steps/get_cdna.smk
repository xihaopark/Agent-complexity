configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_cdna"


rule all:
  input:
    "results/finish/get_cdna.done"


rule run_get_cdna:
  output:
    "results/finish/get_cdna.done"
  run:
    run_step(STEP_ID, output[0])
