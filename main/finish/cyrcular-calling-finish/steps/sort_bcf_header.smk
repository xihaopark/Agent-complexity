configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_bcf_header"


rule all:
  input:
    "results/finish/sort_bcf_header.done"


rule run_sort_bcf_header:
  output:
    "results/finish/sort_bcf_header.done"
  run:
    run_step(STEP_ID, output[0])
