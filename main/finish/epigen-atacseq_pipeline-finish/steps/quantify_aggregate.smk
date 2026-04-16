configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quantify_aggregate"


rule all:
  input:
    "results/finish/quantify_aggregate.done"


rule run_quantify_aggregate:
  output:
    "results/finish/quantify_aggregate.done"
  run:
    run_step(STEP_ID, output[0])
