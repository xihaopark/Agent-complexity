configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "circle_coverage_plot"


rule all:
  input:
    "results/finish/circle_coverage_plot.done"


rule run_circle_coverage_plot:
  output:
    "results/finish/circle_coverage_plot.done"
  run:
    run_step(STEP_ID, output[0])
