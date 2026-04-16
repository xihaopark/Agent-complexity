configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedtools_sort_blacklist"


rule all:
  input:
    "results/finish/bedtools_sort_blacklist.done"


rule run_bedtools_sort_blacklist:
  output:
    "results/finish/bedtools_sort_blacklist.done"
  run:
    run_step(STEP_ID, output[0])
