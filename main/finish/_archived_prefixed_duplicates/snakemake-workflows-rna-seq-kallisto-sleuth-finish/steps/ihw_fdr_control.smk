configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ihw_fdr_control"


rule all:
  input:
    "results/finish/ihw_fdr_control.done"


rule run_ihw_fdr_control:
  output:
    "results/finish/ihw_fdr_control.done"
  run:
    run_step(STEP_ID, output[0])
