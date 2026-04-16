configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map_consensus_tss"


rule all:
  input:
    "results/finish/map_consensus_tss.done"


rule run_map_consensus_tss:
  output:
    "results/finish/map_consensus_tss.done"
  run:
    run_step(STEP_ID, output[0])
