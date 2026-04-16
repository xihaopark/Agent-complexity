configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_mc"


rule all:
  input:
    "results/finish/all_mc.done"


rule run_all_mc:
  output:
    "results/finish/all_mc.done"
  run:
    run_step(STEP_ID, output[0])
