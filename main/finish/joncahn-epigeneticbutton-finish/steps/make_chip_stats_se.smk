configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_chip_stats_se"


rule all:
  input:
    "results/finish/make_chip_stats_se.done"


rule run_make_chip_stats_se:
  output:
    "results/finish/make_chip_stats_se.done"
  run:
    run_step(STEP_ID, output[0])
