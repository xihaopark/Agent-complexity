configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reformat_fp_fn_tp_tables"


rule all:
  input:
    "results/finish/reformat_fp_fn_tp_tables.done"


rule run_reformat_fp_fn_tp_tables:
  output:
    "results/finish/reformat_fp_fn_tp_tables.done"
  run:
    run_step(STEP_ID, output[0])
