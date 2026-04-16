configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "count_plot"


rule all:
  input:
    "results/finish/count_plot.done"


rule run_count_plot:
  output:
    "results/finish/count_plot.done"
  run:
    run_step(STEP_ID, output[0])
