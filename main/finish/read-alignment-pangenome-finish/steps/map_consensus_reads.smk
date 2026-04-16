configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map_consensus_reads"


rule all:
  input:
    "results/finish/map_consensus_reads.done"


rule run_map_consensus_reads:
  output:
    "results/finish/map_consensus_reads.done"
  run:
    run_step(STEP_ID, output[0])
