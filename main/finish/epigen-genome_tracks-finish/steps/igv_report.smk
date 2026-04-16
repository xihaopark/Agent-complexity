configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "igv_report"


rule all:
  input:
    "results/finish/igv_report.done"


rule run_igv_report:
  output:
    "results/finish/igv_report.done"
  run:
    run_step(STEP_ID, output[0])
