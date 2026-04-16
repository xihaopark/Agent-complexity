configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_primerless_reads"


rule all:
  input:
    "results/finish/filter_primerless_reads.done"


rule run_filter_primerless_reads:
  output:
    "results/finish/filter_primerless_reads.done"
  run:
    run_step(STEP_ID, output[0])
