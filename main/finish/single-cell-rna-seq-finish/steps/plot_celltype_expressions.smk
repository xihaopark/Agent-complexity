configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_celltype_expressions"


rule all:
  input:
    "results/finish/plot_celltype_expressions.done"


rule run_plot_celltype_expressions:
  output:
    "results/finish/plot_celltype_expressions.done"
  run:
    run_step(STEP_ID, output[0])
