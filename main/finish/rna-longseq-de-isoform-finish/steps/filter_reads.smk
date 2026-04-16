configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_reads"


rule all:
  input:
    "results/finish/filter_reads.done"


rule run_filter_reads:
  output:
    "results/finish/filter_reads.done"
  run:
    run_step(STEP_ID, output[0])
