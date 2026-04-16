configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tsv_to_excel"


rule all:
  input:
    "results/finish/tsv_to_excel.done"


rule run_tsv_to_excel:
  output:
    "results/finish/tsv_to_excel.done"
  run:
    run_step(STEP_ID, output[0])
