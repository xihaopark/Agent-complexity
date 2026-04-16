configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_pfam"


rule all:
  input:
    "results/finish/get_pfam.done"


rule run_get_pfam:
  output:
    "results/finish/get_pfam.done"
  run:
    run_step(STEP_ID, output[0])
