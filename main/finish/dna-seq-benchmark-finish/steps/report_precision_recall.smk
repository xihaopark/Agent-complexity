configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "report_precision_recall"


rule all:
  input:
    "results/finish/report_precision_recall.done"


rule run_report_precision_recall:
  output:
    "results/finish/report_precision_recall.done"
  run:
    run_step(STEP_ID, output[0])
