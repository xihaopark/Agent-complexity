configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_fp_fn_tp"


rule all:
  input:
    "results/finish/extract_fp_fn_tp.done"


rule run_extract_fp_fn_tp:
  output:
    "results/finish/extract_fp_fn_tp.done"
  run:
    run_step(STEP_ID, output[0])
