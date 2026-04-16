configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reheader_germline"


rule all:
  input:
    "results/finish/reheader_germline.done"


rule run_reheader_germline:
  output:
    "results/finish/reheader_germline.done"
  run:
    run_step(STEP_ID, output[0])
