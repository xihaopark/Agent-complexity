configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methyldackel_mbias_plots"


rule all:
  input:
    "results/finish/methyldackel_mbias_plots.done"


rule run_methyldackel_mbias_plots:
  output:
    "results/finish/methyldackel_mbias_plots.done"
  run:
    run_step(STEP_ID, output[0])
