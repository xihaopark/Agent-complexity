configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mhc_csv_table"


rule all:
  input:
    "results/finish/mhc_csv_table.done"


rule run_mhc_csv_table:
  output:
    "results/finish/mhc_csv_table.done"
  run:
    run_step(STEP_ID, output[0])
