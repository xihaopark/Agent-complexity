configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_consensus_reads"


rule all:
  input:
    "results/finish/sort_consensus_reads.done"


rule run_sort_consensus_reads:
  output:
    "results/finish/sort_consensus_reads.done"
  run:
    run_step(STEP_ID, output[0])
