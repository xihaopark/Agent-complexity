configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "iso_analysis_report"


rule all:
  input:
    "results/finish/iso_analysis_report.done"


rule run_iso_analysis_report:
  output:
    "results/finish/iso_analysis_report.done"
  run:
    run_step(STEP_ID, output[0])
