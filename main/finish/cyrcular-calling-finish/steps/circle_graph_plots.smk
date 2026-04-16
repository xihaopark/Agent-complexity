configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "circle_graph_plots"


rule all:
  input:
    "results/finish/circle_graph_plots.done"


rule run_circle_graph_plots:
  output:
    "results/finish/circle_graph_plots.done"
  run:
    run_step(STEP_ID, output[0])
