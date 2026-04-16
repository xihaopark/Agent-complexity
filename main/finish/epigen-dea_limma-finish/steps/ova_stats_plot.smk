configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ova_stats_plot"


rule all:
  input:
    "results/finish/ova_stats_plot.done"


rule run_ova_stats_plot:
  output:
    "results/finish/ova_stats_plot.done"
  run:
    run_step(STEP_ID, output[0])
