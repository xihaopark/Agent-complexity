configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_consensus_bed"


rule all:
  input:
    "results/finish/create_consensus_bed.done"


rule run_create_consensus_bed:
  output:
    "results/finish/create_consensus_bed.done"
  run:
    run_step(STEP_ID, output[0])
