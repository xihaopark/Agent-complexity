configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bcftools_sort"


rule all:
  input:
    "results/finish/bcftools_sort.done"


rule run_bcftools_sort:
  output:
    "results/finish/bcftools_sort.done"
  run:
    run_step(STEP_ID, output[0])
