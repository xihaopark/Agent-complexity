configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "msisensor_pro_msi"


rule all:
  input:
    "results/finish/msisensor_pro_msi.done"


rule run_msisensor_pro_msi:
  output:
    "results/finish/msisensor_pro_msi.done"
  run:
    run_step(STEP_ID, output[0])
