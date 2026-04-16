configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_column_from_spreadsheet"


rule all:
  input:
    "results/finish/extract_column_from_spreadsheet.done"


rule run_extract_column_from_spreadsheet:
  output:
    "results/finish/extract_column_from_spreadsheet.done"
  run:
    run_step(STEP_ID, output[0])
