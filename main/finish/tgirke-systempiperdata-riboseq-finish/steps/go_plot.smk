configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "go_plot"


rule all:
  input:
    "results/finish/go_plot.done"


rule run_go_plot:
  output:
    "results/finish/go_plot.done"
  run:
    run_step(STEP_ID, output[0])
