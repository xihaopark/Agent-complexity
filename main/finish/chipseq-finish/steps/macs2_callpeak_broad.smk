configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "macs2_callpeak_broad"


rule all:
  input:
    "results/finish/macs2_callpeak_broad.done"


rule run_macs2_callpeak_broad:
  output:
    "results/finish/macs2_callpeak_broad.done"
  run:
    run_step(STEP_ID, output[0])
