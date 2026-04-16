configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "report_fp_fn"


rule all:
  input:
    "results/finish/report_fp_fn.done"


rule run_report_fp_fn:
  output:
    "results/finish/report_fp_fn.done"
  run:
    run_step(STEP_ID, output[0])
