configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "summary_var"


rule all:
  input:
    "results/finish/summary_var.done"


rule run_summary_var:
  output:
    "results/finish/summary_var.done"
  run:
    run_step(STEP_ID, output[0])
