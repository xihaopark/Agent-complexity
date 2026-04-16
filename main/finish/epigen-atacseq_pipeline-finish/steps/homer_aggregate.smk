configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "homer_aggregate"


rule all:
  input:
    "results/finish/homer_aggregate.done"


rule run_homer_aggregate:
  output:
    "results/finish/homer_aggregate.done"
  run:
    run_step(STEP_ID, output[0])
