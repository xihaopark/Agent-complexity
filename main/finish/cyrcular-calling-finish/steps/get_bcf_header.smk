configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_bcf_header"


rule all:
  input:
    "results/finish/get_bcf_header.done"


rule run_get_bcf_header:
  output:
    "results/finish/get_bcf_header.done"
  run:
    run_step(STEP_ID, output[0])
