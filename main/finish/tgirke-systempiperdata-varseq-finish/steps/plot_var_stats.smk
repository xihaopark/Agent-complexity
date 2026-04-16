configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_var_stats"


rule all:
  input:
    "results/finish/plot_var_stats.done"


rule run_plot_var_stats:
  output:
    "results/finish/plot_var_stats.done"
  run:
    run_step(STEP_ID, output[0])
