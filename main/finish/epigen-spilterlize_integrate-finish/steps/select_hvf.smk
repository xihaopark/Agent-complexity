configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "select_hvf"


rule all:
  input:
    "results/finish/select_hvf.done"


rule run_select_hvf:
  output:
    "results/finish/select_hvf.done"
  run:
    run_step(STEP_ID, output[0])
