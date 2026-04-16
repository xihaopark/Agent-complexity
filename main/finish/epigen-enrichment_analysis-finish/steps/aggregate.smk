configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "aggregate"


rule all:
  input:
    "results/finish/aggregate.done"


rule run_aggregate:
  output:
    "results/finish/aggregate.done"
  run:
    run_step(STEP_ID, output[0])
