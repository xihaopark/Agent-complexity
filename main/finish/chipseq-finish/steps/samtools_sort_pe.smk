configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_sort_pe"


rule all:
  input:
    "results/finish/samtools_sort_pe.done"


rule run_samtools_sort_pe:
  output:
    "results/finish/samtools_sort_pe.done"
  run:
    run_step(STEP_ID, output[0])
