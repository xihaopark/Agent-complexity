configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotting_peaks_stats_chip_tf"


rule all:
  input:
    "results/finish/plotting_peaks_stats_chip_tf.done"


rule run_plotting_peaks_stats_chip_tf:
  output:
    "results/finish/plotting_peaks_stats_chip_tf.done"
  run:
    run_step(STEP_ID, output[0])
