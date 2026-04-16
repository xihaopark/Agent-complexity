configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "resolve_baysor"


rule all:
  input:
    "results/finish/resolve_baysor.done"


rule run_resolve_baysor:
  output:
    "results/finish/resolve_baysor.done"
  run:
    run_step(STEP_ID, output[0])
