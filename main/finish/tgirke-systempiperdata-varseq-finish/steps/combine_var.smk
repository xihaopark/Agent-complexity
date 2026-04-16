configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "combine_var"


rule all:
  input:
    "results/finish/combine_var.done"


rule run_combine_var:
  output:
    "results/finish/combine_var.done"
  run:
    run_step(STEP_ID, output[0])
