configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "report"


rule all:
  input:
    "results/finish/report.done"


rule run_report:
  output:
    "results/finish/report.done"
  run:
    run_step(STEP_ID, output[0])
