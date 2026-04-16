configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calling_peaks_macs2_pe"


rule all:
  input:
    "results/finish/calling_peaks_macs2_pe.done"


rule run_calling_peaks_macs2_pe:
  output:
    "results/finish/calling_peaks_macs2_pe.done"
  run:
    run_step(STEP_ID, output[0])
