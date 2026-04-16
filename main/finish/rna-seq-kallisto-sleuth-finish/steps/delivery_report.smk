configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "delivery_report"


rule all:
  input:
    "results/finish/delivery_report.done"


rule run_delivery_report:
  output:
    "results/finish/delivery_report.done"
  run:
    run_step(STEP_ID, output[0])
