configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calc_consensus_reads"


rule all:
  input:
    "results/finish/calc_consensus_reads.done"


rule run_calc_consensus_reads:
  output:
    "results/finish/calc_consensus_reads.done"
  run:
    run_step(STEP_ID, output[0])
