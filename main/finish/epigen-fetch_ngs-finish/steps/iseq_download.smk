configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "iseq_download"


rule all:
  input:
    "results/finish/iseq_download.done"


rule run_iseq_download:
  output:
    "results/finish/iseq_download.done"
  run:
    run_step(STEP_ID, output[0])
