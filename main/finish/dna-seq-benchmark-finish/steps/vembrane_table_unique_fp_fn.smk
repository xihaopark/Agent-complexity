configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "vembrane_table_unique_fp_fn"


rule all:
  input:
    "results/finish/vembrane_table_unique_fp_fn.done"


rule run_vembrane_table_unique_fp_fn:
  output:
    "results/finish/vembrane_table_unique_fp_fn.done"
  run:
    run_step(STEP_ID, output[0])
