configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "touch_complete_flag"


rule all:
  input:
    "results/finish/touch_complete_flag.done"


rule run_touch_complete_flag:
  output:
    "results/finish/touch_complete_flag.done"
  run:
    run_step(STEP_ID, output[0])
