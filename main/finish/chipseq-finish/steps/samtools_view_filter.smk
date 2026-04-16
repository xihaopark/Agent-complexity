configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_view_filter"


rule all:
  input:
    "results/finish/samtools_view_filter.done"


rule run_samtools_view_filter:
  output:
    "results/finish/samtools_view_filter.done"
  run:
    run_step(STEP_ID, output[0])
