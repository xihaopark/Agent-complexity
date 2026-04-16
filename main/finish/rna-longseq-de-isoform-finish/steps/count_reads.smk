configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "count_reads"


rule all:
  input:
    "results/finish/count_reads.done"


rule run_count_reads:
  output:
    "results/finish/count_reads.done"
  run:
    run_step(STEP_ID, output[0])
