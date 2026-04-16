configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "vega_volcano_plot"


rule all:
  input:
    "results/finish/vega_volcano_plot.done"


rule run_vega_volcano_plot:
  output:
    "results/finish/vega_volcano_plot.done"
  run:
    run_step(STEP_ID, output[0])
