configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calling_peaks_atac"


rule all:
  input:
    "results/finish/calling_peaks_atac.done"


rule run_calling_peaks_atac:
  output:
    "results/finish/calling_peaks_atac.done"
  run:
    run_step(STEP_ID, output[0])
