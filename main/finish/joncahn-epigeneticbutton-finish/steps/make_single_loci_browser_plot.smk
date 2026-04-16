configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_single_loci_browser_plot"


rule all:
  input:
    "results/finish/make_single_loci_browser_plot.done"


rule run_make_single_loci_browser_plot:
  output:
    "results/finish/make_single_loci_browser_plot.done"
  run:
    run_step(STEP_ID, output[0])
