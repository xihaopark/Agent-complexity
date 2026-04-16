configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "msisensor_pro_pro_run"


rule all:
  input:
    "results/finish/msisensor_pro_pro_run.done"


rule run_msisensor_pro_pro_run:
  output:
    "results/finish/msisensor_pro_pro_run.done"
  run:
    run_step(STEP_ID, output[0])
