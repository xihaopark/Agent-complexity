configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "msisensor_pro_scan"


rule all:
  input:
    "results/finish/msisensor_pro_scan.done"


rule run_msisensor_pro_scan:
  output:
    "results/finish/msisensor_pro_scan.done"
  run:
    run_step(STEP_ID, output[0])
