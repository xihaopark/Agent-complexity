configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_overview_table"


rule all:
  input:
    "results/finish/filter_overview_table.done"


rule run_filter_overview_table:
  output:
    "results/finish/filter_overview_table.done"
  run:
    run_step(STEP_ID, output[0])
