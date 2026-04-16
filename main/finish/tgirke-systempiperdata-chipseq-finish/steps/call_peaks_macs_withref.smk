configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_peaks_macs_withref"


rule all:
  input:
    "results/finish/call_peaks_macs_withref.done"


rule run_call_peaks_macs_withref:
  output:
    "results/finish/call_peaks_macs_withref.done"
  run:
    run_step(STEP_ID, output[0])
