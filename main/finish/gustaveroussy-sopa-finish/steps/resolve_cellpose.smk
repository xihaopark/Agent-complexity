configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "resolve_cellpose"


rule all:
  input:
    "results/finish/resolve_cellpose.done"


rule run_resolve_cellpose:
  output:
    "results/finish/resolve_cellpose.done"
  run:
    run_step(STEP_ID, output[0])
