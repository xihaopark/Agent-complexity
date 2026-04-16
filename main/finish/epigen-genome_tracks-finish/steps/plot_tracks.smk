configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_tracks"


rule all:
  input:
    "results/finish/plot_tracks.done"


rule run_plot_tracks:
  output:
    "results/finish/plot_tracks.done"
  run:
    run_step(STEP_ID, output[0])
