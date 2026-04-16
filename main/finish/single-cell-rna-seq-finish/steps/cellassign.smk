configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cellassign"


rule all:
  input:
    "results/finish/cellassign.done"


rule run_cellassign:
  output:
    "results/finish/cellassign.done"
  run:
    run_step(STEP_ID, output[0])
