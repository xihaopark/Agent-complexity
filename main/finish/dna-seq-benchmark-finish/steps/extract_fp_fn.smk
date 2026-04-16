configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_fp_fn"


rule all:
  input:
    "results/finish/extract_fp_fn.done"


rule run_extract_fp_fn:
  output:
    "results/finish/extract_fp_fn.done"
  run:
    run_step(STEP_ID, output[0])
