configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_samtools_sort"


rule all:
  input:
    "results/finish/kallisto_samtools_sort.done"


rule run_kallisto_samtools_sort:
  output:
    "results/finish/kallisto_samtools_sort.done"
  run:
    run_step(STEP_ID, output[0])
