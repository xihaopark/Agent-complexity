configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepping_chip_peak_stats"


rule all:
  input:
    "results/finish/prepping_chip_peak_stats.done"


rule run_prepping_chip_peak_stats:
  output:
    "results/finish/prepping_chip_peak_stats.done"
  run:
    run_step(STEP_ID, output[0])
