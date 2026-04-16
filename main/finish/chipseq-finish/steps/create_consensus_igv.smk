configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_consensus_igv"


rule all:
  input:
    "results/finish/create_consensus_igv.done"


rule run_create_consensus_igv:
  output:
    "results/finish/create_consensus_igv.done"
  run:
    run_step(STEP_ID, output[0])
