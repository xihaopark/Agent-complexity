configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "aggregate_rank_internal"


rule all:
  input:
    "results/finish/aggregate_rank_internal.done"


rule run_aggregate_rank_internal:
  output:
    "results/finish/aggregate_rank_internal.done"
  run:
    run_step(STEP_ID, output[0])
