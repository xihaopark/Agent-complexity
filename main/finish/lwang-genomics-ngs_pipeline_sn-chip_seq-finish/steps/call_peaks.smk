configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_peaks"


rule all:
  input:
    "results/finish/call_peaks.done"


rule run_call_peaks:
  output:
    "results/finish/call_peaks.done"
  run:
    run_step(STEP_ID, output[0])
