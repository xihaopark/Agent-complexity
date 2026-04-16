configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calling_peaks_macs2_se"


rule all:
  input:
    "results/finish/calling_peaks_macs2_se.done"


rule run_calling_peaks_macs2_se:
  output:
    "results/finish/calling_peaks_macs2_se.done"
  run:
    run_step(STEP_ID, output[0])
