configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_diffexp_pval_hist"


rule all:
  input:
    "results/finish/plot_diffexp_pval_hist.done"


rule run_plot_diffexp_pval_hist:
  output:
    "results/finish/plot_diffexp_pval_hist.done"
  run:
    run_step(STEP_ID, output[0])
