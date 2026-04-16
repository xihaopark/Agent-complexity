configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "resolve_comseg"


rule all:
  input:
    "results/finish/resolve_comseg.done"


rule run_resolve_comseg:
  output:
    "results/finish/resolve_comseg.done"
  run:
    run_step(STEP_ID, output[0])
