configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "best_peaks_pseudoreps"


rule all:
  input:
    "results/finish/best_peaks_pseudoreps.done"


rule run_best_peaks_pseudoreps:
  output:
    "results/finish/best_peaks_pseudoreps.done"
  run:
    run_step(STEP_ID, output[0])
