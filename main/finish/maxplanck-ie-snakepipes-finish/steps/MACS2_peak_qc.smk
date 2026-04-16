configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "MACS2_peak_qc"


rule all:
  input:
    "results/finish/MACS2_peak_qc.done"


rule run_MACS2_peak_qc:
  output:
    "results/finish/MACS2_peak_qc.done"
  run:
    run_step(STEP_ID, output[0])
