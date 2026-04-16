configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "msisensor_pro_baseline"


rule all:
  input:
    "results/finish/msisensor_pro_baseline.done"


rule run_msisensor_pro_baseline:
  output:
    "results/finish/msisensor_pro_baseline.done"
  run:
    run_step(STEP_ID, output[0])
