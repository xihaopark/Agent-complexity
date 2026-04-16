configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_consensus_reads"


rule all:
  input:
    "results/finish/merge_consensus_reads.done"


rule run_merge_consensus_reads:
  output:
    "results/finish/merge_consensus_reads.done"
  run:
    run_step(STEP_ID, output[0])
