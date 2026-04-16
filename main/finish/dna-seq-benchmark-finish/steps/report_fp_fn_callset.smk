configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "report_fp_fn_callset"


rule all:
  input:
    "results/finish/report_fp_fn_callset.done"


rule run_report_fp_fn_callset:
  output:
    "results/finish/report_fp_fn_callset.done"
  run:
    run_step(STEP_ID, output[0])
