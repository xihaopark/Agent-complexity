configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "peaks_count"


rule all:
  input:
    "results/finish/peaks_count.done"


rule run_peaks_count:
  output:
    "results/finish/peaks_count.done"
  run:
    run_step(STEP_ID, output[0])
