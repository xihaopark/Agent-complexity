configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "vg2svg"


rule all:
  input:
    "results/finish/vg2svg.done"


rule run_vg2svg:
  output:
    "results/finish/vg2svg.done"
  run:
    run_step(STEP_ID, output[0])
