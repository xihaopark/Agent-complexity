configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "microphaser_germline"


rule all:
  input:
    "results/finish/microphaser_germline.done"


rule run_microphaser_germline:
  output:
    "results/finish/microphaser_germline.done"
  run:
    run_step(STEP_ID, output[0])
