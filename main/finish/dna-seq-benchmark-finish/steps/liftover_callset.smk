configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "liftover_callset"


rule all:
  input:
    "results/finish/liftover_callset.done"


rule run_liftover_callset:
  output:
    "results/finish/liftover_callset.done"
  run:
    run_step(STEP_ID, output[0])
