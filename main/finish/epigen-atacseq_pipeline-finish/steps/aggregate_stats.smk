configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "aggregate_stats"


rule all:
  input:
    "results/finish/aggregate_stats.done"


rule run_aggregate_stats:
  output:
    "results/finish/aggregate_stats.done"
  run:
    run_step(STEP_ID, output[0])
