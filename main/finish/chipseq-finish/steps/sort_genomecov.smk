configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_genomecov"


rule all:
  input:
    "results/finish/sort_genomecov.done"


rule run_sort_genomecov:
  output:
    "results/finish/sort_genomecov.done"
  run:
    run_step(STEP_ID, output[0])
