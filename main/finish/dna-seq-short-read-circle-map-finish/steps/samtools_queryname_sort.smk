configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_queryname_sort"


rule all:
  input:
    "results/finish/samtools_queryname_sort.done"


rule run_samtools_queryname_sort:
  output:
    "results/finish/samtools_queryname_sort.done"
  run:
    run_step(STEP_ID, output[0])
