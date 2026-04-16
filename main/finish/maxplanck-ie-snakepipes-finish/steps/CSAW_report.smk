configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "CSAW_report"


rule all:
  input:
    "results/finish/CSAW_report.done"


rule run_CSAW_report:
  output:
    "results/finish/CSAW_report.done"
  run:
    run_step(STEP_ID, output[0])
