configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_consensus_saf"


rule all:
  input:
    "results/finish/create_consensus_saf.done"


rule run_create_consensus_saf:
  output:
    "results/finish/create_consensus_saf.done"
  run:
    run_step(STEP_ID, output[0])
