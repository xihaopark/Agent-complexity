configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "circle_bnds"


rule all:
  input:
    "results/finish/circle_bnds.done"


rule run_circle_bnds:
  output:
    "results/finish/circle_bnds.done"
  run:
    run_step(STEP_ID, output[0])
