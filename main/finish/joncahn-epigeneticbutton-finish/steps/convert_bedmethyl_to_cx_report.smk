configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "convert_bedmethyl_to_cx_report"


rule all:
  input:
    "results/finish/convert_bedmethyl_to_cx_report.done"


rule run_convert_bedmethyl_to_cx_report:
  output:
    "results/finish/convert_bedmethyl_to_cx_report.done"
  run:
    run_step(STEP_ID, output[0])
