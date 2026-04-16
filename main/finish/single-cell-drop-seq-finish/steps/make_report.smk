configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_report"


rule all:
  input:
    "results/finish/make_report.done"


rule run_make_report:
  output:
    "results/finish/make_report.done"
  run:
    run_step(STEP_ID, output[0])
