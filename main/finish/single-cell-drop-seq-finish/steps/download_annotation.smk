configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_annotation"


rule all:
  input:
    "results/finish/download_annotation.done"


rule run_download_annotation:
  output:
    "results/finish/download_annotation.done"
  run:
    run_step(STEP_ID, output[0])
