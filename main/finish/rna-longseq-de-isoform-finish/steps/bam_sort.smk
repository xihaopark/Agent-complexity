configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_sort"


rule all:
  input:
    "results/finish/bam_sort.done"


rule run_bam_sort:
  output:
    "results/finish/bam_sort.done"
  run:
    run_step(STEP_ID, output[0])
