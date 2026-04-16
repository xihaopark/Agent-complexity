configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "macs2_callpeak_narrow"


rule all:
  input:
    "results/finish/macs2_callpeak_narrow.done"


rule run_macs2_callpeak_narrow:
  output:
    "results/finish/macs2_callpeak_narrow.done"
  run:
    run_step(STEP_ID, output[0])
