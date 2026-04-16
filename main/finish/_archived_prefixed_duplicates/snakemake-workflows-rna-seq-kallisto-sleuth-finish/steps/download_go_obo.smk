configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_go_obo"


rule all:
  input:
    "results/finish/download_go_obo.done"


rule run_download_go_obo:
  output:
    "results/finish/download_go_obo.done"
  run:
    run_step(STEP_ID, output[0])
