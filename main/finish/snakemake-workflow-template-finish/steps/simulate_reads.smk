configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "simulate_reads"


rule all:
  input:
    "results/finish/simulate_reads.done"


rule run_simulate_reads:
  output:
    "results/finish/simulate_reads.done"
  run:
    run_step(STEP_ID, output[0])
