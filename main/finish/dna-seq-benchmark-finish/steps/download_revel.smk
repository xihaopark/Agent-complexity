configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_revel"


rule all:
  input:
    "results/finish/download_revel.done"


rule run_download_revel:
  output:
    "results/finish/download_revel.done"
  run:
    run_step(STEP_ID, output[0])
