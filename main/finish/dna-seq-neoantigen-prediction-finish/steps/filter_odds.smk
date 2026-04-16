configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_odds"


rule all:
  input:
    "results/finish/filter_odds.done"


rule run_filter_odds:
  output:
    "results/finish/filter_odds.done"
  run:
    run_step(STEP_ID, output[0])
