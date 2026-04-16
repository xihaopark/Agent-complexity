configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ChIPseeker_plots"


rule all:
  input:
    "results/finish/ChIPseeker_plots.done"


rule run_ChIPseeker_plots:
  output:
    "results/finish/ChIPseeker_plots.done"
  run:
    run_step(STEP_ID, output[0])
