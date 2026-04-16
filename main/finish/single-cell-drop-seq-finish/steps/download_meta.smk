configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_meta"


rule all:
  input:
    "results/finish/download_meta.done"


rule run_download_meta:
  output:
    "results/finish/download_meta.done"
  run:
    run_step(STEP_ID, output[0])
