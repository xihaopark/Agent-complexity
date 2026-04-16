configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_peaks_macs_noref"


rule all:
  input:
    "results/finish/call_peaks_macs_noref.done"


rule run_call_peaks_macs_noref:
  output:
    "results/finish/call_peaks_macs_noref.done"
  run:
    run_step(STEP_ID, output[0])
