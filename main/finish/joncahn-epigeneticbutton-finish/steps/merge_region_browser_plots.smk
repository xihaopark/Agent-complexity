configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_region_browser_plots"


rule all:
  input:
    "results/finish/merge_region_browser_plots.done"


rule run_merge_region_browser_plots:
  output:
    "results/finish/merge_region_browser_plots.done"
  run:
    run_step(STEP_ID, output[0])
